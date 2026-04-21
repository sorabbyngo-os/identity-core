"""
Sorabbyngo Universal ID — Prefix Registry
Every entity type in the ecosystem has a registered prefix.
Adding a new entity type requires a registry entry here first.
"""

class PREFIX:
    # ── Health Platform (Novela) ──────────────────────────────────────────
    PATIENT       = "PAT"   # Patient record
    DOCTOR        = "DOC"   # Doctor / clinician
    CAREGIVER     = "CGV"   # Caregiver
    CHW           = "CHW"   # Community health worker
    HOSPITAL      = "HSP"   # Hospital / facility
    CLINIC        = "CLN"   # Clinic
    PHARMACY      = "PHM"   # Pharmacy
    ADMISSION     = "ADM"   # Ward admission
    APPOINTMENT   = "APT"   # Appointment
    CARE_PLAN     = "CPL"   # Care plan
    PRESCRIPTION  = "RXN"   # Prescription
    MEDICATION    = "MED"   # Medication verification
    LAB_RESULT    = "LAB"   # Laboratory result
    DIAGNOSIS     = "DXN"   # Diagnosis record
    VISIT         = "VST"   # Clinical visit / session

    # ── Monitor System (novela-monitors) ─────────────────────────────────
    MONITOR       = "MON"   # Bedside monitor device
    ALERT         = "ALE"   # Clinical alert
    VITALS        = "VTL"   # Vitals reading
    GATEWAY       = "GTW"   # Ward gateway device

    # ── Identity & Access ─────────────────────────────────────────────────
    USER          = "USR"   # System user account
    SESSION       = "SES"   # Auth session
    API_KEY       = "KEY"   # API key

    # ── Finance ───────────────────────────────────────────────────────────
    TRANSACTION   = "TXN"   # Financial transaction
    INVOICE       = "INV"   # Invoice
    PAYMENT       = "PAY"   # Payment record
    CLAIM         = "CLM"   # Insurance claim

    # ── Infrastructure (Byngonet / OS) ───────────────────────────────────
    NODE          = "NDI"   # Byngonet network node
    DEVICE        = "DEV"   # OS device
    OS_SESSION    = "OSS"   # OS boot session

    # ── Safety & Audit (CML) ─────────────────────────────────────────────
    AUDIT         = "AUD"   # Audit log entry
    INCIDENT      = "INC"   # Security incident
    REPORT        = "RPT"   # System report

    # ── Population Health ─────────────────────────────────────────────────
    OUTBREAK      = "OBK"   # Outbreak / epidemic event
    CAMPAIGN      = "CAM"   # Health campaign

    @classmethod
    def all(cls) -> dict:
        """Return all registered prefixes and their descriptions."""
        return {
            v: k for k, v in cls.__dict__.items()
            if not k.startswith("_") and isinstance(v, str) and len(v) == 3
        }

    @classmethod
    def is_valid(cls, prefix: str) -> bool:
        return prefix in cls.all()
