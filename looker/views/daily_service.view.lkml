view: daily_service {
  sql_table_name: portfolio.daily_service_metrics ;;

  dimension_group: order {
    type: time
    timeframes: [date, week, month, quarter]
    sql: ${TABLE}.order_date ;;
  }

  measure: orders { type: sum sql: ${TABLE}.order_count ;; }
  measure: otif_orders { type: sum sql: ${TABLE}.otif_order_count ;; }
  measure: on_time_orders { type: sum sql: ${TABLE}.on_time_order_count ;; }
  measure: complete_orders { type: sum sql: ${TABLE}.complete_order_count ;; }
  measure: revenue { type: sum value_format_name: usd sql: ${TABLE}.revenue ;; }

  measure: otif_rate {
    type: number
    value_format_name: percent_2
    sql: ${otif_orders} / NULLIF(${orders}, 0) ;;
  }

  dimension: rolling_30d_otif {
    type: number
    value_format_name: percent_2
    sql: ${TABLE}.rolling_30d_otif ;;
  }
}
