from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from fastapi.testclient import TestClient

from src.api.main import app
from src.database.connection import SessionLocal
from src.database.orm_models import Order, Prediction


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_predict_endpoint_and_database_persistence():
    test_order_id = 9999001

    db = SessionLocal()

    try:
        db.query(Prediction).filter(
            Prediction.order_id == test_order_id
        ).delete()

        db.query(Order).filter(
            Order.order_id == test_order_id
        ).delete()

        db.commit()

    finally:
        db.close()

    payload = {
        "order_id": test_order_id,
        "customer_id": 12345,
        "order_date": "2026-10-04T19:30:00",
        "type": "DEBIT",
        "customer_segment": "Consumer",
        "customer_state": "CA",
        "order_country": "Estados Unidos",
        "order_region": "West of USA",
        "shipping_mode": "Standard Class",
        "total_quantity": 3,
        "total_discount": 10.0,
        "num_unique_products": 2,
        "num_unique_categories": 2,
        "num_unique_departments": 1,
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    result = response.json()

    assert result["order_id"] == test_order_id
    assert 0.0 <= result["late_risk_probability"] <= 1.0
    assert result["late_risk_prediction"] in [0, 1]
    assert result["risk_label"] in ["Late", "Not Late"]
    assert result["model_run_id"]

    db = SessionLocal()

    try:
        saved_order = db.query(Order).filter(
            Order.order_id == test_order_id
        ).one()

        saved_prediction = db.query(Prediction).filter(
            Prediction.order_id == test_order_id
        ).one()

        assert saved_order.customer_id == 12345
        assert saved_order.order_hour == 19
        assert saved_order.order_month == 10

        assert (
            saved_prediction.late_risk_probability
            == result["late_risk_probability"]
        )

        assert (
            saved_prediction.late_risk_prediction
            == result["late_risk_prediction"]
        )

        assert saved_prediction.risk_label == result["risk_label"]
        assert saved_prediction.model_run_id == result["model_run_id"]

    finally:
        db.query(Prediction).filter(
            Prediction.order_id == test_order_id
        ).delete()

        db.query(Order).filter(
            Order.order_id == test_order_id
        ).delete()

        db.commit()
        db.close()


def test_duplicate_order_returns_409():
    test_order_id = 9999002

    db = SessionLocal()
    try:
        db.query(Prediction).filter(
            Prediction.order_id == test_order_id
        ).delete()
        db.query(Order).filter(
            Order.order_id == test_order_id
        ).delete()
        db.commit()
    finally:
        db.close()

    payload = {
        "order_id": test_order_id,
        "customer_id": 12345,
        "order_date": "2026-10-04T19:30:00",
        "type": "DEBIT",
        "customer_segment": "Consumer",
        "customer_state": "CA",
        "order_country": "Estados Unidos",
        "order_region": "West of USA",
        "shipping_mode": "Standard Class",
        "total_quantity": 3,
        "total_discount": 10.0,
        "num_unique_products": 2,
        "num_unique_categories": 2,
        "num_unique_departments": 1,
    }

    first_response = client.post("/predict", json=payload)

    assert first_response.status_code == 200

    second_response = client.post("/predict", json=payload)

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Order ID already exists."
    }

    db = SessionLocal()
    try:
        db.query(Prediction).filter(
            Prediction.order_id == test_order_id
        ).delete()
        db.query(Order).filter(
            Order.order_id == test_order_id
        ).delete()
        db.commit()
    finally:
        db.close()