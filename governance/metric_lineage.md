# Governed Metric Lineage

This ledger connects every executive metric to its canonical extract, grain,
tool implementation, and executable validation. Tool-specific formulas may
change syntax, but they may not change the governed business definition.

| Metric ID | Business metric | Canonical source and fields | Evaluation grain | Tableau | Looker | Power BI | Validation evidence |
|---|---|---|---|---|---|---|---|
| `service.unit_fill_rate` | Unit Fill Rate | `order_service_detail.csv`: `units_shipped`, `units_ordered` | Weighted across order quantities | `tableau/calculated_fields.md` | `order_service.view.lkml` | `Unit Fill Rate %` | `executive::Unit Fill Rate`; warehouse/customer reconciliation |
| `service.complete_order_rate` | Complete Order Rate | `order_service_detail.csv`: `in_full`, `order_id` | One row per order | `tableau/calculated_fields.md` | `complete_order_rate` | `Complete Order Rate %` | `executive::Complete Order Rate` |
| `service.on_time_delivery` | On-Time Delivery | `order_service_detail.csv`: `on_time`, `order_id` | One row per order | `tableau/calculated_fields.md` | `on_time_rate` | `On-Time Delivery %` | `executive::On-Time Delivery` |
| `service.otif` | OTIF | `order_service_detail.csv`: `otif`, `order_id` | One row per order | `tableau/calculated_fields.md` | `otif_rate` | `OTIF %` | `executive::OTIF`; component checks |
| `transport.freight_cost_per_kg` | Freight Cost per kg | `order_service_detail.csv`: `freight_cost`, `shipment_weight_kg` | Weighted across shipments | `tableau/calculated_fields.md` | `freight_cost_per_kg` | `Freight Cost per kg` | `executive::Freight Cost per kg`; carrier reconciliation |
| `customer.cost_to_serve_ratio` | Cost-to-Serve Ratio | `customer_service_cost_mart.csv`: `logistics_cost`, `revenue` | Customer or selected filter context | `tableau/calculated_fields.md` | governed ratio concept | governed DAX ratio | customer mart reconciliation |
| `service.rolling_30d_otif` | Rolling 30-Day OTIF | `daily_service_metrics.csv`: `otif_order_count`, `order_count` | Weighted 30-calendar-day window | `tableau/table_calculations.md` | `daily_service.view.lkml` | `Rolling 30-Day OTIF %` | `semantic::rolling 30-day OTIF weighted` |
| `finance.revenue` | Revenue | `order_service_detail.csv`: `revenue` | Sum in filter context | standard measure | `revenue` | `Revenue` | `executive::Revenue`; daily/customer/warehouse reconciliation |
| `finance.logistics_cost` | Logistics Cost | `order_service_detail.csv`: `logistics_cost` | Sum in filter context | standard measure | `logistics_cost` | `Logistics Cost` | `executive::Logistics Cost`; customer/warehouse reconciliation |
