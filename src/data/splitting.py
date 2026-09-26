import pandas as pd


def time_based_split(
    order_level_df: pd.DataFrame,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
):
    """Split order-level data chronologically into train, validation, and test sets."""

    df = (
        order_level_df
        .sort_values("order date (DateOrders)")
        .reset_index(drop=True)
    )

    n = len(df)

    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    return train_df, val_df, test_df