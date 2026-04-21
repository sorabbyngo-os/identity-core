# identity-core — Sorabbyngo Universal ID System

> Every entity in the Sorabbyngo ecosystem has a traceable, tamper-detectable identity.

---

## Format

```
{PREFIX}-{YYYYMMDD}-{REGION}-{RANDOM6}-{CHECK2}

PAT-20260421-KE045-A3X9KM-7F
DOC-20260421-KE047-B7X2QR-3K
TXN-20260421-UG001-C4M8NP-9W
```

| Component | Length | Example | Purpose |
|-----------|--------|---------|---------|
| `PREFIX`  | 3 chars | `PAT` | Entity type |
| `DATE`    | 8 digits | `20260421` | Creation date UTC |
| `REGION`  | 5 chars | `KE045` | Geographic origin |
| `RANDOM`  | 6 chars | `A3X9KM` | Cryptographic entropy |
| `CHECK`   | 2 chars | `7F` | Tamper detection |

---

## Entity Types

### Health Platform (Novela)
| Code | Entity |
|------|--------|
| `PAT` | Patient Record |
| `DOC` | Doctor / Clinician |
| `NRS` | Nurse |
| `CHW` | Community Health Worker |
| `HSP` | Hospital / Facility |
| `CLN` | Clinic |
| `PHM` | Pharmacy |
| `ADM` | Ward Admission |
| `APT` | Appointment |
| `RXN` | Prescription |
| `VRF` | Medication Verification |
| `LAB` | Laboratory Result |
| `DXN` | Diagnosis Record |
| `VST` | Clinical Visit |

### Monitor System
| Code | Entity |
|------|--------|
| `MON` | Bedside Monitor |
| `ALE` | Clinical Alert |
| `VTL` | Vitals Reading |
| `GTW` | Ward Gateway |

### Finance
| Code | Entity |
|------|--------|
| `TXN` | Financial Transaction |
| `PAY` | Payment Record |
| `CLM` | Insurance Claim |

### Infrastructure
| Code | Entity |
|------|--------|
| `NDI` | Byngonet Node |
| `DEV` | OS Device |
| `AUD` | Audit Log Entry |
| `INC` | Security Incident |

---

## Supported Regions

| Country | Codes | Coverage |
|---------|-------|----------|
| Kenya 🇰🇪 | KE001–KE047 | All 47 counties |
| Uganda 🇺🇬 | UG001–UG010 | Major districts |
| Tanzania 🇹🇿 | TZ001–TZ008 | Major regions |
| Rwanda 🇷🇼 | RW001–RW005 | All provinces |
| Ethiopia 🇪🇹 | ET001–ET006 | Major regions |
| Ghana 🇬🇭 | GH001–GH006 | Major regions |
| Nigeria 🇳🇬 | NG001–NG008 | Major states |
| South Africa 🇿🇦 | ZA001–ZA006 | All provinces |

---

## Quick Start

```python
from suid import SUID, PREFIX, validate, ForensicExtractor, AuditLogger

# Generate IDs
patient = SUID.patient("KE045")          # PAT-20260421-KE045-A3X9KM-7F
doctor  = SUID.doctor("KE045")           # DOC-20260421-KE045-B7X2QR-3K
txn     = SUID.transaction("KE047")      # TXN-20260421-KE047-C4M8NP-9W

# Any entity type
alert   = SUID.generate(PREFIX.ALERT, "UG001")

# Validate
validate(patient)                         # True
validate(patient, verify_checksum=True)   # True — checksum verified

# Parse
info = SUID.parse(patient)
# {
#   "prefix": "PAT", "prefix_name": "Patient Record",
#   "date": "2026-04-21", "region": "KE045",
#   "region_name": "Kisii", "country": "Kenya",
#   "checksum_valid": True, "tampered": False
# }

# Audit logging
AuditLogger.create(patient, actor_id=doctor)
AuditLogger.admit(patient, admission_id, actor_id=doctor)
AuditLogger.alert(alert_id, patient_id=patient)

# Forensics
report = ForensicExtractor.entity_report(patient)
summary = ForensicExtractor.law_enforcement_summary(
    suids=[patient, doctor, txn],
    case_number="NPS/CID/2026/001",
    requesting_authority="Kenya National Police Service",
    authorized_by="Head of IT, Sorabbyngo Company",
)
```

---

## Law Enforcement / Forensics

Every SUID embeds forensic metadata without requiring database access:

```python
ForensicExtractor.entity_report("PAT-20260421-KE045-A3X9KM-7F")
# {
#   "entity_type":    "Patient Record",
#   "created_date":   "2026-04-21",
#   "origin_area":    "Kisii",
#   "origin_country": "Kenya",
#   "tampered":       False,
#   "db_queries": {
#     "audit_trail":       "SELECT * FROM audit_logs WHERE entity_id = '...'",
#     "access_log":        "SELECT * FROM audit_logs WHERE action IN ('READ','ACCESS'...",
#     "related_entities":  "SELECT * FROM audit_logs WHERE related_id = '...'",
#   }
# }
```

The `law_enforcement_summary()` method generates a structured report suitable for official submission to police, courts, or regulators — including tamper detection, entity timeline, and breakdown by type and region.

---

## Security Properties

| Property | Implementation |
|----------|---------------|
| Non-guessable | `secrets.choice()` — cryptographically random suffix |
| Tamper-detectable | 2-char checksum over all components |
| Forensically traceable | Date + region embedded in ID |
| Permanent | Prefixes never reused once assigned |
| URL-safe | A-Z, 0-9, hyphens only |

---

## Installation

```bash
pip install -e .          # Development
pip install -e ".[dev]"   # With test dependencies
pytest tests/             # Run tests
```

---

## Integration

Used across the entire Sorabbyngo ecosystem:

- **Novela** — patient, doctor, hospital, prescription, lab result IDs
- **novela-monitors** — monitor, alert, vitals, gateway IDs
- **Byngox** — agent session and decision IDs
- **CML** — audit log IDs (audit entries are themselves SUIDs)
- **Sorabbyngo OS** — node, device, kernel event IDs
- **Finance** — transaction, payment, claim IDs

---

*Sorabbyngo Company · Kisii, Kenya · 2026 · Rhythm of Digital Life*
