from langfuse import Langfuse

def my_support_bot(*, item, **kwargs):
    """
    Customer support bot task function.

    Args:
        item: DatasetItem with .input (dict), .expected_output (str), .metadata (dict)

    Returns:
        dict: The application's output (will be logged to trace)
    """
    query = item.input.get("query", "")

    # In production, this would be an actual LLM call
    # For now, we return a mock response
    responses = {
        "password": "Visit /reset-password or contact support@company.com",
        "order": "I apologize. Let me check your order status. Can you provide your order ID?",
        "refund": "We offer full refunds within 30 days of purchase.",
        "subscription": "You can cancel from account settings or I can transfer you to billing."
    }

    # Simple keyword matching for demonstration
    response = "Thank you for contacting support. How can I help you today?"
    for key, value in responses.items():
        if key in query.lower():
            response = value
            break

    return {"response": response}