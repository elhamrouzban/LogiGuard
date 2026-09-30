from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_predict_endpoint():
    payload = {
        "Type": "DEBIT",
        "Customer_Segment": "Consumer",
        "Customer_State": "CA",
        "Order_Country": "United States",
        "Order_Region": "West of USA",
        "Shipping_Mode": "Standard Class",
        "total_quantity": 1,
        "total_discount": 0.0,
        "num_unique_products": 1,
        "num_unique_categories": 1,
        "num_unique_departments": 1,
        "order_hour": 10,
        "order_dayofweek": 2,
        "order_month": 6,
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    result = response.json()

    assert "late_risk_probability" in result
    assert "late_risk_prediction" in result
    assert "risk_label" in result

    assert 0.0 <= result["late_risk_probability"] <= 1.0
    assert result["late_risk_prediction"] in [0, 1]
    assert result["risk_label"] in ["Late", "Not Late"]