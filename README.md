# Tableau BI Dashboard Lab

A BI specification lab for Tableau, Looker, Sigma and self-service analytics. This repo demonstrates dashboard planning, KPI logic, semantic-layer thinking and stakeholder-ready BI documentation.

This is a synthetic BI lab, not a production dashboard deployment. It is designed to show dashboard requirements, governed KPI logic, data contract validation, and stakeholder-ready review criteria.

## Featured Artifact: Validated Executive Operations Dashboard

| File | What it proves |
| --- | --- |
| `data/executive_ops_dashboard_sample.csv` | Synthetic dashboard-grain source data with revenue, margin, fulfillment, forecast, freight, stockout, and exception scenarios. |
| `python/validate_dashboard_data.py` | Executable data contract validator and KPI calculator using only the Python standard library. |
| `tableau/calculated_fields.md` | Tableau calculated field definitions with guarded division and dashboard-ready metric logic. |
| `tableau/dashboard_wireframes/executive_ops_dashboard.md` | Dense dashboard layout, filters, interactions, alert rules, and QA criteria. |
| `docs/dashboard_data_contract.md` | Field-level source contract, KPI dictionary, validation rules, and semantic layer mapping. |
| `looker/semantic_layer_concepts.md` | Governed metric guidance for Tableau, Looker, and Sigma consumption layers. |

## Local Validation

```bash
python python/validate_dashboard_data.py
```

Expected summary:

- 12 dashboard source rows
- 12 distinct orders
- revenue `9890.0`
- OTIF rate `0.5`
- fill rate `0.9239`
- gross margin rate `0.4176`
- forecast accuracy `0.9898`
- 6 open exceptions

## Skill Evidence

- Tableau calculated fields and dashboard design
- semantic-layer metric definitions
- data contract and dashboard QA thinking
- stakeholder-first dashboard specification
- validation-backed BI metrics
