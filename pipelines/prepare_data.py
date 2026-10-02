from datetime import datetime
from pathlib import Path

from src.data.aggregation import aggregate_to_order_level
from src.data.cleaning import load_and_clean_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main():
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    run_dir = PROCESSED_DATA_DIR / run_timestamp
    processed_data_path = (
        run_dir / f"order_level_clean_{run_timestamp}.csv"
    )

    df_clean = load_and_clean_data()
    order_df = aggregate_to_order_level(df_clean)

    run_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    order_df.to_csv(
        processed_data_path,
        index=False,
    )

    print("\nProcessed dataset created")
    print("-------------------------")
    print(f"Rows: {len(order_df)}")
    print(f"Path: {processed_data_path}")


if __name__ == "__main__":
    main()