# LookML Implementation Examples

The executable semantic examples live in:

- `views/order_service.view.lkml` for order-grain dimensions and governed measures;
- `views/daily_service.view.lkml` for additive daily service numerators and weighted rates;
- `models/operations.model.lkml` for curated explores.

Key design rule: ratio measures aggregate additive numerators and denominators;
they do not average previously calculated percentages across mixed grains.
