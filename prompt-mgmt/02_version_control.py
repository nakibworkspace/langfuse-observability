import os
from dotenv import load_dotenv
load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse import Langfuse, propagate_attributes, get_client, observe
from langfuse.openai import OpenAI

langfuse = Langfuse()

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
