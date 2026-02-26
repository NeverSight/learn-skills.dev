---
name: deslop-writing
description: Clean up AI-generated writing by removing slop (generic tone, filler, inflated claims, vague attributions, list spam) while keeping meaning the same. Use when asked to "humanize" text, remove AI-sounding writing, or align prose with local/author voice.
---

# Deslop Writing

## Overview

Strip AI-generated artifacts from existing text while preserving intent and factual claims. Prefer small, local edits over rewrites unless explicitly requested.

## Workflow

### 1) Establish baseline

- Identify the "source of truth" text (before the AI pass) if available.
- Identify the target audience (internal doc, public post, README, PR description, email).
- Preserve facts. If the text makes a claim without evidence, either add the missing specifics or remove the claim.

### 2) Remove slop patterns

- Delete filler and signposting ("In conclusion", "It's important to note", "Let's dive in", "As mentioned above").
- Replace inflated/marketing language with plain statements.
- Replace vague attributions ("experts say", "many believe") with something checkable or remove it.
- Remove list spam and "rule of three" rhythm when it's not natural.
- Prefer repeating the best word over synonym-cycling.
- Reduce em-dash / bold / emoji habits unless they already match the author's style.

See `references/slop-patterns.md` for a concrete checklist.

### 3) Align to the preferred voice (without cosplay)

- Put the punchline first, then the details.
- Use short paragraphs. Cut anything that doesn't earn its spot.
- Make tradeoffs and limitations explicit (what this does *not* do).
- Sound like a person with skin in the game: specific, candid, non-performative.
- If a repo has a "preferred voice" doc, follow it. If not, default to plain, direct prose.

### 4) Verify

- Meaning stays the same (unless you explicitly fixed an unsupported claim).
- Names, dates, numbers, and APIs remain correct.
- The result reads like one human wrote it, not a style-transfer demo.

### 5) Report

- End with 1-3 sentences: what changed, what you *didn't* change, and any remaining uncertainty.
