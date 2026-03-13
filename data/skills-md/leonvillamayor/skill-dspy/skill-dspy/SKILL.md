---
name: skill-dspy
description: "Expert guide for building AI programs with DSPy — the declarative framework for LM programming with automatic prompt optimization. Use this skill PROACTIVELY whenever: importing dspy, using Signatures/Modules/Optimizers, building RAG/agent/multi-hop pipelines, optimizing with BootstrapFewShot/MIPROv2/COPRO/SIMBA/GEPA/BetterTogether, writing dspy.ChainOfThought/ReAct/Predict/CodeAct, evaluating with dspy.Evaluate, using dspy.Refine/BestOfN for output quality enforcement, configuring any LM provider (OpenAI/Anthropic/Gemini/Ollama/reasoning models), saving/loading compiled programs, integrating MCP tools (stdio or HTTP), streaming, async modules, tracking token usage, or debugging with inspect_history. Covers: LM config, Signatures, Modules, Optimizers, Evaluation, Refine/BestOfN, Tools, Adapters, Streaming, Async, Callbacks, Embeddings, and Save/Load."
license: MIT
metadata:
  author: skill-dspy
  version: "3.1.3"
---

# DSPy Expert Guide

DSPy is a declarative framework for programming language models. Instead of hand-writing prompts, you define *what* your program should do (via Signatures and Modules), and DSPy figures out *how* to prompt the LM to do it — including automatic optimization.

## Core Mental Model

```
Signature  →  defines I/O schema (what to compute)
Module     →  implements a reasoning strategy (how to compute)
Optimizer  →  tunes prompts/weights automatically (how to improve)
Evaluate   →  measures quality (how to measure)
```

---

## 1. Language Model Setup

DSPy uses [LiteLLM](https://litellm.ai/) under the hood, so any provider is supported.

```python
import dspy

# OpenAI
lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_KEY')

# Anthropic
lm = dspy.LM('anthropic/claude-sonnet-4-5-20250929', api_key='YOUR_KEY')

# Google Gemini
lm = dspy.LM('gemini/gemini-2.5-pro-preview-03-25', api_key='YOUR_KEY')

# Ollama (local)
lm = dspy.LM('ollama_chat/llama3', api_base='http://localhost:11434')

# Custom OpenAI-compatible endpoint
lm = dspy.LM('openai/your-model', api_key='KEY', api_base='YOUR_URL')

# Configure globally
dspy.configure(lm=lm)

# Multiple LMs — use context managers for per-call override
with dspy.context(lm=dspy.LM('openai/gpt-4o')):
    result = my_module(question="...")
```

**Key LM parameters:**
- `temperature` — sampling temperature (default: 0.0 for deterministic)
- `max_tokens` — max output tokens
- `cache=True` — enable response caching (default True)
- `num_retries=3` — retries on transient failures
- `model_type` — `"chat"`, `"text"`, or `"responses"` (use `"responses"` for OpenAI reasoning models like o3/o4)
- `use_developer_role=True` — for OpenAI reasoning models that require developer system prompts
- `finetuning_model` — specify a separate model name for fine-tuning (vs inference)
- `callbacks=[...]` — per-LM callback hooks

**Reasoning models (o3, o4-mini, etc.):**
```python
lm = dspy.LM('openai/o3-mini', model_type='responses', temperature=1.0, max_tokens=16000)
dspy.configure(lm=lm, adapter=dspy.TwoStepAdapter(dspy.LM('openai/gpt-4o-mini')))
```

**`dspy.configure` full options:**
```python
dspy.configure(
    lm=lm,
    adapter=dspy.ChatAdapter(),            # global output adapter
    callbacks=[...],                        # global callbacks
    track_usage=True,                       # enable token usage tracking per prediction
    allow_tool_async_sync_conversion=True,  # allow async tools in sync context
    experimental=True,                      # enable experimental features (BetterTogether, BootstrapFinetune)
    max_errors=10,                          # stop Evaluate after N errors
)
```

**Token usage tracking (requires `track_usage=True`):**
```python
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini', cache=False), track_usage=True)
result = my_program(question="What is DSPy?")
print(result.get_lm_usage())   # {'openai/gpt-4o-mini': {'prompt_tokens': 120, 'completion_tokens': 45}}
```

---

## 2. Signatures

Signatures define the *input/output schema* of an LM call.

### Inline (string) signatures
```python
# Simple string: "inputs -> outputs"
predict = dspy.Predict("question -> answer")
cot = dspy.ChainOfThought("context, question -> answer")
```

### Class-based signatures (recommended for typed, documented fields)
```python
class Classify(dspy.Signature):
    """Classify sentiment of a product review."""
    review: str = dspy.InputField()
    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="confidence score 0-1")

class RAGAnswer(dspy.Signature):
    """Answer a question given retrieved context."""
    context: list[str] = dspy.InputField(desc="retrieved passages")
    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="concise factual answer")
    citations: list[int] = dspy.OutputField(desc="indices of supporting passages")
```

### Signature manipulation
```python
# Extend with new fields
ExtendedSig = MySignature.append("new_output", dspy.OutputField(desc="..."), type_=str)

# Update field descriptions
UpdatedSig = MySignature.with_updated_fields("answer", desc="detailed explanation")

# Add instructions
InstructedSig = MySignature.with_instructions("Always respond in Spanish.")
```

**Supported field types:** `str`, `int`, `float`, `bool`, `list[T]`, `dict[K,V]`, `Optional[T]`, `Union[T,U]`, `Literal[...]`, `dspy.Image`, `dspy.Audio`, `dspy.History`, `dspy.Code`, `dspy.File`, custom Pydantic models.

**`dspy.Code` — typed code output:**
```python
class CodeSig(dspy.Signature):
    task: str = dspy.InputField()
    solution: dspy.Code["python"] = dspy.OutputField()  # language-typed code

predictor = dspy.Predict(CodeSig)
result = predictor(task="Write a binary search function")
# result.solution is a Code object with the generated python code
```

**`dspy.File` — file data in pipelines (3.1.0+):**
```python
class ProcessFile(dspy.Signature):
    file: dspy.File = dspy.InputField()
    summary: str = dspy.OutputField()
```

**`dspy.Reasoning` — capture native reasoning from reasoning models:**
```python
# dspy.Reasoning is a type for capturing the native internal chain-of-thought
# from reasoning models (o3, o4-mini, DeepSeek-R1).
# Use it as an output field type to explicitly request reasoning capture.

class ReasonedAnswer(dspy.Signature):
    question: str = dspy.InputField()
    reasoning: dspy.Reasoning = dspy.OutputField()  # captures native CoT
    answer: str = dspy.OutputField()

# NOTE: In DSPy 3.1.3, the automatic injection of dspy.Reasoning into
# ChainOfThought for reasoning models was reverted. You must explicitly
# include dspy.Reasoning in your Signature if you want to capture it.
# For non-reasoning models, dspy.Reasoning behaves like a regular str field.
```

---

## 3. Built-in Modules

All modules inherit from `dspy.Module`. Use them directly or compose them.

| Module | Description | Typical Use |
|--------|-------------|-------------|
| `dspy.Predict` | Single LM call | Simple extraction, classification |
| `dspy.ChainOfThought` | CoT reasoning | Multi-step reasoning, explanation |
| `dspy.ProgramOfThought` | Code-based reasoning (needs Deno) | Math, symbolic computation |
| `dspy.ReAct` | Tool-use agent loop | Search, APIs, multi-tool agents |
| `dspy.CodeAct` | Python code execution (pure fns only) | Complex computations via code |
| `dspy.RLM` | Recursive LM — explores large contexts via REPL | Long documents, complex analysis (3.1.1+) |
| `dspy.MultiChainComparison` | Ensemble of CoT chains | High-accuracy QA |
| `dspy.Refine` | Iterative refinement with feedback | Quality improvement loops |
| `dspy.BestOfN` | Sample N independently, pick best | Reliability via sampling |
| `dspy.Parallel` | Run modules in parallel | Batch processing |

**`dspy.BestOfN` vs `dspy.Refine`:**
- `BestOfN(module, N=5, reward_fn=fn, threshold=1.0)` — N **independent** runs, picks the best. No feedback between attempts.
- `Refine(module, N=3, reward_fn=fn, threshold=1.0)` — N runs **with automatic feedback**. After each failed attempt, DSPy generates hints ("Past Output" + "Instruction" fields) for the next run. Use `Refine` when each attempt can learn from the previous one.

**`dspy.CodeAct` constraint:** only pure Python functions as tools — no lambdas, callable objects, or external libraries:
```python
from dspy.predict import CodeAct   # note: not dspy.CodeAct directly
act = CodeAct("n -> factorial_result", tools=[factorial_fn], max_iters=3)
```

**`dspy.Parallel` full API (3.1.2: `timeout` and `straggler_limit` now exposed):**
```python
parallel = dspy.Parallel(num_threads=8, timeout=120, straggler_limit=0.9, return_failed_examples=False)
results = parallel([(module, example1), (module, example2)])

# Convenience: every dspy.Module has .batch()
results = my_module.batch(examples=[ex1, ex2, ex3], num_threads=4, return_failed_examples=True)
# If return_failed_examples=True: returns (results, failed_examples, exceptions)
```

**`dspy.RLM` — Recursive Language Model (3.1.1+):** Explores large contexts via sandboxed Python REPL. Requires Deno.
```python
rlm = dspy.RLM(
    signature="context, query -> answer",
    max_iterations=20,      # maximum REPL loops
    max_llm_calls=50,       # maximum sub-LM calls
    sub_lm=None,            # optional cheaper model for sub-queries
    tools=None,             # list of custom tool functions
)
result = rlm(context="...very large document...", query="What is the revenue?")
print(result.answer)
print(result.trajectory)       # list of {code, output} steps
```
Built-in REPL tools: `llm_query(prompt)`, `llm_query_batched(prompts)`, `SUBMIT(...)`. Also supports `aforward()` for async.

**`dspy.LocalSandbox` for code execution:**
```python
sandbox = dspy.LocalSandbox()
result = sandbox.execute("value = 2*5 + 4\nvalue")  # returns 14
```

### Usage examples
```python
# Predict — basic
predictor = dspy.Predict("question -> answer")
result = predictor(question="What is 2+2?")
print(result.answer)

# ChainOfThought — adds step-by-step reasoning
cot = dspy.ChainOfThought("question -> answer")
result = cot(question="If a train travels 120km in 2h, what is its speed?")
print(result.reasoning, result.answer)

# ReAct — tool-using agent
def search_web(query: str) -> str:
    """Search the web for information."""
    ...  # your implementation

react = dspy.ReAct("question -> answer", tools=[search_web])
result = react(question="Who won the 2024 Olympics marathon?")

# ProgramOfThought — generates and executes Python code (requires Deno runtime)
pot = dspy.ProgramOfThought("question -> answer", max_iters=3)
result = pot(question="What is the sum of squares from 1 to 10?")
print(result.answer)  # "385"
# ProgramOfThought writes Python code, executes it in a sandbox, and extracts the answer.
# Ideal for math, symbolic computation, and data manipulation tasks.

# BestOfN — pick best of multiple samples
bon = dspy.BestOfN(dspy.ChainOfThought("question -> answer"), N=5, reward_fn=my_metric)

# Refine — iterative improvement
refine = dspy.Refine(dspy.ChainOfThought("draft -> refined"), N=3, reward_fn=quality_check)
```

---

## 4. Custom Modules

Build complex programs by composing modules:

```python
class RAG(dspy.Module):
    def __init__(self, num_docs=5):
        self.num_docs = num_docs
        self.retrieve = dspy.Retrieve(k=num_docs)          # if using a retriever
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

class MultiHopRAG(dspy.Module):
    def __init__(self, hops=2):
        self.generate_query = [dspy.ChainOfThought("context, question -> query") for _ in range(hops)]
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = []
        for i, gen_q in enumerate(self.generate_query):
            query = gen_q(context=context, question=question).query
            context += search(query)   # your search function
        return self.generate_answer(context=context, question=question)
```

**Module API:**
- `module.forward(**kwargs)` — main logic
- `module(...)` — calls forward
- `module.named_predictors()` — iterate over all sub-predictors
- `module.set_lm(lm)` — set LM for all predictors in this module
- `module.get_lm()` — get the LM currently used by the module's predictors
- `module.batch(examples, num_threads=2, return_failed_examples=False)` — run module on a list of examples in parallel (returns list of results; if `return_failed_examples=True`, returns `(results, failed_examples, exceptions)`)
- `module.deepcopy()` — deep copy the module
- `module.reset_copy()` — copy with reset state
- `module.save(path)` / `module.load(path)` — persistence

---

## 5. Data & Examples

```python
# dspy.Example — structured training/eval data
example = dspy.Example(question="What is DSPy?", answer="A framework for LM programming")

# Specify which fields are inputs
example = example.with_inputs("question")
print(example.inputs())   # {'question': ...}
print(example.labels())   # {'answer': ...}

# dspy.Prediction — module output container
pred = dspy.Prediction(answer="42", reasoning="step by step...")
print(pred.answer)

# Load built-in datasets
from dspy.datasets import HotPotQA, GSM8K, MATH
hotpotqa = HotPotQA(train_seed=2024, train_size=500)
trainset = hotpotqa.train
devset = hotpotqa.dev

gsm8k = GSM8K()                # grade-school math word problems
trainset = gsm8k.train          # fields: question, answer (numeric)

math_ds = MATH()                # competition-level math problems
trainset = math_ds.train        # fields: question, answer

# DataLoader — load custom datasets from various sources
from dspy.datasets import DataLoader
dl = DataLoader()

# From HuggingFace
dataset = dl.from_huggingface(
    "dataset_name",
    fields=["question", "answer"],
    input_keys=("question",),
    split="train"
)

# Also supports:
# dl.from_csv("data.csv", fields=["q", "a"], input_keys=("q",))
# dl.from_json("data.json", fields=["q", "a"], input_keys=("q",))
# dl.from_pandas(df, fields=["q", "a"], input_keys=("q",))
# dl.from_parquet("data.parquet", fields=["q", "a"], input_keys=("q",))
```

---

## 6. Optimizers (Teleprompters)

See `references/optimizers.md` for full details. Quick reference:

| Optimizer | Best For | Data Needed | Notes |
|-----------|----------|-------------|-------|
| `BootstrapFewShot` | Few-shot demos, fast | 5-50 examples | |
| `BootstrapFewShotWithRandomSearch` | Better few-shot selection | ~50-200 examples | |
| `MIPROv2` | Full prompt + demo optimization | 50-300 examples | **Default recommendation** |
| `COPRO` | Instruction-only optimization | 20-100 examples | |
| `SIMBA` | Mini-batch stochastic optimization | 20-200 examples | Faster for large programs |
| `GEPA` | Evolutionary prompt optimization | 50+ examples | 5-arg metric required |
| `BetterTogether` | Prompt + weight joint optimization | 100+ examples | Requires `experimental=True` |
| `KNNFewShot` | Dynamic example retrieval | Training set | |
| `Ensemble` | Combine multiple programs | Multiple programs | |
| `BootstrapFinetune` | Fine-tuning LM weights | 100+ examples | Requires `experimental=True` |
| `ArborGRPO` | Reinforcement learning / GRPO | 100+ examples | `pip install arbor-ai`; multi-module RL |

**GEPA critical note — its metric must accept 5 arguments:**
```python
def gepa_metric(gold, pred, trace, pred_name, pred_trace):
    return gold.answer.lower() == pred.answer.lower()
optimizer = dspy.GEPA(metric=gepa_metric, auto="medium", reflection_lm=dspy.LM('openai/gpt-4o'))
```

**BetterTogether (experimental) — combines prompt + weight optimization:**
```python
dspy.settings.experimental = True
from dspy.teleprompt import BetterTogether
optimizer = BetterTogether(metric=my_metric)
optimized = optimizer.compile(program, trainset=trainset, strategy="p -> w -> p")
```

```python
# Standard optimization pattern
optimizer = dspy.MIPROv2(metric=my_metric, auto="medium", num_threads=8)
optimized = optimizer.compile(my_program, trainset=trainset)
optimized.save("optimized.json")
```

---

## 7. Evaluation

See `references/evaluation.md` for full details.

```python
# Define a metric
def my_metric(example, pred, trace=None):
    return example.answer.lower() == pred.answer.lower()

# Run evaluation
evaluator = dspy.Evaluate(
    devset=devset,
    metric=my_metric,
    num_threads=8,
    display_progress=True,
    display_table=5,
)
score = evaluator(my_program)  # returns EvaluationResult

# Built-in metrics
dspy.evaluate.answer_exact_match      # exact string match
dspy.evaluate.answer_passage_match    # answer appears in passage
dspy.SemanticF1()                     # LM-based semantic F1 score
dspy.CompleteAndGrounded()            # checks if answer is complete and grounded in context
```

---

## 8. Output Quality Enforcement (Refine / BestOfN)

**`dspy.Assert` and `dspy.Suggest` were deprecated and removed in DSPy 3.1.x.** Use `dspy.Refine` or `dspy.BestOfN` instead.

### `dspy.Refine` — iterative refinement with automatic feedback

After each failed attempt, DSPy automatically generates feedback ("Past Output" + "Instruction" fields) and feeds it to the next attempt. Use when each retry can learn from the previous one.

```python
def quality_check(example, pred, trace=None):
    """Return a float 0-1 or bool. Refine retries until threshold is met."""
    return len(pred.answer) > 10 and pred.answer[0].isupper()

class QAModule(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("question -> answer")
    def forward(self, question):
        return self.generate(question=question)

# Wrap any module with Refine
refined = dspy.Refine(
    module=QAModule(),
    N=3,              # max attempts (default 3)
    reward_fn=quality_check,
    threshold=1.0,    # reward must reach this to stop early
)
result = refined(question="What is DSPy?")
```

### `dspy.BestOfN` — N independent samples, pick best

Runs N **independent** calls (no feedback between them) and returns the one with the highest reward. Simpler but uses more tokens.

```python
def my_metric(example, pred, trace=None):
    return float(pred.answer.lower().count("dspy") > 0)

best = dspy.BestOfN(
    module=dspy.ChainOfThought("question -> answer"),
    N=5,              # number of independent samples
    reward_fn=my_metric,
    threshold=1.0,    # stop early if reward reaches this
)
result = best(question="Explain DSPy in one sentence.")
```

### When to use which
- **Refine**: When feedback helps — e.g., "your answer was too short, try again with more detail"
- **BestOfN**: When outputs are independent — e.g., creative tasks where variety helps
- **Typed `Literal` fields**: When you just need to constrain outputs to a set of values — use `Literal["a", "b", "c"]` in the Signature (no retry needed, the adapter enforces it)

---

## 9. Tools & MCP

See `references/advanced.md` for full details.

```python
# Define tools as Python functions (used in ReAct/CodeAct)
def calculator(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

def search(query: str, k: int = 3) -> list[str]:
    """Search Wikipedia for passages."""
    results = dspy.ColBERTv2(url='http://...')(query, k=k)
    return [r['text'] for r in results]

agent = dspy.ReAct("question -> answer", tools=[calculator, search])

# MCP tool integration (async)
from mcp import ClientSession
dspy_tool = dspy.Tool.from_mcp_tool(session, mcp_tool_object)
agent = dspy.ReAct("question -> answer", tools=[dspy_tool])
```

---

## 10. Special Data Types

```python
# Images (multimodal)
class DescribeImage(dspy.Signature):
    image: dspy.Image = dspy.InputField()
    description: str = dspy.OutputField()

img_from_url = dspy.Image.from_url("https://example.com/image.jpg")
img_from_file = dspy.Image.from_file("local.png")
img_from_b64 = dspy.Image(url="data:image/png;base64,...")

# Audio
class TranscribeAudio(dspy.Signature):
    audio: dspy.Audio = dspy.InputField()
    transcript: str = dspy.OutputField()

audio = dspy.Audio.from_file("speech.mp3")

# Conversation History
class Chat(dspy.Signature):
    history: dspy.History = dspy.InputField()
    message: str = dspy.InputField()
    response: str = dspy.OutputField()

history = dspy.History(messages=[
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"},
])
```

---

## 11. Save & Load

Two modes — state-only (recommended) vs full program:

```python
# State-only (JSON) — saves signatures, demos, LM per predictor
optimized_program.save("my_program.json")

# State-only (pickle) — needed when state contains non-JSON-serializable objects (e.g., dspy.Image)
optimized_program.save("my_program.pkl", save_program=False)

# Full program (architecture + state) — saves to directory via cloudpickle
optimized_program.save("./my_program_dir/", save_program=True)
# With custom modules that need to be serialized by value:
optimized_program.save("./my_program_dir/", save_program=True, modules_to_serialize=[my_module])

# Load state-only (requires re-instantiating the class)
loaded = MyProgramClass()
loaded.load("my_program.json")

# Load full program (architecture + state) — no need to re-define the class
loaded = dspy.load("./my_program_dir/")
# Returns a fully functional module with all state, signatures, demos, and LM config restored.
```

**Security:** `.pkl` files and `dspy.load()` use cloudpickle/pickle and can execute arbitrary code on load — only load from trusted sources.

---

## Quick Patterns

### RAG pipeline
```python
class RAG(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought('context, question -> answer')
    def forward(self, question):
        context = search(question)   # your retrieval function
        return self.respond(context=context, question=question)

rag = RAG()
tp = dspy.MIPROv2(metric=dspy.SemanticF1(), auto="medium")
optimized_rag = tp.compile(rag, trainset=trainset)
```

### Classification with typed constraints
```python
class Classify(dspy.Module):
    def __init__(self, classes):
        self.classes = classes
        # Literal type constrains the output — no runtime assertions needed
        self.predict = dspy.Predict(
            dspy.Signature("text -> label").with_updated_fields(
                "label", type_=Literal[tuple(classes)]
            )
        )
    def forward(self, text):
        return self.predict(text=text)

# For extra reliability, wrap with Refine
classifier = Classify(classes=["positive", "negative", "neutral"])
def valid_label(example, pred, trace=None):
    return pred.label in ["positive", "negative", "neutral"]

safe_classifier = dspy.Refine(classifier, N=3, reward_fn=valid_label)
```

### Inspect LM calls
```python
dspy.inspect_history(n=5)   # show last 5 LM interactions
```

---

## Reference Files

- `references/optimizers.md` — Deep dive: all optimizers with parameters and strategies
- `references/evaluation.md` — Evaluation, metrics, built-in datasets
- `references/advanced.md` — Adapters, callbacks, streaming, async, MCP, fine-tuning
