"""
SUID Complete Test Suite
"""
import pytest
from suid.generator import SUID
from suid.validator import validate, parse, is_tampered
from suid.registry.prefixes import PREFIX
from suid.forensics.extractor import ForensicExtractor
from suid.audit.logger import AuditLogger


# ── Generator tests ────────────────────────────────────────────────────────

def test_generate_patient():
    suid = SUID.patient("KE047")
    assert suid.startswith("PAT-")
    assert "KE047" in suid
    assert len(suid.split("-")) == 5   # Now 5 parts with checksum

def test_generate_all_prefixes():
    for prefix in PREFIX.all():
        suid = SUID.generate(prefix, "KE045")
        assert suid.startswith(f"{prefix}-")

def test_generate_african_regions():
    """Verify non-Kenya regions work."""
    suid_ug = SUID.patient("UG001")
    assert "UG001" in suid_ug
    suid_tz = SUID.doctor("TZ001")
    assert "TZ001" in suid_tz
    suid_ng = SUID.hospital("NG001")
    assert "NG001" in suid_ng

def test_invalid_prefix():
    with pytest.raises(ValueError):
        SUID.generate("XXX", "KE047")

def test_invalid_region():
    with pytest.raises(ValueError):
        SUID.generate(PREFIX.PATIENT, "KE099")   # KE099 doesn't exist

def test_invalid_region_random():
    with pytest.raises(ValueError):
        SUID.generate(PREFIX.PATIENT, "ZZ999")

def test_uses_secrets():
    """Verify IDs are non-sequential (different suffixes)."""
    ids = SUID.batch(PREFIX.PATIENT, "KE045", count=100)
    suffixes = {s.split("-")[3] for s in ids}
    assert len(suffixes) > 90   # Should be almost all unique

def test_batch():
    suids = SUID.batch(PREFIX.MONITOR, "KE042", count=5)
    assert len(suids) == 5
    for s in suids:
        assert validate(s)

def test_convenience_methods():
    assert SUID.patient().startswith("PAT-")
    assert SUID.doctor().startswith("DOC-")
    assert SUID.nurse().startswith("NRS-")
    assert SUID.hospital().startswith("HSP-")
    assert SUID.transaction().startswith("TXN-")
    assert SUID.audit().startswith("AUD-")
    assert SUID.verification().startswith("VRF-")
    assert SUID.prescription().startswith("RXN-")


# ── Validator tests ────────────────────────────────────────────────────────

def test_validate_v2():
    suid = SUID.patient("KE047")
    assert validate(suid) is True

def test_validate_with_checksum():
    suid = SUID.patient("KE047")
    assert validate(suid, verify_checksum=True) is True

def test_validate_invalid():
    assert validate("NOT-VALID")              is False
    assert validate("PAT-20260420-KE047-A3X9K") is False  # Too short suffix
    assert validate("")                       is False
    assert validate(None)                     is False

def test_tamper_detection():
    suid  = SUID.patient("KE045")
    parts = suid.split("-")
    # Tamper with the suffix
    parts[3] = "XXXXXX"
    tampered = "-".join(parts)
    assert is_tampered(tampered) is True

def test_no_false_tamper():
    suid = SUID.patient("KE045")
    assert is_tampered(suid) is False


# ── Parser tests ───────────────────────────────────────────────────────────

def test_parse_v2():
    suid   = SUID.patient("KE045")
    result = parse(suid)
    assert result["valid"]          is True
    assert result["prefix"]         == "PAT"
    assert result["prefix_name"]    == "Patient Record"
    assert result["region"]         == "KE045"
    assert result["region_name"]    == "Kisii"
    assert result["country"]        == "Kenya"
    assert result["checksum_valid"] is True
    assert result["tampered"]       is False

def test_parse_uganda():
    suid   = SUID.doctor("UG001")
    result = parse(suid)
    assert result["valid"]       is True
    assert result["region_name"] == "Kampala"
    assert result["country"]     == "Uganda"

def test_parse_invalid():
    result = parse("GARBAGE")
    assert result["valid"] is False


# ── PREFIX registry tests ──────────────────────────────────────────────────

def test_all_prefixes_have_descriptions():
    for code, desc in PREFIX.all().items():
        assert len(code) == 3
        assert len(desc) > 0

def test_prefix_domains():
    domains = PREFIX.by_domain()
    assert "PAT" in domains["health"]
    assert "TXN" in domains["finance"]
    assert "AUD" in domains["safety_audit"]
    assert "NDI" in domains["infrastructure"]

def test_prefix_is_valid():
    assert PREFIX.is_valid("PAT") is True
    assert PREFIX.is_valid("XXX") is False

def test_prefix_describe():
    assert "Patient" in PREFIX.describe("PAT")
    assert "Transaction" in PREFIX.describe("TXN")


# ── Forensic extractor tests ───────────────────────────────────────────────

def test_forensic_entity_report():
    suid   = SUID.patient("KE045")
    report = ForensicExtractor.entity_report(suid)
    assert report["entity_type"]   == "Patient Record"
    assert report["origin_area"]   == "Kisii"
    assert report["origin_country"]== "Kenya"
    assert report["tampered"]      is False
    assert "db_queries" in report
    assert "audit_trail" in report["db_queries"]

def test_forensic_tamper_detection():
    suid  = SUID.patient("KE045")
    parts = suid.split("-")
    parts[3] = "XXXXXX"
    tampered = "-".join(parts)
    report = ForensicExtractor.entity_report(tampered)
    assert report["tampered"] is True
    assert "CHECKSUM FAILED" in report["forensic_note"]

def test_forensic_invalid_suid():
    report = ForensicExtractor.entity_report("GARBAGE")
    assert "error" in report

def test_filter_by_type():
    suids = [SUID.patient("KE047"), SUID.doctor("KE047"), SUID.patient("KE045")]
    pats  = ForensicExtractor.filter_by_type(suids, "PAT")
    assert len(pats) == 2

def test_filter_by_region():
    suids = [SUID.patient("KE047"), SUID.patient("KE045"), SUID.doctor("KE045")]
    kisii = ForensicExtractor.filter_by_region(suids, "KE045")
    assert len(kisii) == 2

def test_law_enforcement_summary():
    suids = [
        SUID.patient("KE047"),
        SUID.doctor("KE045"),
        SUID.transaction("KE001"),
    ]
    report = ForensicExtractor.law_enforcement_summary(
        suids,
        case_number="NPS/CID/2026/001",
        requesting_authority="Kenya National Police Service",
        authorized_by="Head of IT, Sorabbyngo Company",
    )
    assert report["summary"]["total_ids"]   == 3
    assert report["summary"]["valid_ids"]   == 3
    assert report["summary"]["tampered_ids"]== 0
    assert "Patient Record"      in report["breakdown"]["by_entity_type"]
    assert "report_type"         in report
    assert "legal_notice"        in report
    assert "timeline"            in report


# ── Audit logger tests ─────────────────────────────────────────────────────

def test_audit_create():
    pat = SUID.patient("KE045")
    doc = SUID.doctor("KE045")
    entry = AuditLogger.create(pat, actor_id=doc)
    assert entry["action"]    == "CREATE"
    assert entry["entity_id"] == pat
    assert entry["actor_id"]  == doc
    assert entry["audit_id"].startswith("AUD-")
    assert validate(entry["audit_id"]) is True   # Audit ID is itself a valid SUID

def test_audit_id_is_suid():
    """Critical: audit IDs must themselves be valid SUIDs."""
    for action in ["CREATE", "READ", "UPDATE", "DELETE", "ALERT", "LOGIN"]:
        entry = AuditLogger.log(action, SUID.patient())
        assert validate(entry["audit_id"]) is True

def test_audit_admit():
    pat = SUID.patient("KE042")
    adm = SUID.admission("KE042")
    doc = SUID.doctor("KE042")
    entry = AuditLogger.admit(pat, adm, actor_id=doc)
    assert entry["action"]     == "ADMIT"
    assert entry["entity_id"]  == pat
    assert entry["related_id"] == adm

def test_audit_alert():
    ale = SUID.alert("KE045")
    pat = SUID.patient("KE045")
    entry = AuditLogger.alert(ale, pat)
    assert entry["action"]     == "ALERT"
    assert entry["related_id"] == pat

# ── Additional tests ───────────────────────────────────────────────────────────
def test_filter_by_date_range():
    """filter_by_date_range returns only IDs created within the window."""
    from datetime import date
    today = date.today().isoformat()
    suids = SUID.batch(PREFIX.PATIENT, "KE047", count=3)
    result = ForensicExtractor.filter_by_date_range(suids, today, today)
    assert len(result) == 3

def test_filter_by_date_range_excludes_out_of_range():
    suids = SUID.batch(PREFIX.PATIENT, "KE047", count=2)
    result = ForensicExtractor.filter_by_date_range(suids, "2020-01-01", "2020-12-31")
    assert len(result) == 0

def test_detect_tampered_in_bulk():
    good    = SUID.patient("KE045")
    parts   = good.split("-")
    parts[3] = "XXXXXX"
    bad     = "-".join(parts)
    result  = ForensicExtractor.detect_tampered([good, bad])
    assert bad  in result
    assert good not in result

def test_bulk_report():
    suids  = [SUID.patient("KE047"), SUID.doctor("KE045")]
    reports = ForensicExtractor.bulk_report(suids)
    assert len(reports) == 2
    assert all(r["valid"] for r in reports)

def test_audit_discharge():
    pat = SUID.patient("KE042")
    adm = SUID.admission("KE042")
    entry = AuditLogger.discharge(pat, adm)
    assert entry["action"] == "DISCHARGE"
    assert entry["related_id"] == adm

def test_audit_login():
    usr = SUID.generate("USR", "KE047")
    entry = AuditLogger.login(usr, ip_address="192.168.1.1")
    assert entry["action"] == "LOGIN"
    assert entry["ip_address"] == "192.168.1.1"

def test_audit_auth_fail():
    usr = SUID.generate("USR", "KE047")
    entry = AuditLogger.auth_fail(usr, ip_address="10.0.0.1")
    assert entry["action"] == "AUTH_FAIL"

def test_suid_uniqueness_across_regions():
    """Same prefix, different regions — all unique."""
    regions = ["KE047", "KE045", "UG001", "TZ001", "NG001"]
    ids = [SUID.patient(r) for r in regions]
    assert len(set(ids)) == len(ids)

def test_prefix_all_returns_dict():
    all_p = PREFIX.all()
    assert isinstance(all_p, dict)
    assert len(all_p) > 40

def test_parse_all_african_countries():
    from suid.regions.africa import COUNTRY_MAP
    for iso2, country in COUNTRY_MAP.items():
        if iso2 == "KE":
            continue
        code = f"{iso2}001"
        from suid.regions.africa import is_valid_region, get_country
        assert is_valid_region(code), f"{code} should be valid"
        assert get_country(code) == country
