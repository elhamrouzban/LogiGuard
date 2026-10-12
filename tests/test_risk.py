from src.shared.risk import get_risk_level


def test_get_risk_level_boundaries():
    assert get_risk_level(0.00) == "No Risk"
    assert get_risk_level(0.39) == "No Risk"

    assert get_risk_level(0.40) == "Low Risk"
    assert get_risk_level(0.59) == "Low Risk"

    assert get_risk_level(0.60) == "Medium Risk"
    assert get_risk_level(0.79) == "Medium Risk"

    assert get_risk_level(0.80) == "High Risk"
    assert get_risk_level(1.00) == "High Risk"