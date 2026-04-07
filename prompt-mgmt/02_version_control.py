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

# Create the prompt in Langfuse (run once)
try:
    prompt = langfuse.prompts.create(
        name="versioned-prompt",
        prompt=initial_prompt,
        description="Initial version of assistant prompt"
    )
    print(f"Created prompt: {prompt.name} (v{prompt.version})")
except Exception as e:
    print(f"Prompt might already exist: {e}")

# Update the prompt - creates a new version
updated_prompt_text = """You are a helpful assistant specialized in coding.
Always provide code examples when possible."""

try:
    updated = langfuse.prompts.update(
        name="versioned-prompt",
        prompt=updated_prompt_text,
        description="Added coding specialization"
    )
    print(f"Updated prompt: {updated.name} (v{updated.version})")
except Exception as e:
    print(f"Update failed: {e}")

# Get all versions
try:
    versions = langfuse.prompts.get_many(name="versioned-prompt")
    print(f"\nAll versions of 'versioned-prompt':")
    for v in versions.data:
        print(f"  - Version {v.version}: {v.prompt[:50]}...")
except Exception as e:
    print(f"Error getting versions: {e}")

# Get specific version
try:
    v1 = langfuse.prompts.get("versioned-prompt", version=1)
    print(f"\nVersion 1 content: {v1.prompt}")

    v2 = langfuse.prompts.get("versioned-prompt", version=2)
    print(f"Version 2 content: {v2.prompt}")
except Exception as e:
    print(f"Error: {e}")
    print("\nTo test versioning: Create prompts in Langfuse UI")
