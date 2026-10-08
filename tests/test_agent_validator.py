from src.agent.validator import validate_copilot_result


def test_valid_prediction_result_passes_validation():
    result = {
        "status": "success",
        "intent": "prediction",
        "order_id": 900002,
        "prediction": {
            "order_id": 900002,
            "late_risk_probability": 0.34,
            "late_risk_prediction": 0,
            "risk_label": "Not Late",
            "threshold": 0.4,
            "model_run_id": "test-model",
        },
    }

    validation = validate_copilot_result(result)

    assert validation["valid"] is True
    assert validation["errors"] == []


def test_prediction_order_id_mismatch_fails_validation():
    result = {
        "status": "success",
        "intent": "prediction",
        "order_id": 900002,
        "prediction": {
            "order_id": 123456,
            "late_risk_probability": 0.34,
            "late_risk_prediction": 0,
            "threshold": 0.4,
        },
    }

    validation = validate_copilot_result(result)

    assert validation["valid"] is False
    assert (
        "Prediction order_id does not match the requested order_id."
        in validation["errors"]
    )


def test_inconsistent_prediction_class_fails_validation():
    result = {
        "status": "success",
        "intent": "prediction",
        "order_id": 900002,
        "prediction": {
            "order_id": 900002,
            "late_risk_probability": 0.80,
            "late_risk_prediction": 0,
            "threshold": 0.4,
        },
    }

    validation = validate_copilot_result(result)

    assert validation["valid"] is False
    assert (
        "Prediction class is inconsistent with probability and threshold."
        in validation["errors"]
    )


def test_missing_shipment_evidence_fails_validation():
    result = {
        "status": "success",
        "intent": "shipment_status",
        "order_id": 900002,
    }

    validation = validate_copilot_result(result)

    assert validation["valid"] is False
    assert "Shipment evidence is missing." in validation["errors"]


def test_error_result_is_valid_structured_response():
    result = {
        "status": "error",
        "message": "Please provide an Order ID.",
    }

    validation = validate_copilot_result(result)

    assert validation["valid"] is True
    assert validation["errors"] == []