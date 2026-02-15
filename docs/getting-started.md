# Getting Started

## Installation

```bash
pip install pyruff
```

## Quick Start

### Format Python code

```python
import ruff

formatted = ruff.format_string("x=1\n")
print(formatted)  # "x = 1\n"
```

### Lint Python code

```python
import ruff

diagnostics = ruff.check("import os\n")
for d in diagnostics:
    print(f"{d.code}: {d.message}")
# F401: `os` imported but unused
```

### Auto-fix violations

```python
import ruff

result = ruff.fix("import os\nimport sys\nprint(sys.path)\n")
print(result.output)
# import sys
# print(sys.path)
```

### List all rules

```python
import ruff

rules = ruff.rules()
print(f"Total rules: {len(rules)}")

r = ruff.rule("F401")
print(f"{r.code}: {r.name} ({r.linter})")
```

### Use config files

```python
import ruff

# Auto-discovers ruff.toml / pyproject.toml from CWD
diagnostics = ruff.check("import os\n")

# Explicit config path
diagnostics = ruff.check("import os\n", config="ruff.toml")

# Ignore all config files
diagnostics = ruff.check("import os\n", isolated=True)
```

## How It Works

pyruff compiles ruff's Rust crates directly into a Python extension module via [PyO3](https://pyo3.rs/) and [Maturin](https://www.maturin.rs/). No `ruff` CLI is needed at runtime — everything runs natively in-process.

## Versioning

pyruff's version matches the ruff version it's built against. For example, `pyruff==0.15.1` uses ruff `0.15.1` crates internally.
