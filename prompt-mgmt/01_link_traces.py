import os
from dotenv import load_dotenv
load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse()

## Method 1: Using the prompt object
prompt = langfuse.get_prompt("movie-critic")
compiled_prompt = prompt.compile(criticlevel="expert", movie="Dune 2")

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = openai.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[{"role": "user", "content": compiled_prompt}],
    # 3. This is the "Magic" line that links the prompt to the trace
    langfuse_prompt=prompt
)

print(completion.choices[0].message.content)

# Method 2: Using the prompt name and type

prompt = langfuse.get_prompt("movie-critic", type="chat")
compiled_prompt = prompt.compile(criticlevel="expert", movie="Dune 2")

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[{"role": "user", "content": compiled_prompt}],
    # 3. This is the "Magic" line that links the prompt to the trace
    langfuse_prompt=prompt
)

print(completion.choices[0].message.content)

# Method 3: Adding Tags and Metadata

import os
from dotenv import load_dotenv
from langfuse import Langfuse, observe, propagate_attributes, get_client
from langfuse.openai import OpenAI

load_dotenv()

# 1. Initialize administrative client (for prompts)
langfuse = Langfuse()

# 2. Initialize local Ollama client (using the wrapped version)
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

@observe() 
def run_movie_critic():
    # 3. Fetch Prompt
    prompt = langfuse.get_prompt("movie-critic")
    compiled_prompt = prompt.compile(criticlevel="expert", movie="Dune 2")

    # 4. V4 LOGIC: Use propagate_attributes context manager
    # Attributes MUST be strings in v4. Values over 200 chars are dropped.
    with propagate_attributes(
        trace_name="movie-review-task",
        session_id="user-unique-session-001",
        tags=["testing", "minimax"],
        metadata={"user_tier": "free", "internal_id": "99"} 
    ):
        # 5. Generate response
        # Because this is inside the 'with' block, it inherits the session_id/tags
        completion = client.chat.completions.create(
            model="llama3.2:latest",
            messages=[{"role": "user", "content": compiled_prompt}],
            langfuse_prompt=prompt
        )
        
        return completion.choices[0].message.content

if __name__ == "__main__":
    result = run_movie_critic()
    print(f"AI Response: {result}")
    
    # 6. Flush using get_client() in v4
    get_client().flush()
