
from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.orm import sessionmaker

from src.agent.tools import (
    find_similar_shipments,
    get_prediction,
    get_shipment,
)
from src.database.connection import engine
from src.database.orm_models import Order, Prediction


@pytest.fixture
def sample_shipments(monkeypatch):
    if engine.url.database != "logiguard_test":
        pytest.fail(
            "Agent integration tests require logiguard_test."
        )

    order_id = 1_000_000_000_000 + uuid4().int % 1_000_000_000_000
    similar_id = order_id + 1

    connection = engine.connect()
    transaction = connection.begin()

    TestSession = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    monkeypatch.setattr(
        "src.agent.tools.SessionLocal",
        TestSession,
    )

    try:
        with TestSession.begin() as db:
            for current_id, probability in (
                (order_id, 0.75),
                (similar_id, 0.70),
            ):
                db.add(
                    Order(
                        order_id=current_id,
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

                db.add(
                    Prediction(
                        order_id=current_id,
                        late_risk_probability=probability,
                        late_risk_prediction=1,
                        risk_label="Late",
                        threshold=0.40,
                        model_run_id="integration-test-model",
                    )
                )

        yield order_id, similar_id

    finally:
        transaction.rollback()
        connection.close()


def test_get_shipment_returns_order_and_prediction(
    sample_shipments,
):
    order_id, _ = sample_shipments

    shipment = get_shipment(order_id)

    assert shipment is not None
    assert shipment["order_id"] == order_id
    assert shipment["customer_id"] == 12345
    assert shipment["shipping_mode"] == "Standard Class"
    assert shipment["late_risk_probability"] == 0.75
    assert shipment["late_risk_prediction"] == 1
    assert shipment["risk_label"] == "Late"
    assert shipment["model_run_id"] == "integration-test-model"


def test_get_prediction_returns_prediction_details(
    sample_shipments,
):
    order_id, _ = sample_shipments

    prediction = get_prediction(order_id)

    assert prediction is not None
    assert prediction["order_id"] == order_id
    assert prediction["late_risk_probability"] == 0.75
    assert prediction["late_risk_prediction"] == 1
    assert prediction["risk_label"] == "Late"
    assert prediction["threshold"] == 0.40
    assert prediction["model_run_id"] == "integration-test-model"
    assert "created_at" in prediction


def test_find_similar_shipments_returns_list(
    sample_shipments,
):
    order_id, similar_id = sample_shipments

    similar = find_similar_shipments(order_id, limit=5)

    assert isinstance(similar, list)
    assert len(similar) == 1
    assert similar[0]["order_id"] == similar_id
    assert similar[0]["late_risk_probability"] == 0.70
    assert similar[0]["risk_label"] == "Late"
    assert similar[0]["probability_distance"] == pytest.approx(
        0.05
    )
