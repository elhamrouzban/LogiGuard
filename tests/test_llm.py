from src.agent.llm import generate_grounded_response


def test_generate_grounded_response_uses_validated_evidence(
    monkeypatch,
):
    class FakeResponse:
        text = (
            "Order 900002 is currently No Risk for late delivery, "
            "with a predicted risk of 34%."
        )

    class FakeModels:
        def generate_content(
            self,
            model,
            contents,
        ):
            assert "900002" in contents
            assert "0.34" in contents
            assert "No Risk" in contents
            assert "Do not derive a different risk level yourself." in contents

            return FakeResponse()

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "test-key"
            self.models = FakeModels()

    monkeypatch.setenv(
        "GEMINI_API_KEY",
        "test-key",
    )

    monkeypatch.setattr(
        "src.agent.llm.genai.Client",
        FakeClient,
    )

    evidence = {
        "order_id": 900002,
        "late_risk_probability": 0.34,
        "risk_label": "Not Late",
        "risk_level": "No Risk",
        "threshold": 0.40,
    }

    result = generate_grounded_response(
        question=(
            "What is the risk prediction "
            "for order 900002?"
        ),
        evidence=evidence,
    )

    assert "900002" in result
    assert "34%" in result
    assert "No Risk" in result
