from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"
CURRENT_MODEL_PATH = MODEL_DIR / "current_model.json"


def main():
    run_id = input("Enter model run ID to promote: ").strip()

    run_dir = MODEL_DIR / run_id

    if not run_dir.exists():
        raise FileNotFoundError(
            f"Model run not found: {run_dir}"
        )

    model_files = list(run_dir.glob("xgboost_stage2_*.joblib"))
    preprocessor_files = list(run_dir.glob("preprocessor_*.joblib"))
    metadata_files = list(run_dir.glob("model_metadata_*.json"))

    if len(model_files) != 1:
        raise ValueError("Expected exactly one model file.")

    if len(preprocessor_files) != 1:
        raise ValueError("Expected exactly one preprocessor file.")

    if len(metadata_files) != 1:
        raise ValueError("Expected exactly one metadata file.")

    metadata_path = metadata_files[0]

    with open(
        metadata_path,
        "r",
        encoding="utf-8",
    ) as file:
        metadata = json.load(file)

    validation_metrics = metadata["validation_metrics"]

    if validation_metrics["roc_auc"] < 0.75:
        raise ValueError(
            "Model quality check failed: validation ROC-AUC is below 0.75."
        )

    current_model = {
        "run_id": run_id,
        "run_directory": run_id,
        "model": str(
            Path(run_id) / model_files[0].name
        ),
        "preprocessor": str(
            Path(run_id) / preprocessor_files[0].name
        ),
        "metadata": str(
            Path(run_id) / metadata_files[0].name
        ),
    }

    with open(
        CURRENT_MODEL_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            current_model,
            file,
            indent=4,
        )

    print("\nModel promoted")
    print("--------------")
    print(f"Run ID: {run_id}")
    print(f"Pointer: {CURRENT_MODEL_PATH}")


if __name__ == "__main__":
    main()