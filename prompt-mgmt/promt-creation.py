"""Create the prompt needed for link-traces.py"""
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['LANGFUSE_PUBLIC_KEY'] = os.getenv('LANGFUSE_PUBLIC_KEY')
os.environ['LANGFUSE_SECRET_KEY'] = os.getenv('LANGFUSE_SECRET_KEY')
os.environ['LANGFUSE_BASE_URL'] = os.getenv('LANGFUSE_BASE_URL')

from langfuse import Langfuse

langfuse = Langfuse()

# Create the prompt with label
langfuse.create_prompt(
    name='my-prompt',
    prompt='You are a helpful assistant.',
    labels=['production']
)

print("Prompt 'my-prompt' created successfully!")
langfuse.flush()
