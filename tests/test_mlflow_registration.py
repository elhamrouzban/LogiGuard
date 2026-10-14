import json
from unittest.mock import MagicMock, patch

from pipelines import register_existing_model_mlflow as registration


def test_register_existing_model_mlflow(tmp_path, monkeypatch):
    models_dir = tmp_path / "models"
    run_dir = models_dir / "test-run"
    run_dir.mkdir(parents=True)

    manifest = {
        "run_id": "test-run",
        "metadata": "test-run/metadata.json",
    }
    metadata = {
        "run_id": "test-run",
        "model_name": "Test XGBoost",
        "threshold": 0.4,
        "hyperparameters": {"max_depth": 5, "learning_rate": 0.07},
        "validation_metrics": {
            "roc_auc": 0.77,
            "confusion_matrix": [[2, 1], [1, 3]],
        },
        "test_metrics": {"roc_auc": 0.78},
        "training_data": {
            "file": "training.csv",
            "path": "data/processed/training.csv",
            "sha256": "example-hash",
        },
    }

    (models_dir / "current_model.json").write_text(json.dumps(manifest))
    (run_dir / "metadata.json").write_text(json.dumps(metadata))

    monkeypatch.setattr(registration, "MODEL_DIR", models_dir)
    monkeypatch.setattr(registration, "MLFLOW_DB", tmp_path / "mlflow.db")

    fake_run = MagicMock()
    fake_run.info.run_id = "test-mlflow-run"

    with (
        patch.object(registration.mlflow, "set_tracking_uri") as tracking,
        patch.object(registration.mlflow, "set_experiment") as experiment,
        patch.object(registration.mlflow, "start_run") as start_run,
        patch.object(registration.mlflow, "log_params") as log_params,
        patch.object(registration.mlflow, "log_param") as log_param,
        patch.object(registration.mlflow, "log_metric") as log_metric,
        patch.object(registration.mlflow, "set_tag") as set_tag,
        patch.object(registration.mlflow, "log_artifact") as log_artifact,
    ):
        start_run.return_value.__enter__.return_value = fake_run

        registration.main()

    tracking.assert_called_once()
    experiment.assert_called_once_with("LogiGuard-XGBoost")
    log_params.assert_called_once_with(metadata["hyperparameters"])
    log_param.assert_called_once_with("threshold", 0.4)
    log_metric.assert_any_call("validation_roc_auc", 0.77)
    log_metric.assert_any_call("test_roc_auc", 0.78)
    assert log_metric.call_count == 2
    set_tag.assert_any_call("training_data_sha256", "example-hash")
    log_artifact.assert_called_once()