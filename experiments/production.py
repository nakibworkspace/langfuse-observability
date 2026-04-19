from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3001")
)

langfuse.create_dataset_item(
    dataset_name="customer-support-test",
    input={"query": "My order is late"},
    expected_output="I apologize. Let me check your order status. Can you provide your order ID?",
    source_trace_id="your-production-trace-id",  # Links back to original trace
    metadata={"source": "production", "flagged": True}
)