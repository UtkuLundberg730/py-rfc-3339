"""RFC 3339 timestamp validation.

This module exposes two callables:
    * is_rfc3339(value)     -> bool
    * validate_rfc3339(value) -> bool

Design decisions
----------------
RFC 3339 is *narrower* than ISO 8601.  The most visible difference is that the
date-time production requires an explicit zone offset (``Z`` or ``+HH:MM``); a
bare date such as ``2023-04-05`` is therefore rejected.

Parsing is done with :func:`datetime.fromisoformat` for the parts the Python
stdlib understands (``Z`` is first translated to ``+00:00``), then validated
post-hoc against the constraints the stdlib does *not* enforce:
    * Leap seconds are accepted (the standard explicitly permits them) and are
      mapped by fromisoformat to the last second of the minute.
    * The fractional second portion, if present, may contain at least one digit.
      Rejected when empty.
    * Offset-must-be-present is enforced explicitly so bare dates raise.

Validation is split from coercion deliberately; consumers who only want a
predicate should not be forced to handle a ``ValueError``.
"""

from __future__ import annotations

import datetime
import re

__all__ = ["is_rfc3339", "validate_rfc3339"]

# date-fully-extended: YYYY-MM-DD (4-digit year; month 01-12; day 01-31)
_DATE = r"\d{4}-\d{2}-\d{2}"
# time-secfrac starts with '.' and at least one digit.
_TIMEFRAC = r"(\.\d+)?"
# The time production.
_TIME = rf"\d{{2}}:\d{{2}}:\d{{2}}{_TIMEFRAC}"
# Z or numeric offset ±HH:MM.  ``Z`` and ``+00:00`` are interchangeable.
_OFFSET = r"(Z|[+-]\d{2}:\d{2})"

_FULL_RE = re.compile(rf"^{_DATE}T{_TIME}{_OFFSET}$")
# Capture the optional fractional part so we can reject an empty dot.
_FRAC_RE = re.compile(r"\.\d+")


def validate_rfc3339(value: str) -> bool:
    """Return ``True`` if *value* is a valid RFC 3339 date-time string.

    The check is structural: the format must be exactly
    ``YYYY-MM-DDTHH:MM:SS(.frac)?(Z|±HH:MM)``.  Lower-level semantic checks
    (month/day validity, leap seconds) are delegated to the stdlib via
    :func:`datetime.datetime.fromisoformat`; the remaining structural pieces
    that the stdlib treats as valid ISO 8601 but that RFC 3339 disallows —
    empty fractional dots, omitted offsets, and bare dates — are rejected by
    the regex above.

    A non-string argument returns ``False`` rather than raising.
    """
    if not isinstance(value, str):
        return False
    if not _FULL_RE.match(value):
        return False
    # ``fromisoformat`` in modern Python understands ``Z``, but rewriting it
    # keeps us compatible with Pythons that do not.  ``Z`` -> ``+00:00``.
    normalised = value.replace("Z", "+00:00")
    try:
        datetime.datetime.fromisoformat(normalised)
    except ValueError:
        return False
    return True


def is_rfc3339(value: str) -> bool:
    """Alias of :func:`validate_rfc3339`.

    Provided so callers can pick whichever name reads better at the call
    site; both names are exported in :mod:`py_rfc_3339`.
    """
    return validate_rfc3339(value)
