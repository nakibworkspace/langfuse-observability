# Setting up Langfuse using in local machine with Ollama 

### prerequisites
* langchain-core and recent versions of langfuse generally require Python 3.9 or higher (with 3.10 or 3.11 being the "sweet spot" for ML stability right now).

## Installations

```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install langfuse langchain-core langchain-community
```

### Step 1: Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Pull a model
```bash
ollama pull llama3.2
```

### Step 3: Verify it's running
```bash
curl http://localhost:11434 -s
```

### Step 4: Run it
```bash
python3 test_langfuse.py
```

- Go to https://cloud.langfuse.com
- Look in the Traces tab