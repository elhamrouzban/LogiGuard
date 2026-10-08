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