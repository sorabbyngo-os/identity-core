<p align="center">
  <img src="https://raw.githubusercontent.com/sorabbyngo-Labs/.github/main/assets/sorabbyngo-logo.jpg" alt="Sorabbyngo" width="480"/>
</p>

<p align="center">
  <strong>Identity Core — Sorabbyngo Universal ID System</strong>
</p>

<p align="center">
  Traceable · Forensic-ready · Kenya-native · Zero dependencies
</p>

---

## What this is

Every entity in the Sorabbyngo ecosystem — patients, doctors, hospitals, devices, transactions, alerts — has a structured Universal ID (SUID) that carries its type, creation date, and Kenyan county of origin directly in the ID string.

No lookups needed. Every ID tells a story.

---

## ID Format
{PREFIX}-{YYYYMMDD}-{REGION}-{RANDOM6}
PAT-20260420-KE047-A3X9KM   ← Patient, 20 Apr 2026, Nairobi
DOC-20260420-KE045-B7YQ2R   ← Doctor, 20 Apr 2026, Kisii
TXN-20260420-KE001-E9VK3J   ← Transaction, 20 Apr 2026, Mombasa
MON-20260420-KE042-D2WL5T   ← Monitor device, 20 Apr 2026, Kisumu

---

## Prefix Registry

| Prefix | Entity | System |
|---|---|---|
| PAT | Patient | Novela |
| DOC | Doctor / Clinician | Novela |
| CGV | Caregiver | Novela |
| CHW | Community Health Worker | Novela |
| HSP | Hospital / Facility | Novela |
| CLN | Clinic | Novela |
| PHM | Pharmacy | Novela |
| ADM | Ward Admission | Novela |
| APT | Appointment | Novela |
| CPL | Care Plan | Novela |
| RXN | Prescription | Novela |
| MED | Medication Verification | Novela |
| LAB | Lab Result | Novela |
| DXN | Diagnosis | Novela |
| VST | Clinical Visit | Novela |
| MON | Monitor Device | novela-monitors |
| ALE | Clinical Alert | novela-monitors |
| VTL | Vitals Reading | novela-monitors |
| GTW | Ward Gateway | novela-monitors |
| USR | System User | identity |
| SES | Auth Session | identity |
| TXN | Transaction | Finance |
| INV | Invoice | Finance |
| PAY | Payment | Finance |
| CLM | Insurance Claim | Finance |
| NDI | Byngonet Node | byngonet |
| DEV | OS Device | sorabbyngo-os |
| AUD | Audit Log Entry | CML |
| INC | Security Incident | CML |
| OBK | Outbreak Event | Population Health |
| CAM | Health Campaign | Population Health |

---

## Usage

```python
from suid import SUID, PREFIX, validate, parse

# Generate IDs
patient_id     = SUID.patient("KE047")      # PAT-20260420-KE047-A3X9KM
doctor_id      = SUID.doctor("KE045")       # DOC-20260420-KE045-B7YQ2R
transaction_id = SUID.transaction("KE001")  # TXN-20260420-KE001-E9VK3J
monitor_id     = SUID.monitor("KE042")      # MON-20260420-KE042-D2WL5T

# Generate any entity type
alert_id = SUID.generate(PREFIX.ALERT, "KE047")

# Validate
validate("PAT-20260420-KE047-A3X9KM")  # True
validate("NOT-VALID")                   # False

# Parse
info = parse("PAT-20260420-KE047-A3X9KM")
# {
#   "valid": True,
#   "prefix": "PAT",
#   "prefix_name": "PATIENT",
#   "date": "2026-04-20",
#   "region": "KE047",
#   "county": "Nairobi",
#   "suffix": "A3X9KM"
# }
```

---

## Forensic Extraction

```python
from suid.forensics.extractor import ForensicExtractor

# Single entity report
report = ForensicExtractor.entity_report("PAT-20260420-KE047-A3X9KM")
# Returns: entity type, creation date, county, DB query to run

# Law enforcement summary report
summary = ForensicExtractor.law_enforcement_summary(
    suids=["PAT-...", "TXN-...", "ADM-..."],
    case_number="CASE-2026-001"
)

# Filter by type, region, or date range
patients = ForensicExtractor.filter_by_type(all_ids, "PAT")
nairobi  = ForensicExtractor.filter_by_region(all_ids, "KE047")
range_ids= ForensicExtractor.filter_by_date_range(all_ids, "2026-01-01", "2026-04-20")
```

---

## DB Query for any SUID

```sql
SELECT * FROM audit_logs
WHERE entity_id  = 'PAT-20260420-KE047-A3X9KM'
   OR related_id = 'PAT-20260420-KE047-A3X9KM'
ORDER BY created_at ASC;
```

---

## Install

```bash
pip install -e .
```

---

## Test

```bash
pytest tests/ -v
```

---

## Part of SORABBYNGO OS

| Repo | Uses identity-core for |
|---|---|
| [novela](https://github.com/sorabbyngo-Labs/novela) | Patient, doctor, hospital, admission IDs |
| [novela-monitors](https://github.com/sorabbyngo-Labs/novela-monitors) | Monitor, alert, gateway IDs |
| [cml](https://github.com/sorabbyngo-Labs/cml) | Audit log IDs |
| [byngonet](https://github.com/sorabbyngo-Labs/byngonet) | Node IDs |
| [sorabbyngo-os](https://github.com/sorabbyngo-Labs/sorabbyngo-os) | Device, session IDs |

---

**Sorabbyngo Company** · Kisii, Kenya · 2026
*Rhythm of Digital Life*
