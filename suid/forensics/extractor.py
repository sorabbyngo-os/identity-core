"""
SUID Forensic Extractor
Used by Sorabbyngo IT department to extract audit trails for law enforcement,
internal investigations, and compliance reviews.

Usage:
    from suid.forensics.extractor import ForensicExtractor

    # Single entity report
    report = ForensicExtractor.entity_report("PAT-20260421-KE045-A3X9KM-7F")

    # Law enforcement package
    report = ForensicExtractor.law_enforcement_summary(
        suids=["PAT-...", "TXN-...", "DOC-..."],
        case_number="NPS/CID/2026/001",
        requesting_authority="Kenya National Police Service",
        authorized_by="Head of IT",
    )
"""

from datetime import datetime, timezone
from suid.generator import SUID
from suid.validator import validate, is_tampered
from suid.registry.prefixes import PREFIX
from suid.regions.africa import get_region, get_country


class ForensicExtractor:
    """
    Tools for extracting forensic information from SUIDs.
    Every method produces structured output suitable for official submission.
    """

    @staticmethod
    def entity_report(suid: str) -> dict:
        """
        Generate a forensic report for a single entity ID.
        Extracts all metadata embedded in the SUID without DB access.

        Args:
            suid: Any valid SUID string

        Returns:
            dict containing entity type, creation date, origin region,
            tamper status, and suggested DB queries.
        """
        if not validate(suid):
            return {
                "error":   f"Invalid SUID: {suid}",
                "valid":   False,
                "tampered": None,
            }

        parsed  = SUID.parse(suid)
        tampered = is_tampered(suid)

        return {
            "suid":           parsed["suid"],
            "valid":          True,
            "tampered":       tampered,
            "entity_type":    parsed["prefix_name"],
            "entity_code":    parsed["prefix"],
            "created_date":   parsed["date"],
            "origin_region":  parsed["region"],
            "origin_area":    parsed["region_name"],
            "origin_country": parsed["country"],
            "random_suffix":  parsed["suffix"],
            "checksum":       parsed.get("checksum"),
            "checksum_valid": parsed.get("checksum_valid"),
            "forensic_note": (
                f"This ID identifies a {parsed['prefix_name']} record "
                f"created on {parsed['date']} "
                f"in {parsed['region_name']}, {parsed['country']}. "
                + ("⚠️  CHECKSUM FAILED — possible tampering." if tampered else "Checksum verified.")
            ),
            "db_queries": {
                "audit_trail": (
                    f"SELECT * FROM audit_logs "
                    f"WHERE entity_id = '{parsed['suid']}' "
                    f"OR related_id = '{parsed['suid']}' "
                    f"ORDER BY created_at ASC;"
                ),
                "entity_record": (
                    f"SELECT * FROM {parsed['prefix'].lower()}_records "
                    f"WHERE suid = '{parsed['suid']}';"
                ),
                "access_log": (
                    f"SELECT * FROM audit_logs "
                    f"WHERE entity_id = '{parsed['suid']}' "
                    f"AND action IN ('READ','ACCESS','EXPORT') "
                    f"ORDER BY created_at ASC;"
                ),
                "related_entities": (
                    f"SELECT * FROM audit_logs "
                    f"WHERE related_id = '{parsed['suid']}' "
                    f"ORDER BY created_at ASC;"
                ),
            },
        }

    @staticmethod
    def bulk_report(suids: list) -> list:
        """Generate forensic reports for a list of SUIDs."""
        return [ForensicExtractor.entity_report(s) for s in suids]

    @staticmethod
    def filter_by_type(suids: list, prefix: str) -> list:
        """Filter SUIDs by entity type prefix."""
        return [s for s in suids if s.upper().startswith(prefix.upper())]

    @staticmethod
    def filter_by_region(suids: list, region: str) -> list:
        """Filter SUIDs by region code."""
        return [s for s in suids if f"-{region.upper()}-" in s.upper()]

    @staticmethod
    def filter_by_date_range(suids: list, start: str, end: str) -> list:
        """
        Filter SUIDs by creation date range.
        Args:
            start: "YYYY-MM-DD"
            end:   "YYYY-MM-DD"
        """
        start_dt = datetime.strptime(start, "%Y-%m-%d").date()
        end_dt   = datetime.strptime(end,   "%Y-%m-%d").date()
        result   = []
        for suid in suids:
            parsed = SUID.parse(suid)
            if not parsed.get("valid"):
                continue
            created = datetime.strptime(parsed["date"], "%Y-%m-%d").date()
            if start_dt <= created <= end_dt:
                result.append(suid)
        return result

    @staticmethod
    def detect_tampered(suids: list) -> list:
        """Return all SUIDs that fail checksum verification."""
        return [s for s in suids if is_tampered(s)]

    @staticmethod
    def law_enforcement_summary(
        suids:                 list,
        case_number:           str  = "",
        requesting_authority:  str  = "",
        authorized_by:         str  = "",
        notes:                 str  = "",
    ) -> dict:
        """
        Generate a structured law enforcement summary report.
        Format suitable for official submission to police, courts, or regulators.

        Args:
            suids:                List of SUIDs related to the case
            case_number:          Official case/reference number
            requesting_authority: e.g. "Kenya National Police Service"
            authorized_by:        e.g. "Head of IT, Sorabbyngo Company"
            notes:                Any additional context

        Returns:
            Structured report dict suitable for PDF export or official submission
        """
        reports    = ForensicExtractor.bulk_report(suids)
        valid      = [r for r in reports if r.get("valid")]
        invalid    = [r for r in reports if not r.get("valid")]
        tampered   = [r for r in valid    if r.get("tampered")]

        by_type    = {}
        by_region  = {}
        by_country = {}
        timeline   = []

        for r in valid:
            t  = r["entity_type"]
            a  = r["origin_area"]
            c  = r["origin_country"]
            dt = r["created_date"]

            by_type[t]    = by_type.get(t, 0) + 1
            by_region[a]  = by_region.get(a, 0) + 1
            by_country[c] = by_country.get(c, 0) + 1
            timeline.append({"suid": r["suid"], "date": dt, "type": t, "area": a})

        timeline.sort(key=lambda x: x["date"])

        return {
            "report_type":          "LAW_ENFORCEMENT_FORENSIC_SUMMARY",
            "case_number":          case_number,
            "requesting_authority": requesting_authority,
            "authorized_by":        authorized_by,
            "generated_at":         datetime.now(timezone.utc).isoformat() + "Z",
            "generated_by":         "Sorabbyngo Identity Core v1.0",
            "company":              "Sorabbyngo Company, Kisii, Kenya",

            "summary": {
                "total_ids":     len(suids),
                "valid_ids":     len(valid),
                "invalid_ids":   len(invalid),
                "tampered_ids":  len(tampered),
                "date_range": {
                    "earliest": timeline[0]["date"]  if timeline else None,
                    "latest":   timeline[-1]["date"] if timeline else None,
                },
            },

            "breakdown": {
                "by_entity_type": by_type,
                "by_region":      by_region,
                "by_country":     by_country,
            },

            "timeline":          timeline,
            "tampered_records":  tampered,
            "invalid_records":   invalid,
            "full_records":      valid,

            "notes": notes,
            "legal_notice": (
                "This report was generated by the Sorabbyngo IT department "
                "in response to a lawful request. All IDs are traceable to "
                "specific entity types, creation dates, and geographic regions. "
                "Tampered IDs (checksum failures) are flagged above and may "
                "indicate unauthorized data modification."
            ),
        }
