from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tableau_ready_exports"
DETAIL_PATH = DATA / "order_service_detail.csv"

REQUIRED_COLUMNS = {
    "order_id", "customer_id", "warehouse", "order_date", "promised_date",
    "units_ordered", "units_shipped", "revenue", "line_count",
    "order_fill_rate", "in_full", "shipment_id", "carrier", "delivery_date",
    "freight_cost", "handling_cost", "exception_cost", "shipment_weight_kg",
    "on_time", "otif", "logistics_cost", "freight_cost_per_kg",
    "delivery_delay_days",
}


def _bool_series(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.astype(bool)
    mapped = series.astype(str).str.strip().str.lower().map({"true": True, "false": False, "1": True, "0": False})
    if mapped.isna().any():
        bad = sorted(series[mapped.isna()].astype(str).unique())
        raise ValueError(f"Invalid boolean values: {bad}")
    return mapped.astype(bool)


def _write(df: pd.DataFrame, name: str) -> None:
    df.to_csv(DATA / name, index=False, lineterminator="\n", float_format="%.12f")


def load_detail() -> pd.DataFrame:
    detail = pd.read_csv(DETAIL_PATH)
    missing = sorted(REQUIRED_COLUMNS - set(detail.columns))
    if missing:
        raise ValueError(f"order_service_detail.csv missing columns: {missing}")
    if detail["order_id"].duplicated().any():
        raise ValueError("order_service_detail.csv must be one row per order_id")
    for column in ["in_full", "on_time", "otif"]:
        detail[column] = _bool_series(detail[column])
    detail["order_date"] = pd.to_datetime(detail["order_date"], errors="raise")
    detail["promised_date"] = pd.to_datetime(detail["promised_date"], errors="raise")
    detail["delivery_date"] = pd.to_datetime(detail["delivery_date"], errors="raise")
    return detail.sort_values("order_id").reset_index(drop=True)


def build_executive_kpis(detail: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        ("Unit Fill Rate", detail["units_shipped"].sum() / detail["units_ordered"].sum(), "percent"),
        ("Complete Order Rate", detail["in_full"].mean(), "percent"),
        ("On-Time Delivery", detail["on_time"].mean(), "percent"),
        ("OTIF", detail["otif"].mean(), "percent"),
        ("Revenue", detail["revenue"].sum(), "currency"),
        ("Logistics Cost", detail["logistics_cost"].sum(), "currency"),
        ("Freight Cost per kg", detail["freight_cost"].sum() / detail["shipment_weight_kg"].sum(), "currency"),
        ("Average Delay Days", detail["delivery_delay_days"].mean(), "number"),
    ]
    return pd.DataFrame(metrics, columns=["metric_name", "metric_value", "format_type"])


def build_carrier_scorecard(detail: pd.DataFrame) -> pd.DataFrame:
    result = detail.groupby("carrier", as_index=False).agg(
        order_count=("order_id", "nunique"),
        on_time_rate=("on_time", "mean"),
        otif_rate=("otif", "mean"),
        avg_delay_days=("delivery_delay_days", "mean"),
        freight_cost=("freight_cost", "sum"),
        shipment_weight_kg=("shipment_weight_kg", "sum"),
    )
    result["freight_cost_per_kg"] = result["freight_cost"] / result["shipment_weight_kg"]
    result["otif_rank"] = result["otif_rate"].rank(method="dense", ascending=False).astype(int)
    return result.sort_values(["otif_rank", "carrier"]).reset_index(drop=True)


def build_warehouse_scorecard(detail: pd.DataFrame) -> pd.DataFrame:
    result = detail.groupby("warehouse", as_index=False).agg(
        order_count=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        logistics_cost=("logistics_cost", "sum"),
        otif_rate=("otif", "mean"),
        on_time_rate=("on_time", "mean"),
        units_ordered=("units_ordered", "sum"),
        units_shipped=("units_shipped", "sum"),
    )
    result["fill_rate"] = result["units_shipped"] / result["units_ordered"]
    return result.drop(columns=["units_ordered", "units_shipped"]).sort_values("warehouse").reset_index(drop=True)


def build_customer_service_cost(detail: pd.DataFrame) -> pd.DataFrame:
    result = detail.groupby("customer_id", as_index=False).agg(
        order_count=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        logistics_cost=("logistics_cost", "sum"),
        otif_rate=("otif", "mean"),
        units_ordered=("units_ordered", "sum"),
        units_shipped=("units_shipped", "sum"),
    )
    result["unit_fill_rate"] = result["units_shipped"] / result["units_ordered"]
    result["cost_to_revenue_ratio"] = result["logistics_cost"] / result["revenue"].where(result["revenue"] != 0)
    return result.drop(columns=["units_ordered", "units_shipped"]).sort_values("customer_id").reset_index(drop=True)


def build_daily_service(detail: pd.DataFrame) -> pd.DataFrame:
    result = detail.groupby("order_date", as_index=False).agg(
        order_count=("order_id", "nunique"),
        units_ordered=("units_ordered", "sum"),
        units_shipped=("units_shipped", "sum"),
        revenue=("revenue", "sum"),
        on_time_order_count=("on_time", "sum"),
        complete_order_count=("in_full", "sum"),
        otif_order_count=("otif", "sum"),
        logistics_cost=("logistics_cost", "sum"),
    ).sort_values("order_date").reset_index(drop=True)
    result["on_time_rate"] = result["on_time_order_count"] / result["order_count"]
    result["complete_order_rate"] = result["complete_order_count"] / result["order_count"]
    result["otif_rate"] = result["otif_order_count"] / result["order_count"]
    result["unit_fill_rate"] = result["units_shipped"] / result["units_ordered"]
    rolling_orders = result["order_count"].rolling(30, min_periods=1).sum()
    rolling_otif_orders = result["otif_order_count"].rolling(30, min_periods=1).sum()
    result["rolling_30d_otif"] = rolling_otif_orders / rolling_orders
    result["rolling_30d_revenue"] = result["revenue"].rolling(30, min_periods=1).sum()
    result["order_date"] = result["order_date"].dt.strftime("%Y-%m-%d")
    columns = [
        "order_date", "order_count", "units_ordered", "units_shipped", "revenue",
        "on_time_order_count", "complete_order_count", "otif_order_count",
        "on_time_rate", "complete_order_rate", "otif_rate", "logistics_cost",
        "unit_fill_rate", "rolling_30d_otif", "rolling_30d_revenue",
    ]
    return result[columns]


def build_data_quality_report(detail: pd.DataFrame) -> pd.DataFrame:
    numeric_nonnegative = [
        "units_ordered", "units_shipped", "revenue", "freight_cost",
        "handling_cost", "exception_cost", "shipment_weight_kg", "logistics_cost",
    ]
    checks = [
        ("detail_row_count_positive", len(detail) > 0, f"rows={len(detail)}"),
        ("order_id_unique", detail["order_id"].is_unique, f"unique={detail['order_id'].nunique()}"),
        ("required_columns_complete", REQUIRED_COLUMNS.issubset(detail.columns), f"columns={len(detail.columns)}"),
        ("required_values_not_null", not detail[list(REQUIRED_COLUMNS)].isna().any().any(), "required fields checked"),
        ("numeric_values_nonnegative", not (detail[numeric_nonnegative] < 0).any().any(), "non-negative measures checked"),
        ("units_shipped_not_above_ordered", bool((detail["units_shipped"] <= detail["units_ordered"]).all()), "order quantity constraint"),
        ("order_fill_rate_range", bool(detail["order_fill_rate"].between(0, 1).all()), "0 <= rate <= 1"),
        ("otif_component_consistency", bool((detail["otif"] == (detail["on_time"] & detail["in_full"])).all()), "OTIF = on_time AND in_full"),
        ("delivery_not_before_order", bool((detail["delivery_date"] >= detail["order_date"]).all()), "delivery_date >= order_date"),
        ("shipment_weight_contract", bool(((detail["shipment_weight_kg"] >= 0) & ((detail["units_shipped"] == 0) | (detail["shipment_weight_kg"] > 0))).all()), "weight is non-negative and positive when units ship"),
        ("logistics_cost_reconciles", bool(((detail["freight_cost"] + detail["handling_cost"] + detail["exception_cost"] - detail["logistics_cost"]).abs() < 1e-8).all()), "freight + handling + exception"),
    ]
    return pd.DataFrame([
        {"check_name": name, "status": "PASS" if passed else "FAIL", "detail": detail_text}
        for name, passed, detail_text in checks
    ])


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    detail = load_detail()
    _write(build_executive_kpis(detail), "executive_kpis.csv")
    _write(build_carrier_scorecard(detail), "carrier_scorecard.csv")
    _write(build_warehouse_scorecard(detail), "warehouse_scorecard.csv")
    _write(build_customer_service_cost(detail), "customer_service_cost_mart.csv")
    _write(build_daily_service(detail), "daily_service_metrics.csv")
    _write(build_data_quality_report(detail), "data_quality_report.csv")
    print(f"Built governed BI exports from {len(detail):,} order-level rows")


if __name__ == "__main__":
    main()
