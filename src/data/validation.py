import numpy as np
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


NUMERIC_COLUMNS = [
    "Category Id",
    "Order Item Discount",
    "Order Item Quantity",
    "Customer Id",
    "Order Id",
]


TEXT_COLUMNS = [
    "Type",
    "Customer Segment",
    "Customer State",
    "Department Name",
    "Order Country",
    "Order Region",
    "Product Name",
    "Shipping Mode",
]


def validate_raw_data(df: pd.DataFrame) -> None:
    """Validate critical assumptions before cleaning."""

    if df.empty:
        raise ValueError("Raw dataset is empty.")

    _validate_required_columns(df)
    _validate_missing_values(df)
    _validate_numeric_columns(df)
    _validate_text_columns(df)
    _validate_target(df)
    _validate_date_column(df)
    _validate_numeric_ranges(df)


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def _validate_missing_values(df: pd.DataFrame) -> None:
    missing_counts = df[REQUIRED_COLUMNS].isna().sum()
    invalid = missing_counts[missing_counts > 0]

    if not invalid.empty:
        raise ValueError(
            "Missing values found in required columns: "
            f"{invalid.to_dict()}"
        )


def _validate_numeric_columns(df: pd.DataFrame) -> None:
    for column in NUMERIC_COLUMNS:
        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce",
        )

        invalid_mask = numeric_values.isna()

        if invalid_mask.any():
            raise ValueError(
                f"Column '{column}' contains "
                f"{invalid_mask.sum()} non-numeric value(s)."
            )

        if not np.isfinite(numeric_values).all():
            raise ValueError(
                f"Column '{column}' contains infinite values."
            )


def _validate_text_columns(df: pd.DataFrame) -> None:
    for column in TEXT_COLUMNS:
        values = df[column].astype("string").str.strip()

        if values.eq("").any():
            raise ValueError(
                f"Column '{column}' contains blank values."
            )


def _validate_target(df: pd.DataFrame) -> None:
    target = pd.to_numeric(
        df["Late_delivery_risk"],
        errors="coerce",
    )

    if target.isna().any():
        raise ValueError(
            "Late_delivery_risk contains invalid values."
        )

    invalid_targets = set(target.unique()) - {0, 1}

    if invalid_targets:
        raise ValueError(
            f"Invalid target values: {invalid_targets}"
        )


def _validate_date_column(df: pd.DataFrame) -> None:
    parsed_dates = pd.to_datetime(
        df["order date (DateOrders)"],
        errors="coerce",
    )

    invalid_count = parsed_dates.isna().sum()

    if invalid_count:
        raise ValueError(
            "order date (DateOrders) contains "
            f"{invalid_count} invalid date value(s)."
        )


def _validate_numeric_ranges(df: pd.DataFrame) -> None:
    quantity = pd.to_numeric(
        df["Order Item Quantity"],
        errors="raise",
    )

    discount = pd.to_numeric(
        df["Order Item Discount"],
        errors="raise",
    )

    order_id = pd.to_numeric(
        df["Order Id"],
        errors="raise",
    )

    customer_id = pd.to_numeric(
        df["Customer Id"],
        errors="raise",
    )

    if (quantity < 0).any():
        raise ValueError(
            "Order Item Quantity contains negative values."
        )

    if (discount < 0).any():
        raise ValueError(
            "Order Item Discount contains negative values."
        )

    if (order_id <= 0).any():
        raise ValueError(
            "Order Id must contain positive values."
        )

    if (customer_id <= 0).any():
        raise ValueError(
            "Customer Id must contain positive values."
        )