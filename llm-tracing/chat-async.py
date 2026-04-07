import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse.openai import AsyncOpenAI

async def main():
    # Async Client
    async_client = AsyncOpenAI()

    completion = await async_client.chat.completions.create(
      name="test-chat",
      model="MiniMax-M2.5",
      messages=[
          {"role": "system", "content": "You are a very accurate calculator. You output only the result of the calculation."},
          {"role": "user", "content": "1 + 100 = "}],
      temperature=0,
      metadata={"someMetadataKey": "someValue"},
    )
    
    print(completion.choices[0].message.content)

# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())