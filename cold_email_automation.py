#!/usr/bin/env python3
"""Lead outreach automation: find pending leads, send cold emails, and report replies.

Usage examples:
  python cold_email_automation.py send
  python cold_email_automation.py check-replies
  python cold_email_automation.py run-daily

Expected files:
  - leads.csv (required): name,email,company,website,notes
  - sent_log.csv (auto-created)
  - replies_report.csv (auto-created)

Environment variables:
  SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
  IMAP_HOST, IMAP_PORT, IMAP_USERNAME, IMAP_PASSWORD
  SENDER_NAME, SENDER_EMAIL, MAX_DAILY_EMAILS (default: 50)
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import imaplib
import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parent
LEADS_FILE = BASE_DIR / "leads.csv"
SENT_LOG_FILE = BASE_DIR / "sent_log.csv"
REPLIES_REPORT_FILE = BASE_DIR / "replies_report.csv"


@dataclass
class Lead:
    name: str
    email: str
    company: str = ""
    website: str = ""
    notes: str = ""


@dataclass
class MailSettings:
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    imap_host: str
    imap_port: int
    imap_username: str
    imap_password: str
    sender_name: str
    sender_email: str
    max_daily: int


def env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def load_settings() -> MailSettings:
    return MailSettings(
        smtp_host=env("SMTP_HOST"),
        smtp_port=int(env("SMTP_PORT", "587")),
        smtp_username=env("SMTP_USERNAME"),
        smtp_password=env("SMTP_PASSWORD"),
        imap_host=env("IMAP_HOST"),
        imap_port=int(env("IMAP_PORT", "993")),
        imap_username=env("IMAP_USERNAME"),
        imap_password=env("IMAP_PASSWORD"),
        sender_name=env("SENDER_NAME"),
        sender_email=env("SENDER_EMAIL"),
        max_daily=int(env("MAX_DAILY_EMAILS", "50")),
    )


def read_leads(path: Path = LEADS_FILE) -> list[Lead]:
    if not path.exists():
        raise FileNotFoundError(f"Missing leads file: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        leads: list[Lead] = []
        for row in reader:
            email = (row.get("email") or "").strip().lower()
            if not email:
                continue
            leads.append(
                Lead(
                    name=(row.get("name") or "").strip(),
                    email=email,
                    company=(row.get("company") or "").strip(),
                    website=(row.get("website") or "").strip(),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return leads


def read_sent_today(path: Path = SENT_LOG_FILE) -> set[str]:
    today = dt.date.today().isoformat()
    sent: set[str] = set()
    if not path.exists():
        return sent

    with path.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("date") == today:
                sent.add((row.get("email") or "").lower())
    return sent


def append_rows(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    file_exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_subject(lead: Lead) -> str:
    if lead.company:
        return f"Quick idea for {lead.company}"
    return "Quick collaboration idea"


def build_body(lead: Lead, sender_name: str) -> str:
    greeting = f"Hi {lead.name}," if lead.name else "Hi there,"
    context = ""
    if lead.company:
        context += f" I came across {lead.company}"
    if lead.website:
        context += f" ({lead.website})"
    if not context:
        context = " I came across your business"

    return (
        f"{greeting}\n\n"
        f"{context} and wanted to reach out with a quick idea that could help you generate more qualified leads. "
        "I can share a short plan tailored to your niche and workflow.\n\n"
        "If you’re open to it, I can send a 3-step recommendation you can review in 5 minutes.\n\n"
        f"Best,\n{sender_name}\n"
    )


def send_cold_emails(settings: MailSettings, leads: list[Lead]) -> int:
    sent_today = read_sent_today()
    remaining = max(settings.max_daily - len(sent_today), 0)
    if remaining == 0:
        print(f"Daily limit reached ({settings.max_daily}).")
        return 0

    queued = [lead for lead in leads if lead.email not in sent_today][:remaining]
    if not queued:
        print("No unsent leads available for today.")
        return 0

    sent_rows: list[dict[str, str]] = []
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_username, settings.smtp_password)

        for lead in queued:
            msg = EmailMessage()
            msg["Subject"] = build_subject(lead)
            msg["From"] = formataddr((settings.sender_name, settings.sender_email))
            msg["To"] = lead.email
            msg.set_content(build_body(lead, settings.sender_name))
            smtp.send_message(msg)

            now = dt.datetime.now().isoformat(timespec="seconds")
            sent_rows.append(
                {
                    "date": dt.date.today().isoformat(),
                    "sent_at": now,
                    "email": lead.email,
                    "name": lead.name,
                    "company": lead.company,
                    "subject": msg["Subject"],
                }
            )
            print(f"Sent: {lead.email}")

    append_rows(
        SENT_LOG_FILE,
        ["date", "sent_at", "email", "name", "company", "subject"],
        sent_rows,
    )
    return len(sent_rows)


def check_replies(settings: MailSettings) -> int:
    now = dt.datetime.now().isoformat(timespec="seconds")
    found_rows: list[dict[str, str]] = []

    with imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port) as imap:
        imap.login(settings.imap_username, settings.imap_password)
        imap.select("INBOX")

        status, data = imap.search(None, "UNSEEN")
        if status != "OK":
            print("Unable to search inbox for replies.")
            return 0

        message_ids = data[0].split()
        for msg_id in message_ids:
            status, msg_data = imap.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if status != "OK" or not msg_data:
                continue

            raw_headers = b""
            for item in msg_data:
                if isinstance(item, tuple) and len(item) > 1:
                    raw_headers += item[1]

            header_text = raw_headers.decode("utf-8", errors="replace")
            if settings.sender_email.lower() in header_text.lower():
                continue

            from_line = next((line[5:].strip() for line in header_text.splitlines() if line.lower().startswith("from:")), "")
            subject_line = next((line[8:].strip() for line in header_text.splitlines() if line.lower().startswith("subject:")), "")
            date_line = next((line[5:].strip() for line in header_text.splitlines() if line.lower().startswith("date:")), "")

            found_rows.append(
                {
                    "checked_at": now,
                    "from": from_line,
                    "subject": subject_line,
                    "email_date": date_line,
                }
            )

    if found_rows:
        append_rows(REPLIES_REPORT_FILE, ["checked_at", "from", "subject", "email_date"], found_rows)

    return len(found_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cold outreach sender and reply reporter")
    parser.add_argument("command", choices=["send", "check-replies", "run-daily"])
    args = parser.parse_args()

    settings = load_settings()

    if args.command == "send":
        leads = read_leads()
        sent_count = send_cold_emails(settings, leads)
        print(f"Sent {sent_count} emails.")
    elif args.command == "check-replies":
        replies = check_replies(settings)
        print(f"Found {replies} potential replies.")
    else:
        leads = read_leads()
        sent_count = send_cold_emails(settings, leads)
        replies = check_replies(settings)
        print(f"Completed daily run: sent={sent_count}, replies={replies}")


if __name__ == "__main__":
    main()
