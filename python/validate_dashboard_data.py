"""Validate Tableau dashboard source data and calculate reference KPIs.

The script uses only the Python standard library so the BI artifact can be
reviewed without Tableau, pandas, or a warehouse connection. It validates the
synthetic order-level dashboard source and prints KPI values that Tableau tiles
should tie back to.
"""

from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path


LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "executive_ops_dashboard_sample.csv"

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "week_start",
    "region",
    "product_category",
    "carrier",
    "customer_segment",
    "revenue",
    "cost",
    "units_ordered",
    "units_shipped",
    "on_time",
    "in_full",
    "freight_cost",
    "forecast_units",
    "actual_units",
    "stockout_risk",
    "exception_status",
    "exception_type",
}


@dataclass(frozen=True)
class ValidationResult:
    name: str
    failing_rows: int
    detail: str = ""


class DashboardValidationError(Exception):
    """Raised when dashboard source data fails deterministic checks."""


def read_rows(path: Path = DATA_PATH) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"Invalid boolean value: {value}")
    return normalized == "true"


def parse_float(value: str) -> float:
    return float(value or 0)


def parse_int(value: str) -> int:
    return int(value or 0)


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def validate_rows(rows: list[dict[str, str]]) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    missing_columns = REQUIRED_COLUMNS - set(rows[0]) if rows else REQUIRED_COLUMNS
    results.append(ValidationResult("required_columns_present", len(missing_columns), ",".join(sorted(missing_columns))))

    order_ids = [row["order_id"] for row in rows]
    results.append(ValidationResult("unique_order_id", len(order_ids) - len(set(order_ids))))

    bad_numeric_rows = []
    bad_quantity_rows = []
    bad_boolean_rows = []
    bad_exception_rows = []
    bad_date_rows = []
    for row in rows:
        try:
            order_date = date.fromisoformat(row["order_date"])
            week_start = date.fromisoformat(row["week_start"])
            if week_start > order_date:
                bad_date_rows.append(row["order_id"])
        except ValueError:
            bad_date_rows.append(row["order_id"])

        numeric_values = [
            parse_float(row["revenue"]),
            parse_float(row["cost"]),
            parse_float(row["freight_cost"]),
            parse_int(row["units_ordered"]),
            parse_int(row["units_shipped"]),
            parse_int(row["forecast_units"]),
            parse_int(row["actual_units"]),
        ]
        if any(value < 0 for value in numeric_values):
            bad_numeric_rows.append(row["order_id"])
        if parse_int(row["units_shipped"]) > parse_int(row["units_ordered"]):
            bad_quantity_rows.append(row["order_id"])
        if parse_int(row["actual_units"]) == 0:
            bad_numeric_rows.append(row["order_id"])
        try:
            parse_bool(row["on_time"])
            parse_bool(row["in_full"])
            parse_bool(row["stockout_risk"])
        except ValueError:
            bad_boolean_rows.append(row["order_id"])
        if row["exception_status"] == "open" and row["exception_type"] in {"", "none"}:
            bad_exception_rows.append(row["order_id"])

    results.extend(
        [
            ValidationResult("non_negative_numeric_values", len(bad_numeric_rows), ",".join(bad_numeric_rows)),
            ValidationResult("units_shipped_not_above_units_ordered", len(bad_quantity_rows), ",".join(bad_quantity_rows)),
            ValidationResult("valid_boolean_values", len(bad_boolean_rows), ",".join(bad_boolean_rows)),
            ValidationResult("open_exceptions_have_type", len(bad_exception_rows), ",".join(bad_exception_rows)),
            ValidationResult("valid_order_and_week_dates", len(bad_date_rows), ",".join(bad_date_rows)),
        ]
    )

    failing = [result for result in results if result.failing_rows > 0]
    if failing:
        details = "; ".join(f"{result.name}={result.detail or result.failing_rows}" for result in failing)
        raise DashboardValidationError(f"Dashboard data validation failed: {details}")
    return results


def calculate_summary(rows: list[dict[str, str]], validation_results: list[ValidationResult]) -> dict[str, object]:
    revenue = sum(parse_float(row["revenue"]) for row in rows)
    cost = sum(parse_float(row["cost"]) for row in rows)
    units_ordered = sum(parse_int(row["units_ordered"]) for row in rows)
    units_shipped = sum(parse_int(row["units_shipped"]) for row in rows)
    freight_cost = sum(parse_float(row["freight_cost"]) for row in rows)
    forecast_units = sum(parse_int(row["forecast_units"]) for row in rows)
    actual_units = sum(parse_int(row["actual_units"]) for row in rows)
    otif_orders = sum(1 for row in rows if parse_bool(row["on_time"]) and parse_bool(row["in_full"]))
    open_exceptions = sum(1 for row in rows if row["exception_status"] == "open")
    stockout_risk_orders = sum(1 for row in rows if parse_bool(row["stockout_risk"]))

    return {
        "source_rows": len(rows),
        "distinct_orders": len({row["order_id"] for row in rows}),
        "revenue": round(revenue, 2),
        "gross_margin_rate": round(safe_divide(revenue - cost, revenue), 4),
        "otif_rate": round(safe_divide(otif_orders, len(rows)), 4),
        "fill_rate": round(safe_divide(units_shipped, units_ordered), 4),
        "forecast_accuracy": round(1 - safe_divide(abs(forecast_units - actual_units), actual_units), 4),
        "open_exceptions": open_exceptions,
        "stockout_risk_orders": stockout_risk_orders,
        "freight_cost_per_order": round(safe_divide(freight_cost, len(rows)), 2),
        "freight_cost_per_shipped_unit": round(safe_divide(freight_cost, units_shipped), 2),
        "validation_checks": len(validation_results),
    }


def run_validation() -> dict[str, object]:
    LOGGER.info("Loading dashboard source data from %s", DATA_PATH)
    rows = read_rows()
    validation_results = validate_rows(rows)
    return calculate_summary(rows, validation_results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    print(json.dumps(run_validation(), indent=2, sort_keys=True))
