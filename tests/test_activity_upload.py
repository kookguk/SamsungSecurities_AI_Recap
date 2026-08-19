import unittest

from src.activity_upload import blank_template_csv, parse_activity_csv, sample_activity_csv


class ActivityUploadTest(unittest.TestCase):
    def test_sample_unifies_all_event_types(self):
        package = parse_activity_csv(sample_activity_csv("C001"))
        self.assertEqual(package["customer"]["name"], "김준호")
        self.assertGreater(package["metrics"]["trade_count"], 0)
        self.assertGreater(package["metrics"]["interest_event_count"], 0)
        self.assertGreater(package["metrics"]["content_event_count"], 0)
        self.assertEqual(package["metrics"]["top_asset_name"], "엔비디아")

    def test_blank_template_is_parseable(self):
        package = parse_activity_csv(blank_template_csv())
        self.assertEqual(package["metrics"]["trade_count"], 1)

    def test_legacy_trade_csv_is_supported(self):
        legacy = "trade_date,symbol,asset_name,market,side,quantity,price,theme\n2026-01-01,NVDA,엔비디아,미국,BUY,1,100,AI\n"
        package = parse_activity_csv(legacy.encode("utf-8"), "테스트")
        self.assertEqual(package["customer"]["name"], "테스트")


if __name__ == "__main__":
    unittest.main()
