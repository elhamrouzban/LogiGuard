import pytest

from src.agent.copilot import run_copilot


@pytest.fixture(autouse=True)
def mock_grounded_response(monkeypatch):
    monkeypatch.setattr(
        "src.agent.copilot.generate_grounded_response",
        lambda question, evidence: "Mocked grounded response.",
    )


def test_copilot_routes_prediction_action():
    result = run_copilot(
        order_id=900002,
        action="prediction",
    )

    assert result["status"] == "success"
    assert result["intent"] == "prediction"
    assert result["order_id"] == 900002
    assert "prediction" in result

    assert result["prediction"]["risk_level"] in {
        "No Risk",
        "Low Risk",
        "Medium Risk",
        "High Risk",
    }

    assert result["answer"] == "Mocked grounded response."


def test_copilot_routes_similar_shipments_action():
    result = run_copilot(
        order_id=900002,
        action="similar_shipments",
    )

    assert result["order_id"] == 900002
    assert result["status"] in [
        "success",
        "not_found",
    ]


def test_copilot_routes_shipment_status_action():
    result = run_copilot(
        order_id=900002,
        action="shipment_status",
    )

    assert result["status"] == "success"
    assert result["intent"] == "shipment_status"
    assert result["order_id"] == 900002
    assert "shipment" in result


def test_copilot_rejects_invalid_prediction_response(
    monkeypatch,
):
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
        order_id=900002,
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