import asyncio
from agents import Agent, ModelSettings, Runner, handoff
from agents.exceptions import InputGuardrailTripwireTriggered
from agents_setup.agents import groq_model
from agents_setup.guardrails import farming_topic_guardrail
from pydantic import BaseModel, Field
from tools.crop_advisor import crop_advisor
from tools.fertilizer import fertilizer_calculator
from tools.govt_support import govt_support_finder
from tools.mandi_price import mandi_price_lookup
from tools.pest_doctor import pest_disease_doctor

LANGUAGE_RULE = (
    "LANGUAGE RULE:\n"
    "Always reply in the SAME language/style the farmer used in their question.\n"
    "- If the farmer writes in Roman Urdu, reply in Roman Urdu.\n"
    "- If the farmer writes in English, reply in English.\n"
    "- NEVER reply in Urdu script (اردو حروف) — always convert to Roman Urdu instead.\n"
    "- Keep responses brief, concise, and under 250 words.\n"
)
# ---- Specialist Agent 1: Agronomy ----
agronomy_agent = Agent(
    name="Agronomy Agent",
    instructions=(
        "You are the Agronomy specialist inside Kisan Dost. "
        "You handle crop recommendation (crop_advisor) and fertilizer "
        "calculation (fertilizer_calculator) questions only.\n\n" + LANGUAGE_RULE
    ),
    model=groq_model,
    model_settings=ModelSettings(max_tokens=600, extra_body={"reasoning_effort": "low"}),
    tools=[fertilizer_calculator, crop_advisor],
)

# ---- Specialist Agent 2: Pest Doctor ----
pest_agent = Agent(
    name="Pest Doctor Agent",
    instructions=(
        "You are the Pest & Disease specialist inside Kisan Dost. "
        "Use pest_disease_doctor to diagnose crop issues from symptoms. "
        "Never give human medical advice.\n\n" + LANGUAGE_RULE
    ),
    model=groq_model,
    model_settings=ModelSettings(max_tokens=800, extra_body={"reasoning_effort": "low"}),
    tools=[pest_disease_doctor],
)

# ---- Specialist Agent 3: Market ----
market_agent = Agent(
    name="Market Agent",
    instructions=(
        "You are the Market specialist inside Kisan Dost. "
        "Use mandi_price_lookup to tell farmers the current mandi price for their crop "
        "and give simple advice on when to sell.\n\n" + LANGUAGE_RULE
    ),
    model=groq_model,
    model_settings=ModelSettings(max_tokens=800, extra_body={"reasoning_effort": "low"}),
    tools=[mandi_price_lookup],
)


# ---- Specialist Agent 4: Govt Support ----
govt_agent = Agent(
    name="Govt Support Agent",
    instructions=(
        "You are the Government Schemes specialist inside Kisan Dost. "
        "Use govt_support_finder to tell farmers about relevant schemes like "
        "Kisan Card, fertilizer subsidy, agri loans, or tractor subsidy.\n\n" + LANGUAGE_RULE
    ),
    model=groq_model,
    model_settings=ModelSettings(max_tokens=800, extra_body={"reasoning_effort": "low"}),
    tools=[govt_support_finder],
)


class HandoffReason(BaseModel):
    reason: str = Field(
        default="Transferring query to specialist agent",
        description="Reason for handoff",
    )


def on_handoff(ctx, data: HandoffReason):
    pass


# ---- Triage Agent ----
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are the front-desk of Kisan Dost. Read the farmer's question and "
        "hand off to the correct specialist:\n"
        "- Fertilizer or crop recommendation questions → Agronomy Agent\n"
        "- Pest, insect, or disease symptom questions → Pest Doctor Agent\n"
        "- Mandi price or selling questions → Market Agent\n"
        "- Government scheme, subsidy, Kisan Card, or loan questions → Govt Support Agent\n"
        "Do not answer farming questions yourself — always hand off.\n\n"
        + LANGUAGE_RULE
    ),
    model=groq_model,
    model_settings=ModelSettings(max_tokens=800, extra_body={"reasoning_effort": "low"}),
    handoffs=[
        handoff(agronomy_agent, on_handoff=on_handoff, input_type=HandoffReason),
        handoff(pest_agent, on_handoff=on_handoff, input_type=HandoffReason),
        handoff(market_agent, on_handoff=on_handoff, input_type=HandoffReason),
        handoff(govt_agent, on_handoff=on_handoff, input_type=HandoffReason),
    ],
    input_guardrails=[farming_topic_guardrail],
)


GUARDRAIL_REPLY = (
    "Maaf kijiye, main sirf kheti-baari se mutalliq sawalat ka jawab de sakta hoon."
)


async def ask_kisan(user_input: str) -> str:
    try:
        result = await Runner.run(triage_agent, user_input)
        return str(result.final_output)
    except InputGuardrailTripwireTriggered:
        return GUARDRAIL_REPLY


async def run_agent(user_input: str):
    reply = await ask_kisan(user_input)
    print(f"\nKisan Dost: {reply}\n")


async def main():
    print("=== Kisan Dost ===")
    print(
        "Apna sawal likho — fertilizer, crop advice, pest/disease, ya mandi rate, kuch bhi pooch sakte ho."
    )
    print("Type 'exit' quit karne ke liye\n")

    while True:
        user_input = input("Kisan: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        await run_agent(user_input)


if __name__ == "__main__":
    asyncio.run(main())