import pandas as pd

from src.data.cleaning import INVALID_STATE_MAP


RAW_REQUIRED_COLUMNS = [
    "Type",
    "Category Id",
    "Customer Segment",
    "Customer State",
    "Department Name",
    "Order Country",
    "Order Item Discount",
    "Order Item Quantity",
    "Order Region",
    "Product Name",
    "Shipping Mode",
    "Customer Id",
    "Order Id",
    "order date (DateOrders)",
]


def prepare_order_for_inference(raw_order: pd.DataFrame) -> dict:
    if raw_order.empty:
        raise ValueError("Order data is empty.")

    missing_columns = [
        column
        for column in RAW_REQUIRED_COLUMNS
        if column not in raw_order.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if raw_order["Order Id"].nunique() != 1:
        raise ValueError(
            "Input must contain exactly one Order Id."
        )

    order_df = raw_order[RAW_REQUIRED_COLUMNS].copy()

    order_df["order date (DateOrders)"] = pd.to_datetime(
        order_df["order date (DateOrders)"],
        errors="raise",
    )

    order_df["Customer State"] = (
        order_df["Customer State"]
        .astype("string")
        .replace(INVALID_STATE_MAP)
    )

    aggregated = (
        order_df
        .groupby("Order Id", as_index=False)
        .agg(
            {
                "Type": "first",
                "Customer Segment": "first",
                "Customer State": "first",
                "Order Country": "first",
                "Order Region": "first",
                "Shipping Mode": "first",
                "Customer Id": "first",
                "order date (DateOrders)": "first",
                "Order Item Quantity": "sum",
                "Order Item Discount": "sum",
                "Product Name": "nunique",
                "Category Id": "nunique",
                "Department Name": "nunique",
            }
        )
    )

    row = aggregated.iloc[0]

    return {
        "order_id": int(row["Order Id"]),
        "customer_id": int(row["Customer Id"]),
        "order_date": row["order date (DateOrders)"].isoformat(),
        "type": row["Type"],
        "customer_segment": row["Customer Segment"],
        "customer_state": row["Customer State"],
        "order_country": row["Order Country"],
        "order_region": row["Order Region"],
        "shipping_mode": row["Shipping Mode"],
        "total_quantity": float(
            row["Order Item Quantity"]
        ),
        "total_discount": float(
            row["Order Item Discount"]
        ),
        "num_unique_products": int(
            row["Product Name"]
        ),
        "num_unique_categories": int(
            row["Category Id"]
        ),
        "num_unique_departments": int(
            row["Department Name"]
        ),
    }