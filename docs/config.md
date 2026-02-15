# Configuration

pyruff automatically discovers and applies ruff configuration, just like the `ruff` CLI does.

## Config Discovery

When no explicit `config` parameter is passed, pyruff searches for configuration files by walking up from the source file's directory (or CWD for `<stdin>`):

1. `.ruff.toml`
2. `ruff.toml`
3. `pyproject.toml` (with `[tool.ruff]` section)

If no project-level config is found, it also checks for user-level config (`~/.config/ruff/ruff.toml` on Linux/macOS).

## Usage

### Auto-discovery (default)

```python
import ruff

# Automatically finds ruff.toml / pyproject.toml from CWD
diagnostics = ruff.check("import os\n")
formatted = ruff.format_string("x=1\n")
```

### Explicit config file

```python
diagnostics = ruff.check("import os\n", config="path/to/ruff.toml")
formatted = ruff.format_string("x=1\n", config="path/to/pyproject.toml")
```

### Isolated mode (ignore all config)

```python
diagnostics = ruff.check("import os\n", isolated=True)
formatted = ruff.format_string("x=1\n", isolated=True)
```

### Override config values

Explicit parameters always override config values:

```python
# Config might say line-length = 88, but this overrides to 120
formatted = ruff.format_string(code, line_length=120)

# Config might have select = ["E"], but this overrides to ["F"]
diagnostics = ruff.check(code, select=["F"])
```

## Supported config options

pyruff reads the same configuration format as the `ruff` CLI. Commonly used options:

```toml
# ruff.toml
line-length = 88
target-version = "py312"
preview = false

[lint]
select = ["E", "F", "W"]
ignore = ["E501"]
extend-select = ["I"]

[format]
quote-style = "double"
indent-style = "space"
```

See the [ruff configuration docs](https://docs.astral.sh/ruff/configuration/) for the full list of options.
