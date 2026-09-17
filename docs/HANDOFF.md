# Handoff Guide

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Audience:** Codex, another coding agent, teammate, or the project owner returning after a break.  
**Current handoff stage:** Documentation complete enough to begin the pre-start data-validation work. Core implementation has not started.

---

# 1. Read This Before Changing Code

Read these files in this order:

1. `PROJECT_STATUS.md`
2. `docs/PROJECT_BLUEPRINT.md`
3. `BACKLOG.md`
4. `docs/EXPECTATIONS.md`
5. `docs/DECISION_LOG.md`
6. `docs/RISK_REGISTER.md`
7. `docs/MASTER_WORKFLOW.md`
8. `docs/CONTEXT.md`
9. latest entries in `docs/PROGRESS_LOG.md`

Do not start by generating the full application stack.

The first implementation work must follow the current `Next 3 Actions` in `PROJECT_STATUS.md` and the highest-priority unfinished P0/P1 backlog tasks.

---

# 2. Current Project State

The topic is selected and has received positive teacher feedback.

The project is:

> **LogiGuard AI — AI Logistics Exception Management & Operations Copilot**

Core problem:

> Predict late-delivery risk using information available before the delivery outcome is known, then help a logistics operations user investigate high-risk shipment exceptions.

Current phase:

> **Scope Finalization / Pre-Implementation**

What has been completed at the planning/documentation level:

- project topic selected;
- business problem and target user defined;
- DataCo selected as the primary dataset;
- binary-classification framing selected;
- authoritative blueprint created and refined;
- Streamlit selected for the UI;
- constrained Operations Copilot design defined;
- deterministic validator selected as the required reviewer;
- four-week plan aligned with teacher feedback;
- backlog updated;
- project status updated;
- decision log created;
- risk register created;
- progress log created.

What has **not** been completed yet:

- local DataCo download/verification;
- exact local row/column counts;
- exact `Late_delivery_risk` semantics verification;
- prediction timestamp;
- feature leakage audit;
- grouping/split strategy;
- leakage-safe baseline;
- PostgreSQL implementation;
- modeling implementation;
- FastAPI;
- Prefect;
- MLflow;
- DVC;
- Streamlit implementation;
- agent implementation;
- Docker;
- monitoring;
- CI/CD implementation.

Do not mark any of those as completed without evidence in the repository.

---

# 3. Immediate Next Actions

Follow `PROJECT_STATUS.md`.

At this handoff point, the next work is:

1. Verify and download the official DataCo V5 dataset and `DescriptionDataCoSupplyChain.csv`.
2. Confirm source/version/license plus actual local schema, row/column counts, and target semantics.
3. Define the prediction timestamp, create the feature leakage audit, identify grouping keys, and define a defensible evaluation split.

After those steps, train the first leakage-safe baseline before expanding product engineering.

---

# 4. Non-Negotiable Modeling Rule

The system must simulate a real prediction made **before the final delivery outcome is known**.

For every feature, ask:

> Would this value genuinely be available at the prediction timestamp?

If not, exclude it.

Known high-risk fields include:

```text
Delivery Status
Days for shipping (real)
```

These are examples to audit, not the complete deny-list.

Do not use apparent model performance as evidence that a feature is valid.

A lower leakage-safe score is preferable to a high invalid score.

---

# 5. Approved ML Scope

Task:

```text
Binary classification
```

Candidate target:

```text
Late_delivery_risk
```

Candidate models:

```text
Majority/simple baseline
Logistic Regression
Decision Tree
Random Forest
XGBoost
```

Primary evaluation metrics:

```text
Precision
Recall
F1
ROC-AUC
Confusion Matrix
PR-AUC when useful
```

Business emphasis:

> Recall for truly late/high-risk shipments, while managing false positives.

Do not invent a model-quality threshold before the leakage-safe baseline exists.

Do not convert the task into a 3-class model merely because the UI may display Low/Medium/High risk bands.

---

# 6. Approved Product Architecture

Intended flow:

```text
DataCo
  ↓
validation / cleaning
  ↓
leakage-safe feature engineering
  ↓
PostgreSQL
  ↓
model training / evaluation
  ↓
MLflow + DVC
  ↓
selected model
  ↓
FastAPI
  ↓
Streamlit
  ↓
Operations Copilot
  ↓
deterministic validator
```

Cross-cutting components:

```text
Prefect
Docker / Docker Compose
GitHub Actions
Prometheus + Grafana
Evidently
```

This is the approved direction, not permission to generate every component immediately.

Build in the backlog order.

---

# 7. Operations Copilot Boundaries

The agent is **not** the predictor.

The ML model produces the risk prediction.

The Operations Copilot may use only explicitly approved read-only tools.

Minimum tool allow-list:

```text
get_prediction(shipment_id)
get_shipment(shipment_id)
query_similar_or_historical_shipments(...)
```

Optional tools only after the core path is stable:

```text
get_hamburg_traffic(...)
get_hamburg_traffic_forecast(...)
get_hamburg_weather(...)
```

The agent must not:

- invent prediction values;
- invent traffic/weather data;
- claim unsupported causality;
- modify shipment data;
- contact carriers/customers;
- execute operational actions;
- create arbitrary tools;
- bypass API/database validation.

Required structured output contract:

```text
risk_summary
top_3_risk_factors
suggested_investigation_steps
evidence_used
confidence_or_notes
```

Use Pydantic validation for this output when implemented.

---

# 8. Reviewer / Validation Boundary

Required MVP:

> deterministic validator

It should check:

- prediction value consistency;
- required schema fields;
- evidence support;
- no fabricated external context;
- decision-support wording;
- uncertainty where appropriate.

Expected result:

```text
APPROVE
```

or:

```text
REJECT + short reason
```

An LLM reviewer is P2/optional and must not delay core delivery.

---

# 9. UI Boundary

UI technology:

> **Streamlit**

One workflow only:

```text
shipment exception table
  ↓
select shipment
  ↓
view prediction/details
  ↓
ask Operations Copilot
  ↓
view structured evidence-backed response
```

Do not add:

- authentication;
- payment;
- multi-tenancy;
- complex admin screens;
- a separate frontend framework unless an explicit later decision supersedes Streamlit.

Streamlit should consume FastAPI/PostgreSQL interfaces rather than duplicate model logic.

---

# 10. External Data Boundary

Core model inference must work without external APIs.

Optional enrichment:

- Hamburg current traffic;
- Hamburg traffic forecast;
- DWD weather.

Do not make external API availability part of automated CI.

Mock external services in CI.

HVCC is excluded as an MVP dependency because unrestricted free access has not been established.

---

# 11. No-Cost Dependency Rule

Do not introduce a paid API or paid data dependency without explicit project-owner approval.

The LLM strategy is still unresolved.

Acceptable future choices:

- course/institution-provided free credits;
- a local/open-source model;
- a genuinely sufficient free provider tier.

If none is available, preserve the deterministic tool/report workflow rather than adding a paid hard dependency.

---

# 12. Explicit MVP Non-Goals

Do not introduce these during the four-week MVP:

```text
Kafka
Spark
Kubernetes
route optimization
vehicle GPS tracking
container tracking
AIS trajectory modeling
vessel ETA trajectory modeling
reinforcement learning
Graph Neural Networks
large multi-agent architecture
autonomous dispatching
carrier/customer automation
proprietary TMS/ERP integrations
mandatory HVCC integration
LLM fine-tuning
unnecessary cloud architecture
```

If a major new technology is proposed, stop and create/update an ADR before implementation.

---

# 13. Four-Week Delivery Order

## Week 1

- DataCo verification
- data validation/cleaning
- prediction timestamp
- leakage audit
- split strategy
- EDA
- baseline / initial candidate models
- PostgreSQL
- package/test/CI skeleton

## Week 2

- feature engineering
- complete model comparison
- error analysis
- model selection
- FastAPI
- Prefect
- MLflow
- DVC
- ML/data quality tests

## Week 3

- Streamlit
- FastAPI/PostgreSQL integration
- constrained Operations Copilot
- structured agent output
- deterministic validator
- optional traffic adapter
- Docker integration

## Week 4

- Prometheus/Grafana
- Evidently
- at least one alert
- complete CI/CD
- integration tests
- stabilization
- README/docs
- demo recording
- presentation

No new major architecture in Week 4.

---

# 14. Git Working Rules

Keep changes small and reviewable.

Preferred workflow:

```text
1. Read status/backlog.
2. Pick one small logical task or tightly related group.
3. Implement it.
4. Run relevant tests/checks.
5. Review the diff.
6. Commit only that logical change.
7. Mark completed backlog tasks.
8. Update PROJECT_STATUS.md.
9. Add a short PROGRESS_LOG entry.
10. Record a new ADR only when an important decision changed.
```

Do not combine unrelated infrastructure, model, UI, and documentation changes into one large commit.

Do not rewrite existing Git history unless explicitly requested.

---

# 15. Documentation Ownership

Use each file for its intended role:

```text
PROJECT_STATUS.md
Current state + immediate next actions

BACKLOG.md
All work items and completion state

docs/PROJECT_BLUEPRINT.md
Authoritative project/product/architecture definition

docs/DECISION_LOG.md
Why important decisions were made

docs/RISK_REGISTER.md
Risks and mitigation status

docs/PROGRESS_LOG.md
Chronological record of actual work

docs/EXPECTATIONS.md
Official capstone engineering requirements

docs/MASTER_WORKFLOW.md
Reusable project lifecycle/process

docs/CONTEXT.md
Background, goals, constraints, and project philosophy

docs/DATA.md
Dataset facts, schema, leakage audit, split strategy
(should be populated after local data validation)

docs/MODELING.md
Experiments, metrics, error analysis, model selection
(should be populated during modeling)
```

Do not duplicate the same purpose across files.

---

# 16. Coding-Agent Rules

A coding agent working on this repository must:

- work from the current backlog rather than inventing a new roadmap;
- distinguish verified facts from assumptions;
- never mark a task complete without repository evidence;
- ask for clarification when a required business/data fact is missing rather than inventing it;
- prefer existing project technologies over adding new libraries;
- keep the project owner able to understand and defend the code;
- write type hints and testable code;
- add tests with meaningful behavior changes;
- preserve the leakage-safe prediction contract;
- keep optional features optional;
- not silently change model target, architecture, agent permissions, or scope;
- update documentation after meaningful implementation changes.

---

# 17. Definition of a Safe Handoff Start

The repository is ready for a coding-agent handoff when the agent can correctly answer from the documentation:

- What problem is being solved?
- Who is the target user?
- What is the ML target?
- What is not yet verified?
- What counts as leakage?
- What should be built first?
- Which technologies are approved?
- What is explicitly out of scope?
- What may the agentic component do?
- Which optional components may be dropped?
- Which file contains current next actions?
- Which decisions require a new ADR?

At the current stage, the correct first coding task is **not** to scaffold the entire system.

The correct first work is the DataCo pre-start validation gate.
