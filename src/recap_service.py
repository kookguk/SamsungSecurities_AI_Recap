from __future__ import annotations

import json
import os
from typing import Any


RECAP_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "pattern_name": {"type": "string"},
        "headline": {"type": "string"},
        "story": {"type": "string"},
        "strength": {"type": "string"},
        "watchout": {"type": "string"},
        "recommended_goal": {"type": "string"},
    },
    "required": ["pattern_name", "headline", "story", "strength", "watchout", "recommended_goal"],
}


FALLBACKS = {
    "C001": {
        "pattern_name": "집중해서 파고드는 테마 탐험가",
        "headline": "AI·반도체를 깊게 본 한 해",
        "story": "준호님은 AI·반도체 종목을 가장 자주 살펴보고 매수했어요. 시장이 크게 흔들린 4월에도 보유를 유지하며 일부 분할 매수했고, 관심 콘텐츠 역시 반도체 리서치에 모였습니다.",
        "strength": "관심 분야를 꾸준히 학습하고 변동 구간에서도 계획을 유지했어요.",
        "watchout": "한 테마의 비중이 높아 시장 변화가 자산 전체에 크게 반영될 수 있어요.",
        "recommended_goal": "분산투자 이해하기",
    },
    "C002": {
        "pattern_name": "꾸준함을 쌓는 루틴 메이커",
        "headline": "매달 이어간 ETF 투자 루틴",
        "story": "서연님은 글로벌 ETF와 연금 콘텐츠를 중심으로 투자 루틴을 이어갔어요. 급락기에도 매도를 서두르지 않았고, 10개월에 걸친 분산 매수로 일관된 장기 행동을 만들었습니다.",
        "strength": "시장 소음보다 정해둔 주기에 맞춰 행동하는 일관성이 돋보였어요.",
        "watchout": "장기 루틴을 유지하되 계좌별 세제 혜택과 자산 배분을 함께 점검할 여지가 있어요.",
        "recommended_goal": "절세 투자 공부하기",
    },
    "C003": {
        "pattern_name": "변화에 빠르게 반응하는 타이밍 서퍼",
        "headline": "뉴스와 가격 변화에 민감했던 한 해",
        "story": "민수님은 시장 뉴스와 급등락 종목을 빠르게 확인하고 짧게 보유하는 거래가 많았어요. 4월 급락 구간에는 보유 비중을 줄였고, 이후 반등 종목을 다시 탐색하는 행동이 이어졌습니다.",
        "strength": "새로운 이슈를 빠르게 발견하고 실행으로 옮기는 민첩성이 있었어요.",
        "watchout": "짧은 판단이 반복되면 처음 세운 투자 기준보다 시장 움직임에 더 크게 흔들릴 수 있어요.",
        "recommended_goal": "장기투자 습관 만들기",
    },
}


def get_api_key(session_key: str | None = None, secrets: Any | None = None) -> str | None:
    if session_key:
        return session_key.strip()
    if secrets is not None:
        try:
            value = secrets.get("OPENAI_API_KEY")
            if value:
                return str(value).strip()
        except Exception:
            pass
    return os.getenv("OPENAI_API_KEY")


def get_model(secrets: Any | None = None) -> str:
    if secrets is not None:
        try:
            value = secrets.get("OPENAI_MODEL")
            if value:
                return str(value)
        except Exception:
            pass
    return os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def generate_recap(
    customer: dict[str, Any],
    metrics: dict[str, Any],
    api_key: str,
    model: str,
) -> dict[str, str]:
    """Generate a grounded Korean recap using the OpenAI Responses API."""
    from openai import OpenAI

    allowed_goals = customer["goal_options"]
    facts = {
        "customer_name": customer["name"],
        "metrics": metrics,
        "allowed_goals": allowed_goals,
    }
    instructions = (
        "당신은 증권사의 투자행동 리캡 에디터다. 제공된 사실만 사용해 한국어로 작성한다. "
        "수익률 예측, 종목 추천, 매수·매도 지시, 성향 단정은 금지한다. 고객을 평가하지 말고 "
        "과거 행동을 비추는 거울처럼 친절하게 설명한다. 수치 근거를 최소 2개 포함한다. "
        "watchout도 비판이 아닌 점검 포인트로 표현한다. recommended_goal은 allowed_goals 중 하나만 고른다. "
        "pattern_name은 18자 이내, headline은 24자 이내, story는 3문장 이내로 작성한다."
    )
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=json.dumps(facts, ensure_ascii=False, default=str),
        text={
            "format": {
                "type": "json_schema",
                "name": "investment_recap",
                "strict": True,
                "schema": RECAP_SCHEMA,
            }
        },
    )
    result = json.loads(response.output_text)
    if result["recommended_goal"] not in allowed_goals:
        result["recommended_goal"] = FALLBACKS[customer["customer_id"]]["recommended_goal"]
    return result


def fallback_recap(customer_id: str) -> dict[str, str]:
    return dict(FALLBACKS[customer_id])

