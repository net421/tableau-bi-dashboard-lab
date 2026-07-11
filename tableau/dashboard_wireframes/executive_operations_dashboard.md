# Executive Operations Dashboard Wireframe

## Canvas

- Desktop: 1440 × 900
- Tablet: 1024 × 768
- Primary audience: operations executives and logistics managers

## Layout

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Title | Date | Warehouse | Carrier | Customer | KPI Target         │
├──────────────┬──────────────┬──────────────┬────────────────────────┤
│ OTIF         │ Fill Rate    │ On-Time      │ Logistics Cost         │
├──────────────┴──────────────┴──────────────┴────────────────────────┤
│ Rolling 30-Day OTIF Trend                                          │
├───────────────────────────────────┬─────────────────────────────────┤
│ Carrier Scorecard                 │ Warehouse Scorecard             │
├───────────────────────────────────┼─────────────────────────────────┤
│ Customer Cost-to-Serve Scatter    │ High-Priority Exceptions        │
└───────────────────────────────────┴─────────────────────────────────┘
```

## Executive Questions Answered

1. Is service improving or deteriorating?
2. Which carrier or warehouse explains the largest OTIF gap?
3. Which customers combine low service with high logistics cost?
4. Where should operations intervene first?

## Interaction Rules

- Filters apply globally unless a sheet is explicitly diagnostic-only.
- Tooltips expose KPI definition and source timestamp.
- KPI cards include target variance.
- Exception tables use action-oriented language, not only metrics.
