# DAX Measures

```DAX
Orders :=
DISTINCTCOUNT ( FactOrderService[order_id] )
```

```DAX
Units Ordered :=
SUM ( FactOrderService[units_ordered] )
```

```DAX
Units Shipped :=
SUM ( FactOrderService[units_shipped] )
```

```DAX
Unit Fill Rate % :=
DIVIDE ( [Units Shipped], [Units Ordered] )
```

```DAX
Complete Order Rate % :=
DIVIDE (
    CALCULATE ( [Orders], FactOrderService[in_full] = TRUE () ),
    [Orders]
)
```

```DAX
On-Time Delivery % :=
DIVIDE (
    CALCULATE ( [Orders], FactOrderService[on_time] = TRUE () ),
    [Orders]
)
```

```DAX
OTIF % :=
DIVIDE (
    CALCULATE ( [Orders], FactOrderService[otif] = TRUE () ),
    [Orders]
)
```

```DAX
Revenue :=
SUM ( FactOrderService[revenue] )
```

```DAX
Logistics Cost :=
SUM ( FactOrderService[logistics_cost] )
```

```DAX
Freight Cost per kg :=
DIVIDE (
    SUM ( FactOrderService[freight_cost] ),
    SUM ( FactOrderService[shipment_weight_kg] )
)
```

```DAX
Rolling 30-Day OTIF % :=
VAR EndDate = MAX ( DimDate[Date] )
VAR DateWindow =
    DATESINPERIOD ( DimDate[Date], EndDate, -30, DAY )
RETURN
    CALCULATE ( [OTIF %], DateWindow )
```

```DAX
Revenue Previous Month :=
CALCULATE ( [Revenue], DATEADD ( DimDate[Date], -1, MONTH ) )
```

```DAX
Revenue MoM % :=
DIVIDE ( [Revenue] - [Revenue Previous Month], [Revenue Previous Month] )
```
