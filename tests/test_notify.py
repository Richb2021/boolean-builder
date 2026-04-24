"""
Tests for tools/notify.py

Run with:
    python -m unittest discover -s tests
"""

import sys
import os
import json
import unittest

# Add tools/ to path so we can import notify directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

import notify


class TestNotifyChannelSkip(unittest.TestCase):
    """When no channels are configured, all results should be skipped."""

    def setUp(self):
        # Remove all notification env vars so no channel is configured
        self._removed = {}
        for key in [
            "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM", "NOTIFY_TO_PHONE",
            "NOTIFY_WEBHOOK_URL",
            "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "NOTIFY_TO_EMAIL",
        ]:
            if key in os.environ:
                self._removed[key] = os.environ.pop(key)

    def tearDown(self):
        os.environ.update(self._removed)

    def test_all_channels_skipped_when_unconfigured(self):
        results = notify.dispatch("test message", channel="all")
        statuses = [r.get("status") for r in results]
        self.assertTrue(
            all(s == "skipped" for s in statuses),
            f"Expected all skipped, got: {statuses}"
        )

    def test_dispatch_returns_list(self):
        results = notify.dispatch("test message", channel="all")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_each_result_has_channel_and_status(self):
        results = notify.dispatch("test message", channel="all")
        for r in results:
            self.assertIn("channel", r)
            self.assertIn("status", r)

    def test_twilio_skipped_without_creds(self):
        result = notify.send_twilio("test")
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["channel"], "twilio")

    def test_webhook_skipped_without_url(self):
        result = notify.send_webhook("test")
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["channel"], "webhook")

    def test_email_skipped_without_creds(self):
        result = notify.send_email("test")
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["channel"], "email")


class TestNotifyInvalidChannel(unittest.TestCase):

    def test_invalid_channel_raises_system_exit(self):
        with self.assertRaises(SystemExit):
            notify.dispatch("test", channel="fax")


if __name__ == "__main__":
    unittest.main()
