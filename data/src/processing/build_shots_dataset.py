import json
from pathlib import Path

import pandas as pd


EVENTS_DIR = Path("data/raw/events")
OUT_PATH = Path("data/processed/shots_sample.csv")


def load_events_file(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as f:
        events = json.load(f)
    return pd.json_normalize(events)


def main():
    if not EVENTS_DIR.exists():
        raise FileNotFoundError(f"Non trovo {EVENTS_DIR}. Hai già scaricato gli events?")

    event_files = list(EVENTS_DIR.glob("*.json"))
    if len(event_files) == 0:
        raise FileNotFoundError(f"Nessun file in {EVENTS_DIR}.")

    shots_dfs = []
    for p in event_files:
        df = load_events_file(p)

        # filtro shot
        if "type.name" not in df.columns:
            print(f"[WARN] {p.name}: manca 'type.name', skip")
            continue

        shots = df[df["type.name"] == "Shot"].copy()
        shots_dfs.append(shots)

    if len(shots_dfs) == 0:
        raise RuntimeError("Non ho trovato nessun evento Shot nei file events.")

    shots_all = pd.concat(shots_dfs, ignore_index=True)

    # Esclusione rigori (se possibile)
    # In StatsBomb di solito: shot.type.name == "Penalty"
    if "shot.type.name" in shots_all.columns:
        shots_all = shots_all[shots_all["shot.type.name"] != "Penalty"].copy()

    # Salvataggio
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shots_all.to_csv(OUT_PATH, index=False)

    # Report per il prof
    print("\n=== SHOTS DATASET (sample) ===")
    print(f"Event files letti: {len(event_files)}")
    print(f"Righe (tiri): {len(shots_all)}")
    print(f"Colonne: {shots_all.shape[1]}")

    print("\nPrime 30 colonne:")
    print(list(shots_all.columns[:30]))

    # Missingness (top 20)
    missing_pct = (shots_all.isna().mean() * 100).sort_values(ascending=False)
    print("\nTop 20 colonne per missing %:")
    print(missing_pct.head(20).round(2))

    print(f"\nSalvato: {OUT_PATH.resolve()}")


if __name__ == "__main__":
    main()