import os
from langfuse.openai import openai
from dotenv import load_dotenv

load_dotenv()

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