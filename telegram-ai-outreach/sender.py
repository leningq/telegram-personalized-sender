"""Sends messages through a Telegram user session via Telethon.

Handles Telegram's flood-wait responses by sleeping for the time Telegram
asks for and retrying once, instead of hammering the API or crashing the
whole run over one rate-limited recipient.
"""

import asyncio
import logging
import os
import random

from telethon import TelegramClient
from telethon.errors import FloodWaitError, UsernameNotOccupiedError

logger = logging.getLogger(__name__)

MIN_DELAY_SECONDS = 20
MAX_DELAY_SECONDS = 40


def build_client() -> TelegramClient:
    api_id = os.environ["TELEGRAM_API_ID"]
    api_hash = os.environ["TELEGRAM_API_HASH"]
    return TelegramClient("outreach_session", api_id, api_hash)


async def send_with_retry(client: TelegramClient, handle: str, message: str) -> tuple[bool, str]:
    """Send one message. Returns (success, status_message)."""
    try:
        await client.send_message(handle, message)
        return True, "sent"
    except FloodWaitError as e:
        logger.warning("Flood wait for %s seconds on @%s, retrying once", e.seconds, handle)
        await asyncio.sleep(e.seconds)
        try:
            await client.send_message(handle, message)
            return True, "sent after flood wait"
        except Exception as retry_error:
            return False, f"failed after flood wait: {retry_error}"
    except UsernameNotOccupiedError:
        return False, "username not found"
    except Exception as e:
        return False, f"failed: {e}"


async def send_batch(leads_with_messages: list[dict], dry_run: bool = False) -> list[dict]:
    """Send each lead's message with a randomized delay between sends.

    leads_with_messages: list of dicts, each with the original lead fields
    plus a "message" key. Returns the same list with "status" added.
    """
    if dry_run:
        for lead in leads_with_messages:
            lead["status"] = "dry-run (not sent)"
        return leads_with_messages

    client = build_client()
    async with client:
        for i, lead in enumerate(leads_with_messages):
            success, status = await send_with_retry(client, lead["telegram_handle"], lead["message"])
            lead["status"] = status
            logger.info("[%d/%d] @%s -> %s", i + 1, len(leads_with_messages), lead["telegram_handle"], status)

            if i < len(leads_with_messages) - 1:
                delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
                await asyncio.sleep(delay)

    return leads_with_messages
