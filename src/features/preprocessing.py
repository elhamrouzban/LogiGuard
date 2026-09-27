import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TARGET = "Late_delivery_risk"
RARE_THRESHOLD = 50

CATEGORICAL_FEATURES = [
    "Type",
    "Customer Segment",
    "Customer State",
    "Order Country",
    "Order Region",
    "Shipping Mode",
]

NUMERIC_FEATURES = [
    "total_quantity",
    "total_discount",
    "num_unique_products",
    "num_unique_categories",
    "num_unique_departments",
    "order_hour",
    "order_dayofweek",
    "order_month",
]


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based features from the order timestamp."""

    df = df.copy()

    df["order_hour"] = df["order date (DateOrders)"].dt.hour
    df["order_dayofweek"] = df["order date (DateOrders)"].dt.dayofweek
    df["order_month"] = df["order date (DateOrders)"].dt.month

    return df


def learn_rare_countries(train_df: pd.DataFrame):
    """Learn rare Order Country categories from the training data only."""

    country_counts = train_df["Order Country"].value_counts()

    rare_countries = country_counts[
        country_counts < RARE_THRESHOLD
    ].index

    return rare_countries


def group_rare_countries(
    df: pd.DataFrame,
    rare_countries,
) -> pd.DataFrame:
    """Map only train-identified rare countries to Other."""

    df = df.copy()

    df["Order Country"] = df["Order Country"].where(
        ~df["Order Country"].isin(rare_countries),
        "Other",
    )

    return df


def build_preprocessor() -> ColumnTransformer:
    """Build the model preprocessing transformer."""

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                StandardScaler(),
                NUMERIC_FEATURES,
            ),
        ]
    )