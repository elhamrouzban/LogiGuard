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
