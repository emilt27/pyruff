from __future__ import annotations

from pathlib import Path

from pyruff._native import format_string as _format_string
from pyruff._types import FormatResult


def format_string(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | Path | None = None,
    isolated: bool = False,
    line_length: int | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
) -> str:
    """Format Python source code string.

    By default, auto-discovers ruff.toml / pyproject.toml config from CWD.
    Pass config= for explicit config path, or isolated=True to ignore all configs.
    """
    return _format_string(
        source,
        filename=filename,
        config=str(config) if config is not None else None,
        isolated=isolated,
        line_length=line_length,
        target_version=target_version,
        preview=preview,
    )


def format_file(
    path: str | Path,
    *,
    write: bool = True,
    config: str | Path | None = None,
    isolated: bool = False,
    line_length: int | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
) -> FormatResult:
    """Format a file. Returns FormatResult with source, output, and changed flag.

    By default, auto-discovers ruff.toml / pyproject.toml config.
    """
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    output = format_string(
        source,
        filename=str(path),
        config=config,
        isolated=isolated,
        line_length=line_length,
        target_version=target_version,
        preview=preview,
    )
    changed = source != output
    if write and changed:
        path.write_text(output, encoding="utf-8")
    return FormatResult(source=source, output=output, changed=changed)
