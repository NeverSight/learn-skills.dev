---
name: prompt-engineering
description: Use when you need to design effective LLM prompts. Intelligently selects optimal prompting methods (Chain of Thought, Few-Shot, Zero-Shot, ReAct, Tree of Thoughts, Self-Consistency) and output formats (XML, JSON, YAML, Natural Language) based on task complexity, target LLM, accuracy requirements, and available context. Trigger on prompt design, prompt optimization, or when choosing between prompting techniques.
---

# Prompt Engineering

## Overview

This skill helps create highly effective prompts by selecting the optimal technique and format based on task characteristics. Analyzes complexity, target LLM, accuracy needs, and context to recommend the best approach from 10+ proven methods and 4 structured formats.

## Quick Start Decision Tree

**Answer these questions to find the right approach:**

### 1. Task Complexity?
- **Simple** → Zero-Shot (see [references/zero-shot.md](references/zero-shot.md))
- **Need format/style** → Few-Shot (see [references/few-shot.md](references/few-shot.md))
- **Multi-step reasoning** → Chain of Thought (see [references/chain-of-thought.md](references/chain-of-thought.md))
- **Tool/API use** → ReAct (see [references/react.md](references/react.md))
- **Complex planning** → Tree of Thoughts (see [references/tree-of-thoughts.md](references/tree-of-thoughts.md))
- **High-stakes** → Self-Consistency (see [references/self-consistency.md](references/self-consistency.md))

### 2. Target LLM?
- **Claude** → XML format (see [references/xml-format.md](references/xml-format.md))
- **GPT** → JSON format (see [references/json-format.md](references/json-format.md))
- **Multi-LLM** → JSON (portable)
- **Human-editable** → YAML (see [references/yaml-format.md](references/yaml-format.md))

### 3. Output Use?
- **Code/API** → JSON
- **Complex hierarchy** → XML (if Claude) or JSON
- **Human editing** → YAML or Natural Language
- **Simple explanation** → Natural Language (see [references/natural-language.md](references/natural-language.md))

**For detailed decision matrix:** [references/decision_matrix.md](references/decision_matrix.md)

---

## Method Selection Quick Reference

| Need | Method | Best Format | Reference |
|------|--------|-------------|-----------|
| Simple task | Zero-Shot | Natural Language | [zero-shot.md](references/zero-shot.md) |
| Style consistency | Few-Shot | Same as examples | [few-shot.md](references/few-shot.md) |
| Multi-step reasoning | CoT | Natural/XML | [chain-of-thought.md](references/chain-of-thought.md) |
| Tool interaction | ReAct | JSON | [react.md](references/react.md) |
| Complex planning | ToT | YAML/XML | [tree-of-thoughts.md](references/tree-of-thoughts.md) |
| High confidence | Self-Consistency | Any | [self-consistency.md](references/self-consistency.md) |

---

## Format Selection Quick Reference

| Target | Complexity | Use Case | Format | Reference |
|--------|-----------|----------|--------|-----------|
| Claude | High | Human | XML | [xml-format.md](references/xml-format.md) |
| Claude | Medium | API | JSON | [json-format.md](references/json-format.md) |
| GPT | Any | API | JSON | [json-format.md](references/json-format.md) |
| Any | Low | Human | Natural | [natural-language.md](references/natural-language.md) |
| Any | Config | Human-editable | YAML | [yaml-format.md](references/yaml-format.md) |
| Multi-LLM | Any | Portable | JSON | [json-format.md](references/json-format.md) |

---

## Common Patterns At-A-Glance

### Zero-Shot Template
```
Task: [X]
Requirements: [Y]
Output: [Z]
```

### Few-Shot Template
```
Task: [X]
Examples:
- Input: A → Output: B
- Input: C → Output: D
Your turn: Input: E → Output: ?
```

### Chain of Thought Template
```
Problem: [X]
Let's think step by step:
1. [Step 1]
2. [Step 2]
3. [Step 3]
Answer: [Y]
```

### ReAct Template
```
Thought: [Reasoning]
Action: [Tool/action]
Observation: [Result]
[Repeat]
```

**For complete templates and examples, see individual method references.**

---

## Common Pitfalls & Quick Fixes

### ❌ Ambiguous Instructions
**Bad:** "Make this better"
**Good:** "Improve by: 1) Add error handling, 2) Optimize to O(n log n), 3) Add docs"

### ❌ Wrong Format for LLM
**Bad:** JSON for Claude complex hierarchy
**Good:** XML for Claude, JSON for GPT/APIs

### ❌ No Examples When Needed
**Bad:** "Extract features in structured format"
**Good:** Show 2-3 concrete input→output examples

### ❌ Overcomplicating Simple Tasks
**Bad:** Tree of Thoughts for "Convert 25°C to F"
**Good:** Simple zero-shot instruction

**For complete pitfalls guide:** [references/pitfalls.md](references/pitfalls.md)

---

## Advanced Techniques

### Combining Methods
- **Few-Shot + CoT:** Examples with reasoning steps (see [references/advanced-combinations.md](references/advanced-combinations.md))
- **ReAct + Self-Consistency:** Multiple tool paths, compare results
- **ToT + XML:** Claude-optimized complex planning

### Meta-Prompting
Ask LLM to help design the prompt:
```
I need a prompt for [task].
Task characteristics: [complexity, LLM, output use, accuracy needs]
Recommend: 1) Technique, 2) Format, 3) Draft template, 4) Why
```

### Prompt Chaining
Break complex tasks into sequential prompts.
**See:** [references/prompt-chaining.md](references/prompt-chaining.md)

---

## Token Efficiency Tips

```
✓ More Efficient          ✗ Less Efficient
- Zero-shot for simple    - 10+ examples
- Concise instructions    - Verbose repetition
- JSON for API parsing    - XML for API parsing
- Direct examples         - Over-explained examples
```

**Typical token counts:**
- Zero-Shot: 50-200 tokens
- Few-Shot (3 examples): 200-800 tokens
- Chain of Thought: 100-500 tokens
- ReAct: 300-1000 tokens
- Tree of Thoughts: 500-2000+ tokens
- Self-Consistency: 500-3000+ tokens

---

## Implementation Checklist

When creating a prompt:

- [ ] Identify task complexity → Choose method
- [ ] Identify target LLM → Choose format
- [ ] Write clear, specific instructions
- [ ] Add examples if Few-Shot/Few-Shot CoT
- [ ] Specify output format explicitly
- [ ] Include constraints and requirements
- [ ] Test with sample inputs
- [ ] Validate outputs
- [ ] Refine based on results

---

## Resources

### References (Detailed Guides)
- [decision_matrix.md](references/decision_matrix.md) - Comprehensive decision framework
- [zero-shot.md](references/zero-shot.md) - Zero-shot prompting guide
- [few-shot.md](references/few-shot.md) - Few-shot prompting guide
- [chain-of-thought.md](references/chain-of-thought.md) - CoT prompting guide
- [react.md](references/react.md) - ReAct prompting guide
- [tree-of-thoughts.md](references/tree-of-thoughts.md) - ToT prompting guide
- [self-consistency.md](references/self-consistency.md) - Self-consistency guide
- [xml-format.md](references/xml-format.md) - XML format best practices
- [json-format.md](references/json-format.md) - JSON format best practices
- [yaml-format.md](references/yaml-format.md) - YAML format best practices
- [natural-language.md](references/natural-language.md) - Natural language best practices
- [pitfalls.md](references/pitfalls.md) - Common mistakes and solutions
- [advanced-combinations.md](references/advanced-combinations.md) - Combining techniques
- [prompt-chaining.md](references/prompt-chaining.md) - Sequential prompt patterns

### Assets (Templates)
- `templates/` - Ready-to-use templates for common scenarios (coming soon)

---

**Navigate to specific references above for detailed implementation guides, templates, and examples.**
