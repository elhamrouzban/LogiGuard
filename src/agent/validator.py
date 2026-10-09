from typing import Any


VALID_INTENTS = {
    "prediction",
    "shipment_status",
    "similar_shipments",
}


def validate_copilot_result(result: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    status = result.get("status")

    if status not in {"success", "error", "not_found"}:
        errors.append("Invalid or missing status.")

    if status != "success":
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }

    order_id = result.get("order_id")

    if not isinstance(order_id, int) or order_id <= 0:
        errors.append("A valid positive order_id is required.")

    intent = result.get("intent")

    if intent not in VALID_INTENTS:
        errors.append("Invalid or missing intent.")
        return {
            "valid": False,
            "errors": errors,
        }

    if intent == "prediction":
        _validate_prediction_result(result, errors)

    elif intent == "shipment_status":
        _validate_shipment_result(result, errors)

    elif intent == "similar_shipments":
        _validate_similar_shipments_result(result, errors)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def _validate_prediction_result(
    result: dict[str, Any],
    errors: list[str],
) -> None:
    prediction = result.get("prediction")

    if not isinstance(prediction, dict):
        errors.append("Prediction evidence is missing.")
        return

    if prediction.get("order_id") != result.get("order_id"):
        errors.append(
            "Prediction order_id does not match the requested order_id."
        )

    probability = prediction.get("late_risk_probability")
    threshold = prediction.get("threshold")
    predicted_class = prediction.get("late_risk_prediction")

    if not isinstance(probability, (int, float)):
        errors.append("Prediction probability must be numeric.")
        return

    if not 0.0 <= float(probability) <= 1.0:
        errors.append("Prediction probability must be between 0 and 1.")

    if not isinstance(threshold, (int, float)):
        errors.append("Prediction threshold must be numeric.")
        return

    expected_class = int(float(probability) >= float(threshold))

    if predicted_class != expected_class:
        errors.append(
            "Prediction class is inconsistent with probability and threshold."
        )


def _validate_shipment_result(
    result: dict[str, Any],
    errors: list[str],
) -> None:
    shipment = result.get("shipment")

    if not isinstance(shipment, dict):
        errors.append("Shipment evidence is missing.")
        return

    if shipment.get("order_id") != result.get("order_id"):
        errors.append(
            "Shipment order_id does not match the requested order_id."
        )


def _validate_similar_shipments_result(
    result: dict[str, Any],
    errors: list[str],
) -> None:
    shipments = result.get("similar_shipments")

    if not isinstance(shipments, list):
        errors.append("Similar shipment evidence must be a list.")
        return

    for shipment in shipments:
        if not isinstance(shipment, dict):
            errors.append("Each similar shipment must be a dictionary.")
            continue

        probability_distance = shipment.get("probability_distance")

        if (
            probability_distance is not None
            and (
                not isinstance(probability_distance, (int, float))
                or probability_distance < 0
            )
        ):
            errors.append(
                "probability_distance must be a non-negative number."
            )