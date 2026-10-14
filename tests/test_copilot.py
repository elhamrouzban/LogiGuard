
import pytest

from src.agent.copilot import run_copilot


TEST_ORDER_ID = 900002


@pytest.fixture(autouse=True)
def mock_grounded_response(monkeypatch):
    monkeypatch.setattr(
        "src.agent.copilot.generate_grounded_response",
        lambda question, evidence: "Mocked grounded response.",
    )


def test_copilot_routes_prediction_action(monkeypatch):
    def fake_get_prediction(order_id):
        return {
            "order_id": order_id,
            "late_risk_probability": 0.80,
            "late_risk_prediction": 1,
            "risk_label": "Late",
            "threshold": 0.40,
            "model_run_id": "test-model",
            "created_at": "2026-10-09T00:00:00",
        }

    monkeypatch.setattr(
        "src.agent.copilot.get_prediction",
        fake_get_prediction,
    )

    result = run_copilot(
        order_id=TEST_ORDER_ID,
        action="prediction",
    )

    assert result["status"] == "success"
    assert result["intent"] == "prediction"
    assert result["order_id"] == TEST_ORDER_ID
    assert result["prediction"]["late_risk_probability"] == 0.80
    assert result["prediction"]["risk_level"] in {
        "No Risk",
        "Low Risk",
        "Medium Risk",
        "High Risk",
    }
    assert result["answer"] == "Mocked grounded response."


def test_copilot_routes_similar_shipments_action(monkeypatch):
    monkeypatch.setattr(
        "src.agent.copilot.find_similar_shipments",
        lambda order_id, limit: [
            {
                "order_id": order_id + 1,
                "late_risk_probability": 0.70,
                "risk_label": "Late",
                "probability_distance": 0.10,
            }
        ],
    )

    result = run_copilot(
        order_id=TEST_ORDER_ID,
        action="similar_shipments",
    )

    assert result["status"] == "success"
    assert result["intent"] == "similar_shipments"
    assert result["order_id"] == TEST_ORDER_ID
    assert len(result["similar_shipments"]) == 1
    assert result["similar_shipments"][0]["order_id"] == TEST_ORDER_ID + 1
    assert result["similar_shipments"][0]["risk_level"] in {
        "No Risk",
        "Low Risk",
        "Medium Risk",
        "High Risk",
    }
    assert result["answer"] == "Mocked grounded response."


def test_copilot_routes_shipment_status_action(monkeypatch):
    monkeypatch.setattr(
        "src.agent.copilot.get_shipment",
        lambda order_id: {
            "order_id": order_id,
            "customer_id": 12345,
            "shipping_mode": "Standard Class",
            "late_risk_probability": 0.75,
            "late_risk_prediction": 1,
            "risk_label": "Late",
            "model_run_id": "test-model",
        },
    )

    result = run_copilot(
        order_id=TEST_ORDER_ID,
        action="shipment_status",
    )

    assert result["status"] == "success"
    assert result["intent"] == "shipment_status"
    assert result["order_id"] == TEST_ORDER_ID
    assert result["shipment"]["shipping_mode"] == "Standard Class"
    assert result["shipment"]["risk_level"] in {
        "No Risk",
        "Low Risk",
        "Medium Risk",
        "High Risk",
    }
    assert result["answer"] == "Mocked grounded response."


def test_copilot_rejects_invalid_prediction_response(monkeypatch):
    def fake_get_prediction(order_id: int):
        return {
            "order_id": order_id,
            "late_risk_probability": 0.80,
            "late_risk_prediction": 0,
            "risk_label": "Not Late",
            "threshold": 0.40,
            "model_run_id": "test-model",
            "created_at": "2026-10-09T00:00:00",
        }

    monkeypatch.setattr(
        "src.agent.copilot.get_prediction",
        fake_get_prediction,
    )

    result = run_copilot(
        order_id=TEST_ORDER_ID,
        action="prediction",
    )

    assert result["status"] == "error"
    assert result["message"] == (
        "Copilot response failed validation."
    )
    assert (
        "Prediction class is inconsistent "
        "with probability and threshold."
        in result["validation_errors"]
    )
