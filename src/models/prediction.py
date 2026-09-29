from pathlib import Path
import json

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODELS_DIR / "xgboost_stage2.joblib"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
METADATA_PATH = MODELS_DIR / "model_metadata.json"


def load_inference_artifacts():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    threshold = metadata["threshold"]

    return model, preprocessor, threshold


def predict_late_risk(
    input_data: pd.DataFrame,
) -> pd.DataFrame:
    model, preprocessor, threshold = load_inference_artifacts()

    prepared_data = preprocessor.transform(input_data)

    probabilities = model.predict_proba(prepared_data)[:, 1]

    predictions = (
        probabilities >= threshold
    ).astype(int)

    results = input_data.copy()

    results["late_risk_probability"] = probabilities
    results["late_risk_prediction"] = predictions

    results["risk_label"] = results[
        "late_risk_prediction"
    ].map({
        0: "Not Late",
        1: "Late",
    })

    return results