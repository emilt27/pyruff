# Upgrading Ruff Version

pyruff's version always matches the ruff version it's built against (pyruff `0.15.1` = ruff `0.15.1`).
When a new ruff version is released, pyruff needs to be updated accordingly.

## Step-by-Step Guide

Assume we're upgrading from `0.15.1` to `0.16.0`.

### 1. Review ruff release notes

Open https://github.com/astral-sh/ruff/releases and review the changes.
Pay attention to:
- Breaking changes in internal crates (new/removed function parameters)
- New rules or linters
- Changes to `LinterSettings`, `PyFormatOptions`, `Diagnostic` API
- Minimum Supported Rust Version (MSRV) changes

### 2. Update versions in Cargo.toml

Replace the tag in **all** git deps:

```toml
# Cargo.toml
[package]
version = "0.16.0"  # <-- change

[dependencies]
ruff_linter = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }           # <-- change
ruff_python_formatter = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }  # <-- change
ruff_workspace = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }         # <-- change
ruff_python_parser = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }     # <-- change
ruff_source_file = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }       # <-- change
ruff_text_size = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }         # <-- change
ruff_python_ast = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }        # <-- change
ruff_db = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }                # <-- change
ruff_formatter = { git = "https://github.com/astral-sh/ruff", tag = "0.16.0" }         # <-- change
```

Quick replacement with sed:
```bash
sed -i '' 's/tag = "0.15.1"/tag = "0.16.0"/g' Cargo.toml
```

### 3. Update version in pyproject.toml

```toml
[project]
version = "0.16.0"  # <-- change
```

### 4. Delete Cargo.lock

```bash
rm Cargo.lock
```

This forces Cargo to re-resolve all dependencies.

### 5. Check MSRV (Minimum Supported Rust Version)

Ruff may require a newer Rust version. Check:
```bash
cargo check 2>&1 | grep "requires rustc"
```

If a newer version is needed, update `rust-toolchain.toml`:
```toml
[toolchain]
channel = "1.XX.0"  # required version
```

And install it:
```bash
rustup install 1.XX.0
```

### 6. Try building

```bash
maturin develop
```

### 7. Fix compilation errors

Common changes that may break:

**Function signature changed:**
```
error[E0061]: this method takes N arguments but M arguments were supplied
```
Check the new signature in ruff source code:
```
https://raw.githubusercontent.com/astral-sh/ruff/refs/tags/0.16.0/crates/ruff_linter/src/linter.rs
```

**Type moved to a different module:**
```
error[E0432]: unresolved import
```
The compiler usually suggests the correct path in the `help:` message.

**Type renamed or removed:**
```
error[E0599]: no method named `...` found
```
Check the new API in release notes or source code.

Files most likely to need changes:
- `src/check.rs` — `lint_only()`, `lint_fix()`, `LinterSettings`, `Diagnostic`
- `src/format.rs` — `format_module_source()`, `PyFormatOptions`
- `src/rules.rs` — `Rule` enum, `FixAvailability`

### 8. Update linter mapping (if new linters were added)

If ruff added new linter prefixes, add them to `rule_linter_name()` in `src/rules.rs`.

### 9. Update PythonVersion mapping (if a new Python version was added)

Check `ruff_python_ast::PythonVersion` — if new variants were added (e.g., `PY315`), add them to:
- `src/format.rs` → `parse_python_version()`
- `src/check.rs` → `apply_overrides()` (PythonVersion match block)

### 10. Run tests

```bash
maturin develop
pytest tests/ -v
```

If the number of rules changed, update `test_list_all_rules()` in `tests/test_rules.py`.

### 11. Commit and tag

```bash
git add -A
git commit -m "Upgrade ruff to 0.16.0"
git tag v0.16.0
git push origin main --tags
```

CI will automatically build wheels and publish to PyPI.

## Checklist

- [ ] Review ruff release notes
- [ ] Update tag in `Cargo.toml` (all 9 crates)
- [ ] Update version in `Cargo.toml`
- [ ] Update version in `pyproject.toml`
- [ ] Delete `Cargo.lock`
- [ ] Check MSRV, update `rust-toolchain.toml` if needed
- [ ] `maturin develop` — build successfully
- [ ] Fix compilation errors in `src/`
- [ ] Add new linter prefixes in `src/rules.rs` (if any)
- [ ] Add new PythonVersion variants (if any)
- [ ] `pytest tests/ -v` — all tests pass
- [ ] Commit, create tag, push
