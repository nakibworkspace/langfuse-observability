import os
from dotenv import load_dotenv

load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse.openai import openai

# Use Chat Creation
response = openai.chat.completions.create(
  model="MiniMax-M2.5", # Use your specific MiniMax model name
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  name="minimax-test-run" # Optional: Langfuse trace name
)

print(response.choices[0].message.content)