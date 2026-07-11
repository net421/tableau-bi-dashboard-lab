# Refresh Strategy

## Local Portfolio Mode

- CSV extracts refreshed after the validated pipeline runs.
- Power BI Desktop refreshes from the local export folder.

## Production-Style Pattern

1. Data pipeline publishes certified marts.
2. Data quality gate passes.
3. Semantic model refresh starts.
4. Refresh status is monitored.
5. Dashboard timestamp updates only after success.

## Incremental Refresh

Partition `FactOrderService` by `order_date` when the dataset becomes large.
Retain historical partitions and refresh only the recent operational window.
