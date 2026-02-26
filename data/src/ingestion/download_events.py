import json
from pathlib import Path
import requests


BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events"
MATCH_IDS_PATH = Path("data/processed/match_ids.json")
OUT_DIR = Path("data/raw/events")


def load_match_ids(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8") as f:
        ids = json.load(f)
    # assicurati siano int
    return [int(x) for x in ids]


def approx_dir_size_mb(folder: Path) -> float:
    if not folder.exists():
        return 0.0
    total = 0
    for p in folder.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total / (1024 * 1024)


def download_event(match_id: int, out_dir: Path) -> bool:
    """
    Ritorna True se scarica e salva.
    Ritorna False se skippa (già presente).
    Lancia eccezione solo per errori imprevisti.
    """
    out_path = out_dir / f"{match_id}.json"
    if out_path.exists():
        return False

    url = f"{BASE_URL}/{match_id}.json"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        print(f"[WARN] {match_id}: HTTP {r.status_code} ({url})")
        return False

    out_path.write_text(r.text, encoding="utf-8")
    return True


def main(limit: int = 20, max_total_mb: float = 300.0):
    """
    limit: quanti match scaricare (per partire leggero)
    max_total_mb: stop se la cartella supera questa dimensione
    """
    if not MATCH_IDS_PATH.exists():
        raise FileNotFoundError(f"Non trovo {MATCH_IDS_PATH}. Hai già generato match_ids.json?")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    match_ids = load_match_ids(MATCH_IDS_PATH)

    # Scarica solo un campione iniziale (limit)
    match_ids = match_ids[:limit]

    skipped = 0
    downloaded = 0

    print(f"Match in input: {len(match_ids)} | cartella events attuale: {approx_dir_size_mb(OUT_DIR):.1f} MB")
    print(f"Limite download: {limit} match | Quota massima cartella: {max_total_mb} MB\n")

    for i, mid in enumerate(match_ids, start=1):

        # quota check
        size_mb = approx_dir_size_mb(OUT_DIR)
        if size_mb >= max_total_mb:
            print(f"\n[STOP] Raggiunta quota {size_mb:.1f} MB (limite {max_total_mb} MB).")
            break

        did_download = download_event(mid, OUT_DIR)
        if did_download:
            downloaded += 1
        else:
            skipped += 1

        if i % 5 == 0 or i == len(match_ids):
            print(f"Progress: {i}/{len(match_ids)} | downloaded={downloaded} skipped={skipped} | size={approx_dir_size_mb(OUT_DIR):.1f} MB")

    print(f"\nFINE: downloaded={downloaded}, skipped={skipped}, size={approx_dir_size_mb(OUT_DIR):.1f} MB")
    print(f"Output dir: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    # CAMBIA QUI se vuoi variare il dataset
    main(limit=20, max_total_mb=300.0)