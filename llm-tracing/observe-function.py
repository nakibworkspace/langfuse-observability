import os
from dotenv import load_dotenv

load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse.openai import openai
from langfuse import observe

# Observe Function
# decorator to automatically create trace and nest generations
@observe()
def main(country: str, user_id: str, **kwargs) -> str:
    # nested generation 1: use MiniMax to get capital of country
    capital = openai.chat.completions.create(
      name="geography-teacher",
      model="MiniMax-M2.5",
      messages=[
          {"role": "system", "content": "You are a Geography teacher helping students learn the capitals of countries. Output only the capital when being asked."},
          {"role": "user", "content": country}],
      temperature=0,
    ).choices[0].message.content

    # nested generation 2: use MiniMax to write poem on capital
    poem = openai.chat.completions.create(
      name="poet",
      model="MiniMax-M2.5",
      messages=[
          {"role": "system", "content": "You are a poet. Create a poem about a city."},
          {"role": "user", "content": capital}],
      temperature=1,
      max_tokens=500,
    ).choices[0].message.content

    return poem
    
print(main("Bulgaria", "admin"))