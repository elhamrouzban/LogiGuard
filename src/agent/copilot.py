

from src.agent.validator import validate_copilot_result

from src.agent.tools import (
    find_similar_shipments,
    get_prediction,
    get_shipment,
)
from src.shared.risk import get_risk_level
from src.agent.llm import generate_grounded_response

def _build_llm_question(
    order_id: int,
    action: str,
) -> str:
    questions = {
        "prediction": (
            f"What is the risk prediction for order {order_id}?"
        ),
        "shipment_status": (
            f"What is the shipment status for order {order_id}?"
        ),
        "similar_shipments": (
            f"Find similar shipments to order {order_id}."
        ),
    }

    return questions[action]


def run_copilot(order_id: str, action: str) -> dict:

    question = _build_llm_question(
        order_id=order_id,
        action=action,
    )


    if action == "similar_shipments":

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

        return _validated_result({
            "status": "success",
            "intent": "similar_shipments",
            "order_id": order_id,
            "similar_shipments": shipments,
            },
            question,
        )

    if action == "prediction":
        prediction = get_prediction(order_id)

        if prediction is None:
            return {
                "status": "not_found",
                "order_id": order_id,
                "message": "Prediction not found.",
            }

        prediction = dict(prediction)
        prediction["risk_level"] = get_risk_level(
            prediction["late_risk_probability"]
        )

        return _validated_result({
            "status": "success",
            "intent": "prediction",
            "order_id": order_id,
            "prediction": prediction,
            },
            question,
        )

    shipment = get_shipment(order_id)

    if shipment is None:
        return {
            "status": "not_found",
            "order_id": order_id,
            "message": "Shipment not found.",
        }

    return _validated_result(
        {
        "status": "success",
        "intent": "shipment_status",
        "order_id": order_id,
        "shipment": shipment,
        },
        question,
    )



def _validated_result(
    result: dict,
    question: str,
) -> dict:
    validation = validate_copilot_result(result)

    if not validation["valid"]:
        return {
            "status": "error",
            "message": "Copilot response failed validation.",
            "validation_errors": validation["errors"],
        }

    try:
        result["answer"] = generate_grounded_response(
            question=question,
            evidence=result,
        )
    except Exception:
        # Gemini is optional. Validated Copilot evidence
        # must remain available if the external LLM fails.
        pass

    return result