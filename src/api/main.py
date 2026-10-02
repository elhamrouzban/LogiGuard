from datetime import datetime

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.models.prediction import predict_late_risk


app = FastAPI(
    title="LogiGuard API",
    version="0.2.0",
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


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


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

    return PredictionResponse(
        order_id=order.order_id,
        late_risk_probability=float(
            result["late_risk_probability"].iloc[0]
        ),
        late_risk_prediction=int(
            result["late_risk_prediction"].iloc[0]
        ),
        risk_label=result["risk_label"].iloc[0],
        model_run_id=result["model_run_id"].iloc[0],
    )