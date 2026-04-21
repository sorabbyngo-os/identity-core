"""
Africa Region Codes — Sorabbyngo expansion markets.
Format: {ISO2}{region_number:03d}

Kenya (KE) — 47 counties — see kenya.py
Uganda (UG) — districts
Tanzania (TZ) — regions
Rwanda (RW) — provinces
Ethiopia (ET) — regions
Ghana (GH) — regions
Nigeria (NG) — states
South Africa (ZA) — provinces
"""

UGANDA_DISTRICTS = {
    "UG001": "Kampala",      "UG002": "Wakiso",
    "UG003": "Mukono",       "UG004": "Jinja",
    "UG005": "Gulu",         "UG006": "Mbarara",
    "UG007": "Arua",         "UG008": "Lira",
    "UG009": "Mbale",        "UG010": "Masaka",
}

TANZANIA_REGIONS = {
    "TZ001": "Dar es Salaam", "TZ002": "Mwanza",
    "TZ003": "Arusha",        "TZ004": "Dodoma",
    "TZ005": "Mbeya",         "TZ006": "Morogoro",
    "TZ007": "Tanga",         "TZ008": "Zanzibar",
}

RWANDA_PROVINCES = {
    "RW001": "Kigali",        "RW002": "Northern",
    "RW003": "Southern",      "RW004": "Eastern",
    "RW005": "Western",
}

ETHIOPIA_REGIONS = {
    "ET001": "Addis Ababa",   "ET002": "Oromia",
    "ET003": "Amhara",        "ET004": "SNNPR",
    "ET005": "Tigray",        "ET006": "Somali",
}

GHANA_REGIONS = {
    "GH001": "Greater Accra", "GH002": "Ashanti",
    "GH003": "Western",       "GH004": "Eastern",
    "GH005": "Northern",      "GH006": "Volta",
}

NIGERIA_STATES = {
    "NG001": "Lagos",         "NG002": "Abuja (FCT)",
    "NG003": "Kano",          "NG004": "Rivers",
    "NG005": "Ogun",          "NG006": "Kaduna",
    "NG007": "Oyo",           "NG008": "Anambra",
}

SOUTH_AFRICA_PROVINCES = {
    "ZA001": "Gauteng",       "ZA002": "Western Cape",
    "ZA003": "KwaZulu-Natal", "ZA004": "Eastern Cape",
    "ZA005": "Limpopo",       "ZA006": "Mpumalanga",
}

# Unified lookup — all regions across all countries
ALL_REGIONS: dict = {}
ALL_REGIONS.update(UGANDA_DISTRICTS)
ALL_REGIONS.update(TANZANIA_REGIONS)
ALL_REGIONS.update(RWANDA_PROVINCES)
ALL_REGIONS.update(ETHIOPIA_REGIONS)
ALL_REGIONS.update(GHANA_REGIONS)
ALL_REGIONS.update(NIGERIA_STATES)
ALL_REGIONS.update(SOUTH_AFRICA_PROVINCES)

COUNTRY_MAP = {
    "KE": "Kenya",      "UG": "Uganda",
    "TZ": "Tanzania",   "RW": "Rwanda",
    "ET": "Ethiopia",   "GH": "Ghana",
    "NG": "Nigeria",    "ZA": "South Africa",
}


def get_region(code: str) -> str:
    """Get region name from any African region code."""
    from suid.regions.kenya import KENYA_COUNTIES
    code = code.upper()
    return (
        KENYA_COUNTIES.get(code) or
        ALL_REGIONS.get(code) or
        "Unknown"
    )


def get_country(code: str) -> str:
    """Get country name from region code prefix."""
    iso2 = code[:2].upper() if len(code) >= 2 else ""
    return COUNTRY_MAP.get(iso2, "Unknown")


def is_valid_region(code: str) -> bool:
    """Check if region code is valid across all supported countries."""
    from suid.regions.kenya import KENYA_COUNTIES
    return code.upper() in KENYA_COUNTIES or code.upper() in ALL_REGIONS
