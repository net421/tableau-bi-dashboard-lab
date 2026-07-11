# Tableau Parameters and Actions

## KPI Selector Parameter

Allowed values:

- OTIF
- Unit Fill Rate
- On-Time Delivery
- Complete Order Rate
- Logistics Cost
- Revenue

A calculated field returns the selected metric.

## Service Target Parameter

Numeric range from 0.50 to 1.00 with a default of 0.95.

Use the target to classify:

```tableau
IF [Selected Service KPI] >= [Service Target] THEN "At/Above Target"
ELSE "Below Target"
END
```

## Dashboard Actions

- Selecting a warehouse filters carriers, customers, and daily trends.
- Selecting a carrier highlights late-order detail.
- Clicking a KPI card navigates to the relevant diagnostic sheet.
- A parameter action switches the primary metric without duplicating sheets.
