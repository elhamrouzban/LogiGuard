from src.agent.copilot import run_copilot


def test_copilot_routes_prediction_question():
    result = run_copilot(
        "What is the risk prediction for order 900002?"
    )

    assert result["status"] == "success"
    assert result["intent"] == "prediction"
    assert result["order_id"] == 900002
    assert "prediction" in result


def test_copilot_routes_similar_shipments_question():
    result = run_copilot(
        "Find similar shipments to order 900002."
    )

    assert result["order_id"] == 900002
    assert result["status"] in [
        "success",
        "not_found",
    ]


def test_copilot_requires_order_id():
    result = run_copilot(
        "What is the shipment status?"
    )

    assert result["status"] == "error"
    assert result["message"] == (
        "Please provide an Order ID."
    )


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
        "What is the risk prediction for order 900002?"
    )

    assert result["status"] == "error"
    assert result["message"] == "Copilot response failed validation."
    assert (
        "Prediction class is inconsistent with probability and threshold."
        in result["validation_errors"]
    )