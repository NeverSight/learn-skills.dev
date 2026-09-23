---
name: dspy
description: >-
  Optimize and build programmatic prompt systems with Stanford DSPy. Signatures, modules
  (Predict, ChainOfThought, ReAct), optimizer/teleprompter selection, compilation,
  caching, evaluation. Use when doing programmatic prompt optimization or building
  compiled prompt programs. Do not use this skill for unrelated requests; route to the
  nearest named specialist.
license: MIT
metadata:
  author: Magnus Hedemark
  version: 1.1.0
  source: https://dspy.ai
---

# DSPy Expert Skill

DSPy is a **compiler for prompt programs**, not a chain or RAG framework. You write Python programs with typed signatures and DSPy optimizes the prompts automatically.

> **⚠️ DSPy is NOT a chain framework.** It does not use `prompt | model | parser`. It does not have LCEL. DSPy operates at a different layer: you define a program with Python control flow and typed signatures, then the *compiler* optimizes the prompts against a metric. If you reach for DSPy expecting LangChain-style composition, you are reaching for the wrong tool.

Think of it as PyTorch for LMs — you define the architecture, the compiler tunes the weights (prompts).

## Core Paradigm

> Read this first. It is the most important thing to understand about DSPy.

```python
import dspy

# 1. Configure the LM
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

# 2. Define a signature (input/output schema)
class QASignature(dspy.Signature):
    """Answer questions concisely."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

# 3. Build a program using modules
qa = dspy.ChainOfThought(QASignature)

# 4. Compile against a metric
optimizer = dspy.MIPROv2(metric=dspy.answer_exact_match)
compiled_qa = optimizer.compile(qa, trainset=trainset, num_trials=25)

# 5. Use the compiled program (portable artifact)
answer = compiled_qa(question="What is DSPy?").answer
```

## Core Principles

1. **DSPy is a compiler, not a chain framework.** You define the program structure with Python control flow and typed signatures. The compiler optimizes the prompts. This is fundamentally different from LangChain's explicit prompt composition.

2. **Signatures define the task.** Input/output field pairs with optional descriptions are the task definition. The syntax is `input1, input2 -> output1, output2`.

3. **Modules are program components.** `dspy.Predict` (direct), `dspy.ChainOfThought` (reasoning), `dspy.ReAct` (tool-use), and custom `dspy.Module` subclasses. Compose them with Python control flow (if/for/while).

4. **Optimizers tune prompts, not weights.** A dozen optimizers (teleprompters) tune instructions, few-shot demos, or both. Selection depends on bottleneck and budget. See the optimizer cheat sheet.

5. **Compile once, serve many.** Compilation is expensive ($3-$300+). The output is a portable artifact via `program.save(path)`. Inference is cheap.

6. **Cache aggressively.** DSPy caches all LM calls by default. Set `DSPY_CACHEDIR` for the current client. Disable with `dspy.LM(..., cache=False)`.

## Where to Start

| You already have... | Start here |
|---|---|
| Nothing — exploring DSPy | Understand the paradigm (read this page first), then build a simple Predict program |
| A working prompt you want to optimize | Port to a DSPy Signature, add ChainOfThought, compile with BootstrapFewShot |
| A multi-step pipeline | Build as a custom dspy.Module with Python control flow, compile with MIPROv2 |
| An agent/tool-use task | Use dspy.ReAct with tools, compile with GEPA or AvatarOptimizer |
| Comparing frameworks | See the Framework Routing Guide |

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Basic prediction | `dspy.Predict(signature)` | `references/core-modules.md` |
| With reasoning | `dspy.ChainOfThought(signature)` | `references/core-modules.md` |
| With tools | `dspy.ReAct(tools=tools)` | `references/agent-patterns.md` |
| Custom program | `class MyProgram(dspy.Module)` | `references/program-patterns.md` |
| Quick optimization | `dspy.BootstrapFewShot(metric)` | `references/optimizer-guide.md` |
| Full optimization | `dspy.MIPROv2(metric, auto="medium")` | `references/optimizer-guide.md` |
| Evaluation | `dspy.Evaluate(metric=fn, devset=examples)` | `references/evaluation.md` |
| Save/load | `program.save(path)` / `program.load(path)` | `references/compilation-guide.md` |
| Retrieval | `dspy.Retrieve(k=5)` | `references/program-patterns.md` |

## Framework Routing Guide

| Scenario | Reach for | Why |
|----------|-----------|-----|
| Prompt optimization / compiled programs | **DSPy** | Only framework that auto-optimizes prompts against a metric |
| Documents to query / RAG | **LlamaIndex** | Data ingestion and retrieval are first-class primitives |
| Chain/agent composition | **LangChain** | LCEL is the cleanest pipe-based composition model |
| State-machine multi-agent | **LangGraph** | Graph topology, subgraphs, human-in-the-loop |
| Search pipelines | **Haystack** | Pipeline model is more mature for search workloads |
| Role-based teams | **CrewAI** | Higher-level agent abstraction |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Core Modules | Building with Predict, ChainOfThought, ReAct | `references/core-modules.md` |
| Optimizer Guide | Choosing and configuring an optimizer | `references/optimizer-guide.md` |
| Program Patterns | RAG, classification, multi-step, tool-use | `references/program-patterns.md` |
| Evaluation | Metrics, evaluation loop, dataset creation | `references/evaluation.md` |
| Compilation Guide | Caching, cost management, save/load | `references/compilation-guide.md` |
| Agent Patterns | ReAct agent, tool-use, AvatarOptimizer | `references/agent-patterns.md` |
| FAQ & Troubleshooting | Common errors and fixes | `references/faq-and-troubleshooting.md` |
| Validation Audit | Research validation of all API claims | `references/validation-audit.md` |
| Worked RAG Example | Full RAG compilation with expected output | `references/example-rag-compilation.md` |

## Template Files

| Template | When to use | File |
|----------|-------------|------|
| Classification | Text classification with BootstrapFewShot | `templates/classification.py` |
| RAG Program | RAG with ColBERT retrieval and ChainOfThought | `templates/rag-program.py` |
| Multi-Step Reasoning | Multi-step program with tool-use | `templates/multi-step.py` |

## Scripts

| Script | Purpose | File |
|--------|---------|------|
| check-setup | Verify DSPy installation and configuration | `scripts/check-setup.py` |

## Troubleshooting

| Symptom | Likely cause | Fix | Reference |
|---------|-------------|-----|-----------|
| Compilation too slow | Too many candidates/threads | Reduce `num_candidates` or use `auto="light"` | `references/optimizer-guide.md` |
| Compilation too expensive | No caching | Enable DSPY_CACHEDIR | `references/compilation-guide.md` |
| Context too long | Too many demos | Reduce `max_bootstrapped_demos` and `max_labeled_demos` | `references/faq-and-troubleshooting.md` |
| Low quality after compile | Wrong optimizer for bottleneck | Check cheat sheet: instructions vs demos vs weights | `references/optimizer-guide.md` |
| Program is not improving | Metric not discriminating | Use a metric that returns float, not bool | `references/evaluation.md` |
| Sub-module not updating | _compiled flag set | Set `module._compiled = False` before recompiling | `references/compilation-guide.md` |

## When NOT to Use DSPy

- Simple single-prompt application — raw API calls are simpler
- Need pre-built application modules (PDF Q&A, text-to-SQL) — use LlamaIndex or LangChain
- One-shot task with no optimization budget — DSPy's compiler overhead won't amortize
- Real-time latency-critical — compilation happens at development time but adds no inference overhead
