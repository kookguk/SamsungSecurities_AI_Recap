import unittest

from src.analytics import calculate_metrics
from src.data_loader import customer_slice, load_demo_data


class AnalyticsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_demo_data()

    def test_three_customers_have_distinct_crash_behaviors(self):
        codes = {
            calculate_metrics(customer_slice(self.data, customer_id))["crash"]["code"]
            for customer_id in ("C001", "C002", "C003")
        }
        self.assertEqual(codes, {"added", "held", "reduced"})

    def test_holding_periods_are_positive_and_distinct(self):
        days = [
            calculate_metrics(customer_slice(self.data, customer_id))["avg_holding_days"]
            for customer_id in ("C001", "C002", "C003")
        ]
        self.assertTrue(all(day > 0 for day in days))
        self.assertGreater(len(set(days)), 1)

    def test_theme_share_is_percentage(self):
        metrics = calculate_metrics(customer_slice(self.data, "C001"))
        self.assertGreater(metrics["top_theme_share"], 0)
        self.assertLessEqual(metrics["top_theme_share"], 100)


if __name__ == "__main__":
    unittest.main()

