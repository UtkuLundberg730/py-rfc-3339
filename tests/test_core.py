"""Tests for :mod:`py_rfc_3339.core`.

The suite is intentionally small but exercises the awkward cases:
fractional seconds, Z vs numeric offset, bare dates,
and non-string input.
"""

from __future__ import annotations

import unittest

from py_rfc_3339 import is_rfc3339, validate_rfc3339


class TestValid(unittest.TestCase):
    def test_zulu(self) -> None:
        self.assertTrue(validate_rfc3339("2023-04-05T14:30:00Z"))

    def test_numeric_offset(self) -> None:
        self.assertTrue(validate_rfc3339("2023-04-05T14:30:00+05:30"))

    def test_negative_offset(self) -> None:
        self.assertTrue(validate_rfc3339("2023-04-05T14:30:00-08:00"))

    def test_fractional_seconds(self) -> None:
        self.assertTrue(validate_rfc3339("2023-04-05T14:30:00.123456Z"))

    def test_single_digit_fraction(self) -> None:
        self.assertTrue(validate_rfc3339("2023-04-05T14:30:00.5Z"))


class TestInvalid(unittest.TestCase):
    def test_empty_string(self) -> None:
        self.assertFalse(validate_rfc3339(""))

    def test_non_string(self) -> None:
        self.assertFalse(validate_rfc3339(None))  # type: ignore[arg-type]
        self.assertFalse(validate_rfc3339(42))   # type: ignore[arg-type]

    def test_bare_date(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-05"))

    def test_space_separator(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-05 14:30:00Z"))

    def test_missing_offset(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-05T14:30:00"))

    def test_empty_fraction(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-05T14:30:00.Z"))

    def test_invalid_month(self) -> None:
        self.assertFalse(validate_rfc3339("2023-13-05T14:30:00Z"))

    def test_invalid_day(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-32T14:30:00Z"))

    def test_offset_without_colon(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-05T14:30:00+0500"))

    def test_lowercase_z_rejected(self) -> None:
        self.assertFalse(validate_rfc3339("2023-04-05T14:30:00z"))

    def test_leap_second_rejected(self) -> None:
        self.assertFalse(validate_rfc3339("2016-12-31T23:59:60Z"))


class TestAlias(unittest.TestCase):
    def test_alias_equivalent(self) -> None:
        self.assertEqual(is_rfc3339("2023-04-05T14:30:00Z"), True)
        self.assertEqual(is_rfc3339("nope"), False)


if __name__ == "__main__":
    unittest.main()
