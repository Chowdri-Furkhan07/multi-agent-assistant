"""Weather agent: fetches current conditions from Open-Meteo.

Open-Meteo requires no API key for non-commercial use, so this agent
needs zero credentials to run. It does two calls:
  1. Geocode the city name to latitude/longitude (Open-Meteo Geocoding API)
  2. Fetch current weather for those coordinates (Open-Meteo Forecast API)
"""

import logging

import requests

logger = logging.getLogger(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_CITY = "Hyderabad"
REQUEST_TIMEOUT = 10  # seconds

# WMO weather codes -> human-readable condition
# https://open-meteo.com/en/docs (see "WMO Weather interpretation codes")
_WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def _geocode(city: str) -> tuple[float, float, str] | None:
    """Resolve a city name to (latitude, longitude, resolved_name)."""
    params = {"name": city, "count": 1}
    response = requests.get(GEOCODING_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    results = response.json().get("results")
    if not results:
        return None
    top = results[0]
    label = f"{top['name']}, {top.get('country', '')}".strip(", ")
    return top["latitude"], top["longitude"], label


def get_weather(city: str = DEFAULT_CITY, api_key: str | None = None) -> str:
    """Return a human-readable current-weather summary for ``city``.

    Args:
        city: City name to query (defaults to Hyderabad).
        api_key: Unused — kept for backward-compatible call signatures.
            Open-Meteo requires no API key.

    Returns:
        A formatted, user-facing weather summary string. On failure, a
        friendly error string is returned instead of raising, so callers
        (Streamlit UI, orchestrator) can display it directly.
    """
    try:
        location = _geocode(city)
    except requests.exceptions.RequestException as exc:
        logger.exception("Geocoding request failed")
        return f"❌ Could not reach geocoding service: {exc}"

    if location is None:
        return f"❌ City '{city}' not found. Please check the spelling."

    lat, lon, resolved_name = location
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,weather_code",
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.exception("Weather request failed")
        return f"❌ Could not reach weather service: {exc}"

    current = response.json().get("current", {})
    temp = current.get("temperature_2m")
    wind_speed = current.get("wind_speed_10m")
    condition = _WEATHER_CODES.get(current.get("weather_code"), "Unknown")

    return (
        f"🌦️ Weather in {resolved_name}:\n"
        f"- Temperature: {temp}°C\n"
        f"- Wind Speed: {wind_speed} km/h\n"
        f"- Condition: {condition}"
    )


if __name__ == "__main__":
    print(get_weather())