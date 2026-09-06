"""Calendar agent: creates a calendar event from a natural-language request.

This is a lightweight placeholder implementation. It does not call the
real Google Calendar API — wire up `google-api-python-client` with OAuth
credentials in `_create_google_calendar_event` to make it functional.
"""

import logging
import uuid

logger = logging.getLogger(__name__)


def _create_google_calendar_event(text: str) -> str:
    """Placeholder for real Google Calendar API integration.

    Replace this with an authenticated call using
    `google-api-python-client` (Calendar API v3) once OAuth credentials
    are configured. Keep credentials out of source control (see
    `.gitignore`).
    """
    fake_event_id = uuid.uuid4().hex[:16]
    return f"https://calendar.google.com/calendar/event?eid={fake_event_id}"


def create_event_from_natural_language(text: str) -> str:
    """Create a calendar event described in natural language.

    Args:
        text: Free-text request, e.g. "Book a meeting on 6th April 9AM".

    Returns:
        A confirmation string including a (placeholder) event link.
    """
    if not text or not text.strip():
        return "❌ Please describe the meeting you'd like to schedule."

    logger.info("Creating calendar event from request: %s", text)
    event_link = _create_google_calendar_event(text)
    return f"✅ Event created from request: \"{text.strip()}\"\n📅 {event_link}"


if __name__ == "__main__":
    print(create_event_from_natural_language("Book a meeting on 6th April 9AM"))