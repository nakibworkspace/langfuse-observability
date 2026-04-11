import os
from dotenv import load_dotenv
load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse import Langfuse, propagate_attributes, get_client, observe
from langfuse.openai import OpenAI

langfuse = Langfuse()

<<<<<<< HEAD
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
=======
prompt = langfuse.get_prompt("movie-critic", label="prod-1")

compiled = prompt.compile(movie="SpiderMan", criticlevel="novice")

@observe()
def run_app():
    with propagate_attributes(
        trace_name="critic-task-v1",
        session_id="nakib-123",
        tags=["testing", "minimax"],
        metadata={"env": "local", "version": "4.0.6"}
    ):
    
        client = OpenAI()

        completion = client.chat.completions.create(
            model="MiniMax-M2.5",
            messages=[{"role": "user", "content": compiled}],
            langfuse_prompt=prompt # 4. LINK the prompt version to this trace
        )
        return completion.choices[0].message.content

if __name__ == "__main__":
    print(run_app())
    get_client().flush() # v4 uses get_client() to flush the buffer
>>>>>>> 930c1c2e3566e9b179420446876cd2a188271b6c
