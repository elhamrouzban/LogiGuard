from datetime import datetime
from pathlib import Path
import json

import joblib
import pandas as pd

from src.data.splitting import time_based_split

from src.features.preprocessing import (
    add_time_features,
    learn_rare_countries,
    group_rare_countries,
    build_preprocessor,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
)

from src.models.baseline import (
    build_baseline_model,
    train_baseline_model,
)

from src.models.evaluation import evaluate_classifier


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = PROJECT_ROOT / "models"
BASELINE_DIR = MODEL_DIR / "baseline"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_latest_processed_data() -> pd.DataFrame:
    run_dirs = sorted(
        path
        for path in PROCESSED_DATA_DIR.iterdir()
        if path.is_dir()
    )

    if not run_dirs:
        raise FileNotFoundError(
            "No processed dataset found. "
            "Run 'python -m pipelines.prepare_data' first."
        )

    latest_run_dir = run_dirs[-1]

    csv_files = list(
        latest_run_dir.glob("order_level_clean_*.csv")
    )

    if len(csv_files) != 1:
        raise ValueError(
            f"Expected exactly one processed dataset in "
            f"{latest_run_dir}, found {len(csv_files)}."
        )

    return pd.read_csv(
        csv_files[0],
        parse_dates=["order date (DateOrders)"],
    )


def main():
    # Unique ID for this baseline training run
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Directory for this baseline version
    run_dir = BASELINE_DIR / run_timestamp

    model_path = (
        run_dir
        / f"logistic_regression_{run_timestamp}.joblib"
    )

    preprocessor_path = (
        run_dir
        / f"preprocessor_{run_timestamp}.joblib"
    )

    metadata_path = (
        run_dir
        / f"metadata_{run_timestamp}.json"
    )

    # 1. Load latest processed order-level dataset
    order_df = load_latest_processed_data()

    # 2. Time-based train / validation / test split
    train_df, val_df, test_df = time_based_split(order_df)

    # 3. Add time-based features
    train_df = add_time_features(train_df)
    val_df = add_time_features(val_df)
    test_df = add_time_features(test_df)

    # 4. Learn rare countries from TRAIN only
    rare_countries = list(
        learn_rare_countries(train_df)
    )

    # 5. Apply same rare-country mapping to all splits
    train_df = group_rare_countries(
        train_df,
        rare_countries,
    )

    val_df = group_rare_countries(
        val_df,
        rare_countries,
    )

    test_df = group_rare_countries(
        test_df,
        rare_countries,
    )

    # 6. Separate model features and target
    feature_columns = (
        CATEGORICAL_FEATURES
        + NUMERIC_FEATURES
    )

    X_train = train_df[feature_columns]
    X_val = val_df[feature_columns]
    X_test = test_df[feature_columns]

    y_train = train_df[TARGET]
    y_val = val_df[TARGET]
    y_test = test_df[TARGET]

    # 7. Fit preprocessing on TRAIN only
    preprocessor = build_preprocessor()

    X_train_prepared = preprocessor.fit_transform(
        X_train
    )

    X_val_prepared = preprocessor.transform(
        X_val
    )

    X_test_prepared = preprocessor.transform(
        X_test
    )

    # 8. Build and train baseline model
    model = build_baseline_model()

    model = train_baseline_model(
        model,
        X_train_prepared,
        y_train,
    )

    # 9. Evaluate validation data
    validation_metrics = evaluate_classifier(
        model,
        X_val_prepared,
        y_val,
    )

    # 10. Evaluate test data
    test_metrics = evaluate_classifier(
        model,
        X_test_prepared,
        y_test,
    )

    print("\nBaseline Validation Metrics")
    print("---------------------------")

    for name, value in validation_metrics.items():
        print(f"{name}: {value}")

    print("\nBaseline Test Metrics")
    print("---------------------")

    for name, value in test_metrics.items():
        print(f"{name}: {value}")

    # 11. Create version directory automatically
    run_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    # 12. Save model and fitted preprocessor
    joblib.dump(
        model,
        model_path,
    )

    joblib.dump(
        preprocessor,
        preprocessor_path,
    )

    # 13. Save metadata
    metadata = {
        "run_id": run_timestamp,
        "model_name": "Baseline Logistic Regression",
        "trained_at": datetime.now().astimezone().isoformat(),
        "feature_columns": feature_columns,
        "rare_countries": rare_countries,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
    }

    with open(
        metadata_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=4,
        )

    # 14. Report saved artifacts
    print("\nSaved baseline version")
    print("----------------------")
    print(f"Run ID:       {run_timestamp}")
    print(f"Model:        {model_path}")
    print(f"Preprocessor: {preprocessor_path}")
    print(f"Metadata:     {metadata_path}")


if __name__ == "__main__":
    main()