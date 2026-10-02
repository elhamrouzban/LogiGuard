from datetime import datetime
from pathlib import Path
import pandas as pd

import json

import joblib
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from xgboost import XGBClassifier
from src.models.evaluation import evaluate_classifier

from src.data.splitting import time_based_split
from src.features.preprocessing import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    add_time_features,
    build_preprocessor,
    group_rare_countries,
    learn_rare_countries,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

SELECTED_THRESHOLD = 0.40

MODEL_PARAMS = {
    "n_estimators": 150,
    "max_depth": 5,
    "learning_rate": 0.07,
    "min_child_weight": 1,
    "subsample": 1.0,
    "colsample_bytree": 0.7,
    "random_state": 42,
    "eval_metric": "logloss",
}


def load_latest_processed_data() -> pd.DataFrame:
    run_dirs = sorted(
        [
            path
            for path in PROCESSED_DATA_DIR.iterdir()
            if path.is_dir()
        ]
    )

    if not run_dirs:
        raise FileNotFoundError(
            "No processed dataset found. Run "
            "'python -m pipelines.prepare_data' first."
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
    # Unique identifier for this training run
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # File names for this model version
    model_filename = f"xgboost_stage2_{run_timestamp}.joblib"
    preprocessor_filename = f"preprocessor_{run_timestamp}.joblib"
    metadata_filename = f"model_metadata_{run_timestamp}.json"

    # Directory for this specific training run
    run_dir = MODEL_DIR / run_timestamp

    model_path = run_dir / model_filename
    preprocessor_path = run_dir / preprocessor_filename
    metadata_path = run_dir / metadata_filename

    # Pointer to the currently selected model version
    current_model_path = MODEL_DIR / "current_model.json"

    # ---------------------------------------------------------
    # 1. Load and clean historical raw data
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # 2. Aggregate item-level data to order level
    # ---------------------------------------------------------
    order_df = load_latest_processed_data()
    # ---------------------------------------------------------
    # 3. Chronological train / validation / test split
    # ---------------------------------------------------------
    train_df, val_df, test_df = time_based_split(order_df)

    # ---------------------------------------------------------
    # 4. Add time-based features
    # ---------------------------------------------------------
    train_df = add_time_features(train_df)
    val_df = add_time_features(val_df)
    test_df = add_time_features(test_df)

    # ---------------------------------------------------------
    # 5. Learn rare countries from TRAIN only
    # ---------------------------------------------------------
    rare_countries = list(learn_rare_countries(train_df))

    # ---------------------------------------------------------
    # 6. Apply the same rare-country mapping to all splits
    # ---------------------------------------------------------
    train_df = group_rare_countries(train_df, rare_countries)
    val_df = group_rare_countries(val_df, rare_countries)
    test_df = group_rare_countries(test_df, rare_countries)

    # ---------------------------------------------------------
    # 7. Separate model features and target
    # ---------------------------------------------------------
    feature_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES

    X_train = train_df[feature_columns]
    X_val = val_df[feature_columns]
    X_test = test_df[feature_columns]

    y_train = train_df[TARGET]
    y_val = val_df[TARGET]
    y_test = test_df[TARGET]

    # ---------------------------------------------------------
    # 8. Fit preprocessing on TRAIN only
    # ---------------------------------------------------------
    preprocessor = build_preprocessor()

    X_train_prepared = preprocessor.fit_transform(X_train)
    X_val_prepared = preprocessor.transform(X_val)
    X_test_prepared = preprocessor.transform(X_test)

    # ---------------------------------------------------------
    # 9. Train final selected XGBoost model
    # ---------------------------------------------------------
    model = XGBClassifier(**MODEL_PARAMS)

    model.fit(
        X_train_prepared,
        y_train,
    )

    validation_metrics = evaluate_classifier(
        model,
        X_val_prepared,
        y_val,
        threshold=SELECTED_THRESHOLD,
    )

    test_metrics = evaluate_classifier(
        model,
        X_test_prepared,
        y_test,
        threshold=SELECTED_THRESHOLD,
    )


    # ---------------------------------------------------------
    # 10. Evaluate at selected operating threshold
    # ---------------------------------------------------------
    validation_metrics = evaluate_classifier(
        model,
        X_val_prepared,
        y_val,
        SELECTED_THRESHOLD,
    )

    test_metrics = evaluate_classifier(
        model,
        X_test_prepared,
        y_test,
        SELECTED_THRESHOLD,
    )

    print("\nValidation metrics")
    print("------------------")

    for name, value in validation_metrics.items():
        print(f"{name}: {value}")

    print("\nTest metrics")
    print("------------")

    for name, value in test_metrics.items():
        print(f"{name}: {value}")

    # ---------------------------------------------------------
    # 11. Create version directory
    # ---------------------------------------------------------
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    run_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    # ---------------------------------------------------------
    # 12. Save model artifacts
    # ---------------------------------------------------------
    joblib.dump(
        model,
        model_path,
    )

    joblib.dump(
        preprocessor,
        preprocessor_path,
    )

    # ---------------------------------------------------------
    # 13. Save metadata
    # ---------------------------------------------------------
    metadata = {
        "run_id": run_timestamp,
        "model_name": "Stage 2 XGBoost",
        "trained_at": datetime.now().astimezone().isoformat(),
        "threshold": SELECTED_THRESHOLD,
        "hyperparameters": MODEL_PARAMS,
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

    # ---------------------------------------------------------
    # 14. Update pointer to current model
    # ---------------------------------------------------------
    current_model = {
        "run_id": run_timestamp,
        "run_directory": run_timestamp,
        "model": str(Path(run_timestamp) / model_filename),
        "preprocessor": str(
            Path(run_timestamp) / preprocessor_filename
        ),
        "metadata": str(
            Path(run_timestamp) / metadata_filename
        ),
    }

    with open(
        current_model_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            current_model,
            file,
            indent=4,
        )

    # ---------------------------------------------------------
    # 15. Report saved artifacts
    # ---------------------------------------------------------
    print("\nSaved model version")
    print("-------------------")
    print(f"Run ID:       {run_timestamp}")
    print(f"Model:        {model_path}")
    print(f"Preprocessor: {preprocessor_path}")
    print(f"Metadata:     {metadata_path}")

    print("\nCurrent model pointer")
    print("---------------------")
    print(current_model_path)


if __name__ == "__main__":
    main()