# Project Status — LogiGuard AI

**Last updated:** 2026-10-15  
**Current phase:** Final documentation, demonstration, and capstone delivery  
**Current working branch:** `feature/final-documentation`

## Project Overview

LogiGuard is a logistics decision-support application that estimates late-delivery risk for orders, prioritizes shipment exceptions, and provides a constrained Operations Copilot. The prediction model is trained on historical DataCo supply-chain data; operational predictions and shipment records are stored in PostgreSQL. The system does not autonomously dispatch shipments or contact customers or carriers.

## Implemented

### Data and modeling

- Historical source: DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS, with raw files kept locally under `data/raw/`.
- Raw-data validation, deterministic cleaning, and item-to-order aggregation in `pipelines/prepare_data.py`; processed CSVs are stored in timestamped directories under `data/processed/`.
- Chronological train/validation/test splitting, training-only learned categorical grouping, and reusable preprocessing.
- Versioned Logistic Regression baseline and selected Stage 2 XGBoost model.
- Final-model training is **manual** (`python -m pipelines.train_final_model`) and writes a versioned model, fitted preprocessor, and metadata. It does **not** automatically change the active model.
- Promotion is **manual** (`python -m pipelines.promote_model`) and requires validation ROC-AUC ≥ 0.75; only successful promotion updates `models/current_model.json`.
- Active run: `2026-10-02_10-36`; selected threshold: `0.40`.
- Active-model evaluation: validation ROC-AUC **0.7717**; test ROC-AUC **0.7747**, test recall **0.8403** (historical holdout results, not measured production performance).
- Model metadata records the developer-confirmed source CSV, its path, and SHA256. Future training runs record the selected dataset filename and path.

### Application

- FastAPI with `/health`, `/predict`, `/predict/raw`, `/shipments`, `/shipments/{order_id}`, raw/processed order lookup, prediction lookup, `/copilot`, and `/metrics`.
- PostgreSQL persistence of raw orders, processed orders, and predictions; predictions include the originating model run ID and threshold.
- Streamlit dashboard for ranked shipment exceptions, selected-shipment detail, and Copilot interaction.
- Constrained Operations Copilot with grounded retrieval and deterministic validation; human operators retain decision responsibility.
- Docker Compose services: PostgreSQL 17, API, Streamlit UI, Prometheus, and Grafana.

### MLOps and monitoring

- **DVC 3.67.1:** processed training CSV is tracked by a committed `.csv.dvc` file; local DVC cache is present and `dvc status` reported `Data and pipelines are up to date`. **No DVC remote** has been configured.
- **MLflow 3.17.1:** existing active model's parameters, validation/test metrics, and dataset provenance were imported as a **historical run** into an independent local SQLite database (`mlflow.db`). This is not an MLflow training run or an automated model registry/promotion workflow.
- **Prometheus/Grafana:** operational HTTP metrics, dashboard, and an `LogiGuardAPIDown` alert after one minute of scrape failure. No external notification destination is configured.
- **Evidently:** manually generated reference-versus-current data and prediction-distribution drift reports. Fewer than 30 current observations are flagged as insufficient data, not confirmed drift.
- No automated retraining or promotion. Real-world model quality cannot be calculated without confirmed delivery outcomes for new orders.

### Quality and CI/CD

- Local full regression on the isolated `logiguard_test` PostgreSQL database: **33 passed, 4 third-party warnings** (last reported 2026-10-14).
- Ruff: **all checks passed**; lint is report-only and does not automatically modify code.
- GitHub Actions runs Python 3.14 dependency installation, Ruff, table creation against a PostgreSQL 17 test service, pytest, and a Docker image build.
- CI/CD branch was merged into `main` through PR #21; earlier GitHub Actions runs passed. The README documentation-branch run shown on 2026-10-15 was **queued**, not yet confirmed successful.
- README has been added and pushed to `feature/final-documentation` (commit `f432fff`); documentation branch has not yet been merged into `main`.

## Known Limitations

- Historical DataCo training data is not validated as representative of any specific logistics company's live operations.
- The dataset itself is excluded from Git. DVC metadata is tracked, but without a remote, a fresh clone cannot retrieve the processed CSV using `dvc pull` alone.
- MLflow run data is local, not stored in Git or exposed by the Docker Compose application; it is not connected to online inference or model promotion.
- Drift reporting is manual. The API-down Prometheus rule has no configured external email/Slack notification channel.
- Production prediction performance cannot be established from unlabeled inference records; drift findings with very small current samples are exploratory.
- Model retraining and promotion require explicit human action.

## Remaining Delivery Work

1. Review the new README against actual startup requirements and demonstration steps.
2. Synchronize outdated top-level planning/status documents without rewriting historical progress entries.
3. Prepare and rehearse the end-to-end demonstration and final presentation.
4. Confirm GitHub Actions results for the documentation branch and merge its PR to `main` when checks pass.

## Source of Truth

- **Code, tests, and configuration:** current implemented behavior.
- **`docs/PROGRESS_LOG.md`:** chronological work record; retain historical entries.
- **`docs/PROJECT_BLUEPRINT.md`:** original requirements and proposed architecture; not all planned features are implemented.
- **`BACKLOG.md`:** task planning; may need synchronization.
- **This file:** current high-level implementation and delivery status.
