---
name: lens-brief
description: "Distill dense context, verbose explanations, or complex topics into concise plain language with an immediate bottom-line conclusion."
---

# lens-brief — Controlled Plain-Language Technical Summary Engine

## Operating Invariants

- **Language Adaptation**: Respond in the caller's active conversational language (e.g., Vietnamese, English).
- **BLUF Primacy**: State the decisive conclusion or answer in the opening sentence.
- **Plain Voice (ASD-STE100)**: Use active voice and short sentences (max 20–25 words); eliminate filler words, phrasal verbs, and passive phrasing.
- **Code Anchoring**: Bind terms directly to concrete repository symbols and relative paths (`file_path`, `SymbolName`) instead of vague pronouns.
- **Context Isolation**: Explain in isolation without modifying files or expanding active scope.

## Domain Rubric

### 1. Plain-Language Translation Matrix (ISO 24495-1)
- *Findable*: Lead with the decisive takeaway in the BLUF blockquote so the core message is found instantly.
- *Understandable*: Clear, single-meaning words in active sentences instead of bureaucratic phrasing or nominalizations.
- *Usable*: State the concrete takeaway or operational action directly in context.

### 2. Word Choice Guidance (Smell vs. Remedy)
- *Smell (Bureaucratic/Nominalized)*: "We decided to carry out an asynchronous refactoring of the authentication pipeline."
- *Remedy*: "We split `AuthService` into two background tasks. This prevents login timeouts."
- *Smell (Passive/Vague)*: "It was observed that degradation of response latencies occurred due to excessive query iterations."
- *Remedy*: "Unindexed nested queries slowed response times by 300ms."

## Canonical Output Contract

```markdown
> **BLUF**: <Single active sentence stating the core conclusion, change, or answer. Max 20 words.>

<1–3 short paragraphs in plain natural prose. Max 25 words per descriptive sentence, 20 words per procedural sentence. Use active voice and ubiquitous symbols. Explain the context, mechanics, or consequence directly.>

*(omit if purely informational)*
**Next Step**: <Concrete command to execute or decisive choice required from caller.>
```
