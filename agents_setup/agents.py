import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()

groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Active Groq model that supports tool calling
groq_model = OpenAIChatCompletionsModel(
    model="openai/gpt-oss-120b",
    openai_client=groq_client
)

kisaan_agent = Agent(
    name="Kisaan Advisor",
    instructions="Aap Pakistan ke kisaanon ke liye ek ziraat expert hain.",
    model=groq_model
)