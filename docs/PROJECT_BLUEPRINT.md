# AI Logistics Exception Management & Operations Copilot
## Authoritative Project Blueprint

**Repository:** `Capstone-2`  
**Project type:** AI Engineering Capstone  
**Planned duration:** 4 weeks  
**Primary market context:** Germany, with a Hamburg-focused operational demo  
**Primary users:** Logistics Operations Coordinator / Dispatcher / Freight Operations Analyst  
**Status:** Project direction reviewed positively by the teacher; scope is being finalized before implementation. The Pre-Start Gate still applies.  
**Last verified:** 2026-09-16

---

## 1. Purpose of This Document

This file is the authoritative project blueprint for the capstone.

A future developer, AI coding agent, reviewer, or teammate should be able to read this file and understand what the project is, which real business problem it solves, who the user is, what the ML target is, which data sources and APIs are allowed, which technologies are in scope, what the AI agent is allowed to do, how data leakage must be prevented, how the system is tested/monitored/versioned, what must be completed each week, and what "done" means.

**Change-control rule:** Do not materially expand this scope without documenting the decision in `docs/DECISION_LOG.md`. The four-week deadline is a hard constraint.

---

# 2. Project Identity

## 2.1 Project Name

**AI Logistics Exception Management & Operations Copilot**

**Teacher review outcome:** The project direction was considered solid and appropriately scoped for a real engineering problem. Specific guidance incorporated into this blueprint: keep the agent's action space constrained, use structured tool calls and actionable output, use Streamlit for the dashboard, and sequence the four weeks so monitoring/CI/CD are finalized after the core ML/API/agent workflow.


Recommended portfolio subtitle:

> Predicting shipment-delay risk and helping logistics operators prioritize high-risk exceptions.

## 2.2 One-Sentence Product Pitch

A decision-support system that predicts which shipments are at risk of late delivery, ranks the operational exceptions that need attention, and uses an AI copilot to explain the risk using model output, shipment history, and optional live Hamburg traffic/weather context.

## 2.3 What This Project Is NOT

This is not a full logistics platform, route-optimization engine, live GPS fleet tracker, Port of Hamburg production system, autonomous dispatcher, shipping-company integration, maritime AIS trajectory system, or a Kafka/Spark/Kubernetes project. It is a **small but complete vertical slice** of a production-style AI system.

---

# 3. Business Problem

Logistics operations teams often manage many shipments simultaneously. Not every shipment requires manual intervention, but some are likely to arrive late.

The operational problem is:

> **Which shipments are most likely to be delayed, and which exceptions should an operations coordinator investigate first?**

Without prioritization, an operator may need to inspect many orders manually, often after a delay is already visible.

The proposed workflow is:

```text
All shipments
    ↓
ML delay-risk scoring
    ↓
High-risk shipment queue
    ↓
Operations Copilot
    ↓
Evidence + explanation
    ↓
Human operator decision
```

The project is a **decision-support system**. A human remains responsible for the final operational decision.

---

# 4. Target User and Job-to-Be-Done

## Primary user

**Logistics Operations Coordinator / Dispatcher / Freight Operations Analyst**

## Current manual job

The user may need to inspect shipment records, compare scheduled delivery expectations, review historical patterns, check traffic/weather, determine which shipments appear risky, prioritize follow-up, and communicate with carriers or customers.

## Job-to-be-done

> When I have many active shipments, help me identify the shipments most at risk of delay, understand why they are risky, and decide which shipment I should investigate first.

## Business value hypothesis

The product aims to reduce manual exception-triage time, missed high-risk shipments, reactive handling, and time spent gathering context from multiple sources.

The capstone will demonstrate the system technically. It will **not claim proven financial ROI** without real company deployment data.

---

# 5. Core Project Question

## Primary ML question

> **Using information available before the delivery outcome is known, can we predict whether a shipment/order has a high risk of late delivery?**

## Primary product question

> **Can an operations user quickly identify and understand high-risk shipment exceptions through one decision-support interface?**

## ML task

Binary classification:

```text
0 = not late / lower late-delivery risk
1 = late-delivery risk
```

The exact target semantics must be confirmed against the source dataset documentation during Week 1.

---

# 6. Scope Freeze

## 6.1 MVP Must Include

- Free/open historical supply-chain data.
- Data ingestion and validation.
- PostgreSQL storage.
- EDA.
- Leakage audit.
- Simple baseline.
- Multiple classical ML models.
- Model evaluation and error analysis.
- MLflow experiment tracking/model lifecycle.
- DVC data/model versioning.
- Small orchestrated batch data/training pipeline.
- FastAPI inference service.
- Docker/containerized local system.
- Automated tests.
- GitHub Actions CI.
- Prometheus/Grafana service monitoring.
- Evidently data/prediction drift monitoring.
- At least one alert.
- Small usable UI.
- One tool-using Operations Copilot.
- Small reviewer/validator step if it does not threaten the core.
- Documentation and 10–15 minute final presentation.

## 6.2 Explicit Non-Goals

Do not add these to the four-week MVP:

- vehicle route optimization;
- carrier optimization;
- real truck GPS tracking;
- real container tracking;
- AIS trajectory modeling;
- ETA prediction from vessel trajectories;
- reinforcement learning;
- Graph Neural Networks;
- Kafka;
- Spark;
- Kubernetes;
- AWS architecture unless all required work is already complete;
- autonomous carrier/customer actions;
- payment integrations;
- proprietary TMS/ERP integrations;
- HVCC as a required dependency;
- multiple independent ML business problems;
- large multi-agent architecture;
- LLM fine-tuning.

---

# 7. System Architecture

```text
                    ┌──────────────────────────────┐
                    │ DataCo historical dataset   │
                    │ Primary training data       │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Ingestion / validation flow │
                    │ Pandas + Pydantic + Prefect │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │   PostgreSQL     │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌──────────────────────────────┐
                    │ Feature engineering         │
                    │ Leakage-safe feature set    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
             ┌─────────────────────────────────────────┐
             │ Baseline / Logistic Regression /        │
             │ Decision Tree / Random Forest / XGBoost │
             └─────────────────────┬───────────────────┘
                                   │
                          MLflow + DVC
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Selected model   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ FastAPI service  │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼──────────────────┐
              │                   │                  │
              ▼                   ▼                  ▼
       PostgreSQL tool      Traffic tool      Weather tool
              │                   │                  │
              └─────────────┬─────┴──────────────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Operations Copilot  │
                  └─────────┬───────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Reviewer/Validator  │
                  │ small and optional  │
                  └─────────┬───────────┘
                            ▼
                       ┌─────────┐
                       │   UI    │
                       └─────────┘

Monitoring:
FastAPI → Prometheus → Grafana
Model/data → Evidently → drift report / alert
```

---

# 8. Data Sources

## 8.1 Primary Training Dataset — REQUIRED

### Name

**DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS**

### Official source

Mendeley Data, Version 5

- Dataset page: https://data.mendeley.com/datasets/8gx2fvg2k6/5
- DOI: https://doi.org/10.17632/8gx2fvg2k6.5
- Authors: Fabian Constante, Fernando Silva, António Pereira
- Published: 2019
- License: **CC BY 4.0**
- Cost: **Free**
- Authentication/payment: **None required for dataset download**

### Main files described by the source

- `DataCoSupplyChainDataset.csv`
- `DescriptionDataCoSupplyChain.csv`
- `tokenized_access_logs.csv` (unstructured/clickstream data; not required for MVP)

### Dataset scale

Published analyses report approximately:

- **180,519 records**
- **53 original structured features**

These counts must be verified locally immediately after download and recorded in the data validation report.

### Why this is the primary source

It contains structured supply-chain/order/delivery information suitable for creating a leakage-aware shipment-delay prediction problem.

### Important limitation

The dataset is historical and is not specifically a Hamburg or German freight-forwarding dataset.

Therefore:

> The ML model must be presented as a capstone model trained on an open global supply-chain dataset, while Hamburg open data is used for operational context/demo enrichment.

Do not claim that the model has been validated on a real Hamburg freight company's production data.

---

## 8.2 Hamburg Current Traffic — OPTIONAL ENRICHMENT

### Official source

**Verkehrslage Hamburg — Transparenzportal Hamburg**

Official dataset page:

https://suche.transparenz.hamburg.de/dataset/verkehrslage-hamburg15

### What it provides

The official description states that traffic conditions are updated every **5 minutes**, covering Hamburg roads, surrounding major roads, and important motorway corridors. Traffic is represented in four congestion/state classes. Resources include WFS/WMS and downloadable data such as CSV/GeoJSON depending on the current dataset version.

### License

**Datenlizenz Deutschland – Namensnennung 2.0**

### Cost

**Free/open data**

### MVP role

This data is context for the copilot/demo, not required for model training.

Example tool:

```text
get_current_hamburg_traffic()
→ current congestion context
→ Copilot may mention it only when returned data supports the claim
```

### Robustness rule

Do not hard-code an old archived resource ZIP URL as the only integration path. Resolve the current resource endpoint from the current official dataset/catalog page.

If the traffic service is unavailable, the core prediction system must still work.

---

## 8.3 Hamburg Short-Term Traffic Forecast — OPTIONAL ENRICHMENT

### Official source

**Verkehrslageprognose Hamburg**

Official GovData page:

https://data.gov.de/suche/daten/verkehrslageprognose-hamburgfa774

Hamburg Transparency Portal page:

https://suche.transparenz.hamburg.de/dataset/verkehrslageprognose-hamburg

### What it provides

- 10-minute traffic forecast;
- 20-minute traffic forecast;
- updates every 5 minutes;
- JSON resources;
- SensorThings API access.

### SensorThings API base

```text
https://frost-transmove.germanywestcentral.cloudapp.azure.com/v1.1/
```

The official GovData resource page contains the current example SensorThings queries for all road segments, 10-minute forecasts, 20-minute forecasts, and locations.

### Important reliability note

The source identifies the forecast service as a **demo service** and warns that maintenance may cause interruptions.

Therefore:

> This source may improve the demo but must never be a required dependency for model inference.

### Cost

No paid subscription is identified on the official open-data catalog page.

---

## 8.4 DWD Weather Data — OPTIONAL ENRICHMENT

### Official source

**Deutscher Wetterdienst (DWD) Climate Data Center Open Data**

Root:

https://opendata.dwd.de/climate_environment/CDC/

Daily observations:

https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/

Historical:

https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/

Recent:

https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/

### Available variables

Depending on station/product: temperature, precipitation, humidity, pressure, wind, sunshine, cloud cover, and related meteorological measurements. DWD provides multiple temporal resolutions including 10-minute, hourly, daily, and monthly products.

### Cost

**Free/open data**

### MVP role

Optional contextual tool for the Operations Copilot. It is **not required** for the first model.

Do not spend Week 1 engineering a complex weather join before the leakage-safe baseline works.

---

## 8.5 HVCC Port-Call API — EXCLUDED FROM MVP

### Source

Hamburg Vessel Coordination Center (HVCC)

https://www.hvcc-hamburg.de/en/digital-services/api-port-call-data/

### Available information

The service advertises vessel schedules, ETA/ETD, ATA/ATD, vessel identification, voyage numbers, previous/next ports, berth information, JSON REST integration, and Swagger/OpenAPI documentation.

### Why it is excluded

The service is offered through three B2B service packages. Public documentation reviewed for this project does **not establish unrestricted public access as free**.

Therefore:

> HVCC data is not permitted to become an MVP dependency.

It may only become a future extension if explicit free/academic access is confirmed in writing.

---

# 9. Cost and Access Policy

The capstone must not depend on paid external data or paid production APIs.

Core tooling/data is intended to be local/free/open source: DataCo/Mendeley, PostgreSQL, MLflow, DVC, Prometheus, Grafana, Evidently, FastAPI, Docker local development.

External enrichment: Hamburg open traffic data and DWD are free/open; Hamburg forecast is an optional open-data/demo source.

## LLM cost constraint

**No paid LLM API may become a hard dependency.**

The LLM provider is a pre-start decision. Acceptable approaches are:

1. institution/course-provided API credit explicitly free to the student;
2. a local/open-source model the developer can run and explain;
3. a free provider tier sufficient for the demo and documented.

The agent architecture must keep the LLM provider replaceable.

If no acceptable free option is available, do not pay merely to complete the capstone; keep the tool/report workflow deterministic until a free option is confirmed.

---

# 10. Prediction-Time Data Contract

This is one of the most important technical rules.

## Prediction moment

The system must simulate a prediction made **before the final delivery outcome is known**.

Every feature must answer:

> Would this value genuinely be available to the operations system at the prediction timestamp?

If not, it cannot be a predictor.

## Target

Candidate target:

```text
Late_delivery_risk
```

Exact semantics must be confirmed from `DescriptionDataCoSupplyChain.csv`.

## Candidate feature families

Only after Week 1 audit, likely candidates include shipping mode, scheduled shipping duration, order time/date features, market/region, product/category information, customer/order metadata available before outcome, and other order-time operational fields.

No feature is automatically approved because it exists in the CSV.

---

# 11. Data Leakage

## 11.1 Meaning

Leakage occurs when the model receives information only known after the delivery outcome, or information that directly/indirectly encodes the target.

A leakage-heavy model can report impressive accuracy while being unusable for real prediction.

## 11.2 High-Risk Fields

The DataCo dataset contains fields requiring a point-in-time audit. Likely post-outcome/leakage fields include:

- `Delivery Status`
- `Days for shipping (real)`

Recent leakage-aware research on DataCo shows that post-outcome fields can substantially inflate apparent model performance.

## 11.3 Required feature audit

Before modeling, create:

| Feature | Available at prediction time? | Leakage risk | Use? | Reason |
|---|---:|---:|---:|---|
| feature_name | Yes/No | Low/Med/High | Yes/No | explanation |

## 11.4 Split strategy

Do not rely only on a naive random row split.

Inspect duplicate/order grouping, repeated entities, timestamps, and whether related rows from the same order can cross train/test boundaries.

Preferred evaluation:

- group-aware split if multiple rows represent one order/entity;
- chronological holdout where feasible;
- ordinary random split only as a diagnostic comparison.

---

# 12. Data Quality Validation

At ingestion, validate at least:

- expected columns;
- data types;
- null rates;
- duplicate keys/rows;
- valid target values;
- impossible numeric ranges;
- category cardinality;
- timestamp parsing;
- row-count sanity;
- class balance.

Validation must fail loudly if critical assumptions break.

Use Pydantic where appropriate for application/API schemas and testable validation functions for dataset-level checks.

---

# 13. EDA

EDA must answer business/modeling questions, not create decorative charts.

Minimum questions:

- What percentage of records are late?
- Is the target imbalanced?
- How does risk vary by shipping mode, region/market/category/time?
- What missing values exist?
- Are there duplicate orders/items?
- Which variables are unavailable at prediction time?
- Which fields appear to encode the target?
- Are there time/segment behavior changes?
- What simple baseline can be established?

Reusable logic belongs in the Python package, not only notebooks.

---

# 14. ML Modeling Plan

## 14.1 Baseline

Use at least one trivial/simple baseline, e.g. majority-class baseline or a simple defensible business rule.

## 14.2 Candidate models

Use course-aligned models:

1. Logistic Regression
2. Decision Tree
3. Random Forest
4. XGBoost

Do not add a more complex model family unless the core system is complete and there is a clear reason.

## 14.3 Metrics

Track:

- Precision
- Recall
- F1
- ROC-AUC
- Confusion Matrix
- PR-AUC if class balance makes it useful

## 14.4 Business-oriented emphasis

Primary business-facing emphasis:

> **Recall for truly high-risk/late shipments**, while keeping false positives manageable.

A false negative may mean an actually late shipment is not surfaced for investigation.

The acceptance threshold must be set after the Week 1 baseline, not invented in advance.

## 14.5 Model selection rule

Choose using leakage-safe performance, stability across splits, interpretability, inference simplicity, operational usefulness, and not merely the highest accuracy number.

---

# 15. Model Explainability

The UI/Copilot must not invent reasons for a prediction.

Preferred approach:

- expose prediction probability;
- expose a small number of model-supported feature contributions when feasible;
- otherwise clearly distinguish observed context from causal explanation.

Do not claim a feature "caused" a delay merely because it is associated with model output.

---

# 16. PostgreSQL

PostgreSQL is the operational data store.

Minimum logical tables:

```text
shipments
predictions
model_versions
agent_interactions
```

Possible simplified schema:

```text
shipments
- shipment_id
- input features required by app
- created_at

predictions
- prediction_id
- shipment_id
- model_version
- delay_probability
- predicted_class
- predicted_at

model_versions
- model_version
- mlflow_run_id
- status
- created_at

agent_interactions
- interaction_id
- shipment_id
- question
- answer
- reviewer_status
- created_at
```

Do not over-normalize the database for this capstone.

---

# 17. Data / Training Pipeline

Use a simple batch pipeline with **Prefect**.

Minimum flow:

```text
download/load raw data
    ↓
validate
    ↓
clean
    ↓
apply leakage-safe feature contract
    ↓
write processed data
    ↓
train/evaluate
    ↓
log to MLflow
    ↓
register/promote selected model
```

Streaming is not required. A manual retraining trigger is acceptable.

---

# 18. MLflow

Use MLflow for reproducibility and model lifecycle.

Log:

- run ID;
- parameters;
- feature/schema version;
- train/validation metrics;
- artifacts such as confusion matrix;
- selected model artifact.

Maintain a clear current/live model. A sophisticated production promotion system is not required.

---

# 19. DVC

Use DVC to version data/model artifacts that should not live directly in Git.

At minimum version:

- raw DataCo dataset reference/artifact;
- processed leakage-safe dataset;
- optional selected model artifact if not handled solely through MLflow.

Git stores code/config/metadata; DVC tracks large artifacts.

---

# 20. FastAPI

Minimum endpoints:

```text
GET  /health
POST /predict
GET  /shipments/{shipment_id}
POST /agent/analyze
```

Optional:

```text
GET /model/info
```

Example `/predict` response:

```json
{
  "shipment_id": "S-1001",
  "delay_probability": 0.78,
  "predicted_class": 1,
  "risk_level": "high",
  "model_version": "v1"
}
```

API rules:

- Pydantic request/response models;
- type hints;
- meaningful HTTP errors;
- no raw stack traces;
- health endpoint;
- load model once on startup where practical.

---

# 21. Operations Copilot

## Role

The agent is not the predictor. It is a constrained decision-support layer that helps a human understand a shipment exception by calling approved tools and returning a short, actionable, structured response.

## Constrained action space

The agent may only use an explicit allow-list of read-only tools. It must not create new tools or perform operational actions.

Minimum tools:

```text
get_prediction(shipment_id)
get_shipment(shipment_id)
query_similar_or_historical_shipments(...)
```

Optional enrichment tools:

```text
get_hamburg_traffic(...)
get_hamburg_traffic_forecast(...)
get_hamburg_weather(...)
```

External tools are contextual only. Core model inference must work without them.

## Example question

> Why is shipment S-1001 flagged as high risk and what should I investigate first?

## Required structured output

The agent must not return an open-ended essay. The response should follow a stable schema that can be validated with Pydantic.

Required fields:

```text
risk_summary
top_3_risk_factors
suggested_investigation_steps
evidence_used
confidence_or_notes
```

Example shape:

```text
Risk Summary:
High-risk shipment; model probability = 0.82

Top 3 Risk Factors:
1. ...
2. ...
3. ...

Suggested Investigation Steps:
1. ...
2. ...
3. ...

Evidence Used:
- prediction API
- shipment record
- historical comparison

Confidence / Notes:
...
```

## Required behavior

1. Retrieve the prediction rather than inventing a risk score.
2. Retrieve relevant shipment fields/history through approved tools.
3. Optionally retrieve live context only when the corresponding tool is available.
4. Separate observed facts from recommendations.
5. Reference the evidence/tool outputs used.
6. Limit recommendations to concrete investigation steps.
7. Return the required structured response.
8. Never claim unavailable live information.

## Forbidden behavior

- invent risk values;
- invent weather/traffic;
- claim causal explanations without evidence;
- execute real operational actions;
- contact carriers/customers;
- modify shipment data;
- write unrestricted/open-ended essays;
- access tools outside the allow-list;
- bypass API/database validation.

---

# 22. Reviewer / Validator

The reviewer remains deliberately small. Its purpose is to validate the structured agent output, not to create a second large autonomous workflow.

## Required deterministic validation

The MVP must check:

- prediction value matches the prediction tool/API;
- required structured fields are present;
- factual claims are supported by tool results;
- no invented weather/traffic is included;
- recommendations are framed as decision support;
- uncertainty is exposed appropriately.

Output:

```text
APPROVE
```

or

```text
REJECT + short reason
```

## Optional LLM reviewer

An additional LLM-based reviewer is **P2/optional**. Add it only if all P1 requirements are already on schedule. Deterministic validation is sufficient for the MVP.

---

# 23. UI — Streamlit Dashboard

**Selected UI technology:** Streamlit.

Streamlit is used because it allows a small Python-based operational dashboard to be built quickly without introducing a separate frontend stack that could threaten the four-week scope.

The UI is an operational dashboard, not a full logistics application.

Minimum components:

```text
Streamlit Dashboard
├── Shipment exception table
│   ├── shipment ID
│   ├── risk score
│   ├── risk level
│   └── filter/sort
├── Selected shipment detail
│   ├── relevant fields
│   ├── prediction
│   └── model version
└── Operations Copilot
    ├── question/input
    ├── structured actionable answer
    ├── evidence used
    └── reviewer status
```

Do not build authentication, payment, multi-tenancy, or complex admin screens.

The UI must remain a single workflow focused on identifying and investigating high-risk shipments.

---

# 24. Monitoring

## 24.1 Service monitoring — Prometheus + Grafana

Monitor at least:

- request count/traffic;
- request latency;
- error rate;
- prediction endpoint health;
- basic process/resource metric where practical.

## 24.2 ML monitoring — Evidently

Compare a production/current batch with a reference training/validation distribution.

Monitor:

- input feature drift;
- prediction distribution drift;
- data quality changes;
- prediction quality over time only when labels are available.

## 24.3 Drift definition

Drift means current shipment data no longer resembles the reference data used to train/validate the model.

Examples:

- shipping-mode distribution changes;
- geographic mix changes;
- category mix changes;
- prediction distribution shifts strongly.

Drift is a warning signal, not automatic proof that accuracy is bad.

## 24.4 Required alert

At least one alert must be demonstrable.

Preferred simple alert:

```text
API error rate above defined threshold
```

Optional second alert:

```text
important feature/prediction drift above threshold
```

---

# 25. Docker

Recommended Docker Compose services:

```text
api
postgres
prometheus
grafana
```

MLflow may run locally as a service if useful. The UI can be containerized if it does not complicate the core.

Goal:

```bash
docker compose up
```

should bring up the required local system with documented setup.

---

# 26. CI/CD — GitHub Actions

On push/pull request, run:

1. lint/format checks;
2. unit tests;
3. integration tests;
4. ML/data-quality tests;
5. model-quality gate where practical;
6. Docker build.

Suggested tooling:

- Ruff
- Black
- pytest
- pre-commit
- GitHub Actions

Optional: publish image to GHCR after local stability.

No cloud deployment is required for the core unless course requirements change.

---

# 27. Testing Strategy

## Unit tests

Examples: feature transformation, risk-level mapping, data validation, agent tool wrappers, leakage deny-list logic.

## Integration tests

Examples: `/predict` with loaded model, database read/write path, `/agent/analyze` with mocked external tools, pipeline-stage integration.

## ML tests

Examples: required features exist, forbidden leakage columns absent, prediction probability valid, model beats trivial baseline by agreed margin, model artifact loads.

## Data validation tests

Examples: target labels valid, row count sane, null-rate thresholds, schema stability.

## External API tests

Do not make fragile live internet calls part of every CI run. Mock Hamburg/DWD calls in CI; keep a manual/scheduled smoke check if needed.

---

# 28. Code Quality Rules

Production code should use:

- proper Python package structure;
- type hints;
- Pydantic;
- small testable functions/classes;
- configuration instead of hard-coded secrets;
- Ruff;
- Black;
- pre-commit.

Avoid notebook-only implementations.

---

# 29. Recommended Repository Structure

```text
Capstone-2/
├── README.md
├── PROJECT_STATUS.md
├── BACKLOG.md
├── pyproject.toml
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── MASTER_WORKFLOW.md
│   ├── CONTEXT.md
│   ├── EXPECTATIONS.md
│   ├── PROJECT_BLUEPRINT.md
│   ├── DECISION_LOG.md
│   ├── PROGRESS_LOG.md
│   └── RISK_REGISTER.md
├── src/
│   └── capstone/
│       ├── data/
│       ├── features/
│       ├── models/
│       ├── api/
│       ├── agents/
│       ├── monitoring/
│       └── config/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── ml/
├── pipelines/
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── evidently/
├── ui/
├── data/
├── presentation/
├── Dockerfile
└── docker-compose.yml
```

Do not create every subfolder before it is needed solely to make the repository look complex.

---

# 30. Four-Week Execution Plan

This sequence incorporates the teacher's review: establish the ML/data core first, expose it through an API and reproducible pipeline second, add the Streamlit/agent product layer third, and reserve the final week for monitoring, CI/CD, stabilization, and demo preparation.

## Week 1 — Data, leakage control, baseline modeling, database

### Goal

Prove the data and ML problem before product engineering.

### Tasks

- Download official Mendeley DataCo V5.
- Record DOI/license/source.
- Inspect actual row/column counts.
- Read `DescriptionDataCoSupplyChain.csv`.
- Define prediction timestamp.
- Audit candidate features for leakage.
- Identify business entity/grouping key.
- Define train/validation/test strategy.
- Clean and validate the data.
- Load cleaned data to PostgreSQL.
- Perform focused EDA.
- Implement trivial baseline and Logistic Regression.
- Train initial Decision Tree / Random Forest / XGBoost candidates if time permits after the leakage-safe baseline.
- Establish package/test/CI skeleton.

### Week 1 exit gate

Do not continue to product engineering unless:

- target is understood;
- leakage-safe feature set exists;
- evaluation split is defensible;
- at least one baseline runs;
- dataset license/source is documented;
- PostgreSQL path works;
- project still works without external live APIs.

## Week 2 — Model selection, FastAPI, pipelines, MLOps foundation

### Tasks

- complete feature engineering;
- complete candidate model comparison;
- error analysis;
- select the primary model;
- implement typed FastAPI prediction service;
- integrate FastAPI with PostgreSQL/model artifact;
- implement Prefect batch/training flow;
- add MLflow experiment tracking/model lifecycle;
- add DVC data/model versioning;
- add model/data-quality tests;
- prepare midterm architecture/results summary if required.

### Week 2 exit gate

- selected model is justified;
- `/predict` works;
- experiments are reproducible;
- data/model lifecycle is documented;
- no known target leakage remains.

## Week 3 — Streamlit dashboard + constrained Operations Copilot

### Tasks

- build the minimal Streamlit dashboard;
- show shipment risk ranking and shipment details;
- connect Streamlit to FastAPI and PostgreSQL;
- implement the constrained Operations Copilot;
- define the agent tool allow-list;
- enforce structured actionable output;
- connect agent to prediction/database tools;
- add one optional enrichment adapter (Hamburg traffic preferred) only if core work is stable;
- implement deterministic reviewer/validator;
- add LLM reviewer only if all P1 work remains on schedule;
- Dockerize/integrate the product path as needed.

### Week 3 exit gate

A user can open Streamlit, see shipment risks, inspect one shipment, request an explanation, and receive a validated structured response with risk factors, investigation steps, and evidence.

## Week 4 — Monitoring, CI/CD, stabilization, demo

### Tasks

- add/finalize Prometheus instrumentation;
- build minimal Grafana dashboard;
- add Evidently drift report;
- configure at least one alert;
- complete GitHub Actions CI/CD checks;
- integration testing;
- fix reliability issues;
- verify Docker/local startup;
- finalize README and run instructions;
- finalize architecture diagram and limitations;
- record/rehearse the demo;
- prepare final presentation;
- cleanup;
- final Definition-of-Done check.

### Week 4 rule

Do **not** add a new model family, streaming platform, cloud provider, external integration, or large product feature during Week 4.

---

# 31. 10–15 Minute Presentation Story

1. **Problem (~1 min):** logistics teams need to identify shipment exceptions early.
2. **User/business value (~1 min):** operations coordinator; prioritize investigation.
3. **Data/leakage (~2 min):** DataCo source, prediction-time contract, removed post-delivery columns.
4. **Modeling (~2 min):** baseline → candidate models → selected model → metrics/error analysis.
5. **Architecture (~2 min):** pipeline, PostgreSQL, MLflow/DVC, FastAPI, Docker.
6. **Demo (~3 min):** risk dashboard → shipment → copilot → evidence/reviewer.
7. **Reliability/MLOps (~1.5 min):** CI, monitoring, drift, alert, retraining path.
8. **Limitations/next step (~1 min):** open historical dataset, no real TMS/company validation, future company-specific retraining.

Focus on engineering decisions and trade-offs, not only accuracy.

---

# 32. Main Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Target leakage | High if ignored | Critical | Point-in-time feature audit; deny-list post-outcome fields; tests |
| Same order/entity leaks across split | Medium | High | Identify grouping key; group-aware/chronological evaluation |
| DataCo domain differs from Hamburg logistics | High | Medium | Honest framing; Hamburg data only as contextual demo |
| Dataset is older | Certain | Medium | Treat as ML-system demonstration; document limitation |
| Hamburg API downtime | Medium | Low | Optional enrichment; cache/mock; core works offline |
| Traffic forecast is demo service | Medium | Low | Never make it required for inference |
| HVCC requires commercial relationship | Medium/High | High | Excluded from MVP |
| Paid LLM dependency | Medium | High | Resolve free/local provider before agent implementation |
| Agent hallucination | Medium | Medium | Tool-grounded answers; validator; distinguish facts/recommendations |
| Scope growth | Medium | Critical | Scope freeze; one ML target; one primary agent |
| Monitoring over-engineering | Medium | Medium | Required metrics + one alert only |
| UI consumes too much time | Medium | Medium | Single dashboard workflow; no auth/multi-tenancy |
| Model score drops after leakage removal | Medium | Low/Medium | Treat leakage-safe honesty as strength; compare to baseline |
| CI depends on live APIs | Medium | Medium | Mock external APIs in CI |

---

# 33. Pre-Start Gate

Before implementation starts, explicitly confirm:

- [ ] Official DataCo V5 downloaded from Mendeley.
- [ ] License saved/documented as CC BY 4.0.
- [ ] `DescriptionDataCoSupplyChain.csv` reviewed.
- [ ] Actual row/feature counts confirmed locally.
- [ ] Target semantics confirmed.
- [ ] Prediction timestamp defined.
- [ ] Leakage feature audit created.
- [ ] Group/time split strategy selected.
- [ ] At least one leakage-safe baseline trained successfully.
- [ ] Hamburg traffic source fetched manually once, but project does not depend on it.
- [ ] Free/no-cost LLM approach selected or fallback agreed.
- [ ] UI approach selected from technology the developer can explain.
- [ ] Scope/non-goals accepted by the team.

If any of the first eight items fails, re-evaluate the project before spending a week on application engineering.

---

# 34. Definition of Done

The project is done when:

- business problem and user are clear;
- official data source/license documented;
- leakage-safe data contract exists;
- EDA and baseline complete;
- multiple models compared;
- selected model justified;
- model/data lifecycle reproducible;
- Python package structured and typed;
- tests pass;
- CI green;
- FastAPI serves model locally;
- Dockerized system runs locally;
- PostgreSQL integrated;
- pipeline reproducible;
- MLflow tracks experiments/model;
- DVC versions required artifacts;
- UI shows shipment risk;
- agent uses real tools instead of inventing context;
- reviewer/validation exists at least deterministically;
- Prometheus/Grafana monitoring exists;
- Evidently drift monitoring exists;
- at least one alert can be demonstrated;
- README explains setup/run/demo;
- limitations explicit;
- presentation fits 10–15 minutes.

---

# 35. Retraining Path

A fully automatic retraining platform is not required.

```text
new batch of shipment data
    ↓
validation
    ↓
drift / performance review
    ↓
manual retraining trigger
    ↓
Prefect training flow
    ↓
MLflow comparison
    ↓
quality gate
    ↓
promote new model version
```

A model is not promoted solely because it is newer.

---

# 36. Security / Privacy Boundaries

The capstone uses public/open data.

For a future commercial version, company shipment/customer data may be sensitive; least-privilege DB access, read-only agent SQL where possible, secret management, and logging hygiene would be required.

These future concerns should be documented but not expanded into a full security project during the capstone.

---

# 37. Commercial Evolution After the Capstone

A plausible future B2B product is:

> Connect a customer's TMS/ERP shipment data, learn company-specific delay patterns, and provide a private exception-management copilot for operations teams.

```text
Customer TMS / ERP
       ↓
customer-specific pipeline
       ↓
customer-specific model
       ↓
delay-risk API
       ↓
operations copilot
       ↓
human workflow
```

Commercial validation would require real customer data, stakeholder interviews, integration requirements, GDPR/security review, domain-specific validation, and measured KPI improvement. These are not required for the four-week capstone.

---

# 38. Rules for Future AI Coding Agents

Any future coding agent working on this repository must:

1. Read this file first.
2. Read `PROJECT_STATUS.md`.
3. Read `docs/EXPECTATIONS.md`.
4. Read `docs/MASTER_WORKFLOW.md`.
5. Check `BACKLOG.md`.
6. Do not add technologies merely because they are popular.
7. Do not expand the MVP beyond the non-goals.
8. Do not use a feature before checking prediction-time availability.
9. Do not claim an API is free without verifying its official source.
10. Do not make HVCC a required dependency.
11. Do not make any external API required for core model inference.
12. Do not introduce a paid API without explicit project-owner approval.
13. Update tests with meaningful behavior changes.
14. Update `PROJECT_STATUS.md` after meaningful work.
15. Record architectural changes in `docs/DECISION_LOG.md`.
16. Prefer small, explainable changes the project owner can defend in an interview.
17. Preserve the ability to complete and present the project within four weeks.

---

# 39. Source Registry

## Primary dataset

**DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS — Mendeley Data V5**  
https://data.mendeley.com/datasets/8gx2fvg2k6/5  
DOI: https://doi.org/10.17632/8gx2fvg2k6.5  
License: CC BY 4.0

## DataCo leakage-aware reference

**Interpretable and leakage-aware prediction of shipment delays in global supply chains**  
Modern Supply Chain Research and Applications, 2026  
https://www.emerald.com/mscra/article/doi/10.1108/MSCRA-04-2026-0035/1394831/Interpretable-and-leakage-aware-prediction-of

Use as methodological evidence that point-in-time leakage auditing matters. Do not copy its solution blindly; reproduce the reasoning independently.

## Hamburg current traffic

**Verkehrslage Hamburg**  
https://suche.transparenz.hamburg.de/dataset/verkehrslage-hamburg15  
License: Datenlizenz Deutschland – Namensnennung 2.0

## Hamburg traffic forecast

**GovData — Verkehrslageprognose Hamburg**  
https://data.gov.de/suche/daten/verkehrslageprognose-hamburgfa774

**Hamburg Transparency Portal**  
https://suche.transparenz.hamburg.de/dataset/verkehrslageprognose-hamburg

**SensorThings base**  
https://frost-transmove.germanywestcentral.cloudapp.azure.com/v1.1/

## DWD open weather/climate data

https://opendata.dwd.de/climate_environment/CDC/

Daily observations:  
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/

## HVCC — reference only, excluded from MVP

https://www.hvcc-hamburg.de/en/digital-services/api-port-call-data/

---

# 40. Decisions Still Requiring Explicit Confirmation

The project scope and data strategy can be frozen now, but these implementation decisions should be resolved before their respective work begins.

### A. Free LLM runtime/provider

Requirement: no paid dependency; developer must understand it; it should integrate with the learned LangChain/LangGraph/tool-calling workflow if an LLM agent is used.

### B. Team capacity / solo fallback

The teacher recommends working with 2–3 team members because ML + MLOps + agent + UI is a heavy four-week workload. If the project is executed solo, protect the deadline by keeping the Streamlit UI minimal, keeping weather/traffic forecast optional, and omitting the LLM reviewer unless the full P1 core is already complete.

### C. Exact production-simulation batch for drift

During Week 3, define how a shifted/current batch will be created for the Evidently demonstration without making false claims about real production traffic.

These are implementation choices, not reasons to change the business problem.

---

# 41. Final Scope Statement

> Build a leakage-aware machine-learning system that predicts late-delivery risk from open supply-chain data; expose the selected model through a tested, containerized FastAPI service; manage the model/data lifecycle with MLflow and DVC; store operational data in PostgreSQL; orchestrate the batch workflow; monitor service health and model/data drift; present shipment exceptions in a small Streamlit dashboard; and provide an evidence-grounded Operations Copilot that can combine model output, shipment history, and optional free Hamburg traffic/weather context to help a human prioritize investigation.

Anything outside that sentence should be treated as optional or out of scope unless a documented decision explicitly changes the project.
