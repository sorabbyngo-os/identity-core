"""
SUID Validator — validates and parses Sorabbyngo Universal IDs.
"""
import re
from suid.generator import SUID

_SUID_PATTERN = re.compile(r'^[A-Z]{3}-\d{8}-KE\d{3}-[A-Z0-9]{6}$')


def validate(suid: str) -> bool:
    """Return True if the string is a valid SUID format."""
    if not isinstance(suid, str):
        return False
    return bool(_SUID_PATTERN.match(suid.strip().upper()))


def parse(suid: str) -> dict:
    """Parse a SUID into its components."""
    return SUID.parse(suid)
