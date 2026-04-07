"""Lab 10: Caching
Learn how to use Langfuse's caching features to reduce costs and improve latency."""
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_BASE_URL")

from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse()

# Cache implementation for prompt results
class PromptCache:
    def __init__(self, ttl_seconds=3600):
        self._cache = {}
        self._ttl = ttl_seconds

    def _make_key(self, prompt: str, **kwargs) -> str:
        import hashlib, json
        data = {"prompt": prompt, **kwargs}
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def get(self, prompt: str, **kwargs):
        key = self._make_key(prompt, **kwargs)
        entry = self._cache.get(key)
        if entry and entry["expires"] > time.time():
            entry["hits"] = entry.get("hits", 0) + 1
            return entry["value"]
        return None

    def set(self, prompt: str, value, **kwargs):
        import time
        key = self._make_key(prompt, **kwargs)
        self._cache[key] = {"value": value, "expires": time.time() + self._ttl, "hits": 0}

cache = PromptCache(ttl_seconds=3600)

print("=== Caching Demo ===\n")

# Test caching with repeated prompts
test_prompt = "What is Python?" * 3
test_kwargs = {"model": "MiniMax-M2.5", "temperature": 0}

# First call - cache miss
print("1. First call (cache miss):")
result1 = cache.get(test_prompt, **test_kwargs)
if not result1:
    completion = openai.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "user", "content": test_prompt}],
        temperature=0
    )
    result1 = completion.choices[0].message.content
    cache.set(test_prompt, result1, **test_kwargs)
    print(f"   Fetched from API: {result1[:50]}...")

# Second call - cache hit
print("\n2. Second call (cache hit):")
result2 = cache.get(test_prompt, **test_kwargs)
if result2:
    print(f"   From cache: {result2[:50]}...")

# Langfuse's built-in prompt caching
print("\n=== Langfuse Prompt Caching ===")
print("Langfuse supports server-side caching for:")
print("  - Frequently used prompts")
print("  - Common prompt templates")
print("  - System prompts that don't change")

# Cache configuration in Langfuse
print("\n=== Cache Configuration ===")
print("Configure caching via Langfuse dashboard:")
print("  1. Go to Settings > Caching")
print("  2. Enable prompt caching")
print("  3. Set cache TTL (time-to-live)")
print("  4. Monitor cache hit rates in Analytics")
