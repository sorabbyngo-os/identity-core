"""
SUID Test Suite
"""
import pytest
from suid.generator import SUID
from suid.validator import validate, parse
from suid.registry.prefixes import PREFIX
from suid.forensics.extractor import ForensicExtractor


def test_generate_patient():
    suid = SUID.patient("KE047")
    assert suid.startswith("PAT-")
    assert "KE047" in suid
    assert len(suid.split("-")) == 4


def test_generate_all_prefixes():
    for prefix in PREFIX.all():
        suid = SUID.generate(prefix, "KE045")
        assert suid.startswith(f"{prefix}-")


def test_invalid_prefix():
    with pytest.raises(ValueError):
        SUID.generate("XXX", "KE047")


def test_invalid_region():
    with pytest.raises(ValueError):
        SUID.generate(PREFIX.PATIENT, "KE099")


def test_validate():
    suid = SUID.patient("KE047")
    assert validate(suid) is True
    assert validate("NOT-VALID") is False
    assert validate("PAT-20260420-KE047-A3X9K") is False  # too short


def test_parse():
    suid = "PAT-20260420-KE047-A3X9KM"
    result = parse(suid)
    assert result["valid"] is True
    assert result["prefix"] == "PAT"
    assert result["prefix_name"] == "PATIENT"
    assert result["county"] == "Nairobi"
    assert result["date"] == "2026-04-20"


def test_forensic_report():
    suid = SUID.patient("KE045")
    report = ForensicExtractor.entity_report(suid)
    assert report["entity_type"] == "PATIENT"
    assert report["origin_county"] == "Kisii"
    assert "db_query" in report


def test_law_enforcement_summary():
    suids = [
        SUID.patient("KE047"),
        SUID.doctor("KE045"),
        SUID.transaction("KE001"),
    ]
    report = ForensicExtractor.law_enforcement_summary(suids, case_number="CASE-001")
    assert report["total_ids"] == 3
    assert report["valid_ids"] == 3
    assert "PATIENT" in report["entities_by_type"]


def test_batch():
    suids = SUID.batch(PREFIX.MONITOR, "KE042", count=5)
    assert len(suids) == 5
    for s in suids:
        assert validate(s)
