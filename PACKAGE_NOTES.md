# Package Notes — Governed BI Upgrade

## Main Improvement

Converted the cross-tool dashboard package into a reproducible governed BI
system. Derived extracts are rebuilt from one canonical order-level source, and
all executive, carrier, warehouse, customer, and daily metrics are independently
reconciled before visual evidence is generated.

## Corrected Metric Semantics

- Warehouse and customer fill rate now use weighted units rather than averaging
  order-level ratios.
- Rolling 30-Day OTIF now weights by order counts rather than averaging daily
  percentages.
- Daily exports expose additive service numerators for Tableau, Looker, and
  Power BI.

## Validation

- 11 source quality checks;
- 26 cross-extract and semantic reconciliation checks;
- 6 pytest tests;
- 3 regenerated PNG evidence files;
- pinned Python dependencies and GitHub Actions evidence artifact.

## Suggested Commit

```text
Add reproducible governed cross-platform BI lab
```
