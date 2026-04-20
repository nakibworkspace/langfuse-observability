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