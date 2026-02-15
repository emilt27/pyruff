# Linting API

## `ruff.check()`

Run the ruff linter on a source code string.

```python
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
) -> list[Diagnostic]
```

### Parameters

- **source** — Python source code to lint
- **filename** — Filename for context (affects file-type detection and config discovery)
- **config** — Path to a `ruff.toml` or `pyproject.toml` config file. If not set, auto-discovers config by walking up from `filename` or CWD
- **isolated** — If `True`, ignore all config files and use default settings
- **select** — Rule codes/prefixes to enable (replaces defaults). E.g., `["E", "F", "W"]`
- **ignore** — Rule codes/prefixes to disable. E.g., `["F401"]`
- **extend_select** — Additional rules on top of defaults/config
- **target_version** — Python version target: `"py37"` through `"py314"`
- **preview** — Enable (`True`) or disable (`False`) preview rules. `None` defers to config
- **ignore_noqa** — Ignore `# noqa` comments

### Examples

```python
import ruff

# Basic check (auto-discovers config)
diagnostics = ruff.check("import os\n")
assert diagnostics[0].code == "F401"

# Explicit config file
diagnostics = ruff.check("import os\n", config="path/to/ruff.toml")

# Ignore all config, use defaults
diagnostics = ruff.check("import os\n", isolated=True)

# Select specific rules
diagnostics = ruff.check("x=1\n", select=["E", "W"])

# Ignore specific rules
diagnostics = ruff.check("import os\n", ignore=["F401"])
assert len(diagnostics) == 0
```

## `ruff.check_file()`

Lint a file from disk.

```python
diagnostics = ruff.check_file("main.py")

# With explicit config
diagnostics = ruff.check_file("main.py", config="ruff.toml")
```

## `ruff.check_paths()`

Lint multiple files/directories.

```python
results = ruff.check_paths(["src/", "tests/"])
for path, diagnostics in results.items():
    for d in diagnostics:
        print(f"{path}:{d.code}: {d.message}")
```

## `ruff.fix()`

Apply auto-fixes to source code.

```python
def fix(
    source: str,
    *,
    filename: str = "<stdin>",
    config: str | Path | None = None,
    isolated: bool = False,
    unsafe_fixes: bool = False,
    # ... same selection options as check()
) -> FixResult
```

### Example

```python
result = ruff.fix("import os\nimport sys\nprint(sys.path)\n")
print(result.output)        # Fixed code without unused import
print(result.fixed_count)   # Number of fixes applied
print(result.remaining)     # Unfixed diagnostics
```

## Types

### `Diagnostic`

```python
@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str           # "F401"
    message: str        # "`os` imported but unused"
    filename: str
    url: str | None     # Link to rule docs
    fixable: bool       # Whether a fix is available
```

### `FixResult`

```python
@dataclass(frozen=True, slots=True)
class FixResult:
    output: str                    # Fixed source code
    fixed_count: int               # Number of violations fixed
    remaining: list[Diagnostic]    # Violations that couldn't be fixed
```
