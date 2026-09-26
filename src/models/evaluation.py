from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)


def evaluate_classifier(model, X, y):
    """Evaluate a binary classification model."""

    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred),
        "recall": recall_score(y, y_pred),
        "f1": f1_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_proba),
        "confusion_matrix": confusion_matrix(y, y_pred),
    }

    return metrics