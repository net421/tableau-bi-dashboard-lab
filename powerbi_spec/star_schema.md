# Power BI Star Schema

## Fact Tables

### FactOrderService

Grain: one row per order.

Measures:

- units ordered;
- units shipped;
- revenue;
- freight cost;
- logistics cost;
- service flags.

## Dimensions

- DimDate
- DimCustomer
- DimCarrier
- DimWarehouse

## Relationships

All relationships are one-to-many from dimensions to `FactOrderService`, with
single-direction filtering.

Do not create many-to-many relationships to solve duplicated KPI problems.
Correct the upstream grain instead.
