from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from src.models.prediction import predict_late_risk


app = FastAPI(
    title="LogiGuard API",
    version="0.1.0",
)


class OrderInput(BaseModel):
    Type: str
    Customer_Segment: str
    Customer_State: str
    Order_Country: str
    Order_Region: str
    Shipping_Mode: str

    total_quantity: float
    total_discount: float

    num_unique_products: int
    num_unique_categories: int
    num_unique_departments: int

    order_hour: int
    order_dayofweek: int
    order_month: int


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.post("/predict")
def predict(order: OrderInput):
    input_data = pd.DataFrame(
        [
            {
                "Type": order.Type,
                "Customer Segment": order.Customer_Segment,
                "Customer State": order.Customer_State,
                "Order Country": order.Order_Country,
                "Order Region": order.Order_Region,
                "Shipping Mode": order.Shipping_Mode,
                "total_quantity": order.total_quantity,
                "total_discount": order.total_discount,
                "num_unique_products": order.num_unique_products,
                "num_unique_categories": order.num_unique_categories,
                "num_unique_departments": order.num_unique_departments,
                "order_hour": order.order_hour,
                "order_dayofweek": order.order_dayofweek,
                "order_month": order.order_month,
            }
        ]
    )

    result = predict_late_risk(input_data)

    return {
        "late_risk_probability": float(
            result["late_risk_probability"].iloc[0]
        ),
        "late_risk_prediction": int(
            result["late_risk_prediction"].iloc[0]
        ),
        "risk_label": result["risk_label"].iloc[0],
    }