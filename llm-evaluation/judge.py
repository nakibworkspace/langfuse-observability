import re, json
import os
from langfuse import get_client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

langfuse = get_client()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.minimax.io/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. Judge prompt (keep it simple & strict)
JUDGE_PROMPT = """
Score the assistant's response based on the reference answer.
Question: {q}
Response: {r}
Reference: {ref}

Return ONLY JSON: {{"score": 0.0 to 1.0, "reason": "short explanation"}}
"""

def clean_judge_output(text):
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'```json\s*|\s*```', '', text)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group() if match else text

# 3. Judge function
def run_judge(question, response, reference):
    prompt = JUDGE_PROMPT.format(q=question, r=response, ref=reference)
    res = client.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,  # Deterministic judging
        max_tokens=400
    )
    raw = res.choices[0].message.content.strip()

    cleaned = clean_judge_output(raw)

    try:
        return json.loads(cleaned)
    except:
        return {"score": 0.5, "reason": "Parse error"}

# 4. Main flow
with langfuse.start_as_current_observation(
    as_type="generation",
    name="candidate-answer",
    model="MiniMax-M2.5",
    input="What is the capital of France?"
) as obs:
    # Generate answer
    out = client.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "user", "content": "What is the capital of France?"}],
        temperature=0.1
    )
    answer = out.choices[0].message.content
    obs.update(output=answer)

    # Judge it
    result = run_judge(
        question="What is the capital of France?",
        response=answer,
        reference="Paris"
    )

    # Score in Langfuse
    obs.score(
        name="factuality",
        value=result["score"],
        data_type="NUMERIC",
        comment=result["reason"]
    )

langfuse.flush()
print(f"Score: {result['score']} | {result['reason']}")
