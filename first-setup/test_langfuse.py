from langchain_community.chat_models import ChatOllama
from langfuse import Langfuse, observe

# Your Langfuse Cloud keys from https://cloud.langfuse.com/settings/keys
langfuse = Langfuse(
    public_key="pk-lf-b1298a69-98f5-49d9-96a3-f4d5c8cd3ad3",
    secret_key="sk-lf-810ef3d1-6cdc-45cf-bcf5-5b7b173758fb",
    host="https://us.cloud.langfuse.com"
)

llm = ChatOllama(model="llama3.2")

@observe(as_type="generation")
def call_llm(prompt):
    return llm.invoke(prompt)

print(call_llm("tell me a joke"))