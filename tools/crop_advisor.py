from agents import function_tool
from pydantic import BaseModel, Field


class CropRecommendation(BaseModel):
    crop: str = Field(description="Recommended crop name")
    expected_yield_per_acre: str = Field(description="Expected crop yield range per acre")
    total_estimated_profit_pkr: int = Field(description="Total estimated profit in PKR for the entire land area")
    notes: str = Field(description="Additional farming advice or environmental requirements")


CROP_DATA = {
    ("rabi", "high"): [{"crop": "Wheat (Gandum)", "yield": "40-45 maunds/acre", "profit": 45000, "notes": "Sabse reliable Rabi crop, achi paani availability chahiye."}],
    ("rabi", "low"): [{"crop": "Chickpea (Chana)", "yield": "12-15 maunds/acre", "profit": 35000, "notes": "Kam paani mein bhi acha result deta hai."}],
    ("kharif", "high"): [{"crop": "Rice (Chawal/Dhan)", "yield": "35-40 maunds/acre", "profit": 55000, "notes": "Zyada paani chahiye lekin profit bhi acha hai."}],
    ("kharif", "low"): [{"crop": "Cotton (Kapas)", "yield": "20-25 maunds/acre", "profit": 60000, "notes": "Drought-tolerant, kam paani mein bhi survive karta hai."}],
}


@function_tool
def crop_advisor(season: str, water_availability: str, land_size_acres: float) -> CropRecommendation:
    """Recommend the best crop based on season (Rabi/Kharif), water availability (high/low), and land size in acres."""
    season_key = season.lower().strip()
    water_key = water_availability.lower().strip()

    if "sardi" in season_key or "rabi" in season_key:
        season_key = "rabi"
    elif "garmi" in season_key or "kharif" in season_key:
        season_key = "kharif"

    if "zyada" in water_key or "full" in water_key or "high" in water_key:
        water_key = "high"
    elif "kam" in water_key or "thoda" in water_key or "low" in water_key:
        water_key = "low"

    options = CROP_DATA.get((season_key, water_key))
    if not options:
        options = [{"crop": "Wheat (Gandum)", "yield": "35-40 maunds/acre", "profit": 40000, "notes": "Standard fallback recommendation for general soils."}]

    best = options[0]
    total_profit = int(best["profit"] * land_size_acres)

    return CropRecommendation(
        crop=best["crop"],
        expected_yield_per_acre=best["yield"],
        total_estimated_profit_pkr=total_profit,
        notes=best["notes"],
    )