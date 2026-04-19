from langfuse import Langfuse
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

langfuse = Langfuse()

# task.py - Your LLM application logic
def my_support_bot(*, item, **kwargs):
    """
    Args:
        item: DatasetItem with .input, .expected_output, .metadata
    Returns:
        dict: Your application's output (will be logged to trace)
    """
    # Replace with real LLM call
    query = item.input.get("query", "")
    return {
        "response": f"Thanks for asking about: {query}. Here's help: [mock answer]"
    }