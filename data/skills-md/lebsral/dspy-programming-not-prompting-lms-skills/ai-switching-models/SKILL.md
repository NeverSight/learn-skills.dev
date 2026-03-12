---
name: ai-switching-models
description: Switch AI providers or models without breaking things. Use when you want to switch from OpenAI to Anthropic, try a cheaper model, stop depending on one vendor, compare models side-by-side, a model update broke your outputs, you need vendor diversification, or you want to migrate to a local model. Covers DSPy model portability — provider config, re-optimization, model comparison, and multi-model pipelines.
---

# Switch Models Without Breaking Things

Guide the user through switching AI models or providers safely. The key insight: optimized prompts don't transfer between models (arxiv 2402.10949v2 — "The Unreasonable Effectiveness of Eccentric Automatic Prompts"). DSPy solves this by separating your task definition (signatures + modules) from model-specific prompts (compiled by optimizers).

## Why switching models breaks things

Hand-tuned prompts are model-specific. A prompt engineered for GPT-4o will perform differently on Claude, Llama, or even GPT-4o-mini. Research shows optimized prompts for one model can actually *hurt* performance on another.

DSPy makes switching safe because:
- **Signatures** define *what* the task is (inputs, outputs, types) — model-independent
- **Modules** define *how* to solve it (chain of thought, ReAct, etc.) — model-independent
- **Compiled prompts** (few-shot examples, instructions) are model-specific — but re-generated automatically by optimizers

**The workflow:** keep your program the same, swap the model, re-optimize. Done.

## When to switch models

- **Cost reduction** — "GPT-4o is too expensive, can we use something cheaper?"
- **New model release** — "A better model just came out, let's try it"
- **Vendor diversification** — "We can't depend on one provider"
- **Data privacy / compliance** — "We need to run models on our own infrastructure"
- **Performance regression** — "The provider updated their model and our outputs got worse"
- **Capability needs** — "We need better code generation / longer context / faster responses"

## Step 1: Configure any provider

DSPy uses [LiteLLM](https://docs.litellm.ai/docs/providers) under the hood, so you can use any supported provider with a simple string:

```python
import dspy

# OpenAI
lm = dspy.LM("openai/gpt-4o")
lm = dspy.LM("openai/gpt-4o-mini")

# Anthropic
lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929")
lm = dspy.LM("anthropic/claude-haiku-4-5-20251001")

# Azure OpenAI
lm = dspy.LM("azure/my-gpt4-deployment")

# Google
lm = dspy.LM("gemini/gemini-2.0-flash")

# Together AI (open-source models)
lm = dspy.LM("together_ai/meta-llama/Llama-3-70b-chat-hf")

# Local models (via Ollama)
lm = dspy.LM("ollama_chat/llama3.1", api_base="http://localhost:11434")

# Any OpenAI-compatible server (vLLM, TGI, etc.)
lm = dspy.LM("openai/my-model", api_base="http://localhost:8000/v1", api_key="none")

dspy.configure(lm=lm)
```

### Environment variables

Set API keys as environment variables — don't hardcode them:

```bash
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
TOGETHER_API_KEY=...
AZURE_API_KEY=...
AZURE_API_BASE=https://your-resource.openai.azure.com/
```

See [LiteLLM provider docs](https://docs.litellm.ai/docs/providers) for the full list of 100+ supported providers.

## Step 2: Benchmark your current model

Before changing anything, measure your baseline. You need a metric and test data.

```python
from dspy.evaluate import Evaluate

# Your existing program and metric
program = MyProgram()
program.load("current_optimized.json")  # load your production prompts

evaluator = Evaluate(
    devset=devset,
    metric=metric,
    num_threads=4,
    display_progress=True,
    display_table=5,
)

# Benchmark with your current model
current_lm = dspy.LM("openai/gpt-4o")
dspy.configure(lm=current_lm)
baseline_score = evaluator(program)
print(f"Current model baseline: {baseline_score:.1f}%")
```

If you don't have a metric or test data yet, use `/ai-improving-accuracy` to set them up first.

## Step 3: Try the new model (quick test)

Swap the model and run your evaluation *without* re-optimizing. This demonstrates the problem — your old prompts don't transfer.

```python
# Try the new model with your OLD optimized prompts
new_lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929")
dspy.configure(lm=new_lm)

naive_score = evaluator(program)
print(f"Old model (optimized):  {baseline_score:.1f}%")
print(f"New model (old prompts): {naive_score:.1f}%")
print(f"Drop: {baseline_score - naive_score:.1f}%")
```

You'll typically see a quality drop — this is expected. The optimized prompts were tuned for the old model.

## Step 4: Re-optimize for the new model

Now re-optimize your program for the new model. Use the same signatures and modules — only the compiled prompts change.

```python
# Configure the new model
new_lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929")
dspy.configure(lm=new_lm)

# Start from a fresh (unoptimized) program
fresh_program = MyProgram()

# Re-optimize for the new model
optimizer = dspy.MIPROv2(metric=metric, auto="medium")
optimized_for_new = optimizer.compile(fresh_program, trainset=trainset)

# Evaluate
reoptimized_score = evaluator(optimized_for_new)
print(f"Old model (optimized):      {baseline_score:.1f}%")
print(f"New model (old prompts):     {naive_score:.1f}%")
print(f"New model (re-optimized):    {reoptimized_score:.1f}%")
```

The re-optimized score should recover most or all of the quality. If it doesn't, either:
- The new model genuinely can't handle this task as well
- Try a heavier optimization (`auto="heavy"`)
- Try BootstrapFewShot first for a quick sanity check

### Quick re-optimization (fast test)

For a quick check before committing to a full MIPROv2 run:

```python
optimizer = dspy.BootstrapFewShot(
    metric=metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
)
quick_optimized = optimizer.compile(fresh_program, trainset=trainset)
quick_score = evaluator(quick_optimized)
```

## Step 5: Compare models systematically

Loop over candidate models, optimize each, and build a comparison table:

```python
candidates = [
    ("openai/gpt-4o", "GPT-4o"),
    ("openai/gpt-4o-mini", "GPT-4o-mini"),
    ("anthropic/claude-sonnet-4-5-20250929", "Claude Sonnet"),
    ("together_ai/meta-llama/Llama-3-70b-chat-hf", "Llama 3 70B"),
]

results = []
for model_id, label in candidates:
    lm = dspy.LM(model_id)
    dspy.configure(lm=lm)

    # Optimize for this model
    fresh = MyProgram()
    optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
    optimized = optimizer.compile(fresh, trainset=trainset)

    # Evaluate
    score = evaluator(optimized)

    # Save the optimized program
    optimized.save(f"optimized_{label.lower().replace(' ', '_')}.json")

    results.append({"model": label, "score": score})
    print(f"{label}: {score:.1f}%")

# Print comparison table
print("\n--- Model Comparison ---")
print(f"{'Model':<25} {'Score':>8}")
print("-" * 35)
for r in sorted(results, key=lambda x: x["score"], reverse=True):
    print(f"{r['model']:<25} {r['score']:>7.1f}%")
```

For a more thorough comparison with MIPROv2 and cost/latency tracking, see [examples.md](examples.md).

## Step 6: Mix models in one pipeline

You don't have to use one model for everything. Assign different models to different steps — cheap for simple tasks, expensive for hard ones.

### Using `dspy.context` (temporary, per-call)

```python
cheap_lm = dspy.LM("openai/gpt-4o-mini")
expensive_lm = dspy.LM("openai/gpt-4o")

dspy.configure(lm=expensive_lm)  # default

class MyPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict(ClassifySignature)
        self.generate = dspy.ChainOfThought(GenerateSignature)

    def forward(self, text):
        # Cheap model for simple classification
        with dspy.context(lm=cheap_lm):
            category = self.classify(text=text)

        # Expensive model for complex generation
        return self.generate(text=text, category=category.label)
```

### Using `set_lm` (permanent, per-module)

```python
pipeline = MyPipeline()
pipeline.classify.set_lm(cheap_lm)
pipeline.generate.set_lm(expensive_lm)
```

See `/ai-cutting-costs` for more cost optimization patterns with per-module LM assignment.

## Step 7: Save and deploy

Save a separate optimized program for each model you might use in production:

```python
# Save per-model optimized programs
optimized_gpt4o.save("optimized_gpt4o.json")
optimized_claude.save("optimized_claude.json")
optimized_llama.save("optimized_llama.json")

# In production — load the right one
import os

model_name = os.environ.get("AI_MODEL", "openai/gpt-4o")
lm = dspy.LM(model_name)
dspy.configure(lm=lm)

program = MyProgram()
program.load(f"optimized_{model_name.split('/')[-1]}.json")
```

## Common scenarios

### GPT-4o to GPT-4o-mini (cost reduction)

1. Benchmark GPT-4o baseline (Step 2)
2. Try GPT-4o-mini with old prompts — see the drop (Step 3)
3. Re-optimize for GPT-4o-mini with MIPROv2 (Step 4)
4. Compare scores — if quality is close enough, ship it

### OpenAI to Anthropic (vendor diversification)

1. Set up Anthropic API key in environment
2. Change model string: `"openai/gpt-4o"` to `"anthropic/claude-sonnet-4-5-20250929"`
3. Re-optimize — different models need different prompts
4. Keep both optimized programs, switch via environment variable

### Cloud to local (data privacy)

1. Set up local model server (Ollama, vLLM, or TGI)
2. Point DSPy at it: `dspy.LM("ollama_chat/llama3.1", api_base="http://localhost:11434")`
3. Re-optimize — local models especially need re-optimization
4. Expect some quality trade-off vs large cloud models; use heavier optimization

### Model version update broke things

When a provider updates their model (e.g., GPT-4o version bump):
1. Run your evaluation to confirm the regression
2. Re-optimize against the updated model
3. Save the new optimized program
4. This is why having evaluation + optimization in your workflow matters — version updates become routine, not emergencies

## Checklist

1. Set up evaluation and metric *before* switching (use `/ai-improving-accuracy`)
2. Benchmark your current model
3. Try the new model with old prompts (expect a drop)
4. Re-optimize for the new model
5. Compare scores — decide if the trade-off is acceptable
6. Save per-model optimized programs
7. Deploy with model selection via environment variable

## Additional resources

- For worked examples (cost migration, vendor switch, model shootout), see [examples.md](examples.md)
- Use `/ai-improving-accuracy` to set up metrics and evaluation before switching
- Use `/ai-cutting-costs` for per-module model assignment and cost optimization
- Use `/ai-building-pipelines` for multi-step pipelines with mixed models
- Use `/ai-fine-tuning` to distill from an expensive model to a cheap one
