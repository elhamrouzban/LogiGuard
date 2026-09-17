# Capstone Backlog / TODO

**Project:** AI Logistics Exception Management & Operations Copilot  
**Purpose:** Living task tracker for all future work  
**Rule:** This file is the long-term task list. `PROJECT_STATUS.md` contains only the current phase and the next few actions.

---


### Task format

Use this format for every task:

```md
- [ ] P1 TASK-001 — Short task description
```

When completed:

```md
- [x] P1 TASK-001 — Short task description
```

### Do not delete completed tasks

Completed tasks should normally stay in this file with `[x]`.

Why:

- preserves project history;
- helps future agents understand what was already done;
- prevents duplicate work;
- makes handoff easier;
- supports presentation and retrospective.

Only remove a task if it was created by mistake or explicitly cancelled.  
For cancelled tasks, use:

```md
- [~] P2 TASK-999 — Cancelled task — reason
```

### Priority system

- **P0 — Blocker:** Project cannot continue safely without this.
- **P1 — Required:** Needed for the capstone / MVP / course expectations.
- **P2 — Valuable:** Strong portfolio value, but not required for the minimum bar.
- **P3 — Optional:** Polish or future extension.

### Workflow rule

At the start of a work session:

1. Read `PROJECT_STATUS.md`.
2. Read the relevant section of this file.
3. Pick the highest-priority unfinished task.
4. Work on only a small logical group of tasks.
5. Commit the work.
6. Mark completed tasks `[x]`.
7. Update `PROJECT_STATUS.md`.
8. Add a short entry to `docs/PROGRESS_LOG.md`.

### Scope rule

Do not add a new major technology or feature unless:

- it supports the approved project scope;
- it fits the 4-week deadline;
- it is something the project owner can explain and defend;
- the decision is documented in `docs/DECISION_LOG.md`.

If the project is executed solo, protect the 4-week deadline by keeping the Streamlit UI minimal, keeping traffic forecast/weather optional, and skipping the LLM reviewer unless all P1 core work is already on schedule.

---

# Phase 0 — Project Freeze / Pre-Start Decisions

- [ ] P0 TASK-001 — Verify the official DataCo V5 dataset source on Mendeley.
- [ ] P0 TASK-002 — Download `DataCoSupplyChainDataset.csv`.
- [ ] P0 TASK-003 — Download `DescriptionDataCoSupplyChain.csv`.
- [ ] P0 TASK-004 — Save the dataset source, DOI, version, and CC BY 4.0 license in project documentation.
- [ ] P0 TASK-005 — Confirm actual row count and column count locally.
- [ ] P0 TASK-006 — Confirm exact meaning of `Late_delivery_risk`.
- [ ] P0 TASK-007 — Define the exact prediction timestamp: what information is assumed available when prediction is made.
- [ ] P0 TASK-008 — Create a first leakage audit for every candidate feature.
- [ ] P0 TASK-009 — Identify order/entity/grouping keys to prevent train/test leakage.
- [ ] P0 TASK-010 — Decide initial train/validation/test split strategy.
- [ ] P0 TASK-011 — Confirm that a leakage-safe baseline can be trained before committing fully to the topic.
- [ ] P1 TASK-012 — Manually test access to Hamburg current traffic open data once.
- [ ] P1 TASK-013 — Manually test access to Hamburg short-term traffic forecast / SensorThings once.
- [ ] P1 TASK-014 — Manually test access to DWD weather data once.
- [ ] P0 TASK-015 — Choose a no-cost LLM strategy for the Operations Copilot.
- [x] P1 TASK-016 — Select Streamlit as the UI technology for the operational dashboard.
- [x] P1 TASK-017 — Confirm project direction, constrained scope, and explicit non-goals after teacher review.
- [ ] P1 TASK-018 — Update `PROJECT_STATUS.md` once the topic is officially locked.
- [ ] P1 TASK-019 — Record topic-selection decision in `docs/DECISION_LOG.md`.

---

# Week 1 — Data, Leakage Audit, Baseline Models, Database

## Repository / Engineering Foundation

- [ ] P1 TASK-020 — Confirm Python package structure under `src/`.
- [ ] P1 TASK-021 — Create/update `pyproject.toml`.
- [ ] P1 TASK-022 — Configure Ruff.
- [ ] P1 TASK-023 — Configure Black.
- [ ] P1 TASK-024 — Configure pre-commit hooks.
- [ ] P1 TASK-025 — Create initial pytest structure.
- [ ] P1 TASK-026 — Create initial GitHub Actions CI skeleton.
- [ ] P1 TASK-027 — Add environment/config strategy without committed secrets.

## Data Ingestion

- [ ] P1 TASK-028 — Build DataCo raw-data loader.
- [ ] P1 TASK-029 — Implement schema/column validation.
- [ ] P1 TASK-030 — Implement target validation.
- [ ] P1 TASK-031 — Validate null rates.
- [ ] P1 TASK-032 — Validate duplicate rows and entity duplication.
- [ ] P1 TASK-033 — Validate timestamp parsing.
- [ ] P1 TASK-034 — Record dataset statistics in `docs/DATA.md`.

## Leakage Audit

- [ ] P0 TASK-035 — Create feature audit table: prediction-time availability, leakage risk, use/exclude reason.
- [ ] P0 TASK-036 — Explicitly audit `Delivery Status`.
- [ ] P0 TASK-037 — Explicitly audit `Days for shipping (real)`.
- [ ] P0 TASK-038 — Audit all other columns that may contain post-outcome information.
- [ ] P1 TASK-039 — Create a leakage deny-list in code/config.
- [ ] P1 TASK-040 — Add automated test that forbidden leakage columns cannot enter model training.

## PostgreSQL

- [ ] P1 TASK-041 — Define minimal PostgreSQL schema.
- [ ] P1 TASK-042 — Create `shipments` table.
- [ ] P1 TASK-043 — Create `predictions` table.
- [ ] P2 TASK-044 — Create `model_versions` table.
- [ ] P2 TASK-045 — Create `agent_interactions` table.
- [ ] P1 TASK-046 — Load cleaned project data into PostgreSQL.

## EDA

- [ ] P1 TASK-047 — Analyze target distribution.
- [ ] P1 TASK-048 — Analyze shipping-mode vs late-delivery rate.
- [ ] P1 TASK-049 — Analyze region/market/category patterns.
- [ ] P1 TASK-050 — Analyze time-related patterns.
- [ ] P1 TASK-051 — Identify suspicious target-correlated features.
- [ ] P1 TASK-052 — Identify missing-data and cardinality issues.
- [ ] P1 TASK-053 — Document EDA findings in `docs/DATA.md` or `docs/MODELING.md`.

## Baseline / Initial Models

- [ ] P1 TASK-054 — Implement trivial majority-class baseline.
- [ ] P1 TASK-055 — Implement first leakage-safe Logistic Regression baseline.
- [ ] P1 TASK-056 — Record baseline Precision, Recall, F1, ROC-AUC, confusion matrix.
- [ ] P0 TASK-057 — Confirm that the project remains viable after leakage removal.
- [ ] P1 TASK-058 — Define initial business-oriented success metric after observing baseline behavior.
- [ ] P1 TASK-184 — Train initial Decision Tree candidate if the leakage-safe baseline and data contract are stable.
- [ ] P1 TASK-185 — Train initial Random Forest candidate if the leakage-safe baseline and data contract are stable.
- [ ] P1 TASK-186 — Train initial XGBoost candidate if the leakage-safe baseline and data contract are stable.

---

# Week 2 — Model Selection, FastAPI, Pipelines, MLflow, DVC

## Feature Engineering

- [ ] P1 TASK-059 — Create reproducible feature-engineering pipeline.
- [ ] P1 TASK-060 — Encode categorical variables appropriately.
- [ ] P1 TASK-061 — Handle scaling where required.
- [ ] P1 TASK-062 — Create only justified date/time features.
- [ ] P1 TASK-063 — Ensure training and inference use identical feature transformations.

## Candidate Models

- [ ] P1 TASK-064 — Complete/finalize Decision Tree experiment and log results.
- [ ] P1 TASK-065 — Complete/finalize Random Forest experiment and log results.
- [ ] P1 TASK-066 — Complete/finalize XGBoost experiment and log results.
- [ ] P1 TASK-067 — Compare all candidate models against the baseline.
- [ ] P1 TASK-068 — Perform error analysis.
- [ ] P1 TASK-069 — Review false negatives as a business-critical error type.
- [ ] P1 TASK-070 — Select primary model and document why.
- [ ] P1 TASK-071 — Record model-selection decision in `docs/DECISION_LOG.md`.

## FastAPI

- [ ] P1 TASK-094 — Create FastAPI application.
- [ ] P1 TASK-095 — Add typed Pydantic request model for prediction.
- [ ] P1 TASK-096 — Add typed response model.
- [ ] P1 TASK-097 — Implement `GET /health`.
- [ ] P1 TASK-098 — Implement `POST /predict`.
- [ ] P1 TASK-099 — Implement `GET /shipments/{shipment_id}`.
- [ ] P1 TASK-100 — Implement `POST /agent/analyze`.
- [ ] P1 TASK-101 — Ensure model loads once where practical.
- [ ] P1 TASK-102 — Add meaningful API error handling.

## MLflow

- [ ] P1 TASK-072 — Set up local MLflow tracking.
- [ ] P1 TASK-073 — Log model parameters.
- [ ] P1 TASK-074 — Log evaluation metrics.
- [ ] P1 TASK-075 — Log artifacts such as confusion matrix.
- [ ] P1 TASK-076 — Log selected model artifact.
- [ ] P1 TASK-077 — Define current/live model version.

## DVC

- [ ] P1 TASK-078 — Initialize DVC if not already initialized.
- [ ] P1 TASK-079 — Version raw DataCo data.
- [ ] P1 TASK-080 — Version processed leakage-safe dataset.
- [ ] P2 TASK-081 — Decide whether selected model artifact is tracked by DVC, MLflow, or both.

## Prefect / Batch Pipeline

- [ ] P1 TASK-082 — Create simple Prefect flow.
- [ ] P1 TASK-083 — Add load/validate stage.
- [ ] P1 TASK-084 — Add clean/feature stage.
- [ ] P1 TASK-085 — Add train/evaluate stage.
- [ ] P1 TASK-086 — Add MLflow logging stage.
- [ ] P1 TASK-087 — Document manual retraining path.

## ML / Data Quality Gates

- [ ] P1 TASK-088 — Add test that required features exist.
- [ ] P1 TASK-089 — Add test that target values are valid.
- [ ] P1 TASK-090 — Add model-load test.
- [ ] P1 TASK-091 — Add prediction-probability validity test.
- [ ] P1 TASK-092 — Add model quality gate against trivial baseline.
- [ ] P1 TASK-093 — Ensure CI runs model/data quality tests.

---

# Week 3 — Streamlit Dashboard, Constrained Agent, Docker

## External Data Adapters

- [ ] P2 TASK-103 — Implement Hamburg current-traffic adapter.
- [ ] P2 TASK-104 — Cache/fail gracefully when Hamburg traffic service is unavailable.
- [ ] P3 TASK-105 — Implement Hamburg 10/20-minute traffic forecast adapter.
- [ ] P3 TASK-106 — Implement DWD weather adapter.
- [ ] P1 TASK-107 — Ensure external APIs are never required for core `/predict`.
- [ ] P1 TASK-108 — Mock all external API calls in automated CI.

## Operations Copilot — Constrained Action Space

- [ ] P1 TASK-109 — Implement `get_prediction(shipment_id)` as a read-only tool.
- [ ] P1 TASK-110 — Implement `get_shipment(shipment_id)` as a read-only tool.
- [ ] P1 TASK-111 — Implement historical/similar-shipment query as a read-only tool.
- [ ] P2 TASK-112 — Expose Hamburg traffic as an optional read-only agent tool.
- [ ] P3 TASK-113 — Expose weather as an optional read-only agent tool.
- [ ] P1 TASK-114 — Define and enforce the agent tool allow-list; no tool creation or operational actions.
- [ ] P1 TASK-115 — Define a Pydantic-validated response schema containing `risk_summary`, `top_3_risk_factors`, `suggested_investigation_steps`, `evidence_used`, and `confidence_or_notes`.
- [ ] P1 TASK-116 — Define the agent instructions so answers are evidence-grounded, separate facts from recommendations, and remain short/actionable rather than open-ended essays.
- [ ] P1 TASK-117 — Prevent the agent from inventing prediction values, traffic, weather, or unsupported causal explanations.
- [ ] P2 TASK-187 — Store agent interactions in PostgreSQL if it does not threaten P1 delivery.

## Reviewer / Validator

- [ ] P1 TASK-118 — Implement deterministic validation of prediction value, required structured fields, and factual tool outputs.
- [ ] P1 TASK-120 — Validator must return approve/reject plus a short reason.
- [ ] P2 TASK-119 — Add a small LLM reviewer only if all P1 core requirements remain on schedule.

## Streamlit UI

- [ ] P1 TASK-121 — Create the minimal Streamlit operational dashboard.
- [ ] P1 TASK-122 — Build shipment exception table with risk score/risk level display.
- [ ] P1 TASK-123 — Add sort/filter for high-risk shipments.
- [ ] P1 TASK-124 — Build selected-shipment detail panel.
- [ ] P1 TASK-125 — Add Operations Copilot input/output area for structured actionable responses.
- [ ] P2 TASK-126 — Display evidence used and reviewer/validator status in Streamlit.
- [ ] P1 TASK-127 — Keep Streamlit limited to one workflow: identify and investigate high-risk shipments.
- [ ] P1 TASK-188 — Connect Streamlit to FastAPI and PostgreSQL rather than embedding separate prediction logic in the UI.

## Docker

- [ ] P1 TASK-128 — Create API Dockerfile.
- [ ] P1 TASK-129 — Create/update Docker Compose.
- [ ] P1 TASK-130 — Add PostgreSQL service.
- [ ] P1 TASK-131 — Add Prometheus service.
- [ ] P1 TASK-132 — Add Grafana service.
- [ ] P2 TASK-133 — Add MLflow service if useful.
- [ ] P1 TASK-134 — Verify local system starts from documented commands.

---

# Week 4 — Monitoring, CI/CD, Stabilization, Demo, Presentation

## Prometheus / Grafana

- [ ] P1 TASK-135 — Instrument request count.
- [ ] P1 TASK-136 — Instrument request latency.
- [ ] P1 TASK-137 — Instrument error rate.
- [ ] P1 TASK-138 — Add basic service-health metric.
- [ ] P1 TASK-139 — Build minimal Grafana dashboard.

## Evidently / Drift

- [ ] P1 TASK-140 — Choose reference dataset for drift monitoring.
- [ ] P1 TASK-141 — Define current/production-like comparison batch without presenting it as real production data.
- [ ] P1 TASK-142 — Monitor selected important input feature drift.
- [ ] P1 TASK-143 — Monitor prediction distribution drift.
- [ ] P1 TASK-144 — Create reproducible Evidently drift report.
- [ ] P1 TASK-145 — Document that drift is a warning, not automatic proof of model failure.

## Alert

- [ ] P1 TASK-146 — Configure at least one demonstrable alert.
- [ ] P1 TASK-147 — Preferred alert: API error rate above defined threshold.
- [ ] P2 TASK-148 — Optional alert: important drift threshold exceeded.


## Testing and Reliability

- [ ] P1 TASK-149 — Complete unit tests.
- [ ] P1 TASK-150 — Complete API integration tests.
- [ ] P1 TASK-151 — Complete PostgreSQL integration test.
- [ ] P1 TASK-152 — Test agent with mocked external services.
- [ ] P1 TASK-153 — Test Dockerized local startup.
- [ ] P1 TASK-154 — Fix all P0/P1 bugs.
- [ ] P1 TASK-155 — Ensure GitHub Actions is green.

## CI/CD

- [ ] P1 TASK-156 — Run Ruff in CI.
- [ ] P1 TASK-157 — Run tests in CI.
- [ ] P1 TASK-158 — Run model/data quality gate in CI.
- [ ] P1 TASK-159 — Build Docker image in CI.
- [ ] P3 TASK-160 — Publish image to GHCR only if everything else is complete.

## Documentation

- [ ] P1 TASK-161 — Finalize README.
- [ ] P1 TASK-162 — Document installation/setup.
- [ ] P1 TASK-163 — Document how to run training.
- [ ] P1 TASK-164 — Document how to run API.
- [ ] P1 TASK-165 — Document how to run Docker Compose.
- [ ] P1 TASK-166 — Document monitoring.
- [ ] P1 TASK-167 — Document retraining workflow.
- [ ] P1 TASK-168 — Document project limitations.
- [ ] P1 TASK-169 — Finalize architecture diagram.
- [ ] P1 TASK-170 — Update `docs/HANDOFF.md`.
- [ ] P1 TASK-171 — Finalize `docs/RISK_REGISTER.md`.
- [ ] P1 TASK-172 — Make sure `PROJECT_STATUS.md` reflects final state.

## Presentation / Demo

- [ ] P1 TASK-173 — Prepare 10–15 minute presentation.
- [ ] P1 TASK-174 — Explain business problem/user in ~1 minute.
- [ ] P1 TASK-175 — Explain data and leakage problem.
- [ ] P1 TASK-176 — Show baseline/model comparison.
- [ ] P1 TASK-177 — Explain architecture and engineering decisions.
- [ ] P1 TASK-178 — Demo shipment risk dashboard.
- [ ] P1 TASK-179 — Demo Operations Copilot.
- [ ] P1 TASK-180 — Demo monitoring/drift/alert.
- [ ] P1 TASK-181 — Present limitations honestly.
- [ ] P1 TASK-182 — Rehearse presentation to stay within time.
- [ ] P1 TASK-183 — Store final slides in `presentation/`.
- [ ] P1 TASK-189 — Record the final project demo after the monitored end-to-end workflow is stable.

---

# Future / Post-Capstone Ideas — Do Not Build During the 4-Week MVP

These are intentionally deferred.

- [ ] P3 FUTURE-001 — Real customer TMS/ERP integration.
- [ ] P3 FUTURE-002 — Company-specific retraining using customer data.
- [ ] P3 FUTURE-003 — Real carrier API integration.
- [ ] P3 FUTURE-004 — HVCC integration if explicit access terms are confirmed.
- [ ] P3 FUTURE-005 — AIS/vessel trajectory modeling.
- [ ] P3 FUTURE-006 — Real-time fleet GPS.
- [ ] P3 FUTURE-007 — ETA prediction.
- [ ] P3 FUTURE-008 — Route optimization.
- [ ] P3 FUTURE-009 — Automated carrier/customer communication.
- [ ] P3 FUTURE-010 — Authentication and multi-tenancy.
- [ ] P3 FUTURE-011 — Public cloud deployment.
- [ ] P3 FUTURE-012 — Commercial security/GDPR hardening.
- [ ] P3 FUTURE-013 — Business ROI study with a real logistics company.

---

# Completed Setup Tasks

Keep completed setup/history here instead of deleting them.

- [x] Created initial repository structure.
- [x] Added master capstone workflow.
- [x] Added project context.
- [x] Added capstone engineering expectations.
- [x] Added initial project status.
- [x] Defined the Logistics Exception Management & Operations Copilot concept.
- [x] Created the authoritative project blueprint.
- [x] Received positive teacher review of the project direction and four-week scope.
- [x] Selected Streamlit for the minimal dashboard based on teacher feedback.
- [x] Refined the blueprint to constrain the Operations Copilot and require structured actionable output.

---

# Backlog Maintenance Rules

1. Never delete a completed task just to make the file shorter.
2. Mark completed work with `[x]`.
3. Cancelled work uses `[~]` plus a reason.
4. Add newly discovered work under the correct phase.
5. Give new tasks a unique ID.
6. P0/P1 tasks must be finished before P2/P3 work unless there is a documented reason.
7. Do not move post-capstone ideas into the MVP without a scope decision.
8. `PROJECT_STATUS.md` should contain only the immediate current state and next actions; this file contains the complete future backlog.
9. `docs/PROGRESS_LOG.md` records what happened in each work session; this file records what still needs to happen.
10. `docs/DECISION_LOG.md` records why important technical/product decisions were made.

---

# Recommended Relationship Between Project Files

```text
PROJECT_STATUS.md
= Where are we right now?
= What are the next 3 actions?

BACKLOG.md
= Everything we still need to do
= Completed tasks remain visible

docs/PROGRESS_LOG.md
= What did we actually do in each work session?

docs/DECISION_LOG.md
= Why did we make important decisions?

docs/PROJECT_BLUEPRINT.md
= What is this project and how is it supposed to work?
```
