# Tableau Calculated Fields

## Revenue

```text
SUM([Revenue])
```

## Gross Margin %

```text
SUM([Revenue] - [Cost]) / SUM([Revenue])
```

## OTIF %

```text
SUM(IF [On Time] = TRUE AND [In Full] = TRUE THEN 1 ELSE 0 END) / COUNT([Order ID])
```

## Fill Rate

```text
SUM([Units Shipped]) / SUM([Units Ordered])
```

## Forecast Accuracy

```text
1 - ABS(SUM([Forecast Units]) - SUM([Actual Units])) / SUM([Actual Units])
```
