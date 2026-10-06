import pandas as pd

from src.features.inference import prepare_order_for_inference


def test_prepare_order_for_inference_aggregates_multiple_items():
    raw_order = pd.DataFrame(
        [
            {
                "Type": "DEBIT",
                "Category Id": 10,
                "Customer Segment": "Consumer",
                "Customer State": "CA",
                "Department Name": "Fitness",
                "Order Country": "Germany",
                "Order Item Discount": 5.0,
                "Order Item Quantity": 2,
                "Order Region": "Western Europe",
                "Product Name": "Product A",
                "Shipping Mode": "Standard Class",
                "Customer Id": 100,
                "Order Id": 500,
                "order date (DateOrders)": "2026-10-06T17:38:31.647Z",
            },
            {
                "Type": "DEBIT",
                "Category Id": 20,
                "Customer Segment": "Consumer",
                "Customer State": "CA",
                "Department Name": "Outdoors",
                "Order Country": "Germany",
                "Order Item Discount": 3.0,
                "Order Item Quantity": 1,
                "Order Region": "Western Europe",
                "Product Name": "Product B",
                "Shipping Mode": "Standard Class",
                "Customer Id": 100,
                "Order Id": 500,
                "order date (DateOrders)": "2026-10-06T17:38:31.647Z",
            },
        ]
    )

    result = prepare_order_for_inference(raw_order)

    assert result["order_id"] == 500
    assert result["customer_id"] == 100
    assert result["total_quantity"] == 3.0
    assert result["total_discount"] == 8.0
    assert result["num_unique_products"] == 2
    assert result["num_unique_categories"] == 2
    assert result["num_unique_departments"] == 2