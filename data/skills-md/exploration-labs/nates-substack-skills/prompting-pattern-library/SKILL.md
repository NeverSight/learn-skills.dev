---
name: prompting-pattern-library
description: Comprehensive library of proven prompting patterns, frameworks, and examples for different use cases. This skill should be used when creating prompting guides, analyzing prompt effectiveness, teaching prompting techniques, or troubleshooting prompting issues. Use when writing about prompting, explaining prompting concepts to others, or improving existing prompts.
---

# Prompting Pattern Library

**Version 1.0** | October 2025 | Tested with Claude 3.5/4, GPT-4/4o, Gemini 1.5 Pro

---

## Navigation

**📖 Full Documentation**: See [README.md](README.md) for complete navigation, use case index, and version notes.

**Quick access by need:**
- **Learning prompting**: Start here, then read [Prompt Patterns](references/prompt-patterns.md)
- **Debugging prompts**: Jump to [Failure Modes](references/failure-modes.md)
- **Building agents**: See [Orchestration Patterns](references/orchestration-patterns.md)
- **Model optimization**: Review [Model Quirks](references/model-quirks.md)

---

## Overview

This skill provides a comprehensive library of prompting patterns, anti-patterns, and model-specific guidance for effective LLM interactions. Use this when creating educational content about prompting, analyzing prompt quality, or explaining prompting techniques to technical and non-technical audiences.

**What's included:**
- 25+ proven prompting patterns with "why it works" analysis
- Common failure modes with diagnosis and fixes
- Model-specific guidance (Claude, GPT-4, Gemini)
- Advanced orchestration patterns for agent systems
- Cross-references throughout for deep-dive learning

---

## Quick Reference: Common Prompting Patterns

### Structural Patterns
**Role Prompting**: Assign a specific role or persona to frame the response
**Chain-of-Thought (CoT)**: Request step-by-step reasoning before final answer
**Few-Shot Learning**: Provide examples of desired input-output pairs
**Zero-Shot with Instructions**: Detailed task description without examples
**Tree of Thoughts**: Explore multiple reasoning paths before choosing best

### Output Control Patterns
**Structured Output**: Request specific formats (JSON, XML, tables, lists)
**Delimiters**: Use clear separators for inputs, examples, and instructions
**Length Control**: Specify desired output length explicitly
**Style Constraints**: Define tone, formality, audience level

### Reasoning Enhancement Patterns
**Self-Consistency**: Generate multiple solutions and select most common
**Reflection**: Ask model to critique its own output
**Decomposition**: Break complex tasks into smaller sub-tasks
**Analogical Reasoning**: Request analogies or comparisons

### Retrieval Patterns
**Citation Requirements**: Demand sources and evidence
**Fact-Checking**: Request verification of claims
**Knowledge Boundaries**: Ask model to acknowledge uncertainty

See `references/prompt-patterns.md` for comprehensive pattern catalog with examples.

## When to Read References

### Always Read First
**Creating prompting educational content**: Read `references/prompt-patterns.md` for pattern catalog with "why it works" analysis
**Debugging problematic prompts**: Read `references/failure-modes.md` for common issues and fixes with cross-referenced solutions
**Cross-model implementation**: Read `references/model-quirks.md` for model-specific considerations and optimization
**Building agent systems**: Read `references/orchestration-patterns.md` for multi-step workflows and agentic architectures

### Read When Needed
**Advanced pattern implementation**: Review specific patterns in references for detailed guidance and research basis
**Teaching prompting**: Use examples from references as teaching materials with "why it works" explanations
**Optimizing existing prompts**: Consult failure modes to identify weaknesses, then apply patterns from prompt-patterns.md
**Agent orchestration**: Reference orchestration-patterns.md for planner-executor, multi-agent collaboration, and evaluation loops

## Core Principles for Effective Prompting

### Specificity Over Generality
Vague: "Write about AI"
Specific: "Write a 500-word technical explanation of transformer attention mechanisms for software engineers with no ML background"

### Provide Context Explicitly
Poor context: "Fix this code"
Good context: "Fix this Python function that should validate email addresses. Current issue: it fails on addresses with plus signs. Python 3.11, standard library only."

### Use Examples When Precision Matters
For tasks requiring specific formats or styles, provide 2-3 high-quality examples rather than lengthy descriptions. Examples communicate requirements more precisely than instructions alone.

### Structure Complex Prompts
For multi-part tasks, use clear sections:
1. Context and background
2. Specific task requirements
3. Output format specifications
4. Constraints and limitations
5. Examples (if applicable)

### Iterate Based on Output
Prompting is experimental. Start simple, observe failure modes, refine incrementally. Most effective prompts emerge through iteration, not perfect first attempts.

## Model-Specific Considerations

Different models respond differently to identical prompts. Key differences:

**Claude (Anthropic)**: Strong with structured output, detailed reasoning, and nuanced tasks. Responds well to polite, conversational prompts. Excellent at maintaining context over long conversations.

**GPT-4 (OpenAI)**: Versatile across domains, strong creative writing, good instruction-following. Benefits from explicit structure. Can be more prone to confident errors.

**Gemini (Google)**: Strong multimodal capabilities, good at analytical tasks. May require more explicit formatting instructions.

See `references/model-quirks.md` for detailed model-specific patterns and anti-patterns.

## Common Failure Modes

### The "Too Polite" Problem
Over-apologetic prompts waste tokens and can reduce output quality. Be direct and clear rather than excessively polite.

### Implicit Assumptions
Models cannot read your mind. What seems obvious to you must be stated explicitly. Common implicit assumptions that cause failures:
- Desired output format
- Audience level
- Required depth of detail
- Constraints (time period, geography, etc.)

### Conflicting Instructions
When instructions contradict each other, models exhibit unpredictable behavior. Example conflict: "Be concise but include comprehensive detail."

### Ambiguous Success Criteria
"Make it better" is not actionable. Define what "better" means: faster, more accurate, more readable, more maintainable, etc.

See `references/failure-modes.md` for comprehensive failure patterns and fixes.

## Using This Skill for Content Creation

### Educational Content
When writing prompting guides or tutorials, use patterns from references as examples. Structure content to move from simple (zero-shot) to complex (chain-of-thought, tree-of-thoughts) patterns.

### Prompt Analysis
To analyze prompt effectiveness, compare against patterns in references. Identify which patterns are present or absent, check for common failure modes.

### Prompt Improvement
To improve existing prompts:
1. Identify the task type and check appropriate patterns in references
2. Check against failure modes in `references/failure-modes.md`
3. Apply relevant structural improvements
4. Test and iterate

## Bundled References

### references/prompt-patterns.md
Comprehensive catalog of 25+ prompting patterns with:
- Pattern name and description
- When to use each pattern
- Concrete examples with "why it works" analysis
- Variations and combinations
- Common pitfalls
- Cross-references to failure modes and model quirks
- Research basis where applicable

### references/failure-modes.md
Common prompting failures organized by:
- Failure type (ambiguity, contradiction, assumption, etc.)
- Symptoms and diagnosis
- Root cause analysis
- Fixes with examples
- Cross-references to relevant patterns
- Prevention checklist

### references/model-quirks.md
Model-specific guidance covering:
- Claude-specific patterns and anti-patterns
- GPT-specific patterns and anti-patterns
- Gemini-specific patterns and anti-patterns
- Cross-model considerations
- When model choice matters
- Model selection decision tree
- Testing strategies across models

### references/orchestration-patterns.md
Advanced patterns for multi-step AI workflows:
- Meta-prompting patterns (prompt generation, optimization loops)
- Multi-agent orchestration (planner-executor, specialist collaboration)
- Evaluation and refinement loops (generate-critique-revise, ensemble evaluation)
- Tool integration patterns (tool selection, function call orchestration)
- Memory and state management (stateful conversations, context summarization)
- Pattern composition for production systems
- Performance optimization strategies
