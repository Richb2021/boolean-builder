#!/usr/bin/env python3
"""
Notification dispatcher for Blue agent routines.

Sends a confirmation message to one or more channels after a routine completes.
Configure channels via environment variables — any combination works.

Supported channels:
    Twilio SMS  — set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, NOTIFY_TO_PHONE
    Webhook     — set NOTIFY_WEBHOOK_URL (works with Slack, Activepieces, Albato, n8n, etc.)
    Email/SMTP  — set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, NOTIFY_TO_EMAIL

Usage:
    python tools/notify.py "Your message here"
    python tools/notify.py --channel twilio "3 todos updated in TA Sprint Demo"
    python tools/notify.py --channel webhook "Build complete"
    python tools/notify.py --channel all "Run finished"   # fires all configured channels
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import base64
import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Channel: Twilio SMS
# ---------------------------------------------------------------------------

def send_twilio(message: str) -> dict:
    """Send an SMS via Twilio REST API."""
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token  = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM")
    to_number   = os.environ.get("NOTIFY_TO_PHONE")

    missing = [k for k, v in {
        "TWILIO_ACCOUNT_SID": account_sid,
        "TWILIO_AUTH_TOKEN": auth_token,
        "TWILIO_FROM": from_number,
        "NOTIFY_TO_PHONE": to_number,
    }.items() if not v]

    if missing:
        return {"channel": "twilio", "status": "skipped",
                "reason": f"Missing env vars: {', '.join(missing)}"}

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    data = urllib.parse.urlencode({
        "From": from_number,
        "To": to_number,
        "Body": message,
    }).encode()

    credentials = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Basic {credentials}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            return {"channel": "twilio", "status": "sent",
                    "sid": result.get("sid"), "to": to_number}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"channel": "twilio", "status": "error", "detail": body}
    except Exception as e:
        return {"channel": "twilio", "status": "error", "detail": str(e)}


# ---------------------------------------------------------------------------
# Channel: Webhook (Slack, Activepieces, Albato, n8n, Make, etc.)
# ---------------------------------------------------------------------------

def send_webhook(message: str) -> dict:
    """POST a JSON payload to a webhook URL."""
    webhook_url = os.environ.get("NOTIFY_WEBHOOK_URL")

    if not webhook_url:
        return {"channel": "webhook", "status": "skipped",
                "reason": "NOTIFY_WEBHOOK_URL not set"}

    payload = json.dumps({
        "text": message,
        "source": "blue-agent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }).encode()

    req = urllib.request.Request(webhook_url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return {"channel": "webhook", "status": "sent",
                    "http_status": resp.status}
    except urllib.error.HTTPError as e:
        return {"channel": "webhook", "status": "error",
                "http_status": e.code, "detail": e.read().decode()}
    except Exception as e:
        return {"channel": "webhook", "status": "error", "detail": str(e)}


# ---------------------------------------------------------------------------
# Channel: Email via SMTP
# ---------------------------------------------------------------------------

def send_email(message: str) -> dict:
    """Send an email via SMTP (works with Gmail, Mailgun, SendGrid SMTP, etc.)."""
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    to_email  = os.environ.get("NOTIFY_TO_EMAIL")

    missing = [k for k, v in {
        "SMTP_HOST": smtp_host,
        "SMTP_USER": smtp_user,
        "SMTP_PASS": smtp_pass,
        "NOTIFY_TO_EMAIL": to_email,
    }.items() if not v]

    if missing:
        return {"channel": "email", "status": "skipped",
                "reason": f"Missing env vars: {', '.join(missing)}"}

    msg = MIMEText(message)
    msg["Subject"] = "Blue Agent — Routine completed"
    msg["From"]    = smtp_user
    msg["To"]      = to_email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string())
        return {"channel": "email", "status": "sent", "to": to_email}
    except Exception as e:
        return {"channel": "email", "status": "error", "detail": str(e)}


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

CHANNELS = {
    "twilio":  send_twilio,
    "webhook": send_webhook,
    "email":   send_email,
}


def dispatch(message: str, channel: str = "all") -> list[dict]:
    """Send to one channel or all configured channels."""
    if channel == "all":
        return [fn(message) for fn in CHANNELS.values()]
    if channel not in CHANNELS:
        print(json.dumps({"error": f"Unknown channel: {channel}. Choose: {', '.join(CHANNELS)} or 'all'"}))
        sys.exit(1)
    return [CHANNELS[channel](message)]


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Send a notification after a Blue agent routine completes."
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="The message to send (required)",
    )
    parser.add_argument(
        "--channel",
        default="all",
        choices=list(CHANNELS.keys()) + ["all"],
        help="Which channel to use (default: all configured channels)",
    )
    args = parser.parse_args()

    if not args.message:
        parser.print_help()
        sys.exit(1)

    results = dispatch(args.message, args.channel)
    print(json.dumps(results, indent=2))

    # Exit non-zero if all channels failed
    if all(r.get("status") in ("error",) for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
