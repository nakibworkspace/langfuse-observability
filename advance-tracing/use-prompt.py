import os
import json
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.openai import openai

load_dotenv()

# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

# 1. Initialize Langfuse Client
langfuse = Langfuse()

# 2. Retrieve the prompt from Langfuse
# This gets the version you labeled 'production'
prompt_obj = langfuse.get_prompt("story_summarization", label="production")

# 3. Prepare your dynamic data
story_text = "Once upon a time, a brave knight named Leo fought a dragon in the snowy mountains of Alps."

# 4. Compile the prompt 
# (Injects the json_schema from the config into the prompt string)
full_prompt_text = prompt_obj.compile(
    json_schema=json.dumps(prompt_obj.config["json_schema"], indent=2)
)

# 5. Call the LLM
# We use prompt_obj.config to stay synced with Langfuse settings
response = openai.chat.completions.create(
    name="summarization-task",
    model=prompt_obj.config["model"],
    temperature=prompt_obj.config["temperature"],
    messages=[
        {"role": "system", "content": full_prompt_text},
        {"role": "user", "content": f"Here is the story: {story_text}"}
    ],
    # This links the generation to the prompt in the Langfuse dashboard
    langfuse_prompt=prompt_obj 
)

print(response.choices[0].message.content)