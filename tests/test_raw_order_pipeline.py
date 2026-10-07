from fastapi.testclient import TestClient

import src.api.main as api_main
from src.api.main import app
from src.database.connection import SessionLocal
from src.database.orm_models import Order, Prediction, RawOrder


client = TestClient(app)

TEST_ORDER_ID = 990001


def _cleanup_test_order():
    db = SessionLocal()

    try:
        db.query(Prediction).filter(
            Prediction.order_id == TEST_ORDER_ID
        ).delete()

        db.query(Order).filter(
            Order.order_id == TEST_ORDER_ID
        ).delete()

        db.query(RawOrder).filter(
            RawOrder.order_id == TEST_ORDER_ID
        ).delete()

        db.commit()

    finally:
        db.close()


def test_raw_and_processed_orders_remain_when_prediction_fails(
    monkeypatch,
):
    _cleanup_test_order()

    raw_order_payload = {
        "order_id": TEST_ORDER_ID,
        "order_customer_id": 19492,
        "order_date": "2018-01-13T12:27:00",
        "type": "TRANSFER",
        "market": "Pacific Asia",
        "order_city": "Bikaner",
        "order_country": "India",
        "order_region": "South Asia",
        "order_state": "Rajasthan",
        "order_status": "PENDING",
        "order_zipcode": None,
        "shipping_mode": "Standard Class",
        "scheduled_shipping_days": 4,
        "customer_id": 19492,
        "customer_first_name": "Irene",
        "customer_last_name": "Luna",
        "customer_email": "irene.luna@example.com",
        "customer_segment": "Consumer",
        "customer_city": "Caguas",
        "customer_country": "Puerto Rico",
        "customer_state": "PR",
        "customer_street": "2679 Rustic Loop",
        "customer_zipcode": "725",
        "customer_latitude": 18.27945137,
        "customer_longitude": -66.0370636,
        "items": [
            {
                "category_id": 73,
                "category_name": "Sporting Goods",
                "department_id": 2,
                "department_name": "Fitness",
                "order_item_cardprod_id": 1360,
                "order_item_discount": 10.0,
                "order_item_discount_rate": 0.03,
                "order_item_id": 9900011,
                "order_item_product_price": 327.75,
                "order_item_quantity": 1,
                "sales": 327.75,
                "order_item_total": 317.75,
                "product_card_id": 1360,
                "product_category_id": 73,
                "product_description": None,
                "product_image": None,
                "product_name": "Product A",
                "product_price": 327.75,
                "product_status": 0,
            },
            {
                "category_id": 73,
                "category_name": "Sporting Goods",
                "department_id": 2,
                "department_name": "Fitness",
                "order_item_cardprod_id": 1361,
                "order_item_discount": 5.0,
                "order_item_discount_rate": 0.02,
                "order_item_id": 9900012,
                "order_item_product_price": 150.0,
                "order_item_quantity": 2,
                "sales": 300.0,
                "order_item_total": 295.0,
                "product_card_id": 1361,
                "product_category_id": 73,
                "product_description": None,
                "product_image": None,
                "product_name": "Product B",
                "product_price": 150.0,
                "product_status": 0,
            },
        ],
    }

    def failing_prediction(_input_data):
        raise RuntimeError("Simulated prediction failure")

    monkeypatch.setattr(
        api_main,
        "predict_late_risk",
        failing_prediction,
    )

    try:
        response = client.post(
            "/predict/raw",
            json=raw_order_payload,
        )

        assert response.status_code == 500
        assert response.json() == {
            "detail": (
                "Raw and processed orders were saved, "
                "but prediction failed."
            )
        }

        db = SessionLocal()

        try:
            raw_order = (
                db.query(RawOrder)
                .filter(RawOrder.order_id == TEST_ORDER_ID)
                .first()
            )

            processed_order = (
                db.query(Order)
                .filter(Order.order_id == TEST_ORDER_ID)
                .first()
            )

            prediction = (
                db.query(Prediction)
                .filter(
                    Prediction.order_id == TEST_ORDER_ID
                )
                .first()
            )

            assert raw_order is not None
            assert processed_order is not None
            assert prediction is None

            assert processed_order.total_quantity == 3
            assert processed_order.total_discount == 15
            assert processed_order.num_unique_products == 2

        finally:
            db.close()

    finally:
        _cleanup_test_order()