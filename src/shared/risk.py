def get_risk_level(probability: float) -> str:
    if probability < 0.40:
        return "No Risk"

    if probability < 0.60:
        return "Low Risk"

    if probability < 0.80:
        return "Medium Risk"

    return "High Risk"