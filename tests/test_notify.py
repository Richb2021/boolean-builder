import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTIFY_SCRIPT = REPO_ROOT / "tools" / "notify.py"


class NotifyCliTests(unittest.TestCase):
    def test_all_skipped_channels_exit_nonzero(self):
        env = os.environ.copy()
        for name in (
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "TWILIO_FROM",
            "NOTIFY_TO_PHONE",
            "NOTIFY_WEBHOOK_URL",
            "SMTP_HOST",
            "SMTP_PORT",
            "SMTP_USER",
            "SMTP_PASS",
            "NOTIFY_TO_EMAIL",
        ):
            env.pop(name, None)

        result = subprocess.run(
            [sys.executable, str(NOTIFY_SCRIPT), "Smoke test message"],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn('"status": "skipped"', result.stdout)


if __name__ == "__main__":
    unittest.main()
