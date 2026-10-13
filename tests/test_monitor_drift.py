import pytest

from pipelines.monitor_drift import load_current, load_model_metadata


def test_model_metadata_matches_active_model():
    metadata = load_model_metadata()

    assert metadata["run_id"]
    assert len(metadata["feature_columns"]) == 14


def test_current_data_matches_model_features():
    metadata = load_model_metadata()
    current = load_current(metadata)

    expected_columns = (
        metadata["feature_columns"]
        + ["late_risk_probability"]
    )

    assert list(current.columns) == expected_columns
    assert current["late_risk_probability"].between(0, 1).all()