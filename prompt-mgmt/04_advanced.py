"""Lab 4: Advanced

Advanced Langfuse prompt features including custom metadata,
analytics, and complex configurations.
"""
import os
from dotenv import load_dotenv
from datetime import datetime
from uuid import uuid4
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
from typing import Dict, Any
import hmac
import hashlib

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_BASE_URL")

from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from langfuse.openai import openai

langfuse = Langfuse()

# Advanced Feature 1: Custom trace attributes
@observe()
def advanced_trace():
    # Set custom trace metadata
    langfuse_context.update_current_trace(
        name="advanced-pipeline",
        metadata={
            "environment": "production",
            "version": "2.1.0",
            "feature_flags": ["new_logic", "beta_ui"],
            "user_tier": "premium"
        },
        session_id="session-" + str(uuid4())[:8]
    )

    completion = openai.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[
            {"role": "system", "content": "You are a data analyst."},
            {"role": "user", "content": "Analyze this dataset: [1,2,3,4,5]"}
        ],
        temperature=0.7,
        metadata={
            "request_id": str(uuid4()),
            "processing_time_ms": random.randint(100, 500)
        }
    )

    return completion.choices[0].message.content

# Advanced Feature 2: Batch processing with traces
def process_batch(batch_id: str, items: list) -> list:
    """Process a batch with individual traces"""
    langfuse_context.update_current_trace(
        name=f"batch-{batch_id}",
        metadata={"batch_size": len(items), "started_at": datetime.utcnow().isoformat()}
    )

    results = []
    for i, item in enumerate(items):
        langfuse_context.update_current_observation(
            name=f"item-{i}",
            metadata={"item_id": item["id"], "item_data": item}
        )

        # Simulate processing
        time.sleep(0.1)
        results.append({"id": item["id"], "status": "processed"})

    return results

# Advanced Feature 3: Weighted random sampling for A/B
def select_model_variant(variant_a_weight: float = 0.5) -> str:
    """Select between model variants based on weight"""
    if random.random() < variant_a_weight:
        return "MiniMax-M2.5"
    return "gpt-3.5-turbo"

# Advanced Feature 4: Generation ID tracking
def track_generation_chain():
    """Track chained generations with parent-child relationships"""

    # First generation
    gen1 = langfuse.generations.create(
        name="chain-step-1",
        prompt="Explain AI in simple terms",
        completion="AI is like teaching computers to think...",
        model="MiniMax-M2.5",
        usage={"prompt_tokens": 10, "completion_tokens": 50}
    )

    # Second generation referencing the first
    langfuse.generations.create(
        name="chain-step-2",
        prompt="Now expand on that",
        completion=gen1.completion + " It can learn from data...",
        model="MiniMax-M2.5",
        parent_generation_id=gen1.id,
        usage={"prompt_tokens": 60, "completion_tokens": 80}
    )

    return "Chain tracked"

# Advanced Feature 5: Secure webhook signatures
def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """Verify webhook payload signature"""
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# Run demonstrations
print("=== Advanced Features Demo ===\n")

print("1. Custom Trace Attributes:")
result = advanced_trace()
print(f"   Result: {result[:50]}...\n")

print("2. Batch Processing:")
items = [{"id": f"item-{i}", "data": f"value-{i}"} for i in range(3)]
results = process_batch("batch-001", items)
print(f"   Processed: {len(results)} items\n")

print("3. Model Variant Selection:")
variant = select_model_variant(0.5)
print(f"   Selected variant: {variant}\n")

print("4. Generation Chain Tracking:")
track_generation_chain()
print("   Chain tracked successfully\n")

print("5. Webhook Signature Verification:")
test_payload = '{"event": "prompt.updated"}'
test_secret = "your-webhook-secret"
test_sig = hmac.new(test_secret.encode(), test_payload.encode(), hashlib.sha256).hexdigest()
is_valid = verify_webhook_signature(test_payload, test_sig, test_secret)
print(f"   Valid signature: {is_valid}")
