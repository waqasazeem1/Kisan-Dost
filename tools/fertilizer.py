from agents import function_tool
from pydantic import BaseModel, Field


class FertilizerPlan(BaseModel):
    crop: str = Field(description="Name of the crop")
    acres: float = Field(description="Land area in acres")
    urea_bags: float = Field(description="Total bags of Urea required (50kg per bag)")
    dap_bags: float = Field(description="Total bags of DAP required (50kg per bag)")
    total_cost_pkr: int = Field(description="Total estimated cost of fertilizer in PKR")


CROP_NPK = {
    "wheat": {"urea": 2.5, "dap": 1.5},
    "gandum": {"urea": 2.5, "dap": 1.5},
    "cotton": {"urea": 3.0, "dap": 2.0},
    "kapas": {"urea": 3.0, "dap": 2.0},
    "rice": {"urea": 2.0, "dap": 1.0},
    "chawal": {"urea": 2.0, "dap": 1.0},
    "maize": {"urea": 3.5, "dap": 2.0},
    "makai": {"urea": 3.5, "dap": 2.0},
}

UREA_PRICE = 3200
DAP_PRICE = 12500


@function_tool
def fertilizer_calculator(crop: str, acres: float) -> FertilizerPlan:
    """Calculate Urea and DAP bags needed for a crop and land size in acres, with total cost in PKR."""
    crop_key = crop.lower().strip()
    rates = CROP_NPK.get(crop_key, {"urea": 2.5, "dap": 1.5})

    urea_bags = round(rates["urea"] * acres, 1)
    dap_bags = round(rates["dap"] * acres, 1)
    total_cost = int(urea_bags * UREA_PRICE + dap_bags * DAP_PRICE)

    return FertilizerPlan(
        crop=crop_key,
        acres=acres,
        urea_bags=urea_bags,
        dap_bags=dap_bags,
        total_cost_pkr=total_cost,
    )