from datetime import datetime

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.database.connection import SessionLocal, get_db
from src.database.orm_models import Order, Prediction, RawOrder
from src.features.inference import (
    prepare_order_for_inference,
    raw_order_to_item_dataframe,
)
from src.models.prediction import predict_late_risk
from src.agent.copilot import run_copilot


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


class OrderItemInput(BaseModel):
    category_id: int
    category_name: str

    department_id: int
    department_name: str

    order_item_cardprod_id: int
    order_item_discount: float = Field(ge=0)
    order_item_discount_rate: float = Field(ge=0)
    order_item_id: int
    order_item_product_price: float = Field(ge=0)
    order_item_quantity: float = Field(gt=0)
    sales: float = Field(ge=0)
    order_item_total: float = Field(ge=0)

    product_card_id: int
    product_category_id: int
    product_description: str | None = None
    product_image: str | None = None
    product_name: str
    product_price: float = Field(ge=0)
    product_status: int


class RawOrderInput(BaseModel):
    order_id: int = Field(gt=0)
    order_customer_id: int = Field(gt=0)
    order_date: datetime

    type: str
    market: str

    order_city: str
    order_country: str
    order_region: str
    order_state: str
    order_status: str
    order_zipcode: str | None = None

    shipping_mode: str
    scheduled_shipping_days: int = Field(ge=0)

    customer_id: int = Field(gt=0)
    customer_first_name: str
    customer_last_name: str
    customer_email: str
    customer_segment: str
    customer_city: str
    customer_country: str
    customer_state: str
    customer_street: str
    customer_zipcode: str | None = None
    customer_latitude: float
    customer_longitude: float

    items: list[OrderItemInput] = Field(min_length=1)


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


class CopilotRequest(BaseModel):
    question: str



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


@app.get(
    "/shipments/{order_id}",
    response_model=ShipmentSummary,
)
def get_shipment(
    order_id: int,
    db: Session = Depends(get_db),
):
    shipment = (
        db.query(Order, Prediction)
        .join(
            Prediction,
            Order.order_id == Prediction.order_id,
        )
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


@app.get("/raw-orders/{order_id}")
def get_raw_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    raw_order = (
        db.query(RawOrder)
        .filter(RawOrder.order_id == order_id)
        .first()
    )

    if raw_order is None:
        raise HTTPException(
            status_code=404,
            detail="Raw order not found.",
        )

    return {
        "id": raw_order.id,
        "order_id": raw_order.order_id,
        "raw_payload": raw_order.raw_payload,
        "received_at": raw_order.received_at,
    }


@app.get("/orders/{order_id}")
def get_processed_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Processed order not found.",
        )

    return {
        "id": order.id,
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
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
        "order_hour": order.order_hour,
        "order_dayofweek": order.order_dayofweek,
        "order_month": order.order_month,
        "created_at": order.created_at,
    }


@app.get("/predictions/{order_id}")
def get_prediction(
    order_id: int,
    db: Session = Depends(get_db),
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.order_id == order_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found.",
        )

    return {
        "id": prediction.id,
        "order_id": prediction.order_id,
        "late_risk_probability": prediction.late_risk_probability,
        "late_risk_prediction": prediction.late_risk_prediction,
        "risk_label": prediction.risk_label,
        "threshold": prediction.threshold,
        "model_run_id": prediction.model_run_id,
        "created_at": prediction.created_at,
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
        existing_order = (
            db.query(Order)
            .filter(Order.order_id == order.order_id)
            .first()
        )

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


@app.post(
    "/predict/raw",
    response_model=PredictionResponse,
)
def predict_raw_order(raw_order: RawOrderInput):
    raw_payload = raw_order.model_dump(
        mode="json"
    )

    # Step 1:
    # Save the complete original order first.
    db = SessionLocal()

    try:
        existing_raw_order = (
            db.query(RawOrder)
            .filter(
                RawOrder.order_id == raw_order.order_id
            )
            .first()
        )

        if existing_raw_order:
            raise HTTPException(
                status_code=409,
                detail="Raw order ID already exists.",
            )

        db_raw_order = RawOrder(
            order_id=raw_order.order_id,
            raw_payload=raw_payload,
        )

        db.add(db_raw_order)
        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to save raw order.",
        ) from exc

    finally:
        db.close()

    # Step 2:
    # Convert items[] into temporary item-level rows
    # and prepare one order-level representation.
    try:
        item_level_data = raw_order_to_item_dataframe(
            raw_payload
        )

        prepared_data = prepare_order_for_inference(
            item_level_data
        )

        prepared_order = OrderInput(
            **prepared_data
        )

    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=422,
            detail=(
                "Raw order was saved, but inference "
                "preparation failed."
            ),
        ) from exc

    # Step 3:
    # Save the processed order before prediction.
    db = SessionLocal()

    try:
        existing_order = (
            db.query(Order)
            .filter(
                Order.order_id == prepared_order.order_id
            )
            .first()
        )

        if existing_order:
            raise HTTPException(
                status_code=409,
                detail="Processed order ID already exists.",
            )

        db_order = Order(
            order_id=prepared_order.order_id,
            customer_id=prepared_order.customer_id,
            order_date=prepared_order.order_date,
            type=prepared_order.type,
            customer_segment=(
                prepared_order.customer_segment
            ),
            customer_state=prepared_order.customer_state,
            order_country=prepared_order.order_country,
            order_region=prepared_order.order_region,
            shipping_mode=prepared_order.shipping_mode,
            total_quantity=prepared_order.total_quantity,
            total_discount=prepared_order.total_discount,
            num_unique_products=(
                prepared_order.num_unique_products
            ),
            num_unique_categories=(
                prepared_order.num_unique_categories
            ),
            num_unique_departments=(
                prepared_order.num_unique_departments
            ),
            order_hour=prepared_order.order_date.hour,
            order_dayofweek=(
                prepared_order.order_date.weekday()
            ),
            order_month=prepared_order.order_date.month,
        )

        db.add(db_order)
        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Raw order was saved, but the processed "
                "order could not be saved."
            ),
        ) from exc

    finally:
        db.close()

    # Step 4:
    # Build the final model input from the processed order.
    input_data = pd.DataFrame(
        [
            {
                "Type": prepared_order.type,
                "Customer Segment": (
                    prepared_order.customer_segment
                ),
                "Customer State": (
                    prepared_order.customer_state
                ),
                "Order Country": (
                    prepared_order.order_country
                ),
                "Order Region": (
                    prepared_order.order_region
                ),
                "Shipping Mode": (
                    prepared_order.shipping_mode
                ),
                "total_quantity": (
                    prepared_order.total_quantity
                ),
                "total_discount": (
                    prepared_order.total_discount
                ),
                "num_unique_products": (
                    prepared_order.num_unique_products
                ),
                "num_unique_categories": (
                    prepared_order.num_unique_categories
                ),
                "num_unique_departments": (
                    prepared_order.num_unique_departments
                ),
                "order_hour": (
                    prepared_order.order_date.hour
                ),
                "order_dayofweek": (
                    prepared_order.order_date.weekday()
                ),
                "order_month": (
                    prepared_order.order_date.month
                ),
            }
        ]
    )

    # Step 5:
    # Run the already-trained model.
    try:
        result = predict_late_risk(
            input_data
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Raw and processed orders were saved, "
                "but prediction failed."
            ),
        ) from exc

    late_risk_probability = float(
        result["late_risk_probability"].iloc[0]
    )

    late_risk_prediction = int(
        result["late_risk_prediction"].iloc[0]
    )

    risk_label = result["risk_label"].iloc[0]
    model_run_id = result["model_run_id"].iloc[0]

    # Step 6:
    # Save prediction separately.
    db = SessionLocal()

    try:
        existing_prediction = (
            db.query(Prediction)
            .filter(
                Prediction.order_id
                == prepared_order.order_id
            )
            .first()
        )

        if existing_prediction:
            raise HTTPException(
                status_code=409,
                detail="Prediction already exists.",
            )

        db_prediction = Prediction(
            order_id=prepared_order.order_id,
            late_risk_probability=late_risk_probability,
            late_risk_prediction=late_risk_prediction,
            risk_label=risk_label,
            threshold=float(
                result["threshold"].iloc[0]
            ),
            model_run_id=model_run_id,
        )

        db.add(db_prediction)
        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Prediction succeeded, but the result "
                "could not be saved."
            ),
        ) from exc

    finally:
        db.close()

    return PredictionResponse(
        order_id=prepared_order.order_id,
        late_risk_probability=late_risk_probability,
        late_risk_prediction=late_risk_prediction,
        risk_label=risk_label,
        model_run_id=model_run_id,
    )


@app.post("/copilot")
def copilot(request: CopilotRequest):
    return run_copilot(request.question)


