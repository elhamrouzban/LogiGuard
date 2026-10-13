
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from evidently import DataDefinition, Dataset, Report
from evidently.presets import DataDriftPreset, DataSummaryPreset

from pipelines.train_final_model import load_latest_processed_data
from src.data.splitting import time_based_split
from src.database.connection import SessionLocal
from src.database.orm_models import Order, Prediction
from src.features.preprocessing import (
    add_time_features,
    group_rare_countries,
)
from src.models.prediction import predict_late_risk


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "monitoring" / "reports"
CURRENT_MODEL_PATH = PROJECT_ROOT / "models" / "current_model.json"

MIN_CURRENT_ROWS = 30


def load_model_metadata():
    with CURRENT_MODEL_PATH.open(encoding="utf-8") as file:
        manifest = json.load(file)

    metadata_path = PROJECT_ROOT / "models" / manifest["metadata"]

    with metadata_path.open(encoding="utf-8") as file:
        metadata = json.load(file)

    if metadata["run_id"] != manifest["run_id"]:
        raise ValueError("Model manifest and metadata do not match.")

    return metadata


def load_reference(metadata):
    # Recreate the chronological training split.
    processed = load_latest_processed_data()
    train_df, _, _ = time_based_split(processed)

    train_df = add_time_features(train_df)

    # Reuse the active model's categorical grouping.
    train_df = group_rare_countries(
        train_df, metadata["rare_countries"]
    )

    reference = train_df[metadata["feature_columns"]].copy()

    # Use a deterministic reference sample to keep reports fast.
    if len(reference) > 5000:
        reference = reference.sample(n=5000, random_state=42)

    reference = reference.reset_index(drop=True)

    # Generate reference probabilities using the active model.
    predictions = predict_late_risk(reference)
    reference["late_risk_probability"] = (
        predictions["late_risk_probability"].to_numpy()
    )

    return reference


def load_current(metadata):
    db = SessionLocal()

    try:
        rows = (
            db.query(Order, Prediction)
            .join(
                Prediction,
                Prediction.order_id == Order.order_id,
            )
            .filter(Prediction.model_run_id == metadata["run_id"])
            .all()
        )

        records = []

        for order, prediction in rows:
            records.append({
                "Type": order.type,
                "Customer Segment": order.customer_segment,
                "Customer State": order.customer_state,
                "Order Country": order.order_country,
                "Order Region": order.order_region,
                "Shipping Mode": order.shipping_mode,
                "total_quantity": order.total_quantity,
                "total_discount": order.total_discount,
                "num_unique_products": order.num_unique_products,
                "num_unique_categories": order.num_unique_categories,
                "num_unique_departments": order.num_unique_departments,
                "order_hour": order.order_hour,
                "order_dayofweek": order.order_dayofweek,
                "order_month": order.order_month,
                "late_risk_probability": prediction.late_risk_probability,
            })

        if not records:
            raise ValueError(
                "No stored predictions for the active model."
            )

        current = pd.DataFrame(records)

        current = group_rare_countries(
            current, metadata["rare_countries"]
        )

        return current[
            metadata["feature_columns"] + ["late_risk_probability"]
        ]

    finally:
        db.close()


def main():
    metadata = load_model_metadata()

    reference = load_reference(metadata)
    current = load_current(metadata)

    print(f"Active model: {metadata['run_id']}")
    print(f"Reference rows: {len(reference)}")
    print(f"Current rows: {len(current)}")


    insufficient_data = len(current) < MIN_CURRENT_ROWS

    if insufficient_data:
        print(
            "STATUS: INSUFFICIENT_DATA — "
            f"Only {len(current)} current rows; "
            f"minimum required: {MIN_CURRENT_ROWS}. "
            "Drift results are exploratory."
        )


    categorical = [
        "Type",
        "Customer Segment",
        "Customer State",
        "Order Country",
        "Order Region",
        "Shipping Mode",
    ]

    numerical = [
        col
        for col in reference.columns
        if col not in categorical
    ]

    definition = DataDefinition(
        categorical_columns=categorical,
        numerical_columns=numerical,
    )

    reference_dataset = Dataset.from_pandas(
        reference,
        data_definition=definition,
    )

    current_dataset = Dataset.from_pandas(
        current,
        data_definition=definition,
    )

    report = Report([
        DataDriftPreset(),
        DataSummaryPreset(),
    ])

    result = report.run(
        current_dataset,
        reference_dataset,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_path = OUTPUT_DIR / f"drift_report_{timestamp}.html"

    result.save_html(str(output_path))

    if insufficient_data:
        html = output_path.read_text(encoding="utf-8")

        warning = """
        <div style="padding:18px; margin:20px;
                    border:2px solid #d97706;
                    background:#fffbeb; color:#92400e;
                    font-family:Arial,sans-serif;">
        <strong>INSUFFICIENT DATA</strong>
        <p>
            Fewer than 30 current observations are available.
            Drift statistics are exploratory and must not be
            interpreted as confirmed production drift.
        </p>
        </div>
        """

        html = html.replace("<body>", "<body>" + warning, 1)
        output_path.write_text(html, encoding="utf-8")

    print(f"Report saved: {output_path}")


if __name__ == "__main__":
    main()
