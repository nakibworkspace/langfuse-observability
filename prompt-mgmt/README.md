# Langfuse Prompt Management Hands-On Lab

Hands-on labs covering key prompt management features in Langfuse.

## Files Created

| File | Topic |
|------|-------|
| `01_link_traces.py` | Link prompts to traces |
| `02_version_control.py` | Prompt versioning |
| `03_playground.py` | Using the Playground |
| `04_advanced.py` | Advanced features |
| `05_variables.py` | Prompt variables |
| `06_prompt_composability.py` | Composing prompts from components |
| `10_caching.py` | Prompt caching |
| `12_webhooks.py` | Webhook events |
| `16_ab_testing.py` | A/B testing prompts |

## Setup

1. Copy `.env.example` to `.env` and fill in credentials
2. Install: `pip install langfuse-python python-dotenv openai flask`

## Testing

```bash
python 01_link_traces.py
python 02_version_control.py
python 05_variables.py
python 10_caching.py
python 12_webhooks.py
python 16_ab_testing.py
```

Note: Some features require prompts to be created in the Langfuse UI first.
