# Tableau Calculated Fields

These calculated fields are written for the synthetic `executive_ops_dashboard_sample.csv` data contract. They demonstrate dashboard logic, not production-certified metrics.

## Revenue

```text
SUM([Revenue])
```

## Gross Margin %

```text
IF SUM([Revenue]) = 0 THEN 0
ELSE SUM([Revenue] - [Cost]) / SUM([Revenue])
END
```

## OTIF %

```text
SUM(IF [On Time] = TRUE AND [In Full] = TRUE THEN 1 ELSE 0 END)
/
COUNTD([Order ID])
```

## Fill Rate

```text
IF SUM([Units Ordered]) = 0 THEN 0
ELSE SUM([Units Shipped]) / SUM([Units Ordered])
END
```

## Forecast Accuracy

```text
IF SUM([Actual Units]) = 0 THEN NULL
ELSE 1 - ABS(SUM([Forecast Units]) - SUM([Actual Units])) / SUM([Actual Units])
END
```

## Open Exceptions

```text
SUM(IF [Exception Status] = "open" THEN 1 ELSE 0 END)
```

## Freight Cost Per Order

```text
IF COUNTD([Order ID]) = 0 THEN 0
ELSE SUM([Freight Cost]) / COUNTD([Order ID])
END
```

## Freight Cost Per Shipped Unit

```text
IF SUM([Units Shipped]) = 0 THEN NULL
ELSE SUM([Freight Cost]) / SUM([Units Shipped])
END
```

## Stockout Risk Orders

```text
SUM(IF [Stockout Risk] = TRUE THEN 1 ELSE 0 END)
```

## Late Or Partial Orders

```text
SUM(
    IF [On Time] = FALSE OR [In Full] = FALSE
    THEN 1
    ELSE 0
    END
)
```

## Service Health Band

```text
IF [OTIF %] >= 0.95 THEN "green"
ELSEIF [OTIF %] >= 0.85 THEN "yellow"
ELSE "red"
END
```
