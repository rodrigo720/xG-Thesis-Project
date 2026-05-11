import pandas as pd
import numpy as np
from pathlib import Path


INPUT_PATH = Path("data/processed/shots_raw_full_wc2022.csv")
OUTPUT_PATH = Path("data/processed/shots_model_ready_wc2022.csv")


def calculate_distance(x, y):

    goal_x = 120
    goal_y = 40

    return np.sqrt((goal_x - x) ** 2 + (goal_y - y) ** 2)


def calculate_angle(x, y):

    goal_width = 7.32
    goal_x = 120

    left_post_y = 40 + goal_width / 2
    right_post_y = 40 - goal_width / 2

    angle = np.arctan2(left_post_y - y, goal_x - x) - np.arctan2(
        right_post_y - y, goal_x - x
    )

    return np.abs(angle)


if __name__ == "__main__":

    df = pd.read_csv(INPUT_PATH)

    # target variable 
    df["goal"] = (df["shot.outcome.name"] == "Goal").astype(int)

    # estrazione coordinate
    coords = df["location"].str.strip("[]").str.split(",", expand=True)

    df["x"] = coords[0].astype(float)
    df["y"] = coords[1].astype(float)

    # feature engineering
    df["distance"] = calculate_distance(df["x"], df["y"])
    df["angle"] = calculate_angle(df["x"], df["y"])


    # selezione colonne utili
    columns = [
        "match_id",
        "team.name",
        "minute",
        "possession",
        "play_pattern.name",
        "position.name",
        "under_pressure",
        "shot.type.name",
        "shot.technique.name",
        "shot.body_part.name",
        "x",
        "y",
        "distance",
        "angle",
        "goal",
        "shot.statsbomb_xg",
    ]

    model_df = df[columns].copy()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    model_df.to_csv(OUTPUT_PATH, index=False)

    print("Dataset per modello creato")
    print(f"Righe: {len(model_df)}")
    print(f"Colonne: {len(model_df.columns)}")