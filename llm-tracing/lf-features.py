import os
from dotenv import load_dotenv

load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse.openai import openai

# This will now show up in your dashboard with full user tracking 
completion = openai.chat.completions.create(
  name="calculator-task",
  model="MiniMax-M2.5",
  messages=[
    {"role": "system", "content": "You are a calculator."},
    {"role": "user", "content": "What is 15% of 200?"}
  ],
  temperature=0,
  metadata={
    "langfuse_tags": ["testing", "v1-release"],
    "langfuse_user_id": "poridhi-user-001",
    "langfuse_session_id": "session-abc-123"
  }
)

print(f"MiniMax Result: {completion.choices[0].message.content}")