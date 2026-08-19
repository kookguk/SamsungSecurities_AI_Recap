import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.recap_service import generate_recap


class FakeResponses:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            output_text=json.dumps(
                {
                    "pattern_name": "근거형 투자자",
                    "headline": "근거로 돌아본 한 해",
                    "story": "평균 보유기간과 관심 테마를 함께 살펴봤어요.",
                    "strength": "일관성이 있었어요.",
                    "watchout": "분산을 점검해볼 수 있어요.",
                    "recommended_goal": "분산투자 이해하기",
                },
                ensure_ascii=False,
            )
        )


class FakeClient:
    last_instance = None

    def __init__(self, api_key):
        self.api_key = api_key
        self.responses = FakeResponses()
        FakeClient.last_instance = self


class RecapServiceTest(unittest.TestCase):
    def test_uses_responses_structured_output(self):
        customer = {
            "customer_id": "C001",
            "name": "김준호",
            "goal_options": ["분산투자 이해하기", "장기투자 습관 만들기"],
        }
        with patch("openai.OpenAI", FakeClient):
            result = generate_recap(customer, {"avg_holding_days": 42}, "test-key", "test-model")
        request = FakeClient.last_instance.responses.kwargs
        self.assertEqual(result["recommended_goal"], "분산투자 이해하기")
        self.assertEqual(request["model"], "test-model")
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertTrue(request["text"]["format"]["strict"])


if __name__ == "__main__":
    unittest.main()
