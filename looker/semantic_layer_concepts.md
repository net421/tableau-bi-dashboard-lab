# Looker Semantic Layer Concepts

The LookML examples centralize dimensions and measures so dashboard creators do
not independently redefine OTIF, fill rate, or logistics cost.

## Important Design Choices

- `order_id` is the order-service primary key.
- Unit fill rate is a ratio of summed units.
- Boolean order metrics can be averaged only because the view grain is one row
  per order.
- Daily rolling metrics live in a dedicated daily view.
- Explores are labeled by business purpose rather than physical table name.

## Production Adaptation Notes

A production implementation should add:

- access grants;
- user attributes;
- persistent derived tables where justified;
- aggregate awareness;
- content validation;
- deployment-mode checks.
