"""Streamlit dashboard for the Agentic AI Assistant."""

import re

import streamlit as st
from dotenv import load_dotenv

from agents.calendar_agent import create_event_from_natural_language
from agents.joke_agent import get_joke
from agents.notifier_agent import NotifierAgentError, send_email
from agents.stock_agent import get_stock_price
from agents.weather_agent import get_weather

load_dotenv()

st.set_page_config(page_title="Agentic AI Assistant", layout="centered")
st.title("🤖 Agentic AI Assistant Dashboard")

st.markdown(
    """
This assistant can:

🌦️ Get real-time weather
💹 Fetch stock prices (like AAPL)
😂 Tell a programming joke
📅 Book a meeting from a natural-language request
📧 Send results via email

**Ask your question** (e.g. _"What's the weather in Hyderabad?"_,
_"Tell me a joke"_, _"Get AAPL stock"_, _"Book a meeting on 6th April 9AM"_)
"""
)

if "response" not in st.session_state:
    st.session_state.response = ""
if "agents_triggered" not in st.session_state:
    st.session_state.agents_triggered = []

user_input = st.text_input("Ask your question:")


def route_query(text: str) -> tuple[str, list[str]]:
    """Route free-text input to the appropriate agent and return its result."""
    lower = text.lower()

    if any(kw in lower for kw in ["weather", "temperature", "climate"]):
        city_match = re.search(r"in (\w+)", lower)
        city = city_match.group(1).capitalize() if city_match else "Hyderabad"
        return get_weather(city), ["Weather"]

    if any(kw in lower for kw in ["stock", "price", "share"]):
        ticker_match = re.search(r"\b([A-Z]{2,5})\b", text)
        ticker = ticker_match.group(1) if ticker_match else "AAPL"
        return get_stock_price(ticker), ["Stock"]

    if any(kw in lower for kw in ["joke", "laugh", "funny"]):
        return get_joke(), ["Joke"]

    if any(kw in lower for kw in ["meeting", "calendar", "book", "appointment", "schedule"]):
        return create_event_from_natural_language(text), ["Calendar"]

    return (
        "❌ I'm not sure how to help with that. Try asking about weather, stocks, jokes, or meetings.",
        [],
    )


if st.button("Run Agent") and user_input:
    try:
        response, agents_triggered = route_query(user_input)
    except Exception as exc:  # surface unexpected agent errors in the UI
        response, agents_triggered = f"❌ Error occurred while running agents: {exc}", []

    st.session_state.response = response
    st.session_state.agents_triggered = agents_triggered

if st.session_state.response:
    st.markdown("### ✅ Result")

    if st.session_state.agents_triggered:
        st.markdown(f"**Agent triggered:** {', '.join(st.session_state.agents_triggered)}")

    st.code(st.session_state.response)

    st.markdown("### 📧 Send Result via Email")
    email_to = st.text_input("Enter recipient email:")

    if st.button("Send Email"):
        if email_to:
            try:
                send_email(email_to, "Agentic AI Result", st.session_state.response)
                st.success("✅ Email sent successfully!")
            except NotifierAgentError as exc:
                st.error(f"❌ Failed to send email: {exc}")
        else:
            st.warning("⚠️ Please enter an email address")

st.divider()
st.caption("Multi-agent assistant · Streamlit UI · lightweight local context tracking")