# LogiGuard API

## Overview

LogiGuard exposes the trained late-delivery risk model through a FastAPI application.

The API currently acts as a model-serving layer. It receives order features directly through an HTTP request, validates the input, passes the data to the production prediction module, and returns the model's risk prediction.

At this stage, the API is not connected to the operational PostgreSQL database. Database integration will be added in a later development stage.

## Application

The FastAPI application is defined in:

`src/api/main.py`

The application can be started from the project root with:

```bash
uvicorn src.api.main:app --reload
```

The local server runs at:

`http://127.0.0.1:8000`

FastAPI automatically provides interactive API documentation at:

`http://127.0.0.1:8000/docs`

Alternative API documentation is available at:

`http://127.0.0.1:8000/redoc`

The OpenAPI schema is available at:

`http://127.0.0.1:8000/openapi.json`

## API Endpoints

### GET `/health`

The health endpoint verifies that the API service is running and responding.

Example response:

```json
{
  "status": "ok"
}
```

This endpoint does not perform any model prediction.

Its purpose is to provide a simple way to verify that the API application is available and responding correctly.

### POST `/predict`

The prediction endpoint receives the features required by the trained late-delivery risk model.

The incoming request is validated using a Pydantic `OrderInput` model.

The validated input is then converted into a Pandas DataFrame using the feature names expected by the saved preprocessing pipeline.

The endpoint calls:

`predict_late_risk()`

from:

`src/models/prediction.py`

The prediction flow is:

```text
HTTP request
    ↓
FastAPI
    ↓
Pydantic OrderInput validation
    ↓
Pandas DataFrame
    ↓
predict_late_risk()
    ↓
saved preprocessor
    ↓
saved XGBoost model
    ↓
selected operating threshold
    ↓
JSON response
```

The current model-serving API receives the order features directly in the request body.

The API is not yet connected to a database.

A future database integration can allow the API to retrieve order information from PostgreSQL instead of requiring all model features to be supplied directly in the request.

## Prediction Input

The `/predict` endpoint currently expects the following fields:

- `Type`
- `Customer_Segment`
- `Customer_State`
- `Order_Country`
- `Order_Region`
- `Shipping_Mode`
- `total_quantity`
- `total_discount`
- `num_unique_products`
- `num_unique_categories`
- `num_unique_departments`
- `order_hour`
- `order_dayofweek`
- `order_month`

Example request:

```json
{
  "Type": "DEBIT",
  "Customer_Segment": "Consumer",
  "Customer_State": "CA",
  "Order_Country": "United States",
  "Order_Region": "West of USA",
  "Shipping_Mode": "Standard Class",
  "total_quantity": 1,
  "total_discount": 0.0,
  "num_unique_products": 1,
  "num_unique_categories": 1,
  "num_unique_departments": 1,
  "order_hour": 10,
  "order_dayofweek": 2,
  "order_month": 6
}
```

## Prediction Output

The API returns three prediction fields:

- `late_risk_probability`
- `late_risk_prediction`
- `risk_label`

Example response:

```json
{
  "late_risk_probability": 0.403239,
  "late_risk_prediction": 1,
  "risk_label": "Late"
}
```

The selected operating threshold is `0.40`.

Therefore, if:

```text
late_risk_probability >= 0.40
```

the prediction is:

```text
1 → Late
```

Otherwise:

```text
0 → Not Late
```

## Interactive API Documentation

FastAPI automatically generates Swagger UI for the application.

It is available at:

`http://127.0.0.1:8000/docs`

Swagger UI allows the API endpoints to be inspected and tested directly from the browser.

The current endpoints are:

```text
GET  /health
POST /predict
```

The `/predict` endpoint can be tested by entering a JSON request body and selecting `Execute`.

A successful request returns HTTP status code:

```text
200
```

together with the prediction response.

## Automated API Tests

Automated API tests are implemented in:

`tests/test_api.py`

The tests use:

- `pytest`
- FastAPI `TestClient`

The purpose of these tests is to verify the software behavior of the API.

These tests are separate from the machine-learning performance evaluation performed during model development.

### Health Check Test

The health check test verifies that:

- `GET /health` responds successfully
- the HTTP status code is `200`
- the response body is:

```json
{
  "status": "ok"
}
```

### Prediction Endpoint Test

The prediction endpoint test sends a valid sample order to:

```text
POST /predict
```

and verifies that:

- the request completes successfully
- the HTTP status code is `200`
- the response contains `late_risk_probability`
- the response contains `late_risk_prediction`
- the response contains `risk_label`
- the probability is between `0` and `1`
- the prediction is either `0` or `1`
- the risk label is either `Late` or `Not Late`

## Running the Automated Tests

From the project root, run:

```bash
pytest tests/test_api.py -v
```

Current test result:

```text
2 passed
```

The passing tests confirm that both the health endpoint and the model prediction endpoint are functioning correctly in the current development environment.

## Current Architecture

The current API architecture is:

```text
Client / Swagger
        ↓
FastAPI
        ↓
Pydantic validation
        ↓
Prediction module
        ↓
Saved preprocessor
        ↓
Saved XGBoost model
        ↓
Threshold 0.40
        ↓
Prediction response
```

The operational database is not yet part of this flow.

Database integration will be introduced separately in a later development stage.