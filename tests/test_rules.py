import pyruff as ruff


def test_list_all_rules():
    all_rules = ruff.rules()
    assert len(all_rules) > 700


def test_list_rules_with_preview():
    stable = ruff.rules()
    with_preview = ruff.rules(preview=True)
    assert len(with_preview) >= len(stable)


def test_get_rule_f401():
    r = ruff.rule("F401")
    assert r.code == "F401"
    assert r.name == "unused-import"
    assert r.linter == "Pyflakes"
    assert r.fixable is True
    assert r.url is not None


def test_get_rule_e501():
    r = ruff.rule("E501")
    assert r.code == "E501"
    assert r.linter == "pycodestyle"


def test_get_rule_not_found():
    import pytest

    with pytest.raises(ruff.RuleNotFoundError):
        ruff.rule("XXXXX")


def test_rule_has_explanation():
    r = ruff.rule("F401")
    assert r.explanation is not None
    assert len(r.explanation) > 0


def test_linters():
    ls = ruff.linters()
    assert len(ls) > 50
    names = {linter.name for linter in ls}
    assert "Pyflakes" in names
    assert "pycodestyle" in names


def test_linter_has_prefix():
    ls = ruff.linters()
    for linter in ls:
        assert len(linter.prefix) > 0
        assert len(linter.name) > 0
