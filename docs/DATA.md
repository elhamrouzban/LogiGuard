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

**Temporal coverage:**  
Order data spans from `2015-01-01 00:00:00` to `2018-01-31 23:38:00`.

Coverage is not uniform across all years:
- 2015 and 2016 include all 12 months.
- 2017 contains fewer records in October–December.
- 2018 contains only January.

Therefore, aggregate monthly order counts are affected by incomplete temporal coverage and should not be interpreted directly as evidence of seasonality or demand trends.


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

### Target Interpretation

`Late_delivery_risk` represents a delay between order creation and shipment, not a delay between order creation and final customer delivery.

Verified timeline:

```text
Order creation
    ↓
Pre-shipment / fulfillment process
    ↓
Shipping date

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

**Shipping Mode — observed predictive signal:**  
Late-delivery rates differ substantially across shipping modes:

- First Class: 95.3%
- Second Class: 76.6%
- Same Day: 45.7%
- Standard Class: 38.1%

This indicates that `Shipping Mode` has strong observed association with `Late_delivery_risk`.

**Current decision:** Retain `Shipping Mode` as a candidate model feature, provided its availability at order creation remains valid under the prediction-time contract.

**Shipping Mode / Scheduled Days redundancy:**  
`Shipping Mode` and `Days for shipment (scheduled)` are deterministically mapped across all 180,519 rows:

- `Same Day` ↔ 0 scheduled days
- `First Class` ↔ 1 scheduled day
- `Second Class` ↔ 2 scheduled days
- `Standard Class` ↔ 4 scheduled days

Therefore, these two columns encode the same scheduling information.

**Order-hour / Same Day target artifact:**  
`order_hour`, derived from `order date (DateOrders)`, shows a strong relationship with `Late_delivery_risk` for `Same Day` orders.

For all 9,737 `Same Day` orders, the exact elapsed time between order creation and shipping is exactly 12 hours.

Because `Days for shipping (real)` is based on calendar-date difference rather than exact elapsed hours:

- orders placed during hours `00–11` remain on the same calendar day and have `Days for shipping (real) = 0`
- orders placed during hours `12–23` cross midnight and have `Days for shipping (real) = 1`

Since `Same Day` maps to `Days for shipment (scheduled) = 0`, this creates a near-deterministic relationship between `order_hour` and the target for Same Day orders.

This is not classic future-information leakage because `order_hour` is available at order creation. However, it reflects a target-generation artifact based on calendar-day boundaries.

**Current decision:** Keep `order_hour` under evaluation and compare model performance with and without it. If retained, document that part of its predictive power comes from this target-definition rule.

**Current decision:** Do not use both simultaneously as independent model features. The final retained representation will be selected during feature engineering.

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

### Financial Feature Redundancy

Verified relationships across all 180,519 rows:

```text
Sales ≈ Order Item Product Price × Order Item Quantity

Order Item Total ≈ Sales - Order Item Discount

Benefit per order = Order Profit Per Order
```

These relationships indicate that several financial fields are derived or redundant rather than independent features.

**Current decision:** Treat these variables as secondary features for delay prediction. Avoid including multiple mathematically overlapping financial fields unless later EDA/modeling shows clear predictive value.

**Important:** This is a redundancy issue, not confirmed target leakage.

**Market / Order Region — observed target association:**  
`Market` shows very little variation in late-delivery rate across categories, with all markets close to the overall target rate.

`Order Region` shows somewhat more variation, but most regions still have similar late-delivery rates.

**Current interpretation:** Geography may provide limited standalone predictive signal, although it may still become useful in combination with other features.

**Category Name — observed target association:**  
`Category Name` contains 51 categories with a highly uneven frequency distribution.

Some categories show noticeably higher or lower late-delivery rates, but the largest categories remain close to the overall dataset rate. The most extreme rates are mostly associated with small sample sizes.

**Current interpretation:** `Category Name` shows weak standalone association with `Late_delivery_risk`. It may still be useful in combination with other features, but it is not currently considered a strong individual predictor.

**Order month — temporal association:**  
Monthly late-delivery rates remain relatively stable across years, generally around the overall dataset rate.

Some month-to-month variation exists, but no strong or consistent seasonal pattern is observed across years.

**Current interpretation:** `order_month` shows weak standalone association with `Late_delivery_risk` and may still be retained as a secondary temporal feature.






## Feature Decision Registry

### KEEP — approved / retained as candidates

- `Shipping Mode`
  - Strong observed association with `Late_delivery_risk`.
  - Available at order time, subject to final prediction-time validation.
  - Do not use simultaneously with `Days for shipment (scheduled)` because they encode the same scheduling information.

- `Days for shipment (scheduled)`
  - Available at order time.
  - Deterministically mapped to `Shipping Mode`.
  - Retain only one of these two representations in the final feature set.

- `Market`
  - Available at order time.
  - Weak standalone association, but may still contribute in combination with other features.

- `Order Region`
  - More granular geographic feature than `Market`.
  - Weak standalone association, but may still contribute in combination with other features.

- `Category Name`
  - **KEEP**
  - Human-readable category representation.
  - Each `Category Id` maps to exactly one `Category Name`.
  - `Category Name` is not strictly one-to-one with `Category Id` because `Electronics` is associated with two category IDs (`13` and `37`).

- `order_month`
  - Weak and inconsistent standalone association.
  - Retain as a secondary temporal candidate.

- `order_dayofweek`
  - Weak standalone association.
  - Retain as a secondary temporal candidate.

- `Category Name`
  - Human-readable representation of the product category.
  - `Category Id` maps one-to-one to `Category Name`, so only one representation is needed.

- `Product Name`
  - Human-readable representation of the product.
  - `Product Card Id` maps one-to-one to `Product Name`, so only one representation is needed.
  - Final usefulness will be evaluated during modeling because it has 118 unique categories.

- `Product Name`
  - **KEEP**
  - More granular product representation.
  - Each `Product Name` maps to exactly one `Product Price`.
  - Retained because `Product Price` alone cannot uniquely identify the product.

- `Type`
  - **KEEP**
  - Low-cardinality categorical feature with 4 values.
  - Shows some variation in late-shipment rate, particularly for `TRANSFER`.
  - Retained as a candidate order-time feature.

- `Customer Segment`
  - **KEEP**
  - Low-cardinality categorical feature with 3 values.
  - Shows very weak standalone association with `Late_delivery_risk`.
  - Retained because it is inexpensive to encode and may still contribute through interactions.

- `Customer State`
  - **KEEP**
  - Retained as the main customer-location feature.
  - Only 3 rows contain invalid ZIP-like values (`91732`, `95758`); these will be treated as missing during preprocessing.

- `Order Country`
  - **KEEP**
  - Destination-country feature with moderate cardinality (`164` values).
  - May capture routing or geographic differences relevant to fulfillment.
  - Retained as the main detailed order-destination feature.

- `Order Item Quantity`
  - **KEEP**
  - Low-cardinality order-time feature with 5 well-supported values.
  - Shows little standalone relationship with `Late_delivery_risk`, but is inexpensive to retain and may contribute through feature interactions.

- `Order Item Quantity`
  - **KEEP**
  - Low-cardinality order-time feature with 5 well-supported values.
  - Shows little standalone relationship with `Late_delivery_risk`, but is inexpensive to retain and may contribute through feature interactions.


### DROP — excluded

- `Days for shipping (real)`
  - Future information / target leakage.

- `Delivery Status`
  - Future information and directly involved in target-generation logic.

- `shipping date (DateOrders)`
  - Future information.

- `Late_delivery_risk`
  - Target.

- `Product Description`
  - 100% missing.

- `Product Status`
  - Constant value.

- `Customer Email`
- `Customer Fname`
- `Customer Lname`
- `Customer Password`
- `Customer Street`
- `Product Image`
  - Identity/privacy/low modeling value.

- `Order Profit Per Order`
  - **DROP**
  - Exact duplicate of `Benefit per order`.
  - Prediction-time availability is not verified.
  - Shows essentially no standalone linear association with `Late_delivery_risk` (`r ≈ -0.004`).
  - Low priority for the late-shipment prediction problem.

- `Benefit per order`
  - **DROP**
  - Exact duplicate of `Order Profit Per Order`.
  - Excluded for the same reasons.

- `Latitude`
- `Longitude`
  - Customer-location coordinates.
  - Not directly aligned with the order-to-shipping target.
  - High-cardinality and largely redundant with customer geography fields.
  - Excluded from the baseline feature set.

- `Sales per customer`
  - **DROP**
  - Exact duplicate of `Order Item Total` across all 180,519 rows.
  - Adds no independent information.

- `Order Item Profit Ratio`
  - **DROP**
  - Strongly correlated with the other profit-related fields (`r ≈ 0.824`).
  - Shows essentially no standalone linear association with `Late_delivery_risk` (`r ≈ -0.002`).
  - Low priority for the late-shipment prediction problem and excluded from the baseline feature set.

- `Order Status`
  - **DROP**
  - Prediction-time availability cannot be verified.
  - The field contains workflow states that may represent post-order information.
  - `CANCELED` and `SUSPECTED_FRAUD` records have `Late_delivery_risk = 0` for all observed rows, increasing target-proximity concerns.
  - Excluded from the baseline feature set to avoid potential post-order information leakage.

- `Order Item Id`
  - **DROP**
  - Unique for every row (`180,519` unique values).
  - Pure row-level identifier with no expected predictive value.

- `Order Id`
  - **DROP as model feature**
  - Order identifier, not a meaningful predictive feature.
  - Retain only for grouping, validation, or train/test split checks.

- `Customer Id`
  - **DROP as raw model feature**
  - High-cardinality customer identifier.
  - May be retained only for grouping or split-leakage checks.

- `Order Customer Id`
  - **DROP**
  - Exact duplicate of `Customer Id` across all rows.

- `Order Zipcode`
  - **DROP**
  - `86.24%` missing values.
  - Too incomplete for the baseline feature set.

- `Product Category Id`
  - **DROP**
  - Exact duplicate of `Category Id` across all rows.

- `Order Item Cardprod Id`
  - **DROP**
  - Exact duplicate of `Product Card Id` across all rows.

- `Order Customer Id`
  - **DROP**
  - Exact duplicate of `Customer Id` across all rows.

- `Category Id`
  - **DROP**
  - Identifier-style representation of category.
  - Dropped in favor of the more interpretable `Category Name`.
  - Note: the mapping is many-to-one rather than strictly one-to-one.
  
- `Product Card Id`
  - **DROP**
  - One-to-one mapping with `Product Name`.
  - Dropped in favor of the more interpretable categorical representation.

- `Department Id`
  - **DROP**
  - One-to-one mapping with `Department Name`.
  - Dropped in favor of the more interpretable categorical representation.

- `Product Price`
  - **DROP**
  - Deterministically derived from `Product Name`.
  - Multiple products may share the same price, so price contains less information than product identity.

- `Customer Country`
  - **DROP**
  - Only two categories with nearly identical late-shipment rates.

- `Customer City`
  - **DROP**
  - Higher-cardinality geographic representation (`563` unique values).
  - Dropped in favor of the lower-cardinality `Customer State`.

- `Customer Zipcode`
  - **DROP**
  - High-cardinality (`996` unique values) and largely redundant with customer geography.
  - Dropped in favor of `Customer State`.

- `Order State`
  - **DROP**
  - High cardinality (`1,089` values).
  - Many categories have very small sample sizes, producing unstable extreme late rates.
  - Dropped to reduce overfitting risk.

- `Order City`
  - **DROP**
  - Very high cardinality (`3,597` values).
  - Too granular for the baseline model and likely to create sparse categories and overfitting.

- `Order Item Discount Rate`
  - **DROP**
  - Approximately derived from `Order Item Discount / Sales`.
  - The rounded relationship holds for 179,834 of 180,519 rows (~99.62%).
  - Excluded to reduce redundant financial information.

- `Order Item Product Price`
  - **DROP**
  - Exact duplicate of `Product Price` across all 180,519 rows.
  - Adds no independent information.

- `Sales`
  - **DROP**
  - Exactly derived from `Order Item Product Price × Order Item Quantity`.
  - Adds no independent information.

- `Order Item Total`
  - **DROP**
  - Derived from `Sales - Order Item Discount` to cent-level precision across the dataset.
  - Redundant with retained order/item information.


### INVESTIGATE — reviewed but not finalized

- `order_hour` *(engineered from `order date (DateOrders)`)*
  - **INVESTIGATE / MODEL EXPERIMENT**
  - Available at prediction time.
  - Shows useful target association.
  - Part of its signal is driven by the `Same Day` calendar-boundary rule.
  - Will be created during feature engineering and evaluated with an ablation test (model with vs. without `order_hour`).
