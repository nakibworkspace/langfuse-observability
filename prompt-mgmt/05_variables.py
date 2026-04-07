"""Lab 5: Variables

Learn how to use variables in Langfuse prompts.
Variables allow dynamic prompt content that gets filled at runtime.
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

# Create prompt with variables using {{variable_name}} syntax
prompt_with_vars = """You are a {{role}} assistant.

Your expertise areas are:
{{expertise_list}}

User context: {{user_context}}

Please help the user with their query."""

# Create prompt in Langfuse
try:
    prompt = langfuse.prompts.create(
        name="variable-prompt",
        prompt=prompt_with_vars,
        description="Prompt demonstrating variables"
    )
    print(f"Created prompt: {prompt.name}")
except Exception as e:
    print(f"Note: {e}")

# Get the prompt and compile with variables
try:
    langfuse_prompt = langfuse.prompts.get("variable-prompt")

    # Define variable values
    variables = {
        "role": "technical",
        "expertise_list": "- Python\n- Machine Learning\n- APIs",
        "user_context": "Developer building an ML pipeline"
    }

    # Get compiled prompt (variables replaced)
    compiled = langfuse_prompt.compile(**variables)
    print(f"\n=== Compiled Prompt ===\n{compiled}")

    # Also use langfuse.openai for direct LLM calls
    from langfuse.openai import openai
    completion = openai.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "system", "content": compiled}],
    )
    print(f"\n=== Model Response ===\n{completion.choices[0].message.content}")

except Exception as e:
    print(f"\nNote: {e}")
    print("\n=== Testing Variables Locally ===")
    # Local variable substitution without Langfuse
    template = "You are a {{role}} specializing in {{specialty}}."
    variables = {"role": "coding assistant", "specialty": "Python"}
    result = template.replace("{{role}}", variables["role"])
    result = result.replace("{{specialty}}", variables["specialty"])
    print(f"Result: {result}")
