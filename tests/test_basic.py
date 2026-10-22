"""Intentionally incomplete executor tests. Green does not cover the contract."""
import unittest
from src.retry_policy import should_retry

class BasicTests(unittest.TestCase):
    def test_first_failure(self): self.assertTrue(should_retry('GET', 503, 1))
    def test_second_failure(self): self.assertTrue(should_retry('GET', 503, 2))
    def test_success(self): self.assertFalse(should_retry('GET', 200, 1))
    def test_post(self): self.assertFalse(should_retry('POST', 503, 1))
    def test_client_error(self): self.assertFalse(should_retry('GET', 404, 1))
    def test_head(self): self.assertTrue(should_retry('HEAD', 429, 1))
