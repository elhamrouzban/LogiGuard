from datetime import datetime

from src.api.main import RawOrderInput


def test_raw_order_schema_accepts_valid_order():
    order = RawOrderInput(
        order_id=75939,
        order_customer_id=19492,
        order_date=datetime(2018, 1, 13, 12, 27),
        type="TRANSFER",
        market="Pacific Asia",
        order_city="Bikaner",
        order_country="India",
        order_region="South Asia",
        order_state="Rajasthan",
        order_status="PENDING",
        order_zipcode=None,
        shipping_mode="Standard Class",
        scheduled_shipping_days=4,
        customer_id=19492,
        customer_first_name="Irene",
        customer_last_name="Luna",
        customer_email="example@example.com",
        customer_segment="Consumer",
        customer_city="Caguas",
        customer_country="Puerto Rico",
        customer_state="PR",
        customer_street="2679 Rustic Loop",
        customer_zipcode="725",
        customer_latitude=18.27945137,
        customer_longitude=-66.0370636,
        items=[
            {
                "category_id": 73,
                "category_name": "Sporting Goods",
                "department_id": 2,
                "department_name": "Fitness",
                "order_item_cardprod_id": 1360,
                "order_item_discount": 16.39,
                "order_item_discount_rate": 0.05,
                "order_item_id": 179254,
                "order_item_product_price": 327.75,
                "order_item_quantity": 1,
                "sales": 327.75,
                "order_item_total": 311.36,
                "product_card_id": 1360,
                "product_category_id": 73,
                "product_description": None,
                "product_image": None,
                "product_name": "Smart watch",
                "product_price": 327.75,
                "product_status": 0,
            }
        ],
    )

    assert order.order_id == 75939
    assert len(order.items) == 1
    assert order.items[0].product_name == "Smart watch"