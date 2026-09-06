"""Unit tests covering agent logic that doesn't require live credentials."""

from agents.calendar_agent import create_event_from_natural_language
from agents.joke_agent import get_joke
from agents.weather_agent import get_weather


def test_get_joke_returns_nonempty_string():
    joke = get_joke()
    assert isinstance(joke, str)
    assert len(joke) > 0


def test_get_weather_without_api_key_returns_friendly_error(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    result = get_weather("Hyderabad", api_key=None)
    assert "❌" in result
    assert "API key" in result


def test_create_event_with_empty_text_returns_prompt():
    result = create_event_from_natural_language("")
    assert "❌" in result


def test_create_event_with_text_returns_confirmation():
    result = create_event_from_natural_language("Book a meeting on 6th April 9AM")
    assert "✅" in result
    assert "calendar.google.com" in result