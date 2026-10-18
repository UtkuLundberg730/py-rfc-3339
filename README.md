# py-rfc-3339

Validates strings against the RFC 3339 date-time format. Returns a plain
boolean; no exceptions, no date objects.

## Usage

```python
from py_rfc_3339 import is_rfc3339, validate_rfc3339

assert is_rfc3339("2023-04-05T14:30:00Z") is True
assert validate_rfc3339("2023-04-05") is False
```

The two names are aliases; pick whichever reads better at the call site.

## Why

Stdlib `datetime.fromisoformat` accepts a *superset* of RFC 3339 — bare
dates, space separators, and lowercase `z` all parse. Code that validates
user input (e.g. JSON Schema `date-time`) needs the narrower contract.
This library enforces it with a small regex and a delegated `fromisoformat`
call for calendar sanity, so behaviour tracks the Python version without
reimplementing it.

The trade-off: leap seconds (e.g. `23:59:60`) are accepted because the
standard permits them and `fromisoformat` clamps them silently; the input is
structural-valid, not necessarily representable as a real `datetime`.

## Edge

Pass a non-string and you get `False`, not a `TypeError`.
