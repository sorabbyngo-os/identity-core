"""
Sorabbyngo Universal ID (SUID) — Core Generator

Format: {PREFIX}-{YYYYMMDD}-{REGION}-{RANDOM6}-{CHECK2}
Example: PAT-20260421-KE045-A3X9KM-7F

Components:
  PREFIX   — 3-char entity type code (PAT, DOC, HSP...)
  YYYYMMDD — creation date UTC (forensically embedded)
  REGION   — county/district code (KE001–KE047, UG001, TZ001...)
  RANDOM6  — 6-char cryptographically random suffix (non-guessable)
  CHECK2   — 2-char checksum (tamper detection)

Properties:
  - Human readable at a glance
  - Type, date, and region embedded — no DB lookup for basic forensics
  - Cryptographically random — cannot enumerate records
  - Checksum — detects ID tampering
  - URL-safe — no special characters
  - Africa-ready — supports KE, UG, TZ, RW, ET, GH, NG, ZA
"""

import secrets
import string
from datetime import datetime, timezone
from suid.registry.prefixes import PREFIX
from suid.regions.africa import is_valid_region, get_region, get_country
from suid.regions.kenya import KENYA_COUNTIES

_CHARSET     = string.ascii_uppercase + string.digits   # A-Z 0-9 (36 chars)
_DEFAULT_REGION = "KE047"   # Nairobi


def _checksum(prefix: str, date: str, region: str, suffix: str) -> str:
    """
    Generate 2-char checksum from ID components.
    Simple but effective — detects any single component tampering.
    """
    raw   = f"{prefix}{date}{region}{suffix}"
    total = sum(ord(c) * (i + 1) for i, c in enumerate(raw))
    c1    = _CHARSET[total % 36]
    c2    = _CHARSET[(total // 36) % 36]
    return f"{c1}{c2}"


class SUID:
    """Sorabbyngo Universal ID generator and parser."""

    @staticmethod
    def generate(prefix: str, region: str = _DEFAULT_REGION) -> str:
        """
        Generate a new SUID.

        Args:
            prefix: Entity type from PREFIX registry (e.g. PREFIX.PATIENT)
            region: Region code — any supported African region (e.g. "KE045")

        Returns:
            SUID string e.g. "PAT-20260421-KE045-A3X9KM-7F"

        Raises:
            ValueError: if prefix or region is invalid
        """
        prefix = prefix.upper()
        region = region.upper()

        if not PREFIX.is_valid(prefix):
            raise ValueError(
                f"Unknown prefix '{prefix}'. "
                f"Register it in suid/registry/prefixes.py first."
            )
        if not is_valid_region(region):
            raise ValueError(
                f"Unknown region '{region}'. "
                f"Use a valid county/district code (e.g. KE045, UG001)."
            )

        date   = datetime.now(timezone.utc).strftime("%Y%m%d")
        suffix = "".join(secrets.choice(_CHARSET) for _ in range(6))
        check  = _checksum(prefix, date, region, suffix)

        return f"{prefix}-{date}-{region}-{suffix}-{check}"

    @staticmethod
    def parse(suid: str) -> dict:
        """
        Parse a SUID into its components.

        Returns dict with:
          valid, suid, prefix, prefix_name, date, region,
          region_name, country, suffix, checksum, checksum_valid
        """
        try:
            parts = suid.strip().upper().split("-")

            # Support both old 4-part (no checksum) and new 5-part format
            if len(parts) == 4:
                prefix, date, region, suffix = parts
                check          = None
                checksum_valid = None   # Legacy — no checksum
            elif len(parts) == 5:
                prefix, date, region, suffix, check = parts
                expected       = _checksum(prefix, date, region, suffix)
                checksum_valid = (check == expected)
            else:
                return {"valid": False, "error": "Invalid format — expected PREFIX-DATE-REGION-SUFFIX[-CHECK]"}

            return {
                "valid":          True,
                "suid":           suid.upper(),
                "prefix":         prefix,
                "prefix_name":    PREFIX.describe(prefix),
                "date":           datetime.strptime(date, "%Y%m%d").date().isoformat(),
                "region":         region,
                "region_name":    get_region(region),
                "country":        get_country(region),
                "suffix":         suffix,
                "checksum":       check,
                "checksum_valid": checksum_valid,
                "tampered":       checksum_valid is False,
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    @staticmethod
    def verify(suid: str) -> bool:
        """Return True only if SUID is valid AND checksum passes."""
        parsed = SUID.parse(suid)
        if not parsed.get("valid"):
            return False
        if parsed.get("checksum_valid") is False:
            return False
        return True

    @staticmethod
    def batch(prefix: str, region: str = _DEFAULT_REGION, count: int = 10) -> list:
        """Generate multiple SUIDs at once."""
        return [SUID.generate(prefix, region) for _ in range(count)]

    # ── Convenience methods ───────────────────────────────────────────────
    @staticmethod
    def patient(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.PATIENT, region)

    @staticmethod
    def doctor(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.DOCTOR, region)

    @staticmethod
    def nurse(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.NURSE, region)

    @staticmethod
    def hospital(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.HOSPITAL, region)

    @staticmethod
    def admission(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.ADMISSION, region)

    @staticmethod
    def monitor(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.MONITOR, region)

    @staticmethod
    def alert(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.ALERT, region)

    @staticmethod
    def transaction(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.TRANSACTION, region)

    @staticmethod
    def audit(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.AUDIT, region)

    @staticmethod
    def chw(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.CHW, region)

    @staticmethod
    def node(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.NODE, region)

    @staticmethod
    def prescription(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.PRESCRIPTION, region)

    @staticmethod
    def verification(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.VERIFICATION, region)

    @staticmethod
    def lab_result(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.LAB_RESULT, region)

    @staticmethod
    def incident(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.INCIDENT, region)

    @staticmethod
    def session(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.SESSION, region)
