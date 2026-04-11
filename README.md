## Core Data Model (How Langfuse Structures Data)

| **Concept**    | **What it represents**                            | **Typical use**                                          |
| -------------- | ------------------------------------------------- | -------------------------------------------------------- |
| **Trace**      | One end-to-end user interaction or request        | A chat turn, an API call, a background job               |
| **Span**       | A logical step inside a trace                     | Data retrieval, tool call, preprocessing, postprocessing |
| **Generation** | A specific LLM call                               | `model=`, prompt, completion, tokens, cost, latency      |
| **Session**    | Groups multiple traces from the same user/context | Multi-turn conversations, user journeys                  |
| **Event**      | Lightweight metadata or logs                      | Debug info, fallback triggers, custom flags              |


## Core Functionalities
1. End-to-End Tracing & Debugging
Visualize the full execution path of an LLM app, including nested calls, RAG steps, agent tool use, and fallbacks.
Automatically captures inputs, outputs, latency, errors, and metadata.
Supports distributed/async systems (e.g., FastAPI + Celery, Next.js + edge functions).
2. Prompt Management & Versioning
Store, label, and version prompts in the UI.
Test prompts directly in Langfuse with sample inputs.
Reference prompts in code by name/version → no hardcoding, easy rollback, A/B testing ready.
3. Datasets & Evaluations
Create datasets of (input, expected_output) or (input, ground_truth) pairs.
Run automated evaluations using:
LLM-as-a-judge (built-in or custom)
Rule-based checks (regex, keyword match, JSON schema)
Custom Python/JS functions (via SDK or webhooks)
Track evaluation scores over time and across prompt/model versions.
4. Scoring & Custom Metrics
Attach human or automated scores to any trace/generation.
Common scores: quality, toxicity, relevance, latency_penalty, cost_efficiency.
Filter, sort, and export traces by score. Build dashboards for SLA monitoring.
5. Cost & Token Tracking
Automatically counts input/output tokens per model.
Estimates cost using provider pricing (OpenAI, Anthropic, Azure, local models, etc.).
Helps you catch runaway costs, compare model efficiency, and set budget alerts.
6. Collaboration & Production Readiness
Role-based access, team workspaces, and audit logs.
Comments & annotations on traces for cross-team debugging (eng, product, QA).
API-first design → export data, integrate with BI tools, or trigger CI/CD pipelines.