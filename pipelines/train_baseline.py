from src.data.cleaning import load_and_clean_data
from src.data.aggregation import aggregate_to_order_level
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


def main():
    # 1. Load and clean raw data
    df_clean = load_and_clean_data()

    # 2. Aggregate to one row per order
    order_df = aggregate_to_order_level(df_clean)

    # 3. Time-based train / validation / test split
    train_df, val_df, test_df = time_based_split(order_df)

    # 4. Add time-based features
    train_df = add_time_features(train_df)
    val_df = add_time_features(val_df)
    test_df = add_time_features(test_df)

    # 5. Learn rare countries from Train only
    rare_countries = learn_rare_countries(train_df)

    # 6. Apply the same rare-country mapping to all splits
    train_df = group_rare_countries(train_df, rare_countries)
    val_df = group_rare_countries(val_df, rare_countries)
    test_df = group_rare_countries(test_df, rare_countries)

    # 7. Separate model features and target
    feature_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES

    X_train = train_df[feature_columns]
    X_val = val_df[feature_columns]
    X_test = test_df[feature_columns]

    y_train = train_df[TARGET]
    y_val = val_df[TARGET]
    y_test = test_df[TARGET]

    # 8. Build and fit preprocessing on Train only
    preprocessor = build_preprocessor()

    X_train_prepared = preprocessor.fit_transform(X_train)
    X_val_prepared = preprocessor.transform(X_val)
    X_test_prepared = preprocessor.transform(X_test)

    # 9. Build and train baseline model
    model = build_baseline_model()

    model = train_baseline_model(
        model,
        X_train_prepared,
        y_train,
    )

    # 10. Evaluate on validation data
    metrics = evaluate_classifier(
        model,
        X_val_prepared,
        y_val,
    )

    print("\nBaseline Logistic Regression")
    print("----------------------------")
    print(f"Accuracy:  {metrics['accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall:    {metrics['recall']:.3f}")
    print(f"F1:        {metrics['f1']:.3f}")
    print(f"ROC-AUC:   {metrics['roc_auc']:.3f}")
    print("\nConfusion Matrix:")
    print(metrics["confusion_matrix"])


if __name__ == "__main__":
    main()
    