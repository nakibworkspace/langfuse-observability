---
title: Overview
seoTitle: "Evaluation of LLM Applications"
description: With Langfuse you can capture all your LLM evaluations in one place. You can combine a variety of different evaluation metrics like model-based evaluations (LLM-as-a-Judge), human annotations or fully custom evaluation workflows via API/SDKs. This allows you to measure quality, tonality, factual accuracy, completeness, and other dimensions of your LLM application.
---

# Evaluation Overview

Evals give you a repeatable check of your LLM application's behavior. You **replace guesswork with data**.

They also help you **catch regressions before you ship a change**. You tweak a prompt to handle an edge case, run your eval, and immediately see if it affected the behavior of your application in unintended ways.

[**Watch this walkthrough**](/watch-demo?tab=evaluation) of Langfuse Evaluation and how to use it to improve your LLM application.

## Getting Started

If you're new to LLM evaluation, start by exploring the [Concepts](/docs/evaluation/core-concepts) page. There's a lot to uncover, and going through the concepts before diving in will speed up your learning curve.

Once you know what you want to do, you can:

- [Create a dataset](/docs/evaluation/experiments/datasets) to measure your LLM application's performance consistently
- [Run an experiment](/docs/evaluation/core-concepts#experiments) get an overview of how your application is doing
- [Set up a live evaluator](/docs/evaluation/evaluation-methods/llm-as-a-judge) to monitor your live traces

Looking for something specific? Take a look under _Evaluation Methods_ and _Experiments_ for guides on specific topics.

## GitHub Discussions

---
title: Concepts
description: Learn the fundamental concepts behind LLM evaluation in Langfuse - Scores, Evaluation Methods, Datasets, and Experiments.
---
# Core Concepts

This page digs into the different concepts of evaluations, and what's available in Langfuse. 

Ready to start? 

- [Create a dataset](/docs/evaluation/experiments/datasets) to measure your LLM application's performance consistently
- [Run an experiment](/docs/evaluation/core-concepts#experiments) to get an overview of how your application is doing
- [Set up LLM-as-a-Judge](/docs/evaluation/evaluation-methods/llm-as-a-judge) to evaluate your live traces

## The Evaluation Loop

LLM applications often have a constant loop of testing and monitoring. 

**Offline evaluation** lets you test your application against a fixed dataset before you deploy. You run your new prompt or model against test cases, review the [scores](#scores), iterate until the results look good, then deploy your changes. In Langfuse, you can do that by running [Experiments](/docs/evaluation/core-concepts#experiments).

**Online evaluation** scores live traces to catch issues in real traffic. When you find edge cases your dataset didn't cover, you add them back to your dataset so future experiments will catch them.

<Frame fullWidth>
  ![The Continuous Evaluation/Iteration Loop](/images/docs/evaluation/continuous-evaluation-loop.png)
</Frame>

> **Here's an example workflow** for building a customer support chatbot
> 1. You update your prompt to make responses less formal.
> 2. Before deploying, you run an **experiment**: test the new prompt against your dataset of customer questions **(offline evaluation)**.
> 3. You review the scores and outputs. The tone improved, but responses are longer and some miss important links.
> 4. You refine the prompt and run the experiment again.
> 5. The results look good now. You deploy the new prompt to production.
> 6. You monitor with **online evaluation** to catch any new edge cases.
> 7. You notice that a customer asked a question in French, but the bot responded in English.
> 8. You add this French query to your dataset so future experiments will catch this issue.
> 9. You update your prompt to support French responses and run another experiment.
> 
> Over time, your dataset grows from a couple of examples to a diverse, representative set of real-world test cases.

## Scores [#scores]

[Scores](/docs/evaluation/scores/overview) are Langfuse's universal data object for storing evaluation results. Any time you want to assign a quality judgment to an LLM output, whether by a human annotation, an LLM judge, a programmatic check, or end-user feedback, the result is stored as a score.

Scores can be attached to traces, observations, sessions, or dataset runs. Every score has a **name**, a **value**, and a **data type** (`NUMERIC`, `CATEGORICAL`, `BOOLEAN`, or `TEXT`). Learn more about [score types](/docs/evaluation/scores/overview#score-types), [how to create scores](/docs/evaluation/scores/overview#how-to-create-scores), and [score analytics](/docs/evaluation/scores/score-analytics) on the dedicated [Scores](/docs/evaluation/scores/overview) page.

## Evaluation Methods [#evaluation-methods]

Evaluation methods are the functions that score traces, observations, sessions, or dataset runs. You can use a variety of evaluation methods to add [scores](#scores).

| Method | What | Use when |
| --- | --- | --- |
| [LLM-as-a-Judge](/docs/evaluation/evaluation-methods/llm-as-a-judge) | Use an LLM to evaluate outputs based on custom criteria | Subjective assessments at scale (tone, accuracy, helpfulness) |
| [Scores via UI](/docs/evaluation/evaluation-methods/scores-via-ui) | Manually add scores to traces directly in the Langfuse UI | Quick quality spot checks, reviewing individual traces |
| [Annotation Queues](/docs/evaluation/evaluation-methods/annotation-queues) | Structured human review workflows with customizable queues | Building ground truth, systematic labeling, team collaboration |
| [Scores via API/SDK](/docs/evaluation/evaluation-methods/scores-via-sdk) | Programmatically add scores using the Langfuse API or SDK | Custom evaluation pipelines, deterministic checks, automated workflows |

When setting up new evaluation methods, you can use [Score Analytics](/docs/evaluation/scores/score-analytics) to analyze or sense-check the scores you produce.
## Experiments [#experiments]

An experiment runs your application against a dataset and evaluates the outputs. This is how you test changes before deploying to production.

### Definitions

Before diving into experiments, it's helpful to understand the building blocks in Langfuse: datasets, dataset items, tasks, scores, and experiments.

| Object | Definition |
| --- | --- |
| **Dataset** | A collection of test cases (dataset items). You can run experiments on a dataset. |
| **Dataset item** | One item in a dataset. Each dataset item contains an input (the scenario to test) and optionally an expected output. |
| **Task** | The application code that you want to test in an experiment. This will be performed on each dataset item, and you will score the output.
| **Evaluation Method** | A function that scores experiment results. In the context of a Langfuse experiment, this can be a [deterministic check](/docs/evaluation/evaluation-methods/custom-scores), or [LLM-as-a-Judge](/docs/evaluation/evaluation-methods/llm-as-a-judge). |
| **Score** | The output of an evaluation. See [Scores](#scores) for the available data types and details.|
| **Experiment Run** | A single execution of your task against all items in a dataset, producing outputs (and scores). |

You can find the data model for these objects [here](/docs/evaluation/experiments/data-model).

### How these work together

This is what happens conceptually:

When you run an experiment on a given **dataset**, each of the **dataset items** will be passed to the **task function** you defined. The task function is generally an LLM call that happens in your application, that you want to test. The task function produces an output for each dataset item. This process is called an **experiment run**. The resulting collection of outputs linked to the dataset items are the **experiment results**. 

Often, you want to score these experiment results. You can use various [evaluation methods](#evaluation-methods) that take in the dataset item and the output produced by the task function, and produce a score based on criteria you define. Based on these scores, you can then get a complete picture of how your application performs across all test cases.

<Frame fullWidth>
  ![Experiments flow](/images/docs/evaluation/experiments-flow.jpg)
</Frame>

You can compare experiment runs to see if a new prompt version improves scores, or identify specific inputs where your application struggles. Based on these experiment results, you can decide whether the change is ready to be deployed to production. 

You can find more details on how these objects link together under the hood on the [data model page](/docs/evaluation/experiments/data-model).

### Two ways to run experiments

You can **run experiments programmatically using the Langfuse SDK**. This gives you full control over the task, evaluation logic, and more. [Learn more about running experiments via SDK](/docs/evaluation/experiments/experiments-via-sdk).

Another way is to **run experiments directly from the Langfuse interface** by selecting a dataset and prompt version. This is useful for quick iterations on prompts without writing code. [Learn more about running experiments via UI](/docs/evaluation/experiments/experiments-via-ui).

<div className="my-6">
  <div className="grid grid-cols-3 gap-2">
    
    <div></div>
    <div className="text-center font-medium p-3 bg-gray-50 dark:bg-gray-800 rounded border dark:border-gray-700">
      **Langfuse Execution**
    </div>
    <div className="text-center font-medium p-3 bg-gray-50 dark:bg-gray-800 rounded border dark:border-gray-700">
      **Local/CI Execution**
    </div>

    
    <div className="font-medium p-3 bg-gray-50 dark:bg-gray-800 rounded border dark:border-gray-700 text-center">
      **Langfuse Dataset**
    </div>
    <div className="p-3 border dark:border-gray-700 rounded text-center bg-green-50 dark:bg-green-900/30">
      [Experiments via UI](/docs/evaluation/experiments/experiments-via-ui)
    </div>
    <div className="p-3 border dark:border-gray-700 rounded text-center bg-blue-50 dark:bg-blue-900/30">
      [Experiments via SDK](/docs/evaluation/experiments/experiments-via-sdk)
    </div>

    
    <div className="font-medium p-3 bg-gray-50 dark:bg-gray-800 rounded border dark:border-gray-700 text-center">
      **Local Dataset**
    </div>
    <div className="p-3 border dark:border-gray-700 rounded text-center bg-red-50 dark:bg-red-900/30">
      Not supported
    </div>
    <div className="p-3 border dark:border-gray-700 rounded text-center bg-blue-50 dark:bg-blue-900/30">
      [Experiments via SDK](/docs/evaluation/experiments/experiments-via-sdk)
    </div>

  </div>
</div>

*While it's optional, we recommend managing the underlying [Datasets](/docs/evaluation/experiments/datasets) in Langfuse as it allows for [1] In-UI comparison tables of different experiments on the same data and [2] Iteratively improve dataset based on production/staging traces.*

## Online Evaluation [#online-evaluation]

For online evaluation, you can configure evaluation methods to automatically score production traces. This helps you catch issues immediately.

Langfuse currently supports LLM-as-a-Judge and human annotation checks for online evaluation. [Deterministic checks are on the roadmap](https://github.com/orgs/langfuse/discussions/6087).

### Monitoring with dashboards

Langfuse offers dashboards to monitor your application performance in real-time. You can also monitor scores in dashboards. You can find more details on how to use dashboards [here](/docs/metrics/features/custom-dashboards).

---
title: Overview
description: Scores are Langfuse's universal data object for storing evaluation results. Learn about score types, how to create scores, and when to use them.
sidebarTitle: Overview
---

# Scores

Scores are Langfuse's universal data object for storing evaluation results. Any time you want to assign a quality judgment to an LLM output, whether by a [human annotation](/docs/evaluation/evaluation-methods/scores-via-ui), an [LLM judge](/docs/evaluation/evaluation-methods/llm-as-a-judge), a [programmatic check](/docs/evaluation/evaluation-methods/scores-via-sdk), or end-user feedback, the result is stored as a score.

Every score has a **name** (like `"correctness"` or `"helpfulness"`), a **value**, and a **[data type](#score-types)**. Scores also support an optional **[comment](#score-comments)** for additional context.

Scores can be attached to [traces](/docs/observability/data-model#traces), [observations](/docs/observability/data-model#observations), [sessions](/docs/observability/data-model#sessions), or [dataset runs](/docs/evaluation/experiments/data-model). Most commonly, scores are attached to traces to evaluate a single end-to-end interaction.

Once you have scores, they show up in [score analytics](/docs/evaluation/scores/score-analytics), can be visualized in [custom dashboards](/docs/metrics/features/custom-dashboards), and can be queried via the [API](/docs/api).

## When to Use Scores [#when-to-use-scores]

Scores become useful when you want to go beyond observing what your application does and start measuring how well it does it. Common use cases:

- **Collecting user feedback**: Capture thumbs up/down or star ratings from your users and attach them to traces. See the [user feedback guide](/docs/observability/features/user-feedback).
- **Monitoring production quality**: Set up automated evaluators (like [LLM-as-a-Judge](/docs/evaluation/evaluation-methods/llm-as-a-judge)) to continuously score live traces for things like hallucination, relevance, or tone.
- **Running guardrails**: Score whether outputs pass safety checks like PII detection, format validation, or content policy compliance.
- **Comparing changes with experiments**: When you change a prompt, model, or pipeline, run an [experiment](/docs/evaluation/experiments) to score the new version against a dataset.

## Score Types [#score-types]

Langfuse supports four score data types:

| Type | Value | Use when |
| --- | --- | --- |
| `NUMERIC` | Float (e.g. `0.9`) | Continuous judgments like accuracy, relevance, or similarity scores |
| `CATEGORICAL` | String from predefined categories (e.g. `"correct"`, `"partially correct"`) | Discrete classifications where the set of possible values is known upfront |
| `BOOLEAN` | `0` or `1` | Pass/fail checks like hallucination detection or format validation |
| `TEXT` | Free-form string (1-500 characters) | Open-ended annotations like reviewer notes or qualitative feedback. Often used for [open coding](https://en.wikipedia.org/wiki/Open_coding) before formalizing into quantifiable scores via [axial coding](https://en.wikipedia.org/wiki/Axial_coding). |

Text scores are designed for qualitative, open-ended scoring. Because free-form text cannot be meaningfully aggregated or compared, text scores are not supported in [experiments](/docs/evaluation/core-concepts#experiments), [LLM-as-a-Judge](/docs/evaluation/evaluation-methods/llm-as-a-judge), or [score analytics](/docs/evaluation/scores/score-analytics).

## How to Create Scores [#how-to-create-scores]

There are four ways to add scores:

- **LLM-as-a-Judge**: Set up [automated evaluators](/docs/evaluation/evaluation-methods/llm-as-a-judge) that score traces based on custom criteria (e.g. hallucination, tone, relevance). These can return numeric or categorical scores plus reasoning, and can run on live production traces or on experiment results.
- **Scores via UI**: Team members [manually score](/docs/evaluation/evaluation-methods/scores-via-ui) traces, observations, or sessions directly in the Langfuse UI. Requires a [score config](/faq/all/manage-score-configs) to be set up first.
- **Annotation Queues**: Set up [structured review workflows](/docs/evaluation/evaluation-methods/annotation-queues) where reviewers work through batches of traces.
- **Scores via API/SDK**: [Programmatically add scores](/docs/evaluation/evaluation-methods/scores-via-sdk) from your application code. This is the way to go for user feedback (thumbs up/down, star ratings), guardrail results, or custom evaluation pipelines.

## Should I Use Scores or Tags? [#scores-vs-tags]

| | Scores | Tags |
|---|---|---|
| **Purpose** | Measure _how good_ something is | Describe _what_ something is |
| **Data** | Numeric, categorical, boolean, or text value | Simple string label |
| **When added** | Can be added at any time, including long after the trace was created | Set during tracing and cannot be changed afterwards |
| **Used for** | Quality measurement, analytics, experiments | Filtering, segmentation, organizing |

As a rule of thumb: if you already know the category at tracing time (e.g. which feature or API endpoint triggered the trace), use a [tag](/docs/observability/features/tags). If you need to classify or evaluate traces later, use a score.

## Score Comments [#score-comments]

Every score supports an optional **comment** field. Use it to capture reasoning (e.g. why an LLM judge assigned a particular score), reviewer notes, or context that helps others understand the score value. Comments are shown alongside scores in the Langfuse UI.

Use a [`TEXT` score](#score-types) instead of comments to capture standalone qualitative feedback -- comments are best for additional reasoning on an existing score.

---
title: LLM-as-a-Judge
sidebarTitle: LLM-as-a-Judge
description: "Learn how LLM-as-a-Judge evaluation works — use large language models to automatically score, evaluate, and monitor your LLM application outputs at scale with rubric-guided assessments."
---

# LLM-as-a-Judge

LLM-as-a-Judge is an evaluation methodology where an LLM is used to assess the quality of outputs produced by another LLM application. Instead of relying solely on human reviewers or simple heuristic metrics, you prompt a capable model (the "judge") to score and reason about application outputs against defined criteria.

This approach has become one of the most popular methods for evaluating LLM applications because it combines the nuance of human judgment with the scalability of automated evaluation.

## How LLM-as-a-Judge Works

The core idea is straightforward: present an LLM with the input, the application's output, and a scoring rubric, then ask it to evaluate the output. The judge model produces a [`score`](/docs/evaluation/scores/overview) along with reasoning explaining its assessment.

A typical LLM-as-a-Judge prompt includes:
1. **Evaluation criteria** — a rubric defining what "good" looks like (e.g., "Score 1 if the answer is factually incorrect, 5 if fully accurate and well-sourced")
2. **Input context** — the original user query or prompt
3. **Output to evaluate** — the application's response
4. **Optional reference** — ground truth or expected output for comparison

The judge model then returns a structured score and reasoning that can be tracked, aggregated, and analyzed over time. In Langfuse, that score can be numeric, categorical, or boolean. Use numeric scores for continuous judgments like helpfulness from `0` to `1`. Use categorical scores when you want explicit labels such as `correct`, `partially_correct`, or `incorrect`. Use boolean scores for binary decisions where the outcome is `true` or `false`, such as whether a user is disagreeing with the assistant, whether a request is out-of-scope, or whether an answer violates policy. For more production-monitoring examples, see [LLM-as-a-Judge for Production Monitoring](/blog/2026-04-01-llm-as-a-judge-production-monitoring).

## Why use LLM-as-a-Judge?

- **Scalable:** Judge thousands of outputs quickly versus human annotators.
- **Human‑like:** Captures nuance (e.g. helpfulness, toxicity, relevance) better than simple metrics, especially when rubric‑guided.
- **Repeatable:** With a fixed rubric, you can rerun the same prompts to get consistent scores.

## How to use LLM-as-a-Judge?

LLM-as-a-Judge evaluators can run on three types of data: **Observations** (individual operations), **Traces** (complete workflows), or **Experiments** (controlled test datasets). Your choice depends on whether you're testing in development or monitoring production, and what level of granularity you need.

### Decision Tree

<div className="flex flex-col items-center gap-6 py-8 my-6">

<Card className="border-2 border-primary">
  <CardContent className="p-4 text-center font-semibold">
    Which data needs to be evaluated?
  </CardContent>
</Card>

<div className="text-2xl text-primary">↓</div>

<div className="flex flex-col md:flex-row gap-12 w-full justify-center">

<div className="flex flex-col items-center gap-4 flex-1 min-w-[280px]">
  <Card className="border-2 border-primary w-full">
    <CardHeader className="p-4">
      <CardTitle className="text-base text-center">Live Production Data</CardTitle>
      <CardDescription className="text-center text-xs">Monitor real-time traffic</CardDescription>
    </CardHeader>
  </Card>

  <div className="text-xl text-primary">↓</div>

  <div className="flex flex-col gap-3 w-full">
    <Card className="border-2 border-primary">
      <CardContent className="p-3">
        <div className="font-semibold text-sm">Observations <span className="text-xs font-normal opacity-70">(Recommended)</span></div>
        <div className="text-xs text-muted-foreground mt-1">Individual operations: LLM calls, retrievals, tool calls</div>
      </CardContent>
    </Card>

    <Card className="border">
      <CardContent className="p-3">
        <div className="font-semibold text-sm">Traces <span className="text-xs font-normal opacity-70">(Legacy)</span></div>
        <div className="text-xs text-muted-foreground mt-1">Complete workflow executions</div>
      </CardContent>
    </Card>
  </div>
</div>

<div className="flex flex-col items-center gap-4 flex-1 min-w-[280px]">
  <Card className="border-2 border-primary w-full">
    <CardHeader className="p-4">
      <CardTitle className="text-base text-center">Offline Experiment Data</CardTitle>
      <CardDescription className="text-center text-xs">Test in controlled environment</CardDescription>
    </CardHeader>
  </Card>

  <div className="text-xl text-primary">↓</div>

  <Card className="border-2 border-primary w-full">
    <CardContent className="p-3">
      <div className="font-semibold text-sm">Experiments</div>
      <div className="text-xs text-muted-foreground mt-1">Controlled test cases with datasets</div>
    </CardContent>
  </Card>
</div>

</div>

</div>

**Production Pattern**: Teams typically use **Experiments** during development to validate changes, then deploy **Observation-level** evaluators in production for scalable, precise monitoring.

### Understanding Each Evaluation Target

<Tabs items={["Live Production Data", "Offline Experiment Data"]}>
<Tab>

Evaluate live production traffic to monitor your LLM application performance in real-time.

<Tabs items={["Observations (Recommended)", "Traces (Legacy)"]}>
<Tab>

Run evaluators on individual observations within your traces—such as LLM calls, retrieval operations, embedding generations, or tool calls.

**Why target Observations**

- **Dramatically faster execution**: Evaluations complete in seconds, not minutes. Eliminates evaluation delays and backlogs. Asynchronous architecture processes thousands of evaluations per minute.
- **Operation-level precision**: Filter by observation type to evaluate only final LLM responses or retrieval steps, not entire workflows. Reduces evaluation volume and cost by targeting specific operations.
- **Compositional evaluation**: Run different evaluators on different operations within one trace. Toxicity on LLM outputs, relevance on retrievals, accuracy on generations—simultaneously.
- **Combined filtering**: Stack observation filters (type, name, metadata) with trace filters (userId, sessionId, tags, version). Example: "all LLM generations in conversations tagged 'customer-support' for premium users".

**Data Flow**

At ingest time, each observation is evaluated against your filter criteria. Matching observations are added to an evaluation queue. Evaluation jobs are then processed asynchronously. Scores are attached to the specific observation, resulting in one score per observation per evaluator. Depending on your filter criteria, multiple observations may match the criteria and result in multiple scores per trace.

**Example Use Cases**
- Evaluate helpfulness of only the final chatbot response to users
- Monitor toxicity scores on all customer-facing LLM generations
- Track retrieval relevance for RAG systems by targeting document retrieval observations

</Tab>

<Tab>

Run evaluators on complete traces, evaluating entire workflow executions from start to finish.

**Consider targeting Observations instead**: Observation-level evaluators complete in seconds (vs minutes for trace-level), eliminating evaluation delays. They also offer better precision for production monitoring. See [upgrade guide](/faq/all/llm-as-a-judge-migration).

**Why target Traces**

- Your evaluation requires full context spanning multiple operations
- You're on legacy SDK versions (Python v2 or JS/TS v3) and cannot upgrade

**Data Flow**

At ingest time, each trace is evaluated against your filter criteria. Matching traces are added to an evaluation queue and processed asynchronously. Scores are attached to the trace itself, resulting in one score per trace per evaluator.

**Example Use Cases**
- Score the accuracy of a multi-step agent workflow, if and only if evaluator needs full context spanning multiple operations (e.g., retrieval → reranking → generation → citation)

</Tab>
</Tabs>

</Tab>

<Tab>

Run evaluators on controlled test datasets to compare model versions, prompt variations, or system configurations in a reproducible environment.

**Why target Experiments**

- You need reproducible benchmarks for decision-making
- Comparing multiple prompt versions or model configurations
- You have datasets with expected outputs (ground truth)

**Data Flow**

Each experiment run generates traces that are automatically scored by your selected evaluators. Think of each experiment item as a test case: input → execution → output → evaluation.

1. Create a dataset with test inputs and (optionally) expected outputs. You may also define your test data locally.
2. Run experiment via UI or SDK—this executes your application code for each dataset item. See [Experiments via UI](/docs/evaluation/experiments/experiments-via-ui) or [Experiments via SDK](/docs/evaluation/experiments/experiments-via-sdk) for more information.
3. Selected evaluators to automatically score the generated outputs
4. Compare results across experiment runs to make data-driven decisions

**Example Use Case**

- Compare GPT-4 vs Claude Opus on 50 customer support questions, evaluate both for accuracy and helpfulness, then deploy the better-performing model

</Tab>
</Tabs>

## Set up step-by-step

<Steps>

### Create a new LLM-as-a-Judge evaluator

Navigate to the Evaluators page and click on the `+ Set up Evaluator` button.

<Frame fullWidth>![Evaluator create](/images/docs/evaluator-create.png)</Frame>

### Set the default model

Next, define the default model used for the evaluations. This step requires an LLM Connection to be set up. Please see [LLM Connections](/docs/administration/llm-connection) for more information.

  It's crucial that the chosen default model supports structured output. This is
  essential for our system to correctly interpret the evaluation results from
  the LLM judge.

### Pick an Evaluator

<Frame fullWidth>![Evaluator select](/images/docs/evaluator-select.png)</Frame>

Next, select an evaluator. There are two main ways:

<Tabs items={["Managed Evaluator", "Custom Evaluator"]}>
<Tab>

Langfuse ships a growing catalog of evaluators built and maintained by us and partners like **Ragas**. Each evaluator captures best-practice evaluation prompts for a specific quality dimension—e.g. _Hallucination_, _Context-Relevance_, _Toxicity_, _Helpfulness_.

- **Ready to use**: no prompt writing required.
- **Continuously expanded**: by adding OSS partner-maintained evaluators and more evaluator types in the future (e.g. regex-based).

</Tab>
<Tab>

When the library doesn't fit your specific needs, add your own:

1. Draft an evaluation prompt with `{{variables}}` placeholders (`input`, `output`, `ground_truth` ...).
2. Choose a **score type**: use **Numeric** for gradients like helpfulness or faithfulness, **Categorical** for discrete labels, or **Boolean** for `true` / `false` decisions such as `User Disagreement`, `Out-of-Scope Request`, or `Insufficient Answer`.
3. If you choose **Categorical**, define the allowed categories. Optionally enable **Allow multiple matches** if more than one label can apply. Langfuse will create one score per selected category. **Boolean** evaluators do not require a category list.
4. Optional: Customize the **score reasoning** prompt and the output prompt for your selected score type.
5. Optional: Pin a custom dedicated model for this evaluator. If no custom model is specified, it will use the default evaluation model (see Section 2).
6. Save → the evaluator can now be reused across your project.

</Tab>
</Tabs>

### Choose which Data to Evaluate

With your evaluator and model selected, configure which data to run the evaluations on. See the [Understanding Each Evaluation Target](#understanding-each-evaluation-target) section above to understand which option fits your use case.

<Tabs items={["Live Production Data", "Offline Experiment Data"]}>
<Tab>

<Tabs items={["Observations (Recommended)", "Traces (Legacy)"]}>
<Tab>

**Configuration Steps**

1. Select "Live Observations" as your evaluation target
2. Filter to specific observations using observation type, trace name, trace tags, userId, sessionId, metadata, and other attributes
3. Configure sampling percentage (e.g., 5%) to manage evaluation costs and throughput

**Requirements**

- **SDK version**: Python v3+ (OTel-based) or JS/TS v4+ (OTel-based)
  - [Python v2 → v3 migration guide](/docs/observability/sdk/upgrade-path/python-v2-to-v3)
  - [JS/TS v3 → v4 migration guide](/docs/observability/sdk/upgrade-path/js-v3-to-v4)
- **When filtering by trace attributes**: To filter observations by trace-level attributes (`userId`, `sessionId`, `version`, `tags`, `metadata`, `traceName`), use [`propagate_attributes()`](/docs/observability/sdk/instrumentation#add-attributes-to-observations) in your instrumentation code. Without this, trace attributes will not be available on observations. If you do set up trace-level attribute filtering and are not propagating attributes to observations, your observations will not be matched by the evaluator.

</Tab>

<Tab>

**Performance consideration**: We recommend using Observation-level evaluators for production monitoring. They complete in seconds (vs minutes for trace-level), eliminating evaluation delays and backlogs. They also offer better precision and cost efficiency. See [upgrade guide](/faq/all/llm-as-a-judge-migration).

**Configuration Steps**

1. Select "Live Traces" as your evaluation target
2. Filter traces by name, tags, userId, and other trace-level attributes
3. Choose whether to run on new traces only or include existing traces (backfilling)
4. Configure sampling percentage (e.g., 5%) to manage evaluation costs and throughput
5. Preview matched traces from the last 24 hours to validate your filter configuration

<Frame fullWidth>
  ![Production tracing data](/images/docs/evaluator-trace-filter.png)
</Frame>

**Requirements**

- **OTel-based SDKs**: If you're using Python v3+ or JS/TS v4+, trace input/output is derived from the root observation by default. To explicitly set trace input/output for these evaluators, use `set_trace_io()` (Python) or `setTraceIO()` (JS/TS). See the [Python v3 → v4](/docs/observability/sdk/upgrade-path/python-v3-to-v4) and [JS/TS v4 → v5](/docs/observability/sdk/upgrade-path/js-v4-to-v5) migration guides.

We recommend migrating to [observation-level evaluators](/faq/all/llm-as-a-judge-migration) instead of using `set_trace_io()` / `setTraceIO()`. Once migrated, you can remove these calls from your codebase entirely.

</Tab>
</Tabs>

</Tab>
<Tab>

**Configuration Steps**

- **[Experiments via UI](/docs/evaluation/experiments/experiments-via-ui)**: When running experiments through the UI, select which evaluators to run. These evaluators will automatically execute on the data generated by your next run.

- **[Experiments via SDK](/docs/evaluation/experiments/experiments-via-sdk)**: Configure evaluators directly in code using the experiment runner SDK.

**Requirements (for Experiments via SDK)**

- **Recommended**: Python >= 3.9.0 or JS/TS >= 4.4.0 with experiment runner functions ([`run_experiment()`](/docs/evaluation/experiments/experiments-via-sdk) / [`experiment.run()`](/docs/evaluation/experiments/experiments-via-sdk)). More performant architecture with built-in evaluator orchestration.
- **Legacy support**: Older SDK versions supported. Upgrade recommended for better performance.

</Tab>
</Tabs>

### Map Variables & preview Evaluation Prompt

You now need to teach Langfuse _which properties_ of your observation, trace, or experiment item represent the actual data to populate these variables for a sensible evaluation. For instance, you might map your system's logged observation input to the prompt's `{{input}}` variable, and the LLM response (observation output) to the prompt's `{{output}}` variable. This mapping is crucial for ensuring the evaluation is sensible and relevant.

<Tabs items={["Live Production Data", "Offline Experiment Data"]}>
<Tab>

- **Prompt Preview**: As you configure the mapping, Langfuse shows a **live preview of the evaluation prompt populated with actual data**. This preview uses historical data from the last 24 hours that matched your filters. You can navigate through several examples to see how their respective data fills the prompt, helping you build confidence that the mapping is correct.
- **JSONPath**: If the data is nested (e.g., within a JSON object), you can use a JSONPath expression (like `$.choices[0].message.content`) to precisely locate it.

<Frame fullWidth>![Filter preview](/images/docs/evaluator-mapping.png)</Frame>

</Tab>
<Tab>

- **Suggested mappings**: The system will often be able to autocomplete common mappings based on typical field names in experiments. For example, if you're evaluating for correctness, and your prompt includes `{{input}}`, `{{output}}`, and `{{ground_truth}}` variables, we would likely suggest mapping these to the experiment item's input, output, and expected_output respectively.
- **Edit mappings**: You can easily edit these suggestions if your experiment schema differs. You can map any properties of your experiment item (e.g., `input`, `expected_output`). Further, as experiments create traces under the hood, using the trace input/output as the evaluation input/output is a common pattern. Think of the trace output as your experiment run's output.

</Tab>
</Tabs>

### Trigger the evaluation

To see your evaluator in action, you need to either [send traces](/docs/observability/get-started) (fastest) or trigger an experiment run (takes longer to setup) via the [UI](/docs/evaluation/experiments/experiments-via-ui) or [SDK](/docs/evaluation/experiments/experiments-via-sdk). Make sure to set the correct target data in the evaluator settings according to how you want to trigger the evaluation.

</Steps>

✨ Done! You have successfully set up an evaluator which will run on your data.

  Need custom logic? Use the SDK instead—see [Custom
  Scores](/docs/evaluation/evaluation-methods/custom-scores) or an [external
  pipeline example](/docs/evaluation/evaluation-methods/scores-via-sdk).

## Debug LLM-as-a-Judge Executions

Every LLM-as-a-Judge evaluator execution creates a full trace, giving you complete visibility into the evaluation process. This allows you to debug prompt issues, inspect model responses, monitor token usage, and trace evaluation history.

You can show the LLM-as-a-Judge execution traces by filtering for the environment `langfuse-llm-as-a-judge` in the tracing table:

<Frame fullWidth>
  ![Tracing table filtered to langfuse-llm-as-a-judge
  environment](/images/docs/evaluation/llm-as-a-judge-debug-traces.png)
</Frame>

<details>
<summary>LLM-as-a-Judge Execution Status</summary>

- **Completed**: Evaluation finished successfully.
- **Error**: Evaluation failed (click execution trace ID for details).
- **Delayed**: Evaluation hit rate limits by the LLM provider and is being retried with exponential backoff.
- **Pending**: Evaluation is queued and waiting to run.

</details>

## Advanced Topics

### Migrating from Trace-Level to Observation-Level Evaluators

If you have existing evaluators running on traces and want to upgrade to running on observations for better performance and reliability, check out our comprehensive [Evaluator Migration Guide](/faq/all/llm-as-a-judge-migration).

### Troubleshooting Observation-Level Evaluators

If your observation-level evaluator isn't executing, see [Why is my observation-level evaluator not executing?](/faq/all/observation-eval-not-executing) for common causes and solutions.

### Backfill Historical Observation Scores

You can run observation-level LLM-as-a-Judge on historical data from the observations table. This is useful if you have already ingested production data and want to score matching observations retroactively with a new or updated evaluator.

**Prerequisite**: Enable the **[Fast Mode](/docs/v4)** toggle for the evaluator. To use the same evaluator on newly ingested data in real time, either upgrade to the latest SDKs (Python v4+ or JS/TS v5+) or, if you ingest directly via OTEL, set `x-langfuse-ingestion-version: 4` on your OTEL span exporter.

To backfill scores:

1. Open the **Traces** table.
2. Filter to the timeframe and trace criteria you want to backfill. Use the same criteria that your evaluator targets.
3. Select the matching rows.
4. Click **Actions** → **Evaluate**.
5. Follow the evaluation flow to run the evaluator on the selected traces and backfill scores for the matching observations.

<Frame fullWidth>
  ![Tracing table with filters applied before backfilling observation-level evaluations](/images/docs/llm-as-a-judge/observation-backfill.png)
</Frame>

This backfill flow runs from the traces table, but the resulting scores are attached to the matching observations inside each trace.

## FAQ

<details>
<summary>What is LLM-as-a-Judge evaluation?</summary>

LLM-as-a-Judge is an evaluation methodology where a large language model (the "judge") assesses the quality of outputs from another LLM application. The judge model is given the input, the application's output, and a scoring rubric, then produces a score with reasoning. It's one of the most popular approaches for evaluating LLM applications because it combines human-like nuance with automated scalability.

</details>

<details>
<summary>How accurate is LLM-as-a-Judge compared to human evaluation?</summary>

Research shows that strong LLM judges (such as GPT-5 class models) achieve 80-90% agreement with human evaluators on many quality dimensions, which is comparable to inter-annotator agreement between humans. Accuracy improves significantly with well-designed rubrics and clear evaluation criteria. For best results, calibrate your LLM-as-a-Judge setup against a small set of human-annotated examples.

</details>

<details>
<summary>What models work best as LLM judges?</summary>

The most capable models generally produce the best evaluations. Models with strong instruction-following and reasoning capabilities (such as GPT-4o, Claude Sonnet, or Gemini Pro) are commonly used. The judge model should support structured output so scores can be reliably parsed. In Langfuse, you configure the judge model via [LLM Connections](/docs/administration/llm-connection).

</details>

<details>
<summary>How much does LLM-as-a-Judge cost?</summary>

Cost depends on the judge model and the size of the inputs being evaluated. A typical evaluation costs $0.01-0.10 per assessment. You can manage costs by: (1) using sampling to evaluate a percentage of traces, (2) targeting specific observations instead of full traces, and (3) choosing cost-effective judge models for simpler evaluations.

</details>

<details>
<summary>Can I use LLM-as-a-Judge for RAG evaluation?</summary>

Yes. LLM-as-a-Judge is particularly effective for RAG pipelines. You can evaluate faithfulness (is the answer grounded in the retrieved context?), relevance (does the answer address the question?), and completeness (does the answer cover all relevant information?). Langfuse also integrates with [RAGAS](/guides/cookbook/evaluation_of_rag_with_ragas) for specialized RAG evaluation metrics.

</details>

## GitHub Discussions

---
title: Annotation Queues
description: Manage your annotation tasks with ease using our new workflow tooling. Create queues, add traces to them, and get a simple UI to review and label LLM application traces in Langfuse.
---

# Annotation Queues [#annotation-queues]

Annotation Queues are a manual [evaluation method](/docs/evaluation/core-concepts#evaluation-methods) which is build for domain experts to add [scores](/docs/evaluation/scores/overview) and comments to traces, observations or sessions.

## Why use Annotation Queues?

- Manually explore application results and add scores and comments to them
- Allow domain experts to add scores and comments to a subset of traces
- Add [corrected outputs](/docs/observability/features/corrections) to capture what the model should have generated
- Align your LLM-as-a-Judge evaluation with human annotation

## Set up step-by-step

<Steps>

### Create a new Annotation Queue

- Click on `New Queue` to create a new queue.
- Select the [`Score Configs`](/docs/evaluation/scores/data-model#score-config) you want to use for this queue.
- Set the `Queue name` and `Description` (optional).
- Assign users to the queue (optional).

An Annotation Queue requires a score config that defines the scoring dimensions for the annotation tasks. See [how to create and manage Score Configs](/faq/all/manage-score-configs#create-a-score-config) for details.

### Add Traces, Observations or Sessions to the Queue

Once you have created annotation queues, you can assign traces, observations or sessions to them.

<Tabs items={["Bulk Selection", "Single Item"]}>
<Tab>
To add multiple traces, sessions or observations to a queue:

1. Select Traces, Observations or Sessions via the checkboxes. 
2. Click on the "Actions" dropdown menu
3. Click on `Add to queue` to add the selected traces, sessions or observations to the queue.
4. Select the queue you want to add the traces, sessions or observations to.

<Frame fullWidth>
  ![Annotate](/images/docs/add_multiple_items_to_queue.png)
</Frame>

</Tab>
<Tab>

To add single traces, sessions or observations:

1. Click on the `Annotate` dropdown
2. Select the queue you want to add the trace, session or observation to

<Frame fullWidth>![Annotate](/images/docs/add_to_queue.png)</Frame>

</Tab>
</Tabs>

### Process Annotation Queue

You will see an annotation task for each item in the queue.

1. On the `Annotate` Card add scores on the defined dimensions
2. Click on `Complete + next` to move to the next annotation task or finish the queue

</Steps>

## Manage Annotation Queues via API

You can manage annotation queues via the [API](https://api.reference.langfuse.com/#tag/annotationqueues/GET/api/public/annotation-queues). This allows for scaling and automating your annotation workflows or using Langfuse as the backbone for a [custom vibe coded annotation tool](/blog/2025-11-25-vibe-coding-custom-annotation-ui).

---
title: Scores via UI
description: Annotate traces and observations with scores in the Langfuse UI to record human-in-the-loop evaluations.
sidebarTitle: Scores via UI
---

# Manual Scores via UI

Adding [scores](/docs/evaluation/scores/overview) via the UI is a manual [evaluation method](/docs/evaluation/core-concepts#evaluation-methods). It is used to collaboratively annotate traces, sessions and observations with evaluation scores.

You can also use [Annotation Queues](docs/evaluation/evaluation-methods/annotation-queues) to streamline working through reviewing larger batches of of traces, sessions and observations.

## Why manually adding scores via UI?

- Allow multiple team members to manually review data and improve accuracy through diverse expertise.
- Standardized score configurations and criteria ensure consistent data labeling across different workflows and scoring types.
- Human baselines provide a reference point for benchmarking other scores and curating high-quality datasets from production logs.

## Set up step-by-step

<Steps>
### Create a Score Config

To add scores in the UI, you need to have at least one Score Config set up. See [how to create and manage Score Configs](/faq/all/manage-score-configs) for details.

### Add Scores

On a Trace, Session or Observation detail view click on `Annotate` to open the annotation form.

<Frame fullWidth>![Annotate](/images/docs/trigger_annotation.png)</Frame>

### Select Score Configs to use

<Frame fullWidth>![Annotate](/images/docs/select_score_configs.png)</Frame>

### Set Score values

<Frame fullWidth>![Annotate](/images/docs/set_score_values.png)</Frame>

### Add score comment (Optional)
<Frame fullWidth>![Annotate](/images/docs/scores_comment.png)</Frame>

### See the Scores
To see your newly added scores on traces or observations, **click on** the `Scores` tab on the trace or observation detail view.

<Frame fullWidth>
  ![Detail scores table](/images/docs/see_created_scores.png)
</Frame>

</Steps>

## Add scores to experiments

When running [experiments via UI](/docs/evaluation/experiments/experiments-via-ui) or via [SDK](/docs/evaluation/experiments/experiments-via-sdk), you can annotate results directly from the experiment compare view. 

**Prerequisites:**
- Set up [score configurations](/faq/all/manage-score-configs) for the dimensions you want to evaluate
- Execute an [experiment via UI](/docs/evaluation/experiments/experiments-via-ui) or [SDK](/docs/evaluation/experiments/experiments-via-sdk) to generate results to review

<Frame fullWidth>
  ![Annotate from compare view](/images/changelog/2025-10-23-annotate-compare-view-overview.png)
</Frame>

The compare view maintains full experiment context: Inputs, outputs, and automated scores, while you review each item. Summary metrics update as you add annotation scores, allowing you to track progress across the experiment.

## GitHub Discussions

---
title: Scores via API/SDK
description: Ingest custom scores via the Langfuse SDKs or API.
sidebarTitle: Scores via API/SDK
---

# Scores via API/SDK

You can use the Langfuse SDKs or API to add [scores](/docs/evaluation/scores/overview) to traces, observations, sessions and dataset runs. This is an evaluation method that allows to set up custom evaluation workflows and extend the scoring capabilities of Langfuse. See the [data model](/docs/evaluation/scores/data-model#scores) for full details on the score object.

## Common Use Cases

- **Collecting user feedback**: collect in-app feedback from your users on application quality or performance. Can be captured in the frontend via our Browser SDK.
  -> [Example Notebook](/guides/cookbook/user-feedback)

- **Custom evaluation data pipeline**: continuously monitor the quality by fetching traces from Langfuse, running custom evaluations, and ingesting scores back into Langfuse.
  -> [Example Notebook](/guides/cookbook/example_external_evaluation_pipelines)

- **Guardrails and security checks**: check if output contains a certain keyword, adheres to a specified structure/format or if the output is longer than a certain length.
  -> [Example Notebook](/guides/cookbook/security-and-guardrails)

- **Custom internal workflow tooling**: build custom internal tooling that helps you manage human-in-the-loop workflows. Ingest scores back into Langfuse, optionally following your custom schema by referencing a config.
- **Custom run-time evaluations**: e.g. track whether the generated SQL code actually worked, or if the structured output was valid JSON.
- **Session-level quality tracking**: score full conversations (for example, support chats or agent threads) by attaching scores via `sessionId` in the SDK/API.

## Ingesting Scores via API/SDKs

Scores can be attached at different levels of granularity: to individual traces, to specific observations within a trace, or to full sessions.

See the [API reference](/docs/api) for full details on the POST and GET endpoints for scores and score configs.

### Trace or Observation-level Scores

You can add scores via the Langfuse SDKs or API. Scores can take one of four data types: **Numeric**, **Categorical**, **Boolean**, or **Text**. See [Score Types](/docs/evaluation/scores/overview#score-types) for details.

If a score is ingested manually using a `trace_id` to link the score to a trace, it is not necessary to wait until the trace has been created. The score will show up in the scores table and will be linked to the trace once the trace with the same `trace_id` is created.

Here are examples by `Score` data types.

For trace and observation scores, `trace_id`/`traceId` is required and `observation_id`/`observationId` is optional. If you attach a score to an observation, always provide both the observation ID and the corresponding trace ID.

<LangTabs items={["Python SDK", "JS/TS SDK", "API"]}>
<Tab>

<Tabs items={["Numeric", "Categorical", "Boolean", "Text"]}>
<Tab>
Numeric score values must be provided as float.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    name="correctness",
    value=0.9,
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    data_type="NUMERIC", # optional, inferred if not provided
    comment="Factually correct", # optional
)

# Method 2: Score current span/generation (within context)
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    # Score the current span
    span.score(
        name="correctness",
        value=0.9,
        data_type="NUMERIC",
        comment="Factually correct"
    )

    # Score the trace
    span.score_trace(
        name="overall_quality",
        value=0.95,
        data_type="NUMERIC"
    )


# Method 3: Score via the current context
with langfuse.start_as_current_observation(as_type="span", name="my-operation"):
    # Score the current span
    langfuse.score_current_span(
        name="correctness",
        value=0.9,
        data_type="NUMERIC",
        comment="Factually correct"
    )

    # Score the trace
    langfuse.score_current_trace(
        name="overall_quality",
        value=0.95,
        data_type="NUMERIC"
    )
```

</Tab>
<Tab>
Categorical score values must be provided as strings.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    name="accuracy",
    value="partially correct",
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    data_type="CATEGORICAL", # optional, inferred if not provided
    comment="Some factual errors", # optional
)

# Method 2: Score current span/generation (within context)
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    # Score the current span
    span.score(
        name="accuracy",
        value="partially correct",
        data_type="CATEGORICAL",
        comment="Some factual errors"
    )

    # Score the trace
    span.score_trace(
        name="overall_quality",
        value="partially correct",
        data_type="CATEGORICAL"
    )

# Method 3: Score via the current context
with langfuse.start_as_current_observation(as_type="span", name="my-operation"):
    # Score the current span
    langfuse.score_current_span(
        name="accuracy",
        value="partially correct",
        data_type="CATEGORICAL",
        comment="Some factual errors"
    )

    # Score the trace
    langfuse.score_current_trace(
        name="overall_quality",
        value="partially correct",
        data_type="CATEGORICAL"
    )
```

</Tab>
<Tab>
Boolean scores must be provided as a float. The value's string equivalent will be automatically populated and is accessible on read. See [API reference](/docs/api) for more details on POST/GET scores endpoints.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    name="helpfulness",
    value=0, # 0 or 1
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    data_type="BOOLEAN", # required, numeric values without data type would be inferred as NUMERIC
    comment="Incorrect answer", # optional
)

# Method 2: Score current span/generation (within context)
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    # Score the current span
    span.score(
        name="helpfulness",
        value=1, # 0 or 1
        data_type="BOOLEAN",
        comment="Very helpful response"
    )

    # Score the trace
    span.score_trace(
        name="overall_quality",
        value=1, # 0 or 1
        data_type="BOOLEAN"
    )
# Method 3: Score via the current context
with langfuse.start_as_current_observation(as_type="span", name="my-operation"):
    # Score the current span
    langfuse.score_current_span(
        name="helpfulness",
        value=1, # 0 or 1
        data_type="BOOLEAN",
        comment="Very helpful response"
    )

    # Score the trace
    langfuse.score_current_trace(
        name="overall_quality",
        value=1, # 0 or 1
        data_type="BOOLEAN"
    )
```

</Tab>
<Tab>
Text score values must be provided as strings between 1 and 500 characters.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    name="reviewer_notes",
    value="The response was helpful but could be more concise.",
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    data_type="TEXT", # optional, inferred if not provided
    comment="Reviewed by QA team", # optional
)

# Method 2: Score current span/generation (within context)
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    # Score the current span
    span.score(
        name="reviewer_notes",
        value="The response was helpful but could be more concise.",
        data_type="TEXT",
        comment="Reviewed by QA team"
    )

    # Score the trace
    span.score_trace(
        name="overall_notes",
        value="Good quality overall, minor formatting issues.",
        data_type="TEXT"
    )

# Method 3: Score via the current context
with langfuse.start_as_current_observation(as_type="span", name="my-operation"):
    # Score the current span
    langfuse.score_current_span(
        name="reviewer_notes",
        value="The response was helpful but could be more concise.",
        data_type="TEXT",
        comment="Reviewed by QA team"
    )

    # Score the trace
    langfuse.score_current_trace(
        name="overall_notes",
        value="Good quality overall, minor formatting issues.",
        data_type="TEXT"
    )
```

</Tab>
</Tabs>

</Tab>
<Tab>

<Tabs items={["Numeric", "Categorical", "Boolean", "Text"]}>
<Tab>
Numeric score values must be provided as float.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "correctness",
  value: 0.9,
  dataType: "NUMERIC", // optional, inferred if not provided
  comment: "Factually correct", // optional
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
<Tab>
Categorical score values must be provided as strings.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "accuracy",
  value: "partially correct",
  dataType: "CATEGORICAL", // optional, inferred if not provided
  comment: "Factually correct", // optional
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
<Tab>
Boolean scores must be provided as a float. The value's string equivalent will be automatically populated and is accessible on read. See [API reference](/docs/api) for more details on POST/GET scores endpoints.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "helpfulness",
  value: 0, // 0 or 1
  dataType: "BOOLEAN", // required, numeric values without data type would be inferred as NUMERIC
  comment: "Incorrect answer", // optional
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
<Tab>
Text score values must be provided as strings between 1 and 500 characters.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "reviewer_notes",
  value: "The response was helpful but could be more concise.",
  dataType: "TEXT", // optional, inferred if not provided
  comment: "Reviewed by QA team", // optional
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
</Tabs>

</Tab>
<Tab>

You can also create scores directly via the [REST API](https://api.reference.langfuse.com/#tag/score/POST/api/public/scores). Authenticate using HTTP Basic Auth with your Langfuse Public Key as username and Secret Key as password.

<Tabs items={["Numeric", "Categorical", "Boolean", "Text"]}>
<Tab>
Numeric score values must be provided as float.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "correctness",
    "value": 0.9,
    "dataType": "NUMERIC",
    "comment": "Factually correct"
  }'
```

</Tab>
<Tab>
Categorical score values must be provided as strings.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "accuracy",
    "value": "partially correct",
    "dataType": "CATEGORICAL",
    "comment": "Some factual errors"
  }'
```

</Tab>
<Tab>
Boolean scores must be provided as a float (`0` or `1`). The value's string equivalent will be automatically populated and is accessible on read.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "helpfulness",
    "value": 0,
    "dataType": "BOOLEAN",
    "comment": "Incorrect answer"
  }'
```

</Tab>
<Tab>
Text score values must be provided as strings between 1 and 500 characters.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "reviewer_notes",
    "value": "The response was helpful but could be more concise.",
    "dataType": "TEXT",
    "comment": "Reviewed by QA team"
  }'
```

</Tab>
</Tabs>

</Tab>
</LangTabs>

### Session-level Scores

To score an entire session (without attaching the score to a trace or observation), provide only `session_id` (Python SDK) or `sessionId` (JS/TS SDK and API).

<LangTabs items={["Python SDK", "JS/TS SDK", "API"]}>
<Tab>

```python
from langfuse import get_client
langfuse = get_client()

langfuse.create_score(
    name="session_quality",
    value=0.85,
    session_id="session_id_here",
    data_type="NUMERIC",
    comment="Overall conversation quality"
)
```

</Tab>
<Tab>

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  name: "session_quality",
  value: 0.85,
  sessionId: "session_id_here",
  dataType: "NUMERIC",
  comment: "Overall conversation quality",
});

await langfuse.flush();
```

</Tab>
<Tab>

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_id_here",
    "name": "session_quality",
    "value": 0.85,
    "dataType": "NUMERIC",
    "comment": "Overall conversation quality"
  }'
```

</Tab>
</LangTabs>

## Advanced

### Preventing Duplicate Scores

By default, Langfuse allows for multiple scores of the same `name` on the same trace. This is useful if you'd like to track the evolution of a score over time or if e.g. you've received multiple user feedback scores on the same trace.

In some cases, you want to prevent this behavior or update an existing score. This can be achieved by creating an **idempotency key** on the score and add this as an `id` (JS/TS) / `score_id` (Python) when creating the score, e.g. `<trace_id>-<score_name>`.

Note that if you expect API calls for the same score to be 30+ days apart, you should also use the same timestamp. See [How to update traces, observations, and scores](/faq/all/tracing-data-updates#updating-traces-observations-and-scores) for more details.

### Enforcing a Score Config

Score configs are helpful when you want to standardize your scores for future analysis.

To enforce a score config, you can provide a `configId` when creating a score to reference a `ScoreConfig` that was previously created. `Score Configs` can be defined in the Langfuse UI or via our API. [See our guide on how to create and manage score configs](/faq/all/manage-score-configs).

Whenever you provide a `ScoreConfig`, the score data will be validated against the config. The following rules apply:

- **Score Name**: Must equal the config's name
- **Score Data Type**: When provided, must match the config's data type
- **Score Value when Type is `NUMERIC`**: Value must be within the min and max values defined in the config (if provided, min and max are optional and otherwise are assumed as -∞ and +∞ respectively)
- **Score Value when Type is `CATEGORICAL`**: Value must map to one of the categories defined in the config
- **Score Value when Type is `BOOLEAN`**: Value must equal `0` or `1`
- **Score Value when Type is `TEXT`**: Value must be a non-empty string of at most 500 characters

<LangTabs items={["Python SDK", "JS/TS SDK", "API"]}>

<Tab>

<Tabs items={["Numeric Scores", "Categorical Scores", "Boolean Scores", "Text Scores"]}>
<Tab>
When ingesting numeric scores, you can provide the value as a float. If you provide a configId, the score value will be validated against the config's numeric range, which might be defined by a minimum and/or maximum value.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    session_id="session_id_here", # optional, ID of the session the score relates to
    name="accuracy",
    value=0.9,
    comment="Factually correct", # optional
    score_id="unique_id", # optional, can be used as an idempotency key to update the score subsequently
    config_id="78545-6565-3453654-43543", # optional, to ensure that the score follows a specific min/max value range
    data_type="NUMERIC" # optional, possibly inferred
)

# Method 2: Score within context
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    span.score(
        name="accuracy",
        value=0.9,
        comment="Factually correct",
        config_id="78545-6565-3453654-43543",
        data_type="NUMERIC"
    )
```

</Tab>
<Tab>
Categorical scores are used to evaluate data that falls into specific categories. When ingesting categorical scores, you can provide the value as a string. If you provide a configId, the score value will be validated against the config's categories.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    name="correctness",
    value="correct",
    comment="Factually correct", # optional
    score_id="unique_id", # optional, can be used as an idempotency key to update the score subsequently
    config_id="12345-6565-3453654-43543", # optional, to ensure that the score maps to a specific category defined in a score config
    data_type="CATEGORICAL" # optional, possibly inferred
)

# Method 2: Score within context
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    span.score(
        name="correctness",
        value="correct",
        comment="Factually correct",
        config_id="12345-6565-3453654-43543",
        data_type="CATEGORICAL"
    )
```

</Tab>
<Tab>
When ingesting boolean scores, you can provide the value as a float. If you provide a configId, the score's name and config's name must match as well as their data types.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    name="helpfulness",
    value=1,
    comment="Factually correct", # optional
    score_id="unique_id", # optional, can be used as an idempotency key to update the score subsequently
    config_id="93547-6565-3453654-43543", # optional, can be used to infer the score data type and validate the score value
    data_type="BOOLEAN" # optional, possibly inferred
)

# Method 2: Score within context
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    span.score(
        name="helpfulness",
        value=1,
        comment="Factually correct",
        config_id="93547-6565-3453654-43543",
        data_type="BOOLEAN"
    )
```

</Tab>
<Tab>
When ingesting text scores, provide the value as a string (1–500 characters). If you provide a configId, the score's name and config's name must match as well as their data types.

```python
from langfuse import get_client
langfuse = get_client()

# Method 1: Score via low-level method
langfuse.create_score(
    trace_id="trace_id_here",
    observation_id="observation_id_here", # optional
    name="reviewer_notes",
    value="The response was helpful but could be more concise.",
    comment="Reviewed by QA team", # optional
    score_id="unique_id", # optional, can be used as an idempotency key to update the score subsequently
    config_id="24680-6565-3453654-43543", # optional
    data_type="TEXT" # optional, possibly inferred
)

# Method 2: Score within context
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    span.score(
        name="reviewer_notes",
        value="The response was helpful but could be more concise.",
        comment="Reviewed by QA team",
        config_id="24680-6565-3453654-43543",
        data_type="TEXT"
    )
```

</Tab>
</Tabs>

</Tab>
<Tab>

<Tabs items={["Numeric Scores", "Categorical Scores", "Boolean Scores", "Text Scores"]}>
<Tab>
When ingesting numeric scores, you can provide the value as a float. If you provide a configId, the score value will be validated against the config's numeric range, which might be defined by a minimum and/or maximum value.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "accuracy",
  value: 0.9,
  comment: "Factually correct", // optional
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  configId: "78545-6565-3453654-43543", // optional, to ensure that the score follows a specific min/max value range
  dataType: "NUMERIC", // optional, possibly inferred
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
<Tab>
Categorical scores are used to evaluate data that falls into specific categories. When ingesting categorical scores, you can provide the value as a string. If you provide a configId, the score value will be validated against the config's categories.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "correctness",
  value: "correct",
  comment: "Factually correct", // optional
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  configId: "12345-6565-3453654-43543", // optional, to ensure that a score maps to a specific category defined in a score config
  dataType: "CATEGORICAL", // optional, possibly inferred
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
<Tab>
When ingesting boolean scores, you can provide the value as a float. If you provide a configId, the score's name and config's name must match as well as their data types.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "helpfulness",
  value: 1,
  comment: "Factually correct", // optional
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  configId: "93547-6565-3453654-43543", // optional, can be used to infer the score data type and validate the score value
  dataType: "BOOLEAN", // optional, possibly inferred
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
<Tab>
When ingesting text scores, provide the value as a string (1–500 characters). If you provide a configId, the score's name and config's name must match as well as their data types.

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  traceId: message.traceId,
  observationId: message.generationId, // optional
  name: "reviewer_notes",
  value: "The response was helpful but could be more concise.",
  comment: "Reviewed by QA team", // optional
  id: "unique_id", // optional, can be used as an idempotency key to update the score subsequently
  configId: "24680-6565-3453654-43543", // optional
  dataType: "TEXT", // optional, possibly inferred
});

// Flush the scores in short-lived environments
await langfuse.flush();
```

</Tab>
</Tabs>

</Tab>
<Tab>

You can also enforce score configs via the [REST API](https://api.reference.langfuse.com/#tag/score/POST/api/public/scores) by providing a `configId`.

<Tabs items={["Numeric Scores", "Categorical Scores", "Boolean Scores", "Text Scores"]}>
<Tab>
When ingesting numeric scores, you can provide the value as a float. If you provide a configId, the score value will be validated against the config's numeric range.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "id": "unique_id",
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "accuracy",
    "value": 0.9,
    "dataType": "NUMERIC",
    "configId": "78545-6565-3453654-43543",
    "comment": "Factually correct"
  }'
```

</Tab>
<Tab>
Categorical scores are used to evaluate data that falls into specific categories. If you provide a configId, the score value will be validated against the config's categories.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "id": "unique_id",
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "correctness",
    "value": "correct",
    "dataType": "CATEGORICAL",
    "configId": "12345-6565-3453654-43543",
    "comment": "Factually correct"
  }'
```

</Tab>
<Tab>
When ingesting boolean scores, you can provide the value as a float. If you provide a configId, the score's name and config's name must match as well as their data types.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "id": "unique_id",
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "helpfulness",
    "value": 1,
    "dataType": "BOOLEAN",
    "configId": "93547-6565-3453654-43543",
    "comment": "Factually correct"
  }'
```

</Tab>
<Tab>
When ingesting text scores, provide the value as a string (1–500 characters). If you provide a configId, the score's name and config's name must match as well as their data types.

```bash
curl -X POST https://cloud.langfuse.com/api/public/scores \
  -u "pk-lf-...":"sk-lf-..." \
  -H "Content-Type: application/json" \
  -d '{
    "id": "unique_id",
    "traceId": "trace_id_here",
    "observationId": "observation_id_here",
    "name": "reviewer_notes",
    "value": "The response was helpful but could be more concise.",
    "dataType": "TEXT",
    "configId": "24680-6565-3453654-43543",
    "comment": "Reviewed by QA team"
  }'
```

</Tab>
</Tabs>

</Tab>

See [API reference](/docs/api) for more details on POST/GET score configs endpoints.

</LangTabs>

### Inferred Score Properties

Certain score properties might be inferred based on your input:

- **If you don't provide a score data type** it will always be inferred. See tables below for details.
- **For boolean and categorical scores**, we will provide the score value in both numerical and string format where possible. The score value format that is not provided as input, i.e. the translated value is referred to as the inferred value in the tables below.
- **On read for boolean scores both** numerical and string representations of the score value will be returned, e.g. both 1 and True.
- **For categorical scores**, the string representation is always provided and a numerical mapping of the category will be produced only if a `ScoreConfig` was provided.

Detailed Examples:

<Tabs items={["Numeric Scores", "Categorical Scores", "Boolean Scores", "Text Scores"]}>
<Tab>
For example, let's assume you'd like to ingest a numeric score to measure **accuracy**. We have included a table of possible score ingestion scenarios below.

| Value   | Data Type | Config Id | Description                                                 | Inferred Data Type | Valid                            |
| ------- | --------- | --------- | ----------------------------------------------------------- | ------------------ | -------------------------------- |
| `0.9`   | `Null`    | `Null`    | Data type is inferred                                       | `NUMERIC`          | Yes                              |
| `0.9`   | `NUMERIC` | `Null`    | No properties inferred                                      |                    | Yes                              |
| `depth` | `NUMERIC` | `Null`    | Error: data type of value does not match provided data type |                    | No                               |
| `0.9`   | `NUMERIC` | `78545`   | No properties inferred                                      |                    | Conditional on config validation |
| `0.9`   | `Null`    | `78545`   | Data type inferred                                          | `NUMERIC`          | Conditional on config validation |
| `depth` | `NUMERIC` | `78545`   | Error: data type of value does not match provided data type |                    | No                               |

</Tab>
<Tab>
For example, let's assume you'd like to ingest a categorical score to measure **correctness**. We have included a table of possible score ingestion scenarios below.

| Value     | Data Type     | Config Id | Description                                                 | Inferred Data Type | Inferred Value representation       | Valid                            |
| --------- | ------------- | --------- | ----------------------------------------------------------- | ------------------ | ----------------------------------- | -------------------------------- |
| `correct` | `Null`        | `Null`    | Data type is inferred                                       | `CATEGORICAL`      |                                     | Yes                              |
| `correct` | `CATEGORICAL` | `Null`    | No properties inferred                                      |                    |                                     | Yes                              |
| `1`       | `CATEGORICAL` | `Null`    | Error: data type of value does not match provided data type |                    |                                     | No                               |
| `correct` | `CATEGORICAL` | `12345`   | Numeric value inferred                                      |                    | `4` numeric config category mapping | Conditional on config validation |
| `correct` | `NULL`        | `12345`   | Data type inferred                                          | `CATEGORICAL`      |                                     | Conditional on config validation |
| `1`       | `CATEGORICAL` | `12345`   | Error: data type of value does not match provided data type |                    |                                     | No                               |

</Tab>
<Tab>
For example, let's assume you'd like to ingest a boolean score to measure **helpfulness**. We have included a table of possible score ingestion scenarios below.

| Value   | Data Type | Config Id | Description                                                 | Inferred Data Type | Inferred Value representation | Valid                            |
| ------- | --------- | --------- | ----------------------------------------------------------- | ------------------ | ----------------------------- | -------------------------------- |
| `1`     | `BOOLEAN` | `Null`    | Value's string equivalent inferred                          |                    | `True`                        | Yes                              |
| `true`  | `BOOLEAN` | `Null`    | Error: data type of value does not match provided data type |                    |                               | No                               |
| `3`     | `BOOLEAN` | `Null`    | Error: boolean data type expects `0` or `1` as input value  |                    |                               | No                               |
| `0.9`   | `Null`    | `93547`   | Data type and value's string equivalent inferred            | `BOOLEAN`          | `True`                        | Conditional on config validation |
| `depth` | `BOOLEAN` | `93547`   | Error: data type of value does not match provided data type |                    |                               | No                               |

</Tab>
<Tab>
For example, let's assume you'd like to ingest a text score to capture **reviewer notes**. Text scores must be non-empty strings of at most 500 characters.

| Value   | Data Type | Config Id | Description                                                 | Inferred Data Type | Valid                            |
| ------- | --------- | --------- | ----------------------------------------------------------- | ------------------ | -------------------------------- |
| `"Good response"` | `Null`    | `Null`    | Data type is inferred                              | `TEXT`             | Yes                              |
| `"Good response"` | `TEXT`    | `Null`    | No properties inferred                             |                    | Yes                              |
| `0.9`   | `TEXT`    | `Null`    | Error: data type of value does not match provided data type |                    | No                               |
| `"Good response"` | `TEXT`    | `24680`   | No properties inferred                             |                    | Conditional on config validation |
| `"Good response"` | `Null`    | `24680`   | Data type inferred                                 | `TEXT`             | Conditional on config validation |
| `""`    | `TEXT`    | `Null`    | Error: text scores must be non-empty                        |                    | No                               |

</Tab>
</Tabs>

## Update Existing Scores via API/SDKs [#update]

When creating a score, you can provide an optional `id` (JS/TS) / `score_id` (Python) parameter. This will update the score if it already exists within your project.

If you want to update a score without needing to fetch the list of existing scores from Langfuse, you can set your own `id` parameter as an idempotency key when initially creating the score.
