# Executive Operations Dashboard Data Contract

This contract preserves the strongest governed-source ideas from the original
partial dashboard proposal and applies them to the complete cross-tool BI lab.
The artifacts are synthetic portfolio evidence, not a certified production
semantic layer.

## Canonical Detail Extract

Primary file: `data/tableau_ready_exports/order_service_detail.csv`

Grain: exactly one row per `order_id`.

| Field group | Key fields | Contract |
|---|---|---|
| Identity | `order_id`, `shipment_id` | `order_id` is unique and non-null. |
| Dimensions | `customer_id`, `warehouse`, `carrier`, `order_date` | Stable filtering dimensions. |
| Quantity | `units_ordered`, `units_shipped` | Non-negative; shipped cannot exceed ordered. |
| Service | `in_full`, `on_time`, `otif` | `otif = in_full AND on_time`. |
| Finance | `revenue`, `freight_cost`, `handling_cost`, `exception_cost`, `logistics_cost` | Non-negative; logistics cost reconciles to components. |
| Delivery | `promised_date`, `delivery_date`, `delivery_delay_days` | Dates parse and delivery is not before order date. |

## Derived Extracts

| File | Grain | Purpose |
|---|---|---|
| `executive_kpis.csv` | one row per governed KPI | Executive cards and reference totals. |
| `daily_service_metrics.csv` | one row per order date | Weighted daily and rolling service trends. |
| `carrier_scorecard.csv` | one row per carrier | Carrier service and freight performance. |
| `warehouse_scorecard.csv` | one row per warehouse | Warehouse service, revenue, and cost. |
| `customer_service_cost_mart.csv` | one row per customer | Customer service and cost-to-serve analysis. |
| `data_quality_report.csv` | one row per quality rule | Human-readable source contract evidence. |

## Aggregation Rules

- Unit Fill Rate is always `SUM(units_shipped) / SUM(units_ordered)`.
- Complete Order Rate, On-Time Delivery, and OTIF use order counts.
- Freight Cost per kg is weighted by shipment weight.
- Cost-to-Serve Ratio is `SUM(logistics_cost) / SUM(revenue)`.
- Rolling 30-Day OTIF is weighted by order counts, never an unweighted average
  of daily rates.

## Change Control

A definition or grain change must update the KPI dictionary, metric-lineage
ledger, derived-export builder, validation script, tests, Tableau calculations,
LookML, DAX, and dashboard annotations in the same pull request.
