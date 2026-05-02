# SUID Integration Guide

## Installing

```bash
pip install -e .         # from identity-core repo root
pip install -e ".[dev]"  # with test dependencies
```

## Basic usage

```python
from suid import SUID, PREFIX, validate, AuditLogger, ForensicExtractor

# Generate
patient = SUID.patient("KE045")        # PAT-20260421-KE045-A3X9KM-7F
doctor  = SUID.doctor("KE047")
node    = SUID.node("KE047")

# Any prefix
alert = SUID.generate(PREFIX.ALERT, "UG001")

# Validate
validate(patient)                        # True
validate(patient, verify_checksum=True)  # True — full verification

# Parse
info = SUID.parse(patient)
# info["prefix_name"]  → "Patient Record"
# info["region_name"]  → "Kisii"
# info["country"]      → "Kenya"
# info["tampered"]     → False
```

## Audit logging

```python
AuditLogger.create(patient_id, actor_id=doctor_id)
AuditLogger.admit(patient_id, admission_id, actor_id=doctor_id)
AuditLogger.login(user_id, ip_address="192.168.1.1")
AuditLogger.auth_fail(user_id, ip_address="10.0.0.1")
AuditLogger.export(record_id, actor_id=user_id)
```

All audit entries generate their own AUD- SUID and write to the
hash-chained ledger (sorabbyngo-security) when available.

## Forensics

```python
# Single entity
report = ForensicExtractor.entity_report(patient_id)

# Law enforcement package
summary = ForensicExtractor.law_enforcement_summary(
    suids=[patient_id, doctor_id, txn_id],
    case_number="NPS/CID/2026/001",
    requesting_authority="Kenya National Police Service",
    authorized_by="Head of IT, Sorabbyngo Company",
)

# Filter helpers
pats    = ForensicExtractor.filter_by_type(suids, "PAT")
kisii   = ForensicExtractor.filter_by_region(suids, "KE045")
recent  = ForensicExtractor.filter_by_date_range(suids, "2026-01-01", "2026-12-31")
tampered = ForensicExtractor.detect_tampered(suids)
```

## Supported regions

Kenya: KE001–KE047 (all 47 counties)
Uganda: UG001–UG010 | Tanzania: TZ001–TZ008 | Rwanda: RW001–RW005
Ethiopia: ET001–ET006 | Ghana: GH001–GH006 | Nigeria: NG001–NG008
South Africa: ZA001–ZA006
