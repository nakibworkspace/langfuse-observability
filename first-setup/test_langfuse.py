from langchain_community.chat_models import ChatOllama
from langfuse import Langfuse, observe

# Your Langfuse Cloud keys from https://cloud.langfuse.com/settings/keys
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://us.cloud.langfuse.com"
)

llm = ChatOllama(model="llama3.2")

@observe(as_type="generation")
def call_llm(prompt):
    return llm.invoke(prompt)

print(call_llm("tell me a joke"))