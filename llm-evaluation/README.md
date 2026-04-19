# Hands-on Lab: LLM Evaluation Methods with Langfuse

## Introduction

This lab teaches the fundamentals of LLM evaluation using Langfuse, an open-source observability platform. You will learn three distinct evaluation methods: basic response tracking, LLM-as-a-judge scoring, and full evaluation pipelines with routing logic.

The lab takes a practical approach, using Python scripts to demonstrate real-world evaluation patterns that you can adapt for production systems.

**Prerequisites:** Basic Python knowledge, familiarity with REST APIs, and understanding of LLM concepts.

---

## Learning Objectives

By the end of this lab, you will be able to:

1. Initialize Langfuse SDK and track LLM interactions
2. Implement basic response scoring with rule-based evaluation
3. Build an LLM-as-a-judge system for automated quality assessment
4. Create evaluation pipelines with conditional routing logic
5. Visualize evaluation results in the Langfuse UI

---

## Prologue: The Challenge

You join a machine learning team at a product company. The team has deployed several LLM-powered features, but they lack visibility into response quality. Stakeholders report inconsistent outputs, and the team cannot identify which prompts or models perform best.

Your task is to implement an evaluation system that:

- Tracks every LLM response with full context
- Scores responses automatically using both rule-based and LLM-as-judge methods
- Routes low-quality responses for human review
- Provides a unified dashboard for quality monitoring

This lab teaches you the evaluation methods to solve this problem.

---

## Environment Setup

Ensure your system has Python 3.8 or later. This lab uses MiniMax as the LLM provider and Langfuse for observability.

### 1. Navigate to the project directory

```bash
cd llm-evaluation
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install langfuse openai python-dotenv
```

### 4. Verify environment configuration

The `.env` file contains the required credentials:

```bash
cat .env
```

Expected output:

```
OPENAI_API_KEY=sk-cp-...
OPENAI_BASE_URL=https://api.minimax.io/v1
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=http://localhost:3001
```

---

## Chapter 1: Basic LLM Response Tracking

The first evaluation method tracks LLM responses and applies simple rule-based scoring. This approach works well when you have clear acceptance criteria, such as mathematical answers or predefined outputs.

### 1.1 What You Will Build

You will create a script that:

- Calls an LLM with a test question
- Tracks the full interaction in Langfuse
- Scores the response using string matching
- Displays the evaluation result

### 1.2 Think First: Response Tracking

**Question:** Why is it important to track both the input and output of LLM calls?

<details>
<summary>Click to review</summary>

Tracking both input and output enables:
- Debugging: Understanding what prompted a specific response
- Analysis: Identifying patterns in model behavior
- Compliance: Maintaining audit trails for production systems
- Evaluation: Comparing responses against reference answers

</details>

### 1.3 Implementation

Create or examine `judge.py`:

```python
import os
from openai import OpenAI
from langfuse import get_client
from dotenv import load_dotenv

load_dotenv()

# Initialize Langfuse v4 client
langfuse = get_client()

# Initialize MiniMax client
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.minimax.io/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Start an observation (v4 uses observations-first model)
with langfuse.start_as_current_observation(
    as_type="generation",
    name="local-math-query",
    model="MiniMax-M2.5",
    input="What is 2 + 2?"
) as generation:
    # Call MiniMax model
    response = client.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "user", "content": "What is 2 + 2?"}],
        temperature=0.1
    )

    output_text = response.choices[0].message.content

    # Update the observation with output
    generation.update(output=output_text)

    # Score the observation
    generation.score(
        name="correctness",
        value=1.0 if "4" in output_text else 0.0,
        data_type="NUMERIC",
        comment="MiniMax model answered correctly"
    )

# Flush to ensure scores are sent
langfuse.flush()

print(f"Score sent to Langfuse!")
```

### 1.4 Understanding the Code

The script follows this flow:

| Step | Component | Purpose |
|------|-----------|---------|
| 1 | `get_client()` | Initialize Langfuse SDK using environment variables |
| 2 | `OpenAI()` | Create client configured for MiniMax API |
| 3 | `start_as_current_observation()` | Begin tracking an LLM call as a generation |
| 4 | `client.chat.completions.create()` | Call the LLM |
| 5 | `generation.update()` | Record the model's response |
| 6 | `generation.score()` | Attach an evaluation score |
| 7 | `langfuse.flush()` | Ensure all data is sent to Langfuse |

### 1.5 Test and Verify

**Predict:** What score will this script produce?

```bash
python judge.py
```

<details>
<summary>Click to verify</summary>

The script outputs: `Score sent to Langfuse!`

The score depends on whether the response contains "4". With the mathematical question "What is 2 + 2?", the MiniMax model typically responds with "4", so the score is 1.0.

</details>

### 1.6 Checkpoint

**Self-Assessment:**

- [ ] Script runs without errors
- [ ] Output displays "Score sent to Langfuse!"
- [ ] You can explain the role of `langfuse.flush()`
- [ ] You understand why we use `start_as_current_observation()`

---

## Chapter 2: LLM-as-a-Judge Scoring

Rule-based scoring works for simple cases, but many evaluation criteria require contextual judgment. LLM-as-a-judge uses a second LLM to evaluate responses, enabling complex quality assessment.

### 2.1 What You Will Build

You will build a system where:

- A primary LLM generates responses to questions
- A judge LLM evaluates those responses against reference answers
- Scores and reasoning are recorded in Langfuse

### 2.2 Think First: Judge LLMs

**Question:** Why use an LLM to evaluate another LLM rather than writing explicit rules?

<details>
<summary>Click to review</summary>

LLM-as-a-judge handles:
- Subjective quality dimensions (helpfulness, tone, clarity)
- Context-dependent criteria that vary by question
- Edge cases that are difficult to codify explicitly
- Scalability across diverse prompt types

The trade-off is consistency and cost—judge LLMs may vary in their evaluations and add latency.

</details>

### 2.3 Implementation

Examine `scoring.py`:

```python
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

# Judge prompt (keep it simple & strict)
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

# Judge function
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

# Main flow
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
```

### 2.4 Understanding the Code

The evaluation flow:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Query    │────>│  Primary LLM     │────>│  Candidate      │
│ "Capital of     │     │  MiniMax-M2.5    │     │  Response       │
│  France?"       │     │                  │     │  "Paris"        │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          v
                                              ┌─────────────────────┐
                                              │   Judge LLM         │
                                              │   (same model,      │
                                              │    temperature=0)   │
                                              └──────────┬──────────┘
                                                         │
                                                         v
                                              ┌─────────────────────┐
                                              │  Score + Reason     │
                                              │  {"score": 1.0,     │
                                              │   "reason": "..."}  │
                                              └──────────┬──────────┘
                                                         │
                                                         v
                                              ┌─────────────────────┐
                                              │  Langfuse           │
                                              │  - trace            │
                                              │  - score            │
                                              │  - metadata         │
                                              └─────────────────────┘
```

Key components:

| Component | Purpose |
|-----------|---------|
| `JUDGE_PROMPT` | Template that instructs the judge on evaluation criteria |
| `clean_judge_output()` | Parses JSON from LLM response, handling thinking tags |
| `run_judge()` | Invokes the judge LLM with temperature=0 for consistency |
| `obs.score()` | Records the evaluation with both numeric score and text comment |

### 2.5 Test and Verify

**Predict:** What will the judge score for "Paris is the capital of France"?

```bash
python scoring.py
```

<details>
<summary>Click to verify</summary>

Expected output: `Score: 1.0 | Correct answer`

The judge LLM recognizes "Paris" matches the reference and returns a score of 1.0 with an appropriate reason.

</details>

### 2.6 Checkpoint

**Self-Assessment:**

- [ ] Script runs and produces a score
- [ ] You can explain why `temperature=0.0` for the judge
- [ ] You understand the purpose of `clean_judge_output()`
- [ ] You can describe when to use LLM-as-a-judge vs rule-based scoring

---

## Chapter 3: Full Evaluation Pipeline with Routing

Production systems need more than scoring—they need action. This chapter combines generation, evaluation, and routing into a complete pipeline that tags low-quality responses for human review.

### 3.1 What You Will Build

You will create a pipeline that:

- Generates a response to a test question
- Uses LLM-as-a-judge to evaluate quality
- Applies routing logic based on scores
- Attaches metadata for filtering in Langfuse UI

### 3.2 Think First: Evaluation Routing

**Question:** Why would you route low-scoring responses to human review rather than simply discarding them?

<details>
<summary>Click to review</summary>

Routing to human review enables:

- **Error analysis**: Understanding why the system failed
- **Continuous improvement**: Creating training data from failures
- **Quality assurance**: Ensuring no harmful responses reach users
- **Graceful degradation**: Maintaining service while flagging issues

The routing decision is a business policy—not all low scores indicate failure; some may indicate edge cases requiring human judgment.

</details>

### 3.3 Implementation

Examine `annotate.py`:

```python
import re, json
import os
from langfuse import Langfuse
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
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group() if match else text

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

# Configuration
TEST_MODE = True  # Force routing for testing
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

    # Attach metadata for queue filtering
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
```

### 3.4 Understanding the Code

The pipeline architecture:

```
                    ┌─────────────────┐
                    │  Configuration  │
                    │  QUESTION,      │
                    │  REFERENCE,     │
                    │  TEST_MODE      │
                    └────────┬────────┘
                             │
                             v
              ┌──────────────────────────────┐
              │  Step 1: Generate Response   │
              │  Primary LLM: MiniMax-M2.5   │
              └──────────────┬───────────────┘
                             │
                             v
              ┌──────────────────────────────┐
              │  Step 2: Run Judge           │
              │  Judge LLM: MiniMax-M2.5     │
              │  temperature=0.0             │
              └──────────────┬───────────────┘
                             │
                             v
              ┌──────────────────────────────┐
              │  Step 3: Routing Logic       │
              │  if score < 0.7:             │
              │    tag = "low-score"         │
              │  if "error" in reason:       │
              │    tag = "judge-failed"      │
              └──────────────┬───────────────┘
                             │
                             v
              ┌──────────────────────────────┐
              │  Step 4: Record to Langfuse  │
              │  - generation trace          │
              │  - score (factuality_judge)  │
              │  - metadata (routing_tag)    │
              └──────────────────────────────┘
```

Routing logic details:

| Condition | Routing Tag | Needs Review |
|-----------|-------------|--------------|
| `TEST_MODE = True` | `low-score` | `true` |
| `score < 0.7` | `low-score` | `true` |
| `"error" or "parse" in reason` | `judge-failed` | `true` |
| Otherwise | `none` | `false` |

### 3.5 Test and Verify

**Predict:** What routing tag will be assigned when TEST_MODE=True?

```bash
python annotate.py
```

<details>
<summary>Click to verify</summary>

Expected output: `Done! Score: 1.0 | Routing: low-score`

Since `TEST_MODE = True`, all responses are routed to "low-score" regardless of the actual score. This allows testing the routing pipeline without needing intentionally bad responses.

</details>

### 3.6 Experiment: Disable Test Mode

1. Open `annotate.py`
2. Change `TEST_MODE = True` to `TEST_MODE = False`
3. Run the script again
4. Observe the routing tag

**Question:** What happens to the routing when the judge score is 1.0 and TEST_MODE=False?

<details>
<summary>Click to review</summary>

When `TEST_MODE=False` and the score is 1.0 (above 0.7 threshold), the routing tag becomes "none" and `needs_review` becomes False. The response passes quality checks and does not require human review.

</details>

### 3.7 Checkpoint

**Self-Assessment:**

- [ ] Script runs and displays score and routing
- [ ] You can explain the routing logic
- [ ] You understand when to use TEST_MODE
- [ ] You can describe how metadata enables filtering in Langfuse UI

---

## Viewing Results in Langfuse UI

After running each script, view the results in Langfuse.

### Access Langfuse

Open https://cloud.langfuse.com and log in with your account.

### Navigate to Traces

1. Click **Traces** in the sidebar
2. Find your trace by name:
   - `local-math-query` (from judge.py)
   - `candidate-answer` (from scoring.py, annotate.py)

### View Trace Details

For each trace, you can see:

| Field | Description |
|-------|-------------|
| Input | The prompt sent to the LLM |
| Output | The LLM's response |
| Scores | Evaluation scores (correctness, factuality, factuality_judge) |
| Metadata | Routing tags and flags (from annotate.py) |

### Filter by Routing Tag

To find traces needing review:

1. In the Traces view, click **Filters** or **Metadata**
2. Filter by:
   - `routing_tag = "low-score"` — responses scoring below threshold
   - `routing_tag = "judge-failed"` — responses where judge parsing failed

### View Scores Dashboard

1. Click **Scores** in the sidebar
2. See all recorded scores across traces
3. Click any score to jump to its associated trace

---

## Epilogue: The Complete System

You have implemented three evaluation methods that work together in a production system:

| Method | Script | Use Case |
|--------|--------|----------|
| Basic Tracking | `judge.py` | Debugging, simple correctness checks |
| LLM-as-a-Judge | `scoring.py` | Complex quality assessment |
| Full Pipeline | `annotate.py` | Production routing with metadata |

The three scripts demonstrate a progression from simple logging to intelligent routing. Each layer adds capability:

1. **Observation** — Capture every LLM interaction
2. **Evaluation** — Score responses automatically
3. **Action** — Route based on quality thresholds

Verify all three scripts work:

```bash
python judge.py
python scoring.py
python annotate.py
```

Each script should complete without errors and display confirmation messages.

---

## The Principles

1. **Always track inputs and outputs** — Without visibility, you cannot improve
2. **Choose evaluation method by complexity** — Rule-based for simple cases, LLM-as-judge for nuanced quality
3. **Separate scoring from routing** — Evaluate first, then decide what to do with results
4. **Include metadata for filtering** — Tags enable efficient review workflows
5. **Flush before exit** — Short scripts must call `langfuse.flush()` to ensure data is sent

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'langfuse'"

**Cause:** Virtual environment not activated or packages not installed.

**Solution:**

```bash
source venv/bin/activate
pip install langfuse openai python-dotenv
```

### Error: "Parse error" in score output

**Cause:** Judge LLM response was not valid JSON.

**Solution:** Check the `clean_judge_output()` function handles the model's specific output format. Some models wrap JSON in markdown code blocks or include thinking tags.

### No trace appearing in Langfuse

**Cause:** Script exited before data was sent.

**Solution:** Ensure `langfuse.flush()` is called at the end of the script.

### Auth errors (401/403)

**Cause:** Invalid API keys in `.env` file.

**Solution:** Verify all environment variables are set correctly:

```bash
echo $OPENAI_API_KEY
echo $LANGFUSE_PUBLIC_KEY
echo $LANGFUSE_SECRET_KEY
```

---

## Next Steps

Extend the evaluation system:

1. **Add more evaluation dimensions** — Helpfulness, toxicity, coherence
2. **Implement A/B testing** — Compare prompt templates by scoring each
3. **Create automated alerts** — Trigger notifications when scores drop
4. **Build a dataset** — Export scored traces for fine-tuning

---

## Additional Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse SDK Reference](https://langfuse.com/docs/sdk/python)
- [LLM Evaluation Concepts](https://langfuse.com/docs/evaluation/core-concepts)
- [MiniMax API Documentation](https://platform.minimaxi.com/document/Guide)