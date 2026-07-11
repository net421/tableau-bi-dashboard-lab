# Power Query Transformations

Recommended M steps:

1. Load validated order-service extract.
2. Promote headers.
3. Assign explicit data types.
4. Parse date columns.
5. Convert service flags to logical values.
6. Replace invalid blank numeric values with null, not zero.
7. Add refresh timestamp.
8. Reject duplicate `order_id` rows.
9. Load dimensions separately.
10. Disable load for intermediate queries.

Example duplicate guard:

```powerquery
let
    Source = Csv.Document(File.Contents(ParameterFilePath), [Delimiter=",", Encoding=65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(
        Headers,
        {
            {"order_id", type text},
            {"order_date", type date},
            {"revenue", Currency.Type},
            {"otif", type logical}
        }
    ),
    DuplicateOrders = Table.SelectRows(
        Table.Group(Typed, {"order_id"}, {{"Rows", each Table.RowCount(_), Int64.Type}}),
        each [Rows] > 1
    )
in
    if Table.RowCount(DuplicateOrders) > 0
    then error "Duplicate order_id values detected"
    else Typed
```
