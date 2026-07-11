# Validation Summary

- Governed exports rebuilt from `order_service_detail.csv`: 2,400 orders.
- Source quality controls: 11 passed, 0 failed.
- Cross-extract and semantic reconciliations: 26 passed, 0 failed.
- Pytest: 6 passed.
- Visual evidence regenerated: 3 PNG files.
- Unit Fill Rate uses weighted shipped and ordered units at every grain.
- Rolling 30-Day OTIF uses rolling OTIF-order counts divided by rolling order counts.
- Tableau, Looker, Sigma, and Power BI definitions map to the same metric-lineage ledger.
