import os
from openai import OpenAI
from langfuse import get_client
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize Langfuse v4 client
langfuse = get_client()  # Uses env vars: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST

# 2. Initialize Ollama via OpenAI-compatible client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Dummy key required by OpenAI SDK
)

# 3. Start an observation (v4 uses observations-first model) [[5]]
with langfuse.start_as_current_observation(
    as_type="generation",
    name="local-math-query",
    model="llama3.2",
    input="What is 2 + 2?"
) as generation:
    
    # 4. Call local Ollama model
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": "What is 2 + 2?"}],
        temperature=0.1
    )
    output_text = response.choices[0].message.content
    
    # 5. Update the observation with output
    generation.update(output=output_text)
    
    # 6. ✅ Score the observation (NOT trace_id="first-trace")
    generation.score(
        name="correctness",
        value=1.0 if "4" in output_text else 0.0,  # Must be float for NUMERIC
        data_type="NUMERIC",  # Optional: inferred if omitted
        comment="Local model answered correctly"
    )

# 7. Flush to ensure scores are sent (critical for short scripts) [[12]]
langfuse.flush()

print(f"Score sent to Langfuse!")