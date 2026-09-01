```markdown
# telegram-personalized-sender

Telegram outreach tool (Telethon + Claude) that writes a unique, personalized opening message for each lead from a CSV — instead of blasting the same text to everyone — with flood-wait handling and a dry-run preview.

## Features

- CSV-driven — one row per lead: name, handle, business type, city, notes
- Claude-generated opening line per lead, grounded in their actual context (falls back to a built-in template if no API key is set)
- Real Telegram user session via Telethon — reaches any username, not just people who already messaged a bot
- `FloodWaitError` handling — waits it out automatically instead of crashing
- Randomized delay between sends (default 20–40s)
- `--dry-run` mode — preview every generated message before anything sends
- Every run logged to `sent_log.csv` (sent / failed / dry-run, per recipient)

## ⚠️ Important

Mass messaging can violate [Telegram's Terms of Service](https://telegram.org/tos) and get your account limited or banned. This tool sends messages from **your personal account** via the Telegram API (not through a bot). Use it for real leads and existing contacts, not cold spam to random accounts, and keep delays reasonable (20+ sec between messages is recommended).

## Requirements

- Python 3.10+
- API ID and API Hash from [my.telegram.org](https://my.telegram.org)
- (optional) Anthropic API key — without it, messages fall back to a built-in template

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own values:

```
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=your_api_hash_here
ANTHROPIC_API_KEY=
```

## Run

```bash
python main.py leads_example.csv --dry-run   # preview — sends nothing
python main.py leads_example.csv             # sends for real
```

On first run, Telethon will ask for your phone number, then a verification code (and a 2FA password if enabled) — enter them in the terminal. After a successful login, a session file is created — **do not publish it**, it grants full access to the account, same as a password.

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point — reads the CSV, drives personalization + sending, writes the log |
| `personalize.py` | Generates each message via Claude, with a template fallback |
| `sender.py` | Telethon client, send-with-retry, flood-wait handling, delay between sends |
| `leads_example.csv` | Sample lead list (synthetic data, safe to run against) |
```

