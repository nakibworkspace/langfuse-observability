import os
from dotenv import load_dotenv
load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

import random
from langfuse import Langfuse, observe, propagate_attributes, get_client
from langfuse.openai import OpenAI

langfuse = Langfuse()
client = OpenAI()

@observe()
def run_ab_test_critic(movie_title):
    # 1. Fetch both options from the cache
    prompt_a = langfuse.get_prompt("movie-critic", label="prod-1")
    prompt_b = langfuse.get_prompt("movie-critic", label="basic")

    # 2. The Flip: 50/50 chance
    selected_prompt = random.choice([prompt_a, prompt_b])
    
    # 3. Track which one was picked in the metadata
    version_label = "A" if selected_prompt == prompt_a else "B"

    with propagate_attributes(
        trace_name="critic-ab-test",
        tags=["ab-test", f"version-{version_label}"], # Tagging is crucial for filtering later!
        metadata={"experimental_group": version_label}
    ):
        completion = client.chat.completions.create(
            model="MiniMax-M2.5",
            messages=[{"role": "user", "content": selected_prompt.compile(movie=movie_title)}],
            langfuse_prompt=selected_prompt # CRITICAL: This links the metrics to Version A or B
        )
        return completion.choices[0].message.content

if __name__ == "__main__":
    result = run_ab_test_critic("Inception")
    print(result)
    
    # This ensures all background traces are sent before the script exits
    langfuse.flush()