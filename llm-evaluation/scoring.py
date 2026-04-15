import os
from openai import OpenAI
from langfuse import get_client
from dotenv import load_dotenv
load_ dotenv()
# 1. Initialize Langfuse v4 client
langfuse = get_ client()  # Uses env vars: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
# 2. Initialize MiniMax client
client = OpenAI(
    base_ url=os.getenv("OPENAI_BASE_URL", "https://api.minimax.io/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)
# 3. Start an observation (v4 uses observations-first model)
with langfuse.start_as_current_observation(
    as_type="generation",
    name="local-math-query",
    model="MiniMax-Text-01",
    input="What is 2 + 2?"
) as generation:
    # 4. Call MiniMax model
    response = client.chat.completions.create(
        model="MiniMax-Text-01",
        messages=[{"role": "user", "content": "What is 2 + 2?"}],
        temperature=0.1
    )
    output_text = response.choices[0].message.content
    # 5. Update the observation with output
    generation.update(output=output_text)
    # 6. Score the observation
    generation.score(
        name="correctness",
        value=1.0 if "4" in output_text else 0.0,  # Must be float for NUMERIC
        data_type="NUMERIC",  # Optional: inferred if omitted
        comment="MiniMax model answered correctly"
    )
# 7. Flush to ensure scores are sent (critical for short scripts)
langfuse.flush()
print(f"Score sent to Langfuse!")
