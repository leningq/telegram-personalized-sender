

```markdown
# telegram-personalized-sender

**Stop sending the same message to everyone.** This tool reads a CSV of leads, writes a unique opening line for each one with Claude based on their actual business, then sends it over Telegram — with delays and flood-wait handling so the account doesn't get flagged.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![Telethon](https://img.shields.io/badge/telegram-telethon-26A5E4?logo=telegram&logoColor=white)
![Claude](https://img.shields.io/badge/AI-Claude-D97757)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

### Why

A plain auto-sender blasts one identical message to a list — reads like spam, gets ignored (or gets the account banned). This one writes a different opener for every recipient, grounded in who they actually are:

```
> auto-sender:        "Hi! Check out our services, DM for info 🚀"
> this tool (Anna, bakery, Riga, "recently opened a second location"):
  "Noticed Anna (bakery in Riga) — recently opened a second location.
   We build small tools (booking, reminders, simple automation)
   for businesses like yours. Worth a quick look?"
```

### Features

- **CSV in, personalized message out** — one row per recipient: name, handle, business type, city, notes
- **Claude-generated opener per lead**, grounded in their actual context — not a copy-pasted mass message
- **Runs with zero secrets** — no API key set, falls back to a built-in template so the pipeline still works end to end
- **Real Telegram user session (Telethon)**, not a bot — reaches any username, not just people who already messaged a bot
- **Flood-wait aware** — randomized delay between sends, automatic retry on `FloodWaitError` instead of crashing the run
- **`--dry-run` mode** — generate and preview every message before anything gets sent
- **Every run logged** to `sent_log.csv` (sent / failed / dry-run, per recipient)

> [!WARNING]
> This sends from **your personal Telegram account** via the Telegram API, not through a bot. Mass or unsolicited messaging can violate [Telegram's Terms of Service](https://telegram.org/tos) and get an account limited or banned. Use it for real leads and existing contacts — not cold spam to random accounts — and keep delays reasonable (default: 20–40s between sends).

### Requirements

| | |
|---|---|
| Python | 3.10+ |
| Telegram | `api_id` / `api_hash` from [my.telegram.org](https://my.telegram.org) |
| Anthropic API key | optional — without it, messages use the built-in template |

### Quick start

```bash
pip install -r requirements.txt
cp .env.example .env            # fill in TELEGRAM_API_ID, TELEGRAM_API_HASH, ANTHROPIC_API_KEY

python main.py leads_example.csv --dry-run   # preview — sends nothing
python main.py leads_example.csv             # sends for real
```

On first run, Telethon asks for your phone number, then a login code (and a 2FA password if you have one set) — enter them in the terminal. A session file is saved afterward so you won't need to log in again.

### Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point — reads the CSV, drives personalization + sending, writes the log |
| `personalize.py` | Generates each message via Claude, with a template fallback |
| `sender.py` | Telethon client, send-with-retry, flood-wait handling, delay between sends |
| `leads_example.csv` | Sample lead list (synthetic data, safe to run against) |

> [!IMPORTANT]
> `.env`, `*.session`, and `sent_log.csv` are already in `.gitignore` — the session file grants full access to your Telegram account, same as a password. Never commit it.

---

Built with `Python` · `Telethon` · `Claude`
```

