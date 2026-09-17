# Decision Log

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Purpose:** Record important project decisions and the reasoning behind them.  
**Rule:** This file explains *why* important choices were made. It should not duplicate the backlog or project status.

---

## How to Use This File

Use one decision record for any choice that materially affects:

- project scope;
- architecture;
- data strategy;
- model strategy;
- APIs or external dependencies;
- agent behavior;
- UI technology;
- MLOps/monitoring approach;
- delivery timeline;
- security or deployment boundaries.

Do **not** use this file for routine implementation details.

Each decision should contain:

```md
## ADR-XXX — Decision title

**Date:** YYYY-MM-DD  
**Status:** Accepted / Superseded / Rejected

### Context
What problem or uncertainty required a decision?

### Decision
What was decided?

### Alternatives Considered
What other reasonable options were considered?

### Why
Why was this choice made?

### Consequences
What does this decision imply for the project?
```

If a decision changes later, do not delete the old record. Mark it `Superseded` and add a new ADR.

---

# ADR-001 — Select the Logistics Exception Management Capstone Topic

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The capstone needed to satisfy all of the following:

- real business relevance;
- alignment with the German job market;
- strong fit for AI Engineering / ML Engineering;
- free and sufficiently large training data;
- meaningful ML rather than a simple LLM wrapper;
- natural fit for MLOps, monitoring, API, UI, and an AI agent;
- realistic completion within approximately four weeks.

Several candidate topics were evaluated, including support-ticket triage, predictive maintenance, energy forecasting, industrial quality inspection, cybersecurity, and logistics.

### Decision

Select:

> **LogiGuard AI — AI Logistics Exception Management & Operations Copilot**

The core product predicts late-delivery risk and helps a logistics operations user prioritize high-risk shipment exceptions.

### Alternatives Considered

- AI Incident & Support Triage Platform
- Industrial Predictive Maintenance Copilot
- German Energy Forecasting & Operations Agent
- Industrial Visual Quality Inspection System
- Cybersecurity Alert Triage Copilot
- EU Tender Intelligence Platform

### Why

The logistics topic provides a strong balance of:

- business relevance;
- Germany/Hamburg relevance;
- classical ML depth;
- software engineering;
- MLOps;
- agentic AI;
- product/UI potential;
- available free/open data;
- portfolio value.

### Consequences

The project is no longer in topic-selection mode.

Future work should focus on validating the data and executing the approved scope rather than continuing to search for new capstone ideas.

---

# ADR-002 — Use DataCo as the Primary Training Dataset

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The project needs a dataset that is:

- free;
- large enough for ML;
- legally reusable for a capstone;
- suitable for shipment/delivery-risk prediction;
- available without paid API access.

### Decision

Use:

> **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS — Mendeley Data V5**

as the primary training dataset.

Approximate published scale:

- ~180,000 records
- ~53 structured features

License:

- CC BY 4.0

### Alternatives Considered

- proprietary logistics APIs;
- port-specific commercial data;
- live AIS-based vessel data;
- smaller synthetic logistics datasets.

### Why

DataCo provides sufficient structured supply-chain data for a classical binary-classification problem and does not require a paid subscription.

### Consequences

The model must be presented honestly as trained on an open historical supply-chain dataset, not as validated on a real Hamburg logistics company's production data.

The exact row/column counts and target semantics must still be verified locally before implementation proceeds.

---

# ADR-003 — Define the Core ML Problem as Binary Classification

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The project needs one clear ML problem that can be trained, evaluated, deployed, monitored, and explained within four weeks.

### Decision

Use a binary classification task:

```text
0 = not late / lower late-delivery risk
1 = late-delivery risk
```

Candidate target:

```text
Late_delivery_risk
```

### Alternatives Considered

- multi-class low/medium/high risk prediction;
- delay-duration regression;
- ETA prediction;
- route optimization;
- multiple ML targets.

### Why

Binary classification:

- matches the source dataset naturally;
- is easier to evaluate and defend;
- supports Logistic Regression, Decision Tree, Random Forest, and XGBoost;
- keeps the capstone focused;
- fits the 4-week scope.

### Consequences

Any Low/Medium/High labels shown in the UI will be presentation/business layers derived from model probability, not separate model classes, unless later evidence justifies changing the target.

---

# ADR-004 — Enforce Strict Data-Leakage Controls

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The DataCo dataset contains delivery-related fields that may only be known after the delivery outcome.

Using these as model inputs could produce unrealistically high model performance.

### Decision

Create a prediction-time feature audit before model training.

Every feature must answer:

> Would this value be available when the prediction is supposed to be made?

Fields that fail this test must be excluded.

Known high-risk examples include:

- `Delivery Status`
- `Days for shipping (real)`

### Alternatives Considered

- use all available features;
- rely only on correlation-based feature selection;
- remove leakage only after modeling.

### Why

The project must demonstrate realistic predictive modeling, not inflated performance caused by future information.

### Consequences

A leakage-safe model with lower performance is preferred over a leakage-heavy model with impressive but invalid metrics.

Leakage tests must become part of the automated ML/data-quality checks.

---

# ADR-005 — Keep the Four-Week MVP Narrow

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The project must include ML, API, MLOps, monitoring, UI, and an agent, all within approximately four weeks.

Adding unrelated infrastructure would increase delivery risk without improving the capstone's learning value.

### Decision

Keep the MVP limited to:

- one main ML problem;
- one operational dashboard;
- one main agent workflow;
- one monitoring setup;
- one local containerized deployment path.

Explicitly exclude from the MVP:

- Kafka;
- Spark;
- Kubernetes;
- route optimization;
- GPS fleet tracking;
- AIS trajectory modeling;
- autonomous dispatching;
- large multi-agent systems;
- unnecessary AWS/cloud architecture;
- proprietary logistics integrations.

### Alternatives Considered

A broader "full logistics platform" with streaming, routing, live tracking, and multiple agent roles.

### Why

The teacher explicitly supported avoiding unnecessary tools and keeping Kafka, Spark, and Kubernetes out of scope.

### Consequences

New major technologies may only be added if the full P1 core is already complete and the scope change is documented.

---

# ADR-006 — Use FastAPI as the Model/Application API

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The selected ML model must be exposed to the UI and agent through a typed service layer.

### Decision

Use FastAPI with Pydantic request/response validation.

Minimum endpoints:

```text
GET  /health
POST /predict
GET  /shipments/{shipment_id}
POST /agent/analyze
```

### Alternatives Considered

- direct model calls from the UI;
- Flask;
- frontend calling model files directly.

### Why

FastAPI aligns with the course expectations and provides:

- typed endpoints;
- validation;
- clear separation between model/service/UI;
- straightforward testing;
- clean integration with the agent.

### Consequences

The Streamlit UI must call the API rather than implement duplicate prediction logic.

---

# ADR-007 — Use Streamlit for the Capstone UI

**Date:** 2026-09-16  
**Status:** Accepted

### Context

The project needs a usable UI, but building a full separate frontend stack would consume too much time.

The teacher specifically recommended a Streamlit dashboard.

### Decision

Use Streamlit for the operational dashboard.

The UI will contain:

- shipment exception table;
- risk score / risk level;
- selected-shipment details;
- Operations Copilot interface;
- evidence/reviewer information where useful.

### Alternatives Considered

- React or another separate frontend framework;
- no UI;
- notebook-based interface.

### Why

Streamlit:

- is Python-based;
- is fast to implement;
- is easy to explain;
- keeps frontend complexity low;
- supports the 4-week deadline.

### Consequences

The UI remains intentionally minimal.

No authentication, multi-tenancy, payment, or complex admin interface will be built.

---

# ADR-008 — Constrain the Operations Copilot

**Date:** 2026-09-16  
**Status:** Accepted

### Context

The teacher recommended constraining the agent's action space so it produces reliable, actionable outputs rather than open-ended essays.

A free-form agent would increase hallucination risk and make the project harder to test.

### Decision

The Operations Copilot will:

- use an explicit read-only tool allow-list;
- not create new tools;
- not perform autonomous operational actions;
- not modify shipment data;
- not contact customers/carriers;
- not invent model scores, traffic, or weather.

Minimum tools:

```text
get_prediction(shipment_id)
get_shipment(shipment_id)
query_similar_or_historical_shipments(...)
```

Optional read-only tools:

```text
get_hamburg_traffic(...)
get_hamburg_traffic_forecast(...)
get_hamburg_weather(...)
```

### Alternatives Considered

- unrestricted general-purpose agent;
- fully autonomous agent;
- multi-agent planner/executor architecture.

### Why

A constrained agent is:

- easier to test;
- easier to defend;
- safer;
- more useful to an operations user;
- more realistic for a production-style system.

### Consequences

The agent becomes a decision-support layer, not a general chatbot or autonomous operator.

---

# ADR-009 — Require Structured Agent Output

**Date:** 2026-09-16  
**Status:** Accepted

### Context

The teacher recommended actionable output such as "Top 3 Factors for Risk" and "Suggested Investigation Steps" instead of long free-form answers.

### Decision

The agent response must follow a stable structured schema.

Required fields:

```text
risk_summary
top_3_risk_factors
suggested_investigation_steps
evidence_used
confidence_or_notes
```

The response should be validated with Pydantic where practical.

### Alternatives Considered

- unrestricted natural-language response;
- long conversational explanation.

### Why

Structured responses improve:

- usability;
- testability;
- reliability;
- UI rendering;
- reviewer validation;
- presentation clarity.

### Consequences

The agent prompt, tool layer, API response, validator, and Streamlit UI must all support the same structured output contract.

---

# ADR-010 — Use Deterministic Validation as the Required Reviewer

**Date:** 2026-09-16  
**Status:** Accepted

### Context

A second LLM reviewer could improve validation, but it would add complexity and possibly cost/time risk.

### Decision

For the MVP, implement deterministic validation that checks:

- prediction value consistency;
- required structured fields;
- factual claims against tool outputs;
- no invented external context;
- recommendation wording;
- uncertainty handling.

An LLM reviewer is optional/P2.

### Alternatives Considered

- mandatory second-agent reviewer;
- no validation layer;
- fully autonomous multi-agent workflow.

### Why

Deterministic validation satisfies the reliability goal while protecting the 4-week timeline.

### Consequences

The project does not depend on a second LLM call.

If time remains after all P1 work is complete, a small LLM reviewer may be added.

---

# ADR-011 — Keep External Hamburg Data Optional

**Date:** 2026-09-15  
**Status:** Accepted

### Context

Hamburg traffic and DWD weather data provide useful local operational context, but external services may be unavailable or change.

### Decision

Use Hamburg traffic and DWD weather only as optional enrichment tools.

Core `/predict` inference must work without them.

### Alternatives Considered

- require live traffic/weather for every prediction;
- train the primary model directly on live external APIs;
- omit all local context.

### Why

Optional enrichment provides Hamburg relevance without making the project fragile.

### Consequences

CI must mock external API calls.

If an external service is unavailable during the demo, the core ML/API/UI workflow must still work.

---

# ADR-012 — Exclude HVCC as an MVP Dependency

**Date:** 2026-09-15  
**Status:** Accepted

### Context

HVCC provides useful port-call data, but unrestricted free public access was not confirmed.

The project must not become dependent on paid or uncertain APIs.

### Decision

Do not use HVCC as a required MVP dependency.

### Alternatives Considered

- build the project around HVCC port-call data;
- assume academic access will be available.

### Why

The project has a zero-paid-API constraint and must avoid future access blockers.

### Consequences

HVCC remains a possible future extension only if explicit free/academic access is confirmed.

---

# ADR-013 — Use Local/Open MLOps Components

**Date:** 2026-09-15  
**Status:** Accepted

### Context

The capstone must demonstrate production-style model lifecycle and monitoring without requiring paid infrastructure.

### Decision

Use:

- PostgreSQL — operational data store
- Prefect — batch pipeline orchestration
- MLflow — experiment/model tracking
- DVC — data/model artifact versioning
- Docker / Docker Compose — reproducible local runtime
- Prometheus + Grafana — service monitoring
- Evidently — data/prediction drift monitoring
- GitHub Actions — CI/CD checks

### Alternatives Considered

- paid managed cloud services;
- Kubernetes;
- complex streaming infrastructure.

### Why

These tools match the course expectations, can run locally, and support a complete end-to-end engineering story.

### Consequences

Public cloud deployment is optional, not required for completion.

---

# ADR-014 — Adopt the Teacher-Reviewed Four-Week Timeline

**Date:** 2026-09-16  
**Status:** Accepted

### Context

The original plan was technically valid but aggressive for one person.

The teacher suggested a more practical execution sequence.

### Decision

Use this implementation order:

### Week 1

- clean/validate data;
- remove leaked features;
- train baseline/initial models;
- set up PostgreSQL.

### Week 2

- finalize model selection;
- build FastAPI;
- build Prefect pipeline;
- add MLflow/DVC and model/data checks.

### Week 3

- build Streamlit dashboard;
- connect FastAPI/database;
- implement constrained Operations Copilot and tools;
- add deterministic validator;
- Dockerize/integrate product path.

### Week 4

- Prometheus/Grafana;
- Evidently;
- alert;
- CI/CD;
- stabilization;
- documentation;
- demo recording;
- presentation.

### Alternatives Considered

- build all infrastructure in parallel;
- implement UI/agent before the core ML/API path;
- add monitoring during early modeling.

### Why

The sequence builds dependencies in a logical order and protects the deadline.

### Consequences

Week 4 is a stabilization week, not a feature-development week.

---

# ADR-015 — Protect the Project if Executed Solo

**Date:** 2026-09-16  
**Status:** Accepted

### Context

The teacher warned that ML + MLOps + agent + UI is a heavy workload for one person and recommended 2–3 team members.

### Decision

If the project is executed solo:

- keep Streamlit minimal;
- keep Hamburg traffic forecast optional;
- keep DWD weather optional;
- keep the LLM reviewer optional;
- prioritize all P0/P1 backlog items over P2/P3 features.

### Alternatives Considered

- preserve all optional features even if solo;
- expand the project to match a larger team scope.

### Why

The capstone must be complete and defensible rather than broad and unfinished.

### Consequences

Optional features may be dropped without changing the core project definition.

---

# Decision Summary

Current accepted project decisions:

```text
Topic:
LogiGuard AI — Logistics Exception Management & Operations Copilot

ML:
Binary late-delivery-risk classification

Primary data:
DataCo V5 / Mendeley / CC BY 4.0

Core models:
Logistic Regression
Decision Tree
Random Forest
XGBoost

Database:
PostgreSQL

API:
FastAPI + Pydantic

Pipeline:
Prefect

MLOps:
MLflow + DVC

UI:
Streamlit

Agent:
Constrained, read-only, tool-using Operations Copilot

Agent output:
Structured and actionable

Validation:
Deterministic required
LLM reviewer optional

Monitoring:
Prometheus + Grafana + Evidently

Runtime:
Docker / Docker Compose

CI/CD:
GitHub Actions

External context:
Hamburg traffic / DWD weather optional

Paid/uncertain APIs:
Not required

Major excluded scope:
Kafka, Spark, Kubernetes, route optimization, GPS/AIS tracking, autonomous dispatching, large multi-agent systems
```
