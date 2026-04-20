# Langfuse Experiments: Building and Evaluating LLM Applications

## Introduction

This lab teaches how to use Langfuse's experiment framework to systematically test and evaluate LLM applications. You will create datasets, run controlled experiments with scoring, and version your evaluation data for reproducible testing.

This lab takes a practical approach: you will build each component incrementally, running code after each concept is introduced to see results in the Langfuse UI.

**Prerequisites:** Basic Python knowledge, familiarity with REST API concepts, and understanding of LLM application fundamentals.

## Learning Objectives

By the end of this lab, you will be able to:

1. Create datasets and dataset items in Langfuse
2. Organize datasets using virtual folder structures
3. Define task functions that process dataset inputs
4. Run experiments to evaluate LLM application outputs
5. Implement evaluator functions for automatic scoring
6. Version datasets for reproducible experiments
7. Track experiment results and scores in the Langfuse UI

## Prologue: The Challenge

You join a team building a customer support chatbot. The bot handles various customer queries, but the team lacks a systematic way to:

- Test the bot against a consistent set of test cases
- Track performance across different model versions
- Reproduce experiments to compare prompt changes

Your task is to implement an experiment framework using Langfuse that enables the team to run repeatable evaluations, track scores over time, and identify when model changes improve or degrade performance.

## Environment Setup

Start the Langfuse local development environment using Docker:

```bash
cd /home/poridhian/code/langfuse-observability/experiments
docker compose up -d
```

Wait for all services to be healthy. Verify Langfuse is running:

```bash
curl http://localhost:3001/api/public/health
```

Expected output:

```json
{"status":"ok","service":"langfuse-web"}
```

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
pip install langfuse python-dotenv openai
```

Create a `.env` file with your Langfuse credentials:

```bash
# Get these from Langfuse UI at Settings > API Keys
LANGFUSE_PUBLIC_KEY=your_public_key_here
LANGFUSE_SECRET_KEY=your_secret_key_here
LANGFUSE_HOST=http://localhost:3001
```

Create a `langfuse_client.py` helper module for initializing the client:

```python
# langfuse_client.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

def get_langfuse_client():
    """Initialize and return Langfuse client."""
    return Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
    )
```

---

## Chapter 1: Creating Datasets

Datasets are the foundation of the experiment framework. A dataset contains multiple test cases (dataset items), each with an input and optionally an expected output for comparison.

### 1.1 Think First: Dataset Structure

Consider a customer support chatbot that needs testing. Each test case should contain:

- The customer's query (input)
- The expected response (expected_output)
- Metadata about the test case (category, difficulty, source)

**Question:** Why is it useful to include expected_output in a dataset?

<details>
<summary>Click to review</summary>

Expected outputs enable automated scoring. Without them, you can only manually review responses. With expected outputs, you can run evaluators that automatically calculate scores like exact match, similarity, or custom metrics.

</details>

### 1.2 Implementation

Create a dataset using the Langfuse SDK:

```python
# create_dataset.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# Create dataset with metadata
dataset = langfuse.create_dataset(
    name="customer-support-test",
    description="Test cases for support bot v1",
    metadata={
        "author": "Poridhi",
        "created_for": "langfuse-learning",
        "type": "benchmark",
        "version": "1.0"
    }
)

print(f"Created dataset: {dataset.name}")
print(f"Dataset ID: {dataset.id}")
```

Run the script:

```bash
python create_dataset.py
```

### 1.3 Understanding the Code

The `create_dataset` method accepts:
- `name`: Unique identifier for the dataset
- `description`: Human-readable description
- `metadata`: Additional key-value pairs for filtering or documentation

**Question:** What happens if you run the script twice with the same dataset name?

<details>
<summary>Click to review</summary>

Langfuse returns the existing dataset if the name already exists (idempotent operation). This is useful for maintaining the same dataset across multiple script runs.

</details>

### 1.4 Expected Output in Langfuse UI

After running the script, navigate to the Langfuse UI:

1. Open http://localhost:3001 in your browser
2. Go to **Datasets** in the left sidebar
3. You should see the `customer-support-test` dataset

![Dataset in UI](https://example.com/dataset-created.png)

> **Note:** Screenshot shows the dataset list after creation. The dataset appears with its metadata in the description column.

---

## Chapter 2: Adding Dataset Items

With a dataset created, you now add individual test cases. Each item represents one input-output pair to evaluate.

### 2.1 Think First: Item Structure

Each dataset item typically contains:

```json
{
  "input": {"query": "How do I reset my password?"},
  "expected_output": "Visit /reset-password or contact support@company.com",
  "metadata": {"category": "account", "difficulty": "easy"}
}
```

**Question:** What is the difference between input and expected_output?

<details>
<summary>Click to review</summary>

`input` is what you send to your LLM application (the prompt/query). `expected_output` is the correct answer you want to compare against. The evaluator uses expected_output to score the actual output from your application.

</details>

### 2.2 Implementation

Add items to your dataset:

```python
# add_items.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# Add multiple items
items = [
    {
        "input": {"query": "How do I reset my password?"},
        "expected_output": "Visit /reset-password or contact support@company.com",
        "metadata": {"category": "account", "difficulty": "easy", "source": "manual"}
    },
    {
        "input": {"query": "My order is late"},
        "expected_output": "I apologize. Let me check your order status. Can you provide your order ID?",
        "metadata": {"category": "shipping", "difficulty": "medium", "source": "production"}
    },
    {
        "input": {"query": "What is your refund policy?"},
        "expected_output": "We offer full refunds within 30 days of purchase. Please provide your order number.",
        "metadata": {"category": "billing", "difficulty": "easy", "source": "manual"}
    },
    {
        "input": {"query": "I want to cancel my subscription"},
        "expected_output": "You can cancel your subscription from the account settings page, or I can transfer you to our billing team.",
        "metadata": {"category": "account", "difficulty": "medium", "source": "production", "flagged": True}
    }
]

for item_data in items:
    item = langfuse.create_dataset_item(
        dataset_name="customer-support-test",
        input=item_data["input"],
        expected_output=item_data["expected_output"],
        metadata=item_data["metadata"]
    )
    print(f"Added item: {item.id}")

print(f"Total items added: {len(items)}")
```

Run the script:

```bash
python add_items.py
```

### 2.3 CSV Upload via UI

Alternatively, you can upload datasets via the Langfuse UI:

1. Navigate to **Datasets** in Langfuse
2. Click on your dataset `customer-support-test`
3. Click the **Upload** button (upper right)
4. Select a CSV file with columns: `input`, `expected_output`, `metadata` (as JSON)

Example CSV format:

```csv
input,expected_output,metadata
"How do I reset my password?","Visit /reset-password","{""category"": ""account"", ""difficulty"": ""easy""}"
"My order is late","Let me check your order status","{""category"": ""shipping"", ""difficulty"": ""medium""}"
```

### 2.4 Expected Output in Langfuse UI

After adding items, refresh the dataset view:

1. Click on the `customer-support-test` dataset
2. You should see 4 items in the table
3. Each row shows the input query, expected output, and metadata tags

![Dataset items](https://example.com/dataset-items.png)

> **Note:** The items table displays input/output columns. You can expand each row to see full metadata.

### 2.5 Checkpoint

**Self-Assessment:**
- [ ] Dataset appears in the Datasets list
- [ ] All 4 items are visible in the dataset detail view
- [ ] Metadata tags (category, difficulty) are displayed
- [ ] You can explain the difference between input and expected_output

---

## Chapter 3: Dataset Foldering and Organization

Langfuse supports virtual folder organization using slash notation in dataset names. This helps organize datasets by category, project, or version.

### 3.1 Think First: Folder Naming

When you create a dataset with a name containing slashes:

```python
langfuse.create_dataset(name="evaluation/qa/customer_support")
```

**Question:** What happens to this dataset name in the UI?

<details>
<summary>Click to review</summary>

The slash creates a virtual folder hierarchy. The dataset appears nested under `evaluation > qa` in the sidebar, with `customer_support` as the final dataset name.

</details>

### 3.2 Implementation

Create organizationally structured datasets:

```python
# foldering.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# Create datasets in different virtual folders
datasets_to_create = [
    {
        "name": "evaluation/qa/customer_support",
        "description": "QA tests for support bot"
    },
    {
        "name": "evaluation/qa/billing",
        "description": "QA tests for billing queries"
    },
    {
        "name": "production/monitored_queries",
        "description": "Real queries from production for ongoing monitoring"
    }
]

for ds in datasets_to_create:
    dataset = langfuse.create_dataset(
        name=ds["name"],
        description=ds["description"]
    )
    print(f"Created: {dataset.name}")

# List all datasets to see folder structure
all_datasets = langfuse.datasets.list()
print(f"\nTotal datasets: {len(all_datasets)}")
for ds in all_datasets:
    print(f"  - {ds.name}")
```

Run the script:

```bash
python foldering.py
```

### 3.3 Expected Output in Langfuse UI

Navigate to the Datasets view:

1. The sidebar now shows a folder hierarchy:
   - `evaluation/` (expandable)
     - `qa/`
       - `customer_support`
       - `billing`
   - `production/`
     - `monitored_queries`

2. Clicking folders expands/collapses them
3. Datasets are organized under their parent folders

### 3.4 Checkpoint

**Self-Assessment:**
- [ ] Folder hierarchy appears in the sidebar
- [ ] Folders can be expanded and collapsed
- [ ] You can explain the benefit of organizing datasets this way

---

## Chapter 4: Defining Task Functions

A task function is the LLM application logic you want to evaluate. It receives a dataset item as input and returns the model's output.

### 4.1 Think First: Task Function Interface

Consider this task function signature:

```python
def my_support_bot(*, item, **kwargs):
    # item.input contains the query
    # item.expected_output contains the correct answer
    # Return a dict with the model's response
    return {"response": "..."}
```

**Question:** Why does the function use `*` in the signature?

<details>
<summary>Click to review</summary>

The asterisk forces keyword-only arguments. This ensures the function is called with named parameters (`item=...`), which is how Langfuse invokes task functions. It also allows forward compatibility with additional kwargs.

</details>

### 4.2 Implementation

Create a task function file:

```python
# task.py
from langfuse import Langfuse

def my_support_bot(*, item, **kwargs):
    """
    Customer support bot task function.

    Args:
        item: DatasetItem with .input (dict), .expected_output (str), .metadata (dict)

    Returns:
        dict: The application's output (will be logged to trace)
    """
    query = item.input.get("query", "")

    # In production, this would be an actual LLM call
    # For now, we return a mock response
    responses = {
        "password": "Visit /reset-password or contact support@company.com",
        "order": "I apologize. Let me check your order status. Can you provide your order ID?",
        "refund": "We offer full refunds within 30 days of purchase.",
        "subscription": "You can cancel from account settings or I can transfer you to billing."
    }

    # Simple keyword matching for demonstration
    response = "Thank you for contacting support. How can I help you today?"
    for key, value in responses.items():
        if key in query.lower():
            response = value
            break

    return {"response": response}
```

### 4.3 Testing the Task Function

Create a test script to verify the task function works:

```python
# test_task.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv
from task import my_support_bot

load_dotenv()

# Get a dataset item to test with
langfuse = Langfuse()
dataset = langfuse.get_dataset("customer-support-test")

if dataset.items:
    test_item = dataset.items[0]
    print(f"Testing with input: {test_item.input}")

    result = my_support_bot(item=test_item)
    print(f"Output: {result}")

    if test_item.expected_output:
        print(f"Expected: {test_item.expected_output}")
else:
    print("No items in dataset")
```

Run the test:

```bash
python test_task.py
```

Expected output:

```
Testing with input: {'query': 'How do I reset my password?'}
Output: {'response': 'Visit /reset-password or contact support@company.com'}
Expected: Visit /reset-password or contact support@company.com
```

---

## Chapter 5: Running Experiments

An experiment runs your task function against all items in a dataset and optionally evaluates the outputs using evaluators.

### 5.1 Think First: Experiment vs. Traces

**Question:** How does running an experiment differ from making LLM calls directly?

<details>
<summary>Click to review</summary>

Experiments provide:
1. Automatic linking to the source dataset
2. Batch execution across all dataset items
3. Built-in evaluation scoring
4. Comparison across experiment runs
5. Version control for reproducibility

Traces are individual LLM interactions. Experiments are systematic evaluations across datasets.

</details>

### 5.2 Implementation

Create an experiment runner with evaluators:

```python
# run_experiment.py
from langfuse import get_client, Evaluation
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

# Import your task function
from task import my_support_bot

# Define an evaluator function
def exact_match_evaluator(*, input, output, expected_output, **kwargs):
    """
    Grades one item: 1.0 if output matches expected, else 0.0

    Args:
        input: The dataset item input
        output: The task function's output
        expected_output: The expected correct answer

    Returns:
        Evaluation: Score object with name, value, and comment
    """
    if not expected_output:
        return Evaluation(
            name="exact_match",
            value=None,
            comment="No expected output provided"
        )

    # Handle dict or string outputs
    expected = expected_output.get("response", "") if isinstance(expected_output, dict) else str(expected_output)
    actual = output.get("response", "") if isinstance(output, dict) else str(output)

    score = 1.0 if expected.strip().lower() == actual.strip().lower() else 0.0
    return Evaluation(
        name="exact_match",
        value=score,
        comment=f"Expected: {expected} | Got: {actual}"
    )

# Run the experiment
dataset = langfuse.get_dataset("customer-support-test")

result = dataset.run_experiment(
    name="support_bot_baseline_v1",
    description="First baseline run with exact match scoring",
    task=my_support_bot,
    evaluators=[exact_match_evaluator],
    metadata={"model": "mock", "prompt_version": "v1.0"}
)

# Print summary
print(result.format())

# Print per-item results
print("\n--- Per-Item Results ---")
for item_result in result.item_results:
    print(f"\nInput: {item_result.input}")
    print(f"Output: {item_result.output}")
    for eval in item_result.evaluations:
        print(f"  Score: {eval.name} = {eval.value}")

langfuse.flush()
```

Run the experiment:

```bash
python run_experiment.py
```

### 5.3 Expected Output in Langfuse UI

After running the experiment:

1. Go to **Experiments** in the sidebar
2. Click on `support_bot_baseline_v1`
3. View the experiment results showing:
   - Total items run
   - Average score
   - Per-item breakdown with inputs, outputs, and scores

![Experiment results](https://example.com/experiment-results.png)

> **Note:** The experiment detail view shows each item with its score. Items that match exactly show score 1.0, others show 0.0.

### 5.4 Checkpoint

**Self-Assessment:**
- [ ] Experiment appears in Experiments list
- [ ] All dataset items were processed
- [ ] Scores are visible per item
- [ ] You can explain how the evaluator function works

---

## Chapter 6: Dataset Versioning

Langfuse maintains a complete history of dataset changes. You can fetch datasets as they existed at any point in time, enabling reproducible experiments.

### 6.1 Think First: Version Control for Data

**Question:** Why is it important to be able to run experiments against a specific dataset version?

<details>
<summary>Click to review</summary>

Versioning ensures:
1. Reproducibility: Re-run the same experiment with the same data
2. Auditability: Know exactly what data was used for each experiment
3. Comparison: Compare model performance across different dataset versions
4. Rollback: Revert to previous dataset states if needed

This is essential for production systems where you need to prove results.

</details>

### 6.2 Implementation

Add more items to the dataset, then fetch a previous version:

```python
# add_production_items.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# Add more items to the dataset
production_items = [
    {
        "input": {"query": "How do I track my package?"},
        "expected_output": "You can track your package using the tracking link in your confirmation email.",
        "metadata": {"category": "shipping", "difficulty": "easy", "source": "production"}
    },
    {
        "input": {"query": "I was charged twice for my order"},
        "expected_output": "I apologize for the duplicate charge. Let me verify and process an immediate refund.",
        "metadata": {"category": "billing", "difficulty": "hard", "source": "production"}
    }
]

for item_data in production_items:
    langfuse.create_dataset_item(
        dataset_name="customer-support-test",
        input=item_data["input"],
        expected_output=item_data["expected_output"],
        metadata=item_data["metadata"]
    )
    print(f"Added: {item_data['input']['query']}")

print(f"\nTotal items now: {len(production_items) + 4}")
```

Run to add items:

```bash
python add_production_items.py
```

Now fetch the dataset at a previous point in time:

```python
# version_fetch.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

langfuse = Langfuse()

# Fetch the dataset at a specific timestamp
# Use a time just before you added the new items
version_ts = datetime(2026, 4, 20, 12, 0, 0, tzinfo=timezone.utc)

dataset_at_version = langfuse.get_dataset(
    name="customer-support-test",
    version=version_ts
)

print(f"Dataset name: {dataset_at_version.name}")
print(f"Items at this version: {len(dataset_at_version.items)}")
print("\nItems:")
for item in dataset_at_version.items:
    print(f"  - {item.input}")

# Compare with current version
current_dataset = langfuse.get_dataset(name="customer-support-test")
print(f"\n--- Comparison ---")
print(f"Items at version: {len(dataset_at_version.items)}")
print(f"Items now: {len(current_dataset.items)}")
```

Run the version fetch:

```bash
python version_fetch.py
```

### 6.3 Expected Output in Langfuse UI

In the Langfuse UI:

1. Go to **Datasets** > `customer-support-test`
2. Click the **History** tab
3. View the timeline of changes:
   - When dataset was created
   - When items were added
   - Each change with timestamp

![Dataset history](https://example.com/dataset-history.png)

> **Note:** The history view shows a complete audit trail of all changes to the dataset.

### 6.4 Checkpoint

**Self-Assessment:**
- [ ] You can fetch a dataset at a specific timestamp
- [ ] The versioned dataset contains only items that existed at that time
- [ ] You can explain why versioning is important for reproducibility

---

## Chapter 7: Versioned Experiments

Combine dataset versioning with experiments to run reproducible evaluations against historical dataset states.

### 7.1 Think First: Reproducible Evaluation

**Question:** What would happen if you ran the same experiment today without versioning, but then added more items to the dataset next week?

<details>
<summary>Click to review</summary>

Without versioning, the experiment would include new items, making it impossible to directly compare results. Versioned experiments ensure:
- Same data across all runs
- Fair comparison between model versions
- Reproducible benchmark results

</details>

### 7.2 Implementation

Run an experiment against a specific dataset version:

```python
# versioned_experiment.py
from langfuse import Langfuse, Evaluation
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from task import my_support_bot

load_dotenv()

langfuse = Langfuse()

# Define the evaluator
def exact_match_evaluator(*, input, output, expected_output, **kwargs):
    if not expected_output:
        return Evaluation(name="exact_match", value=None, comment="No expected output")

    expected = expected_output.get("response", "") if isinstance(expected_output, dict) else str(expected_output)
    actual = output.get("response", "") if isinstance(output, dict) else str(output)

    score = 1.0 if expected.strip().lower() == actual.strip().lower() else 0.0
    return Evaluation(name="exact_match", value=score, comment=f"Expected: {expected} | Got: {actual}")

# Get dataset at a specific version
version_ts = datetime(2026, 4, 20, 12, 0, 0, tzinfo=timezone.utc)
versioned_dataset = langfuse.get_dataset(
    name="customer-support-test",
    version=version_ts
)

print(f"Running experiment on dataset version: {version_ts}")
print(f"Number of items: {len(versioned_dataset.items)}")

# Run experiment on the versioned dataset
result = versioned_dataset.run_experiment(
    name="baseline_against_v1",
    description="Baseline run against original 4 items",
    task=my_support_bot,
    evaluators=[exact_match_evaluator],
    metadata={
        "dataset_version": version_ts.isoformat(),
        "prompt_version": "v1.0"
    }
)

print("\n--- Experiment Results ---")
print(result.format())

langfuse.flush()
```

Run the versioned experiment:

```bash
python versioned_experiment.py
```

### 7.3 Expected Output in Langfuse UI

In the Langfuse UI:

1. Go to **Experiments**
2. Find `baseline_against_v1`
3. Click to view details
4. Note the metadata shows the dataset version timestamp

The experiment was run against only the 4 original items, regardless of any items added afterward.

### 7.4 Checkpoint

**Self-Assessment:**
- [ ] Experiment runs against the versioned dataset
- [ ] Metadata includes the version timestamp
- [ ] You can explain the difference between versioned and non-versioned experiments

---

## Epilogue: The Complete System

Your experiment framework is now complete. Here is what was built:

| Component | Purpose | File |
|-----------|---------|------|
| Dataset | Container for test cases | `create_dataset.py` |
| Dataset Items | Individual test cases with input/expected output | `add_items.py` |
| Task Function | The LLM application to evaluate | `task.py` |
| Evaluator | Scoring logic for outputs | `run_experiment.py` |
| Experiment | Batch execution with scoring | `run_experiment.py` |
| Dataset Versioning | Point-in-time data snapshots | `version_fetch.py` |
| Versioned Experiment | Reproducible evaluation runs | `versioned_experiment.py` |

Verify the complete system:

```bash
# List all datasets
python -c "
from langfuse import Langfuse
from dotenv import load_dotenv
load_dotenv()
lf = Langfuse()
for ds in lf.datasets.list():
    print(f'{ds.name}: {len(lf.get_dataset(ds.name).items)} items')
"
```

---

## The Principles

1. **Always version your evaluation data** — Reproducibility is essential for reliable benchmarking
2. **Separate task from evaluation** — Keep your LLM application logic independent from scoring logic
3. **Use metadata strategically** — Tag items with category, difficulty, and source for filtered evaluations
4. **Run experiments on historical states** — Compare model improvements against the same baseline
5. **Track scores over time** — Use experiment metadata to correlate performance with changes

---

## Troubleshooting

### Error: "Dataset not found"

**Cause:** The dataset name does not exist or was created in a different project.

**Solution:**

```python
# Verify the dataset exists
langfuse = Langfuse()
all_datasets = langfuse.datasets.list()
for ds in all_datasets:
    print(ds.name)
```

### Error: "Authentication failed"

**Cause:** Invalid or expired API keys in the `.env` file.

**Solution:**

1. Go to Langfuse UI: Settings > API Keys
2. Generate new keys
3. Update the `.env` file

### Error: "Item has no attribute 'input'"

**Cause:** Passing wrong object type to task function.

**Solution:**

Ensure you pass the dataset item object directly:

```python
# Correct
result = my_support_bot(item=dataset.items[0])

# Wrong - passing a dict
result = my_support_bot(item=dataset.items[0].input)
```

### Experiment shows no scores

**Cause:** Evaluator function not returning proper Evaluation object.

**Solution:**

Verify your evaluator returns the correct structure:

```python
def my_evaluator(*, input, output, expected_output, **kwargs):
    return Evaluation(
        name="my_score",
        value=1.0,  # Must be a number
        comment="Optional explanation"
    )
```

---

## Next Steps

After completing this lab:

1. **Add more evaluators** — Implement ROUGE, BLEU, or LLM-as-a-judge evaluators
2. **Integrate real LLM calls** — Replace the mock task with actual OpenAI/Anthropic calls
3. **Create score configurations** — Use Langfuse's built-in score configs for standardized metrics
4. **Build a dashboard** — Visualize experiment results over time
5. **Add automated CI/CD** — Run experiments as part of your deployment pipeline

---

## Additional Resources

- [Langfuse Experiments Documentation](https://langfuse.com/docs/experiments)
- [Dataset Concepts](https://langfuse.com/docs/evaluation/core-concepts)
- [Python SDK Reference](https://python.reference.langfuse.com)
- [Evaluation Guide](https://langfuse.com/docs/evaluation)