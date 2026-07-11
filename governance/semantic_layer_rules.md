# Semantic Layer Rules

## Certified Dimensions

- Order Date
- Customer
- Carrier
- Warehouse

## Certified Measures

- Orders
- Units Ordered
- Units Shipped
- Revenue
- Logistics Cost
- Unit Fill Rate
- Complete Order Rate
- On-Time Delivery
- OTIF
- Freight Cost per kg

## Grain Protection

`order_service_detail.csv` is one row per order. Measures from this table can be
aggregated by order date, customer, warehouse, and carrier without double
counting orders.

## Naming Rules

- Percent metrics end with `_rate` or `%` in presentation layers.
- Cost and revenue measures use currency formatting.
- Boolean dimensions use positive business language: `On Time`, `In Full`,
  `OTIF`.
- Tool-specific names must map back to the same governed definition.

## Change Control

A KPI definition change should update:

1. this semantic-layer document;
2. the KPI dictionary;
3. validation code;
4. Tableau calculated fields;
5. LookML measures;
6. Power BI DAX;
7. dashboard annotations.
