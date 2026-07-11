connection: "portfolio_warehouse"

include: "/views/*.view.lkml"

explore: order_service {
  label: "Order Service Performance"
  description: "Certified order-level service and logistics measures."
}

explore: daily_service {
  label: "Daily Service Trends"
  description: "Daily and rolling operational KPI trends."
}
