from agents import function_tool
from pydantic import BaseModel, Field


class MandiPriceInfo(BaseModel):
    crop: str = Field(description="Name of the crop")
    mandi_name: str = Field(description="Name of the agricultural wholesale market")
    price_per_maund_pkr: int = Field(description="Current market price in PKR per maund (40 kg)")
    trend: str = Field(description="Market trend (rising, falling, or stable)")
    advice: str = Field(description="Actionable advice on when to sell the produce")


CROP_MAPPING = {
    "gandum": "wheat", "wheat": "wheat",
    "kapas": "cotton", "cotton": "cotton", "phutti": "cotton",
    "chawal": "rice", "rice": "rice", "dhan": "rice",
    "makai": "maize", "maize": "maize",
    "chana": "chickpea", "chickpea": "chickpea",
    "ganna": "sugarcane", "sugarcane": "sugarcane",
}

MANDI_PRICES = {
    "wheat": {"price": 3200, "trend": "stable", "mandi": "Faisalabad Mandi"},
    "cotton": {"price": 8500, "trend": "rising", "mandi": "Multan Mandi"},
    "rice": {"price": 4500, "trend": "falling", "mandi": "Sheikhupura Mandi"},
    "maize": {"price": 2800, "trend": "stable", "mandi": "Sahiwal Mandi"},
    "chickpea": {"price": 11000, "trend": "rising", "mandi": "Faisalabad Mandi"},
    "sugarcane": {"price": 400, "trend": "stable", "mandi": "Jhang Mandi"},
}


@function_tool
def mandi_price_lookup(crop: str) -> MandiPriceInfo:
    """Look up the current wholesale mandi price for a crop and give selling advice."""
    raw_key = crop.lower().strip()
    crop_key = CROP_MAPPING.get(raw_key, raw_key)
    data = MANDI_PRICES.get(crop_key)

    if not data:
        return MandiPriceInfo(
            crop=raw_key,
            mandi_name="N/A",
            price_per_maund_pkr=0,
            trend="unknown",
            advice="Is fasal ka rate hamare paas mojood nahi. Qareebi mandi committee se maloomat lein.",
        )

    if data["trend"] == "rising":
        advice = "Rate barh raha hai — thora intezar karein, behtar price mil sakta hai."
    elif data["trend"] == "falling":
        advice = "Rate gir raha hai — jaldi bech dena faida mand ho sakta hai."
    else:
        advice = "Rate stable hai — apni zaroorat ke mutabiq bech sakte hain."

    return MandiPriceInfo(
        crop=crop_key,
        mandi_name=data["mandi"],
        price_per_maund_pkr=data["price"],
        trend=data["trend"],
        advice=advice,
    )