from __future__ import annotations

import json
import os
from typing import Any


SLIDE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "sequence": {"type": "integer"},
        "kicker": {"type": "string"},
        "headline": {"type": "string"},
        "body": {"type": "string"},
        "evidence": {"type": "string"},
        "icon": {"type": "string", "enum": ["taste", "stock", "market", "pattern", "journey"]},
    },
    "required": ["sequence", "kicker", "headline", "body", "evidence", "icon"],
}

GOAL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "goal_id": {"type": "string"},
        "title": {"type": "string"},
        "reason": {"type": "string"},
        "first_step": {"type": "string"},
        "icon": {"type": "string", "enum": ["compass", "habit", "balance", "study", "shield", "calendar"]},
    },
    "required": ["goal_id", "title", "reason", "first_step", "icon"],
}

JOURNEY_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "recap_title": {"type": "string"},
        "recap_subtitle": {"type": "string"},
        "analysis_summary": {"type": "string"},
        "investor_word": {"type": "string"},
        "slides": {"type": "array", "minItems": 5, "maxItems": 5, "items": SLIDE_SCHEMA},
        "goals": {"type": "array", "minItems": 3, "maxItems": 3, "items": GOAL_SCHEMA},
    },
    "required": ["recap_title", "recap_subtitle", "analysis_summary", "investor_word", "slides", "goals"],
}

CONTENT_CARD_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "category": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "cta": {"type": "string"},
        "icon": {"type": "string", "enum": ["report", "lesson", "market", "etf", "tax", "routine"]},
    },
    "required": ["category", "title", "description", "cta", "icon"],
}

MYPICK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "popup_title": {"type": "string"},
        "popup_body": {"type": "string"},
        "watch_title": {"type": "string"},
        "watch_symbol": {"type": "string"},
        "watch_reason": {"type": "string"},
        "market_title": {"type": "string"},
        "market_body": {"type": "string"},
        "content_cards": {"type": "array", "minItems": 3, "maxItems": 3, "items": CONTENT_CARD_SCHEMA},
        "routine_title": {"type": "string"},
        "routine_body": {"type": "string"},
        "routine_frequency": {"type": "string"},
    },
    "required": [
        "popup_title",
        "popup_body",
        "watch_title",
        "watch_symbol",
        "watch_reason",
        "market_title",
        "market_body",
        "content_cards",
        "routine_title",
        "routine_body",
        "routine_frequency",
    ],
}


MYPICK_CATALOG = [
    {"category": "리서치", "title": "관심 테마 주간 리포트", "use": "관심 테마의 주요 변화를 정기적으로 확인"},
    {"category": "투자기초", "title": "ETF로 배우는 자산배분", "use": "테마 집중도를 낮추고 분산 원리를 학습"},
    {"category": "투자습관", "title": "나의 월간 투자 루틴", "use": "정해진 주기로 계획을 점검"},
    {"category": "시장읽기", "title": "변동성 장세 체크리스트", "use": "급등락 구간의 행동 기준 정리"},
    {"category": "연금·절세", "title": "ISA·연금 첫걸음", "use": "장기 목표와 계좌 활용법 학습"},
    {"category": "해외주식", "title": "미국시장 마감 브리핑", "use": "해외 관심시장 핵심 이슈 확인"},
    {"category": "리스크", "title": "투자 비중 셀프 점검", "use": "종목·테마별 편중을 스스로 확인"},
]


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


def _structured_response(
    *, api_key: str, model: str, instructions: str, payload: dict[str, Any], schema: dict[str, Any], name: str
) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=json.dumps(payload, ensure_ascii=False, default=str),
        text={"format": {"type": "json_schema", "name": name, "strict": True, "schema": schema}},
    )
    return json.loads(response.output_text)


def generate_journey(customer: dict[str, Any], metrics: dict[str, Any], api_key: str, model: str) -> dict[str, Any]:
    instructions = (
        "당신은 mPOP의 연말 Investment Recap 에디터이자 행동 데이터 분석가다. 입력은 Python이 검증·집계한 "
        "2026년 투자 활동 사실이다. 사실에 없는 수익률이나 인과관계를 만들지 않는다. 종목 추천, 가격 전망, "
        "매수·매도 지시는 금지한다. 고객을 평가하거나 투자성향을 확정하지 말고 과거 행동을 따뜻하고 세련된 "
        "2인칭 이야기로 바꾼다. slides는 정확히 5개이며 순서대로 ①투자의 취향 ②가장 자주 만난 종목 "
        "③시장 변동 순간의 선택 ④한 단어로 표현한 패턴 ⑤내년으로 이어지는 여정을 다룬다. 각 headline은 "
        "22자 이내의 감성 카피, body는 2문장 이내, evidence는 입력 수치를 짧게 표시한다. investor_word는 "
        "긍정적이고 중립적인 한국어 명사 1개다. goals는 사전 정의 목록에서 고르는 것이 아니라 Recap을 근거로 "
        "새롭게 추천하는 서로 다른 목표 3개다. 목표는 18자 이내로 측정·실천 가능해야 하며 상품 가입이나 "
        "특정 종목 거래를 유도하지 않는다. goal_id는 goal_1, goal_2, goal_3으로 작성한다."
    )
    return _structured_response(
        api_key=api_key,
        model=model,
        instructions=instructions,
        payload={"customer": customer, "verified_metrics": metrics},
        schema=JOURNEY_SCHEMA,
        name="investment_recap_journey",
    )


def generate_mypick_plan(
    customer: dict[str, Any], metrics: dict[str, Any], journey: dict[str, Any], goal: dict[str, Any], api_key: str, model: str
) -> dict[str, Any]:
    instructions = (
        "당신은 mPOP my PICK 개인화 편집자다. 고객의 검증된 과거 행동, Recap, 고객이 직접 선택한 2027 목표를 "
        "연결해 my PICK 페이지 구성을 만든다. 제공된 콘텐츠 카탈로그 안에서 가장 적합한 3개 모듈을 선택해 "
        "고객 언어로 재작성한다. watch 항목은 고객이 이미 거래하거나 관심을 보인 top_symbol만 사용하고 신규 종목을 "
        "추천하지 않는다. 최신 시세·뉴스를 아는 척하지 않으며, 매수·매도·수익 보장 표현을 금지한다. 팝업은 "
        "'새롭게 업데이트된 my PICK을 확인해볼까요?'라는 의미를 담되 고객의 목표와 연결해 2문장 이내로 쓴다. "
        "모든 문구는 짧고 모바일 화면에 적합하게 작성한다."
    )
    return _structured_response(
        api_key=api_key,
        model=model,
        instructions=instructions,
        payload={
            "customer": customer,
            "verified_metrics": metrics,
            "recap": journey,
            "selected_goal": goal,
            "available_mypick_catalog": MYPICK_CATALOG,
        },
        schema=MYPICK_SCHEMA,
        name="mypick_personalization",
    )


def fallback_journey(customer: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    name = customer["name"]
    top_theme = metrics["top_theme"]
    top_asset = metrics["top_asset_name"]
    word = "탐색" if metrics["top_theme_share"] >= 60 else "리듬"
    crash = metrics["crash"]["label"]
    slides = [
        {
            "sequence": 1,
            "kicker": "나의 투자 취향",
            "headline": "올해 투자에도 취향이 있었습니다",
            "body": f"{name}님은 수많은 선택 속에서 {top_theme} 테마를 가장 오래 바라봤어요.",
            "evidence": f"상위 테마 비중 {metrics['top_theme_share']:.0f}%",
            "icon": "taste",
        },
        {
            "sequence": 2,
            "kicker": "가장 자주 만난 이름",
            "headline": f"올해의 익숙한 이름, {top_asset}",
            "body": "매수와 매도, 관심 조회까지 반복해서 마주한 종목은 올해의 투자 관심을 보여줍니다.",
            "evidence": f"{metrics['top_symbol_meetings']}회 거래 기록",
            "icon": "stock",
        },
        {
            "sequence": 3,
            "kicker": "시장이 움직인 순간",
            "headline": "그 순간에도 나만의 선택이 있었습니다",
            "body": f"4월 시장이 크게 흔들린 구간에서 {crash} 행동이 관찰됐어요.",
            "evidence": "동일 시장 −8.4% 관찰 구간",
            "icon": "market",
        },
        {
            "sequence": 4,
            "kicker": "AI가 찾은 한 단어",
            "headline": f"2026년의 투자는 ‘{word}’",
            "body": f"평균 {metrics['avg_holding_days']:.0f}일의 보유기간과 {metrics['monthly_buy_months']}개월의 매수 기록에서 반복된 리듬을 찾았어요.",
            "evidence": f"활동일 {metrics['active_days']}일",
            "icon": "pattern",
        },
        {
            "sequence": 5,
            "kicker": "NEXT 2027",
            "headline": "기록은 끝나도 여정은 계속됩니다",
            "body": "올해의 행동을 바탕으로 지금의 나에게 어울리는 다음 목표를 준비했어요.",
            "evidence": "Recap 기반 목표 3개 생성",
            "icon": "journey",
        },
    ]
    concentrated_theme = metrics["top_theme_share"] >= 60 and metrics["top_theme"] not in {"글로벌분산", "자산배분", "채권"}
    if concentrated_theme:
        goals = [
            ("한 달 한 번 비중 점검", "집중된 테마 비중을 정기적으로 확인해요.", "월말에 테마별 비중을 기록하기", "balance"),
            ("분기마다 새 테마 공부", "익숙한 영역 밖의 투자 언어를 넓혀요.", "분기별 기초 콘텐츠 1개 완주하기", "study"),
            ("급락기 행동 기준 만들기", "변동 순간의 선택을 미리 정리해요.", "나만의 3가지 체크리스트 쓰기", "shield"),
        ]
    elif metrics["avg_holding_days"] < 60:
        goals = [
            ("90일 보유 기준 세우기", "짧은 판단 전에 목표 기간을 먼저 정해요.", "거래 전 보유 목표일 기록하기", "calendar"),
            ("뉴스 확인 횟수 줄이기", "시장 소음과 나의 기준을 분리해요.", "시황 확인 시간을 하루 2회로 정하기", "habit"),
            ("월간 투자 복기 남기기", "반복된 선택을 한 달 단위로 돌아봐요.", "월말에 잘한 점과 아쉬운 점 쓰기", "study"),
        ]
    else:
        goals = [
            ("투자 루틴 12개월 잇기", "올해의 꾸준한 리듬을 내년에도 이어가요.", "월 1회 투자 점검일 지정하기", "habit"),
            ("계좌별 목적 구분하기", "장기 목표에 맞게 자금의 역할을 나눠봐요.", "계좌별 목표를 한 문장으로 쓰기", "compass"),
            ("분기별 자산배분 점검", "꾸준함에 정기적인 균형 점검을 더해요.", "분기 말 비중 변화 확인하기", "balance"),
        ]
    return {
        "recap_title": f"{name}님의 한 해 투자기록이 도착했어요!",
        "recap_subtitle": "2026년의 선택을 AI가 하나의 이야기로 엮었습니다.",
        "analysis_summary": f"{top_theme} 관심과 {metrics['avg_holding_days']:.0f}일 평균 보유 리듬이 함께 관찰됐습니다.",
        "investor_word": word,
        "slides": slides,
        "goals": [
            {"goal_id": f"goal_{idx}", "title": title, "reason": reason, "first_step": step, "icon": icon}
            for idx, (title, reason, step, icon) in enumerate(goals, start=1)
        ],
    }


def fallback_mypick(
    customer: dict[str, Any], metrics: dict[str, Any], journey: dict[str, Any], goal: dict[str, Any]
) -> dict[str, Any]:
    name = customer["name"]
    top_asset = metrics["top_asset_name"]
    top_symbol = metrics["top_symbol"]
    goal_title = goal["title"]
    return {
        "popup_title": "새롭게 업데이트된 my PICK을 확인해볼까요?",
        "popup_body": f"{name}님의 Recap과 ‘{goal_title}’ 목표를 반영해 관심 정보와 투자 콘텐츠를 새로 구성했어요.",
        "watch_title": top_asset,
        "watch_symbol": top_symbol,
        "watch_reason": "올해 가장 자주 만난 종목의 새로운 리서치를 이어서 확인할 수 있어요.",
        "market_title": f"{metrics['top_market']} 시장, 오늘은 무엇을 봐야 할까요?",
        "market_body": f"지난해 관심이 높았던 {metrics['top_theme']} 테마와 시장 변동성 콘텐츠를 우선 배치했어요.",
        "content_cards": [
            {
                "category": "목표 맞춤",
                "title": goal_title,
                "description": goal["first_step"],
                "cta": "첫 단계 시작하기",
                "icon": "routine",
            },
            {
                "category": "투자기초",
                "title": "ETF로 배우는 자산배분",
                "description": "내 포트폴리오의 테마별 비중을 이해하는 기초 콘텐츠예요.",
                "cta": "5분 콘텐츠 보기",
                "icon": "etf",
            },
            {
                "category": "시장읽기",
                "title": "변동성 장세 체크리스트",
                "description": "시장이 흔들릴 때 확인할 기준을 미리 정리해보세요.",
                "cta": "체크리스트 열기",
                "icon": "market",
            },
        ],
        "routine_title": f"‘{goal_title}’을 위한 월간 체크인",
        "routine_body": "Recap에서 찾은 행동 변화를 한 달에 한 번 가볍게 돌아봅니다.",
        "routine_frequency": "매월 마지막 영업일",
    }
