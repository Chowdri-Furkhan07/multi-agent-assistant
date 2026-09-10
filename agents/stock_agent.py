"""Stock agent: fetches latest OHLC price data via yfinance."""

import logging

import yfinance as yf

logger = logging.getLogger(__name__)

DEFAULT_TICKER = "AAPL"


def get_stock_price(ticker: str = DEFAULT_TICKER) -> str:
    """Return a formatted latest-session price summary for ``ticker``.

    Args:
        ticker: Stock ticker symbol, e.g. ``"AAPL"``.

    Returns:
        A formatted summary string, or a friendly error message if the
        ticker is invalid or data could not be retrieved.
    """
    ticker = ticker.upper().strip()

    try:
        history = yf.Ticker(ticker).history(period="1d")
    except Exception as exc:  # yfinance can raise a variety of network/parse errors
        logger.exception("Failed to fetch stock data for %s", ticker)
        return f"❌ Error fetching stock data for '{ticker}': {exc}"

    if history.empty:
        return f"❌ No data found for ticker '{ticker}'. Please check the symbol."

    close_price = float(history["Close"].iloc[-1])
    open_price = float(history["Open"].iloc[-1])
    high_price = float(history["High"].iloc[-1])
    low_price = float(history["Low"].iloc[-1])

    return (
        f"📊 Stock Details for {ticker}:\n"
        f"💰 Current Price: ${close_price:.2f}\n"
        f"📈 Open Price: ${open_price:.2f}\n"
        f"🔺 High: ${high_price:.2f}\n"
        f"🔻 Low: ${low_price:.2f}"
    )


if __name__ == "__main__":
    print(get_stock_price())
