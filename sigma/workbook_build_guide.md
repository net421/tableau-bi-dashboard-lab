# Sigma Workbook Build Guide

## Pages

1. Executive Overview
2. Carrier Performance
3. Warehouse Performance
4. Customer Cost-to-Serve
5. Order Exceptions
6. Metric Definitions

## Recommended Controls

- Order date range
- Warehouse
- Carrier
- Customer
- KPI target
- Metric selector

## Self-Service Guardrails

- Publish certified datasets rather than raw order lines.
- Lock governed KPI formulas.
- Allow users to create local calculations only in sandbox pages.
- Display metric owners and definitions in the workbook.
- Use workbook permissions to separate viewers, explorers, and editors.

## Input Tables

Use the CSV extracts in `data/tableau_ready_exports/`, or replace them with
warehouse tables using the same column contracts.
