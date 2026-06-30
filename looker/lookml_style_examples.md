# LookML-Style Example

```lookml
measure: total_revenue {
  type: sum
  sql: ${revenue} ;;
}

measure: orders_count {
  type: count_distinct
  sql: ${order_id} ;;
}
```
