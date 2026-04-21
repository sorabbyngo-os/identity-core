"""
Kenya County Codes — all 47 counties
Format: KE{county_number:03d}
"""

KENYA_COUNTIES = {
    "KE001": "Mombasa",
    "KE002": "Kwale",
    "KE003": "Kilifi",
    "KE004": "Tana River",
    "KE005": "Lamu",
    "KE006": "Taita Taveta",
    "KE007": "Garissa",
    "KE008": "Wajir",
    "KE009": "Mandera",
    "KE010": "Marsabit",
    "KE011": "Isiolo",
    "KE012": "Meru",
    "KE013": "Tharaka Nithi",
    "KE014": "Embu",
    "KE015": "Kitui",
    "KE016": "Machakos",
    "KE017": "Makueni",
    "KE018": "Nyandarua",
    "KE019": "Nyeri",
    "KE020": "Kirinyaga",
    "KE021": "Murang'a",
    "KE022": "Kiambu",
    "KE023": "Turkana",
    "KE024": "West Pokot",
    "KE025": "Samburu",
    "KE026": "Trans Nzoia",
    "KE027": "Uasin Gishu",
    "KE028": "Elgeyo Marakwet",
    "KE029": "Nandi",
    "KE030": "Baringo",
    "KE031": "Laikipia",
    "KE032": "Nakuru",
    "KE033": "Narok",
    "KE034": "Kajiado",
    "KE035": "Kericho",
    "KE036": "Bomet",
    "KE037": "Kakamega",
    "KE038": "Vihiga",
    "KE039": "Bungoma",
    "KE040": "Busia",
    "KE041": "Siaya",
    "KE042": "Kisumu",
    "KE043": "Homa Bay",
    "KE044": "Migori",
    "KE045": "Kisii",
    "KE046": "Nyamira",
    "KE047": "Nairobi",
}

def get_county(code: str) -> str:
    return KENYA_COUNTIES.get(code, "Unknown")

def get_code(county: str) -> str:
    for code, name in KENYA_COUNTIES.items():
        if name.lower() == county.lower():
            return code
    return "KE000"
