---
name: prompt-reasoning-and-chaining
description: Load when the task requires multi-step reasoning (chain-of-thought) or when a complex workflow should be decomposed into sequential LLM calls (prompt chaining). Covers CoT levels, structured reasoning, reasoning model caveats, chaining patterns, inter-step validation, error propagation, and shared concept alignment.
---

# Prompt Reasoning and Chaining

Detailed techniques for multi-step reasoning within a single prompt and decomposition across multiple prompts.

---

## 1. Chain of Thought (CoT)

Instruct the model to reason step-by-step before giving a final answer. Significantly improves accuracy on math, logic, multi-constraint, and analytical tasks.

**When to use:** Tasks where a human would need to think through the problem. Skip for simple lookups or straightforward generation — CoT adds latency and tokens for no benefit on easy tasks.

**Three levels:**

| Level | Instruction | Tradeoff |
|-------|------------|----------|
| Basic | "Think step by step." | Easy, but reasoning is unstructured |
| Guided | "First do X, then consider Y, finally decide Z." | More reliable, still mixes reasoning with answer |
| Structured | Use tags to separate reasoning from answer | Best — reasoning is cleanly separated from output |

**Structured CoT template:**
```
Analyze this problem step by step.

Write your reasoning inside <reasoning> tags.
Write only your final answer inside <answer> tags.
```

**Concrete example — eligibility checking:**
```
# Weak — model jumps to conclusion, frequently errs on edge cases
Is this applicant eligible for a senior discount?
Applicant: age 63, annual income $34,000, loyalty member since 2019.
Eligibility rules: age ≥ 65 OR (age ≥ 60 AND loyalty member ≥ 5 years AND income < $40,000).

# Strong — forces the model to work through each condition
Is this applicant eligible for a senior discount?
Applicant: age 63, annual income $34,000, loyalty member since 2019.
Eligibility rules: age ≥ 65 OR (age ≥ 60 AND loyalty member ≥ 5 years AND income < $40,000).

Work through each condition in <reasoning> tags, then give your final decision in <answer> tags.
```

**Critical rule:** The model must *output* its reasoning. If you instruct it to "think" but don't give it a place to write the thinking, performance doesn't improve. Reasoning that isn't generated doesn't happen.

**Reasoning models caveat:** Models with built-in reasoning (OpenAI o-series, Claude with extended thinking, Gemini thinking mode) perform internal CoT. Adding explicit CoT to these models is redundant and can hurt — the model reasons internally, then your prompt asks it to reason again, leading to wasted tokens and sometimes conflicting logic. When using reasoning models, give the task directly.

---

## 2. Prompt Chaining

Break complex tasks into sequential subtasks, each handled by a separate prompt. Output of step N becomes input to step N+1.

**When to use:** Multi-step workflows where a single prompt leads to skipped steps, inconsistent quality, or exceeds reliable attention span. Also useful when different steps benefit from different models.

**Principles:**
- Each step should have a single, clear objective.
- Pass structured output (JSON, XML) between steps for clean handoffs.
- Independent subtasks can run in parallel.
- Add a verification step at the end for high-stakes tasks (generate → review → refine).

**Common patterns:**
- Extract → Transform → Validate
- Research → Outline → Draft → Edit
- Generate → Self-critique → Revise
- Classify → Route → Handle (for agent architectures)

**Concrete example — Extract → Classify → Draft:**
```python
# Step 1: Extract (single, focused objective)
step1_prompt = """
Extract every distinct complaint from the support ticket below.
Output a JSON array of strings, one per complaint. Output nothing else.

<ticket>{{ticket_text}}</ticket>
"""
complaints = json.loads(call_llm(step1_prompt))

# Step 2: Classify (receives structured output from step 1)
step2_prompt = f"""
Classify each complaint below into exactly one category:
authentication, performance, billing, other.
Output a JSON array of objects with "complaint" and "category" fields. Output nothing else.

<complaints>{json.dumps(complaints)}</complaints>
"""
classified = json.loads(call_llm(step2_prompt))

# Step 3: Draft response (receives structured output from step 2)
step3_prompt = f"""
You are a customer support agent. Draft a concise, empathetic reply
addressing each classified issue directly.

<issues>{json.dumps(classified)}</issues>
"""
reply = call_llm(step3_prompt)
```

### Error Propagation and Inter-Step Resilience

In real pipelines, step N can produce malformed or subtly wrong output that silently corrupts step N+1.

**Validate between steps** — Parse and schema-validate after each step. If step 1 should produce a JSON array and returns a markdown list, catch it immediately.

**Retry with feedback** — When validation fails, retry the failed step with the error appended: "Your previous output was invalid: [error]. Produce valid output matching this schema: [schema]." Cap retries at 2–3.

**Design downstream steps to be resilient:**
```
The input below was produced by a prior processing step and may contain
errors or missing fields. If a field is missing or malformed, note it
and proceed with what is available rather than fabricating data.
```

### Shared Concept Alignment

If multiple chained calls reference the same domain concepts (e.g., "lead", "qualified"), every prompt in the chain must define those terms identically. Each LLM call is stateless — it doesn't inherit understanding from a prior call.

Extract shared definitions into a common preamble block and inject it into every step that needs it.
