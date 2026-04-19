from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# add_item.py
langfuse.create_dataset_item(
    dataset_name="customer-support-test",
    input={"query": "How do I reset my password?"},
    expected_output="Visit /reset-password or contact support@company.com",
    metadata={
        "category": "account",
        "difficulty": "easy",
        "source": "manual"
    }
)