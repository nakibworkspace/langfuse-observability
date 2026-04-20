# Langfuse Experiments Lab — Architecture Diagrams

---

## Diagram 1: Lab Overview — What's Happening in This Lab

```mermaid
flowchart TD
    subgraph ENV["🐳 Environment Setup"]
        DC[Docker Compose\nLangfuse + Postgres + Redis]
        PY[Python venv\nlangfuse · openai · python-dotenv]
        ENV_FILE[.env\nPUBLIC_KEY · SECRET_KEY · HOST]
    end

    subgraph DATA["📦 Chapter 1–3: Build the Dataset"]
        DS[Create Dataset\ncustomer-support-test]
        ITEMS[Add Dataset Items\ninput + expected_output + metadata]
        FOLDERS[Organize with Folders\nevaluation/qa/customer_support\nproduction/monitored_queries]
        DS --> ITEMS --> FOLDERS
    end

    subgraph TASK["⚙️ Chapter 4: Define Task Function"]
        TF["task.py\nmy_support_bot(*, item, **kwargs)\n→ returns dict with response"]
        TEST[test-task.py\nManually verify output vs expected]
        TF --> TEST
    end

    subgraph EXPERIMENT["🧪 Chapter 5: Run Experiment"]
        EXP[run_experiment.py\ndataset.run_experiment()]
        EVAL[Evaluator Function\nexact_match_evaluator\n→ returns Evaluation score]
        RESULT[ExperimentResult\nper-item scores + summary]
        EXP --> EVAL --> RESULT
    end

    subgraph VERSION["🕐 Chapter 6–7: Versioning"]
        ADD[Add More Items\nproduction data]
        FETCH[version_fetch.py\nget_dataset at timestamp]
        VEXP[versioned_experiment.py\nrun on historical snapshot]
        ADD --> FETCH --> VEXP
    end

    subgraph UI["🖥️ Langfuse UI  localhost:3001"]
        UI_DS[Datasets View\nfolder tree + items table]
        UI_EXP[Experiments View\nscores · per-item breakdown]
        UI_HIST[Dataset History\naudit trail of changes]
    end

    ENV --> DATA
    DATA --> TASK
    TASK --> EXPERIMENT
    EXPERIMENT --> VERSION

    DATA -.->|visible in| UI_DS
    EXPERIMENT -.->|visible in| UI_EXP
    VERSION -.->|visible in| UI_HIST
```

---

## Diagram 2: How Experiments Work on Datasets — Behind the Scenes

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant SDK as Langfuse SDK
    participant Runner as Experiment Runner
    participant Task as Task Function<br/>(your LLM app)
    participant Eval as Evaluator Function
    participant LF as Langfuse Backend
    participant UI as Langfuse UI

    Dev->>SDK: get_dataset("customer-support-test", version=ts)
    SDK->>LF: GET /datasets/{name}?version=ts
    LF-->>SDK: Dataset + DatasetItems[]

    Dev->>SDK: dataset.run_experiment(name, task, evaluators)
    SDK->>LF: POST /dataset-runs  →  creates DatasetRun
    LF-->>SDK: DatasetRun { id, name }

    loop For each DatasetItem (concurrent)
        SDK->>Runner: dispatch item
        Runner->>Task: task(item=DatasetItem)
        Note over Task: item.input → LLM call<br/>returns output dict
        Task-->>Runner: output

        Runner->>LF: POST /traces  →  creates Trace<br/>links Trace to DatasetRunItem
        LF-->>Runner: Trace { traceId }

        Runner->>LF: POST /dataset-run-items<br/>{ datasetRunId, datasetItemId, traceId }

        Runner->>Eval: evaluator(input, output, expected_output)
        Note over Eval: compares output vs expected<br/>returns Evaluation(name, value, comment)
        Eval-->>Runner: Evaluation { name="exact_match", value=1.0 }

        Runner->>LF: POST /scores<br/>{ traceId, name, value, comment }
    end

    Runner->>SDK: aggregate all item results
    SDK-->>Dev: ExperimentResult.format()

    Dev->>UI: view Experiments tab
    UI->>LF: GET /dataset-runs/{id}/items
    LF-->>UI: items + traces + scores
    UI-->>Dev: per-item table with scores
```

---

## Data Model: Objects & Relationships

```mermaid
classDiagram
    direction LR

    class Dataset {
        +string name
        +string description
        +object metadata
    }

    class DatasetItem {
        +string id
        +object input
        +object expectedOutput
        +object metadata
        +string status  ACTIVE|ARCHIVED
        +string sourceTraceId
    }

    class DatasetRun {
        +string id
        +string name
        +string description
        +object metadata
    }

    class DatasetRunItem {
        +string id
        +string datasetRunId
        +string datasetItemId
        +string traceId
    }

    class Trace {
        +object input
        +object output
    }

    class Score {
        +string name
        +float value
        +string comment
    }

    Dataset "1" --> "n" DatasetItem : contains
    Dataset "1" --> "n" DatasetRun  : has runs
    DatasetRun "1" --> "n" DatasetRunItem : has items
    DatasetRunItem "1" --> "1" DatasetItem : references
    DatasetRunItem "1" --> "1" Trace : linked to
    Trace "1" --> "n" Score : scored by
```
