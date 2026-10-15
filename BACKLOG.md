# LogiGuard AI — Delivery Backlog

**Updated:** 2026-10-15
**Purpose:** Current checklist for capstone delivery. Completed items reflect the implementation and verification recorded in the project; deferred items are not presented as implemented.
**Current priority:** Stable demo, recorded backup, presentation, and final delivery checks.

## Completed — Data and ML

- [x] Obtain and validate the historical DataCo dataset; clean and aggregate item-level records to one order per row.
- [x] Implement chronological train/validation/test splitting and leakage-aware features.
- [x] Compare Logistic Regression, Decision Tree, Random Forest, and XGBoost; tune candidate models.
- [x] Select Stage 2 XGBoost, with operating threshold `0.40`, and evaluate on held-out test data.
- [x] Implement versioned processed-data preparation: `python -m pipelines.prepare_data`.
- [x] Implement versioned baseline and final training pipelines.
- [x] Keep training separate from explicit manual model promotion, with validation ROC-AUC gate >= 0.75.
- [x] Preserve `models/current_model.json` as the sole current-model pointer.
- [x] Record training CSV filename/path automatically for future manual training runs.
- [x] Record developer-confirmed dataset provenance and verified SHA256 for active run `2026-10-02_10-36`.

## Completed — Product and Runtime

- [x] Build FastAPI inference endpoints for order-level and raw item-level requests.
- [x] Validate raw requests and aggregate raw items into the prediction-time feature representation.
- [x] Persist raw orders, processed orders, and predictions in PostgreSQL.
- [x] Provide read-only shipment, order, prediction, and raw-order retrieval APIs.
- [x] Implement a Streamlit shipment-risk dashboard and selected-shipment detail view.
- [x] Implement the constrained Operations Copilot with approved read-only tools and deterministic validation.
- [x] Run API, UI, PostgreSQL, Prometheus, and Grafana through Docker Compose.

## Completed — MLOps, Monitoring, and CI

- [x] Track the active processed training CSV with DVC; verify `dvc status` is up to date.
- [x] Register the existing active model's hyperparameters, validation/test metrics, and dataset provenance as an MLflow **historical import**.
- [x] Keep MLflow's local SQLite tracking store separate from the operational PostgreSQL database.
- [x] Instrument the FastAPI service with Prometheus request/latency/error metrics.
- [x] Provision Grafana's API monitoring dashboard and an API-down Prometheus alert.
- [x] Implement manual Evidently reports covering feature and prediction-distribution drift.
- [x] Flag drift reports with fewer than 30 current rows as insufficient data.
- [x] Run Ruff, PostgreSQL-backed pytest, and Docker image build in GitHub Actions.
- [x] Verify local full regression: **33 passed, 4 third-party warnings**; Ruff passed.

## Completed — Documentation

- [x] Write the project README covering setup, manual data/model lifecycle, Docker, API, MLOps, monitoring, and CI.
- [x] Update `PROJECT_STATUS.md` for the current delivery phase.
- [x] Preserve `docs/PROGRESS_LOG.md` as chronological history.
- [x] Review and reconcile the delivery backlog and record newer architecture decisions in the decision log.

## Remaining — Final Delivery (Priority)

- [ ] Verify a stable demonstration scenario against the current Streamlit UI and API using controlled demo data.
- [ ] Prepare and record a short, successful backup demo video; avoid exposing keys or personal data.
- [ ] Prepare final English presentation slides, including the business problem, data leakage controls, model results, architecture, product demo, MLOps, and limitations.
- [ ] Rehearse the presentation with a timer and verify the expected presentation duration.
- [ ] Review the final README and supporting diagrams/screenshots against the actual product behavior.
- [ ] Review any remaining stale planning/handoff documents for misleading *current-status* claims; preserve historical decisions and progress entries.
- [ ] Check final GitHub Actions results and complete the documentation PR/merge.

## Known Limitations / Deferred, Not Completed

- [ ] Configure a DVC remote so another machine can retrieve the dataset using DVC alone; currently the tracked content is local.
- [ ] Add actual outcome labels and enough recent cases to assess production predictive quality; historical test metrics do not establish production accuracy.
- [ ] Configure external alert notifications; the API-down Prometheus rule exists but no email/Slack integration is configured.
- [ ] Schedule or automate drift reporting and establish a validated ML-specific alert policy; reports currently run manually.
- [ ] Add automatic experiment logging to **future** training runs if needed; current MLflow record is a historical import, not a training-time run.
- [ ] Implement Prefect orchestration if subsequently required; it is an original plan, not verified as implemented.
- [ ] Decide whether further optional tooling (Black, pre-commit, an MLflow service or registry, advanced CI quality gates) provides enough value to justify scope expansion.

## Beyond Capstone Scope

Real customer TMS/ERP integration, carrier APIs, authenticated multi-tenant deployment, real-time GPS/AIS, routing/ETA optimization, paid data integrations, and public cloud deployment remain future ideas, not claims about the current system.

**Safety rule:** No monitoring task, CI check, or MLOps tool automatically retrains a model, changes its threshold, or promotes a candidate. Model promotion requires a manual decision.
