from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tableau_ready_exports"
TOLERANCE = 1e-9


def _bool_series(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.astype(bool)
    mapped = series.astype(str).str.strip().str.lower().map({"true": True, "false": False, "1": True, "0": False})
    if mapped.isna().any():
        raise ValueError(f"Invalid boolean values in {series.name}")
    return mapped.astype(bool)


def load_detail() -> pd.DataFrame:
    detail = pd.read_csv(DATA / "order_service_detail.csv")
    for column in ["in_full", "on_time", "otif"]:
        detail[column] = _bool_series(detail[column])
    return detail


def calculate_metrics() -> dict[str, float]:
    detail = load_detail()
    return {
        "Unit Fill Rate": detail["units_shipped"].sum() / detail["units_ordered"].sum(),
        "Complete Order Rate": detail["in_full"].mean(),
        "On-Time Delivery": detail["on_time"].mean(),
        "OTIF": detail["otif"].mean(),
        "Revenue": detail["revenue"].sum(),
        "Logistics Cost": detail["logistics_cost"].sum(),
        "Freight Cost per kg": detail["freight_cost"].sum() / detail["shipment_weight_kg"].sum(),
        "Average Delay Days": detail["delivery_delay_days"].mean(),
    }


def _frame_close(actual: pd.DataFrame, expected: pd.DataFrame, keys: list[str], numeric: list[str]) -> tuple[bool, float]:
    merged = actual.merge(expected, on=keys, suffixes=("_actual", "_expected"), how="outer", indicator=True)
    if not (merged["_merge"] == "both").all():
        return False, float("inf")
    max_diff = 0.0
    for column in numeric:
        diff = (merged[f"{column}_actual"] - merged[f"{column}_expected"]).abs().max()
        max_diff = max(max_diff, float(diff))
    return max_diff < TOLERANCE, max_diff


def validation_checks() -> list[dict[str, object]]:
    detail = load_detail()
    checks: list[dict[str, object]] = []

    def add(name: str, passed: bool, expected: object, actual: object) -> None:
        checks.append({"check_name": name, "status": "PASS" if passed else "FAIL", "expected": expected, "actual": actual})

    expected_metrics = pd.read_csv(DATA / "executive_kpis.csv").set_index("metric_name")["metric_value"].to_dict()
    actual_metrics = calculate_metrics()
    for name, value in actual_metrics.items():
        expected = float(expected_metrics[name])
        add(f"executive::{name}", abs(value - expected) < TOLERANCE, expected, float(value))
    add("semantic::OTIF not above on-time", actual_metrics["OTIF"] <= actual_metrics["On-Time Delivery"], actual_metrics["On-Time Delivery"], actual_metrics["OTIF"])
    add("semantic::OTIF not above complete-order", actual_metrics["OTIF"] <= actual_metrics["Complete Order Rate"], actual_metrics["Complete Order Rate"], actual_metrics["OTIF"])
    add("grain::order_service_detail unique", detail["order_id"].is_unique, len(detail), detail["order_id"].nunique())
    add("semantic::row OTIF components", bool((detail["otif"] == (detail["on_time"] & detail["in_full"])).all()), True, bool((detail["otif"] == (detail["on_time"] & detail["in_full"])).all()))

    carrier_expected = detail.groupby("carrier", as_index=False).agg(
        order_count=("order_id", "nunique"), on_time_rate=("on_time", "mean"),
        otif_rate=("otif", "mean"), avg_delay_days=("delivery_delay_days", "mean"),
        freight_cost=("freight_cost", "sum"), shipment_weight_kg=("shipment_weight_kg", "sum"),
    )
    carrier_expected["freight_cost_per_kg"] = carrier_expected["freight_cost"] / carrier_expected["shipment_weight_kg"]
    carrier_expected["otif_rank"] = carrier_expected["otif_rate"].rank(method="dense", ascending=False).astype(int)
    carrier_actual = pd.read_csv(DATA / "carrier_scorecard.csv")
    carrier_cols = ["order_count", "on_time_rate", "otif_rate", "avg_delay_days", "freight_cost", "shipment_weight_kg", "freight_cost_per_kg", "otif_rank"]
    passed, diff = _frame_close(carrier_actual, carrier_expected, ["carrier"], carrier_cols)
    add("extract::carrier_scorecard reconciles", passed, 0.0, diff)

    warehouse_expected = detail.groupby("warehouse", as_index=False).agg(
        order_count=("order_id", "nunique"), revenue=("revenue", "sum"),
        logistics_cost=("logistics_cost", "sum"), otif_rate=("otif", "mean"),
        on_time_rate=("on_time", "mean"), units_ordered=("units_ordered", "sum"),
        units_shipped=("units_shipped", "sum"),
    )
    warehouse_expected["fill_rate"] = warehouse_expected["units_shipped"] / warehouse_expected["units_ordered"]
    warehouse_expected = warehouse_expected.drop(columns=["units_ordered", "units_shipped"])
    warehouse_actual = pd.read_csv(DATA / "warehouse_scorecard.csv")
    warehouse_cols = ["order_count", "revenue", "logistics_cost", "otif_rate", "on_time_rate", "fill_rate"]
    passed, diff = _frame_close(warehouse_actual, warehouse_expected, ["warehouse"], warehouse_cols)
    add("extract::warehouse_scorecard reconciles", passed, 0.0, diff)

    customer_expected = detail.groupby("customer_id", as_index=False).agg(
        order_count=("order_id", "nunique"), revenue=("revenue", "sum"),
        logistics_cost=("logistics_cost", "sum"), otif_rate=("otif", "mean"),
        units_ordered=("units_ordered", "sum"), units_shipped=("units_shipped", "sum"),
    )
    customer_expected["unit_fill_rate"] = customer_expected["units_shipped"] / customer_expected["units_ordered"]
    customer_expected["cost_to_revenue_ratio"] = customer_expected["logistics_cost"] / customer_expected["revenue"]
    customer_expected = customer_expected.drop(columns=["units_ordered", "units_shipped"])
    customer_actual = pd.read_csv(DATA / "customer_service_cost_mart.csv")
    customer_cols = ["order_count", "revenue", "logistics_cost", "otif_rate", "unit_fill_rate", "cost_to_revenue_ratio"]
    passed, diff = _frame_close(customer_actual, customer_expected, ["customer_id"], customer_cols)
    add("extract::customer_service_cost reconciles", passed, 0.0, diff)

    daily = pd.read_csv(DATA / "daily_service_metrics.csv")
    daily["weighted_30d_expected"] = daily["otif_order_count"].rolling(30, min_periods=1).sum() / daily["order_count"].rolling(30, min_periods=1).sum()
    max_diff = float((daily["rolling_30d_otif"] - daily["weighted_30d_expected"]).abs().max())
    add("semantic::rolling 30-day OTIF weighted", max_diff < TOLERANCE, 0.0, max_diff)
    rev_diff = float((daily["rolling_30d_revenue"] - daily["revenue"].rolling(30, min_periods=1).sum()).abs().max())
    add("extract::rolling 30-day revenue reconciles", rev_diff < TOLERANCE, 0.0, rev_diff)
    add("grain::daily_service unique date", daily["order_date"].is_unique, len(daily), daily["order_date"].nunique())

    dq = pd.read_csv(DATA / "data_quality_report.csv")
    add("quality::all source checks pass", bool((dq["status"] == "PASS").all()), len(dq), int((dq["status"] == "PASS").sum()))

    lineage = (ROOT / "governance" / "metric_lineage.md").read_text(encoding="utf-8")
    for metric in ["Unit Fill Rate", "Complete Order Rate", "On-Time Delivery", "OTIF", "Freight Cost per kg", "Cost-to-Serve Ratio", "Rolling 30-Day OTIF"]:
        add(f"lineage::{metric}", metric in lineage, True, metric in lineage)
    return checks


def main() -> None:
    checks = validation_checks()
    output = pd.DataFrame(checks)
    output.to_csv(ROOT / "validation" / "bi_metric_validation_report.csv", index=False, lineterminator="\n")
    failed = output.loc[output["status"] != "PASS"]
    summary = {"checks": len(output), "failed": len(failed)}
    print(json.dumps(summary, indent=2))
    if not failed.empty:
        raise SystemExit(f"BI metric validation failed:\n{failed.to_string(index=False)}")


if __name__ == "__main__":
    main()
