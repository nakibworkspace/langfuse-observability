"""Lab 6: Prompt Composability
Learn how to compose prompts from multiple smaller prompts. This allows reusability and modular prompt design."""
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

# Define reusable prompt components
SYSTEM_PROMPT = """You are a helpful AI assistant.
Your responses should be clear and concise."""

STYLE_GUIDELINES = """Follow these style guidelines:
- Use simple language
- Include examples when helpful
- Format code properly"""

DOMAIN_PREFIXES = {
    "coding": "Focus on providing working code examples.",
    "writing": "Focus on clear, well-structured prose.",
    "analysis": "Focus on data-driven insights."
}

def compose_prompt(base_prompt: str, style: str, domain: str) -> str:
    """Compose a complete prompt from components"""
    parts = [
        SYSTEM_PROMPT,
        STYLE_GUIDELINES,
        DOMAIN_PREFIXES.get(domain, ""),
        base_prompt
    ]
    return "\n\n".join(p for p in parts if p)

# Create prompts in Langfuse (conceptual)
prompt_configs = [
    ("system-base", SYSTEM_PROMPT, "Core system instructions"),
    ("style-guide", STYLE_GUIDELINES, "Style guidelines"),
    ("coding-style", DOMAIN_PREFIXES["coding"], "Coding-specific style")
]

for name, content, desc in prompt_configs:
    try:
        langfuse.prompts.create(name=name, prompt=content, description=desc)
    except:
        pass

print("=== Prompt Composability Demo ===\n")

# Compose prompts dynamically
test_cases = [
    ("Explain what is a variable", "writing", "coding"),
    ("Write a function to sort a list", "coding", "coding"),
    ("Analyze this data trend", "analysis", "writing")
]

for base, style, domain in test_cases:
    composed = compose_prompt(base, style, domain)
    print(f"Base: {base}")
    print(f"Composed prompt preview: {composed[:80]}...")
    print("-" * 50)

# Using prompt references
print("\n=== Using Prompt References ===")
print("You can reference other prompts in Langfuse:")
print("  {{prompt:system-base}}")
print("  {{prompt:style-guide}}")
print("\nThis allows creating a library of reusable components.")
