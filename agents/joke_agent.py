"""Joke agent: returns a random programming joke."""

import random

_JOKES = [
    "Eight bytes walk into a bar. The bartender asks, 'Can I get you anything?' "
    "'Yeah,' reply the bytes. 'Make us a double.'",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "There are only 10 kinds of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
]


def get_joke() -> str:
    """Return a random programming joke."""
    return random.choice(_JOKES)


if __name__ == "__main__":
    print(get_joke())