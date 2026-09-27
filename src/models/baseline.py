from sklearn.linear_model import LogisticRegression


def build_baseline_model() -> LogisticRegression:
    """Create the Week 1 baseline Logistic Regression model."""

    return LogisticRegression(
        max_iter=1000,
        random_state=42,
    )


def train_baseline_model(
    model: LogisticRegression,
    X_train,
    y_train,
) -> LogisticRegression:
    """Train the baseline model."""

    model.fit(X_train, y_train)
    return model