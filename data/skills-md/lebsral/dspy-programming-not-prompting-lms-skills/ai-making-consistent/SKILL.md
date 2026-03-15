---
name: ai-making-consistent
description: Make your AI give the same answer every time. Use when AI gives different answers to the same question, outputs are unpredictable, responses vary between runs, you need deterministic AI behavior, or your AI is unreliable. Covers DSPy consistency techniques — temperature, typed outputs, assertions, and optimization.
---

# Make Your AI Consistent

Guide the user through making their AI give reliable, predictable outputs. This is different from "wrong answers" — the AI might be right 80% of the time but unpredictably different each run.

## Step 1: Diagnose the inconsistency

Ask the user:
1. **What's varying?** (the answer itself, the format, the length, the level of detail?)
2. **How bad is it?** (slightly different wording vs. completely different answers)
3. **Does it matter for your use case?** (sometimes variation is fine, sometimes it breaks downstream code)

### Quick test: run the same input 5 times

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

for i in range(5):
    result = my_program(question="What is the capital of France?")
    print(f"Run {i+1}: {result.answer}")
```

If outputs vary, apply the fixes below in order.

## Step 2: Set temperature to 0

The single biggest consistency fix. Temperature controls randomness — set it to 0 for deterministic outputs:

```python
lm = dspy.LM("openai/gpt-4o-mini", temperature=0)
dspy.configure(lm=lm)
```

This alone fixes most consistency issues. Some providers may still have slight variation even at temperature=0 due to floating point non-determinism, but it's minimal.

## Step 3: Constrain output types

Loose output types = more room for variation. Lock them down.

### Use `Literal` for fixed categories

```python
from typing import Literal

class Classify(dspy.Signature):
    """Classify the text."""
    text: str = dspy.InputField()
    # BAD: label: str — AI can say "positive", "Positive", "pos", "POSITIVE", etc.
    # GOOD: locked to exact values
    label: Literal["positive", "negative", "neutral"] = dspy.OutputField()
```

### Use Pydantic models for structured output

```python
from pydantic import BaseModel, Field

class StructuredOutput(BaseModel):
    category: str
    confidence: float = Field(ge=0.0, le=1.0)
    tags: list[str]

class MySignature(dspy.Signature):
    """Process the input."""
    text: str = dspy.InputField()
    result: StructuredOutput = dspy.OutputField()
```

Pydantic validates the output structure, catching format inconsistencies.

### Use `bool` and `int` for simple outputs

```python
class CheckFact(dspy.Signature):
    """Is this statement true?"""
    statement: str = dspy.InputField()
    is_true: bool = dspy.OutputField()  # Only True or False — no variation
```

## Step 4: Add output constraints with assertions

Use `dspy.Assert` for hard requirements and `dspy.Suggest` for soft preferences:

```python
class ConsistentResponder(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(MySignature)

    def forward(self, text):
        result = self.respond(text=text)

        # Hard constraint — retry if violated
        dspy.Assert(
            len(result.answer) < 200,
            "Answer must be under 200 characters"
        )

        # Soft constraint — hint to improve
        dspy.Suggest(
            result.answer.endswith("."),
            "Answer should end with a period"
        )

        return result
```

### Common consistency assertions

```python
# Length constraints
dspy.Assert(len(result.answer.split()) <= 50, "Keep answer under 50 words")

# Format constraints
dspy.Assert(result.answer[0].isupper(), "Answer should start with a capital letter")

# Content constraints
dspy.Assert(
    not any(word in result.answer.lower() for word in ["maybe", "perhaps", "i think"]),
    "Answer should be definitive, not hedging"
)
```

## Step 5: Optimize to lock in patterns

Optimization teaches the AI consistent patterns through examples. Even a simple `BootstrapFewShot` run dramatically improves consistency:

```python
# The few-shot examples teach the AI what "good" looks like,
# including format, length, and style
optimizer = dspy.BootstrapFewShot(
    metric=metric,
    max_bootstrapped_demos=4,
)
optimized = optimizer.compile(my_program, trainset=trainset)
```

For best consistency, make your metric penalize inconsistency:

```python
def consistency_metric(example, prediction, trace=None):
    correct = prediction.answer.lower() == example.answer.lower()
    # Penalize answers that are too long or too short
    right_length = 5 <= len(prediction.answer.split()) <= 30
    # Penalize hedging language
    no_hedging = not any(w in prediction.answer.lower() for w in ["maybe", "perhaps"])
    return correct and right_length and no_hedging
```

## Step 6: Use caching for identical inputs

DSPy caches LM calls by default. For identical inputs, you'll always get the same output:

```python
# First call — hits the API
result1 = my_program(question="What is Python?")

# Second call with same input — returns cached result (instant, identical)
result2 = my_program(question="What is Python?")

# result1 and result2 are guaranteed identical
```

## Consistency checklist

1. Set `temperature=0`
2. Use `Literal` types for categorical outputs
3. Use Pydantic models for structured outputs
4. Use `bool`/`int` for simple yes/no or numeric outputs
5. Add `dspy.Assert` for format constraints
6. Optimize with BootstrapFewShot to lock in patterns
7. Rely on caching for repeated identical inputs

## Additional resources

- If the AI is consistent but *wrong*, use `/ai-improving-accuracy`
- If the AI is throwing errors, use `/ai-fixing-errors`
