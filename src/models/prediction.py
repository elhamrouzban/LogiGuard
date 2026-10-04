from pathlib import Path
import json

import joblib
import pandas as pd

from src.features.preprocessing import group_rare_countries


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "models"

CURRENT_MODEL_PATH = MODELS_DIR / "current_model.json"


def load_inference_artifacts():
    with open(
        CURRENT_MODEL_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        current_model = json.load(file)

    model_path = MODELS_DIR / current_model["model"]
    preprocessor_path = MODELS_DIR / current_model["preprocessor"]
    metadata_path = MODELS_DIR / current_model["metadata"]

    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)

    with open(
        metadata_path,
        "r",
        encoding="utf-8",
    ) as file:
        metadata = json.load(file)

    return model, preprocessor, metadata


def predict_late_risk(
    input_data: pd.DataFrame,
) -> pd.DataFrame:
    model, preprocessor, metadata = load_inference_artifacts()

    threshold = metadata["threshold"]
    rare_countries = metadata["rare_countries"]

    prepared_input = group_rare_countries(
        input_data,
        rare_countries,
    )

    prepared_data = preprocessor.transform(prepared_input)

    probabilities = model.predict_proba(prepared_data)[:, 1]

    predictions = (
        probabilities >= threshold
    ).astype(int)

    results = input_data.copy()

    results["late_risk_probability"] = probabilities
    results["late_risk_prediction"] = predictions

    results["risk_label"] = results[
        "late_risk_prediction"
    ].map(
        {
            0: "Not Late",
            1: "Late",
        }
    )

    results["model_run_id"] = metadata["run_id"]
    results["threshold"] = threshold

    return results