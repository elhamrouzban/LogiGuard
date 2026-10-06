from datetime import datetime

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.database.connection import SessionLocal
from src.database.orm_models import Order, Prediction
from src.models.prediction import predict_late_risk
from src.database.connection import get_db



app = FastAPI(
    title="LogiGuard API",
    version="0.3.0",
)


class OrderInput(BaseModel):
    order_id: int
    customer_id: int

    order_date: datetime

    type: str
    customer_segment: str
    customer_state: str
    order_country: str
    order_region: str
    shipping_mode: str

    total_quantity: float = Field(ge=0)
    total_discount: float = Field(ge=0)

    num_unique_products: int = Field(ge=1)
    num_unique_categories: int = Field(ge=1)
    num_unique_departments: int = Field(ge=1)


class PredictionResponse(BaseModel):
    order_id: int
    late_risk_probability: float
    late_risk_prediction: int
    risk_label: str
    model_run_id: str

class ShipmentSummary(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    customer_segment: str
    order_country: str
    order_region: str
    shipping_mode: str
    late_risk_probability: float
    late_risk_prediction: int
    risk_label: str
    model_run_id: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }

@app.get("/shipments", response_model=list[ShipmentSummary])
def get_shipments():
    db = SessionLocal()

    try:
        rows = (
            db.query(Order, Prediction)
            .join(
                Prediction,
                Prediction.order_id == Order.order_id,
            )
            .order_by(
                Prediction.late_risk_probability.desc()
            )
            .all()
        )

        return [
            ShipmentSummary(
                order_id=order.order_id,
                customer_id=order.customer_id,
                order_date=order.order_date,
                customer_segment=order.customer_segment,
                order_country=order.order_country,
                order_region=order.order_region,
                shipping_mode=order.shipping_mode,
                late_risk_probability=prediction.late_risk_probability,
                late_risk_prediction=prediction.late_risk_prediction,
                risk_label=prediction.risk_label,
                model_run_id=prediction.model_run_id,
            )
            for order, prediction in rows
        ]

    finally:
        db.close()

@app.get("/shipments/{order_id}", response_model=ShipmentSummary)
def get_shipment(order_id: int, db: Session = Depends(get_db)):
    shipment = (
        db.query(Order, Prediction)
        .join(Prediction, Order.order_id == Prediction.order_id)
        .filter(Order.order_id == order_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found.",
        )

    order, prediction = shipment

    return ShipmentSummary(
        order_id=order.order_id,
        customer_id=order.customer_id,
        order_date=order.order_date,
        customer_segment=order.customer_segment,
        order_country=order.order_country,
        order_region=order.order_region,
        shipping_mode=order.shipping_mode,
        late_risk_probability=prediction.late_risk_probability,
        late_risk_prediction=prediction.late_risk_prediction,
        risk_label=prediction.risk_label,
        model_run_id=prediction.model_run_id,
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
)

def predict(order: OrderInput):
    input_data = pd.DataFrame(
        [
            {
                "Type": order.type,
                "Customer Segment": order.customer_segment,
                "Customer State": order.customer_state,
                "Order Country": order.order_country,
                "Order Region": order.order_region,
                "Shipping Mode": order.shipping_mode,
                "total_quantity": order.total_quantity,
                "total_discount": order.total_discount,
                "num_unique_products": order.num_unique_products,
                "num_unique_categories": order.num_unique_categories,
                "num_unique_departments": order.num_unique_departments,
                "order_hour": order.order_date.hour,
                "order_dayofweek": order.order_date.weekday(),
                "order_month": order.order_date.month,
            }
        ]
    )

    result = predict_late_risk(input_data)

    late_risk_probability = float(
        result["late_risk_probability"].iloc[0]
    )

    late_risk_prediction = int(
        result["late_risk_prediction"].iloc[0]
    )

    risk_label = result["risk_label"].iloc[0]

    model_run_id = result["model_run_id"].iloc[0]

    db = SessionLocal()

    try:

        existing_order = db.query(Order).filter(
            Order.order_id == order.order_id
        ).first()

        if existing_order:
            raise HTTPException(
                status_code=409,
                detail="Order ID already exists.",
            )

        db_order = Order(
            order_id=order.order_id,
            customer_id=order.customer_id,
            order_date=order.order_date,
            type=order.type,
            customer_segment=order.customer_segment,
            customer_state=order.customer_state,
            order_country=order.order_country,
            order_region=order.order_region,
            shipping_mode=order.shipping_mode,
            total_quantity=order.total_quantity,
            total_discount=order.total_discount,
            num_unique_products=order.num_unique_products,
            num_unique_categories=order.num_unique_categories,
            num_unique_departments=order.num_unique_departments,
            order_hour=order.order_date.hour,
            order_dayofweek=order.order_date.weekday(),
            order_month=order.order_date.month,
        )

        db_prediction = Prediction(
            order_id=order.order_id,
            late_risk_probability=late_risk_probability,
            late_risk_prediction=late_risk_prediction,
            risk_label=risk_label,
            threshold=float(
                result["threshold"].iloc[0]
            ), 
           model_run_id=model_run_id,
        )

        db.add(db_order)
        db.add(db_prediction)

        db.commit()

    except HTTPException:
        raise

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save prediction to database.",
        ) from exc
    finally:
        db.close()

    return PredictionResponse(
        order_id=order.order_id,
        late_risk_probability=late_risk_probability,
        late_risk_prediction=late_risk_prediction,
        risk_label=risk_label,
        model_run_id=model_run_id,
    )