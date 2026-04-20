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