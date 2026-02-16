from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Location:
    row: int
    column: int


@dataclass(frozen=True, slots=True)
class Edit:
    location: Location
    end_location: Location
    content: str


@dataclass(frozen=True, slots=True)
class Fix:
    message: str
    applicability: str  # "safe" | "unsafe" | "display"
    edits: list[Edit]


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    filename: str
    url: str | None = None
    fix: Fix | None = None
    fixable: bool = False


@dataclass(frozen=True, slots=True)
class Rule:
    code: str
    name: str
    linter: str
    fixable: bool
    preview: bool
    explanation: str | None = None
    url: str | None = None


@dataclass(frozen=True, slots=True)
class Linter:
    prefix: str
    name: str


@dataclass(frozen=True, slots=True)
class FixResult:
    output: str
    fixed_count: int
    remaining: list[Diagnostic]


@dataclass(frozen=True, slots=True)
class FormatResult:
    source: str
    output: str
    changed: bool
