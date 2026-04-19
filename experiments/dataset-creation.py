from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

# Create dataset
langfuse.create_dataset(
    name="customer-support-test",
    # optional description
    description="Test cases for support bot v1",
    # optional metadata
    metadata={
        "author": "Poridhi",
        "date": "2022-01-01",
        "created_for": "langfuse-learning",
        "type": "benchmark",
        "version": "1.0"
    }
)
