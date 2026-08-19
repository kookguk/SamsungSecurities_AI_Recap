import json
import tempfile
import unittest
from pathlib import Path

from src.memory_store import save_goal


class MemoryStoreTest(unittest.TestCase):
    def test_save_goal_creates_valid_memory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "memory.json"
            entry = save_goal("T001", "테스트", "분산투자 이해하기", path=path)
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(entry["goal_year"], 2027)
            self.assertEqual(saved["customers"]["T001"]["selected_goal"], "분산투자 이해하기")


if __name__ == "__main__":
    unittest.main()

