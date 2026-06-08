"""Placeholder for v1 LLM integration.

v0 intentionally does not call any LLM API. The first stable loop is:
C# file -> static scan -> Markdown report -> manual verification.
"""

from __future__ import annotations


def is_enabled() -> bool:
    """Return False because v0 has no LLM integration."""
    return False
