import json
from pathlib import Path

import mlflow


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"
MLFLOW_DB = PROJECT_ROOT / "mlflow.db"

def main():
    manifest = json.loads(
        (MODEL_DIR / "current_model.json").read_text(encoding="utf-8")
    )

    metadata_path = MODEL_DIR / manifest["metadata"]
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    if metadata["run_id"] != manifest["run_id"]:
        raise ValueError("Model manifest and metadata do not match.")

    mlflow.set_tracking_uri(f"sqlite:///{MLFLOW_DB}")
    mlflow.set_experiment("LogiGuard-XGBoost")

    with mlflow.start_run(
        run_name=metadata["run_id"],
        tags={
            "source_run_id": metadata["run_id"],
            "registration_type": "historical_import",
            "model_name": metadata["model_name"],
        },
    ) as run:
        mlflow.log_params(metadata["hyperparameters"])
        mlflow.log_param("threshold", metadata["threshold"])

        for split in ("validation", "test"):
            for name, value in metadata[f"{split}_metrics"].items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    mlflow.log_metric(f"{split}_{name}", value)

        training_data = metadata.get("training_data", {})

        for key in ("file", "path", "sha256"):
            if key in training_data:
                mlflow.set_tag(f"training_data_{key}", training_data[key])

        mlflow.log_artifact(str(metadata_path), artifact_path="metadata")

        print("MLflow registration: PASS")
        print("Source model:", metadata["run_id"])
        print("MLflow run:", run.info.run_id)


if __name__ == "__main__":
    main()