from __future__ import annotations

import csv
import io
from collections import Counter
from typing import Any

from src.analytics import calculate_metrics
from src.data_loader import customer_slice, load_demo_data


ACTIVITY_COLUMNS = [
    "customer_id",
    "customer_name",
    "event_date",
    "event_type",
    "symbol",
    "asset_name",
    "market",
    "side",
    "quantity",
    "price",
    "theme",
    "content_type",
    "content_topic",
    "dwell_seconds",
    "completed",
]

EVENT_ALIASES = {
    "TRADE": "TRADE",
    "BUY": "TRADE",
    "SELL": "TRADE",
    "거래": "TRADE",
    "INTEREST": "INTEREST",
    "WATCH": "INTEREST",
    "WATCH_ADD": "INTEREST",
    "QUOTE_VIEW": "INTEREST",
    "RESEARCH_VIEW": "INTEREST",
    "관심": "INTEREST",
    "CONTENT": "CONTENT",
    "콘텐츠": "CONTENT",
}


def _decode(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "cp949", "utf-8"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("CSV 인코딩을 읽을 수 없습니다. UTF-8 또는 CP949로 저장해주세요.")


def _clean(row: dict[str, Any]) -> dict[str, str]:
    return {
        str(key).strip().lower(): "" if value is None else str(value).strip()
        for key, value in row.items()
        if key is not None
    }


def parse_activity_csv(raw: bytes, customer_name: str = "고객") -> dict[str, Any]:
    """Parse a unified activity CSV and return data compatible with analytics.py."""
    text = _decode(raw)
    if not text.strip():
        raise ValueError("CSV가 비어 있습니다.")
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",\t;")
    except csv.Error:
        dialect = csv.excel
    rows = [_clean(row) for row in csv.DictReader(io.StringIO(text), dialect=dialect)]
    rows = [row for row in rows if any(row.values())]
    if not rows:
        raise ValueError("헤더 아래에 활동 데이터가 없습니다.")

    # 기존 trades.csv도 바로 업로드할 수 있도록 호환합니다.
    legacy_trade = "trade_date" in rows[0] and "event_type" not in rows[0]
    if not legacy_trade and "event_date" not in rows[0]:
        raise ValueError("필수 열 event_date가 없습니다. 샘플 CSV 형식을 확인해주세요.")

    trades: list[dict[str, str]] = []
    interests: list[dict[str, str]] = []
    content: list[dict[str, str]] = []
    skipped = 0

    for index, row in enumerate(rows, start=2):
        event_date = row.get("event_date") or row.get("trade_date", "")
        raw_type = "TRADE" if legacy_trade else row.get("event_type", "").upper()
        event_type = EVENT_ALIASES.get(raw_type, raw_type)
        if not event_date:
            skipped += 1
            continue
        try:
            if event_type == "TRADE":
                side = (row.get("side") or raw_type).upper()
                if side not in {"BUY", "SELL"}:
                    raise ValueError(f"{index}행의 side는 BUY 또는 SELL이어야 합니다.")
                for field in ("symbol", "quantity", "price"):
                    if not row.get(field):
                        raise ValueError(f"{index}행 거래에 {field} 값이 없습니다.")
                float(row["quantity"])
                float(row["price"])
                trades.append(
                    {
                        "trade_date": event_date,
                        "symbol": row["symbol"],
                        "asset_name": row.get("asset_name") or row["symbol"],
                        "market": row.get("market") or "기타",
                        "side": side,
                        "quantity": row["quantity"],
                        "price": row["price"],
                        "theme": row.get("theme") or "기타",
                    }
                )
            elif event_type == "INTEREST":
                interests.append(
                    {
                        "event_date": event_date,
                        "event_type": raw_type or "INTEREST",
                        "symbol": row.get("symbol") or "-",
                        "market": row.get("market") or "기타",
                        "theme": row.get("theme") or "기타",
                    }
                )
            elif event_type == "CONTENT":
                dwell = row.get("dwell_seconds") or "0"
                int(float(dwell))
                content.append(
                    {
                        "event_date": event_date,
                        "content_id": row.get("content_id") or f"UP-{index}",
                        "content_type": row.get("content_type") or "콘텐츠",
                        "topic": row.get("content_topic") or row.get("topic") or "기타",
                        "dwell_seconds": str(int(float(dwell))),
                        "completed": (row.get("completed") or "false").lower(),
                    }
                )
            else:
                skipped += 1
        except ValueError:
            raise
        except Exception as error:
            raise ValueError(f"{index}행을 처리할 수 없습니다: {error}") from error

    if not trades:
        raise ValueError("투자 행동을 계산하려면 TRADE 이벤트가 1개 이상 필요합니다.")

    first = rows[0]
    resolved_name = first.get("customer_name") or customer_name or "고객"
    customer_id = first.get("customer_id") or "UPLOAD-001"
    data = {
        "customer": {"customer_id": customer_id, "name": resolved_name},
        "trades": trades,
        "interests": interests,
        "content": content,
        "market_events": [
            {
                "event_id": "MKT-2026-APR",
                "name": "4월 글로벌 기술주 급락",
                "start_date": "2026-04-07",
                "end_date": "2026-04-10",
                "market_drop_pct": -8.4,
            }
        ],
    }
    metrics = calculate_metrics(data)
    metrics.update(_activity_summary(data))
    return {
        "customer": data["customer"],
        "metrics": metrics,
        "data": data,
        "row_count": len(rows),
        "skipped_count": skipped,
    }


def _activity_summary(data: dict[str, Any]) -> dict[str, Any]:
    trades = data["trades"]
    interests = data["interests"]
    symbol_counts = Counter(row["symbol"] for row in trades)
    symbol_names = {row["symbol"]: row["asset_name"] for row in trades}
    market_counts = Counter(row["market"] for row in trades + interests)
    top_symbol = symbol_counts.most_common(1)[0][0]
    dates = sorted(row["trade_date"] for row in trades)
    return {
        "top_symbol": top_symbol,
        "top_asset_name": symbol_names[top_symbol],
        "top_symbol_meetings": symbol_counts[top_symbol],
        "top_market": market_counts.most_common(1)[0][0] if market_counts else "기타",
        "analysis_period": f"{dates[0]} ~ {dates[-1]}",
        "interest_event_count": len(interests),
        "content_event_count": len(data["content"]),
    }


def sample_activity_csv(customer_id: str) -> bytes:
    data = load_demo_data()
    sliced = customer_slice(data, customer_id)
    customer = sliced["customer"]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=ACTIVITY_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in sliced["trades"]:
        writer.writerow(
            {
                "customer_id": customer_id,
                "customer_name": customer["name"],
                "event_date": row["trade_date"],
                "event_type": "TRADE",
                "symbol": row["symbol"],
                "asset_name": row["asset_name"],
                "market": row["market"],
                "side": row["side"],
                "quantity": row["quantity"],
                "price": row["price"],
                "theme": row["theme"],
            }
        )
    for row in sliced["interests"]:
        writer.writerow(
            {
                "customer_id": customer_id,
                "customer_name": customer["name"],
                "event_date": row["event_date"],
                "event_type": row["event_type"],
                "symbol": row["symbol"],
                "market": row["market"],
                "theme": row["theme"],
            }
        )
    for row in sliced["content"]:
        writer.writerow(
            {
                "customer_id": customer_id,
                "customer_name": customer["name"],
                "event_date": row["event_date"],
                "event_type": "CONTENT",
                "content_type": row["content_type"],
                "content_topic": row["topic"],
                "dwell_seconds": row["dwell_seconds"],
                "completed": row["completed"],
            }
        )
    return buffer.getvalue().encode("utf-8-sig")


def blank_template_csv() -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=ACTIVITY_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerow(
        {
            "customer_id": "C001",
            "customer_name": "김고객",
            "event_date": "2026-01-10",
            "event_type": "TRADE",
            "symbol": "005930",
            "asset_name": "삼성전자",
            "market": "국내",
            "side": "BUY",
            "quantity": "10",
            "price": "80000",
            "theme": "AI·반도체",
        }
    )
    return buffer.getvalue().encode("utf-8-sig")

