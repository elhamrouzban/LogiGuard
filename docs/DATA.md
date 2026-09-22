# Data Documentation

**Project:** LogiGuard AI — AI Logistics Exception Management & Operations Copilot  
**Current stage:** Week 1 — Data Validation / Leakage Audit  
**Purpose:** Keep verified dataset facts, prediction-time assumptions, leakage decisions, feature decisions, and next data steps in one concise source of truth.

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

### Verified shape and target

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

- 2015 and 2016 contain all 12 months.
- 2017 has fewer records in October–December.
- 2018 contains only January.

Aggregate monthly counts are therefore affected by incomplete temporal coverage and should not be interpreted directly as seasonality or demand trends.

### Description-file mismatch

The dataset has 53 columns while the description file documents 52 fields.

```text
Dataset:     shipping date (DateOrders)
Description: Shipping date (DateOrders)
```

This is only a case difference.

`Order Zipcode` exists in the dataset but has no matching field in the description file. It is undocumented in the source description and is excluded from the baseline for data-quality reasons described below.

---

## 2. Verified Timeline and Target Logic

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

### Target interpretation

`Late_delivery_risk` represents a delay between **order creation and shipment**, not a delay between order creation and final customer delivery.

```text
Order creation
    ↓
Pre-shipment / fulfillment process
    ↓
Shipping date
```

The dataset does not contain a verified final-customer delivery timestamp. The label therefore measures fulfillment / pre-shipment delay against the scheduled duration and should not be interpreted as a last-mile delivery-delay label.

---

## 3. Prediction-Time Contract and Leakage Rule

### Prediction point

> Predict late-shipment risk at **order creation time**, before the actual shipping date and realized shipping duration are known.

A model feature is valid only if it would genuinely be available at that point.

### Confirmed future information or target leakage

Never use these as model inputs:

- `Days for shipping (real)` — realized future duration and direct target component.
- `Delivery Status` — post-order outcome information and direct target component.
- `shipping date (DateOrders)` — future timestamp.
- `Late_delivery_risk` — target.

`Order Status` is also excluded, but for a different reason: its snapshot timing cannot be verified and several values may represent post-order workflow states. It is treated as a potential leakage risk, not as confirmed leakage.

---

## 4. Verified Feature Findings

This section records reusable dataset facts. Final model inclusion is defined once in the **Raw Feature Decision Registry**.

### 4.1 Shipping service and target artifact

`Shipping Mode` has strong observed association with the target:

- First Class: 95.3% late
- Second Class: 76.6% late
- Same Day: 45.7% late
- Standard Class: 38.1% late

`Shipping Mode` and `Days for shipment (scheduled)` are deterministically mapped across all rows:

```text
Same Day       ↔ 0 scheduled days
First Class    ↔ 1 scheduled day
Second Class   ↔ 2 scheduled days
Standard Class ↔ 4 scheduled days
```

They encode the same scheduling information; the baseline keeps `Shipping Mode` and drops `Days for shipment (scheduled)`.

#### Same-Day / order-hour artifact

For all **9,737 Same Day** orders, exact elapsed time from order creation to shipping is exactly **12 hours**.

Because `Days for shipping (real)` uses calendar-date difference:

- order hours `00–11` + 12 hours stay on the same calendar date → real shipping days = 0
- order hours `12–23` + 12 hours cross midnight → real shipping days = 1

Since Same Day has scheduled days = 0, `order_hour` becomes nearly deterministic for the target within this shipping mode. This is **not classic future leakage** because order hour is available at prediction time, but it is a target-generation artifact. `order_hour` therefore requires an ablation test before final use.

### 4.2 Temporal features

Year-aware monthly late rates are generally close to the overall target rate and do not show a strong consistent seasonal pattern. Day-of-week association is also weak.

- `order_month`: weak / inconsistent standalone signal.
- `order_dayofweek`: weak standalone signal.
- Raw `order date (DateOrders)` is not passed directly to the model; it is retained only as the source for engineered time features and split logic.

### 4.3 Geographic hierarchy and signal

`Market` contains 5 categories and `Order Region` contains 23. Each `Order Region` belongs to exactly one `Market`, so `Market` is a coarser redundant representation. Late rates by both are mostly close to the overall target rate; `Order Region` is retained for possible interaction effects.

Customer geography:

- `Customer Country`: 2 categories with nearly identical late rates.
- `Customer State`: 46 observed values and retained as the main customer-location representation.
- `Customer City`: 563 values; too granular relative to state for the baseline.
- `Customer Zipcode`: 996 values; higher-cardinality and geographically redundant.
- Three `Customer State` rows contain ZIP-like invalid values (`91732`, `95758`); treat them as missing during preprocessing.
- `Latitude` / `Longitude` align with customer-location information in inspected records and are excluded as high-cardinality geographic detail that is not directly aligned with the order-to-shipping target.

Order destination geography:

- `Order Country`: 164 values; retained as the detailed destination feature.
- `Order State`: 1,089 values; many very small groups produce unstable 0% / 100% late rates.
- `Order City`: 3,597 values; too granular for the baseline.
- `Order Zipcode`: 86.24% missing and undocumented in the description file.

Repeated state/city names can appear under multiple countries or regions, so non-unique `State → Country` or `City → State` mappings are not by themselves evidence of corruption.

### 4.4 Product, category, and department representations

Verified mappings:

```text
Category Id       → Category Name      (one-to-one from ID to name)
Category Id       = Product Category Id (all rows)
Product Card Id   → Product Name       (one-to-one from ID to name)
Product Card Id   = Order Item Cardprod Id (all rows)
Department Id     → Department Name    (one-to-one from ID to name)
Product Name      → Product Price      (each product name has one price)
Order Item Product Price = Product Price (all rows)
```

`Product Name` has 118 values while `Product Price` has 75, so multiple products can share a price. The baseline therefore retains the more informative human-readable names and drops redundant IDs / price representations.

`Category Name` has 51 unevenly distributed categories. Extreme late rates mostly occur in small groups; standalone association is weak, but the feature is retained for possible interactions.

### 4.5 Financial redundancy

Verified relationships:

```text
Benefit per order = Order Profit Per Order                       (all rows)
Sales per customer = Order Item Total                            (all rows)
Sales = Order Item Product Price × Order Item Quantity           (all rows)
Order Item Total ≈ Sales - Order Item Discount                   (cent-level precision)
Order Item Discount Rate ≈ Order Item Discount / Sales           (after 2-decimal rounding in 179,834 / 180,519 rows; ~99.62%)
```

Additional observations:

- `Order Item Profit Ratio` correlates strongly with the profit fields (`r ≈ 0.824`) but has almost no linear association with the target (`r ≈ -0.002`).
- `Benefit per order` / `Order Profit Per Order` also show almost no linear association with the target (`r ≈ -0.004`).

These are redundancy / prioritization findings, not confirmed target leakage. The baseline keeps `Order Item Discount` and `Order Item Quantity` while excluding overlapping financial representations.

### 4.6 Order Status

The source documentation does not state when `Order Status` was captured relative to order creation. Values include workflow states such as `PENDING_PAYMENT`, `PROCESSING`, `COMPLETE`, `CANCELED`, and `PAYMENT_REVIEW`.

Observed target behavior:

- `CANCELED` rows always have target 0.
- `SUSPECTED_FRAUD` rows always have target 0.
- Other statuses are closer to the overall target distribution.

Because timing cannot be verified and the field may contain post-order information close to the target, it is excluded from the baseline.

### 4.7 Data-quality-only findings

- `Product Description`: 100% missing.
- `Product Status`: constant.
- `Order Item Id`: unique for all 180,519 rows.
- `Customer Id = Order Customer Id` across all rows.

---

## 5. Raw Feature Decision Registry

**Rule:** every one of the dataset's 53 raw columns appears exactly once below. `KEEP` means retained as a baseline candidate; `DROP` means excluded from model inputs. Some dropped identifiers remain available for grouping, validation, or split logic.

| Raw feature | Decision | Reason |
|---|---|---|
| `Type` | KEEP | Low-cardinality (4 values), available at order time, and shows some target variation; may help interactions. |
| `Days for shipping (real)` | DROP | Future realized duration and direct component of target generation. |
| `Days for shipment (scheduled)` | DROP | Deterministically equivalent to `Shipping Mode`; keep one representation only. |
| `Benefit per order` | DROP | Exact duplicate of `Order Profit Per Order`; timing unverified and negligible standalone target association. |
| `Sales per customer` | DROP | Exact duplicate of `Order Item Total`. |
| `Delivery Status` | DROP | Future/post-order information and direct target-generation component. |
| `Late_delivery_risk` | DROP | Target, never a model input. |
| `Category Id` | DROP | Redundant with `Category Name`; prefer interpretable name. |
| `Category Name` | KEEP | Human-readable category representation; 51 values; weak standalone signal but possible interaction value. |
| `Customer City` | DROP | 563 categories; more granular and sparse than retained `Customer State`. |
| `Customer Country` | DROP | Only 2 categories with nearly identical late rates. |
| `Customer Email` | DROP | Identity/privacy field with no justified modeling value. |
| `Customer Fname` | DROP | Identity/privacy field with no justified modeling value. |
| `Customer Id` | DROP | High-cardinality identifier; retain only for grouping / split-leakage checks. |
| `Customer Lname` | DROP | Identity/privacy field with no justified modeling value. |
| `Customer Password` | DROP | Sensitive identity/security field; never use for modeling. |
| `Customer Segment` | KEEP | Low-cardinality (3 values), cheap to encode, and may contribute through interactions despite weak standalone signal. |
| `Customer State` | KEEP | Main customer-location representation; moderate cardinality. Three invalid ZIP-like values will be treated as missing. |
| `Customer Street` | DROP | Identity/privacy and very granular location field. |
| `Customer Zipcode` | DROP | 996 values and largely redundant with customer geography; prefer state. |
| `Department Id` | DROP | One-to-one with `Department Name`; prefer interpretable name. |
| `Department Name` | KEEP | Human-readable department representation; avoids redundant ID encoding. |
| `Latitude` | DROP | High-cardinality customer-location detail, redundant with geography fields and not directly aligned with fulfillment-delay target. |
| `Longitude` | DROP | Same rationale as `Latitude`. |
| `Market` | DROP | Coarser hierarchy than `Order Region`; each region maps to one market. |
| `Order City` | DROP | Very high cardinality (3,597); sparse and overfitting-prone for baseline. |
| `Order Country` | KEEP | Moderate cardinality (164) and retained as detailed order-destination geography. |
| `Order Customer Id` | DROP | Exact duplicate of `Customer Id`. |
| `order date (DateOrders)` | DROP | Do not use raw timestamp directly; retain only for temporal feature engineering and split logic. |
| `Order Id` | DROP | Identifier, not a predictive feature; retain only for grouping / validation / split checks. |
| `Order Item Cardprod Id` | DROP | Exact duplicate of `Product Card Id`. |
| `Order Item Discount` | KEEP | Primary retained discount representation after dropping the near-derived discount rate. |
| `Order Item Discount Rate` | DROP | Approximately derived from discount / sales; 99.62% match after 2-decimal rounding. |
| `Order Item Id` | DROP | Unique for every row; pure row identifier. |
| `Order Item Product Price` | DROP | Exact duplicate of `Product Price`. |
| `Order Item Profit Ratio` | DROP | Overlaps profit family; `r ≈ 0.824` with profit fields and negligible target association (`r ≈ -0.002`). |
| `Order Item Quantity` | KEEP | Five well-supported values; little standalone signal but low cost and plausible interaction value. |
| `Sales` | DROP | Exactly derived from item price × quantity; no independent information. |
| `Order Item Total` | DROP | Derived from sales − discount to cent-level precision; redundant. |
| `Order Profit Per Order` | DROP | Exact duplicate of `Benefit per order`; timing unverified and negligible standalone target association. |
| `Order Region` | KEEP | 23-category geographic representation; more informative granularity than `Market` and may help interactions. |
| `Order State` | DROP | High cardinality (1,089) with many tiny groups and unstable extreme rates. |
| `Order Status` | DROP | Prediction-time timing cannot be verified; may contain post-order workflow information and target-proximate states. |
| `Order Zipcode` | DROP | 86.24% missing and undocumented in source description. |
| `Product Card Id` | DROP | Redundant with `Product Name`; prefer interpretable name. |
| `Product Category Id` | DROP | Exact duplicate of `Category Id`. |
| `Product Description` | DROP | 100% missing. |
| `Product Image` | DROP | URL/image reference with no justified baseline modeling value. |
| `Product Name` | KEEP | 118-category product representation; more informative than price because multiple products share the same price. |
| `Product Price` | DROP | Functionally determined by `Product Name` and duplicated by `Order Item Product Price`; less informative than product identity. |
| `Product Status` | DROP | Constant; no predictive information. |
| `Shipping Mode` | KEEP | Available at order time, strong observed target association, and chosen over deterministically equivalent scheduled days. |
| `shipping date (DateOrders)` | DROP | Future timestamp unavailable at prediction time. |

### Baseline raw KEEP set

```text
Type
Category Name
Customer Segment
Customer State
Department Name
Order Country
Order Item Discount
Order Item Quantity
Order Region
Product Name
Shipping Mode
```

Identifiers such as `Customer Id`, `Order Id`, and the raw order timestamp may still be retained outside the model matrix for grouping, validation, split design, and reproducibility.

---

## 6. Engineered and Analysis-Only Columns

These are **not part of the 53 raw columns**.

### Engineered model candidates

- `order_month` — **KEEP as candidate**; weak / inconsistent standalone association, but cheap temporal context.
- `order_dayofweek` — **KEEP as candidate**; weak standalone association, but cheap temporal context.
- `order_hour` — **INVESTIGATE / ABLATION**; available at prediction time, but part of its signal comes from the Same-Day calendar-boundary artifact. Compare model performance with and without it.

### Analysis-only columns

- `order_to_shipping_days`
- `calculated_late`
- `calendar_shipping_days`

`calculated_late` and `calendar_shipping_days` expose target-generation logic and must never be predictive inputs. `order_to_shipping_days` is also derived using the future shipping timestamp and is analysis-only.

---

## 7. Validation Status

### Completed

- [x] Official files obtained and stored locally.
- [x] Raw files excluded from Git.
- [x] Dataset loads successfully.
- [x] Row / column counts verified.
- [x] Target distribution verified.
- [x] Description-file mismatch checked.
- [x] Actual shipping-day derivation verified.
- [x] Exact target-generation rule verified.
- [x] Prediction point defined at order creation.
- [x] Confirmed leakage fields identified.
- [x] All 53 raw features reviewed and assigned a single KEEP / DROP decision.
- [x] Major redundancy and cardinality checks completed.

### Pending

- [ ] Run final data-quality audit: nulls, duplicate rows/entities, data types, timestamp validity, constants, and suspicious values.
- [ ] Apply documented cleaning rules, including invalid `Customer State` values.
- [ ] Identify entity / grouping keys for leakage-safe evaluation.
- [ ] Define train / validation / test split strategy.
- [ ] Create leakage-safe processed data.
- [ ] Train first baseline and run `order_hour` ablation.

---

## 8. Storage / Reproducibility

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

## 9. Next Steps

1. Run the final data-quality audit.
2. Apply the documented cleaning rules.
3. Define grouping keys and a leakage-safe train / validation / test split.
4. Build the processed baseline feature set.
5. Train the first leakage-safe baseline and compare results with vs. without `order_hour`.

