# Data Documentation

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Current stage:** Week 1 — Data Validation / Leakage Audit  
**Purpose:** Keep verified dataset facts, prediction-time assumptions, leakage decisions, validation status, and next data steps in one concise source of truth.

---

## 1. Dataset

**Name:** DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS  
**Source:** Mendeley Data, Version 5  
**DOI:** https://doi.org/10.17632/8gx2fvg2k6.5  
**License:** CC BY 4.0

Required local files:

```text
data/raw/DataCoSupplyChainDataset.csv
data/raw/DescriptionDataCoSupplyChain.csv
```

Raw data stays local and is excluded from Git.

---

## 2. Verified Facts

```text
Rows:    180,519
Columns: 53
Target:  Late_delivery_risk
```

Target meaning from the source description:

```text
1 = late delivery
0 = not late delivery
```

Target distribution:

```text
1: 98,977 rows (54.83%)
0: 81,542 rows (45.17%)
```

The target is not severely imbalanced.

### Description-file mismatch

The dataset has 53 columns while the description file documents 52 fields.

Verified mismatch:

```text
Dataset:     shipping date (DateOrders)
Description: Shipping date (DateOrders)
```

This is only a case difference.

`Order Zipcode` exists in the dataset but has no matching documented field in the description file, so it remains **undocumented/pending verification**.

---

## 3. Verified Timeline and Target Logic

### Actual shipping days

Across all **180,519 rows**:

```text
Days for shipping (real)
=
calendar-day difference between
order date (DateOrders)
and
shipping date (DateOrders)
```

### Target-generation rule

Across all **180,519 rows**, `Late_delivery_risk` is exactly reproduced by:

```text
Late_delivery_risk = 1
if:
Days for shipping (real) > Days for shipment (scheduled)
and
Delivery Status != "Shipping canceled"
```

For canceled shipments, the target remains `0`.

### Interpretation

The delay label measures the order-to-shipping period against the scheduled duration. It therefore includes time before shipment leaves the company and is not limited to transportation time after shipment.

---

## 4. Prediction-Time Contract

### Working prediction point

> Predict late-delivery risk at **order creation time**, before the actual shipping date and realized shipping duration are known.

A feature is valid only if it would genuinely be available at that moment.

---

## 5. Feature Availability / Leakage Audit

### Confirmed future information or target leakage

Do not use as model features:

- `Days for shipping (real)`
- `Delivery Status`
- `shipping date (DateOrders)`
- `Late_delivery_risk` — target

### Likely available at order time

- `Type`
- `Days for shipment (scheduled)`
- `Category Id`
- `Category Name`
- `Customer City`
- `Customer Country`
- `Customer Id`
- `Customer Segment`
- `Customer State`
- `Customer Zipcode`
- `Department Id`
- `Department Name`
- `Market`
- `Order City`
- `Order Country`
- `Order Customer Id`
- `order date (DateOrders)`
- `Order Id`
- `Order Item Cardprod Id`
- `Order Item Discount`
- `Order Item Discount Rate`
- `Order Item Id`
- `Order Item Product Price`
- `Order Item Quantity`
- `Sales`
- `Order Item Total`
- `Order Region`
- `Order State`
- `Order Zipcode`
- `Product Card Id`
- `Product Category Id`
- `Product Name`
- `Product Price`
- `Shipping Mode`

These are not yet the final feature set; identifier leakage, cardinality, redundancy, usefulness, and split leakage still need review.

### Exclude for identity / privacy / low modeling value

- `Customer Email`
- `Customer Fname`
- `Customer Lname`
- `Customer Password`
- `Customer Street`
- `Product Image`

### Ambiguous — verify before use

- `Benefit per order`
- `Sales per customer`
- `Latitude`
- `Longitude`
- `Order Item Profit Ratio`
- `Order Profit Per Order`
- `Order Status`
- `Product Description`
- `Product Status`

### `Order Status`

**Status:** Ambiguous — requires timing verification.

The source documentation lists workflow states such as `PENDING_PAYMENT`, `PROCESSING`, `COMPLETE`, `CANCELED`, and `PAYMENT_REVIEW`, but does not specify when the recorded status was captured relative to order creation.

Observed data shows that `CANCELED` and `SUSPECTED_FRAUD` records always have `Late_delivery_risk = 0`, while other statuses have a target distribution close to the overall dataset distribution.

This makes `Order Status` potentially informative, but not yet safe to use.

**Current decision:** Keep it excluded from model features until prediction-time availability is verified.

### Notebook-derived columns

Created only for analysis, not raw model features:

- `order_to_shipping_days`
- `calculated_late`
- `calendar_shipping_days`

`calculated_late` and `calendar_shipping_days` expose target-generation logic and must never be used as predictive features.

---

## 6. Validation Status

### Completed

- [x] Official files obtained and stored locally.
- [x] Raw files excluded from Git.
- [x] Dataset loads successfully.
- [x] Row/column counts verified.
- [x] Target definition and distribution verified.
- [x] Description-file mismatch checked.
- [x] Actual shipping-day derivation verified.
- [x] Exact target-generation rule verified.
- [x] Confirmed leakage fields identified.
- [x] Working prediction timestamp defined.
- [x] Initial feature-availability audit created.

### Pending

- [ ] Verify ambiguous fields.
- [ ] Finalize prediction timestamp.
- [ ] Complete final leakage audit.
- [ ] Check nulls, duplicates, data types, timestamps, and category cardinality.
- [ ] Identify entity/grouping keys.
- [ ] Define train/validation/test split strategy.
- [ ] Create leakage-safe processed data.
- [ ] Train the first leakage-safe baseline.

---

## 7. Storage / Reproducibility

Local ML data:

```text
data/raw/
data/interim/
data/processed/
```

PostgreSQL will later store operational application data such as:

```text
shipments
predictions
model_versions
agent_interactions
```

The repository stores code, documentation, validation logic, setup instructions, and later DVC metadata if used; it does not store the raw DataCo dataset.

---

## 8. Next Steps

1. Verify the ambiguous fields against the source description and business timing.
2. Finalize the prediction timestamp.
3. Complete the leakage audit.
4. Run data-quality checks.
5. Define grouping keys and train/validation/test split strategy.

EDA and baseline modeling start after these checks are sufficiently complete.
