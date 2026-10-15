# LogiGuard AI

**Shipment delay-risk prediction and an evidence-grounded Operations Copilot.**

LogiGuard is an AI engineering capstone that helps logistics operators identify potentially late orders, prioritize shipment exceptions, and investigate them through a constrained copilot. It is a decision-support prototype, not a live fleet-tracking or autonomous dispatch system.

## Demo Video

Watch the LogiGuard AI demo to see the complete workflow,
including order submission, late-delivery risk prediction,
operations insights, and API monitoring.

[Watch or Download Demo Video](docs/demo/logiguard-demo.mp4)

## 1. Dataset and data preparation

The historical training source is **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS**, Mendeley Data v5 ([source](https://data.mendeley.com/datasets/8gx2fvg2k6/5), [DOI](https://doi.org/10.17632/8gx2fvg2k6.5), CC BY 4.0).

Download `DataCoSupplyChainDataset.csv` and `DescriptionDataCoSupplyChain.csv` from the source and place them in `data/raw/`. The raw CSV files are not stored in Git.

```text
data/raw/          Historical source files
data/interim/      Intermediate exploration and splits
data/processed/    Timestamped order-level datasets
```

From the repository root, with Python **3.14** and a virtual environment:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pipelines.prepare_data
```

The preparation pipeline loads and validates the raw data, cleans it, aggregates item-level rows to one record per order, and writes a **new timestamped CSV** under `data/processed/YYYY-MM-DD_HH-MM/`. The verified existing processed dataset contains **65,752 orders**. Data preparation does not retrain or activate a model.

## 2. Model training and selection (manual)

LogiGuard uses a chronological train/validation/test split, training-only preprocessing, and leakage-conscious order-time features. A versioned Logistic Regression baseline is available; the selected model is **Stage 2 XGBoost**.

```bash
# Optional: train a versioned baseline
python -m pipelines.train_baseline

# Optional: train a new XGBoost candidate; does NOT activate it
python -m pipelines.train_final_model
```

Final-model training reads the newest timestamped processed dataset, creates a new directory in `models/<run_id>/`, and saves the trained model, fitted preprocessor, and evaluation metadata. For future runs, metadata also records the selected training CSV filename and path.

**Activation is separate and requires deliberate human action:**

```bash
python -m pipelines.promote_model
# Enter the exact model run ID at the prompt.
```

Promotion checks that the selected model bundle is present and its **validation ROC-AUC is at least 0.75** before updating `models/current_model.json`. **Do not run promotion merely to set up or demonstrate the application.** Training, monitoring, DVC, MLflow, and CI do not automatically promote a model.

### Active model

| Item | Verified value |
|---|---|
| Model run | `2026-10-02_10-36` |
| Algorithm | Stage 2 XGBoost |
| Decision threshold | `0.40` |
| Validation ROC-AUC | `0.7717` |
| Test ROC-AUC | `0.7747` |
| Test recall | `0.8403` |
| Training CSV | `data/processed/2026-10-02_10-19/order_level_clean_2026-10-02_10-19.csv` |

The historical training-data provenance was confirmed by the project developer and recorded in the model metadata after training. Metrics are historical holdout results, **not measured production accuracy**.

## 3. Run the application with Docker Compose

Requirements: Docker with Compose, and the versioned active-model artifacts in `models/`. Create a local `.env` file in the project root (do **not** commit it):

```dotenv
POSTGRES_DB=logiguard
POSTGRES_USER=logiguard_user
POSTGRES_PASSWORD=CHANGE_ME
GEMINI_API_KEY=YOUR_KEY_IF_USING_THE_LLM_COPILOT
```

Then run:

```bash
docker compose up --build -d
docker compose ps
```

The API container creates the required PostgreSQL tables on startup. The Compose PostgreSQL instance is exposed on **host port 5433**, not 5432; services inside Docker use `db:5432`. The database is stored in a named Docker volume.

| Service | URL |
|---|---|
| Streamlit dashboard | http://localhost:8501 |
| FastAPI interactive docs | http://localhost:8000/docs |
| API health | http://localhost:8000/health |
| Prometheus metrics | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

```bash
# Stop services without deleting persisted database or monitoring volumes
docker compose down
```

The UI connects to the API through the `API_URL` environment variable, set to `http://api:8000` in Compose. The API needs PostgreSQL through `DATABASE_URL`. The Operations Copilot uses grounded shipment/prediction tools and an LLM integration; a valid Gemini API key is needed for its LLM-backed responses. Core ML inference does not require external traffic or weather feeds.

## 4. Operational API and dashboard

The FastAPI application exposes these implemented endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/predict` | Predict an order-level input and persist the order/prediction |
| POST | `/predict/raw` | Accept item-level raw order input, prepare it, predict, and persist records |
| GET | `/shipments` | List shipments by descending predicted delay risk |
| GET | `/shipments/{order_id}` | Read one shipment |
| GET | `/orders/{order_id}` | Read processed order data |
| GET | `/raw-orders/{order_id}` | Read the original raw order payload |
| GET | `/predictions/{order_id}` | Read its stored prediction |
| POST | `/copilot` | Investigate an order with an allowed action |
| GET | `/metrics` | Prometheus metrics |

The `/copilot` request accepts an `order_id` and one of `prediction`, `shipment_status`, or `similar_shipments`. It combines read-only operational evidence with a constrained, validated response; it does **not** modify shipments or carry out dispatcher actions. The Streamlit UI displays the shipment queue, selected details, and copilot results. See `/docs` for complete request schemas rather than relying on partial example payloads.

## 5. Model and data lifecycle tooling

**DVC — dataset versioning.** The processed dataset `data/processed/2026-10-02_10-19/order_level_clean_2026-10-02_10-19.csv` has a tracked `.csv.dvc` pointer. The large CSV itself is excluded from Git. On the development machine:

```bash
python -m pip install "dvc==3.67.1"
python -m dvc status
```

The tracked data is stored in a **local DVC cache**; no shared DVC remote is configured. Cloning the Git repository alone does not provide the CSV or guarantee it can be retrieved with `dvc pull`.

**MLflow — historical experiment record.** The active model's hyperparameters, holdout metrics, and dataset provenance were imported into an independent **local SQLite** tracking database (`mlflow.db`). This was a *historical import*, not a model-training run executed by MLflow. MLflow does not control deployment or model promotion.

```bash
# With development dependencies installed and a populated local mlflow.db:
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001
```

MLflow UI: http://127.0.0.1:5001. The database is local/ignored by Git; another clone will not have the existing experiment history automatically. The optional registration script `python -m pipelines.register_existing_model_mlflow` creates a **new** import run when executed; it is not part of normal application startup and should not be rerun unnecessarily.

## 6. Monitoring

- **Prometheus** scrapes the FastAPI `/metrics` endpoint every **15 seconds**.
- **Grafana** provides a provisioned API dashboard with traffic, 5xx error rate, p95 latency, and memory panels.
- An alert rule, `LogiGuardAPIDown`, detects failure to scrape the API for **one minute**. A notification delivery channel has **not** been configured.
- **Evidently** provides an on-demand report comparing historical reference features/model probabilities with stored predictions for the active model:

```bash
# Requires the processed dataset, active model bundle, and stored predictions.
python -m pipelines.monitor_drift
```

Reports are saved locally under `monitoring/reports/`. With fewer than **30** current observations, the report marks drift results **INSUFFICIENT DATA** and exploratory. Drift is **not** proof of model-performance degradation; production accuracy requires actual delivery-outcome labels, which are not currently supplied by this workflow. Monitoring never automatically retrains or replaces the model.

## 7. Tests and CI

```bash
python -m ruff check .
```

Tests that exercise PostgreSQL must use an **isolated test database**. GitHub Actions automatically provisions PostgreSQL 17 with database `logiguard_test`, creates tables, runs Ruff and pytest, then checks the Docker image build. For a locally configured PostgreSQL connection, the following runs tests against `logiguard_test` without changing the application's normal `.env`:

```bash
python - <<'PY'
import os
import subprocess
import sys
from src.database.connection import engine

url = engine.url.set(database="logiguard_test")
assert url.database == "logiguard_test"
env = {**os.environ, "DATABASE_URL": url.render_as_string(hide_password=False)}
raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q"], env=env))
PY
```

**Create the test database and its tables before local tests**; do not point the test suite at the operational `logiguard` database. Most recently verified locally: **33 passed, 4 third-party warnings; Ruff passed**. CI is defined in `.github/workflows/ci.yml` and runs on pushes and pull requests.

## 8. Repository layout

```text
src/                 Data processing, features, model inference, API, agent, database
pipelines/           Data preparation, training, manual promotion, drift, MLflow import
models/              Versioned model bundles and active-model pointer
data/                Raw, intermediate, and versioned processed datasets
ui/                  Streamlit dashboard
monitoring/          Prometheus/Grafana configuration and local drift reports
tests/               Unit and integration tests
.github/workflows/    GitHub Actions CI
docs/                Decisions, progress log, architecture and engineering documentation
```

## 9. Boundaries and reproducibility

This project uses historical global supply-chain data; it has **not** been validated on real live freight-operator shipments. Model scores support prioritization, not causal explanations or automated operational decisions. Training and model activation are manual and separate. DVC data content and MLflow history currently remain local and need separately managed storage for reproduction on another machine. See `data/README.md` for dataset acquisition and `docs/PROGRESS_LOG.md` for the implementation history.
