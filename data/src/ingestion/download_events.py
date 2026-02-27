import json
from pathlib import Path
import requests


BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events"
MATCH_IDS_PATH = Path("data/processed/match_ids.json")
OUT_DIR = Path("data/raw/events")


def load_match_ids(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8") as f:
        ids = json.load(f)
    return [int(x) for x in ids]


def approx_dir_size_mb(folder: Path) -> float:
    if not folder.exists():
        return 0.0
    total = 0
    for p in folder.rglob("*"):
        if p.is_file():
            total += p.stat().st_size #chiedo il dettaglio del file con .stat() e .st_size prendo il BYTE
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


def main(n_matches: int = 20, max_total_mb: float = 300.0):

    if not MATCH_IDS_PATH.exists():
        raise FileNotFoundError(f"Non trovo {MATCH_IDS_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    match_ids = load_match_ids(MATCH_IDS_PATH)

    skipped = 0
    downloaded = 0

    print(f"Match totali disponibili: {len(match_ids)}")
    print(f"Richiesti: {n_matches}")
    print(f"Quota massima disco: {max_total_mb} MB")
    print(f"Dimensione iniziale cartella: {approx_dir_size_mb(OUT_DIR):.1f} MB\n")

    for mid in match_ids:

        # Stop per numero match
        if downloaded >= n_matches:
            print(f"\n[STOP] Raggiunto limite match richiesti: {n_matches}")
            break

        # Stop per spazio disco
        size_mb = approx_dir_size_mb(OUT_DIR)
        if size_mb >= max_total_mb:
            print(f"\n[STOP] Raggiunta quota disco {size_mb:.1f} MB")
            break

        did_download = download_event(mid, OUT_DIR)

        if did_download:
            downloaded += 1
        else:
            skipped += 1

        if downloaded % 5 == 0:
            print(f"Downloaded={downloaded} | Size={approx_dir_size_mb(OUT_DIR):.1f} MB")

    print(f"\nFINE: downloaded={downloaded}, skipped={skipped}, size={approx_dir_size_mb(OUT_DIR):.1f} MB")


if __name__ == "__main__":
    # CAMBIA QUI se vuoi variare il dataset
    main(limit=20, max_total_mb=300.0)