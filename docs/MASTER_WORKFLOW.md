# AI Engineering Capstone — Master Workflow & Documentation

## Purpose

This document is the operating manual for the LogiGuard AI capstone.

## Current Phase

**Model Lifecycle Finalization / Pre-API Integration**

The project is no longer in topic selection or pre-implementation.

## Current Architecture

```text
Raw DataCo data
        ↓
validate
        ↓
clean
        ↓
aggregate
        ↓
prepare_data.py
        ↓
versioned processed dataset
        ↓
        ├── train_baseline.py
        │       ↓
        │   baseline model + preprocessor + metadata
        │
        └── train_final_model.py
                ↓
            candidate model + preprocessor + metadata
                ↓
            promote_model.py
                ↓
            quality gate
                ↓
            current_model.json
                ↓
            inference / API
```

## Completed Core Modeling Work

- Data understanding and quality analysis
- Leakage-safe feature selection
- Chronological train / validation / test split
- Reusable preprocessing and feature engineering
- Logistic Regression baseline
- Decision Tree experiment and tuning
- Random Forest experiment and tuning
- XGBoost experiment and two-stage tuning
- Threshold analysis
- Stage 2 XGBoost selection
- Final untouched test evaluation
- `order_hour` ablation analysis
- Versioned processed datasets
- Versioned baseline artifacts
- Versioned final-model artifacts
- Explicit model promotion
- Promotion quality gate

## Baseline Role

The Logistic Regression model is a benchmark.

Each baseline run stores:

- trained model
- fitted preprocessor
- metadata
- validation metrics
- test metrics

Baseline runs are stored under:

```text
models/baseline/<run_id>/
```

Baseline models are not promoted to `current_model.json`.

## Final Model Lifecycle

Training:

```bash
python -m pipelines.train_final_model
```

Promotion:

```bash
python -m pipelines.promote_model
```

Promotion is separate from training.

Current lightweight promotion rule:

```text
validation ROC-AUC >= 0.75
```

Only a promoted model becomes the model used for inference.

## Next Vertical Slice

```text
new order
    ↓
FastAPI / Pydantic
    ↓
derive model features
    ↓
load promoted model bundle
    ↓
preprocess
    ↓
predict
    ↓
persist order + prediction in PostgreSQL
    ↓
return API response
```

## Immediate Priorities

1. Complete FastAPI prediction integration.
2. Persist prediction workflow to PostgreSQL.
3. Add end-to-end API → model → database tests.
4. Clean remaining training-pipeline technical debt.
5. Add Prefect.
6. Add MLflow.
7. Add DVC.
8. Dockerize.
9. Build Streamlit.
10. Add constrained Operations Copilot.
11. Add monitoring, drift, alerting, and CI/CD.

## Documentation Roles

- `PROJECT_STATUS.md` — current state and immediate next actions
- `BACKLOG.md` — complete task list
- `docs/PROJECT_BLUEPRINT.md` — approved project definition and intended architecture
- `docs/PROGRESS_LOG.md` — chronological implementation history
- `docs/DECISION_LOG.md` — architectural and project decisions
- `docs/MODEL_DEVELOPMENT.md` — experiment and model-selection evidence
- Current code/tests — implementation source of truth

## Definition of Done

The project is complete when a new person can:

1. Understand the problem.
2. Reproduce data preparation.
3. Reproduce baseline training.
4. Reproduce final-model training.
5. Identify the promoted model.
6. Run the FastAPI service.
7. Run the Dockerized local system.
8. Use the UI.
9. Inspect tests and CI.
10. View monitoring and drift.
11. See at least one alert.
12. Understand the Operations Copilot role.
13. Continue development from the documentation.

## What To Do Right Now

1. Finish documentation synchronization.
2. Complete FastAPI + PostgreSQL integration.
3. Add end-to-end tests.
4. Continue with remaining MLOps components.
