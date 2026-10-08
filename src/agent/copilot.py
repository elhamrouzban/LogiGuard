
import re

from src.agent.tools import (
    find_similar_shipments,
    get_prediction,
    get_shipment,
)


def extract_order_id(question: str) -> int | None:
    match = re.search(r"\b\d+\b", question)

    if match is None:
        return None

    return int(match.group())


def run_copilot(question: str) -> dict:
    
    order_id = extract_order_id(question)

    if order_id is None:
        return {
            "status": "error",
            "message": "Please provide an Order ID.",
        }

    normalized_question = question.lower()

    if "similar" in normalized_question:
        shipments = find_similar_shipments(
            order_id=order_id,
            limit=5,
        )

        if not shipments:
            return {
                "status": "not_found",
                "order_id": order_id,
                "message": (
                    "No similar shipments were found."
                ),
            }

        return {
            "status": "success",
            "intent": "similar_shipments",
            "order_id": order_id,
            "similar_shipments": shipments,
        }

    if (
        "prediction" in normalized_question
        or "risk" in normalized_question
        or "probability" in normalized_question
    ):
        prediction = get_prediction(order_id)

        if prediction is None:
            return {
                "status": "not_found",
                "order_id": order_id,
                "message": "Prediction not found.",
            }

        return {
            "status": "success",
            "intent": "prediction",
            "order_id": order_id,
            "prediction": prediction,
        }

    shipment = get_shipment(order_id)

    if shipment is None:
        return {
            "status": "not_found",
            "order_id": order_id,
            "message": "Shipment not found.",
        }

    return {
        "status": "success",
        "intent": "shipment_status",
        "order_id": order_id,
        "shipment": shipment,
    }