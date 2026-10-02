# PROJECT STATUS

**Last updated:** 2026-10-02  
**Current phase:** Model Lifecycle Finalization / Pre-API Integration  
**Overall status:** On track

## Current Objective

Finalize the production-style data and model lifecycle, synchronize project documentation, then continue with FastAPI and PostgreSQL integration.

## Completed

- [x] Project topic and scope selected and teacher-reviewed
- [x] DataCo dataset loaded and analyzed
- [x] Raw-data validation implemented
- [x] Data cleaning implemented
- [x] Item-level data aggregated to order level
- [x] Chronological train / validation / test split implemented
- [x] Reusable preprocessing and feature engineering implemented
- [x] Logistic Regression baseline trained
- [x] Decision Tree, Random Forest, and XGBoost evaluated
- [x] Tree-based candidates tuned
- [x] Stage 2 XGBoost selected as primary model
- [x] Operating threshold `0.40` selected
- [x] Final untouched test evaluation completed
- [x] `order_hour` ablation analysis completed
- [x] Versioned processed-data pipeline implemented
- [x] Versioned baseline training implemented
- [x] Versioned final-model training implemented
- [x] Training separated from model promotion
- [x] Promotion quality gate implemented
- [x] Current-model pointer implemented with `models/current_model.json`

## In Progress

- [ ] Synchronize remaining documentation
- [ ] Finalize FastAPI-to-model integration
- [ ] Connect prediction workflow to PostgreSQL

## Next 3 Actions

1. Finish documentation synchronization.
2. Integrate FastAPI prediction with the promoted model.
3. Persist orders and predictions in PostgreSQL.

## Blockers

No current blocker.

## Current Technical State

- Main dataset: DataCo Smart Supply Chain Dataset
- Target: `Late_delivery_risk`
- Data validation: Implemented
- Data cleaning: Implemented
- Processed data: Versioned under `data/processed/<run_id>/`
- Split strategy: Chronological
- Baseline: Logistic Regression, versioned
- Candidate models: Decision Tree, Random Forest, XGBoost
- Primary model: Stage 2 tuned XGBoost
- Operating threshold: `0.40`
- Validation ROC-AUC: approximately `0.772`
- Test ROC-AUC: approximately `0.775`
- Test Recall: approximately `0.840`
- Model artifacts: Versioned
- Preprocessor artifacts: Versioned
- Metadata: Versioned
- Promotion: Separate manual pipeline
- Promotion quality gate: Validation ROC-AUC must be at least `0.75`
- Current model pointer: `models/current_model.json`
- FastAPI: Initial `/health` and `/predict` exist; integration still needs completion
- PostgreSQL: Initial database structure exists; prediction persistence still needs integration
- Tests: Initial API and prediction tests exist; broader coverage still needed
- MLflow: Planned
- DVC: Planned
- Prefect: Planned
- Docker: Planned
- Streamlit: Planned
- Monitoring / drift / alerting: Planned

## Current Data / Model Lifecycle

```text
Raw DataCo data
        ↓
validate
        ↓
clean
        ↓
aggregate to order level
        ↓
prepare_data.py
        ↓
versioned processed dataset
        ↓
        ├── train_baseline.py
        │       ↓
        │   versioned Logistic Regression
        │   + preprocessor
        │   + metadata
        │
        └── train_final_model.py
                ↓
            versioned XGBoost candidate
            + preprocessor
            + metadata
                ↓
            promote_model.py
                ↓
            model quality gate
                ↓
            current_model.json
                ↓
            prediction / API
```

## Source of Truth Rule

- `PROJECT_STATUS.md` = current state and next actions
- `BACKLOG.md` = complete task list
- `docs/PROJECT_BLUEPRINT.md` = project definition and target architecture
- `docs/PROGRESS_LOG.md` = chronological implementation history
- `docs/DECISION_LOG.md` = important decisions and rationale
- Current code and tests = implementation source of truth
