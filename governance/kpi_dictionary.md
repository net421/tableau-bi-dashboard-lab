# Governed KPI Dictionary

## Governance Rules

Every KPI must declare:

1. business definition;
2. numerator;
3. denominator;
4. grain;
5. filter context;
6. null handling;
7. owner;
8. validation query or script.

## Core Metrics

### Unit Fill Rate

**Definition:** Units shipped divided by units ordered.

```text
SUM(units_shipped) / SUM(units_ordered)
```

- Grain: evaluated over order-line quantities.
- Valid range: 0–1.
- Do not average order-level fill rates for the enterprise KPI.
- Owner: Supply Chain Analytics.

### Complete Order Rate

**Definition:** Percentage of orders with all requested units shipped.

```text
COUNTD(IF in_full THEN order_id END) / COUNTD(order_id)
```

- Grain: one row per order.
- This is not the same as unit fill rate.

### On-Time Delivery

**Definition:** Percentage of orders delivered on or before promised date.

```text
COUNTD(IF on_time THEN order_id END) / COUNTD(order_id)
```

### OTIF

**Definition:** Percentage of orders that are both on time and in full.

```text
COUNTD(IF otif THEN order_id END) / COUNTD(order_id)
```

- OTIF cannot exceed either on-time delivery or complete-order rate.

### Freight Cost per kg

```text
SUM(freight_cost) / SUM(shipment_weight_kg)
```

- Use weighted aggregation, not average row-level cost per kg.

### Cost-to-Serve Ratio

```text
SUM(logistics_cost) / SUM(revenue)
```

- Evaluate by customer, region, or channel.
- Exclude records with zero revenue from ratios.

### Rolling 30-Day OTIF

- Computed over daily order counts.
- Requires weighted numerator and denominator.
- Avoid averaging daily OTIF rates unless every day has identical order volume.

## Metric Ownership

| Domain | Business Owner | Technical Owner |
|---|---|---|
| Service | VP Operations | Analytics Engineering |
| Transportation | Logistics Director | BI Engineering |
| Customer Cost-to-Serve | Finance + Operations | Analytics Engineering |
| Warehouse Performance | Warehouse Operations | BI Engineering |
