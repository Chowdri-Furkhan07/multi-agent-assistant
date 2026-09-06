"""Shared context/state tracker for agent runs.

Note: this module was renamed from `mcp/` to `core/` to avoid clashing
with the official `mcp` (Model Context Protocol) PyPI package. The name
"MCP" in this project's history refers to a simple local JSON context
file, not the Anthropic Model Context Protocol.
"""

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONTEXT_PATH = Path(os.getenv("CONTEXT_FILE", "context.json"))

_DEFAULT_STATE: dict[str, Any] = {
    "goal": "",
    "agents": {},
}


def load_context(path: Path = DEFAULT_CONTEXT_PATH) -> dict[str, Any]:
    """Load the shared context file, returning a default structure if absent."""
    if not path.exists():
        return dict(_DEFAULT_STATE)

    with path.open(encoding="utf-8") as f:
        return json.load(f)


def update_context(data: dict[str, Any], path: Path = DEFAULT_CONTEXT_PATH) -> None:
    """Write the shared context file atomically."""
    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp_path.replace(path)


def record_agent_result(agent_name: str, result: str, path: Path = DEFAULT_CONTEXT_PATH) -> None:
    """Record a single agent's result into the shared context file."""
    context = load_context(path)
    context.setdefault("agents", {})[agent_name] = {
        "status": "complete",
        "result": result,
    }
    update_context(context, path)