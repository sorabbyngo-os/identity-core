"""
Sorabbyngo Universal ID — Prefix Registry
Every entity type in the ecosystem has a registered 3-char prefix.
Adding a new entity type requires a registry entry here first.

Governance rule: prefixes are permanent once assigned.
Never reuse a prefix — it breaks forensic traceability.
"""


class PREFIX:
    # ── Health Platform (Novela) ──────────────────────────────────────────
    PATIENT       = "PAT"   # Patient record
    DOCTOR        = "DOC"   # Doctor / clinician
    NURSE         = "NRS"   # Nurse
    CAREGIVER     = "CGV"   # Caregiver / family
    CHW           = "CHW"   # Community health worker
    HOSPITAL      = "HSP"   # Hospital / facility
    CLINIC        = "CLN"   # Clinic
    PHARMACY      = "PHM"   # Pharmacy
    LABORATORY    = "LBF"   # Laboratory facility
    ADMISSION     = "ADM"   # Ward admission
    APPOINTMENT   = "APT"   # Appointment
    CARE_PLAN     = "CPL"   # Care plan
    PRESCRIPTION  = "RXN"   # Prescription
    MEDICATION    = "MED"   # Medication / drug record
    VERIFICATION  = "VRF"   # Medication verification (counterfeit check)
    LAB_RESULT    = "LAB"   # Laboratory result
    DIAGNOSIS     = "DXN"   # Diagnosis record
    VISIT         = "VST"   # Clinical visit / session
    DISCHARGE     = "DSC"   # Patient discharge
    REFERRAL      = "REF"   # Patient referral
    CONSENT       = "CNS"   # Patient consent record
    IMMUNIZATION  = "IMN"   # Immunization record
    ALLERGY       = "ALG"   # Allergy record

    # ── Monitor System (novela-monitors) ─────────────────────────────────
    MONITOR       = "MON"   # Bedside monitor device
    ALERT         = "ALE"   # Clinical alert
    VITALS        = "VTL"   # Vitals reading batch
    GATEWAY       = "GTW"   # Ward gateway (Raspberry Pi)
    WARD          = "WRD"   # Hospital ward

    # ── Identity & Access ─────────────────────────────────────────────────
    USER          = "USR"   # System user account
    SESSION       = "SES"   # Auth session
    API_KEY       = "KEY"   # API key
    ROLE          = "ROL"   # Access role assignment

    # ── Finance ───────────────────────────────────────────────────────────
    TRANSACTION   = "TXN"   # Financial transaction
    INVOICE       = "INV"   # Invoice
    PAYMENT       = "PAY"   # Payment record
    CLAIM         = "CLM"   # Insurance / NHIF claim
    RECEIPT       = "RCP"   # Payment receipt

    # ── Infrastructure (Byngonet / Sorabbyngo OS) ─────────────────────────
    NODE          = "NDI"   # Byngonet network node
    DEVICE        = "DEV"   # OS device
    OS_SESSION    = "OSS"   # OS boot session
    KERNEL_EVENT  = "KRN"   # Kernel-level event

    # ── Safety & Audit (CML) ─────────────────────────────────────────────
    AUDIT         = "AUD"   # Audit log entry
    INCIDENT      = "INC"   # Security incident
    REPORT        = "RPT"   # System report
    CML_DECISION  = "CMD"   # CML safety filter decision

    # ── Population Health ─────────────────────────────────────────────────
    OUTBREAK      = "OBK"   # Outbreak / epidemic event
    CAMPAIGN      = "CAM"   # Health campaign
    SURVEY        = "SVY"   # Health survey
    POPULATION    = "POP"   # Population health record

    # ── Descriptions — used in forensic reports ───────────────────────────
    _DESCRIPTIONS = {
        "PAT": "Patient Record",
        "DOC": "Doctor / Clinician",
        "NRS": "Nurse",
        "CGV": "Caregiver",
        "CHW": "Community Health Worker",
        "HSP": "Hospital / Facility",
        "CLN": "Clinic",
        "PHM": "Pharmacy",
        "LBF": "Laboratory Facility",
        "ADM": "Ward Admission",
        "APT": "Appointment",
        "CPL": "Care Plan",
        "RXN": "Prescription",
        "MED": "Medication Record",
        "VRF": "Medication Verification",
        "LAB": "Laboratory Result",
        "DXN": "Diagnosis Record",
        "VST": "Clinical Visit",
        "DSC": "Patient Discharge",
        "REF": "Patient Referral",
        "CNS": "Patient Consent",
        "IMN": "Immunization Record",
        "ALG": "Allergy Record",
        "MON": "Bedside Monitor",
        "ALE": "Clinical Alert",
        "VTL": "Vitals Reading",
        "GTW": "Ward Gateway",
        "WRD": "Hospital Ward",
        "USR": "User Account",
        "SES": "Auth Session",
        "KEY": "API Key",
        "ROL": "Access Role",
        "TXN": "Financial Transaction",
        "INV": "Invoice",
        "PAY": "Payment Record",
        "CLM": "Insurance Claim",
        "RCP": "Payment Receipt",
        "NDI": "Byngonet Node",
        "DEV": "OS Device",
        "OSS": "OS Boot Session",
        "KRN": "Kernel Event",
        "AUD": "Audit Log Entry",
        "INC": "Security Incident",
        "RPT": "System Report",
        "CMD": "CML Safety Decision",
        "OBK": "Outbreak Event",
        "CAM": "Health Campaign",
        "SVY": "Health Survey",
        "POP": "Population Record",
    }

    @classmethod
    def all(cls) -> dict:
        """Return all registered prefixes → descriptions."""
        return dict(cls._DESCRIPTIONS)

    @classmethod
    def is_valid(cls, prefix: str) -> bool:
        return prefix.upper() in cls._DESCRIPTIONS

    @classmethod
    def describe(cls, prefix: str) -> str:
        return cls._DESCRIPTIONS.get(prefix.upper(), "Unknown Entity Type")

    @classmethod
    def by_domain(cls) -> dict:
        """Return prefixes grouped by domain — useful for dashboards."""
        return {
            "health":          ["PAT","DOC","NRS","CGV","CHW","HSP","CLN","PHM","LBF",
                                 "ADM","APT","CPL","RXN","MED","VRF","LAB","DXN","VST",
                                 "DSC","REF","CNS","IMN","ALG"],
            "monitoring":      ["MON","ALE","VTL","GTW","WRD"],
            "identity_access": ["USR","SES","KEY","ROL"],
            "finance":         ["TXN","INV","PAY","CLM","RCP"],
            "infrastructure":  ["NDI","DEV","OSS","KRN"],
            "safety_audit":    ["AUD","INC","RPT","CMD"],
            "population":      ["OBK","CAM","SVY","POP"],
        }
