# AI Engineering Capstone — Master Workflow & Documentation

## Purpose
This document is the operating manual for the capstone. It should let any team member—or future you—understand:
- what the project is trying to achieve,
- what has already been done,
- what is currently in progress,
- what must happen next,
- why major decisions were made,
- and whether the project satisfies the capstone expectations.

---

# 1. Non-Negotiable Project Expectations

The project should ultimately include:

- A clear real-world problem and value proposition
- Real data and a reproducible data pipeline
- EDA
- A baseline and multiple model experiments
- Clean Python package structure
- OOP where useful
- Type hints
- Pydantic validation
- Ruff / Black / pre-commit
- Automated tests
- GitHub Actions CI
- Model-quality gate
- FastAPI service
- Dockerized local execution
- Experiment tracking and model registry
- Data/model versioning
- Retraining path
- Monitoring
- Drift tracking
- At least one alert
- A usable UI
- A 10–15 minute final presentation
- Optional agentic layer when it performs a real function

Minimum engineering bar:

`tested Python package → FastAPI → Docker → GitHub Actions → monitoring + one alert`

---

# 2. Core Project Principle

> One strong problem + one strong modeling story + one polished product.

Do not add a technology because it is fashionable. Every major component must have a clear reason.

---

# 3. Project Phases

## Phase 0 — Topic Selection

### Goal
Choose a problem that is valuable, measurable, feasible in 4 weeks, data-supported, and suitable for AI Engineering.

### Questions
- Who is the user?
- What problem do they have?
- Why does it matter?
- Is the problem measurable?
- Is suitable data available?
- Is there a meaningful ML task?
- Can the project naturally support an API, pipeline, monitoring, and UI?
- Does an agent have a real role?
- Can a strong MVP be completed in 4 weeks?

### Exit Criteria
- [ ] Primary topic selected
- [ ] Backup topic selected
- [ ] Target user defined
- [ ] Business value clear
- [ ] Data source confirmed
- [ ] ML task measurable
- [ ] Agent role justified or explicitly excluded
- [ ] Feasible in 4 weeks

---

## Phase 1 — Problem Framing & Project Charter

### Deliverables
- Problem statement
- Target user
- Current pain
- Value proposition
- Inputs
- Outputs
- ML/AI task
- Baseline definition
- ML metric
- Product/system metrics
- MVP
- Nice-to-have features
- Out-of-scope list
- Risks

### Exit Criteria
- [ ] Problem explainable in 60 seconds
- [ ] Success measurable
- [ ] MVP fits 4 weeks
- [ ] Out-of-scope items explicit

---

## Phase 2 — Data Discovery & Data Contract

### Tasks
- Acquire sample data
- Inspect schema
- Identify missingness
- Identify leakage risk
- Identify imbalance
- Identify drift risk
- Define target variable
- Document data source and license
- Define SQL schema if relevant
- Create data validation tests
- Version data with DVC or equivalent

### Exit Criteria
- [ ] Data source works
- [ ] Schema documented
- [ ] Target valid
- [ ] Leakage risks understood
- [ ] Data-quality tests exist
- [ ] Reproducible ingestion path exists

---

## Phase 3 — EDA & Baseline

### Tasks
- Technical EDA
- Business-relevant EDA
- Define train/validation/test strategy
- Build simplest defensible baseline
- Log baseline experiment
- Begin error analysis

### Exit Criteria
- [ ] Baseline exists
- [ ] Metric reproducible
- [ ] Split strategy justified
- [ ] Major data issues documented
- [ ] First error analysis complete

---

## Phase 4 — Modeling & Experimentation

### Tasks
- Feature engineering
- Train 2–4 meaningful candidate models
- Track experiments
- Compare against baseline
- Tune only when justified
- Perform error analysis
- Define model-quality gate
- Select candidate model

### Exit Criteria
- [ ] Multiple models compared fairly
- [ ] Experiments reproducible
- [ ] Winning model justified
- [ ] Limitations documented
- [ ] Quality threshold defined

---

## Phase 5 — Engineering Foundation / Vertical Slice

### Required Foundation
- Proper Python package
- Type hints
- Pydantic
- Ruff
- Black
- pre-commit
- pytest
- FastAPI
- Docker
- GitHub Actions

### Vertical Slice
Build the thinnest working path:

`sample input → API → model → prediction → response`

### Exit Criteria
- [ ] Package imports cleanly
- [ ] FastAPI endpoint works
- [ ] Typed request/response
- [ ] Docker runs locally
- [ ] Unit tests pass
- [ ] Integration test passes
- [ ] CI green

---

## Phase 6 — Data/Training Pipeline & MLOps

### Tasks
- Select orchestration tool: Prefect / Airflow / Dagster
- Build training pipeline
- Use SQL/dbt if relevant
- Track experiments in MLflow
- Register models
- Version data/model artifacts
- Define model promotion pattern
- Define retraining path
- Manual retraining trigger is acceptable

### Exit Criteria
- [ ] Training pipeline runs end-to-end
- [ ] Experiment traceable to code + data version
- [ ] Current model version identifiable
- [ ] Retraining documented
- [ ] Model-quality gate works

---

## Phase 7 — Monitoring & Drift

### Service Monitoring
Track:
- latency
- traffic/request count
- error rate
- saturation/resource signal where feasible

### ML Monitoring
Track:
- input drift
- prediction drift/distribution
- prediction quality over time if labels are available

### Tools
- Prometheus
- Grafana
- Evidently

### Exit Criteria
- [ ] Monitoring dashboard works
- [ ] Drift report works
- [ ] At least one alert configured
- [ ] Alert threshold documented
- [ ] Monitoring can be demonstrated live

---

## Phase 8 — Product UI & Agent Layer

### UI
The UI must expose the real user workflow, not simply decorate the model.

### Agent Rule
An agent is justified only if it performs a real function such as:
- selecting tools,
- querying SQL,
- retrieving evidence,
- calling the ML API,
- planning a workflow,
- generating an explanation,
- validating another agent's output.

### Preferred Scope
Level 1:
`User → Agent → Tools / Model / Data → Answer`

Level 2:
`User → Primary Agent → Validator/Reviewer → Final Answer`

Avoid large multi-agent systems unless the problem genuinely requires them.

### Exit Criteria
- [ ] Main user workflow works from UI
- [ ] Agent role documented
- [ ] Agent tools explicit
- [ ] Tool inputs/outputs validated
- [ ] Agent evaluated
- [ ] Validator has objective checks if used
- [ ] Fallback behavior exists

---

## Phase 9 — Hardening, Demo & Handoff

### Tasks
- Freeze major features
- Fix bugs
- Improve critical-path tests
- Verify clean install
- Verify Docker startup
- Verify API
- Verify UI
- Verify monitoring
- Clean README
- Create architecture diagram
- Finalize documentation
- Write demo script
- Prepare presentation
- Document limitations
- Document future work

### Exit Criteria
- [ ] Clean clone can be run from documentation
- [ ] Dockerized service runs locally
- [ ] CI green
- [ ] UI works
- [ ] Monitoring works
- [ ] Alert works
- [ ] README complete
- [ ] Slides in repo
- [ ] Demo rehearsed
- [ ] Team can explain engineering decisions

---

# 4. Four-Week Execution Plan

## Week 1 — De-risk
- Problem definition
- Data acquisition
- EDA
- Baseline
- Repo structure
- Package skeleton
- FastAPI skeleton
- Docker skeleton
- Test skeleton
- CI skeleton

## Week 2 — Prove
- Candidate models
- Error analysis
- Data/training pipeline
- MLflow
- DVC
- Model-quality gate
- Mid-term presentation

## Week 3 — Productize
- Final model integration
- API hardening
- UI
- Agent layer
- Monitoring
- Drift tracking
- Alert

## Week 4 — Stabilize
No major new architecture.

Focus on:
- tests
- bug fixing
- reliability
- monitoring
- documentation
- demo
- presentation
- cleanup

---

# 5. Required Documentation Files

Recommended repository documentation:

- `README.md`
- `PROJECT_STATUS.md`
- `BACKLOG.md`
- `docs/PROJECT_CHARTER.md`
- `docs/ARCHITECTURE.md`
- `docs/DATA.md`
- `docs/MODELING.md`
- `docs/API.md`
- `docs/MLOPS.md`
- `docs/MONITORING.md`
- `docs/AGENT_DESIGN.md`
- `docs/DECISION_LOG.md`
- `docs/PROGRESS_LOG.md`
- `docs/RISK_REGISTER.md`
- `docs/HANDOFF.md`
- `presentation/`

---

# 6. PROJECT_STATUS.md Template

This is the most important continuity document.

Update it at the end of every meaningful working session.

## Project Status

**Last updated:**  
**Updated by:**  
**Current phase:**  
**Overall status:** Not started / On track / At risk / Blocked

### Current Objective
-

### Completed
-

### In Progress
-

### Next 3 Actions
1.
2.
3.

### Blockers / Risks
-

### Latest Decisions
-

### Technical State
- Data:
- Baseline:
- Best model:
- API:
- Docker:
- Tests:
- CI:
- MLflow:
- DVC:
- Pipeline:
- Monitoring:
- Drift:
- Alert:
- UI:
- Agent:
- Deployment:

### How to Resume
1. Read this file.
2. Read the latest progress-log entries.
3. Read unresolved backlog items.
4. Read latest architecture decisions.
5. Run tests.
6. Start Docker.
7. Run one end-to-end prediction.
8. Continue with “Next 3 Actions”.

---

# 7. Progress Log Template

Add one entry after every meaningful work session.

## YYYY-MM-DD

### Goal
-

### Completed
-

### Learned / Discovered
-

### Problems / Blockers
-

### Decisions Made
-

### Files / PRs / Experiments Affected
-

### Next Session — First Action
-

---

# 8. Decision Log / ADR Template

## ADR-XXX — Decision Title

**Date:**  
**Status:** Proposed / Accepted / Rejected / Superseded

### Context
What decision is needed?

### Decision
What did we choose?

### Alternatives Considered
-

### Why
-

### Consequences
Positive:
-

Negative:
-

Follow-up:
-

---

# 9. Definition of Done

The project is complete when a new person can:

1. Understand the problem from the README.
2. Identify the target user and value.
3. Identify the data source and assumptions.
4. See the baseline.
5. See fair model comparison and error analysis.
6. Reproduce training.
7. Identify the current model version.
8. Run the FastAPI service in Docker.
9. Use the UI.
10. Inspect tests and green CI.
11. View service monitoring.
12. View drift tracking.
13. See at least one configured alert.
14. Understand the agent's role, if present.
15. Read decisions and limitations.
16. Continue development without asking the original author what happened.

---

# 10. What To Do Right Now

Do not code the model yet.

The project is currently in:

**Phase 0 — Pre-Project / Topic Selection**

Immediate actions:

1. Create the project GitHub repository.
2. Add this master workflow document.
3. Create `PROJECT_STATUS.md`.
4. Set current phase to `0 — Topic Selection`.
5. Create `BACKLOG.md`.
6. Add the first backlog items:
   - define project-selection criteria
   - identify candidate topics
   - score candidate topics
   - confirm data availability
   - choose primary topic
   - choose backup topic
7. Commit this documentation as the first project commit.
8. Only after this foundation is created, begin topic selection.

Suggested first commit message:

`chore: initialize capstone documentation and project workflow`

At this moment, the correct next technical task is **not model building**.

The correct next project task is:

> Build the decision framework for selecting the capstone topic.
