"""
SUID Validator — validates and parses Sorabbyngo Universal IDs.
Supports all African region codes and optional checksum verification.
"""

import re
from suid.generator import SUID

# Supports: KE001–KE047, UG001, TZ001, RW001, ET001, GH001, NG001, ZA001
# 5-part (with checksum) and 4-part (legacy, no checksum)
_SUID_PATTERN_V2 = re.compile(
    r'^[A-Z]{3}-\d{8}-[A-Z]{2}\d{3}-[A-Z0-9]{6}-[A-Z0-9]{2}$'
)
_SUID_PATTERN_V1 = re.compile(
    r'^[A-Z]{3}-\d{8}-[A-Z]{2}\d{3}-[A-Z0-9]{6}$'
)


def validate(suid: str, verify_checksum: bool = False) -> bool:
    """
    Validate a SUID.

    Args:
        suid:             The SUID string to validate
        verify_checksum:  If True, also verify the embedded checksum.
                          Use this for high-security contexts (transactions, audits).

    Returns:
        True if valid format (and checksum if requested)
    """
    if not isinstance(suid, str):
        return False

    s = suid.strip().upper()

    if not (_SUID_PATTERN_V2.match(s) or _SUID_PATTERN_V1.match(s)):
        return False

    if verify_checksum:
        return SUID.verify(s)

    return True


def parse(suid: str) -> dict:
    """Parse a SUID into its components."""
    return SUID.parse(suid)


def is_tampered(suid: str) -> bool:
    """
    Return True if the SUID checksum fails — indicates possible tampering.
    Only applies to v2 SUIDs (5-part with checksum).
    """
    parsed = SUID.parse(suid)
    return parsed.get("tampered", False)
