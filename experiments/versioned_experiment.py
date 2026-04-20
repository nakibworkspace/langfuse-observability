from langfuse import Langfuse
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from task import my_support_bot

load_dotenv()

langfuse = Langfuse()

version_ts = datetime(2026, 4, 20, 14, 52, 4, tzinfo=timezone.utc)
versioned_dataset = langfuse.get_dataset(
    name="customer-support-test",
    version=version_ts
)

result = versioned_dataset.run_experiment(
    name="baseline_against_v1",
    task=my_support_bot
)