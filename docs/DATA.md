# Data Documentation

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
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

The repository stores code, documentation, validation logic, setup instructions, and later DVC metadata if used; it does not store the raw DataCo dataset.
---

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
  - **KEEP**
  - Strong observed association with `Late_delivery_risk`.
  - Retained as the shipping-service representation.
  - `Days for shipment (scheduled)` is dropped because it is deterministically redundant with `Shipping Mode`.

- `Order Region`
  - More granular geographic feature than `Market`.
  - Weak standalone association, but may still contribute in combination with other features.

- `order_month`
  - Weak and inconsistent standalone association.
  - Retain as a secondary temporal candidate.

- `order_dayofweek`
  - Weak standalone association.
  - Retain as a secondary temporal candidate.

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

- `Category Id`
  - **KEEP**
  - Retained as the categorical category-code representation.
  - Data-quality review showed that `Category Name` is not semantically reliable for all categories.
  - Must be treated as categorical, not numeric/ordinal.

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

- `Category Name`
  - **DROP**
  - Data-quality review found inconsistent semantic labeling.
  - `Category Id = 13` and `Category Id = 37` are both labeled `Electronics`, despite representing different departments and product groups.
  - Dropped to avoid collapsing distinct category groups into the same unreliable label.

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

- `Market`
  - ***DROP*** 
  — coarser geographic representation than `Order Region`.


### INVESTIGATE — reviewed but not finalized

- `order_hour` *(engineered from `order date (DateOrders)`)*
  - **INVESTIGATE / MODEL EXPERIMENT**
  - Available at prediction time.
  - Shows useful target association.
  - Part of its signal is driven by the `Same Day` calendar-boundary rule.
  - Will be created during feature engineering and evaluated with an ablation test (model with vs. without `order_hour`).


## 9. Data Quality Audit

The raw dataset was audited before preprocessing to identify missing values, duplicate records, structural inconsistencies, invalid values, datatype issues, and other data-quality problems.

The raw data remains unchanged during the audit. Cleaning decisions are documented first and applied later when creating the processed modeling dataset.

### 9.1 Missing Values

Initial missing-value review found:

- `Product Description`: 100% missing → already excluded.
- `Order Zipcode`: 86.24% missing → already excluded.
- `Customer Zipcode`: 3 missing values → no modeling action required because the feature is excluded.
- `Customer Lname`: 8 missing values → no modeling action required because the feature is excluded.

No other raw columns contain recorded missing values.

Note: `Customer State` currently reports no missing values in the raw dataset, but 3 previously identified ZIP-like invalid values (`91732`, `95758`) will be converted to missing during preprocessing.

### 9.2 Duplicate Rows and Order Structure

- No exact duplicate rows were found.
- The dataset contains 65,752 unique `Order Id` values across 180,519 rows.
- Orders contain between 1 and 5 rows/items, with an average of approximately 2.75 rows per order.
- 45,902 orders contain more than one row/item.
- `Late_delivery_risk` is fully consistent within each `Order Id`.

**Implication:**  
The dataset is item-level, while the target is order-level. Train/validation/test splitting must prevent rows from the same `Order Id` from appearing in multiple splits.

### 9.3 Category Mapping Consistency

`Category Id` maps consistently to a single `Category Name`, but the relationship is not strictly one-to-one.

**Final decision:** Retain `Category Id` as a categorical code and drop `Category Name`.

`Category Name` is not semantically reliable because `Category Id = 13` and `Category Id = 37` are both labeled `Electronics` despite representing different departments and product groups.

### 9.4 Numeric Value Validation

- `Order Item Discount`
  - No missing or negative values.
  - Discount never exceeds `Sales`.
  - High values were checked and were consistent with the corresponding sales amount and discount rate.
  - No confirmed invalid outliers were found.

- `Order Item Quantity`
  - No missing values.
  - Valid observed range: 1–5.
  - No suspicious values were found.


## Raw Feature Action List

### KEEP / RETAIN

1. `Type`: **KEEP** — categorical; use in baseline.

2. `Category Id`: **KEEP** — categorical code; do not treat as continuous numeric.

3. `Customer Segment`: **KEEP** — low-cardinality categorical feature.

4. `Customer State`: **KEEP + CLEAN** — main customer geography feature; convert 3 invalid ZIP-like values to missing.

5. `Department Name`: **KEEP** — human-readable department representation.

6. `Order Country`: **KEEP** — destination-country categorical feature.

7. `Order Item Discount`: **KEEP** — primary discount representation.

8. `Order Item Quantity`: **KEEP** — low-cardinality order-time feature.

9. `Order Region`: **KEEP** — lower-cardinality geographic representation.

10. `Product Name`: **KEEP** — categorical product representation.

11. `Shipping Mode`: **KEEP** — main shipping-service representation; strong target association.

12. `Customer Id`: **RETAIN TECHNICALLY / DROP FROM MODEL** — use only for grouping and split checks.

13. `Order Id`: **RETAIN TECHNICALLY / DROP FROM MODEL** — required for order-level grouping and leakage-safe splitting.

14. `order date (DateOrders)`: **RETAIN FOR FEATURE ENGINEERING / DROP AS RAW MODEL FEATURE** — source for time features such as hour, day-of-week, and month.

15. `Late_delivery_risk`: **TARGET** — prediction label only; never use as model input.


### DROP

16. `Days for shipping (real)`: **DROP** — future information / target leakage.

17. `Days for shipment (scheduled)`: **DROP** — redundant with `Shipping Mode`.

18. `Benefit per order`: **DROP** — exact duplicate of `Order Profit Per Order`; timing uncertain and low priority.

19. `Sales per customer`: **DROP** — exact duplicate of `Order Item Total`.

20. `Delivery Status`: **DROP** — future information and part of target-generation logic.

21. `Category Name`: **DROP** — unreliable semantic labels; distinct category IDs can share the incorrect label `Electronics`.

22. `Customer City`: **DROP** — high-cardinality customer geography; use `Customer State` instead.

23. `Customer Country`: **DROP** — only two values with little useful variation.

24. `Customer Email`: **DROP** — identity/privacy; no modeling value.

25. `Customer Fname`: **DROP** — identity/privacy.

26. `Customer Lname`: **DROP** — identity/privacy; also contains 8 missing values.

27. `Customer Password`: **DROP** — sensitive identity field; no modeling value.

28. `Customer Street`: **DROP** — identity/privacy and high cardinality.

29. `Customer Zipcode`: **DROP** — high-cardinality customer geography; 3 missing values.

30. `Department Id`: **DROP** — redundant code; use `Department Name`.

31. `Latitude`: **DROP** — customer-location coordinates; high cardinality and redundant with customer geography.

32. `Longitude`: **DROP** — customer-location coordinates; high cardinality and redundant with customer geography.

33. `Market`: **DROP** — coarser geographic representation than `Order Region`.

34. `Order City`: **DROP** — very high cardinality (`3,597`).

35. `Order Customer Id`: **DROP** — exact duplicate of `Customer Id`.

36. `Order Item Cardprod Id`: **DROP** — exact duplicate of `Product Card Id`.

37. `Order Item Discount Rate`: **DROP** — approximately derived from `Order Item Discount / Sales`.

38. `Order Item Id`: **DROP** — unique row identifier.

39. `Order Item Product Price`: **DROP** — exact duplicate of `Product Price`.

40. `Order Item Profit Ratio`: **DROP** — redundant profit-family feature with very weak target association.

41. `Sales`: **DROP** — derived from item price × quantity.

42. `Order Item Total`: **DROP** — derived from `Sales - Order Item Discount`.

43. `Order Profit Per Order`: **DROP** — exact duplicate of `Benefit per order`; timing uncertain and low priority.

44. `Order State`: **DROP** — high cardinality and many rare categories.

45. `Order Status`: **DROP** — prediction-time availability not verified; possible post-order information.

46. `Order Zipcode`: **DROP** — 86.24% missing.

47. `Product Card Id`: **DROP** — identifier representation; use `Product Name`.

48. `Product Category Id`: **DROP** — exact duplicate of `Category Id`.

49. `Product Description`: **DROP** — 100% missing.

50. `Product Image`: **DROP** — image/URL metadata; no baseline modeling value.

51. `Product Price`: **DROP** — redundant with product identity and exact duplicate of `Order Item Product Price`.

52. `Product Status`: **DROP** — constant column.

53. `shipping date (DateOrders)`: **DROP** — future information / leakage.


## retained / technical / target features a

1. `Type`: **KEEP** — no missing values; 4 categories; treat as categorical.
2. `Category Id`: **KEEP** — no missing; 51 categories; treat as categorical code.
3. `Customer Segment`: **KEEP** — no missing; 3 categories; treat as categorical.
4. `Customer State`: KEEP + CLEAN — 3 invalid ZIP-like values; treat as categorical.
5. `Department Name`: **KEEP** — no missing; 11 categories; treat as categorical.
6. `Order Country`: **KEEP + GROUP RARE CATEGORIES** — no missing; 164 categories; several very rare countries; treat as categorical and group infrequent values into `Other`.
7. `Order Item Discount`: **KEEP** — no missing or negative values; high values are valid and consistent with `Sales` and `Discount Rate`; numeric feature.
8. `Order Item Quantity`: **KEEP** — no missing; valid range 1–5; no suspicious values.
9. `Order Region`: **KEEP** — no missing; 23 categories; no problematic rare categories.
10. `Product Name`: **KEEP + GROUP RARE CATEGORIES** — no missing; 118 categories; several products have very low counts, so rare products should be grouped into `Other`.
11. `Shipping Mode`: **KEEP** — no missing; 4 categories; strong target association; use as categorical.
12. `Customer Id`: **RETAIN TECHNICALLY / DROP FROM MODEL** — no missing; customer identifier; use only for grouping and split-leakage checks.
13. `Order Id`: **RETAIN TECHNICALLY / DROP FROM MODEL** — no missing; order identifier; use for order-level grouping and leakage-safe splitting.
14. `order date (DateOrders)`: **RETAIN FOR FEATURE ENGINEERING / DROP AS RAW MODEL FEATURE** — no missing; parsed correctly as datetime; use for temporal features and time-based split.
15. `Late_delivery_risk`: **TARGET** — no missing; binary label (0/1); never use as model input.



## Customer-level entity structure + split leakage check

### Customer-Level Structure

- 20,652 unique customers.
- 11,768 customers placed more than one order.
- Customers have between 1 and 15 orders, with an average of 3.18 orders per customer.

**Implication:**  
If splitting only by `Order Id`, the same customer may appear in both train and test sets. This is not direct target leakage, but it can make evaluation slightly optimistic because customer-related patterns may appear in both splits.

The final split strategy should compare:
- order-level grouped splitting
- time-based splitting
- customer overlap between splits

**Temporal consideration:**  
Because customer behavior, products, and operational patterns may change over time, a time-based split will be considered to test how well the model generalizes from past data to future orders.

### Rare-Category Handling

- `Order Country`: group categories with fewer than 50 training rows into `Other`.
  - 52 rare countries
  - 930 affected rows (0.52%)

- `Product Name`: group categories with fewer than 50 training rows into `Other`.
  - 13 rare products
  - 343 affected rows (0.19%)

Rare-category thresholds must be learned from the training split only and then applied unchanged to validation/test data.

### Order–Customer Consistency

- Every `Order Id` is linked to exactly one `Customer Id`.
- No order is associated with multiple customers.

**Implication:**  
Order-level grouping is structurally valid. Customer overlap across different orders can still occur and should be considered during split design.


### Final Cleaning Decisions

- `Customer State`
  - Replace invalid ZIP-like values (`91732`, `95758`) with missing/unknown.

- `Order Country`
  - Group categories with fewer than 50 training rows into `Other`.

- `Product Name`
  - Group categories with fewer than 50 training rows into `Other`.

- `Category Id`
  - Keep as categorical code; do not treat as continuous numeric.

- `order date (DateOrders)`
  - Parse as datetime.
  - Retain only for temporal feature engineering and split design.

- `Customer Id`
  - Retain only for grouping / split-leakage checks.

- `Order Id`
  - Retain only for order-level grouping / leakage-safe splitting.

- `Late_delivery_risk`
  - Keep as target only.

- Drop all features previously marked `DROP` before modeling.