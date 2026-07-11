# Tableau Calculated Fields

## Unit Fill Rate

```tableau
SUM([units_shipped]) / SUM([units_ordered])
```

## Complete Order Rate

```tableau
COUNTD(IF [in_full] THEN [order_id] END)
/
COUNTD([order_id])
```

## On-Time Delivery

```tableau
COUNTD(IF [on_time] THEN [order_id] END)
/
COUNTD([order_id])
```

## OTIF

```tableau
COUNTD(IF [otif] THEN [order_id] END)
/
COUNTD([order_id])
```

## Freight Cost per kg

```tableau
SUM([freight_cost]) / SUM([shipment_weight_kg])
```

## Cost-to-Serve Ratio

```tableau
SUM([logistics_cost]) / SUM([revenue])
```

## Delay Bucket

```tableau
IF [delivery_delay_days] <= 0 THEN "On Time"
ELSEIF [delivery_delay_days] <= 2 THEN "1–2 Days Late"
ELSEIF [delivery_delay_days] <= 5 THEN "3–5 Days Late"
ELSE "6+ Days Late"
END
```

## Service Exception Priority

```tableau
IF NOT [otif] AND [logistics_cost] > { FIXED : MEDIAN([logistics_cost]) }
THEN "High"
ELSEIF NOT [otif]
THEN "Medium"
ELSE "Normal"
END
```
