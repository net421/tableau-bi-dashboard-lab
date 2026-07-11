view: order_service {
  sql_table_name: portfolio.order_service_detail ;;

  dimension: order_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.order_id ;;
  }

  dimension_group: order {
    type: time
    timeframes: [date, week, month, quarter, year]
    sql: ${TABLE}.order_date ;;
  }

  dimension: customer_id { type: string sql: ${TABLE}.customer_id ;; }
  dimension: carrier { type: string sql: ${TABLE}.carrier ;; }
  dimension: warehouse { type: string sql: ${TABLE}.warehouse ;; }
  dimension: on_time { type: yesno sql: ${TABLE}.on_time ;; }
  dimension: in_full { type: yesno sql: ${TABLE}.in_full ;; }
  dimension: otif { type: yesno sql: ${TABLE}.otif ;; }

  measure: orders {
    type: count_distinct
    sql: ${order_id} ;;
  }

  measure: units_ordered { type: sum sql: ${TABLE}.units_ordered ;; }
  measure: units_shipped { type: sum sql: ${TABLE}.units_shipped ;; }

  measure: unit_fill_rate {
    type: number
    value_format_name: percent_2
    sql: ${units_shipped} / NULLIF(${units_ordered}, 0) ;;
  }

  measure: complete_order_rate {
    type: average
    value_format_name: percent_2
    sql: CASE WHEN ${in_full} THEN 1.0 ELSE 0.0 END ;;
  }

  measure: on_time_rate {
    type: average
    value_format_name: percent_2
    sql: CASE WHEN ${on_time} THEN 1.0 ELSE 0.0 END ;;
  }

  measure: otif_rate {
    type: average
    value_format_name: percent_2
    sql: CASE WHEN ${otif} THEN 1.0 ELSE 0.0 END ;;
  }

  measure: revenue {
    type: sum
    value_format_name: usd
    sql: ${TABLE}.revenue ;;
  }

  measure: logistics_cost {
    type: sum
    value_format_name: usd
    sql: ${TABLE}.logistics_cost ;;
  }

  measure: freight_cost_per_kg {
    type: number
    value_format_name: usd
    sql: SUM(${TABLE}.freight_cost) / NULLIF(SUM(${TABLE}.shipment_weight_kg), 0) ;;
  }
}
