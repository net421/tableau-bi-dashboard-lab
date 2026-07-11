from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tableau_ready_exports"
OUT = ROOT / "screenshots"


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    carrier = pd.read_csv(DATA / "carrier_scorecard.csv").sort_values("otif_rate")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(carrier["carrier"], carrier["otif_rate"])
    ax.set_title("Carrier OTIF Rate")
    ax.set_xlabel("OTIF rate")
    ax.set_xlim(0, 1)
    save(fig, "carrier_otif.png")

    customer = pd.read_csv(DATA / "customer_service_cost_mart.csv")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(customer["otif_rate"], customer["cost_to_revenue_ratio"], s=customer["order_count"] * 4, alpha=0.65)
    ax.set_title("Customer Service vs Cost-to-Serve")
    ax.set_xlabel("OTIF rate")
    ax.set_ylabel("Cost-to-revenue ratio")
    ax.set_xlim(0, 1)
    save(fig, "customer_cost_to_serve.png")

    daily = pd.read_csv(DATA / "daily_service_metrics.csv")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(pd.to_datetime(daily["order_date"]), daily["rolling_30d_otif"])
    ax.set_title("Weighted Rolling 30-Day OTIF")
    ax.set_xlabel("Order date")
    ax.set_ylabel("OTIF rate")
    ax.set_ylim(0, 1)
    save(fig, "rolling_30d_otif.png")
    print("Generated 3 dashboard evidence images")


if __name__ == "__main__":
    main()
