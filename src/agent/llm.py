import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai


load_dotenv()


MODEL_NAME = "gemini-3.5-flash-lite"


def generate_grounded_response(
    question: str,
    evidence: dict[str, Any],
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = _build_grounded_prompt(
        question=question,
        evidence=evidence,
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


def _build_grounded_prompt(
    question: str,
    evidence: dict[str, Any],
) -> str:
    evidence_json = json.dumps(
        evidence,
        indent=2,
        ensure_ascii=False,
        default=str,
    )

    return f"""
    You are the LogiGuard Operations Copilot.

    Answer the user's question using ONLY the validated evidence below.

    Your audience is a logistics operations user, not a machine-learning engineer.

    Prioritize:
    - the business risk level
    - the late-delivery risk as a percentage when useful
    - whether the order needs operational attention

    Rules:
    - Use only the supplied evidence.
    - Do not invent facts, causes, or recommendations.
    - Do not change numeric values.
    - Do not derive a different risk level yourself.
    - Use the supplied risk_level exactly as provided.
    - Do not mention technical fields such as threshold, model_run_id,
    or binary prediction values unless the user explicitly asks for them.
    - If the evidence is insufficient, clearly say so.
    - Keep the answer concise and operationally useful.

    User question:
    {question}

    Validated evidence:
    {evidence_json}

    Return only the final user-facing answer.
    """.strip()