from langfuse import Langfuse
import os
from dotenv import load_dotenv
from task import my_support_bot

load_dotenv()

# Get a dataset item to test with
langfuse = Langfuse()
dataset = langfuse.get_dataset("customer-support-test")

if dataset.items:
    test_item = dataset.items[0]
    print(f"Testing with input: {test_item.input}")

    result = my_support_bot(item=test_item)
    print(f"Output: {result}")

    if test_item.expected_output:
        print(f"Expected: {test_item.expected_output}")
else:
    print("No items in dataset")