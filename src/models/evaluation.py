import pandas as pd

from sklearn.model_selection import cross_validate
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    brier_score_loss
)


def cross_validate_models(models, X_train, y_train, cv):
    results = []

    scoring = {
        "pr_auc": "average_precision",
        "roc_auc": "roc_auc"
    }

    for name, model in models.items():
        scores = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )

        results.append({
            "model": name,
            "mean_pr_auc": scores["test_pr_auc"].mean(),
            "std_pr_auc": scores["test_pr_auc"].std(),
            "mean_roc_auc": scores["test_roc_auc"].mean(),
            "std_roc_auc": scores["test_roc_auc"].std()
        })

    return pd.DataFrame(results).sort_values(
        by="mean_pr_auc",
        ascending=False
    )


def evaluate_probabilities(y_true, y_proba, model_name):
    return {
        "model": model_name,
        "pr_auc": average_precision_score(y_true, y_proba),
        "roc_auc": roc_auc_score(y_true, y_proba),
        "brier_score": brier_score_loss(y_true, y_proba)
    }