# Data Documentation

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Purpose:** Document verified dataset facts, data-quality findings, leakage analysis, and the modeling data contract.  
**Current stage:** Initial dataset verification and pre-start data validation.

---

## 1. Primary Dataset

**Name:** DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS  
**Source:** Mendeley Data, Version 5  
**DOI:** https://doi.org/10.17632/8gx2fvg2k6.5  
**License:** CC BY 4.0  

Required source files:

```text
data/raw/DataCoSupplyChainDataset.csv
data/raw/DescriptionDataCoSupplyChain.csv
```

Raw source files are stored locally and intentionally excluded from Git.

---

## 2. Verified Local Dataset Facts

Verified from the local copy of `DataCoSupplyChainDataset.csv`.

### Shape

```text
Rows:    180,519
Columns: 53
```

### Candidate Target

```text
Late_delivery_risk
```

The source description defines this as:

```text
1 = late delivery
0 = not late delivery
```

### Target Distribution

```text
1: 98,977 rows (54.83%)
0: 81,542 rows (45.17%)
```

### Initial Interpretation

The target is not severely imbalanced.

This means the first baseline can use ordinary binary-classification metrics without treating extreme class imbalance as the primary problem.

---

## 3. First Verified Columns

The first columns in the local dataset include:

```text
Type
Days for shipping (real)
Days for shipment (scheduled)
Benefit per order
Sales per customer
Delivery Status
Late_delivery_risk
Category Id
Category Name
Customer City
```

No feature is approved for modeling merely because it exists in the dataset.

Every candidate feature must later pass the prediction-time availability and leakage audit.

---

## 4. Description File Consistency Check

The local dataset contains 53 columns, while the description file documents 52 fields.

A direct schema comparison found:

### Present in dataset but not exactly matched in description

```text
Order Zipcode
shipping date (DateOrders)
```

### Present in description but not exactly matched in dataset

```text
Shipping date (DateOrders)
```

### Interpretation

`shipping date (DateOrders)` vs `Shipping date (DateOrders)` is a case-only naming mismatch.

`Order Zipcode` appears in the dataset but does not have a matching documented field in the description file.

### Current Rule

`Order Zipcode` must be treated as undocumented until its semantics are independently confirmed.

Do not use it as a model feature merely because it is available.

---

## 5. Known Leakage-Risk Fields

The following fields are already identified as high-risk and require explicit exclusion or justification.

### `Delivery Status`

This field represents the delivery outcome/status and is therefore likely to reveal the target directly or indirectly.

Current status:

```text
Leakage risk: High
Model use: Do not use unless a future analysis proves it is available before the prediction timestamp.
```

### `Days for shipping (real)`

This field represents the actual realized shipping duration.

Because it is only known after shipping has occurred, it is a strong post-outcome leakage candidate.

Current status:

```text
Leakage risk: High
Model use: Exclude from predictive features.
```

### `Days for shipment (scheduled)`

This field represents planned/scheduled shipping duration.

Current interpretation:

```text
Potentially valid pre-outcome feature
```

It still requires confirmation against the final prediction timestamp.

---

## 6. Data Validation Status

### Completed

- [x] Official dataset files obtained.
- [x] Raw files stored locally under `data/raw/`.
- [x] Raw files excluded from Git.
- [x] Dataset loads successfully with pandas.
- [x] Local row count verified.
- [x] Local column count verified.
- [x] Target distribution verified.
- [x] Candidate target definition confirmed from the description file.
- [x] Dataset-vs-description schema mismatch checked.

### Not Yet Completed

- [ ] Define exact prediction timestamp.
- [ ] Audit every feature for prediction-time availability.
- [ ] Build complete leakage audit table.
- [ ] Identify entity/grouping keys.
- [ ] Define train/validation/test split strategy.
- [ ] Check null rates.
- [ ] Check duplicates.
- [ ] Check timestamp parsing.
- [ ] Check suspicious target-correlated fields.
- [ ] Create leakage-safe processed dataset.
- [ ] Train first leakage-safe baseline.

---

## 7. Prediction-Time Data Contract

Not finalized yet.

Before modeling begins, the project must define:

> At what exact business moment is the model supposed to predict late-delivery risk?

Once that point is fixed, every candidate feature will be classified as:

```text
Available before prediction
Available only after prediction
Ambiguous / requires verification
```

Only features genuinely available at prediction time may enter the model.

---

## 8. Planned Leakage Audit Table

The full audit will use this structure:

| Feature | Available at prediction time? | Leakage risk | Use? | Reason |
|---|---|---|---|---|
| `Delivery Status` | No / outcome-derived | High | No | Reveals delivery outcome |
| `Days for shipping (real)` | No | High | No | Realized shipping duration is known after shipment |
| `Days for shipment (scheduled)` | Likely yes | Low/Medium | Pending | Must confirm against prediction timestamp |
| `Order Zipcode` | Unknown | Unknown | Pending | Undocumented in description file |

This table will be expanded to all relevant columns before training.

---

## 9. Storage Strategy

### Local ML Data

```text
data/raw/
data/interim/
data/processed/
```

Purpose:

- `raw/` — original downloaded source files
- `interim/` — intermediate cleaned/transformed files
- `processed/` — leakage-safe model-ready datasets

These files are local and are not committed to Git.

### Operational Application Data

PostgreSQL will later be used for runtime/application data such as:

```text
shipments
predictions
model_versions
agent_interactions
```

PostgreSQL does not replace the local raw-training-data directory.

---

## 10. Reproducibility Rule

The repository should contain:

- source code;
- validation logic;
- data setup instructions;
- dataset source/version/license;
- schema expectations;
- transformations;
- DVC metadata later, if used.

The repository should not contain the raw DataCo dataset itself.

A new developer should be able to clone the repository, download the official dataset from the documented source, place it under `data/raw/`, and reproduce the validation and processing workflow.

---

## 11. Next Data Step

The next required data decision is:

> Define the exact prediction timestamp.

That decision is required before a trustworthy feature/leakage audit can be completed.
