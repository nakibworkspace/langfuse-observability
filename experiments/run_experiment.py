# run_experiment.py
from langfuse import get_client, Evaluation  # ← Import Evaluation
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

dataset = langfuse.get_dataset("customer-support-test")

# 1. Your task function (unchanged)
def my_support_bot(*, item, **kwargs):
    query = item.input.get("query", "")
    return {"response": f"Mock answer for: {query}"}

# 2. Define an evaluator function (item-level scoring)
def exact_match_evaluator(*, input, output, expected_output, **kwargs):
    """Grades one item: 1.0 if output matches expected, else 0.0"""
    if not expected_output:
        return Evaluation(name="exact_match", value=None, comment="No expected output")
    
    # Handle dict or string outputs
    expected = expected_output.get("response", "") if isinstance(expected_output, dict) else str(expected_output)
    actual = output.get("response", "") if isinstance(output, dict) else str(output)
    
    score = 1.0 if expected.strip().lower() == actual.strip().lower() else 0.0
    return Evaluation(name="exact_match", value=score, comment=f"Expected: {expected} | Got: {actual}")

# 3. Run experiment WITH evaluator
result = dataset.run_experiment(
    name="support_bot_baseline_v1",
    description="First baseline run with scoring",
    task=my_support_bot,
    evaluators=[exact_match_evaluator],  # ← Pass evaluator here
    metadata={"model": "minimax-m2.5", "prompt_version": "v1.0"}
)

# 4. Print results
print(result.format())

# Optional: See evaluator results per item
for item_result in result.item_results:
    for eval in item_result.evaluations:
        print(f"{eval.name}: {eval.value} — {eval.comment}")

langfuse.flush()