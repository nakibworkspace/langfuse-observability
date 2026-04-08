import os
from dotenv import load_dotenv
from langfuse import Langfuse, get_client
from langfuse.openai import OpenAI

load_dotenv()

langfuse = Langfuse()

# Text prompt w variables
langfuse.create_prompt(
    name="movie-critic",
    type="text",
    prompt="As a {{criticlevel}} movie critic, do you like {{movie}}?",
    labels=["production"]
)

# chat prompt w variables
# langfuse.create_prompt(
#     name="movie-critic-chat",
#     type="chat",
#     prompt=[
#         {
#             "role": "system",
#             "content": "You are a {{criticlevel}} movie critic."
#         },
#         {
#             "role": "user",
#             "content": "What do you think about {{movie}}?"
#         }
#     ],
#     labels=["production"],
# )