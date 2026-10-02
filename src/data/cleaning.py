from pathlib import Path

import pandas as pd

from src.data.validation import validate_raw_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "DataCoSupplyChainDataset.csv"

TARGET = "Late_delivery_risk"

MODEL_FEATURES = [
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
]

TECHNICAL_COLUMNS = [
    "Customer Id",
    "Order Id",
    "order date (DateOrders)",
]

KEEP_COLUMNS = MODEL_FEATURES + TECHNICAL_COLUMNS + [TARGET]

INVALID_STATE_MAP = {
    "91732": "CA",
    "95758": "CA",
}


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the original DataCo dataset."""

    return pd.read_csv(
        path,
        encoding="ISO-8859-1",
    )


def clean_item_level_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the finalized item-level cleaning decisions."""

    df_clean = df[KEEP_COLUMNS].copy()

    df_clean["order date (DateOrders)"] = pd.to_datetime(
        df_clean["order date (DateOrders)"],
        errors="raise",
    )

    df_clean["Customer State"] = (
        df_clean["Customer State"]
        .astype("string")
        .replace(INVALID_STATE_MAP)
    )

    return df_clean


def load_and_clean_data(
    path: Path = RAW_DATA_PATH,
) -> pd.DataFrame:
    """Load, validate, and clean the raw item-level dataset."""

    df = load_raw_data(path)

    validate_raw_data(df)

    return clean_item_level_data(df)