# Looker Semantic Layer Concepts

This lab uses Looker-style concepts to describe governed BI metrics:

- Explores represent curated analytical entry points.
- Dimensions describe filterable/groupable fields.
- Measures define reusable metrics.
- Business definitions should be consistent across dashboards.

## Shared Semantic Contract

| Semantic object | Tableau equivalent | Looker equivalent | Sigma equivalent |
| --- | --- | --- | --- |
| `orders` explore / data source | Published data source | Explore | Worksheet / dataset |
| `order_id` | Dimension | Dimension primary key | Column |
| `revenue` | Measure / calculated field | Sum measure | Aggregate formula |
| `otif_rate` | Calculated field | Measure with filtered count | Formula metric |
| `fill_rate` | Calculated field | Measure ratio | Formula metric |
| `open_exceptions` | Calculated field | Filtered count measure | CountIf formula |
| `forecast_accuracy` | Calculated field | Measure ratio | Formula metric |

## Governance Notes

- KPI formulas should be defined once and reused across dashboards.
- Published Tableau data sources, Looker Explores, and Sigma datasets should expose the same metric names and grains.
- Distinct-order metrics must use `COUNTD(order_id)` or equivalent to prevent duplicated joins from inflating counts.
- Metrics with denominators need documented zero-handling.
- Dashboard consumers should see synthetic lab framing in captions or README context.
