# Quick Guide: Running Prompt Management Labs

## Prerequisites

1. Start Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Ensure `.env` file has valid API keys (Langfuse and MiniMax)

---

## Running the Labs

### 01_link_traces.py
- **Purpose:** Link prompts to LLM traces for observability
- **Run:**
  ```bash
  python 01_link_traces.py
  ```
- **Expected:** Prints AI response, trace appears in Langfuse dashboard

### 02_version_control.py
- **Purpose:** Demonstrate prompt versioning and labels
- **Run:**
  ```bash
  python 02_version_control.py
  ```
- **Expected:** Prints AI response using version-controlled prompt

### 03_playground.py
- **Purpose:** Use Langfuse Playground for testing
- **Run:** No script - open http://localhost:3000 in browser
- **Note:** Use the UI to test prompts interactively

### 04_advanced.py
- **Purpose:** Advanced Langfuse features (functions, async)
- **Run:**
  ```bash
  python 04_advanced.py
  ```
- **Expected:** Demonstrates function calling or async patterns

### 05_variables.py
- **Purpose:** Create prompts with dynamic variables
- **Run:**
  ```bash
  python 05_variables.py
  ```
- **Expected:** Creates prompts with `{{variable}}` syntax in Langfuse

### 06_prompt_composability.py
- **Purpose:** Compose prompts from reusable components
- **Run:**
  ```bash
  python 06_prompt_composability.py
  ```
- **Expected:** Demonstrates prompt composition patterns

### 10_caching.py
- **Purpose:** Understand prompt caching behavior
- **Run:**
  ```bash
  python 10_caching.py
  ```
- **Expected:** Shows caching demo and Langfuse caching config info

### 12_webhooks.py
- **Purpose:** Set up webhooks for prompt change notifications
- **Run:**
  ```bash
  python 12_webhooks.py
  ```
- **Expected:** Starts webhook server on port 5000
- **Note:** Configure webhook URL in Langfuse UI to receive events

### 16_ab_testing.py
- **Purpose:** A/B test different prompt versions
- **Run:**
  ```bash
  python 16_ab_testing.py
  ```
- **Expected:** Randomly selects prompt variant, prints response with version info

### promt-creation.py
- **Purpose:** Create initial test prompt in Langfuse
- **Run:**
  ```bash
  python promt-creation.py
  ```
- **Expected:** Creates "my-prompt" in Langfuse with production label

---

## Testing Flow (Recommended Order)

1. Create prompts:
   ```bash
   python promt-creation.py
   python 05_variables.py
   ```

2. Test basic functionality:
   ```bash
   python 01_link_traces.py
   ```

3. Test advanced features:
   ```bash
   python 02_version_control.py
   python 16_ab_testing.py
   python 06_prompt_composability.py
   python 10_caching.py
   ```

4. For webhooks (requires additional setup):
   ```bash
   python 12_webhooks.py
   # Then update a prompt in UI to trigger webhook
   ```

---

## Checking Results

- **Langfuse Dashboard:** http://localhost:3000
  - View traces, prompts, and generations
- **Webhook Server:** http://localhost:5000/webhook
  - Run `12_webhooks.py` to start