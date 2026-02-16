"""pyruff — Native Python API for Ruff linter and formatter."""

from pyruff._check import check, check_file, check_paths, fix
from pyruff._format import format_file, format_string
from pyruff._rules import linters, rule, rules
from pyruff._types import (
    Diagnostic,
    Edit,
    Fix,
    FixResult,
    FormatResult,
    Linter,
    Location,
    Rule,
)
from pyruff.exceptions import (
    ConfigError,
    ParseError,
    RuffError,
    RuleNotFoundError,
)

__all__ = [
    # Check / Fix
    "check",
    "check_file",
    "check_paths",
    "fix",
    # Format
    "format_string",
    "format_file",
    # Rules
    "rules",
    "rule",
    "linters",
    # Types
    "Diagnostic",
    "Edit",
    "Fix",
    "FixResult",
    "FormatResult",
    "Linter",
    "Location",
    "Rule",
    # Exceptions
    "RuffError",
    "ParseError",
    "ConfigError",
    "RuleNotFoundError",
]
