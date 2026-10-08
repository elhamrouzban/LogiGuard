from src.database.connection import SessionLocal
from src.database.orm_models import Order, Prediction


def get_shipment(order_id: int) -> dict | None:
    db = SessionLocal()

    try:
        shipment = (
            db.query(Order, Prediction)
            .join(
                Prediction,
                Prediction.order_id == Order.order_id,
            )
            .filter(Order.order_id == order_id)
            .first()
        )

        if shipment is None:
            return None

        order, prediction = shipment

        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "order_date": order.order_date.isoformat(),
            "type": order.type,
            "customer_segment": order.customer_segment,
            "customer_state": order.customer_state,
            "order_country": order.order_country,
            "order_region": order.order_region,
            "shipping_mode": order.shipping_mode,
            "total_quantity": order.total_quantity,
            "total_discount": order.total_discount,
            "num_unique_products": order.num_unique_products,
            "num_unique_categories": order.num_unique_categories,
            "num_unique_departments": order.num_unique_departments,
            "late_risk_probability": (
                prediction.late_risk_probability
            ),
            "late_risk_prediction": (
                prediction.late_risk_prediction
            ),
            "risk_label": prediction.risk_label,
            "threshold": prediction.threshold,
            "model_run_id": prediction.model_run_id,
        }

    finally:
        db.close()



def get_prediction(order_id: int) -> dict | None:
    db = SessionLocal()

    try:
        prediction = (
            db.query(Prediction)
            .filter(Prediction.order_id == order_id)
            .first()
        )

        if prediction is None:
            return None

        return {
            "order_id": prediction.order_id,
            "late_risk_probability": (
                prediction.late_risk_probability
            ),
            "late_risk_prediction": (
                prediction.late_risk_prediction
            ),
            "risk_label": prediction.risk_label,
            "threshold": prediction.threshold,
            "model_run_id": prediction.model_run_id,
            "created_at": (
                prediction.created_at.isoformat()
            ),
        }

    finally:
        db.close()



def find_similar_shipments(
    order_id: int,
    limit: int = 5,
) -> list[dict]:
    db = SessionLocal()

    try:
        target = (
            db.query(Order, Prediction)
            .join(
                Prediction,
                Prediction.order_id == Order.order_id,
            )
            .filter(Order.order_id == order_id)
            .first()
        )

        if target is None:
            return []

        target_order, target_prediction = target

        rows = (
            db.query(Order, Prediction)
            .join(
                Prediction,
                Prediction.order_id == Order.order_id,
            )
            .filter(
                Order.order_id != order_id,
                Order.order_country
                == target_order.order_country,
                Order.order_region
                == target_order.order_region,
                Order.shipping_mode
                == target_order.shipping_mode,
            )
            .all()
        )

        similar_shipments = []

        for order, prediction in rows:
            probability_distance = abs(
                prediction.late_risk_probability
                - target_prediction.late_risk_probability
            )

            similar_shipments.append(
                {
                    "order_id": order.order_id,
                    "order_country": order.order_country,
                    "order_region": order.order_region,
                    "shipping_mode": order.shipping_mode,
                    "late_risk_probability": (
                        prediction.late_risk_probability
                    ),
                    "risk_label": prediction.risk_label,
                    "probability_distance": (
                        probability_distance
                    ),
                }
            )

        similar_shipments.sort(
            key=lambda shipment: (
                shipment["probability_distance"]
            )
        )

        return similar_shipments[:limit]

    finally:
        db.close()