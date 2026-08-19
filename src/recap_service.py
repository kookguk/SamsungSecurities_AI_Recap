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
        "content_focus": {"type": "string"},
        "icon": {"type": "string", "enum": ["compass", "habit", "balance", "study", "shield", "calendar"]},
    },
    "required": ["goal_id", "title", "reason", "content_focus", "icon"],
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
        "icon": {"type": "string", "enum": ["report", "news", "lesson", "market", "etf", "tax", "routine"]},
    },
    "required": ["category", "title", "description", "cta", "icon"],
}

MYPICK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "popup_title": {"type": "string"},
        "watch_title": {"type": "string"},
        "watch_symbol": {"type": "string"},
        "watch_reason": {"type": "string"},
        "market_title": {"type": "string"},
        "market_body": {"type": "string"},
        "content_cards": {"type": "array", "minItems": 3, "maxItems": 3, "items": CONTENT_CARD_SCHEMA},
        "update_title": {"type": "string"},
        "update_body": {"type": "string"},
        "update_frequency": {"type": "string"},
    },
    "required": [
        "popup_title",
        "watch_title",
        "watch_symbol",
        "watch_reason",
        "market_title",
        "market_body",
        "content_cards",
        "update_title",
        "update_body",
        "update_frequency",
    ],
}


MYPICK_CATALOG = [
    {"format": "리포트", "category": "AI·반도체", "title": "반도체 업황 주간 리포트", "use": "업황·수요·공급 변화와 핵심 기업 이슈 요약"},
    {"format": "뉴스", "category": "관심종목", "title": "내 종목 주요 뉴스", "use": "이미 관심을 보인 종목의 공시·실적·산업 뉴스 모음"},
    {"format": "리포트", "category": "ETF·분산", "title": "ETF 트렌드 리포트", "use": "테마 밖 시장과 자산군의 흐름 비교"},
    {"format": "시황", "category": "시장변동", "title": "변동성 장세 브리핑", "use": "급등락 배경과 시장 위험 요인 해설"},
    {"format": "뉴스", "category": "금리·채권", "title": "금리와 채권 이슈", "use": "중앙은행·금리·채권시장 주요 변화 요약"},
    {"format": "뉴스", "category": "연금·절세", "title": "ISA·연금 제도 업데이트", "use": "세제와 연금 관련 제도 변화 전달"},
    {"format": "시황", "category": "해외시장", "title": "미국시장 마감 브리핑", "use": "해외 관심시장의 핵심 지수와 산업 이슈 요약"},
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
        "새롭게 만드는 서로 다른 'AI 추천 목표' 3개다. 이 목표는 고객이 직접 수행할 행동 계획이 아니라 "
        "2027년 my PICK이 지속적으로 찾아서 우선 노출할 리포트·뉴스·시황의 주제를 뜻한다. title은 18자 이내로 "
        "'AI·반도체 흐름 깊이 보기', '시장 변동성 먼저 읽기'처럼 작성한다. 기록하기, 습관 만들기, 횟수 정하기 등 "
        "고객의 실행 과제를 목표로 추천하지 않는다. content_focus에는 my PICK에 연결할 구체적인 리포트·뉴스 유형을 "
        "한 문장으로 작성한다. 상품 가입이나 특정 종목 거래를 유도하지 않는다. goal_id는 goal_1, goal_2, goal_3이다."
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
        "연결해 my PICK 페이지 구성을 만든다. 선택한 목표의 content_focus를 최우선 기준으로 제공된 콘텐츠 카탈로그 "
        "안에서 가장 적합한 3개 모듈을 선택해 "
        "고객 언어로 재작성한다. 세 모듈에는 리포트와 뉴스가 각각 최소 1개 포함되어야 한다. watch 항목은 고객이 이미 거래하거나 관심을 보인 top_symbol만 사용하고 신규 종목을 "
        "추천하지 않는다. 최신 시세·뉴스를 아는 척하지 않으며, 매수·매도·수익 보장 표현을 금지한다. popup_title은 "
        "'새롭게 업데이트된 my PICK을 확인해볼까요?'라는 의미를 담아 짧게 쓴다. 팝업 본문은 화면에서 고정 문구로 제공된다. "
        "모든 문구는 짧고 모바일 화면에 적합하게 작성한다. update 항목은 고객 행동을 요구하는 루틴이 아니라 "
        "선택한 AI 추천 목표에 맞춰 my PICK 피드가 어떤 주기와 내용으로 갱신되는지 설명한다."
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
            "body": "올해의 행동을 바탕으로 내년 my PICK에서 이어볼 관심 정보 주제를 준비했어요.",
            "evidence": "Recap 기반 AI 추천 목표 3개 생성",
            "icon": "journey",
        },
    ]
    concentrated_theme = metrics["top_theme_share"] >= 60 and metrics["top_theme"] not in {"글로벌분산", "자산배분", "채권"}
    if concentrated_theme:
        goals = [
            (f"{top_theme} 흐름 깊이 보기", "올해 가장 관심이 높았던 테마의 변화를 이어서 살펴봐요.", f"{top_theme} 업황 리포트·핵심 기업 뉴스", "study"),
            (f"{top_asset} 이슈 모아보기", "자주 만난 종목과 연결된 실적·산업 이슈를 한곳에서 확인해요.", f"{top_asset} 리서치·공시·주요 뉴스", "compass"),
            ("테마 밖 시장 함께 보기", "관심 테마와 다른 자산군의 흐름도 함께 비교해볼 수 있어요.", "ETF 트렌드 리포트·자산배분 시장 뉴스", "balance"),
        ]
    elif metrics["avg_holding_days"] < 60:
        goals = [
            ("시장 변동성 먼저 읽기", "빠르게 움직이는 시장의 배경과 위험 요인을 먼저 살펴봐요.", "급등락 시황·변동성 해설·리스크 리포트", "shield"),
            (f"{top_theme} 뉴스 모아보기", "자주 반응했던 테마의 핵심 이슈를 한 흐름으로 확인해요.", f"{top_theme} 산업 뉴스·기업 이슈·주간 리포트", "study"),
            ("국내외 시황 한눈에 보기", "시장별 이슈를 비교해 움직임의 맥락을 넓게 살펴봐요.", "국내·미국시장 마감 브리핑과 주요 뉴스", "compass"),
        ]
    else:
        goals = [
            ("글로벌 ETF 흐름 보기", "꾸준히 관심을 보인 글로벌 분산 상품의 변화를 이어서 살펴봐요.", "글로벌 ETF 리포트·지수별 주요 뉴스", "balance"),
            ("금리·채권 변화 살펴보기", "장기 투자에 영향을 주는 금리와 채권시장의 맥락을 확인해요.", "중앙은행 뉴스·금리 전망·채권시장 리포트", "study"),
            ("연금·절세 소식 받아보기", "장기 여정과 연결되는 제도 변화를 놓치지 않도록 모아봐요.", "ISA·연금 세제 뉴스와 제도 업데이트", "compass"),
        ]
    return {
        "recap_title": f"{name}님의 한 해 투자기록이 도착했어요!",
        "recap_subtitle": "2026년의 선택을 AI가 하나의 이야기로 엮었습니다.",
        "analysis_summary": f"{top_theme} 관심과 {metrics['avg_holding_days']:.0f}일 평균 보유 리듬이 함께 관찰됐습니다.",
        "investor_word": word,
        "slides": slides,
        "goals": [
            {"goal_id": f"goal_{idx}", "title": title, "reason": reason, "content_focus": focus, "icon": icon}
            for idx, (title, reason, focus, icon) in enumerate(goals, start=1)
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
        "watch_title": top_asset,
        "watch_symbol": top_symbol,
        "watch_reason": "올해 가장 자주 만난 종목의 리서치·공시·산업 뉴스를 모아서 확인할 수 있어요.",
        "market_title": f"{metrics['top_market']} 시장, 오늘은 무엇을 봐야 할까요?",
        "market_body": f"‘{goal_title}’에 맞춰 {goal['content_focus']}를 우선 배치했어요.",
        "content_cards": [
            {
                "category": "맞춤 리포트",
                "title": f"{goal_title} 주간 리포트",
                "description": goal["content_focus"],
                "cta": "리포트 보기",
                "icon": "report",
            },
            {
                "category": "관심 뉴스",
                "title": f"{metrics['top_theme']} 오늘의 주요 뉴스",
                "description": "관심 테마의 실적·산업·정책 이슈를 한곳에 모았어요.",
                "cta": "뉴스 모아보기",
                "icon": "news",
            },
            {
                "category": "시장 브리핑",
                "title": f"{metrics['top_market']} 시장 핵심 이슈",
                "description": "관심 시장의 움직임과 배경을 짧은 시황으로 정리했어요.",
                "cta": "오늘의 시황 보기",
                "icon": "market",
            },
        ],
        "update_title": f"‘{goal_title}’ 맞춤 피드",
        "update_body": f"{goal['content_focus']}를 중심으로 새 리포트와 뉴스를 my PICK에 이어서 반영합니다.",
        "update_frequency": "리포트·뉴스 발행 시 업데이트",
    }
