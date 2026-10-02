# Capstone Backlog / TODO

**Project:** AI Logistics Exception Management & Operations Copilot  
**Purpose:** Living task tracker for all future work  
**Rule:** `PROJECT_STATUS.md` contains only the current phase and next few actions.

---

# Completed Data / Modeling Work

- [x] Validate raw DataCo data
- [x] Clean raw data
- [x] Aggregate item-level data to order level
- [x] Implement chronological train / validation / test split
- [x] Implement reusable feature engineering
- [x] Implement categorical encoding and numerical scaling
- [x] Train Logistic Regression baseline
- [x] Train Decision Tree
- [x] Train Random Forest
- [x] Train XGBoost
- [x] Tune Decision Tree
- [x] Tune Random Forest
- [x] Perform two-stage XGBoost tuning
- [x] Compare candidate models against baseline
- [x] Select Stage 2 XGBoost
- [x] Select operating threshold `0.40`
- [x] Evaluate selected model on untouched test set
- [x] Perform `order_hour` ablation analysis
- [x] Implement versioned processed-data pipeline
- [x] Refactor baseline training to use processed data
- [x] Version baseline model, preprocessor, and metadata
- [x] Refactor final-model training to use processed data
- [x] Version final model, preprocessor, and metadata
- [x] Separate training from model promotion
- [x] Implement `promote_model.py`
- [x] Add validation ROC-AUC promotion quality gate
- [x] Maintain `models/current_model.json` as promoted-model pointer

---

# Current Priority — FastAPI + PostgreSQL

- [x] Create FastAPI application
- [x] Implement `GET /health`
- [x] Implement initial `POST /predict`
- [x] Create initial Pydantic prediction request model
- [ ] Finalize realistic operational order input schema
- [ ] Derive aggregate model features from new order input
- [ ] Reuse promoted model bundle for inference
- [ ] Persist incoming order in PostgreSQL
- [ ] Persist prediction in PostgreSQL
- [ ] Include model run/version information in stored prediction
- [ ] Finalize typed prediction response
- [ ] Add API error handling
- [ ] Add end-to-end API → model → database integration test

---

# Training Pipeline Cleanup

- [ ] Remove duplicate/redundant evaluation code in `train_final_model.py`
- [ ] Add formal model-load pytest
- [ ] Add prediction-probability validity pytest
- [ ] Add automated test for required model features
- [ ] Add automated leakage-column protection test

---

# PostgreSQL

- [x] Create initial database connection layer
- [x] Create initial ORM models
- [x] Create order table structure
- [x] Create prediction table structure
- [ ] Align model-version field with `model_run_id`
- [ ] Remove hard-coded database credentials from source code
- [ ] Add environment-based database configuration
- [ ] Add PostgreSQL integration test

---

# MLOps

## Prefect

- [ ] Wrap current data preparation and training stages in Prefect
- [ ] Document manual retraining flow

## MLflow

- [ ] Set up local MLflow
- [ ] Log model parameters
- [ ] Log validation/test metrics
- [ ] Log selected artifacts
- [ ] Connect model runs to experiment tracking

## DVC

- [ ] Initialize DVC
- [ ] Version raw dataset
- [ ] Version processed datasets
- [ ] Decide final model-artifact ownership between DVC and MLflow

---

# Engineering Foundation

- [ ] Finalize `pyproject.toml`
- [ ] Configure Ruff
- [ ] Configure Black
- [ ] Configure pre-commit
- [ ] Create GitHub Actions CI
- [ ] Run tests in CI
- [ ] Run model/data quality checks in CI

---

# Product Layer

## Streamlit

- [ ] Create minimal Streamlit dashboard
- [ ] Display shipment/order risk
- [ ] Add high-risk filtering
- [ ] Add selected-order detail view
- [ ] Connect Streamlit to FastAPI and PostgreSQL

## Operations Copilot

- [ ] Finalize no-cost LLM strategy
- [ ] Implement read-only prediction tool
- [ ] Implement read-only shipment/order tool
- [ ] Implement historical comparison tool
- [ ] Enforce tool allow-list
- [ ] Implement structured Pydantic output
- [ ] Add deterministic validator
- [ ] Prevent unsupported factual claims

---

# Docker / Runtime

- [ ] Create API Dockerfile
- [ ] Create Docker Compose
- [ ] Add PostgreSQL service
- [ ] Add Prometheus service
- [ ] Add Grafana service
- [ ] Add MLflow service if useful
- [ ] Verify local startup from documented commands

---

# Monitoring / Drift / Alerting

- [ ] Instrument request count
- [ ] Instrument request latency
- [ ] Instrument error rate
- [ ] Build minimal Grafana dashboard
- [ ] Create Evidently reference/current comparison
- [ ] Monitor important feature drift
- [ ] Monitor prediction distribution drift
- [ ] Configure at least one alert

---

# Documentation / Finalization

- [ ] Finalize README
- [ ] Document installation/setup
- [ ] Document training
- [ ] Document API
- [ ] Document Docker Compose
- [ ] Document monitoring
- [ ] Document retraining workflow
- [ ] Document limitations
- [ ] Finalize architecture diagram
- [ ] Update `docs/HANDOFF.md`
- [ ] Finalize `docs/RISK_REGISTER.md`
- [ ] Finalize `PROJECT_STATUS.md`

---

# Presentation / Demo

- [ ] Prepare 10–15 minute presentation
- [ ] Explain business problem and target user
- [ ] Explain data and leakage problem
- [ ] Show baseline/model comparison
- [ ] Explain architecture and engineering decisions
- [ ] Demo prediction workflow
- [ ] Demo Streamlit dashboard
- [ ] Demo Operations Copilot
- [ ] Demo monitoring/drift/alert
- [ ] Present limitations
- [ ] Rehearse presentation
- [ ] Store final slides in `presentation/`

---

# Future / Post-Capstone Ideas

- [ ] Real customer TMS/ERP integration
- [ ] Company-specific retraining
- [ ] Carrier API integration
- [ ] HVCC integration if access is confirmed
- [ ] AIS/vessel trajectory modeling
- [ ] Real-time fleet GPS
- [ ] ETA prediction
- [ ] Route optimization
- [ ] Authentication and multi-tenancy
- [ ] Public cloud deployment
