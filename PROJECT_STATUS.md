# PROJECT STATUS

**Last updated:** 2026-09-17  
**Current phase:** Scope Finalization / Pre-Implementation  
**Overall status:** On track

## Current Objective

Finalize the approved project scope and complete the pre-start validation before implementation begins.

The project is now:

> **LogiGuard AI — AI Logistics Exception Management & Operations Copilot**

The core scope has been reviewed positively by the teacher. The next objective is to validate the primary dataset, confirm the leakage-safe prediction setup, and complete the remaining pre-start decisions before Week 1 implementation.

## Completed

- [x] Initialized Git repository
- [x] Created initial project structure
- [x] Added master capstone workflow
- [x] Added project context
- [x] Added capstone engineering expectations
- [x] Selected the capstone topic
- [x] Defined the business problem and target user
- [x] Defined the main ML task as binary late-delivery-risk classification
- [x] Defined the main training dataset: DataCo Smart Supply Chain Dataset
- [x] Defined free/open optional Hamburg traffic and DWD weather enrichment sources
- [x] Created the authoritative project blueprint
- [x] Received positive teacher review of the project direction and 4-week scope
- [x] Selected Streamlit as the UI technology
- [x] Constrained the Operations Copilot to structured, evidence-grounded tool use
- [x] Updated `docs/PROJECT_BLUEPRINT.md` after teacher feedback
- [x] Updated `BACKLOG.md` after teacher feedback

## In Progress

- [ ] Complete the pre-start data and feasibility gate
- [ ] Confirm the exact target semantics and prediction timestamp
- [ ] Create the first leakage audit and evaluation split strategy

## Next 3 Actions

1. Verify and download the official DataCo V5 dataset and its description file from Mendeley.
2. Confirm the actual dataset schema, row/column counts, target semantics, and prediction-time feature availability.
3. Create the first leakage audit and define a defensible train/validation/test split before implementation continues.

## Blockers

No current blocker.

Implementation should not begin until the first pre-start data checks confirm that:

- the target is understood;
- a leakage-safe feature set is possible;
- the evaluation split is defensible;
- the dataset source/license is documented.

## Current Technical State

- Project topic: Selected and teacher-reviewed
- Project scope: Finalized at blueprint level
- Main dataset: Selected; local validation not yet completed
- Data license: Identified as CC BY 4.0; local documentation still pending
- Target: `Late_delivery_risk`; exact semantics still to be verified from source description
- Prediction timestamp: Not yet finalized
- Leakage audit: Not started
- Train/validation/test split: Not finalized
- PostgreSQL: Planned, not implemented
- EDA: Not started
- Baseline: Not started
- Candidate models: Logistic Regression, Decision Tree, Random Forest, XGBoost
- Best model: Not selected
- FastAPI: Planned, not implemented
- Streamlit UI: Selected, not implemented
- Agent: Constrained Operations Copilot defined, not implemented
- Agent output schema: Defined at blueprint level, not implemented
- Reviewer/validator: Deterministic MVP approach defined, not implemented
- Docker: Planned, not implemented
- Tests: Not started
- CI: Not started
- MLflow: Planned, not implemented
- DVC: Planned, not implemented
- Prefect pipeline: Planned, not implemented
- Monitoring: Prometheus + Grafana planned, not implemented
- Drift monitoring: Evidently planned, not implemented
- Alert: Planned, not implemented
- Deployment: Local/containerized execution planned; public cloud deployment not required

## Approved Core Scope

The capstone will build one end-to-end AI engineering workflow:

```text
DataCo supply-chain data
        ↓
validation + leakage audit
        ↓
feature engineering
        ↓
binary classification model
        ↓
FastAPI
        ↓
PostgreSQL + optional traffic/weather tools
        ↓
constrained Operations Copilot
        ↓
structured actionable response
        ↓
Streamlit dashboard
        ↓
monitoring / drift / CI
```

Explicitly out of scope for the 4-week MVP:

- route optimization
- GPS tracking
- AIS/vessel tracking
- Kafka
- Spark
- Kubernetes
- autonomous dispatching
- large multi-agent architecture
- proprietary port integrations
- mandatory paid APIs
- unnecessary cloud architecture

## Teacher Feedback Incorporated

The following teacher recommendations are now part of the project plan:

- Keep the project focused and avoid unnecessary infrastructure.
- Constrain the agent's action space.
- Use structured tool calls.
- Return actionable outputs such as:
  - Top 3 Risk Factors
  - Suggested Investigation Steps
  - Evidence Used
- Use Streamlit for the dashboard.
- Sequence the 4 weeks as:
  - Week 1: data, leakage removal, baseline models, database
  - Week 2: FastAPI, model selection, pipelines, MLflow/DVC
  - Week 3: Streamlit dashboard, agent, database/API tools
  - Week 4: monitoring, CI/CD, stabilization, demo/presentation
- If executed solo, protect scope aggressively and keep optional components optional.

## Resume Instructions

If returning to this project after a long break:

1. Read `PROJECT_STATUS.md`.
2. Read `docs/PROJECT_BLUEPRINT.md`.
3. Read `BACKLOG.md`.
4. Read `docs/EXPECTATIONS.md`.
5. Read `docs/MASTER_WORKFLOW.md`.
6. Read the latest entries in `docs/PROGRESS_LOG.md`.
7. Read relevant entries in `docs/DECISION_LOG.md`.
8. Continue with the first unfinished item under “Next 3 Actions”.

## Source of Truth Rule

- `PROJECT_STATUS.md` = current state and next actions
- `BACKLOG.md` = all future and completed tasks
- `docs/PROJECT_BLUEPRINT.md` = authoritative project definition and architecture
- `docs/PROGRESS_LOG.md` = what happened in each work session
- `docs/DECISION_LOG.md` = why important decisions were made
