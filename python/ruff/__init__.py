"""pyruff — Native Python API for Ruff linter and formatter."""

from ruff._check import check, check_file, check_paths, fix
from ruff._format import format_file, format_string
from ruff._rules import linters, rule, rules
from ruff._types import (
    Diagnostic,
    Edit,
    Fix,
    FixResult,
    FormatResult,
    Linter,
    Location,
    Rule,
)
from ruff.exceptions import (
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
