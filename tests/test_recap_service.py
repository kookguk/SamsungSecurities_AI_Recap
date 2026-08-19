import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.activity_upload import parse_activity_csv, sample_activity_csv
from src.recap_service import fallback_journey, generate_journey, generate_mypick_plan


JOURNEY_RESULT = {
    "recap_title": "나의 투자기록",
    "recap_subtitle": "한 해의 이야기",
    "analysis_summary": "검증된 요약",
    "investor_word": "리듬",
    "slides": [
        {"sequence": i, "kicker": "장면", "headline": "제목", "body": "내용", "evidence": "근거", "icon": icon}
        for i, icon in enumerate(["taste", "stock", "market", "pattern", "journey"], start=1)
    ],
    "goals": [
        {"goal_id": f"goal_{i}", "title": f"관심 목표 {i}", "reason": "이유", "content_focus": "리포트와 뉴스", "icon": "habit"}
        for i in range(1, 4)
    ],
}

MYPICK_RESULT = {
    "popup_title": "새 my PICK",
    "popup_body": "목표를 반영했어요.",
    "watch_title": "엔비디아",
    "watch_symbol": "NVDA",
    "watch_reason": "기존 관심 종목",
    "market_title": "시장 요약",
    "market_body": "관심 기반 요약",
    "content_cards": [
        {"category": "기초", "title": f"콘텐츠 {i}", "description": "설명", "cta": "보기", "icon": "lesson"}
        for i in range(1, 4)
    ],
    "update_title": "맞춤 피드",
    "update_body": "리포트와 뉴스 업데이트",
    "update_frequency": "새 콘텐츠 발행 시",
}


class FakeResponses:
    calls = []

    def create(self, **kwargs):
        FakeResponses.calls.append(kwargs)
        schema_name = kwargs["text"]["format"]["name"]
        result = JOURNEY_RESULT if schema_name == "investment_recap_journey" else MYPICK_RESULT
        return SimpleNamespace(output_text=json.dumps(result, ensure_ascii=False))


class FakeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.responses = FakeResponses()


class RecapServiceTest(unittest.TestCase):
    def setUp(self):
        FakeResponses.calls = []

    def test_two_stage_pipeline_uses_strict_structured_outputs(self):
        customer = {"customer_id": "C001", "name": "김준호"}
        metrics = {"top_symbol": "NVDA"}
        with patch("openai.OpenAI", FakeClient):
            journey = generate_journey(customer, metrics, "test-key", "test-model")
            plan = generate_mypick_plan(customer, metrics, journey, journey["goals"][0], "test-key", "test-model")
        self.assertEqual(len(journey["slides"]), 5)
        self.assertEqual(len(journey["goals"]), 3)
        self.assertEqual(len(plan["content_cards"]), 3)
        self.assertEqual([call["text"]["format"]["name"] for call in FakeResponses.calls], ["investment_recap_journey", "mypick_personalization"])
        self.assertTrue(all(call["text"]["format"]["strict"] for call in FakeResponses.calls))

    def test_fallback_goals_are_generated_from_each_personas_metrics(self):
        goal_sets = []
        for customer_id in ("C001", "C002", "C003"):
            package = parse_activity_csv(sample_activity_csv(customer_id))
            journey = fallback_journey(package["customer"], package["metrics"])
            goal_sets.append(tuple(goal["title"] for goal in journey["goals"]))
            self.assertTrue(all("content_focus" in goal for goal in journey["goals"]))
        self.assertEqual(len(set(goal_sets)), 3)


if __name__ == "__main__":
    unittest.main()
