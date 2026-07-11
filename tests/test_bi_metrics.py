from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation"))

from validate_bi_metrics import calculate_metrics, validation_checks  # noqa: E402


def test_metric_ranges() -> None:
    metrics = calculate_metrics()
    for name in ["Unit Fill Rate", "Complete Order Rate", "On-Time Delivery", "OTIF"]:
        assert 0 <= metrics[name] <= 1


def test_otif_is_component_consistent() -> None:
    metrics = calculate_metrics()
    assert metrics["OTIF"] <= metrics["On-Time Delivery"]
    assert metrics["OTIF"] <= metrics["Complete Order Rate"]


def test_export_grain_is_one_row_per_order() -> None:
    detail = pd.read_csv(ROOT / "data/tableau_ready_exports/order_service_detail.csv")
    assert detail["order_id"].is_unique


def test_all_cross_extract_reconciliations_pass() -> None:
    failed = [check for check in validation_checks() if check["status"] != "PASS"]
    assert failed == []


def test_weighted_fill_rate_is_not_mean_of_order_ratios() -> None:
    detail = pd.read_csv(ROOT / "data/tableau_ready_exports/order_service_detail.csv")
    warehouse = pd.read_csv(ROOT / "data/tableau_ready_exports/warehouse_scorecard.csv").set_index("warehouse")
    for name, rows in detail.groupby("warehouse"):
        weighted = rows["units_shipped"].sum() / rows["units_ordered"].sum()
        assert abs(weighted - warehouse.loc[name, "fill_rate"]) < 1e-9


def test_rolling_otif_uses_order_weighting() -> None:
    daily = pd.read_csv(ROOT / "data/tableau_ready_exports/daily_service_metrics.csv")
    expected = daily["otif_order_count"].rolling(30, min_periods=1).sum() / daily["order_count"].rolling(30, min_periods=1).sum()
    assert (expected - daily["rolling_30d_otif"]).abs().max() < 1e-9
