# Executive Operations Dashboard Data Contract

This artifact defines a synthetic order-level dashboard source for Tableau, Looker, and Sigma-style BI review. It is a portfolio lab, not a production dashboard or certified enterprise dataset.

## Source Contract

Primary file: `data/executive_ops_dashboard_sample.csv`

Grain: one row per `order_id`.

| Field | Type | BI Role | Notes |
| --- | --- | --- | --- |
| `order_id` | string | primary key | Must be unique. |
| `order_date` | date | date filter | Dashboard date range. |
| `week_start` | date | trend date | Week bucket should not be after order date. |
| `region` | string | dimension/filter | Service geography. |
| `product_category` | string | dimension/filter | Product grouping. |
| `carrier` | string | dimension/filter | Logistics provider. |
| `customer_segment` | string | dimension/filter | Executive segmentation. |
| `revenue` | numeric | measure | Non-negative. |
| `cost` | numeric | measure | Non-negative. |
| `units_ordered` | integer | measure denominator | Non-negative. |
| `units_shipped` | integer | measure numerator | Cannot exceed ordered units. |
| `on_time` | boolean | OTIF component | True/false only. |
| `in_full` | boolean | OTIF component | True/false only. |
| `freight_cost` | numeric | logistics cost | Non-negative. |
| `forecast_units` | integer | forecast metric | Non-negative. |
| `actual_units` | integer | forecast metric | Must be positive for forecast accuracy. |
| `stockout_risk` | boolean | exception dimension | True/false only. |
| `exception_status` | string | exception filter | `open` or `closed`. |
| `exception_type` | string | exception detail | Open exceptions require a specific type. |

## KPI Dictionary

| KPI | Formula | Dashboard Use |
| --- | --- | --- |
| Revenue | `SUM(revenue)` | Executive top-line tile and trend. |
| Gross Margin % | `SUM(revenue - cost) / SUM(revenue)` | Profitability tile and segment scatter plot. |
| OTIF % | Distinct orders where `on_time` and `in_full` / distinct orders | Service reliability tile and heatmap. |
| Fill Rate | `SUM(units_shipped) / SUM(units_ordered)` | Fulfillment tile and trend. |
| Forecast Accuracy | `1 - ABS(SUM(forecast_units) - SUM(actual_units)) / SUM(actual_units)` | Planning quality panel. |
| Open Exceptions | Count rows where `exception_status = 'open'` | Triage workload tile and detail table. |
| Freight Cost Per Shipped Unit | `SUM(freight_cost) / SUM(units_shipped)` | Carrier cost comparison. |
| Stockout Risk Orders | Count rows where `stockout_risk = true` | Inventory-risk filter and alert. |

## Validation Contract

`python/validate_dashboard_data.py` checks:

- required columns are present
- `order_id` is unique
- numeric values are non-negative
- `units_shipped <= units_ordered`
- boolean fields contain valid true/false values
- open exceptions have a meaningful exception type
- order dates and week buckets parse correctly
- actual units are non-zero before forecast accuracy is displayed

## Semantic Layer Mapping

| Governed metric | Tableau | Looker | Sigma |
| --- | --- | --- | --- |
| Revenue | Published calculated field | `total_revenue` measure | Certified aggregate formula |
| OTIF % | `[OTIF %]` calculated field | `otif_rate` measure | Certified formula metric |
| Fill Rate | `[Fill Rate]` calculated field | `fill_rate` measure | Certified formula metric |
| Open Exceptions | `[Open Exceptions]` calculated field | filtered count measure | CountIf formula |
| Forecast Accuracy | `[Forecast Accuracy]` calculated field | ratio measure | Certified formula metric |

## Recruiter Review Guide

- Inspect the data contract first to understand grain and fields.
- Review Tableau calculated fields for guarded division and business-readable logic.
- Run the validator and compare output to top-row KPI expectations.
- Read the dashboard wireframe to see layout, filters, interactions, alerts, and QA criteria.
- Use the Looker/Sigma notes to confirm semantic-layer awareness beyond a single BI tool.
