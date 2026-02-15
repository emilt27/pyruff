# pyruff

Native Python API for the [Ruff](https://github.com/astral-sh/ruff) linter and formatter.

pyruff compiles Ruff's Rust crates directly into a Python extension module via [PyO3](https://pyo3.rs/) and [Maturin](https://www.maturin.rs/). No `ruff` CLI needed at runtime — everything runs natively in-process with zero overhead.

## Installation

```bash
pip install pyruff
```

## Quick Start

```python
import ruff

# Format code
formatted = ruff.format_string("x=1\n")
# "x = 1\n"

# Lint code
diagnostics = ruff.check("import os\n")
for d in diagnostics:
    print(f"{d.code}: {d.message}")
# F401: `os` imported but unused

# Auto-fix violations
result = ruff.fix("import os\nimport sys\nprint(sys.path)\n")
print(result.output)
# import sys\nprint(sys.path)\n

# List rules
all_rules = ruff.rules()
r = ruff.rule("F401")
print(f"{r.code}: {r.name} ({r.linter})")
```

## Features

- **Linting** — `check()`, `check_file()`, `check_paths()` with full rule selection
- **Auto-fix** — `fix()` with safe/unsafe fix support
- **Formatting** — `format_string()`, `format_file()` with all formatting options
- **Rules** — `rules()`, `rule()`, `linters()` for rule metadata and introspection
- **Config resolution** — Automatically discovers `ruff.toml` / `pyproject.toml` config, just like `ruff` CLI
- **Python 3.12 — 3.14** support

## Config Resolution

pyruff automatically discovers and applies your existing ruff configuration:

```python
# Auto-discovers ruff.toml / pyproject.toml from CWD
diagnostics = ruff.check("import os\n")

# Explicit config path
diagnostics = ruff.check("import os\n", config="path/to/ruff.toml")

# Ignore all config, use defaults
diagnostics = ruff.check("import os\n", isolated=True)

# Explicit params override config values
formatted = ruff.format_string(code, line_length=120)
```

## Versioning

pyruff's version matches the ruff version it's built against.
For example, `pyruff==0.15.1` uses ruff `0.15.1` crates internally.

## Documentation

- [Getting Started](docs/getting-started.md)
- [Linting API](docs/check.md) — `check()`, `fix()`, `check_file()`, `check_paths()`
- [Formatting API](docs/format.md) — `format_string()`, `format_file()`
- [Rules API](docs/rules.md) — `rules()`, `rule()`, `linters()`
- [Configuration](docs/config.md) — Config discovery and resolution
- [Upgrading Ruff](UPGRADE_RUFF.md) — Step-by-step guide for ruff version upgrades

## Development

### Prerequisites

- **Python 3.12+** (3.14 supported)
- **Rust 1.91+** (install via [rustup](https://rustup.rs/))
- **Maturin** (Python build tool for Rust extensions)

### Setup

```bash
# Clone the repo
git clone https://github.com/your-org/pyruff.git
cd pyruff

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dev dependencies
pip install maturin pytest ruff
```

### Build

```bash
# Development build (debug, installed in .venv)
maturin develop

# Or use the helper script
bin/build
```

### Run Tests

```bash
pytest tests/ -v

# Or use the helper script
bin/test
```

### Linting & Formatting

```bash
# Rust
cargo fmt --check
cargo clippy -- -D warnings

# Python
ruff check python/ tests/
ruff format --check python/ tests/

# Or use the helper scripts
bin/lint
bin/fmt-check
```

### Helper Scripts

The `bin/` directory contains convenience scripts for common dev tasks:

| Script | Description |
|---|---|
| `bin/build` | Build and install in dev mode |
| `bin/test` | Run all tests |
| `bin/lint` | Run all linters (Rust + Python) |
| `bin/fmt` | Format all code (Rust + Python) |
| `bin/fmt-check` | Check formatting without changes |
| `bin/ci` | Run full CI pipeline locally |

### Release

Releases are automated via GitHub Actions. To release a new version:

1. Update version in `Cargo.toml` and `pyproject.toml`
2. Commit and push
3. Create a git tag: `git tag v0.15.1 && git push origin --tags`
4. CI builds wheels for Linux/macOS/Windows and publishes to PyPI

## License

MIT
