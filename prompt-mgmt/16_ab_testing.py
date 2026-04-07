"""Lab 16: A/B Testing
Learn how to run A/B tests on prompts in Langfuse to compare performance."""
import os
from dotenv import load_dotenv
load_dotenv()
import random

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_BASE_URL")

from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse()

class ABTester:
    def __init__(self, experiment_name: str, variants: dict):
        self.experiment_name = experiment_name
        self.variants = variants
        self.results = {name: {"count": 0, "scores": []} for name in variants}

    def get_variant(self, user_id: str = None):
        if user_id:
            idx = hash(user_id) % len(self.variants)
            variant_name = list(self.variants.keys())[idx]
        else:
            variant_name = random.choice(list(self.variants.keys()))
        return variant_name, self.variants[variant_name]

    def record_result(self, variant_name: str, score: float = None):
        self.results[variant_name]["count"] += 1
        if score is not None:
            self.results[variant_name]["scores"].append(score)

    def get_stats(self) -> dict:
        stats = {}
        total = sum(r["count"] for r in self.results.values())
        for name, data in self.results.items():
            scores = data["scores"]
            stats[name] = {
                "count": data["count"],
                "avg_score": sum(scores) / len(scores) if scores else None,
                "share": data["count"] / total if total > 0 else 0
            }
        return stats

experiment = ABTester(
    experiment_name="prompt-format-test",
    variants={
        "formal": "You are a professional technical writer. Write clear, formal documentation.",
        "casual": "You are a friendly tech buddy. Explain things in a casual, easy-going way."
    }
)

print("=== A/B Testing Demo ===\n")

test_users = [f"user_{i}" for i in range(10)]

for user_id in test_users:
    variant_name, prompt = experiment.get_variant(user_id)
    try:
        completion = openai.chat.completions.create(
            model="MiniMax-M2.5",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Explain what is an API"}
            ],
            temperature=0.7
        )
        simulated_score = random.uniform(0.6, 1.0)
        experiment.record_result(variant_name, simulated_score)
        print(f"User {user_id}: {variant_name} -> score: {simulated_score:.2f}")
    except Exception as e:
        print(f"User {user_id}: {variant_name} -> (error: {e})")

print("\n=== A/B Test Results ===")
stats = experiment.get_stats()
for variant, data in stats.items():
    print(f"\n{variant}:")
    print(f"  Users: {data['count']}")
    print(f"  Avg Score: {data['avg_score']:.2f}" if data['avg_score'] else "  Avg Score: N/A")
    print(f"  Share: {data['share']*100:.1f}%")

print("\n=== Langfuse A/B Testing ===")
print("1. Dashboard > Experiments")
print("2. Define prompt variants (A, B, C...)")
print("3. Set traffic allocation")
print("4. Track metrics: latency, cost, scores")
