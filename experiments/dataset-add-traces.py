# dataset-add-trace.py
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# Get the dataset
dataset = langfuse.get_dataset("customer-support-test")

# Get items in the dataset
items = dataset.items

if not items:
    print("No items found in dataset. Run add_items.py first.")
    exit(1)

# Use the first item
item = items[0]
print(f"Using dataset item: {item.id}")
print(f"Input: {item.input}")

# Create a trace and link to dataset item
response_output = "Visit /reset-password or contact support@company.com"

# Start the trace (root span) using start_as_current_observation
with langfuse.start_as_current_observation(
    name="support-query-trace",
    as_type="span",
    input=item.input,
    metadata={"dataset_item_id": item.id}
):
    # Add a generation (LLM call) to the trace
    # Use start_observation to get a LangfuseGeneration object
    gen = langfuse.start_observation(
        name="support_bot_response",
        as_type="generation",
        input=item.input,
        model="mock-model",
        metadata={"dataset_item_id": item.id}
    )
    # End the generation first
    gen.end()

    # Then update it with output using update_current_generation
    langfuse.update_current_generation(output=response_output)

    # Get trace ID
    trace_id = langfuse.get_current_trace_id()
    print(f"\nCreated trace: {trace_id}")

print(f"\nDataset item: {item.id}")
print(f"Trace ID: {trace_id}")

print("\nView in Langfuse dashboard:")
host = os.getenv('LANGFUSE_HOST', 'http://localhost:3001')
print(f"  - Trace: {host}/traces/{trace_id}")
print(f"  - Dataset: {host}/datasets/{dataset.id}")

langfuse.flush()