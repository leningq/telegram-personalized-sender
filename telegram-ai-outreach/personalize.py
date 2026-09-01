"""Generates a short, specific outreach opener for one lead.

Uses the Claude API when ANTHROPIC_API_KEY is set. Falls back to a plain
template otherwise, so the rest of the pipeline is runnable and testable
without any API key.
"""

import os

SYSTEM_PROMPT = (
    "You write short, specific Telegram outreach openers for a small "
    "web development and automation agency (Buildlab). One or two "
    "sentences, no greetings like 'Hi there', no generic sales language, "
    "no emoji. Reference the recipient's actual business type and notes "
    "so it clearly isn't a copy-pasted mass message. End with a soft, "
    "low-pressure question inviting a reply."
)

TEMPLATE = (
    "Noticed {name} ({business_type} in {city}) — {notes}. "
    "We build small tools (booking, reminders, simple automation) for "
    "businesses like yours. Worth a quick look?"
)


def generate_message(lead: dict) -> str:
    """Return a personalized message string for a single lead row."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return TEMPLATE.format(
            name=lead["name"],
            business_type=lead["business_type"],
            city=lead["city"],
            notes=lead.get("notes", "").strip() or "growing steadily",
        )

    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    user_prompt = (
        f"Recipient: {lead['name']}\n"
        f"Business type: {lead['business_type']}\n"
        f"City: {lead['city']}\n"
        f"Notes: {lead.get('notes', 'none')}\n\n"
        "Write the outreach opener."
    )

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text.strip()
