import ruff


def test_format_string_basic(unformatted_code):
    result = ruff.format_string(unformatted_code)
    assert result == "x = 1\n"


def test_format_string_already_formatted(clean_code):
    result = ruff.format_string(clean_code)
    assert result == clean_code


def test_format_string_idempotent():
    code = "x = 1\ny = 2\n"
    first = ruff.format_string(code)
    second = ruff.format_string(first)
    assert first == second


def test_format_string_multiline():
    code = "result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five)\n"
    result = ruff.format_string(code, line_length=40)
    assert "\n" in result.rstrip("\n")


def test_format_string_with_line_length():
    code = "x = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}\n"
    short = ruff.format_string(code, line_length=30)
    long = ruff.format_string(code, line_length=120)
    assert len(short.splitlines()) > len(long.splitlines())


def test_format_file(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x=1\n")
    result = ruff.format_file(f)
    assert result.changed is True
    assert result.output == "x = 1\n"
    assert f.read_text() == "x = 1\n"


def test_format_file_no_write(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x=1\n")
    result = ruff.format_file(f, write=False)
    assert result.changed is True
    assert f.read_text() == "x=1\n"  # Not modified


def test_format_file_no_change(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x = 1\n")
    result = ruff.format_file(f)
    assert result.changed is False
