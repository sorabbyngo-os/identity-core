"""
Sorabbyngo Universal ID (SUID) — Core Generator

Format: {PREFIX}-{YYYYMMDD}-{REGION}-{RANDOM6}
Example: PAT-20260420-KE047-A3X9KM

Components:
  PREFIX   — 3-char entity type code
  YYYYMMDD — creation date (UTC)
  REGION   — Kenya county code (KE001–KE047)
  RANDOM6  — 6-char alphanumeric random suffix (case-insensitive)

Properties:
  - Human readable at a glance
  - Carries type, date, and region in the ID itself
  - Non-sequential — cannot enumerate records
  - Forensically traceable — date and region embedded
  - URL-safe — no special characters
"""

import random
import string
from datetime import datetime, timezone
from suid.registry.prefixes import PREFIX
from suid.regions.kenya import KENYA_COUNTIES


_CHARSET = string.ascii_uppercase + string.digits  # A-Z 0-9
_DEFAULT_REGION = "KE047"  # Nairobi default


class SUID:
    """Sorabbyngo Universal ID generator and parser."""

    @staticmethod
    def generate(prefix: str, region: str = _DEFAULT_REGION) -> str:
        """
        Generate a new SUID.

        Args:
            prefix: Entity type prefix from PREFIX registry (e.g. PREFIX.PATIENT)
            region: Kenya county code (e.g. "KE047" for Nairobi)

        Returns:
            SUID string e.g. "PAT-20260420-KE047-A3X9KM"

        Raises:
            ValueError: if prefix or region is invalid
        """
        if not PREFIX.is_valid(prefix):
            raise ValueError(f"Unknown prefix: {prefix}. Register it in suid/registry/prefixes.py")

        if region not in KENYA_COUNTIES:
            raise ValueError(f"Unknown region: {region}. Use a valid Kenya county code.")

        date    = datetime.now(timezone.utc).strftime("%Y%m%d")
        suffix  = "".join(random.choices(_CHARSET, k=6))

        return f"{prefix}-{date}-{region}-{suffix}"

    @staticmethod
    def parse(suid: str) -> dict:
        """
        Parse a SUID into its components.

        Returns:
            dict with keys: prefix, prefix_name, date, region, county, suffix, valid
        """
        from suid.regions.kenya import get_county

        try:
            parts = suid.strip().upper().split("-")
            if len(parts) != 4:
                return {"valid": False, "error": "Invalid format — expected PREFIX-DATE-REGION-SUFFIX"}

            prefix, date, region, suffix = parts

            prefix_map = PREFIX.all()

            return {
                "valid":       True,
                "suid":        suid.upper(),
                "prefix":      prefix,
                "prefix_name": prefix_map.get(prefix, "Unknown"),
                "date":        datetime.strptime(date, "%Y%m%d").date().isoformat(),
                "region":      region,
                "county":      get_county(region),
                "suffix":      suffix,
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    @staticmethod
    def batch(prefix: str, region: str = _DEFAULT_REGION, count: int = 10) -> list:
        """Generate multiple SUIDs at once."""
        return [SUID.generate(prefix, region) for _ in range(count)]

    # ── Convenience methods per entity type ──────────────────────────────────

    @staticmethod
    def patient(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.PATIENT, region)

    @staticmethod
    def doctor(region: str = _DEFAULT_REGION) -> str:
        return SUID.generate(PREFIX.DOCTOR, region)

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
