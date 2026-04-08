import os
from dotenv import load_dotenv
from langfuse import Langfuse, propagate_attributes, get_client, observe
from langfuse.openai import OpenAI

load_dotenv()

langfuse = Langfuse()

prompt = langfuse.get_prompt("movie-critic", label="prod-1")

compiled = prompt.compile(movie="SpiderMan", criticlevel="novice")

@observe()
def run_app():
    with propagate_attributes(
        trace_name="critic-task-v1",
        session_id="nakib-123",
        tags=["testing", "ollama"],
        metadata={"env": "local", "version": "4.0.6"}
    ):
    
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

        completion = client.chat.completions.create(
            model="llama3.2:latest",
            messages=[{"role": "user", "content": compiled}],
            langfuse_prompt=prompt # 4. LINK the prompt version to this trace
        )
        return completion.choices[0].message.content

if __name__ == "__main__":
    print(run_app())
    get_client().flush() # v4 uses get_client() to flush the buffer
