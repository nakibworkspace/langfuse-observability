from typing import List
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

load_dotenv()

# MiniMax Configuration
# Set env vars before importing langfuse.openai
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

from langfuse.openai import OpenAI

# We initialize the client with MiniMax's endpoint
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# Pydantic Class
class StepByStepAIResponse(BaseModel):
    title: str
    steps: List[str]
schema = StepByStepAIResponse.model_json_schema() # returns a dict like JSON schema


# Execute the Tool-Calling request
response = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[
        {"role": "user", "content": "Explain how to assemble a PC"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_answer_for_user_query",
                "description": "Get user answer in a series of steps",
                "parameters": StepByStepAIResponse.model_json_schema()
            }
        }
    ],
    tool_choice={"type": "function", "function": {"name": "get_answer_for_user_query"}}
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)