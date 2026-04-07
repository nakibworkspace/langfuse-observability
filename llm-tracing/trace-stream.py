import os
from langfuse.openai import openai
from dotenv import load_dotenv

load_dotenv()

# Streaming functionality.
completion = openai.chat.completions.create(
  name="test-chat",
  model="MiniMax-M2.5",
  messages=[
      {"role": "system", "content": "You are a professional comedian."},
      {"role": "user", "content": "Tell me a joke."}],
  temperature=0,
  metadata={"someMetadataKey": "someValue"},
  stream=True
)

for chunk in completion:
  print(chunk.choices[0].delta.content, end="")