---
name: ai-stopping-hallucinations
description: Stop your AI from making things up. Use when your AI hallucinates, fabricates facts, isn't grounded in real data, doesn't cite sources, makes unsupported claims, or you need to verify AI responses against source material. Covers citation enforcement, faithfulness verification, grounding via retrieval, and confidence thresholds.
---

# Stop Your AI From Making Things Up

Guide the user through making their AI factually grounded. The core principle: never trust a bare LM output — always verify against sources.

## Why AI hallucinates

LMs generate plausible-sounding text, not verified facts. Hallucination happens when:
- The model has no source material to ground its answer
- The prompt doesn't enforce citations or evidence
- There's no verification step after generation
- Temperature is too high for factual tasks

The fix isn't better prompting — it's **programmatic constraints** that force grounding.

## Step 1: Understand the grounding situation

Ask the user:
1. **Do you have source documents?** (knowledge base, docs, database) → use retrieval-grounded answers
2. **Is it general knowledge?** (no docs, just the model's knowledge) → use self-consistency checks
3. **How bad is a hallucination?** (annoying vs. dangerous) → determines how strict the checks should be

## Step 2: Citation enforcement

Force the AI to cite sources for every claim. Uses `dspy.Assert` to reject answers without citations.

```python
import dspy
import re

class CitedAnswer(dspy.Signature):
    """Answer the question using the provided sources. Cite every claim with [1], [2], etc."""
    context: list[str] = dspy.InputField(desc="Numbered source documents")
    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="Answer with inline citations like [1], [2]")

class CitationEnforcer(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought(CitedAnswer)

    def forward(self, context, question):
        result = self.answer(context=context, question=question)

        # Every 1-2 sentences must have a citation
        sentences = [s.strip() for s in result.answer.split(".") if s.strip()]
        citations_found = [bool(re.search(r"\[\d+\]", s)) for s in sentences]

        # Check that at least half the sentences have citations
        citation_ratio = sum(citations_found) / max(len(sentences), 1)
        dspy.Assert(
            citation_ratio >= 0.5,
            "Answer must cite sources. Use [1], [2], etc. after claims. "
            f"Only {citation_ratio:.0%} of sentences have citations."
        )

        # Check that cited numbers actually exist in the context
        cited_nums = set(int(n) for n in re.findall(r"\[(\d+)\]", result.answer))
        valid_nums = set(range(1, len(context) + 1))
        invalid = cited_nums - valid_nums
        dspy.Assert(
            len(invalid) == 0,
            f"Citations {invalid} don't match any source. Valid sources: [1] to [{len(context)}]."
        )

        return result
```

## Step 3: Faithfulness verification

After generating an answer, use a second LM call to check if it's actually supported by the sources.

```python
class CheckFaithfulness(dspy.Signature):
    """Check if every claim in the answer is supported by the context."""
    context: list[str] = dspy.InputField(desc="Source documents")
    answer: str = dspy.InputField(desc="Generated answer to verify")
    is_faithful: bool = dspy.OutputField(desc="Is every claim supported by the context?")
    unsupported_claims: list[str] = dspy.OutputField(desc="Claims not found in context")

class FaithfulResponder(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=5)
        self.answer = dspy.ChainOfThought(CitedAnswer)
        self.verify = dspy.Predict(CheckFaithfulness)

    def forward(self, question):
        context = self.retrieve(question).passages
        result = self.answer(context=context, question=question)

        check = self.verify(context=context, answer=result.answer)
        dspy.Assert(
            check.is_faithful,
            f"Answer contains unsupported claims: {check.unsupported_claims}. "
            "Rewrite using only information from the provided sources."
        )

        return result
```

When `dspy.Assert` fails, DSPy automatically retries the LM call, feeding back the error message so the model can self-correct. This retry loop (called backtracking) runs up to `max_backtrack_attempts` times (default: 2).

## Step 4: Self-check pattern

Generate an answer, then ask the model to verify its own claims against the sources. Lightweight and good for most cases.

```python
class SelfCheckedAnswer(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought("context, question -> answer")
        self.check = dspy.ChainOfThought(CheckFaithfulness)

    def forward(self, context, question):
        result = self.answer(context=context, question=question)

        verification = self.check(context=context, answer=result.answer)
        dspy.Suggest(
            verification.is_faithful,
            f"Some claims may not be supported: {verification.unsupported_claims}. "
            "Consider revising to stick closer to the sources."
        )

        return dspy.Prediction(
            answer=result.answer,
            is_verified=verification.is_faithful,
            unsupported=verification.unsupported_claims,
        )
```

Use `dspy.Suggest` (soft) instead of `dspy.Assert` (hard) when you want to flag issues without blocking the response.

## Step 5: Cross-check pattern

Generate the answer twice independently, then compare. If two independent generations disagree, something is probably made up.

```python
class CrossChecked(dspy.Module):
    def __init__(self):
        self.gen_a = dspy.ChainOfThought("context, question -> answer")
        self.gen_b = dspy.ChainOfThought("context, question -> answer")
        self.compare = dspy.Predict(CompareAnswers)

    def forward(self, context, question):
        a = self.gen_a(context=context, question=question)
        b = self.gen_b(context=context, question=question)

        check = self.compare(answer_a=a.answer, answer_b=b.answer)
        dspy.Assert(
            check.agree,
            f"Two independent answers disagree: {check.discrepancy}. "
            "This suggests hallucination. Regenerate with closer attention to sources."
        )

        return a

class CompareAnswers(dspy.Signature):
    """Check if two independently generated answers agree on the facts."""
    answer_a: str = dspy.InputField()
    answer_b: str = dspy.InputField()
    agree: bool = dspy.OutputField(desc="Do they agree on all factual claims?")
    discrepancy: str = dspy.OutputField(desc="What they disagree on, if anything")
```

Best for high-stakes outputs where the cost of hallucination is high. Doubles your LM calls but catches inconsistencies.

## Step 6: Grounding via retrieval

The single most effective anti-hallucination measure: give the AI source material and constrain it to that material. Connect to `/ai-searching-docs` for the full RAG setup.

```python
class GroundedQA(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=5)
        self.answer = dspy.ChainOfThought(CitedAnswer)
        self.verify = dspy.Predict(CheckFaithfulness)

    def forward(self, question):
        # Ground in retrieved sources
        context = self.retrieve(question).passages

        # Generate with citation requirement
        result = self.answer(context=context, question=question)

        # Verify faithfulness
        check = self.verify(context=context, answer=result.answer)
        dspy.Assert(
            check.is_faithful,
            f"Unsupported claims: {check.unsupported_claims}. "
            "Only use information from the provided sources."
        )

        return result
```

## Step 7: Confidence thresholds

Flag low-confidence outputs for human review instead of showing them to users.

```python
class ConfidenceGated(dspy.Signature):
    """Answer the question and rate your confidence."""
    context: list[str] = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="0.0 to 1.0, how confident are you?")
    reasoning: str = dspy.OutputField(desc="Why this confidence level?")

class GatedResponder(dspy.Module):
    def __init__(self, threshold=0.7):
        self.respond = dspy.ChainOfThought(ConfidenceGated)
        self.threshold = threshold

    def forward(self, context, question):
        result = self.respond(context=context, question=question)

        if result.confidence < self.threshold:
            return dspy.Prediction(
                answer=result.answer,
                needs_review=True,
                confidence=result.confidence,
                reason=result.reasoning,
            )

        return dspy.Prediction(
            answer=result.answer,
            needs_review=False,
            confidence=result.confidence,
        )
```

## How backtracking works

When `dspy.Assert` fails:
1. DSPy catches the assertion failure
2. The error message is fed back to the LM as additional context
3. The LM retries generation with the feedback ("your answer had unsupported claims X, Y")
4. This repeats up to `max_backtrack_attempts` times
5. If all retries fail, the assertion raises an error

This is why good error messages matter — they're literally the feedback the model uses to improve.

## Choosing the right pattern

| Pattern | Cost | Latency | Best for |
|---------|------|---------|----------|
| Citation enforcement | 1 LM call | Low | When you have numbered sources |
| Faithfulness verification | 2 LM calls | Medium | RAG systems, doc Q&A |
| Self-check | 2 LM calls | Medium | General fact-checking |
| Cross-check | 3 LM calls | High | High-stakes, critical outputs |
| Confidence gating | 1 LM call | Low | Human-in-the-loop systems |
| Retrieval grounding | 1 retrieval + 1-2 LM | Medium | When you have a knowledge base |

## Key principles

- **Grounding beats prompting.** Giving the AI sources to cite is more effective than asking it to "be accurate."
- **Assert for critical facts.** Use `dspy.Assert` when hallucination is unacceptable (medical, legal, financial).
- **Suggest for nice-to-haves.** Use `dspy.Suggest` when you want to flag but not block.
- **Layer your defenses.** Combine retrieval + citation + verification for the strongest protection.
- **Good error messages help.** The Assert message becomes the model's self-correction prompt.

## Additional resources

- Use `/ai-searching-docs` for retrieval-augmented generation (RAG) setup
- Use `/ai-checking-outputs` for general output validation (format, safety, quality)
- Use `/ai-following-rules` for enforcing business rules and content policies
- See `examples.md` for complete worked examples
