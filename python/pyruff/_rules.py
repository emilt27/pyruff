from __future__ import annotations

from pyruff._native import get_rule as _get_rule
from pyruff._native import get_rules as _get_rules
from pyruff._types import Linter, Rule


def _raw_to_rule(raw: dict) -> Rule:
    return Rule(
        code=raw["code"],
        name=raw["name"],
        linter=raw["linter"],
        fixable=raw["fixable"],
        preview=raw["preview"],
        explanation=raw.get("explanation"),
        url=raw.get("url"),
    )


def rules(*, preview: bool = False) -> list[Rule]:
    """List all available ruff rules."""
    return [_raw_to_rule(r) for r in _get_rules(preview=preview)]


def rule(code: str) -> Rule:
    """Get detailed info about a specific rule."""
    return _raw_to_rule(_get_rule(code))


def linters() -> list[Linter]:
    """List all supported linters."""
    seen = {}
    for r in _get_rules(preview=True):
        linter_name = r["linter"]
        code = r["code"]
        prefix = "".join(c for c in code if c.isalpha())
        if prefix not in seen:
            seen[prefix] = Linter(prefix=prefix, name=linter_name)
    return list(seen.values())
