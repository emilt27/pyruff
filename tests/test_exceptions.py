import pytest

import pyruff as ruff


def test_ruff_error_hierarchy():
    assert issubclass(ruff.ParseError, ruff.RuffError)
    assert issubclass(ruff.ConfigError, ruff.RuffError)
    assert issubclass(ruff.RuleNotFoundError, ruff.RuffError)


def test_rule_not_found_error():
    with pytest.raises(ruff.RuleNotFoundError):
        ruff.rule("INVALID999")


def test_parse_error_on_format():
    # Incomplete syntax that can't be formatted
    with pytest.raises(ruff.ParseError):
        ruff.format_string("def f(\n")
