# Sigma Self-Service BI Notes

Sigma-style self-service BI emphasizes spreadsheet-like exploration on governed warehouse data. This portfolio lab frames Sigma as a consumption layer for curated marts and certified metrics.

## Self-Service Guardrails

- Start exploration from the governed order-level dataset, not raw extracts.
- Use certified metric columns for OTIF, fill rate, margin, forecast accuracy, and exceptions.
- Keep row-level exception tables linked to KPI tiles so users can audit the aggregate.
- Use protected formulas for denominator handling rather than ad hoc analyst copies.
- Publish a short data freshness and validation note beside executive-facing worksheets.
