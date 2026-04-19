from langfuse import Langfuse
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

langfuse = Langfuse()

# Fetch as of a specific timestamp
version_ts = datetime(2026, 4, 19, 21, 28, 46, tzinfo=timezone.utc)
dataset = langfuse.get_dataset(
    name="customer-support-test",
    version=version_ts  # Optional: omit for latest
)

print(f"Items at version: {len(dataset.items)}")
for item in dataset.items:
    print(f"- {item.input}")

