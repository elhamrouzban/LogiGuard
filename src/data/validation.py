import pandas as pd


REQUIRED_COLUMNS = [
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
    "Late_delivery_risk",
]


def validate_raw_data(df: pd.DataFrame) -> None:
    """Validate critical assumptions before cleaning."""

    if df.empty:
        raise ValueError("Raw dataset is empty.")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    invalid_targets = set(
        df["Late_delivery_risk"].dropna().unique()
    ) - {0, 1}

    if invalid_targets:
        raise ValueError(
            f"Invalid target values: {invalid_targets}"
        )

    if df["Late_delivery_risk"].isna().any():
        raise ValueError(
            "Late_delivery_risk contains missing values."
        )

    if df["Order Id"].isna().any():
        raise ValueError(
            "Order Id contains missing values."
        )

    if df["Customer Id"].isna().any():
        raise ValueError(
            "Customer Id contains missing values."
        )

    if (pd.to_numeric(
        df["Order Item Quantity"],
        errors="coerce",
    ) < 0).any():
        raise ValueError(
            "Order Item Quantity contains negative values."
        )

    if (pd.to_numeric(
        df["Order Item Discount"],
        errors="coerce",
    ) < 0).any():
        raise ValueError(
            "Order Item Discount contains negative values."
        )