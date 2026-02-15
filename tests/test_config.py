"""Tests for config resolution — auto-discovery and explicit config paths."""

from __future__ import annotations

import ruff


def test_check_with_explicit_config(tmp_path):
    """Explicit config path overrides defaults."""
    config = tmp_path / "ruff.toml"
    config.write_text('[lint]\nselect = ["E501"]\n')

    # Short line — no E501
    diagnostics = ruff.check("x = 1\n", config=str(config))
    assert len(diagnostics) == 0


def test_check_with_config_selects_rules(tmp_path):
    """Config that selects only E501 should not flag F401."""
    config = tmp_path / "ruff.toml"
    config.write_text('[lint]\nselect = ["E501"]\n')

    diagnostics = ruff.check("import os\n", config=str(config))
    assert all(d.code != "F401" for d in diagnostics)


def test_check_isolated_ignores_config(tmp_path):
    """isolated=True ignores all config files."""
    config = tmp_path / "ruff.toml"
    config.write_text('[lint]\nselect = ["E501"]\n')

    # With isolated=True, default rules apply, including F401
    diagnostics = ruff.check("import os\n", config=str(config), isolated=True)
    assert any(d.code == "F401" for d in diagnostics)


def test_check_override_beats_config(tmp_path):
    """Explicit select= param overrides config selection."""
    config = tmp_path / "ruff.toml"
    config.write_text('[lint]\nselect = ["E501"]\n')

    # Config says E501 only, but explicit select says F401
    diagnostics = ruff.check("import os\n", config=str(config), select=["F401"])
    assert any(d.code == "F401" for d in diagnostics)


def test_format_with_config_line_length(tmp_path):
    """Config line-length is respected."""
    config = tmp_path / "ruff.toml"
    config.write_text("line-length = 40\n")

    long_line = "result = some_function(argument_one, argument_two, argument_three)\n"
    formatted = ruff.format_string(long_line, config=str(config))
    # With 40 char limit, should be reformatted to multiple lines
    assert "\n" in formatted.rstrip("\n")


def test_format_isolated_uses_defaults():
    """isolated=True uses default formatting settings."""
    formatted = ruff.format_string("x=1\n", isolated=True)
    assert formatted == "x = 1\n"


def test_check_nonexistent_config_raises():
    """Passing a nonexistent config file raises ConfigError."""
    import pytest

    with pytest.raises(ruff.ConfigError):
        ruff.check("x = 1\n", config="/nonexistent/ruff.toml")


def test_fix_with_config(tmp_path):
    """fix() respects config file."""
    config = tmp_path / "ruff.toml"
    config.write_text('[lint]\nselect = ["F401"]\n')

    result = ruff.fix("import os\nimport sys\nprint(sys.path)\n", config=str(config))
    assert result.fixed_count >= 1
    assert "import os" not in result.output


def test_fix_isolated(tmp_path):
    """fix() with isolated=True ignores config."""
    result = ruff.fix("import os\n", isolated=True)
    assert result.fixed_count >= 1


def test_format_file_with_config(tmp_path):
    """format_file() respects config."""
    config = tmp_path / "ruff.toml"
    config.write_text("line-length = 40\n")

    py_file = tmp_path / "test.py"
    long_line = "result = some_function(argument_one, argument_two, argument_three)\n"
    py_file.write_text(long_line)

    result = ruff.format_file(py_file, config=str(config), write=False)
    assert result.changed
    assert "\n" in result.output.rstrip("\n")


def test_check_preview_from_config(tmp_path):
    """preview=true in config enables preview rules."""
    config = tmp_path / "ruff.toml"
    config.write_text('preview = true\n[lint]\nselect = ["ALL"]\n')

    # Just verify it doesn't crash and returns diagnostics
    diagnostics = ruff.check("x = 1\n", config=str(config))
    assert isinstance(diagnostics, list)


def test_check_preview_override(tmp_path):
    """Explicit preview= overrides config."""
    config = tmp_path / "ruff.toml"
    config.write_text('preview = false\n[lint]\nselect = ["ALL"]\n')

    # Override preview to True
    diagnostics = ruff.check("x = 1\n", config=str(config), preview=True)
    assert isinstance(diagnostics, list)
