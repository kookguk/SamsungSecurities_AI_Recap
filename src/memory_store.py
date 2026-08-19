from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MEMORY_PATH = ROOT / "memory" / "customer_memory.json"


def load_memories(path: Path = DEFAULT_MEMORY_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": "1.0", "customers": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_goal(
    customer_id: str,
    customer_name: str,
    goal: str,
    source: str = "remember_me_recap",
    path: Path = DEFAULT_MEMORY_PATH,
) -> dict[str, Any]:
    memory = load_memories(path)
    previous = memory.setdefault("customers", {}).get(customer_id, {})
    entry = {
        **previous,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "goal_year": 2027,
        "selected_goal": goal,
        "source": source,
        "consent_scope": "crm_preference_demo",
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    memory["customers"][customer_id] = entry
    path.parent.mkdir(parents=True, exist_ok=True)

    handle, temp_name = tempfile.mkstemp(prefix="memory_", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            json.dump(memory, file, ensure_ascii=False, indent=2)
        Path(temp_name).replace(path)
    finally:
        temp_path = Path(temp_name)
        if temp_path.exists():
            temp_path.unlink()
    return entry


def selected_goal(customer_id: str, default: str, path: Path = DEFAULT_MEMORY_PATH) -> str:
    return load_memories(path).get("customers", {}).get(customer_id, {}).get("selected_goal", default)


def crm_card(customer: dict[str, Any], metrics: dict[str, Any], goal: str) -> dict[str, str]:
    name = customer["name"]
    if goal == "분산투자 이해하기":
        return {
            "eyebrow": "지난 목표를 기억했어요",
            "title": f"{name}님, 한 테마 밖의 기회도 살펴볼까요?",
            "body": f"지난해 {metrics['top_theme']} 매수 비중은 {metrics['top_theme_share']:.0f}%였어요. 자산배분 기초를 5분 콘텐츠로 확인해보세요.",
            "cta": "ETF 자산배분 시작하기",
            "tone": "mint",
            "icon": "🧩",
        }
    if goal == "절세 투자 공부하기":
        return {
            "eyebrow": "2027 목표 이어가기",
            "title": f"{name}님을 위한 ISA 첫 체크리스트",
            "body": f"{metrics['monthly_buy_months']}개월간 이어온 투자 루틴을 절세 계좌와 연결해볼 수 있어요. 구조부터 차근차근 알아보세요.",
            "cta": "ISA·연금 기본 가이드",
            "tone": "lavender",
            "icon": "🧾",
        }
    return {
        "eyebrow": "오늘의 투자 루틴",
        "title": f"{name}님, 오래 가져갈 기준을 정해볼까요?",
        "body": f"지난해 평균 보유기간은 {metrics['avg_holding_days']:.0f}일이었어요. 목표 기간을 정하는 작은 루틴부터 시작해보세요.",
        "cta": "나의 장기투자 루틴 만들기",
        "tone": "peach",
        "icon": "🌱",
    }

