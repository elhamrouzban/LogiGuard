from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.models.prediction import predict_late_risk


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