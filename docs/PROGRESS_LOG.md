# Progress Log

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Purpose:** Chronological record of meaningful project work sessions.  
**Rule:** Record what actually happened. Do not use this file for future plans except for the immediate next step at the end of each entry.

---

## How to Use This File

Add one entry after every meaningful work session.

Each entry should contain:

```md
## YYYY-MM-DD — Short session title

### Completed
- What was actually completed.

### Decisions / Changes
- Important scope or implementation changes made during the session.

### Blockers / Open Questions
- Anything unresolved.

### Next Step
- The next concrete action.
```

Do not rewrite old entries to make the project history look cleaner. If an earlier statement becomes outdated, leave it in history and record the new decision in a later entry.

Major architectural or product decisions belong in `docs/DECISION_LOG.md`.

---

# 2026-09-08 — Initial Capstone Planning

### Completed

- Reviewed the AI Engineering course direction and capstone expectations.
- Identified the need for a capstone that combines:
  - real business value;
  - measurable machine learning;
  - software engineering;
  - API/product delivery;
  - MLOps;
  - monitoring;
  - a meaningful agentic component.
- Established that the project should make use of the project owner's previous web-development experience rather than becoming a notebook-only data-science project.
- Began evaluating multiple candidate project domains.

### Decisions / Changes

- Career positioning for the capstone was centered on AI Engineering / Applied AI Engineering, with ML Engineering as a secondary fit.
- The project should result in a usable product workflow, not only exploratory notebooks.

### Blockers / Open Questions

- Final topic had not yet been selected.

### Next Step

Evaluate candidate topics against business relevance, available data, technical depth, and four-week feasibility.

---

# 2026-09-11 — Repository and Documentation Foundation

### Completed

- Initialized the project repository structure.
- Added the master capstone workflow.
- Added project context documentation.
- Added capstone engineering expectations.
- Added initial `PROJECT_STATUS.md`.
- Created the first backlog structure for task tracking.

### Decisions / Changes

- Adopted a documentation-first workflow.
- Established that each independent logical change should be committed separately in Git.
- Established the roles of:
  - `PROJECT_STATUS.md`
  - `BACKLOG.md`
  - `docs/MASTER_WORKFLOW.md`
  - `docs/CONTEXT.md`
  - `docs/EXPECTATIONS.md`

### Blockers / Open Questions

- Final topic was still under evaluation.

### Next Step

Select the project topic and create its authoritative technical blueprint.

---

# 2026-09-15 — Logistics Project Direction Selected

### Completed

- Selected the logistics exception-management direction.
- Defined the working project as:
  - late-delivery-risk prediction;
  - shipment exception prioritization;
  - an Operations Copilot for evidence-grounded investigation support.
- Selected DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS as the primary candidate training dataset.
- Defined optional Hamburg traffic and DWD weather data as contextual enrichment.
- Identified data leakage as a critical modeling risk.
- Defined the primary ML task as binary classification.
- Created the authoritative project blueprint.

### Decisions / Changes

- One strong ML problem will remain the center of the project.
- The model will predict late-delivery risk.
- Low/Medium/High labels, if used in the UI, are presentation layers over model probability rather than separate model classes.
- External live APIs must not be required for core prediction.
- Paid or uncertain APIs must not become MVP dependencies.
- Kafka, Spark, Kubernetes, AIS tracking, route optimization, and other large-scope additions were excluded from the four-week MVP.

### Blockers / Open Questions

- DataCo had not yet been locally downloaded and validated.
- Exact target semantics still needed confirmation from the source description.
- Prediction timestamp and leakage-safe feature contract still needed to be defined.

### Next Step

Obtain teacher feedback and finalize the engineering scope before implementation.

---

# 2026-09-16 — Teacher Review and Scope Refinement

### Completed

- Received positive teacher feedback on the project direction.
- Confirmed that the project solves a real problem and covers the intended engineering cycle.
- Incorporated the teacher's recommendation to constrain the agent.
- Selected Streamlit for the dashboard.
- Revised the four-week implementation sequence.
- Updated the project blueprint accordingly.

### Decisions / Changes

Teacher feedback incorporated into the project:

- Keep Kafka, Spark, and Kubernetes out of scope.
- Constrain the agent's action space.
- Use structured tool calls.
- Prefer actionable structured outputs instead of open-ended essays.
- Use deterministic validation as the required MVP reviewer.
- Keep an LLM reviewer optional.
- Use Streamlit for the dashboard.
- Protect scope aggressively if the project is executed solo.

Revised delivery sequence:

- Week 1: data, leakage control, baseline/initial models, PostgreSQL.
- Week 2: model selection, FastAPI, Prefect, MLflow, DVC.
- Week 3: Streamlit, constrained Operations Copilot, integration, Docker.
- Week 4: Prometheus/Grafana, Evidently, alerting, CI/CD, stabilization, demo, presentation.

### Blockers / Open Questions

- Primary dataset still not locally validated.
- No-cost LLM runtime/provider still not selected.
- Team capacity / solo execution still affects optional scope.

### Next Step

Bring backlog, status, decision log, and handoff documentation in sync before starting implementation.

---

# 2026-09-17 — Documentation Synchronization Before Coding Handoff

### Completed

- Updated `docs/PROJECT_BLUEPRINT.md` after teacher feedback.
- Updated `BACKLOG.md` to reflect the revised timeline and constrained agent design.
- Updated `PROJECT_STATUS.md` from Topic Selection to Scope Finalization / Pre-Implementation.
- Created `docs/DECISION_LOG.md`.
- Recorded the accepted project decisions in ADR-style entries.
- Defined Streamlit as the selected UI.
- Defined the agent output contract at the planning level:
  - `risk_summary`
  - `top_3_risk_factors`
  - `suggested_investigation_steps`
  - `evidence_used`
  - `confidence_or_notes`
- Confirmed that deterministic validation is required and an LLM reviewer remains optional.

### Decisions / Changes

The repository documentation is being prepared for a coding-agent handoff, but implementation must still begin with the pre-start data-validation gate rather than immediately generating the application stack.

### Blockers / Open Questions

Not blockers yet, but unresolved pre-start items remain:

- official DataCo V5 local download/verification;
- exact local row/column counts;
- exact target semantics;
- prediction timestamp;
- leakage audit;
- grouping/split strategy;
- leakage-safe baseline;
- no-cost LLM strategy.

### Next Step

Complete the pre-start data gate beginning with the official DataCo dataset and description file.

---

# 2026-10-02 — Implementation Catch-Up and Current Architecture Audit

### Completed

Since the previous progress-log entry, the project moved from planning into working implementation.

#### Data and feature pipeline

- Added reusable raw-data loading, validation, cleaning, aggregation, splitting, and preprocessing code under `src/`.
- Confirmed the primary raw dataset is loaded from:
  - `data/raw/DataCoSupplyChainDataset.csv`
- Implemented item-level cleaning and selection of leakage-safe model inputs.
- Implemented order-level aggregation so model training uses one row per `Order Id`.
- Implemented chronological train / validation / test splitting.
- Implemented reproducible time-based feature engineering.
- Implemented rare-country grouping learned from training data only.
- Implemented a reusable `ColumnTransformer` with:
  - `OneHotEncoder(handle_unknown="ignore")`
  - `StandardScaler`

#### Modeling

- Completed model-development work in the modeling notebook.
- Evaluated the main candidate model families.
- Selected Stage 2 XGBoost as the current final model implementation.
- Selected operating threshold `0.40`.
- Final model hyperparameters currently used in the training pipeline include:
  - `n_estimators=150`
  - `max_depth=5`
  - `learning_rate=0.07`
  - `min_child_weight=1`
  - `subsample=1.0`
  - `colsample_bytree=0.7`
  - `random_state=42`

#### Reusable training pipelines

- Added `pipelines/train_baseline.py`.
- Added `pipelines/train_final_model.py`.
- Moved major data/model logic out of notebooks into reusable Python modules.
- Confirmed that retraining can be triggered manually with:

```bash
python -m pipelines.train_final_model
```

#### Model versioning

- Changed final-model saving from fixed filenames to versioned run directories.
- Each final training run now saves:
  - model artifact;
  - fitted preprocessor;
  - model metadata.
- Added `models/current_model.json` as a pointer to the model bundle currently selected for inference.
- Confirmed that inference resolves the model, preprocessor, and metadata paths through this pointer.

#### Inference

- Added `src/models/prediction.py`.
- Confirmed that prediction:
  - reads `models/current_model.json`;
  - loads the corresponding fitted model;
  - loads the corresponding fitted preprocessor;
  - loads metadata from the same run;
  - retrieves the selected threshold;
  - retrieves train-learned rare-country values;
  - performs preprocessing;
  - calculates late-delivery probability and binary prediction;
  - records the originating model run ID in the result.

#### FastAPI

- Added a FastAPI application.
- Added:
  - `GET /health`
  - `POST /predict`
- Added a Pydantic request model.
- Added an API test using FastAPI `TestClient`.

#### PostgreSQL foundation

- Added SQLAlchemy database configuration.
- Added ORM models for:
  - `orders`
  - `predictions`
- Added table-creation support.
- Confirmed that the current API does not yet persist new orders or predictions to PostgreSQL.

#### Tests

- Added API coverage for:
  - health endpoint;
  - prediction endpoint.
- Added a prediction smoke script.
- Identified that the current prediction smoke script is not yet a true pytest test because it does not contain assertions inside a `test_*` function.

#### Repository audit

- Reviewed the actual current project structure rather than relying only on older planning documents.
- Confirmed that no additional hidden data, training, inference, or database pipelines currently exist outside the inspected files.
- Confirmed that several planning documents are outdated and must later be synchronized with the implemented architecture.

### Decisions / Changes

- The project is no longer considered to be in planning or model-selection mode.
- Current work is focused on engineering the model lifecycle and end-to-end automation.
- The following three runtime responsibilities will be separated clearly:

```text
Data Pipeline
Raw data
→ validation
→ cleaning
→ aggregation
→ processed dataset

Training Pipeline
Processed dataset
→ split
→ training-time feature preparation
→ fit preprocessor
→ train model
→ evaluate
→ save versioned model bundle
→ promote approved model

Prediction Pipeline
New order
→ request validation
→ inference-time preparation
→ current approved model bundle
→ prediction
→ PostgreSQL persistence
→ API response
```

- Training-time validation/test evaluation uses the newly trained in-memory model.
- Online inference uses the model referenced through `current_model.json`.
- The data-cleaning lifecycle should be separated from the model-training lifecycle.
- The training pipeline should eventually consume a validated processed dataset rather than owning the full raw-data cleaning workflow.
- Train/validation/test splitting will remain part of the training/evaluation lifecycle rather than being permanently fixed inside the data-cleaning pipeline.
- Fitted/learned transformations must remain part of the model bundle and must be reused during inference.

### Blockers / Open Questions

- `train_final_model.py` currently performs validation and test evaluation twice; the duplicate evaluation block must be removed.
- The current final training pipeline still starts directly from raw data instead of a separately materialized processed dataset.
- A dedicated data-preparation pipeline does not yet exist.
- The current API expects already-engineered model features rather than a raw operational order.
- Training-time feature preparation and inference-time feature preparation are not yet represented by one explicit shared contract.
- The API does not yet persist orders or predictions to PostgreSQL.
- Database models and prediction outputs currently use slightly different model-identification fields and need alignment.
- Current training automatically updates `current_model.json`; a future quality/promotion gate should prevent an unsuitable retrained model from replacing the approved model merely because it is newer.
- MLflow, DVC, Prefect, Docker, monitoring, drift tracking, and CI/CD are still pending.
- Several Markdown documents no longer represent the implemented state and must be updated incrementally as the architecture stabilizes.

### Next Step

Strengthen and verify the raw-data validation contract before extracting raw-data preparation into a dedicated data pipeline.

---

# 2026-10-02 — Raw-Data Validation Hardening

### Completed

- Expanded `src/data/validation.py` so invalid future raw data fails before cleaning and model training.
- Added validation for:
  - empty datasets;
  - missing required columns;
  - missing values in required fields;
  - invalid/non-numeric values in numeric fields;
  - infinite numeric values;
  - blank text values;
  - invalid target values;
  - invalid order dates;
  - negative quantity;
  - negative discount;
  - non-positive order IDs;
  - non-positive customer IDs.
- Kept deterministic correction/normalization separate from rejection of invalid data.
- Verified the strengthened validation by running the full final-model training pipeline successfully.
- The existing DataCo raw dataset passed the stricter validation rules.
- The final training run completed successfully with unchanged validation/test behavior.

Validation metrics from the verification run:

```text
accuracy:  0.6766703842644226
precision: 0.6813806837039496
recall:    0.7639069767441861
f1:        0.7202876940619244
roc_auc:   0.7716837872569746
```

Test metrics from the verification run:

```text
accuracy:  0.6525397951941599
precision: 0.640600870419767
recall:    0.8403314917127072
f1:        0.7269975304708038
roc_auc:   0.7746903663674294
```

### Decisions / Changes

- Raw-data validation and raw-data cleaning are treated as separate responsibilities.
- The validation layer should fail loudly for unsafe or ambiguous values rather than silently guessing corrections.
- Cleaning should only make deterministic transformations that can be defended.
- Future invalid-data failures can later be connected to logging, monitoring, and alerting instead of building a separate notification system at this stage.

### Blockers / Open Questions

- The raw validation rules currently reflect the known model/data contract and will need automated unit tests.
- Exact production behavior for every possible unknown category or malformed request has not yet been implemented.
- The dedicated data-preparation pipeline has not yet been extracted.


# 2026-10-02 — Added Versioned Data Preparation Pipeline

### Completed

- Added `pipelines/prepare_data.py`.
- The pipeline now:
  - loads raw data;
  - validates raw data;
  - cleans item-level data;
  - aggregates data to one row per order;
  - saves a processed dataset.
- Processed datasets are saved in timestamped folders so previous versions are preserved.
- Timestamp format:
  - `YYYY-MM-DD_HH-MM`
- Verified the pipeline successfully created a processed dataset with 65,752 rows.

### Decisions / Changes

- Processed datasets must not overwrite previous versions.
- Each data-preparation run creates a new timestamped dataset version.

### Blockers / Open Questions

- Training still reads raw data directly and does not yet consume the processed dataset.

# 2026-10-02 — Training Uses Versioned Processed Data

### Completed

- Updated `pipelines/train_final_model.py` to load the latest processed dataset instead of starting from raw data.
- Removed raw-data cleaning and aggregation from the training pipeline.
- Kept train/validation/test splitting and training-time preprocessing inside the training workflow.
- Changed model run timestamps to a readable date-and-time format:
  - `YYYY-MM-DD_HH-MM`
- Verified the training pipeline successfully after the refactor.
- Validation and test metrics remained unchanged.
- Cleaned up old model artifacts that were no longer needed.

### Decisions / Changes

- Data preparation and model training are now separate workflows.
- Processed datasets and model runs are versioned by date and time.
- Training consumes prepared order-level data instead of rebuilding it from raw data.

### Blockers / Open Questions

- Training still updates `current_model.json` automatically.
- Model promotion still needs to be separated from training.

# 2026-10-02 — Separated Model Training and Promotion

### Completed

- Updated `pipelines/train_final_model.py` so training no longer changes `current_model.json`.
- Added `pipelines/promote_model.py`.
- Verified that a new model version can be trained and saved without affecting the current model.
- Verified that a selected run can be promoted manually.
- Confirmed that `current_model.json` updates only during the promotion step.

### Decisions / Changes

- Training and model promotion are now separate workflows.
- A newly trained model does not automatically become the current model.
- Promotion is an explicit step.

### Blockers / Open Questions

- No automated model-quality gate exists yet before promotion.

# 2026-10-02 — Added Model Promotion Quality Check

### Completed

- Updated `pipelines/promote_model.py`.
- Added a lightweight quality check before model promotion.
- Promotion now reads the selected model metadata.
- A model can only be promoted when validation ROC-AUC is at least `0.75`.
- Verified that promotion succeeds for a valid model run.

### Decisions / Changes

- Model promotion remains a separate manual step.
- A minimal quality gate is used to prevent clearly weak models from becoming the current model.

### Blockers / Open Questions

- More advanced promotion rules are intentionally deferred.

# 2026-10-02 — Updated and Versioned Baseline Training Pipeline

### Completed

- Updated `pipelines/train_baseline.py` to use the latest versioned processed dataset.
- Removed raw-data cleaning and aggregation from baseline training.
- Baseline and final-model training now use the same processed-data source and split logic.
- Baseline Logistic Regression is now saved as a versioned training run.
- Each baseline run stores:
  - trained model;
  - fitted preprocessor;
  - metadata;
  - validation metrics;
  - test metrics.
- Baseline runs are stored under `models/baseline/<run_id>/`.
- Successfully executed and verified the updated baseline pipeline.

### Decisions / Changes

- Baseline models are benchmarks and are not promoted to `current_model.json`.
- Baseline artifacts are versioned so historical comparisons remain reproducible.
- Candidate/final models can be compared against stored baseline metrics using their metadata.

## 2026-10-04 — API and Database Integration Completed

- Updated the FastAPI prediction endpoint to accept order-level input and derive time-based model features from `order_date`.
- Connected the prediction endpoint to the promoted model through the inference layer.
- Persisted both orders and prediction results to PostgreSQL.
- Stored the active `model_run_id` and the model threshold with each prediction.
- Added an API/database integration test covering:
  - `GET /health`
  - `POST /predict`
  - model inference
  - PostgreSQL persistence
  - verification of saved order and prediction records
  - cleanup of test data
- Confirmed the integration test passes successfully.
- Moved `DATABASE_URL` out of source code and into a local `.env` file.
- Added `.env` to `.gitignore`.
- Verified PostgreSQL connectivity through the environment-based configuration.
- Removed duplicate model evaluation logic from `train_final_model.py`.

- Added duplicate-order handling to `POST /predict`.
- Duplicate `order_id` requests now return `409 Conflict` instead of `500 Internal Server Error`.
- Added an automated API test for duplicate-order behavior.
- Confirmed all API tests pass successfully.


## 2026-10-05 — Read-Only Shipments API Added

- Added a new read-only FastAPI endpoint:
  - `GET /shipments`
- The endpoint joins operational `orders` with their corresponding `predictions`.
- Shipment results are ordered by `late_risk_probability` in descending order so higher-risk shipments appear first.
- Added a typed `ShipmentSummary` response model.
- The endpoint does not modify database state.
- Added an automated integration test for `GET /shipments`.
- Confirmed the API test suite passes with 4 tests.
- This endpoint is intended to support the upcoming Streamlit shipment exception dashboard.

## Single Shipment Endpoint

Added:

GET /shipments/{order_id}

Purpose:
Return one specific shipment and its prediction details by order ID.

Behavior:
- Returns shipment + prediction data for an existing order.
- Returns 404 if the shipment does not exist.

Test added:
test_get_single_shipment_returns_saved_order

Status:
Passed successfully.


## Streamlit Selected Shipment Details

Added shipment selection to the Streamlit dashboard.

Flow:
- Streamlit loads shipments from `GET /shipments`.
- User selects an `order_id`.
- Streamlit calls `GET /shipments/{order_id}`.
- Details for the selected shipment and prediction are displayed.

Verification:
- Tested manually in Streamlit.
- Changing the selected order updates the displayed shipment details successfully.

## Streamlit API Configuration

Updated the Streamlit dashboard to read the FastAPI base URL from the `API_URL` environment variable.

Default local value:
`http://127.0.0.1:8000`

Verification:
- Shipment table loads successfully.
- Selected shipment details still load successfully.




## 2026-10-06 — Raw Order Inference Preparation

### Completed

- Added `src/features/inference.py`.
- Added `prepare_order_for_inference()`.
- The new inference preparation logic accepts one raw order represented by one or more item-level rows.
- The function validates that the input contains exactly one `Order Id`.
- The function selects only the raw fields required for prediction-time preparation.
- The function parses `order date (DateOrders)`.
- The function applies the existing `Customer State` cleaning rule.
- The function always aggregates the order to order level, even when the order contains only one item.
- Aggregation creates:
  - `total_quantity`
  - `total_discount`
  - `num_unique_products`
  - `num_unique_categories`
  - `num_unique_departments`
- The function returns data in the same shape currently expected by the existing `POST /predict` endpoint.

### Testing

Added:

`tests/test_inference_preparation.py`

The test verifies that a raw order with multiple item rows is correctly aggregated into one order-level object.

Test command:

```bash
python -m pytest tests/test_inference_preparation.py -v



### Additional Inference Test

Added a single-item order test to confirm that aggregation is always applied, even when an order contains only one item.

The test verifies that a single raw item is converted to the expected order-level fields:

- `total_quantity`
- `total_discount`
- `num_unique_products`
- `num_unique_categories`
- `num_unique_departments`

Test command:

```bash
python -m pytest tests/test_inference_preparation.py -v

Result:
2 passed



### Inference Validation Tests

Added validation coverage for the raw-order inference preparation path.

The tests verify that the inference preparation rejects:

- empty input
- multiple `Order Id` values in one request
- negative `Order Item Quantity`

Existing tests also continue to verify:

- aggregation of multi-item orders
- aggregation of single-item orders

Test command:

```bash
python -m pytest tests/test_inference_preparation.py -v


## Raw Order Storage

Added a new PostgreSQL table for preserving original incoming order payloads.

### Changes

- Added `RawOrder` ORM model.
- Added PostgreSQL `JSONB` storage for raw order payloads.
- Added `raw_orders` table with:
  - `id`
  - `order_id`
  - `raw_payload`
  - `received_at`
- Updated database table creation imports.

### Verification

Ran:

```bash
python -m src.database.create_tables


## Raw Order API Schema

### Completed

- Expanded the raw-order API schema to represent a complete order-time snapshot.
- Added customer information, order destination fields, shipping configuration, and detailed item/product fields.
- Preserved `items` as a list so one order can contain multiple items.
- Excluded post-outcome fields such as:
  - `Days for shipping (real)`
  - `Delivery Status`
  - `Late_delivery_risk`
  - `shipping date (DateOrders)`
- Excluded `Customer Password`.

### Testing

Added:

`tests/test_raw_order_schema.py`

The test verifies that a valid raw order with nested items is accepted by the Pydantic schema.

Test command:

```bash
python -m pytest tests/test_raw_order_schema.py -v



## Raw Order Inference Adapter

### Completed

- Added a production-only adapter for raw order payloads.
- Converts nested `items[]` into item-level rows expected by the existing inference preparation logic.
- Reuses the existing inference aggregation without changing any training, preprocessing, or model-training files.
- Verified multi-item raw orders aggregate correctly before prediction.

### Testing

Ran:

```bash
python -m pytest tests/test_inference_preparation.py -v