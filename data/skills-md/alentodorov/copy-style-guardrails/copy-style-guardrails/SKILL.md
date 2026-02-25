---
name: copy-style-guardrails
description: Enforce modern, natural copywriting guardrails and rewrite copy to avoid staccato contrast, slogan fragments, and repeated adjective stacks. Use when drafting or rewriting marketing, product, website, or UX copy, including headlines, taglines, CTAs, and short brand statements, especially when the input includes contrasty sentence patterns that need smoothing.
license: MIT
compatibility: Works with any skills-compatible agent (Claude Code, etc.)
metadata:
  author: alentodorov
  version: "1.0.0"
---

# Copy Style Guardrails

## Overview

Write or rewrite copy in a smooth, conversational voice that avoids slogan-like fragments and contrasty sentence beats while preserving meaning and intent.

## Guardrails

Follow these rules every time you generate or revise copy:

- Avoid these sentence patterns entirely, even if they seem persuasive:
  - "All the X. None of the Y."
  - "It's not X. It's Y."
  - "No X. No Y. No Z."
  - Repeated adjective fragments like "Simple. Effective. Easy."
- Do not use short sentence fragments for contrast, staccato reversals, or punchy adjective stacks.
- Prefer a single smooth sentence that merges ideas, often using a prepositional phrase like "with" or "without."
- Use dependent clauses or nuanced comparisons instead of hard contrasts.
- Reframe negatives into a positive benefit where possible.
- Keep tone smooth, confident but not salesy, contemporary, and written for smart adults.

## Rewrite Workflow

1. Scan the input for any of the banned patterns or staccato fragments.
2. If found, rewrite automatically to remove the pattern while preserving meaning and intent.
3. Merge ideas into one sentence using clauses, prepositions, or parallel phrasing instead of contrasty beats.
4. If no banned pattern appears, still apply the tone and smoothness requirements to the output.

## Examples

### Before and After

| Input (Banned Pattern) | Output (Rewritten) |
|------------------------|-------------------|
| "All the power. None of the complexity." | "Full power with a simple interface." |
| "It's not a tool. It's a partner." | "A tool that works alongside you like a partner." |
| "Fast. Reliable. Secure." | "Fast and reliable with built-in security." |
| "No fees. No hassle. No limits." | "Use it freely without fees, hassle, or limits." |

### Full Rewrite Example

**Input:**
> "Simple. Powerful. Affordable. It's not just software. It's your competitive edge."

**Output:**
> "Simple and powerful software at a price that makes sense—giving you a real competitive edge."
