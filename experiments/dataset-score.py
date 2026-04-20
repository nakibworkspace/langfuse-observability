# dataset-score.py
from langfuse import get_client, Evaluation
import os
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

# Get the dataset
dataset = langfuse.get_dataset("customer-support-test")

# Define your task function
def support_bot_task(*, item, **kwargs):
    query = item.input.get("query", "")

    # Mock response based on query
    responses = {
        "password": "Visit /reset-password or contact support@company.com",
        "order": "I apologize. Let me check your order status. Can you provide your order ID?",
        "refund": "We offer full refunds within 30 days of purchase.",
        "subscription": "You can cancel from account settings or I can transfer you to billing."
    }

    response = "Thank you for contacting support. How can I help you today?"
    for key, value in responses.items():
        if key in query.lower():
            response = value
            break

    return {"response": response}


# Define evaluator: exact match
def exact_match_evaluator(*, input, output, expected_output, **kwargs):
    if not expected_output:
        return Evaluation(name="exact_match", value=None, comment="No expected output")

    expected = expected_output.get("response", "") if isinstance(expected_output, dict) else str(expected_output)
    actual = output.get("response", "") if isinstance(output, dict) else str(output)

    score = 1.0 if expected.strip().lower() == actual.strip().lower() else 0.0
    return Evaluation(name="exact_match", value=score, comment=f"Expected: {expected} | Got: {actual}")


# Define evaluator: contains keywords
def contains_keyword_evaluator(*, input, output, **kwargs):
    query = input.get("query", "").lower()
    actual = output.get("response", "") if isinstance(output, dict) else str(output)

    keywords_map = {
        "password": ["reset", "reset-password", "support@"],
        "order": ["order", "order id", "check"],
        "refund": ["refund", "30 days", "purchase"],
        "subscription": ["cancel", "billing", "settings"]
    }

    for key, keywords in keywords_map.items():
        if key in query:
            matches = sum(1 for kw in keywords if kw in actual.lower())
            score = matches / len(keywords)
            return Evaluation(
                name="contains_keyword",
                value=score,
                comment=f"Found {matches}/{len(keywords)} keywords"
            )

    return Evaluation(name="contains_keyword", value=0.0, comment="No keywords to check")


# Define evaluator: response length
def response_length_evaluator(*, output, **kwargs):
    actual = output.get("response", "") if isinstance(output, dict) else str(output)
    length = len(actual.split())

    if 3 <= length <= 50:
        score = 1.0
    elif length < 3:
        score = 0.5
    else:
        score = 0.5

    return Evaluation(name="response_length", value=score, comment=f"Response has {length} words")


# Run the experiment with evaluators
result = dataset.run_experiment(
    name="support_bot_scoring_v1",
    description="Scoring run with multiple evaluators",
    task=support_bot_task,
    evaluators=[
        exact_match_evaluator,
        contains_keyword_evaluator,
        response_length_evaluator
    ],
    metadata={
        "model": "mock-model",
        "prompt_version": "v1.0",
        "evaluators_used": ["exact_match", "contains_keyword", "response_length"]
    }
)

print("EXPERIMENT RESULTS")

print(f"\nExperiment: {result.name}")
print(f"Total items: {len(result.item_results)}")

# Calculate average scores
for eval_name in ["exact_match", "contains_keyword", "response_length"]:
    scores = []
    for item in result.item_results:
        for eval_obj in item.evaluations:
            if eval_obj.name == eval_name and eval_obj.value is not None:
                scores.append(eval_obj.value)
                break
    if scores:
        avg = sum(scores) / len(scores)
        print(f"  {eval_name}: {avg:.2f} (avg)")

# Print per-item results
print("\n Per-Item Results")
for item_result in result.item_results:
    print(f"\nItem: {item_result.item.id}")
    print(f"  Input: {item_result.item.input}")
    print(f"  Output: {item_result.output}")
    for eval_obj in item_result.evaluations:
        print(f"    - {eval_obj.name}: {eval_obj.value} ({eval_obj.comment})")

print("\nView in Langfuse dashboard:")
if result.dataset_run_url:
    print(f"  {result.dataset_run_url}")

langfuse.flush()