from __future__ import annotations

from pathlib import Path

from ruff._native import check_source as _check_source
from ruff._native import fix_source as _fix_source
from ruff._types import Diagnostic, FixResult


def _raw_to_diagnostic(raw: dict, filename: str) -> Diagnostic:
    return Diagnostic(
        code=raw.get("code", ""),
        message=raw.get("message", ""),
        filename=filename,
        url=raw.get("url"),
        fixable=raw.get("fixable", False),
    )


def check(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | Path | None = None,
    isolated: bool = False,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    extend_select: list[str] | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
    ignore_noqa: bool = False,
) -> list[Diagnostic]:
    """Run ruff linter on source code string. Returns list of diagnostics.

    By default, auto-discovers ruff.toml / pyproject.toml config from CWD.
    Pass config= for explicit config path, or isolated=True to ignore all configs.
    Explicit params (select, ignore, etc.) override config values.
    """
    raw = _check_source(
        source,
        filename=filename,
        config=str(config) if config is not None else None,
        isolated=isolated,
        select=select,
        ignore=ignore,
        extend_select=extend_select,
        target_version=target_version,
        preview=preview,
        ignore_noqa=ignore_noqa,
    )
    return [_raw_to_diagnostic(d, filename) for d in raw]


def check_file(
    path: str | Path,
    **kwargs,
) -> list[Diagnostic]:
    """Run ruff linter on a file."""
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    kwargs.setdefault("filename", str(path))
    return check(source, **kwargs)


def check_paths(
    paths: list[str | Path],
    **kwargs,
) -> dict[str, list[Diagnostic]]:
    """Run ruff linter on multiple files."""
    result = {}
    for p in paths:
        p = Path(p)
        if p.is_file():
            result[str(p)] = check_file(p, **kwargs)
        elif p.is_dir():
            for f in sorted(p.rglob("*.py")):
                result[str(f)] = check_file(f, **kwargs)
    return result


def fix(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | Path | None = None,
    isolated: bool = False,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    extend_select: list[str] | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
    ignore_noqa: bool = False,
    unsafe_fixes: bool = False,
) -> FixResult:
    """Apply fixes and return result.

    By default, auto-discovers ruff.toml / pyproject.toml config.
    """
    raw = _fix_source(
        source,
        filename=filename,
        config=str(config) if config is not None else None,
        isolated=isolated,
        select=select,
        ignore=ignore,
        extend_select=extend_select,
        target_version=target_version,
        preview=preview,
        ignore_noqa=ignore_noqa,
        unsafe_fixes=unsafe_fixes,
    )
    remaining = [_raw_to_diagnostic(d, filename) for d in raw.get("remaining", [])]
    return FixResult(
        output=raw["output"],
        fixed_count=raw.get("fixed_count", 0),
        remaining=remaining,
    )
