from typing import Any

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(
    model: Any,
    X,
    y,
    threshold: float = 0.5,
) -> dict:
    """Evaluate a binary classifier at a specified probability threshold."""

    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    return {
        "accuracy": accuracy_score(y, predictions),
        "precision": precision_score(y, predictions),
        "recall": recall_score(y, predictions),
        "f1": f1_score(y, predictions),
        "roc_auc": roc_auc_score(y, probabilities),
        "confusion_matrix": confusion_matrix(y, predictions).tolist(),
    }