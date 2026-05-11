import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = "reports/model_results"
FIGURES_DIR = "reports/figures"

PREDICTIONS_PATH = f"{RESULTS_DIR}/test_predictions_wc2022.csv"
DATA_PATH = "data/processed/shots_model_ready_wc2022.csv"


def plot_model_vs_statsbomb():
    df = pd.read_csv(PREDICTIONS_PATH)

    corr = df["model_xg"].corr(df["statsbomb_xg"])

    corr_df = pd.DataFrame({
        "comparison": ["model_xg_vs_statsbomb_xg"],
        "pearson_correlation": [corr]
    })

    corr_df.to_csv(
        f"{RESULTS_DIR}/model_statsbomb_correlation.csv",
        index=False
    )

    plt.figure(figsize=(7, 5))
    plt.scatter(df["statsbomb_xg"], df["model_xg"], alpha=0.6)
    plt.xlabel("StatsBomb xG")
    plt.ylabel("Model predicted xG")
    plt.title(f"Correlation between Model xG and StatsBomb xG\nPearson r = {corr:.3f}")
    plt.grid(True)
    plt.savefig(
        f"{FIGURES_DIR}/model_vs_statsbomb_correlation.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


def plot_numeric_feature_correlation():
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "x": "location_x",
        "y": "location_y"
    })

    numeric_features = [
        "minute",
        "possession",
        "location_x",
        "location_y",
        "distance",
        "angle"
    ]

    corr_matrix = df[numeric_features].corr()

    corr_matrix.to_csv(
        f"{RESULTS_DIR}/numeric_features_correlation_matrix.csv"
    )

    plt.figure(figsize=(8, 6))
    plt.imshow(corr_matrix, aspect="auto")
    plt.colorbar(label="Pearson correlation")
    plt.xticks(range(len(numeric_features)), numeric_features, rotation=45, ha="right")
    plt.yticks(range(len(numeric_features)), numeric_features)
    plt.title("Correlation Matrix of Numerical Features")

    for i in range(len(numeric_features)):
        for j in range(len(numeric_features)):
            plt.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha="center", va="center")

    plt.tight_layout()
    plt.savefig(
        f"{FIGURES_DIR}/numeric_features_correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    plot_model_vs_statsbomb()
    plot_numeric_feature_correlation()

    print("Interpretation figures saved correctly.")


if __name__ == "__main__":
    main()