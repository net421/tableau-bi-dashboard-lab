# Tableau Table Calculations

## Running Revenue

```tableau
RUNNING_SUM(SUM([revenue]))
```

## Weighted Rolling 30-Day OTIF

Use the daily service extract. The numerator and denominator must be rolled
separately; averaging daily rates is not valid when daily order volume differs.

```tableau
WINDOW_SUM(SUM([otif_order_count]), -29, 0)
/
WINDOW_SUM(SUM([order_count]), -29, 0)
```

## Period-over-Period Revenue Change

```tableau
(SUM([revenue]) - LOOKUP(SUM([revenue]), -1))
/
ABS(LOOKUP(SUM([revenue]), -1))
```

## Carrier Rank

```tableau
RANK_DENSE(AVG([otif_rate]), "desc")
```

## Share of Logistics Cost

```tableau
SUM([logistics_cost]) / TOTAL(SUM([logistics_cost]))
```

## Validation Note

Table calculations depend on partitioning and addressing. The workbook build
guide must explicitly configure compute-using fields, sort order, partition
dimensions, and date densification behavior.
