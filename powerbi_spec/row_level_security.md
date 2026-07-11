# Row-Level Security

## Scenario

Regional or warehouse managers should only see assigned warehouses.

## Security Mapping

Create:

```text
UserWarehouseAccess
- user_email
- warehouse
```

Relate `UserWarehouseAccess[warehouse]` to `DimWarehouse[warehouse]`.

Role filter:

```DAX
UserWarehouseAccess[user_email] = USERPRINCIPALNAME()
```

## Validation

Test:

- one user with one warehouse;
- one user with multiple warehouses;
- an executive user with all warehouses;
- an unknown user with no access.

RLS must not alter metric definitions; it only limits visible rows.
