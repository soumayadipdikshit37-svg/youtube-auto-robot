# youtube-auto-robot
Automated YouTube video creation and upload.

## Cold email automation (lead outreach)
This repo now also includes `cold_email_automation.py` to help you:
- Send personalized cold emails to leads from `leads.csv`
- Limit sending to `50` emails per day (customizable)
- Check inbox for new replies and log them to `replies_report.csv`

### 1) Install requirements
```bash
pip install -r requirements.txt
```

### 2) Prepare leads
Create a `leads.csv` file in the repo root:
```csv
name,email,company,website,notes
Jane Doe,jane@example.com,Acme,https://acme.com,Marketing agency
```

### 3) Set environment variables
```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@example.com
export SMTP_PASSWORD=your-password-or-app-password

export IMAP_HOST=imap.gmail.com
export IMAP_PORT=993
export IMAP_USERNAME=your-email@example.com
export IMAP_PASSWORD=your-password-or-app-password

export SENDER_NAME="Your Name"
export SENDER_EMAIL=your-email@example.com
export MAX_DAILY_EMAILS=50
```

### 4) Run commands
Send emails:
```bash
python cold_email_automation.py send
```

Check replies:
```bash
python cold_email_automation.py check-replies
```

Run both in one daily job:
```bash
python cold_email_automation.py run-daily
```

### 5) Schedule daily sending (Linux cron example)
Run every day at 09:00:
```cron
0 9 * * * cd /workspace/youtube-auto-robot && /usr/bin/python3 cold_email_automation.py run-daily >> daily_email.log 2>&1
```

### Output files
- `sent_log.csv`: all sent emails with timestamp and subject
- `replies_report.csv`: potential replies found in inbox

> Important: follow anti-spam laws (CAN-SPAM/GDPR), use valid business targeting, and include opt-out language where required.
