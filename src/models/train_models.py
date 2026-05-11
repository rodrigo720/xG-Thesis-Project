import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import (
    precision_recall_curve,
    PrecisionRecallDisplay,
    ConfusionMatrixDisplay,
    confusion_matrix
)
from sklearn.calibration import CalibrationDisplay

from src.models.preprocessing import clean_dataset, get_feature_columns
from src.models.model_builders import build_model
from src.models.evaluation import cross_validate_models, evaluate_probabilities

import warnings

#per migliorare la versione di scikitlearn
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


DATA_PATH = "data/processed/shots_model_ready_wc2022.csv"

RESULTS_DIR = "reports/model_results"
FIGURES_DIR = "reports/figures"

RANDOM_STATE = 42


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    #print("COLONNE PRIMA DEL CLEAN:")
    #print(df.columns.tolist())

    df = clean_dataset(df)

    #print("COLONNE DOPO IL CLEAN:")
    #print(df.columns.tolist())

    numeric_features, categorical_features = get_feature_columns()
    feature_columns = numeric_features + categorical_features

    #print("FEATURE RICHIESTE:")
    #print(feature_columns)

    missing_cols = [col for col in feature_columns if col not in df.columns]
    #print("COLONNE MANCANTI:")
    #print(missing_cols)

    if missing_cols:
        raise ValueError(f"Colonne mancanti nel dataset: {missing_cols}")

    target = "goal"

    X = df[feature_columns]
    y = df[target]

    statsbomb_xg = df["shot.statsbomb_xg"]

    X_train, X_test, y_train, y_test, sb_xg_train, sb_xg_test = train_test_split(
        X,
        y,
        statsbomb_xg,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    models = build_model(random_state=RANDOM_STATE)

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    cv_results = cross_validate_models(models, X_train, y_train, cv)
    cv_results.to_csv(
        f"{RESULTS_DIR}/cv_results_wc2022.csv",
        index=False
    )

    best_model_name = cv_results.iloc[0]["model"]
    best_model = models[best_model_name]

    print("CV results:")
    print(cv_results)
    print(f"\nBest model: {best_model_name}")

    best_model.fit(X_train, y_train)

    y_proba = best_model.predict_proba(X_test)[:, 1]
    y_pred = best_model.predict(X_test)

    predictions_df = X_test.copy()

    predictions_df["goal"] = y_test.values
    predictions_df["model_xg"] = y_proba
    predictions_df["statsbomb_xg"] = sb_xg_test.values

    predictions_df.to_csv(
        f"{RESULTS_DIR}/test_predictions_wc2022.csv",
        index = False
    )


    test_metrics = []

    test_metrics.append(
        evaluate_probabilities(
            y_true=y_test,
            y_proba=y_proba,
            model_name=best_model_name
        )
    )

    test_metrics.append(
        evaluate_probabilities(
            y_true=y_test,
            y_proba=sb_xg_test,
            model_name="statsbomb_xg"
        )
    )

    test_metrics_df = pd.DataFrame(test_metrics)
    test_metrics_df.to_csv(
        f"{RESULTS_DIR}/test_metrics_wc2022.csv",
        index=False
    )

    print("\nTest metrics:")
    print(test_metrics_df)

    PrecisionRecallDisplay.from_predictions(
        y_test,
        y_proba,
        name=best_model_name
    )
    PrecisionRecallDisplay.from_predictions(
        y_test,
        sb_xg_test,
        name="StatsBomb xG"
    )
    plt.title("Precision-Recall Curve - WC 2022")
    plt.savefig(f"{FIGURES_DIR}/pr_curve_wc2022.png", dpi=300, bbox_inches="tight")
    plt.close()

    CalibrationDisplay.from_predictions(
        y_test,
        y_proba,
        name=best_model_name,
        n_bins=10
    )
    CalibrationDisplay.from_predictions(
        y_test,
        sb_xg_test,
        name="StatsBomb xG",
        n_bins=10
    )
    plt.title("Calibration Curve - WC 2022")
    plt.savefig(f"{FIGURES_DIR}/calibration_curve_wc2022.png", dpi=300, bbox_inches="tight")
    plt.close()

    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm).plot()
    plt.title(f"Confusion Matrix - {best_model_name}")
    plt.savefig(f"{FIGURES_DIR}/confusion_matrix_wc2022.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()