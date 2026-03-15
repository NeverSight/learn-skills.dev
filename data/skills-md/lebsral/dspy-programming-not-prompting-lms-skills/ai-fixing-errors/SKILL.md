---
name: ai-fixing-errors
description: Fix broken AI features. Use when your AI is throwing errors, producing wrong outputs, crashing, returning garbage, not responding, or behaving unexpectedly. Covers DSPy debugging, error diagnosis, and troubleshooting.
---

# Fix Your Broken AI

Systematic approach to diagnosing and fixing AI features that aren't working. Run through these checks in order.

## Quick Diagnostic Checklist

### 1. Is the AI provider configured?

```python
import dspy

# Check current config
print(dspy.settings.lm)  # Should show your LM, not None

# If None, configure it:
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)
```

**Common issues:**
- Forgot to call `dspy.configure(lm=lm)`
- API key not set in environment
- Wrong model name format (should be `provider/model-name`)

### 2. Does the AI respond at all?

```python
# Test the AI provider directly
lm = dspy.LM("openai/gpt-4o-mini")
response = lm("Hello, respond with just 'OK'")
print(response)
```

### 3. Is the task definition correct?

```python
# Check your signature defines the right fields
class MySignature(dspy.Signature):
    """Clear task description here."""
    input_field: str = dspy.InputField(desc="what this contains")
    output_field: str = dspy.OutputField(desc="what to produce")

# Verify by inspecting
print(MySignature.fields)
```

**Common issues:**
- Missing `dspy.InputField()` / `dspy.OutputField()` annotations
- Wrong type hints (use `str`, `list[str]`, `Literal[...]`, Pydantic models)
- Vague or missing docstring (the docstring IS the task instruction)

### 4. Are you passing the right inputs?

```python
# Check that input field names match
result = my_program(question="test")  # field name must match signature

# Wrong:
result = my_program(q="test")  # 'q' doesn't match 'question'
result = my_program("test")    # positional args don't work
```

### 5. Is the output being parsed?

```python
result = my_program(question="test")
print(result)                    # see all fields
print(result.answer)             # access specific field
print(type(result.answer))       # check type
```

**Common issues with typed outputs:**
- `Literal` type doesn't match any of the provided options
- Pydantic model validation fails
- List output returns string instead of list

## Inspect What the AI Actually Sees

The most powerful debugging tool — shows exactly what prompts were sent and what came back:

```python
# Show the last 3 AI calls
dspy.inspect_history(n=3)
```

This shows:
- The full prompt sent to the AI
- The AI's raw response
- How DSPy parsed the response

**What to look for:**
- Is the prompt clear? Does it describe the task well?
- Is the AI's response in the expected format?
- Are few-shot examples (if any) helpful or misleading?

## Common Errors and Fixes

### `AttributeError: 'NoneType' has no attribute ...`
**Cause:** AI provider not configured.
**Fix:** Call `dspy.configure(lm=lm)` before using any module.

### `ValueError: Could not parse output`
**Cause:** AI output doesn't match expected format.
**Fix:**
- Check `dspy.inspect_history()` to see what the AI returned
- Simplify your output types
- Add clearer field descriptions
- Use `dspy.ChainOfThought` instead of `dspy.Predict` (reasoning helps formatting)

### `TypeError: forward() got an unexpected keyword argument`
**Cause:** Input field name mismatch.
**Fix:** Make sure you're passing keyword arguments that match your signature's `InputField` names.

### Search/retriever returns empty results
**Cause:** Retriever not configured or wrong endpoint.
**Fix:**
```python
# Check retriever config
print(dspy.settings.rm)

# Test retriever directly
rm = dspy.ColBERTv2(url="http://...")
results = rm("test query", k=3)
print(results)
```

### Optimizer makes things worse
**Cause:** Bad metric, too little data, or overfitting.
**Fix:**
- Manually verify your metric on 10-20 examples
- Add more training data
- Reduce `max_bootstrapped_demos`
- Use a validation set to check for overfitting

### `dspy.Assert` / `dspy.Suggest` failures
**Cause:** AI output doesn't meet constraints.
**Fix:**
- Check if constraints are reasonable (not too strict)
- Make constraint messages more descriptive
- Ensure the AI can reasonably satisfy the constraints

## Advanced Debugging

### Enable verbose tracing

```python
dspy.configure(lm=lm, trace=[])
# Now run your program — trace will be populated
result = my_program(question="test")
```

### Inspect module structure

```python
# Print the module tree
print(my_program)

# See all named predictors
for name, predictor in my_program.named_predictors():
    print(f"{name}: {predictor}")
```

### Test individual components

Break your pipeline into pieces and test each one:

```python
class MyPipeline(dspy.Module):
    def __init__(self):
        self.step1 = dspy.ChainOfThought("question -> search_query")
        self.step2 = dspy.Retrieve(k=3)
        self.step3 = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        query = self.step1(question=question)
        print(f"Step 1 output: {query.search_query}")  # Debug

        context = self.step2(query.search_query)
        print(f"Step 2 retrieved: {len(context.passages)} passages")  # Debug

        answer = self.step3(context=context.passages, question=question)
        print(f"Step 3 output: {answer.answer}")  # Debug

        return answer
```

### Compare prompts before/after optimization

```python
# Before optimization
baseline = MyProgram()
baseline(question="test")
print("=== BASELINE PROMPT ===")
dspy.inspect_history(n=1)

# After optimization
optimized = MyProgram()
optimized.load("optimized.json")
optimized(question="test")
print("=== OPTIMIZED PROMPT ===")
dspy.inspect_history(n=1)
```

## Additional resources

- For complete error index, see [reference.md](reference.md)
- To measure and improve accuracy, use `/ai-improving-accuracy`
- Use `/ai-tracing-requests` to trace a specific request end-to-end (every LM call, retrieval, latency)
- For DSPy API details, see `docs/dspy-reference.md`
