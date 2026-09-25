# Data Documentation

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Purpose:** Keep verified dataset facts, prediction-time assumptions, leakage decisions, data-quality findings, and final feature decisions in one concise source of truth.

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

### Temporal coverage

Order data spans from `2015-01-01 00:00:00` to `2018-01-31 23:38:00`.

Coverage is not uniform:
- 2015 and 2016 contain all 12 months.
- 2017 contains fewer records in October–December.
- 2018 contains only January.

Therefore, aggregate monthly order counts should not be interpreted directly as evidence of seasonality or demand trends.

### Description-file mismatch

The dataset has 53 columns while the description file documents 52 fields.

Verified mismatch:

```text
Dataset:     shipping date (DateOrders)
Description: Shipping date (DateOrders)
```

This is only a case difference.

`Order Zipcode` exists in the dataset but has no matching documented field in the description file.

---

## 3. Verified Timeline and Target Logic

### Actual shipping days

Across all 180,519 rows:

```text
Days for shipping (real)
=
calendar-day difference between
order date (DateOrders)
and
shipping date (DateOrders)
```

### Target-generation rule

Across all 180,519 rows, `Late_delivery_risk` is exactly reproduced by:

```text
Late_delivery_risk = 1
if:
Days for shipping (real) > Days for shipment (scheduled)
and
Delivery Status != "Shipping canceled"
```

For canceled shipments, the target remains `0`.

### Target interpretation

`Late_delivery_risk` represents delay between order creation and shipping, not delay until final customer delivery.

```text
Order creation
    ↓
Pre-shipment / fulfillment process
    ↓
Shipping date
```

The label therefore measures order-to-shipping delay against the scheduled duration.

---

## 4. Prediction-Time Contract

> Predict late-delivery risk at **order creation time**, before the actual shipping date and realized shipping duration are known.

A model feature is valid only if it would genuinely be available at that moment.

---

## 5. Leakage and Special Feature Findings

### Confirmed future information / target leakage

Never use as model inputs:

- `Days for shipping (real)`
- `Delivery Status`
- `shipping date (DateOrders)`
- `Late_delivery_risk` — target only

### Shipping Mode vs. scheduled days

`Shipping Mode` and `Days for shipment (scheduled)` are deterministically mapped across all 180,519 rows:

- `Same Day` ↔ 0 days
- `First Class` ↔ 1 day
- `Second Class` ↔ 2 days
- `Standard Class` ↔ 4 days

**Final decision:** keep `Shipping Mode` and drop `Days for shipment (scheduled)`.

Observed late-delivery rates by shipping mode:

- First Class: 95.3%
- Second Class: 76.6%
- Same Day: 45.7%
- Standard Class: 38.1%

### Order-hour target artifact

For all 9,737 `Same Day` rows, exact elapsed order-to-shipping time is 12 hours.

Because `Days for shipping (real)` uses calendar-day difference:
- orders placed at hours `00–11` stay on the same calendar day;
- orders placed at hours `12–23` cross midnight.

This creates a near-deterministic relationship between `order_hour` and the target for Same Day orders.

`order_hour` is not classic future-information leakage because it is available at order creation, but part of its signal is caused by the target-generation rule.

**Decision:** `order_hour` remains an engineered feature to evaluate later with an ablation test.

### Order Status

`Order Status` timing relative to order creation cannot be verified. Workflow states may contain post-order information, and `CANCELED` / `SUSPECTED_FRAUD` rows show target-proximity concerns.

**Final decision:** DROP.

### Notebook-derived analysis columns

Never use as raw model features:

- `order_to_shipping_days`
- `calculated_late`
- `calendar_shipping_days`

---

## 6. Verified Redundancy and Mapping Findings

### Financial redundancy

Verified across all 180,519 rows:

```text
Sales ≈ Order Item Product Price × Order Item Quantity
Order Item Total ≈ Sales - Order Item Discount
Benefit per order = Order Profit Per Order
Sales per customer = Order Item Total
```

Additional verified relationships:
- `Order Item Product Price` = `Product Price`
- `Order Item Discount Rate` is approximately derived from `Order Item Discount / Sales` in 179,834 of 180,519 rows (~99.62%).
- `Order Item Profit Ratio` is strongly correlated with profit fields and has very weak standalone target association.

### Identifier / code redundancy

Verified exact mappings:

- `Customer Id` = `Order Customer Id`
- `Category Id` = `Product Category Id`
- `Product Card Id` = `Order Item Cardprod Id`
- `Department Id` maps one-to-one to `Department Name`
- `Product Card Id` maps one-to-one to `Product Name`
- each `Product Name` maps to one `Product Price`

### Category-label inconsistency

`Category Id` maps to one `Category Name`, but the reverse mapping is not one-to-one.

`Category Id = 13` and `Category Id = 37` are both labeled `Electronics`, despite representing different departments and product groups.

**Final decision:** keep `Category Id` as a categorical code and drop `Category Name`.

---

## 7. Data Quality Audit

The raw dataset was audited before preprocessing. Raw data remains unchanged; cleaning decisions are applied later in the processed dataset.

### Missing values

- `Product Description`: 100% missing → DROP
- `Order Zipcode`: 86.24% missing → DROP
- `Customer Zipcode`: 3 missing values → already DROP
- `Customer Lname`: 8 missing values → already DROP
- No other raw columns contain recorded missing values.

`Customer State` has no recorded missing values, but 3 ZIP-like invalid values (`91732`, `95758`) will be converted to missing/unknown during preprocessing.

### Duplicate rows and order structure

- No exact duplicate rows.
- 65,752 unique `Order Id` values across 180,519 rows.
- Orders contain 1–5 rows/items.
- Average ≈ 2.75 rows/items per order.
- 45,902 orders contain more than one row/item.
- `Late_delivery_risk` is fully consistent within each `Order Id`.

**Implication:** the dataset is item-level while the target is order-level. Rows from the same `Order Id` must not be split across train/validation/test.

### Customer structure

- 20,652 unique customers.
- 11,768 customers placed more than one order.
- 1–15 orders per customer.
- Average ≈ 3.18 orders per customer.
- Every `Order Id` belongs to exactly one `Customer Id`.

Customer overlap across splits may still occur and should be measured during split design.

### Numeric value validation

`Order Item Discount`:
- no missing or negative values;
- never exceeds `Sales`;
- high values were checked and are consistent with sales amount and discount rate;
- no confirmed invalid outliers.

`Order Item Quantity`:
- no missing values;
- valid observed range: 1–5;
- no suspicious values found.

### Rare categories

Exploratory full-dataset counts using threshold `< 50` rows:

- `Order Country`: 52 rare countries, 930 rows (0.52%)
- `Product Name`: 13 rare products, 343 rows (0.19%)

The actual rare-category mapping must be learned from the training split only and then applied unchanged to validation/test data.

---

## 8. Raw Feature Action List

### KEEP / RETAIN

1. `Type` — **KEEP** — categorical; 4 categories.
2. `Category Id` — **KEEP** — categorical code; do not treat as numeric/ordinal.
3. `Customer Segment` — **KEEP** — categorical; 3 categories.
4. `Customer State` — **KEEP + CLEAN** — convert invalid ZIP-like values to missing/unknown.
5. `Department Name` — **KEEP** — categorical; 11 categories.
6. `Order Country` — **KEEP + GROUP RARE** — categorical; 164 categories.
7. `Order Item Discount` — **KEEP** — numeric.
8. `Order Item Quantity` — **KEEP** — valid range 1–5.
9. `Order Region` — **KEEP** — categorical; 23 categories.
10. `Product Name` — **KEEP + GROUP RARE** — categorical; 118 categories.
11. `Shipping Mode` — **KEEP** — categorical; 4 categories.
12. `Customer Id` — **RETAIN TECHNICALLY / DROP FROM MODEL** — grouping and split checks only.
13. `Order Id` — **RETAIN TECHNICALLY / DROP FROM MODEL** — order-level grouping and leakage-safe split.
14. `order date (DateOrders)` — **RETAIN FOR FEATURE ENGINEERING / DROP AS RAW MODEL FEATURE** — parse as datetime; use for temporal features and split design.
15. `Late_delivery_risk` — **TARGET ONLY**.

### DROP

16. `Days for shipping (real)` — future information / target leakage.
17. `Days for shipment (scheduled)` — redundant with `Shipping Mode`.
18. `Benefit per order` — duplicate of `Order Profit Per Order`; timing uncertain.
19. `Sales per customer` — duplicate of `Order Item Total`.
20. `Delivery Status` — future information / target-generation logic.
21. `Category Name` — unreliable semantic labeling.
22. `Customer City` — high-cardinality; use `Customer State`.
23. `Customer Country` — only two categories with little useful variation.
24. `Customer Email` — identity/privacy; no modeling value.
25. `Customer Fname` — identity/privacy.
26. `Customer Lname` — identity/privacy; 8 missing.
27. `Customer Password` — sensitive identity field.
28. `Customer Street` — identity/privacy; high cardinality.
29. `Customer Zipcode` — high cardinality; 3 missing.
30. `Department Id` — redundant with `Department Name`.
31. `Latitude` — high-cardinality customer-location coordinate; redundant.
32. `Longitude` — high-cardinality customer-location coordinate; redundant.
33. `Market` — coarser than `Order Region`.
34. `Order City` — very high cardinality.
35. `Order Customer Id` — duplicate of `Customer Id`.
36. `Order Item Cardprod Id` — duplicate of `Product Card Id`.
37. `Order Item Discount Rate` — approximately derived.
38. `Order Item Id` — unique row identifier.
39. `Order Item Product Price` — duplicate of `Product Price`.
40. `Order Item Profit Ratio` — redundant profit feature; weak target association.
41. `Sales` — derived from price × quantity.
42. `Order Item Total` — derived from sales − discount.
43. `Order Profit Per Order` — duplicate of `Benefit per order`; timing uncertain.
44. `Order State` — high cardinality; many rare categories.
45. `Order Status` — timing not verified; possible post-order information.
46. `Order Zipcode` — 86.24% missing.
47. `Product Card Id` — identifier; use `Product Name`.
48. `Product Category Id` — duplicate of `Category Id`.
49. `Product Description` — 100% missing.
50. `Product Image` — metadata; no baseline modeling value.
51. `Product Price` — redundant with product identity; duplicate of item price.
52. `Product Status` — constant.
53. `shipping date (DateOrders)` — future information / leakage.

---

## 9. Final Cleaning Decisions

- Parse `order date (DateOrders)` as datetime.
- Replace invalid ZIP-like values (`91732`, `95758`) with `CA`, based on the verified `Customer Zipcode → Customer State` mapping.
- Treat `Category Id` as categorical.
- Group rare `Order Country` values into `Other` using a threshold learned from the training split only.
- Group rare `Product Name` values into `Other` using a threshold learned from the training split only.
- Retain `Customer Id` and `Order Id` only for grouping and split checks.
- Keep `Late_delivery_risk` as target only.
- Drop all features marked `DROP` before modeling.
- Keep the raw dataset unchanged; apply these actions when creating the cleaned/processed dataset.



# Order-Level Aggregation

The raw DataCo dataset is item-level: a single `Order Id` may appear across multiple rows because one order can contain multiple items.

During validation, the following structure was confirmed:

- 180,519 item-level rows.
- 65,752 unique `Order Id` values.
- All rows belonging to the same `Order Id` have:
  - the same `order date (DateOrders)`,
  - the same `shipping date (DateOrders)`,
  - the same `Late_delivery_risk`,
  - the same `Customer Id`.

Because the prediction target is constant within each order, the modeling unit was changed from item-level rows to one row per order.

### Within-Order Feature Consistency

The retained features were checked to determine whether their values remain constant within an `Order Id`.

The following features were fully consistent within each order:

- `Type`
- `Customer Segment`
- `Customer State`
- `Order Country`
- `Order Region`
- `Shipping Mode`
- `Customer Id`
- `order date (DateOrders)`
- `Late_delivery_risk`

These features can therefore be retained with the first observed value during order-level aggregation.

The following retained features vary across items within the same order:

- `Order Item Discount`
- `Product Name`
- `Category Id`
- `Department Name`
- `Order Item Quantity`

Observed orders containing more than one value for each item-level feature:

- `Order Item Discount`: 45,780 orders
- `Product Name`: 44,578 orders
- `Category Id`: 44,563 orders
- `Department Name`: 41,471 orders
- `Order Item Quantity`: 38,816 orders

Because these features are item-level, selecting only the first value would discard information from the remaining items. They were therefore aggregated into order-level summary features.

### Aggregation Rules

The following aggregation rules were applied:

- `Order Item Quantity` → `total_quantity`
  - Sum of item quantities within each order.

- `Order Item Discount` → `total_discount`
  - Sum of item discounts within each order.

- `Product Name` → `num_unique_products`
  - Number of unique products within each order.

- `Category Id` → `num_unique_categories`
  - Number of unique product categories within each order.

- `Department Name` → `num_unique_departments`
  - Number of unique departments represented within each order.

For features that are constant within an order, the first value was retained:

- `Type`
- `Customer Segment`
- `Customer State`
- `Order Country`
- `Order Region`
- `Shipping Mode`
- `Customer Id`
- `order date (DateOrders)`
- `Late_delivery_risk`

`Order Id` remains the grouping key and technical identifier.

### Resulting Order-Level Dataset

After aggregation:

- Rows: 65,752
- Unique `Order Id`: 65,752
- Columns: 15
- Missing values in retained columns: 0

Target distribution:

- `Late_delivery_risk = 1`: 54.82%
- `Late_delivery_risk = 0`: 45.18%

Aggregated feature ranges:

- `total_quantity`: 1–24
- `num_unique_products`: 1–5
- `num_unique_categories`: 1–5
- `num_unique_departments`: 1–5

### Modeling Implication

The order-level representation prevents multi-item orders from being counted multiple times during model training.

Without aggregation, an order containing five items would contribute five training rows while a single-item order would contribute only one row, even though the target is defined at the order level.

The aggregated dataset therefore aligns the modeling unit with the target unit: one row per order and one late-delivery label per order.


### Interim Dataset

The cleaned, order-level dataset is saved as:

`data/interim/order_level_clean.csv`

This file contains the post-cleaning, pre-split dataset and is used as the input for train/validation/test splitting.


## Train / Validation / Test Split

A chronological 70/15/15 split was used on the order-level dataset.

- Train: 46,026 orders
  - 2015-01-01 → 2017-03-16
  - Late rate: 54.85%

- Validation: 9,863 orders
  - 2017-03-16 → 2017-09-05
  - Late rate: 54.50%

- Test: 9,863 orders
  - 2017-09-05 → 2018-01-31
  - Late rate: 55.05%

The split preserves chronological order so the model is trained on past orders and evaluated on later orders.

Split files are saved under:

`data/interim/splits/`





## Model Preprocessing

Preprocessing is learned from the training split only and then applied unchanged to validation and test data.

### Rare-Category Handling

- `Order Country` categories with fewer than 50 training observations are mapped to `Other`.
- The frequent-category list is derived only from the training data.
- Unseen countries in validation/test are also mapped to `Other`.

### Feature Encoding

Categorical features are encoded using:

`OneHotEncoder(handle_unknown="ignore")`

Categorical features:

- `Type`
- `Customer Segment`
- `Customer State`
- `Order Country`
- `Order Region`
- `Shipping Mode`

Numeric features are standardized using `StandardScaler`.

Numeric features:

- `total_quantity`
- `total_discount`
- `num_unique_products`
- `num_unique_categories`
- `num_unique_departments`
- `order_hour`
- `order_dayofweek`
- `order_month`

The fitted preprocessing transformer produces 168 model-ready features.




## Baseline Model Comparison

Two baseline classifiers have been evaluated on the validation set using the same preprocessed feature matrix.

### Logistic Regression

Validation performance:

- Accuracy: `0.701`
- Precision: `0.836`
- Recall: `0.561`
- F1-score: `0.671`
- ROC-AUC: `0.743`

The model provides strong precision, but misses a substantial number of actual late orders.
