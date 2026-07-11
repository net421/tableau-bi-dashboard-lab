# Tableau LOD Expressions

## Customer Lifetime Revenue

```tableau
{ FIXED [customer_id] : SUM([revenue]) }
```

## Customer Lifetime Logistics Cost

```tableau
{ FIXED [customer_id] : SUM([logistics_cost]) }
```

## Order-Level Shipped Units

Use when the source is later expanded back to order-line grain.

```tableau
{ FIXED [order_id] : SUM([units_shipped]) }
```

## Carrier Enterprise OTIF

```tableau
{ FIXED [carrier] :
    COUNTD(IF [otif] THEN [order_id] END)
}
/
{ FIXED [carrier] : COUNTD([order_id]) }
```

## Warehouse Revenue Share

```tableau
SUM([revenue])
/
{ FIXED : SUM([revenue]) }
```

## When to Use LODs

Use LOD expressions to protect KPI grain, not merely to make calculations look
advanced. Each LOD should document why the visualization filter context would
otherwise produce an incorrect result.
