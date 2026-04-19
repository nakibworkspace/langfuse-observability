# annotate.py
import re, json
import os
from langfuse import Langfuse  # Standard v4 init
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize Langfuse v4.0.6
langfuse = Langfuse()

# Initialize MiniMax client
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.minimax.io/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

JUDGE_PROMPT = """
Score the assistant's response based on the reference answer.
Question: {q}
Response: {r}
Reference: {ref}

IMPORTANT: 
- Do NOT think out loud. Do NOT use <think> tags.
- Return ONLY valid JSON, nothing else.
- Format: {{"score": 0.0 to 1.0, "reason": "one short sentence"}}
- Example: {{"score": 1.0, "reason": "Correct answer"}}
"""

def clean_judge_output(text):
    """Remove <think>...</think> tags and extract JSON"""
    # Strip thinking blocks
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    
    # Try to find JSON object in remaining text
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    return text

def run_judge(question, response, reference):
    prompt = JUDGE_PROMPT.format(q=question, r=response, ref=reference)
    res = client.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=300
    )
    raw = res.choices[0].message.content.strip()

    cleaned = clean_judge_output(raw)

    try:
        return json.loads(cleaned)
    except Exception as e:
        return {"score": 0.5, "reason": f"Parse error: {str(e)[:50]}"}

# ============ CONFIG ============
TEST_MODE = False  # Force routing for testing
# ================================

QUESTION = "What is the capital of France?"
REFERENCE = "Paris"

# 1. Generate answer
candidate_response = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[{"role": "user", "content": QUESTION}],
    temperature=0.1
).choices[0].message.content

# 2. Run judge
judge_result = run_judge(QUESTION, candidate_response, REFERENCE)

# 3. Routing logic (decide BEFORE creating observation)
routing_tag = "none"
needs_review = False

if TEST_MODE:
    routing_tag = "low-score"
    needs_review = True
else:
    if judge_result["score"] < 0.7:
        routing_tag = "low-score"
        needs_review = True
    if "error" in judge_result["reason"].lower() or "parse" in judge_result["reason"].lower():
        routing_tag = "judge-failed"
        needs_review = True

# 4. Create observation + log metadata for queue routing
with langfuse.start_as_current_observation(
    as_type="generation",
    name="candidate-answer",
    model="MiniMax-M2.5",
    input=QUESTION
) as obs:
    
    obs.update(output=candidate_response)
    
    # Attach metadata for queue filtering (v4.0.6 compatible)
    obs.update(metadata={
        "routing_tag": routing_tag,
        "needs_review": needs_review,
        "judge_score": judge_result["score"]
    })
    
    # Attach judge score
    obs.score(
        name="factuality_judge",
        value=judge_result["score"],
        data_type="NUMERIC",
        comment=judge_result["reason"]
    )

langfuse.flush()

print(f"Done! Score: {judge_result['score']} | Routing: {routing_tag}")