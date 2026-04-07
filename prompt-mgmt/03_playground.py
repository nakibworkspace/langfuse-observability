"""Lab 3: Playground

Learn how to use the Langfuse Playground for testing prompts.
The Playground allows you to test prompts interactively before
deploying them to production.
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

# Fetch a prompt to test in playground-like scenario
try:
    # Get a prompt from Langfuse
    prompt = langfuse.prompts.get("my-prompt", version=1)

    print("=== Langfuse Playground Simulation ===")
    print(f"Prompt Name: {prompt.name}")
    print(f"Version: {prompt.version}")
    print(f"\nPrompt Content:")
    print(prompt.compiled)
    print("\n" + "="*50)

    # Simulate playground test
    test_input = "Hello, how can you help me?"
    print(f"\nTest Input: {test_input}")
    print("Test Output would appear in playground UI")

except Exception as e:
    print(f"Note: {e}")
    print("\n=== Playground Setup ===")
    print("1. Go to Langfuse Dashboard > Playground")
    print("2. Select a prompt from the dropdown")
    print("3. Test with different inputs")
    print("4. Compare model responses")
    print("\nThe playground also provides:")
    print("- Model selection (GPT-4, Claude, etc.)")
    print("- Temperature/max tokens config")
    print("- Real-time cost tracking")
