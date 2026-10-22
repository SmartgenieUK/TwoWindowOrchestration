"""Reviewer-owned checks derived from docs/CONTRACT.md, not the executor summary."""
import unittest
from src.retry_policy import should_retry

class AcceptanceTests(unittest.TestCase):
    def test_first_attempt_can_retry(self): self.assertTrue(should_retry('GET', 503, 1, 3))
    def test_second_attempt_can_retry(self): self.assertTrue(should_retry('GET', 503, 2, 3))
    def test_final_attempt_stops(self): self.assertFalse(should_retry('GET', 503, 3, 3))
    def test_past_final_attempt_stops(self): self.assertFalse(should_retry('GET', 503, 4, 3))
    def test_one_total_attempt_means_no_retries(self): self.assertFalse(should_retry('GET', 503, 1, 1))
    def test_success_stops(self): self.assertFalse(should_retry('GET', 200, 1))
    def test_head_can_retry(self): self.assertTrue(should_retry('HEAD', 503, 1))
    def test_normalizes_method(self): self.assertTrue(should_retry(' get ', 503, 1))
    def test_post_never_retries(self): self.assertFalse(should_retry('POST', 503, 1))
    def test_other_methods_never_retry(self):
        for method in ['PUT', 'PATCH', 'DELETE', 'OPTIONS', 'CUSTOM']:
            with self.subTest(method=method): self.assertFalse(should_retry(method, 503, 1))
    def test_allowlisted_statuses(self):
        for status in [429, 500, 502, 503, 504]:
            with self.subTest(status=status): self.assertTrue(should_retry('GET', status, 1))
    def test_other_statuses_stop(self):
        for status in [201, 301, 400, 401, 404, 501, 505]:
            with self.subTest(status=status): self.assertFalse(should_retry('GET', status, 1))
    def test_positive_counters(self):
        for attempt, maximum in [(0, 3), (-1, 3), (1, 0), (1, -1)]:
            with self.subTest(attempt=attempt, maximum=maximum):
                with self.assertRaises(ValueError): should_retry('GET', 503, attempt, maximum)
    def test_status_range(self):
        for status in [99, 600]:
            with self.assertRaises(ValueError): should_retry('GET', status, 1)
    def test_numeric_types(self):
        for args in [('GET', True, 1, 3), ('GET', 503, True, 3), ('GET', 503, 1, False),
                     ('GET', '503', 1, 3), ('GET', 503, 1.5, 3), ('GET', 503, 1, '3')]:
            with self.subTest(args=args):
                with self.assertRaises(ValueError): should_retry(*args)
    def test_method_validation(self):
        for method in ['', '  ', None, 12]:
            with self.assertRaises(ValueError): should_retry(method, 503, 1)
    def test_retry_budget_invariant(self):
        for maximum in range(1, 8):
            retries = sum(should_retry('GET', 503, n, maximum) for n in range(1, maximum + 2))
            with self.subTest(maximum=maximum): self.assertEqual(retries, maximum - 1)
    def test_default_is_three_total_attempts(self): self.assertFalse(should_retry('GET', 503, 3))
