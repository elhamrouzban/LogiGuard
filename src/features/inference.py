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


def raw_order_to_item_dataframe(raw_order: dict) -> pd.DataFrame:
    items = raw_order.get("items", [])

    if not items:
        raise ValueError("Raw order must contain at least one item.")

    rows = []

    for item in items:
        rows.append(
            {
                "Type": raw_order["type"],
                "Category Id": item["category_id"],
                "Customer Segment": raw_order["customer_segment"],
                "Customer State": raw_order["customer_state"],
                "Department Name": item["department_name"],
                "Order Country": raw_order["order_country"],
                "Order Item Discount": item["order_item_discount"],
                "Order Item Quantity": item["order_item_quantity"],
                "Order Region": raw_order["order_region"],
                "Product Name": item["product_name"],
                "Shipping Mode": raw_order["shipping_mode"],
                "Customer Id": raw_order["customer_id"],
                "Order Id": raw_order["order_id"],
                "order date (DateOrders)": raw_order["order_date"],
            }
        )

    return pd.DataFrame(rows)


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

    required_values = raw_order[RAW_REQUIRED_COLUMNS]

    if required_values.isna().any().any():
        raise ValueError(
            "Missing values found in required order fields."
        )

    if (
        pd.to_numeric(
            raw_order["Order Item Quantity"],
            errors="raise",
        )
        < 0
    ).any():
        raise ValueError(
            "Order Item Quantity contains negative values."
        )

    if (
        pd.to_numeric(
            raw_order["Order Item Discount"],
            errors="raise",
        )
        < 0
    ).any():
        raise ValueError(
            "Order Item Discount contains negative values."
        )

    if (
        pd.to_numeric(
            raw_order["Order Id"],
            errors="raise",
        )
        <= 0
    ).any():
        raise ValueError(
            "Order Id must contain positive values."
        )

    if (
        pd.to_numeric(
            raw_order["Customer Id"],
            errors="raise",
        )
        <= 0
    ).any():
        raise ValueError(
            "Customer Id must contain positive values."
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
        "order_date": row[
            "order date (DateOrders)"
        ].isoformat(),
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