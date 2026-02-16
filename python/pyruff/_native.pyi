"""Type stubs for the native Rust module."""

def format_string(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | None = None,
    isolated: bool = False,
    line_length: int | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
) -> str: ...
def check_source(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | None = None,
    isolated: bool = False,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    extend_select: list[str] | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
    ignore_noqa: bool = False,
) -> list[dict]: ...
def fix_source(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | None = None,
    isolated: bool = False,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    extend_select: list[str] | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
    ignore_noqa: bool = False,
    unsafe_fixes: bool = False,
) -> dict: ...
def get_rules(*, preview: bool = False) -> list[dict]: ...
def get_rule(code: str) -> dict: ...

# Exceptions
class RuffError(Exception): ...
class ParseError(RuffError): ...
class ConfigError(RuffError): ...
class RuleNotFoundError(RuffError): ...
