
from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.orm import sessionmaker

from pipelines.monitor_drift import (
    load_current,
    load_model_metadata,
)
from src.database.connection import engine
from src.database.orm_models import Order, Prediction


def test_model_metadata_matches_active_model():
    metadata = load_model_metadata()

    assert metadata["run_id"]
    assert len(metadata["feature_columns"]) == 14


def test_current_data_matches_model_features(monkeypatch):
    if engine.url.database != "logiguard_test":
        pytest.fail(
            "Drift integration tests require logiguard_test."
        )

    metadata = load_model_metadata()
    order_id = 2_000_000_000_000 + uuid4().int % 1_000_000_000_000

    connection = engine.connect()
    transaction = connection.begin()

    TestSession = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    monkeypatch.setattr(
        "pipelines.monitor_drift.SessionLocal",
        TestSession,
    )

    try:
        with TestSession.begin() as db:
            db.add(
                Order(
                    order_id=order_id,
                    customer_id=12345,
                    order_date=datetime(2026, 10, 13, 10, 0),
                    type="DEBIT",
                    customer_segment="Consumer",
                    customer_state="CA",
                    order_country="Estados Unidos",
                    order_region="West of USA",
                    shipping_mode="Standard Class",
                    total_quantity=3,
                    total_discount=10.0,
                    num_unique_products=2,
                    num_unique_categories=2,
                    num_unique_departments=1,
                    order_hour=10,
                    order_dayofweek=1,
                    order_month=10,
                )
            )

            db.flush()

            db.add(
                Prediction(
                    order_id=order_id,
                    late_risk_probability=0.75,
                    late_risk_prediction=1,
                    risk_label="Late",
                    threshold=0.40,
                    model_run_id=metadata["run_id"],
                )
            )

        current = load_current(metadata)

        expected_columns = (
            metadata["feature_columns"]
            + ["late_risk_probability"]
        )

        assert list(current.columns) == expected_columns
        assert len(current) == 1
        assert current["late_risk_probability"].between(0, 1).all()
        assert current["late_risk_probability"].iloc[0] == pytest.approx(
            0.75
        )

    finally:
        transaction.rollback()
        connection.close()
