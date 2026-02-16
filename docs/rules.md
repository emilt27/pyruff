# Rules API

## `pyruff.rules()`

List all available ruff rules.

```python
def rules(*, preview: bool = False) -> list[Rule]
```

### Example

```python
import pyruff

all_rules = pyruff.rules()
print(f"Total: {len(all_rules)} rules")

# Include preview rules
all_including_preview = pyruff.rules(preview=True)
```

## `pyruff.rule()`

Get detailed information about a specific rule.

```python
def rule(code: str) -> Rule
```

### Example

```python
r = pyruff.rule("F401")
print(r.code)         # "F401"
print(r.name)         # "unused-import"
print(r.linter)       # "Pyflakes"
print(r.fixable)      # True
print(r.explanation)  # Detailed explanation text
print(r.url)          # Link to docs
```

Raises `RuleNotFoundError` for unknown rule codes.

## `pyruff.linters()`

List all supported linters.

```python
def linters() -> list[Linter]
```

### Example

```python
for linter in pyruff.linters():
    print(f"{linter.prefix}: {linter.name}")
# F: Pyflakes
# E: pycodestyle
# ...
```

## Types

### `Rule`

```python
@dataclass(frozen=True, slots=True)
class Rule:
    code: str               # "F401"
    name: str               # "unused-import"
    linter: str             # "Pyflakes"
    fixable: bool
    preview: bool
    explanation: str | None
    url: str | None
```

### `Linter`

```python
@dataclass(frozen=True, slots=True)
class Linter:
    prefix: str    # "F"
    name: str      # "Pyflakes"
```
