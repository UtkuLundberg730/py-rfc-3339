"""Package init: re-export the public API."""

from .core import is_rfc3339, validate_rfc3339

__all__ = ["is_rfc3339", "validate_rfc3339"]
