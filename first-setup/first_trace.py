import os
from langfuse.openai import openai

# 1. Ollama Configuration
# Note: When running Docker, use 'localhost' if the script is on the host, 
# or 'host.docker.internal' if the script itself is in a container.
openai.api_key = "ollama" # Ollama doesn't require a real key, but a string is needed
openai.base_url = "http://localhost:11434/v1/"

# 2. Langfuse Credentials
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-a10908fd-642a-4b87-9acd-f398efce94b2"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-e2437042-fe54-4b6b-a410-bf212710a520"
os.environ["LANGFUSE_BASE_URL"] = "http://localhost:3001"

# 3. Execution
response = openai.chat.completions.create(
  model="llama3.2:latest", # Ensure you have run 'ollama pull llama3'
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  name="ollama-local-test"
)

print(response.choices[0].message.content)