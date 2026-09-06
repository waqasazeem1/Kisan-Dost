import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

async def list_models():
    client = AsyncOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    try:
        models = await client.models.list()
        print("\n=== AAP KI GROQ KEY PAR ACTIVE MODELS ===")
        for m in models.data:
            print(f"- {m.id}")
    except Exception as e:
        print("Error listing models:", e)

if __name__ == "__main__":
    asyncio.run(list_models())