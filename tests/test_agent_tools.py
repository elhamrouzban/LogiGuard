from src.agent.tools import get_shipment
from src.agent.tools import get_prediction

from src.agent.tools import (
    find_similar_shipments,
    get_prediction,
    get_shipment,
)



def test_get_shipment_returns_order_and_prediction():
    shipment = get_shipment(900002)

    assert shipment is not None
    assert shipment["order_id"] == 900002

    assert "customer_id" in shipment
    assert "shipping_mode" in shipment

    assert "late_risk_probability" in shipment
    assert "late_risk_prediction" in shipment
    assert "risk_label" in shipment
    assert "model_run_id" in shipment



def test_get_prediction_returns_prediction_details():
    prediction = get_prediction(900002)

    assert prediction is not None
    assert prediction["order_id"] == 900002

    assert "late_risk_probability" in prediction
    assert "late_risk_prediction" in prediction
    assert "risk_label" in prediction
    assert "threshold" in prediction
    assert "model_run_id" in prediction
    assert "created_at" in prediction



def test_find_similar_shipments_returns_list():
    similar = find_similar_shipments(
        900002,
        limit=5,
    )

    assert isinstance(similar, list)
    assert len(similar) <= 5

    for shipment in similar:
        assert shipment["order_id"] != 900002
        assert "late_risk_probability" in shipment
        assert "risk_label" in shipment
        assert "probability_distance" in shipment