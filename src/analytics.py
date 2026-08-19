from __future__ import annotations

from collections import Counter, defaultdict, deque
from datetime import date, datetime
from typing import Any


YEAR_END = date(2026, 12, 31)


def _day(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _won(value: float) -> str:
    if value >= 100_000_000:
        return f"{value / 100_000_000:.1f}억원"
    if value >= 10_000:
        return f"{value / 10_000:.0f}만원"
    return f"{value:,.0f}원"


def _average_holding_days(trades: list[dict[str, str]]) -> float:
    """Quantity-weighted FIFO holding period, including positions open at year-end."""
    lots: dict[str, deque[list[Any]]] = defaultdict(deque)
    weighted_days = 0.0
    weighted_quantity = 0.0

    for row in sorted(trades, key=lambda item: (item["trade_date"], item["side"] == "BUY")):
        symbol = row["symbol"]
        quantity = float(row["quantity"])
        trade_day = _day(row["trade_date"])
        if row["side"] == "BUY":
            lots[symbol].append([quantity, trade_day])
            continue

        remaining = quantity
        while remaining > 0 and lots[symbol]:
            lot_quantity, bought = lots[symbol][0]
            matched = min(remaining, lot_quantity)
            weighted_days += max((trade_day - bought).days, 0) * matched
            weighted_quantity += matched
            lot_quantity -= matched
            remaining -= matched
            if lot_quantity <= 1e-9:
                lots[symbol].popleft()
            else:
                lots[symbol][0][0] = lot_quantity

    for queue in lots.values():
        for quantity, bought in queue:
            weighted_days += max((YEAR_END - bought).days, 0) * quantity
            weighted_quantity += quantity

    return round(weighted_days / weighted_quantity, 1) if weighted_quantity else 0.0


def _theme_stats(trades: list[dict[str, str]]) -> tuple[str, float, float, dict[str, float]]:
    theme_amounts: dict[str, float] = defaultdict(float)
    for row in trades:
        if row["side"] == "BUY":
            theme_amounts[row["theme"]] += float(row["quantity"]) * float(row["price"])
    total = sum(theme_amounts.values()) or 1.0
    shares = {theme: amount / total for theme, amount in theme_amounts.items()}
    top_theme = max(shares, key=shares.get) if shares else "-"
    hhi = sum(share**2 for share in shares.values())
    return top_theme, round(shares.get(top_theme, 0) * 100, 1), round(hhi * 100, 1), shares


def _crash_behavior(trades: list[dict[str, str]], events: list[dict[str, Any]]) -> dict[str, Any]:
    primary = events[0]
    start, end = _day(primary["start_date"]), _day(primary["end_date"])
    window = [row for row in trades if start <= _day(row["trade_date"]) <= end]
    buy = sum(float(row["quantity"]) * float(row["price"]) for row in window if row["side"] == "BUY")
    sell = sum(float(row["quantity"]) * float(row["price"]) for row in window if row["side"] == "SELL")
    if sell > buy * 1.3 and sell > 0:
        code, label = "reduced", "급락기에 비중 축소"
    elif buy > sell * 1.3 and buy > 0:
        code, label = "added", "급락기에 분할 매수"
    else:
        code, label = "held", "급락기에도 보유 유지"
    return {
        "event": primary["name"],
        "market_drop_pct": primary["market_drop_pct"],
        "code": code,
        "label": label,
        "buy_amount": round(buy),
        "sell_amount": round(sell),
        "activity_count": len(window),
    }


def _content_stats(content: list[dict[str, str]]) -> dict[str, Any]:
    seconds: dict[str, int] = defaultdict(int)
    completed: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    for row in content:
        seconds[row["topic"]] += int(row["dwell_seconds"])
        if row["completed"].lower() == "true":
            completed[row["topic"]] += 1
        formats[row["content_type"]] += 1
    top_topic = max(seconds, key=seconds.get) if seconds else "-"
    return {
        "top_topic": top_topic,
        "top_topic_minutes": round(seconds.get(top_topic, 0) / 60),
        "total_views": len(content),
        "completion_count": sum(completed.values()),
        "favorite_format": formats.most_common(1)[0][0] if formats else "-",
    }


def _interest_stats(interests: list[dict[str, str]]) -> dict[str, Any]:
    themes = Counter(row["theme"] for row in interests)
    markets = Counter(row["market"] for row in interests)
    symbols = Counter(row["symbol"] for row in interests)
    return {
        "top_theme": themes.most_common(1)[0][0] if themes else "-",
        "top_market": markets.most_common(1)[0][0] if markets else "-",
        "top_symbol": symbols.most_common(1)[0][0] if symbols else "-",
        "events": len(interests),
    }


def calculate_metrics(customer_data: dict[str, Any]) -> dict[str, Any]:
    trades = customer_data["trades"]
    buy_rows = [row for row in trades if row["side"] == "BUY"]
    sell_rows = [row for row in trades if row["side"] == "SELL"]
    buy_amount = sum(float(row["quantity"]) * float(row["price"]) for row in buy_rows)
    top_theme, top_share, hhi, theme_shares = _theme_stats(trades)
    active_days = len({row["trade_date"] for row in trades})
    monthly_buys = len({row["trade_date"][:7] for row in buy_rows})
    return {
        "active_days": active_days,
        "trade_count": len(trades),
        "buy_count": len(buy_rows),
        "sell_count": len(sell_rows),
        "buy_amount": round(buy_amount),
        "buy_amount_label": _won(buy_amount),
        "avg_holding_days": _average_holding_days(trades),
        "top_theme": top_theme,
        "top_theme_share": top_share,
        "theme_concentration_hhi": hhi,
        "theme_shares": theme_shares,
        "monthly_buy_months": monthly_buys,
        "crash": _crash_behavior(trades, customer_data["market_events"]),
        "content": _content_stats(customer_data["content"]),
        "interest": _interest_stats(customer_data["interests"]),
    }


def evidence_lines(metrics: dict[str, Any]) -> list[str]:
    crash = metrics["crash"]
    return [
        f"평균 보유기간 {metrics['avg_holding_days']:.0f}일",
        f"{metrics['top_theme']} 매수 비중 {metrics['top_theme_share']:.0f}%",
        f"시장 {abs(crash['market_drop_pct']):.1f}% 하락 구간: {crash['label']}",
        f"{metrics['content']['top_topic']} 콘텐츠 {metrics['content']['top_topic_minutes']}분 탐색",
    ]

