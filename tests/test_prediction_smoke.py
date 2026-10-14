import pandas as pd

from src.models.prediction import predict_late_risk

def test_prediction_smoke():

    sample_order = pd.DataFrame(
        [
            {
                "Type": "DEBIT",
                "Customer Segment": "Consumer",
                "Customer State": "CA",
                "Order Country": "United States",
                "Order Region": "West of USA",
                "Shipping Mode": "Standard Class",
                "total_quantity": 1,
                "total_discount": 0.0,
                "num_unique_products": 1,
                "num_unique_categories": 1,
                "num_unique_departments": 1,
                "order_hour": 10,
                "order_dayofweek": 2,
                "order_month": 6,
            }
        ]
    )

    result = predict_late_risk(sample_order)

    print(
        result[
            [
                "late_risk_probability",
                "late_risk_prediction",
                "risk_label",
            ]
        ]
    )