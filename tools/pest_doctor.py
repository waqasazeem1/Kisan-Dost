from agents import function_tool
from pydantic import BaseModel, Field


class PestDiagnosis(BaseModel):
    likely_issue: str = Field(description="Identified pest or crop disease name")
    treatment: str = Field(description="Recommended medicine or fungicide treatment")
    safe_dosage: str = Field(description="Safe dosage limit per acre or per liter of water")
    warning: str = Field(description="Safety precautions and handling warnings")


PEST_DATABASE = [
    {
        "keywords": ["whitefly", "white insect", "chitay keeray", "leaves curling", "pattay murh", "sufaid makhi", "safed makhi"],
        "issue": "Whitefly (Sufaid Makhi)",
        "treatment": "Imidacloprid spray",
        "dosage": "200ml per acre, diluted in 100L water — SAFE LIMIT, do not exceed",
        "warning": "Spray shaam ko karein jab dhoop kam ho. Bachon aur janwaron ko door rakhein.",
    },
    {
        "keywords": ["aphid", "chota keera", "sticky leaves", "chipchipa", "aphids", "sundhi", "kala keera"],
        "issue": "Aphids (Chotay Keeray)",
        "treatment": "Neem oil spray (organic) ya Acetamiprid",
        "dosage": "5ml neem oil per liter water",
        "warning": "Neem oil safe hai lekin phir bhi dastane pehen kar spray karein.",
    },
    {
        "keywords": ["yellow leaves", "peeli pattay", "pattay peele", "fungus", "spots", "leaf spot", "brown spots"],
        "issue": "Fungal Leaf Spot",
        "treatment": "Copper-based fungicide",
        "dosage": "3g per liter water — SAFE LIMIT",
        "warning": "Zyada dosage mitti ko nuksan pohcha sakti hai.",
    },
    {
        "keywords": ["rust", "orange pustule", "zangeer", "zang", "brown powder", "surkh dhabay"],
        "issue": "Leaf Rust (Zang)",
        "treatment": "Propiconazole fungicide",
        "dosage": "Label ke mutabiq, roughly 25ml per 100L water — SAFE LIMIT",
        "warning": "Pehle chhoti patch par try karein. Phal/pattay khane se pehle waiting period follow karein.",
    },
    {
        "keywords": ["blight", "wilting", "pattay jalna", "water-soaked", "late blight", "sookhna"],
        "issue": "Blight",
        "treatment": "Mancozeb ya copper fungicide",
        "dosage": "2g per liter water — SAFE LIMIT",
        "warning": "Geela mausam mein repeat spray se pehle label padhein.",
    },
]


@function_tool
def pest_disease_doctor(symptoms_description: str) -> PestDiagnosis:
    """Identify likely pest or disease from farmer's symptom description and give safe treatment dosage."""
    desc_lower = symptoms_description.lower().strip()

    for entry in PEST_DATABASE:
        if any(keyword in desc_lower for keyword in entry["keywords"]):
            return PestDiagnosis(
                likely_issue=entry["issue"],
                treatment=entry["treatment"],
                safe_dosage=entry["dosage"],
                warning=entry["warning"],
            )

    return PestDiagnosis(
        likely_issue="Pehchan nahi ho saki (unclear symptoms)",
        treatment="Local agriculture extension officer se check karayein",
        safe_dosage="N/A — pehle sahi diagnosis zaroori hai",
        warning="Bina sahi pehchan ke koi bhi dawai spray na karein.",
    )