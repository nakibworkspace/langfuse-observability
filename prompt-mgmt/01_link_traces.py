"""Lab 1: Link to Traces

Learn how to link Langfuse prompts to traced LLM calls.
In Langfuse, you can link a prompt to a trace by using the prompt's name
and version in your API calls. This creates a direct connection between
your prompt management and observability.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Langfuse
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_BASE_URL")

from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse()

# Method 1: Get prompt from Langfuse and use in trace
try:
    prompt_obj = langfuse.prompts.get("my-prompt", version=1)

    completion = openai.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[
            {"role": "system", "content": prompt_obj.compiled},
            {"role": "user", "content": "What is machine learning?"}
        ],
        prompt=prompt_obj.name,
    )

    print(f"Response: {completion.choices[0].message.content}")
    print(f"Trace linked to prompt: {prompt_obj.name}")

except Exception as e:
    print(f"Note: {e}")
    print("\nTo test this feature:")
    print("1. Create a prompt in Langfuse UI named 'my-prompt'")
    print("2. Add a version with content like 'You are a helpful assistant.'")
    print("3. Run this script again")

# Method 2: Direct prompt reference in metadata
completion2 = openai.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Explain variables in Python"}
    ],
    metadata={
        "langfuse_prompt_name": "my-prompt",
        "langfuse_prompt_version": 1
    }
)

print(f"\nMethod 2 - Direct reference:")
print(f"Response: {completion2.choices[0].message.content}")
