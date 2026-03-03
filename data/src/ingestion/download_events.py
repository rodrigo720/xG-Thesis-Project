import json
from pathlib import Path
import requests

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"


def load_match_ids_wc2022(matches_file: Path) -> list[int]:
    with matches_file.open("r", encoding="utf-8") as f:
        matches = json.load(f)

    match_ids = [m["match_id"] for m in matches]
    return match_ids


def download_event(match_id: int, out_dir: Path) -> Path:
    out_path = out_dir / f"{match_id}.json"
    if out_path.exists():
        return out_path

    url = f"{BASE_URL}/events/{match_id}.json"
    r = requests.get(url, timeout=30)

    if r.status_code != 200:
        raise RuntimeError(f"Download fallito: HTTP {r.status_code} per url {url}")

    out_path.write_text(r.text, encoding="utf-8")
    return out_path


if __name__ == "__main__":

    events_dir = Path("data/raw/events")
    events_dir.mkdir(parents=True, exist_ok=True)

    matches_file = Path("data/raw/matches/43_106.json")  # WC2022
    if not matches_file.exists():
        raise FileNotFoundError(f"Non trovo il file: {matches_file}")

    match_ids = load_match_ids_wc2022(matches_file)
    print(f"Trovati {len(match_ids)} match_id (WC2022).")

    downloaded = 0
    skipped = 0

    for i, match_id in enumerate(match_ids, start=1):
        out_path = events_dir / f"{match_id}.json"

        if out_path.exists():
            skipped += 1
        else:
            download_event(match_id, events_dir)
            downloaded += 1

        if i % 10 == 0 or i == len(match_ids):
            print(f"Progress: {i}/{len(match_ids)} | downloaded={downloaded} skipped={skipped}")

    print(f"\nFINE: downloaded={downloaded}, skipped={skipped}")
    print(f"Events dir: {events_dir.resolve()}")