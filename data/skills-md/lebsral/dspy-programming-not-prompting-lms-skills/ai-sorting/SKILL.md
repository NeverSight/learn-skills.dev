---
name: ai-sorting
description: Auto-sort, categorize, or label content using AI. Use when sorting tickets into categories, auto-tagging content, labeling emails, detecting sentiment, routing messages to the right team, triaging support requests, building a spam filter, intent detection, topic classification, or any task where text goes in and a category comes out.
---

# Build an AI Content Sorter

Guide the user through building an AI that sorts, tags, or categorizes content. Powered by DSPy classification — works with any label set.

## Step 1: Define the sorting task

Ask the user:
1. **What are you sorting?** (tickets, emails, reviews, messages, etc.)
2. **What are the categories?** (list all labels/buckets)
3. **One category per item, or multiple?** (e.g., "priority" vs "all applicable tags")

## Step 2: Build the sorter

### Single category (most common)

```python
import dspy
from typing import Literal

# Your categories
CATEGORIES = ["billing", "technical", "account", "feature_request", "general"]

class SortContent(dspy.Signature):
    """Sort the message into the correct category."""
    message: str = dspy.InputField(desc="The content to sort")
    category: Literal[tuple(CATEGORIES)] = dspy.OutputField(desc="The assigned category")

sorter = dspy.ChainOfThought(SortContent)
```

Using `Literal` locks the output to valid categories only — the AI can't hallucinate labels. `ChainOfThought` adds reasoning which improves accuracy over bare `Predict`.

### Multiple tags

```python
class TagContent(dspy.Signature):
    """Assign all applicable tags to the content."""
    message: str = dspy.InputField(desc="The content to tag")
    tags: list[Literal[tuple(CATEGORIES)]] = dspy.OutputField(desc="All applicable tags")

tagger = dspy.ChainOfThought(TagContent)
```

## Step 3: Test the quality

```python
from dspy.evaluate import Evaluate

def sorting_metric(example, prediction, trace=None):
    return prediction.category == example.category

evaluator = Evaluate(
    devset=devset,
    metric=sorting_metric,
    num_threads=4,
    display_progress=True,
    display_table=5,
)
score = evaluator(sorter)
```

For multi-tag, use F1 or Jaccard similarity instead of exact match.

## Step 4: Improve accuracy

Start with `BootstrapFewShot` — fast and usually gives a solid boost:

```python
optimizer = dspy.BootstrapFewShot(
    metric=sorting_metric,
    max_bootstrapped_demos=4,
)
optimized_sorter = optimizer.compile(sorter, trainset=trainset)
```

If accuracy still isn't good enough, upgrade to `MIPROv2`:

```python
optimizer = dspy.MIPROv2(
    metric=sorting_metric,
    auto="medium",
)
optimized_sorter = optimizer.compile(sorter, trainset=trainset)
```

## Step 5: Use it

```python
result = optimized_sorter(message="I was charged twice on my credit card last month")
print(f"Category: {result.category}")
print(f"Reasoning: {result.reasoning}")
```

## Key patterns

- **Use `Literal` types** to lock outputs to valid categories
- **Use `ChainOfThought`** over `Predict` — reasoning improves sorting accuracy
- **Include a `hint` field** during training for tricky examples:
  ```python
  class SortWithHint(dspy.Signature):
      message: str = dspy.InputField()
      hint: str = dspy.InputField(desc="Optional hint for ambiguous cases")
      category: Literal[tuple(CATEGORIES)] = dspy.OutputField()
  ```
  Set `hint` in training data, leave empty at inference time.
- **Confidence scores**: Add a float output field if you need confidence

## Additional resources

- For worked examples (sentiment, intent, topics), see [examples.md](examples.md)
- Need scores instead of categories? Use `/ai-scoring`
- Next: `/ai-improving-accuracy` to measure and improve your AI
