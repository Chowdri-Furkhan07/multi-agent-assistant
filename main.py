"""CLI entry point: runs the weather, stock, and joke agents, then emails
a summary and records results to the shared context file.
"""

import logging
import os

from dotenv import load_dotenv

from agents.joke_agent import get_joke
from agents.notifier_agent import NotifierAgentError, send_email
from agents.stock_agent import get_stock_price
from agents.weather_agent import get_weather
from core.context_manager import record_agent_result

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

DEFAULT_TICKER = os.getenv("DEFAULT_STOCK_TICKER", "AAPL")


def run() -> None:
    weather = get_weather()
    record_agent_result("WeatherAgent", weather)

    stock = get_stock_price(DEFAULT_TICKER)
    record_agent_result("StockAgent", stock)

    joke = get_joke()
    record_agent_result("JokeAgent", joke)

    summary = f"{weather}\n\n{stock}\n\nJoke: {joke}"
    logger.info("Summary:\n%s", summary)

    recipient = os.getenv("NOTIFY_EMAIL")
    if recipient:
        try:
            send_email(recipient, "Daily Agentic AI Summary", summary)
            record_agent_result("NotifierAgent", "Sent")
        except NotifierAgentError as exc:
            logger.error("Notification failed: %s", exc)
            record_agent_result("NotifierAgent", f"Failed: {exc}")
    else:
        logger.info("NOTIFY_EMAIL not set — skipping email notification.")


if __name__ == "__main__":
    run()