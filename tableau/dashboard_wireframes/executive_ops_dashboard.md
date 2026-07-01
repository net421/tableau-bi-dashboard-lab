# Executive Operations Dashboard Wireframe

## Audience

Executives, operations leaders, BI managers, supply chain analysts, and finance partners reviewing service, margin, and exception performance.

## Dashboard Purpose

Give leaders a one-screen operating view that connects revenue, margin, fulfillment reliability, forecast quality, freight cost, and open exceptions. The dashboard should support both executive scanning and analyst triage.

## Data Source

Primary source: `data/executive_ops_dashboard_sample.csv`

Grain: one row per order.

Required validation before publishing:

- `Order ID` is unique.
- Numeric KPI fields are non-negative.
- `Units Shipped` does not exceed `Units Ordered`.
- Boolean fields contain valid true/false values.
- Open exception rows have an exception type.
- Forecast accuracy denominator is non-zero when the KPI is displayed.

## Top KPI Band

| Tile | Primary calculation | Alert rule |
| --- | --- | --- |
| Revenue | `SUM([Revenue])` | Show down arrow if below prior period target. |
| Gross Margin % | `SUM([Revenue]-[Cost]) / SUM([Revenue])` | Red below 30%, yellow below 40%. |
| OTIF % | On-time and in-full orders / distinct orders | Red below 85%, yellow below 95%. |
| Fill Rate | Units shipped / units ordered | Red below 90%, yellow below 97%. |
| Open Exceptions | Count open exception rows | Red when high-priority exceptions exist. |
| Forecast Accuracy | `1 - ABS(forecast - actual) / actual` | Red below 80%, yellow below 90%. |

## Main Views

1. Trend line: weekly revenue, OTIF %, and fill rate.
2. Bar chart: freight cost and freight cost per shipped unit by carrier.
3. Heatmap: OTIF % by region and product category.
4. Scatter plot: revenue vs gross margin % by customer segment.
5. Exception table: open late, partial, high-cost, and stockout-risk orders.
6. Forecast accuracy panel by product category and region.

## Filters

- Date range
- Region
- Product category
- Carrier
- Customer segment

## Interactions

- Selecting a region filters carrier, heatmap, and exception table.
- Selecting a carrier highlights freight cost trend and late/partial exceptions.
- Clicking an exception row should reveal order id, customer segment, promised date, units ordered, units shipped, and exception type.
- KPI tiles should retain context filters but not be affected by exception table row selection.

## Exception Priority Logic

| Priority | Rule |
| --- | --- |
| High | Open exception with stockout risk or fill rate below 80%. |
| Medium | Open exception with late delivery or partial fill. |
| Monitor | Closed exception or forecast accuracy below threshold but no service failure. |

## QA Checklist

- Top KPI totals tie to the validator output.
- Filtered views preserve order grain and do not double-count revenue.
- Tooltips show metric formulas in stakeholder language.
- Null/zero denominator cases render as `0` or `NULL` intentionally.
- Open exception count matches the row-level exception table.
- Dashboard title and captions identify the data as synthetic portfolio evidence.
