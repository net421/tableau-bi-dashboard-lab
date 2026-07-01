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

measure: otif_orders {
  type: count_distinct
  sql: ${order_id} ;;
  filters: [on_time: "yes", in_full: "yes"]
}

measure: otif_rate {
  type: number
  sql: ${otif_orders} / nullif(${orders_count}, 0) ;;
  value_format_name: percent_2
}

measure: fill_rate {
  type: number
  sql: sum(${units_shipped}) / nullif(sum(${units_ordered}), 0) ;;
  value_format_name: percent_2
}

measure: open_exceptions {
  type: count_distinct
  sql: ${order_id} ;;
  filters: [exception_status: "open"]
}
```
