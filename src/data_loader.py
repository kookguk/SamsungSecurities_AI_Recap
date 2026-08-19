from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def _read_csv(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _read_json(name: str) -> Any:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def load_demo_data() -> dict[str, Any]:
    """Load all synthetic datasets used by the demo."""
    return {
        "customers": _read_json("customers.json"),
        "trades": _read_csv("trades.csv"),
        "interests": _read_csv("interest_events.csv"),
        "content": _read_csv("content_events.csv"),
        "market_events": _read_json("market_events.json"),
    }


def customer_slice(data: dict[str, Any], customer_id: str) -> dict[str, Any]:
    customer = next(item for item in data["customers"] if item["customer_id"] == customer_id)
    return {
        "customer": customer,
        "trades": [row for row in data["trades"] if row["customer_id"] == customer_id],
        "interests": [row for row in data["interests"] if row["customer_id"] == customer_id],
        "content": [row for row in data["content"] if row["customer_id"] == customer_id],
        "market_events": data["market_events"],
    }

