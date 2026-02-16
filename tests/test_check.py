import pyruff as ruff


def test_check_unused_import(unused_import_code):
    diagnostics = ruff.check(unused_import_code)
    assert len(diagnostics) == 1
    assert diagnostics[0].code == "F401"
    assert "os" in diagnostics[0].message
    assert diagnostics[0].fixable is True


def test_check_no_violations(clean_code):
    diagnostics = ruff.check(clean_code)
    assert diagnostics == []


def test_check_multiple_violations(multi_violation_code):
    diagnostics = ruff.check(multi_violation_code)
    codes = {d.code for d in diagnostics}
    assert "F401" in codes


def test_check_with_select():
    code = "x=1\nimport os\n"
    # Select only pycodestyle E rules
    diagnostics = ruff.check(code, select=["E"])
    codes = {d.code for d in diagnostics}
    # Should not have F401 (Pyflakes), only E rules
    assert "F401" not in codes


def test_check_with_ignore():
    code = "import os\n"
    diagnostics = ruff.check(code, ignore=["F401"])
    assert len(diagnostics) == 0


def test_check_with_extend_select():
    code = "x = 1\n"
    # Default rules + extend with additional ones
    d1 = ruff.check(code)
    d2 = ruff.check(code, extend_select=["ALL"])
    assert len(d2) >= len(d1)


def test_check_ignore_noqa():
    code = "import os  # noqa: F401\n"
    # With noqa respected
    d1 = ruff.check(code)
    assert len(d1) == 0
    # With noqa ignored
    d2 = ruff.check(code, ignore_noqa=True)
    assert len(d2) == 1


def test_check_file(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("import os\n")
    diagnostics = ruff.check_file(f)
    assert len(diagnostics) == 1
    assert diagnostics[0].code == "F401"


def test_check_paths(tmp_path):
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.py"
    f1.write_text("import os\n")
    f2.write_text("x = 1\n")
    result = ruff.check_paths([tmp_path])
    assert str(f1) in result
    assert str(f2) in result
    assert len(result[str(f1)]) == 1
    assert len(result[str(f2)]) == 0


def test_fix_removes_unused_import(fixable_code):
    result = ruff.fix(fixable_code)
    assert "import os" not in result.output
    assert "import sys" in result.output
    assert result.fixed_count > 0


def test_fix_no_changes_needed(clean_code):
    result = ruff.fix(clean_code)
    assert result.output == clean_code
    assert result.fixed_count == 0
    assert result.remaining == []
