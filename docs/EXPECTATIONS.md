# AI Engineering Capstone Expectations

## Clean and Structured Code
- proper Python package, not notebook-only
- OOP where appropriate
- type hints
- Pydantic validation
- Ruff
- Black
- pre-commit hooks

## Testing and CI/CD
- pytest unit tests
- integration tests
- ML tests
- data-validation tests
- GitHub Actions
- linting in CI
- tests on push / pull request
- model-quality gate
- Docker build in CI
- secrets management
- optional image publishing to GHCR

## Model Service API and Docker
- FastAPI
- typed endpoints
- request validation
- response validation
- Dockerfile
- containerized local execution

Public deployment is optional.

## Data Pipeline
Use a pipeline that feeds the model.

Possible tools:
- Prefect
- Airflow
- Dagster
- SQL
- dbt
- batch processing
- streaming

The technical choice should be justified by the project problem and scope.

## MLOps
Expected capabilities:
- reproducible experiments
- model version tracking
- training traceability
- model registry
- retraining path
- clear deployment / promotion pattern

Expected tools:
- MLflow for experiment tracking and model registry
- DVC for data and/or model versioning

Manual retraining is acceptable.

## Monitoring

### Service Monitoring
Use Prometheus + Grafana.

Track at minimum:
- latency
- traffic
- errors
- saturation or resource signal where feasible

### ML Monitoring
Use Evidently.

Track at minimum:
- input drift
- prediction drift / distribution
- prediction quality over time when labels are available

At least one alert must be configured.

## Deliverables
- structured GitHub repository
- documented README
- tests present
- green CI
- running containerized FastAPI service
- CI/CD pipeline
- monitoring dashboard
- drift tracking
- at least one alert
- final presentation
- presentation slides stored in the repository

## Presentation
Approximate duration: 10–15 minutes.

Focus on:
- the real problem
- system architecture
- engineering decisions
- model lifecycle
- reliability
- monitoring
- limitations
- not only model accuracy

## Minimum Engineering Bar

> Tested Python package → containerized FastAPI service → GitHub Actions pipeline → monitoring + one live alert