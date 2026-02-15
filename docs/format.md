# Formatting API

## `ruff.format_string()`

Format a Python source code string.

```python
def format_string(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | Path | None = None,
    isolated: bool = False,
    line_length: int | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
) -> str
```

### Parameters

- **source** — Python source code to format
- **filename** — Filename for context (affects .pyi handling and config discovery)
- **config** — Path to a `ruff.toml` or `pyproject.toml` config file. If not set, auto-discovers config by walking up from `filename` or CWD
- **isolated** — If `True`, ignore all config files and use default settings
- **line_length** — Maximum line length (default: 88). Overrides config value
- **target_version** — Python version target: `"py37"` through `"py314"`. Overrides config value
- **preview** — Enable (`True`) or disable (`False`) preview formatting. `None` defers to config

### Examples

```python
import ruff

# Basic formatting (auto-discovers config)
formatted = ruff.format_string("x=1\n")
assert formatted == "x = 1\n"

# Explicit config file
formatted = ruff.format_string("x=1\n", config="ruff.toml")

# Ignore all config, use defaults
formatted = ruff.format_string("x=1\n", isolated=True)

# Custom line length (overrides config)
formatted = ruff.format_string(long_code, line_length=120)

# Format as .pyi stub
formatted = ruff.format_string(code, filename="types.pyi")
```

## `ruff.format_file()`

Format a file on disk.

```python
def format_file(
    path: str | Path,
    *,
    write: bool = True,
    config: str | Path | None = None,
    isolated: bool = False,
    line_length: int | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
) -> FormatResult
```

### Parameters

- **path** — Path to the Python file
- **write** — Whether to write back to file (default: True)
- Other parameters same as `format_string()`

### Example

```python
result = ruff.format_file("main.py")
print(result.changed)  # True if formatting changed anything
print(result.output)   # Formatted source

# Check only, don't write
result = ruff.format_file("main.py", write=False)
```

## Types

### `FormatResult`

```python
@dataclass(frozen=True, slots=True)
class FormatResult:
    source: str       # Original source
    output: str       # Formatted source
    changed: bool     # Whether formatting changed anything
```
