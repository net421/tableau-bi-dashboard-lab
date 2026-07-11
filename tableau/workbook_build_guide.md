# Tableau Workbook Build Guide

## Data Sources

Use:

- `order_service_detail.csv` for order-level diagnostics;
- `daily_service_metrics.csv` for trends;
- `carrier_scorecard.csv` for carrier comparison;
- `customer_service_cost_mart.csv` for cost-to-serve;
- `warehouse_scorecard.csv` for warehouse comparison;
- `executive_kpis.csv` for validated headline values.

## Recommended Relationships

Avoid physical joins that duplicate order rows. Keep each extract as a logical
table and connect only when a cross-source dashboard requires it.

## Build Sequence

1. Create governed calculated fields.
2. Format rates as percentages and costs as currency.
3. Build KPI cards.
4. Build daily trend sheet.
5. Build carrier and warehouse scorecards.
6. Build customer cost-to-serve scatter.
7. Add filters and parameter actions.
8. Add metric-definition tooltips.
9. Reconcile displayed values with `executive_kpis.csv`.
10. Capture screenshots for the README.

## Performance Guidance

- Prefer extracts for the local portfolio dataset.
- Hide unused fields.
- Avoid unnecessary high-cardinality quick filters.
- Use order-level marts rather than order-line joins in Tableau.
- Document any context filters required by LOD expressions.
