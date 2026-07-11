from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "tableau_ready_exports" / "order_service_detail.csv"
SEED = 4212026
ORDER_COUNT = 2400
CUSTOMERS = [f"C{i:04d}" for i in range(1, 181)]
WAREHOUSES = ["WH-CENTRAL", "WH-NORTH", "WH-SOUTH"]
CARRIERS = ["CarrierA", "CarrierB", "CarrierC", "CarrierD"]
START_DATE = date(2025, 1, 1)


def money(value: float) -> float:
    return round(value, 2)


def generate_rows() -> list[dict[str, object]]:
    rng = random.Random(SEED)
    rows: list[dict[str, object]] = []
    for index in range(1, ORDER_COUNT + 1):
        order_id = f"O{index:06d}"
        order_date = START_DATE + timedelta(days=rng.randrange(365))
        promised_date = order_date + timedelta(days=rng.randint(3, 8))
        units_ordered = rng.randint(8, 120)
        in_full = rng.random() < 0.86
        if in_full:
            units_shipped = units_ordered
        else:
            shortage = rng.randint(1, min(units_ordered, max(2, int(units_ordered * 0.18))))
            units_shipped = units_ordered - shortage
        on_time = rng.random() < 0.73
        delay_days = rng.choice([-2, -1, 0]) if on_time else rng.randint(1, 6)
        delivery_date = promised_date + timedelta(days=delay_days)
        otif = on_time and in_full

        unit_price = rng.uniform(35, 260)
        revenue = money(units_ordered * unit_price)
        shipment_weight_kg = round(units_shipped * rng.uniform(0.8, 7.5), 2)
        freight_rate = rng.uniform(0.35, 0.95)
        freight_cost = money((shipment_weight_kg * freight_rate) + rng.uniform(8, 45))
        handling_cost = money(units_shipped * rng.uniform(0.5, 2.1))
        exception_cost = money(0 if otif else rng.uniform(12, 160))
        logistics_cost = money(freight_cost + handling_cost + exception_cost)
        freight_cost_per_kg = round(freight_cost / shipment_weight_kg, 6) if shipment_weight_kg else 0.0

        rows.append({
            "order_id": order_id,
            "customer_id": rng.choice(CUSTOMERS),
            "warehouse": rng.choices(WAREHOUSES, weights=[0.42, 0.34, 0.24], k=1)[0],
            "order_date": order_date.isoformat(),
            "promised_date": promised_date.isoformat(),
            "units_ordered": units_ordered,
            "units_shipped": units_shipped,
            "revenue": revenue,
            "line_count": rng.randint(1, 5),
            "order_fill_rate": round(units_shipped / units_ordered, 6),
            "in_full": in_full,
            "shipment_id": f"S{index:06d}",
            "carrier": rng.choices(CARRIERS, weights=[0.30, 0.28, 0.24, 0.18], k=1)[0],
            "delivery_date": delivery_date.isoformat(),
            "freight_cost": freight_cost,
            "handling_cost": handling_cost,
            "exception_cost": exception_cost,
            "shipment_weight_kg": shipment_weight_kg,
            "on_time": on_time,
            "otif": otif,
            "logistics_cost": logistics_cost,
            "freight_cost_per_kg": freight_cost_per_kg,
            "delivery_delay_days": delay_days,
        })
    return rows


def main() -> None:
    rows = generate_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows):,} deterministic order-service rows at {OUTPUT}")


if __name__ == "__main__":
    main()
