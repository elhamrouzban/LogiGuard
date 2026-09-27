import pandas as pd


def aggregate_to_order_level(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Aggregate cleaned item-level data to one row per Order Id."""

    order_level_df = (
        df_clean
        .groupby("Order Id", as_index=False)
        .agg({
            "Type": "first",
            "Customer Segment": "first",
            "Customer State": "first",
            "Order Country": "first",
            "Order Region": "first",
            "Shipping Mode": "first",
            "Customer Id": "first",
            "order date (DateOrders)": "first",
            "Late_delivery_risk": "first",
            "Order Item Quantity": "sum",
            "Order Item Discount": "sum",
            "Product Name": "nunique",
            "Category Id": "nunique",
            "Department Name": "nunique",
        })
    )

    order_level_df = order_level_df.rename(
        columns={
            "Order Item Quantity": "total_quantity",
            "Order Item Discount": "total_discount",
            "Product Name": "num_unique_products",
            "Category Id": "num_unique_categories",
            "Department Name": "num_unique_departments",
        }
    )

    return order_level_df