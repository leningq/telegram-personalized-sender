"""CLI entry point: reads leads.csv, personalizes, sends, logs results.

Usage:
    python main.py leads.csv
    python main.py leads.csv --dry-run
"""

import argparse
import asyncio
import csv
import logging
import sys

from dotenv import load_dotenv

from personalize import generate_message
from sender import send_batch

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def read_leads(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_log(path: str, leads: list[dict]) -> None:
    if not leads:
        return
    fieldnames = list(leads[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(leads)


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Send personalized Telegram outreach messages.")
    parser.add_argument("leads_csv", help="CSV with columns: name, telegram_handle, business_type, city, notes")
    parser.add_argument("--dry-run", action="store_true", help="Generate messages but don't send them")
    parser.add_argument("--log", default="sent_log.csv", help="Where to write the results log")
    args = parser.parse_args()

    leads = read_leads(args.leads_csv)
    if not leads:
        logger.error("No leads found in %s", args.leads_csv)
        sys.exit(1)

    logger.info("Loaded %d leads from %s", len(leads), args.leads_csv)

    for lead in leads:
        lead["message"] = generate_message(lead)
        if args.dry_run:
            print(f"\n@{lead['telegram_handle']} ({lead['name']}):\n{lead['message']}")

    results = asyncio.run(send_batch(leads, dry_run=args.dry_run))
    write_log(args.log, results)
    logger.info("Done. Results written to %s", args.log)


if __name__ == "__main__":
    main()
