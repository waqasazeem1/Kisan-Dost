from agents import function_tool
from pydantic import BaseModel, Field


class GovtSupportInfo(BaseModel):
    scheme_name: str = Field(description="Name of the government support scheme")
    eligibility: str = Field(description="Who can apply for this scheme")
    benefit: str = Field(description="What the farmer gets from this scheme")
    how_to_apply: str = Field(description="Steps or place to apply")


# Hardcoded realistic Punjab/Pakistan agri schemes
SCHEMES = {
    "kisan card": {
        "eligibility": "Registered farmers with a valid CNIC and land record (malkiyat ya theka).",
        "benefit": "Subsidized loans, fertilizer, aur agri-inputs seedha card ke zariye.",
        "apply": "Nazdeeki Zarai Taraqiati Bank (ZTBL) ya Kisan Card centre mein CNIC aur land record ke sath jama karayein.",
    },
    "fertilizer subsidy": {
        "eligibility": "Chhotay aur darmiyanay kisan jinke paas 25 acre tak zameen ho.",
        "benefit": "Urea aur DAP par har bag pe sarkari subsidy, market rate se kam qeemat.",
        "apply": "Punjab Agriculture Department ke dealer se registered dukanon par CNIC dikha kar khareedein.",
    },
    "agri loan": {
        "eligibility": "Koi bhi kisan jiske paas zameen ka sabooti record ho.",
        "benefit": "Kam markup rate par loan — beej, khaad, machinery ke liye.",
        "apply": "ZTBL ya kisi bhi commercial bank ki agri-loan branch mein CNIC aur zameen ke kagzaat le kar jayein.",
    },
    "tractor subsidy": {
        "eligibility": "Chhotay kisan jinke paas apna tractor nahi.",
        "benefit": "Naye tractor ki khareed par sarkari subsidy ya asaan qiston par scheme.",
        "apply": "Agriculture Department Punjab ki website (agripunjab.gov.pk) ya zilay ke agri office se maloomat lein.",
    },
}

# Keyword mapping so farmers can ask in their own words
KEYWORD_MAP = {
    "kisan card": "kisan card",
    "card": "kisan card",
    "fertilizer": "fertilizer subsidy",
    "khaad": "fertilizer subsidy",
    "subsidy": "fertilizer subsidy",
    "loan": "agri loan",
    "qarza": "agri loan",
    "karza": "agri loan",
    "tractor": "tractor subsidy",
}


@function_tool
def govt_support_finder(need: str) -> GovtSupportInfo:
    """Find relevant Pakistani government agriculture schemes (Kisan Card, fertilizer subsidy, agri loan, tractor subsidy) based on the farmer's need."""
    need_lower = need.lower().strip()

    matched_key = None
    for keyword, scheme_key in KEYWORD_MAP.items():
        if keyword in need_lower:
            matched_key = scheme_key
            break

    if not matched_key:
        matched_key = "kisan card"  # sensible default — most general scheme

    scheme = SCHEMES[matched_key]

    return GovtSupportInfo(
        scheme_name=matched_key.title(),
        eligibility=scheme["eligibility"],
        benefit=scheme["benefit"],
        how_to_apply=scheme["apply"],
    )