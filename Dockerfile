FROM python:3.14-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY pyproject.toml ./
COPY src ./src
COPY models ./models
COPY ui ./ui

RUN pip install --no-cache-dir .