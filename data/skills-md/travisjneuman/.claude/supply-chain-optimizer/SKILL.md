---
name: supply-chain-optimizer
description: Supply chain analysis, inventory optimization, logistics planning, vendor evaluation, and demand forecasting frameworks. Use when analyzing supply chains, optimizing inventory, or evaluating suppliers.
---

# Supply Chain Optimizer

Comprehensive frameworks for supply chain analysis, inventory management, logistics optimization, and vendor evaluation.

## Supply Chain Mapping Template

### End-to-End Supply Chain Map

```
RAW MATERIALS → SUPPLIERS → MANUFACTURING → DISTRIBUTION → CUSTOMER

MAPPING STEPS:
1. Identify all nodes (suppliers, plants, warehouses, customers)
2. Map material flows between nodes
3. Map information flows (orders, forecasts, POs)
4. Map financial flows (payments, invoicing)
5. Record lead times at each stage
6. Identify bottlenecks and single points of failure

NODE DETAIL TEMPLATE:
| Node           | Type       | Location  | Lead Time | Capacity | Utilization |
| -------------- | ---------- | --------- | --------- | -------- | ----------- |
|                | Supplier   |           |           |          |             |
|                | Plant      |           |           |          |             |
|                | Warehouse  |           |           |          |             |
|                | DC         |           |           |          |             |
```

## Inventory Optimization

### Economic Order Quantity (EOQ)

```
EOQ = sqrt(2DS / H)

Where: D = Annual demand, S = Ordering cost/order, H = Holding cost/unit/year
Total Cost = (D/Q)S + (Q/2)H + DC

Example: D=10,000, S=$50, H=$5 → EOQ = 447 units, 22.4 orders/year
```

### Safety Stock & Reorder Point

```
SAFETY STOCK: SS = z x sigma_dLT
REORDER POINT: ROP = (Avg Daily Demand x Lead Time) + Safety Stock

SERVICE LEVEL FACTORS:
| Service Level | z-Score | Use Case          |
| ------------- | ------- | ----------------- |
| 90.0%         | 1.28    | Basic coverage    |
| 95.0%         | 1.65    | Standard          |
| 99.0%         | 2.33    | High service      |
| 99.9%         | 3.09    | Critical items    |
```

### Inventory KPI Dashboard

| Metric                | Formula                                  | Target          |
| --------------------- | ---------------------------------------- | --------------- |
| Inventory Turns       | COGS / Average Inventory                 | Industry-specific |
| Days of Supply        | Average Inventory / (COGS / 365)         | Minimize        |
| Fill Rate             | Orders Filled Complete / Total Orders    | 97%+            |
| Stockout Rate         | Stockout Events / Total Demand Events    | < 2%            |
| Carrying Cost %       | Holding Costs / Average Inventory Value  | 15-30%          |
| Dead Stock %          | No-movement Items / Total SKUs           | < 5%            |
| Inventory Accuracy    | Correct Counts / Total Counts            | 99%+            |
| GMROI                 | Gross Margin / Average Inventory Cost    | > 2.0           |

## ABC-XYZ Analysis Framework

```
ABC CLASSIFICATION (Value):
A Items: Top 20% of SKUs = ~80% of annual consumption value
  → Tight control, frequent review, accurate forecasts
B Items: Next 30% of SKUs = ~15% of value
  → Moderate control, periodic review
C Items: Bottom 50% of SKUs = ~5% of value
  → Minimal control, simple replenishment rules

XYZ CLASSIFICATION (Demand Variability):
X: Coefficient of Variation < 0.5 → Stable, predictable demand
Y: CV between 0.5 and 1.0 → Some variation, trend/seasonal
Z: CV > 1.0 → Highly irregular, sporadic demand

COMBINED MATRIX:
| Class | AX         | AY           | AZ            |
| ----- | ---------- | ------------ | ------------- |
| Strat | JIT/Kanban | Forecast     | Order on demand|
| Class | BX         | BY           | BZ            |
| Strat | Reorder pt | Buffer stock | Min/Max       |
| Class | CX         | CY           | CZ            |
| Strat | Bulk buy   | Periodic rev | Eliminate?     |
```

## Vendor Scorecard

### Supplier Evaluation Matrix

| Criteria           | Weight | Score (1-5) | Weighted Score | Notes |
| ------------------ | ------ | ----------- | -------------- | ----- |
| Quality (PPM)      | 25%    |             |                |       |
| Delivery (OTIF)    | 20%    |             |                |       |
| Pricing            | 20%    |             |                |       |
| Responsiveness     | 10%    |             |                |       |
| Financial Health   | 10%    |             |                |       |
| Innovation         | 5%     |             |                |       |
| Sustainability     | 5%     |             |                |       |
| Risk Profile       | 5%     |             |                |       |
| **Total**          | 100%   |             | **__ / 5.0**   |       |

```
RATING SCALE:
4.5-5.0  Strategic Partner — expand relationship
3.5-4.4  Preferred Supplier — maintain, develop
2.5-3.4  Approved Supplier — improvement plan required
< 2.5    Probation / Exit — find alternative
```

### Supplier Performance Tracking

| KPI                 | Target  | Q1 Actual | Q2 Actual | Q3 Actual | Q4 Actual | Trend |
| ------------------- | ------- | --------- | --------- | --------- | --------- | ----- |
| On-Time Delivery    | 98%+    |           |           |           |           |       |
| Quality (PPM)       | < 500   |           |           |           |           |       |
| Lead Time (days)    |         |           |           |           |           |       |
| Price Variance      | +/- 2%  |           |           |           |           |       |
| Response Time (hrs) | < 24    |           |           |           |           |       |
| Corrective Actions  | < 2/qtr |           |           |           |           |       |

## Total Cost of Ownership (TCO)

```
TCO = Acquisition Costs + Operating Costs + Disposal Costs

ACQUISITION COSTS:
  Purchase price
+ Shipping / freight
+ Customs / duties / tariffs
+ Procurement labor
+ Quality inspection
+ Supplier qualification
= Total Acquisition

OPERATING COSTS (over useful life):
  Maintenance & repair
+ Inventory carrying cost
+ Warranty claims
+ Downtime cost (if component fails)
+ Training / support
+ Quality failures (scrap, rework)
= Total Operating

DISPOSAL COSTS:
  Decommissioning
+ Recycling / disposal fees
+ Environmental compliance
= Total Disposal

TCO = Total Acquisition + Total Operating + Total Disposal
```

### TCO Comparison Template

| Cost Element         | Supplier A | Supplier B | Supplier C |
| -------------------- | ---------- | ---------- | ---------- |
| Unit Price           |            |            |            |
| Shipping             |            |            |            |
| Duties / Tariffs     |            |            |            |
| Quality Cost (est.)  |            |            |            |
| Inventory Carry Cost |            |            |            |
| Lead Time Cost       |            |            |            |
| Risk Premium         |            |            |            |
| **Total TCO/Unit**   |            |            |            |
| **Annual TCO**       |            |            |            |

## Demand Forecasting Methods

| Method              | Best For                   | Horizon      | Data Required         |
| ------------------- | -------------------------- | ------------ | --------------------- |
| Moving Average      | Stable demand              | Short-term   | 3-12 periods history  |
| Exponential Smooth  | Trend detection            | Short-term   | Recent weighted data  |
| Holt-Winters        | Seasonal patterns          | Medium-term  | 2+ years seasonal     |
| Linear Regression   | Trend with causal factors  | Medium-term  | Demand + drivers      |
| ARIMA               | Complex time series        | Short-medium | 50+ data points       |
| Machine Learning    | Multi-variable patterns    | Any          | Large datasets        |
| Delphi / Expert     | New products, disruptions  | Long-term    | Expert panel          |

### Forecast Accuracy Metrics

```
MAD (Mean Absolute Deviation):
MAD = (1/n) x SUM(|Actual - Forecast|)

MAPE (Mean Absolute Percentage Error):
MAPE = (1/n) x SUM(|Actual - Forecast| / Actual) x 100

BIAS (Tracking Signal):
Bias = SUM(Actual - Forecast) / MAD
Target: Between -4 and +4

ACCURACY BENCHMARKS:
| Forecast Horizon | Good MAPE | Acceptable MAPE |
| ---------------- | --------- | --------------- |
| 1 month          | < 15%     | < 25%           |
| 3 months         | < 25%     | < 35%           |
| 6 months         | < 30%     | < 45%           |
| 12 months        | < 35%     | < 50%           |
```

## Logistics Optimization

### Transportation Mode Selection

| Mode     | Cost/Unit | Speed     | Capacity  | Best For                      |
| -------- | --------- | --------- | --------- | ----------------------------- |
| Truck    | Medium    | Fast      | Medium    | Regional, door-to-door        |
| Rail     | Low       | Slow      | Very High | Bulk, long-distance domestic  |
| Ocean    | Very Low  | Very Slow | Very High | International, bulk cargo     |
| Air      | Very High | Very Fast | Low       | High-value, urgent, perishable|
| Intermodal | Low-Med | Medium    | High      | Long-distance, cost-effective |

### Warehouse Layout Optimization

```
SLOTTING STRATEGY:
Fast movers (A items) → Near shipping dock, prime pick locations
Medium movers (B items) → Middle zones
Slow movers (C items) → High racks, far locations

LAYOUT PRINCIPLES:
1. Minimize travel distance for highest-velocity items
2. Group items frequently ordered together
3. Separate receiving and shipping areas
4. Reserve staging areas for cross-docking
5. Maintain clear aisle widths for equipment
```

## Lead Time Analysis

```
TOTAL LEAD TIME:
Order Processing Time
+ Supplier Manufacturing Time
+ Transportation Time
+ Receiving / Inspection Time
+ Internal Processing Time
= Total Lead Time

LEAD TIME VARIABILITY:
Track actual vs. quoted lead times over 12+ orders
Calculate standard deviation
Use for safety stock calculations

LEAD TIME REDUCTION STRATEGIES:
| Strategy              | Typical Reduction | Effort    |
| --------------------- | ----------------- | --------- |
| Vendor-managed inv.   | 30-50%            | Medium    |
| Local sourcing        | 40-70%            | High      |
| Process automation    | 10-30%            | Medium    |
| Blanket POs           | 20-40%            | Low       |
| Consignment stock     | 50-80%            | Medium    |
| 3PL consolidation     | 10-25%            | Low       |
```

## Supply Chain Risk Assessment

### Risk Identification Matrix

| Risk Category    | Risk Event              | Likelihood | Impact | Score | Mitigation             |
| ---------------- | ----------------------- | ---------- | ------ | ----- | ---------------------- |
| Supply           | Single-source failure   |            |        |       | Dual-source            |
| Demand           | Demand spike/collapse   |            |        |       | Buffer stock, flex     |
| Logistics        | Port congestion         |            |        |       | Alternate routes       |
| Geopolitical     | Tariffs, sanctions      |            |        |       | Nearshoring            |
| Natural Disaster | Earthquake, flood       |            |        |       | Geographic diversity   |
| Cyber            | System breach           |            |        |       | Security protocols     |
| Quality          | Batch failure           |            |        |       | Inspection, redundancy |
| Financial        | Supplier bankruptcy     |            |        |       | Financial monitoring   |

```
RISK SCORING:
Likelihood: 1 (Rare) to 5 (Almost Certain)
Impact: 1 (Negligible) to 5 (Catastrophic)
Risk Score = Likelihood x Impact

ACTION THRESHOLDS:
20-25  Critical — immediate action, executive attention
12-19  High — mitigation plan required within 30 days
6-11   Medium — monitor quarterly, contingency plans
1-5    Low — accept or monitor annually
```

## KPI Dashboard Template

| Category   | KPI                      | Target          |
| ---------- | ------------------------ | --------------- |
| Cost       | SC Cost as % of Revenue  | 5-10%           |
| Cost       | Cost per Order           | Minimize        |
| Service    | Perfect Order Rate       | 95%+            |
| Service    | On-Time In-Full (OTIF)   | 98%+            |
| Service    | Customer Fill Rate       | 97%+            |
| Efficiency | Inventory Turns          | Industry-specific|
| Efficiency | Cash-to-Cash Cycle       | Minimize        |
| Efficiency | Warehouse Utilization    | 85%             |
| Efficiency | Forecast Accuracy (MAPE) | < 20%           |

## See Also

- [Operations](../operations/SKILL.md)
- [Finance](../finance/SKILL.md)
- [Risk Management](../risk-management/SKILL.md)
