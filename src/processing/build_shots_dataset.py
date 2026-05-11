import json
from pathlib import Path

import pandas as pd


MATCHES_FILE = Path("data/raw/matches/43_106.json")          # WC2022 matches
EVENTS_DIR = Path("data/raw/events")                        # events per match_id
OUT_PATH = Path("data/processed/shots_raw_full_wc2022.csv") # output


def load_matches_index(matches_file: Path) -> pd.DataFrame:
    """
    Ritorna un dataframe con almeno:
    match_id, home_team, away_team, match_date (se disponibile)
    """
    with matches_file.open("r", encoding="utf-8") as f:
        matches = json.load(f)

    df = pd.json_normalize(matches)

    # colonne attese nei matches StatsBomb
    # home_team.home_team_name / away_team.away_team_name a volte sono nested;

    possible_home = [c for c in df.columns if c in ("home_team.home_team_name", "home_team.name")]
    possible_away = [c for c in df.columns if c in ("away_team.away_team_name", "away_team.name")]
    possible_date = [c for c in df.columns if c in ("match_date",)]

    if "match_id" not in df.columns:
        raise KeyError("Nel file matches manca la colonna 'match_id'.")

    home_col = possible_home[0] if possible_home else None
    away_col = possible_away[0] if possible_away else None
    date_col = possible_date[0] if possible_date else None

    out = pd.DataFrame({"match_id": df["match_id"]})

    if home_col:
        out["home_team"] = df[home_col]
    else:
        out["home_team"] = pd.NA

    if away_col:
        out["away_team"] = df[away_col]
    else:
        out["away_team"] = pd.NA

    if date_col:
        out["match_date"] = df[date_col]
    else:
        out["match_date"] = pd.NA

    return out


def load_events_df(events_path: Path) -> pd.DataFrame:
    with events_path.open("r", encoding="utf-8") as f:
        events = json.load(f)
    return pd.json_normalize(events)


def main():
    if not MATCHES_FILE.exists():
        raise FileNotFoundError(f"Non trovo: {MATCHES_FILE}")

    if not EVENTS_DIR.exists():
        raise FileNotFoundError(f"Non trovo la cartella events: {EVENTS_DIR}")

    matches_idx = load_matches_index(MATCHES_FILE)
    match_ids = matches_idx["match_id"].tolist()

    print(f"Match in WC2022 (da matches file): {len(match_ids)}")

    shots_list = []
    missing_events_files = 0

    for i, match_id in enumerate(match_ids, start=1):
        ev_path = EVENTS_DIR / f"{match_id}.json"

        if not ev_path.exists():
            missing_events_files += 1
            print(f"[WARN] manca events file: {ev_path.name}")
            continue

        df = load_events_df(ev_path)

        if "type.name" not in df.columns:
            print(f"[WARN] {ev_path.name}: manca 'type.name', skip")
            continue

        shots = df[df["type.name"] == "Shot"].copy()

        # aggiungo match_id se non presente (di solito c'è)
        if "match_id" not in shots.columns:
            shots["match_id"] = match_id

        shots_list.append(shots)

        if i % 10 == 0 or i == len(match_ids):
            print(f"Progress: {i}/{len(match_ids)}")

    if missing_events_files > 0:
        print(f"\n[INFO] File events mancanti: {missing_events_files} (questi match saranno esclusi)")

    if len(shots_list) == 0:
        raise RuntimeError("Non ho trovato nessun evento Shot. Controlla gli events scaricati.")

    shots_all = pd.concat(shots_list, ignore_index=True)

    # Escludo rigori 
    if "shot.type.name" in shots_all.columns:
        shots_all = shots_all[shots_all["shot.type.name"] != "Penalty"].copy()

    # Merge con home/away dal matches index

    shots_all = shots_all.merge(matches_idx, on="match_id", how="left")

    # team che effettua il tiro
    team_col = "team.name" if "team.name" in shots_all.columns else None
    if team_col:
        shots_all["is_home"] = (shots_all[team_col] == shots_all["home_team"]).astype("Int64")
    else:
        shots_all["is_home"] = pd.NA

    # Salvataggio
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shots_all.to_csv(OUT_PATH, index=False)

    # Report
    print("\n=== SHOTS RAW FULL (WC2022) ===")
    print(f"Righe (tiri, penalty esclusi): {len(shots_all)}")
    print(f"Colonne: {shots_all.shape[1]}")

    print("\nPrime 30 colonne:")
    print(list(shots_all.columns[:30]))

    missing_pct = (shots_all.isna().mean() * 100).sort_values(ascending=False)
    print("\nTop 20 colonne per missing %:")
    print(missing_pct.head(20).round(2))

    print(f"\nSalvato: {OUT_PATH.resolve()}")


if __name__ == "__main__":
    main()