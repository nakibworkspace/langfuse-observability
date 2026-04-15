# Quick Guide: Testing Evaluation Scripts with Langfuse

## Overview

This directory contains three evaluation scripts:

| Script | Purpose |
|--------|---------|
| `judge.py` | Basic Langfuse tracking demo - generates a response and scores it |
| `annotate.py` | Full evaluation pipeline - generates answer, runs judge LLM to score, applies routing logic |
| `scoring.py` | Alias for judge.py (similar functionality) |

---

## Prerequisites

1. **Environment variables** (already configured in `.env`):
   - `OPENAI_API_KEY` - MiniMax API key
   - `OPENAI_BASE_URL` - MiniMax endpoint
   - `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` - Langfuse credentials
   - `LANGFUSE_BASE_URL` - Langfuse cloud URL

2. **Python dependencies**:
   ```bash
   pip install langfuse openai python-dotenv
   ```

---

## How to Run Each Script

### 1. Test `judge.py` (Basic Demo)

```bash
python judge.py
```

**What it does:**
- Starts a Langfuse observation
- Calls MiniMax-Text-01 with "What is 2 + 2?"
- Scores the response (1.0 if output contains "4", else 0.0)
- Flushes to Langfuse

**Expected output:**
```
Score sent to Langfuse!
```

---

### 2. Test `scoring.py`

```bash
python scoring.py
```

**Behavior:** Same as `judge.py` (duplicate functionality, uses MiniMax-Text-01).

---

### 3. Test `annotate.py` (Full Evaluation Pipeline)

```bash
python annotate.py
```

**What it does:**
- Generates an answer to "What is the capital of France?"
- Runs a judge LLM (MiniMax-M2.5) to score the response against reference "Paris"
- Applies routing logic (see below)
- Logs score + metadata to Langfuse

**Routing Logic:**
```python
if TEST_MODE:  # Currently True
    routing_tag = "low-score"
    needs_review = True
else:
    if score < 0.7:
        routing_tag = "low-score"
        needs_review = True
    if "error" in reason:
        routing_tag = "judge-failed"
        needs_review = True
```

**Expected output:**
```
Done! Score: 1.0 | Routing: low-score
```
(Note: Since `TEST_MODE = True`, all runs get routed to "low-score" for testing)

---

## What to Do in Langfuse UI

### Step 1: Access Langfuse
Open: https://cloud.langfuse.com

Log in with your account.

### Step 2: Navigate to Traces

1. From the sidebar, click **"Traces"**
2. You should see your trace(s) listed

### Step 3: View Trace Details

For **judge.py / scoring.py**:
- Click on the trace named `local-math-query`
- You'll see:
  - **Input**: "What is 2 + 2?"
  - **Output**: "4" (or similar)
  - **Score**: `correctness: 1.0` (or 0.0)

For **annotate.py**:
- Click on the trace named `candidate-answer`
- You'll see:
  - **Input**: "What is the capital of France?"
  - **Output**: The generated answer
  - **Score**: `factuality_judge: <score>` (e.g., 1.0)
  - **Metadata** (expand to see):
    - `routing_tag`: "low-score"
    - `needs_review`: true
    - `judge_score`: <score>

### Step 4: Filter by Routing Tag (Optional)

To find traces needing review in Langfuse:

1. In the Traces view, look for **"Filters"** or **"Metadata"** filter
2. Filter by:
   - `routing_tag = "low-score"` - responses that scored below threshold
   - `routing_tag = "judge-failed"` - responses where judge parsing failed

### Step 5: View Scores Dashboard

1. Click **"Scores"** in the sidebar
2. You'll see:
   - `correctness` score from judge.py/scoring.py
   - `factuality_judge` score from annotate.py
3. Click any score to see the associated trace and comment

---

## Testing Tips

1. **Run each script multiple times** to generate more data points
2. **Modify the QUESTION/REFERENCE** in `annotate.py` to test different scenarios
3. **Toggle TEST_MODE** in `annotate.py` to `False` to test real routing logic (scores < 0.7 trigger review)
4. **Check the comment field** - it contains the judge's reasoning

---

## Common Issues

| Issue | Solution |
|-------|----------|
| "Parse error" in score | Judge response wasn't valid JSON - check API response |
| No trace appearing | Run `langfuse.flush()` at end of script |
| Auth errors | Verify `.env` variables are set correctly |
