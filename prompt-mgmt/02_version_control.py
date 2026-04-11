"""Lab 2: Version Control

Learn how Langfuse handles prompt versioning.
Langfuse automatically versions your prompts when you update them,
allowing you to track changes over time and roll back if needed.
"""
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_BASE_URL")

from langfuse import Langfuse

langfuse = Langfuse()

# Create a prompt with initial version
initial_prompt = """You are a helpful assistant."""

# Create the prompt in Langfuse (run ONCE - the first time only!)
try:
    prompt = langfuse.create_prompt(
        name="versioned-prompt",
        prompt=initial_prompt,
        labels=["v1"]
    )
    print(f"Created prompt: {prompt.name}")
except Exception as e:
    print(f"Prompt might already exist: {e}")

# Update the prompt - creates a new version
updated_prompt_text = """You are a helpful assistant specialized in coding.
Always provide code examples when possible."""

# Note: In newer Langfuse API, use create_ to add new versions with labels
try:
    updated = langfuse.create_prompt(
        name="versioned-prompt",
        prompt=updated_prompt_text,
        labels=["v2"]
    )
    print(f"Updated prompt: {updated.name}")
except Exception as e:
    print(f"Update failed: {e}")

# Get all versions - use get_prompt with labels
try:
    v1 = langfuse.get_prompt("versioned-prompt", label="v1")
    print(f"\nVersion v1 content: {v1.prompt}")

    v2 = langfuse.get_prompt("versioned-prompt", label="v2")
    print(f"Version v2 content: {v2.prompt}")
except Exception as e:
    print(f"Error: {e}")
    print("\nTo test versioning: Create prompts in Langfuse UI")
