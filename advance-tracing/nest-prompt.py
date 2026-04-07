import os
import uuid
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.openai import openai

load_dotenv()

# Setup environment for MiniMax
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 1. Initialize the client
langfuse = Langfuse()

# 2. Generate unique IDs manually
# This is what the newer SDK does automatically
my_trace_id = str(uuid.uuid4())
my_span_id = str(uuid.uuid4())

print(f"Starting trace with ID: {my_trace_id}")

# 3. Create the Span
# In older SDKs, we use the client to "span" directly
span = langfuse.span(
    name="Story-Analysis-Workflow",
    trace_id=my_trace_id,
    id=my_span_id
)

# 4. The LLM Call
# We link it to the trace and span using the manual IDs
response = openai.chat.completions.create(
    model="MiniMax-M2.5",
    name="summarization-task",
    messages=[{"role": "user", "content": "Tell me a joke about Python programming."}],
    trace_id=my_trace_id,
    parent_observation_id=my_span_id
)

# 5. End the span
span.end(output="AI finished successfully")

# 6. Push to server
langfuse.flush()

print("Check Langfuse now! Everything should be nested.")