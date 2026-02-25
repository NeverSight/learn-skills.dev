---
name: tldr-expert
description: |
  Concise summarization and information distillation. Covers executive summaries, code change summaries, PR descriptions, meeting notes, technical briefs, and progressive disclosure patterns.

  Use when writing PR descriptions, summarizing code changes, creating executive briefs, distilling long discussions, or generating release notes.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# TL;DR Expert

## Overview

The TL;DR Expert skill produces clear, concise summaries of technical content. It applies structured patterns to distill complex information into actionable briefs at the right level of detail for the audience.

**When to use:** Writing PR descriptions, summarizing code changes for reviewers, creating executive briefs for stakeholders, distilling long discussions into decisions and action items, or generating release notes.

**When NOT to use:** Writing full documentation (use the `docs` skill), producing marketing copy, creating detailed tutorials, or writing specifications that require exhaustive coverage.

## Quick Reference

| Pattern           | Format                                           | Key Points                                     |
| ----------------- | ------------------------------------------------ | ---------------------------------------------- |
| Executive summary | Conclusion first, then evidence, then details    | Lead with the recommendation; inverted pyramid |
| PR description    | What changed, why, how to test                   | Reviewers read the title and first paragraph   |
| Code change       | Files changed, key decisions, impact areas       | Focus on intent, not line-by-line diff         |
| Meeting notes     | Decisions, action items, open questions          | Skip discussion; capture outcomes              |
| Release notes     | User-facing changes, breaking changes, migration | Write for users, not developers                |
| Technical brief   | Problem, solution, alternatives, recommendation  | One page max; link to details                  |

## Common Mistakes

| Mistake                                   | Correct Pattern                                             |
| ----------------------------------------- | ----------------------------------------------------------- |
| Too verbose; includes every detail        | Cut to 20% of original length while keeping 80% of value    |
| Missing context; assumes reader knows     | Include one sentence of background before the summary       |
| Burying the lead in the third paragraph   | First sentence states the conclusion or key change          |
| No actionable items in meeting notes      | Every meeting summary ends with owners and deadlines        |
| Summarizing HOW instead of WHY            | Lead with intent and impact, not implementation details     |
| No audience awareness                     | Adjust depth: exec = 3 bullets, dev = 1 paragraph           |
| Release notes written for developers      | Focus on what users can do differently, not code changes    |
| PR description says "various fixes"       | List each change with a reason; vague helps no one          |
| Missing breaking changes in release notes | Breaking changes get their own section with migration steps |
| Using jargon for non-technical audience   | Match vocabulary to the reader's expertise level            |

## Delegation

- **Content discovery**: Use `Explore` agent to gather source material
- **Detailed review**: Use `Task` agent for thorough analysis before summarizing
- **Code review**: Delegate to `code-reviewer` agent for change impact assessment

> If the `docs` skill is available, delegate full documentation tasks to it.

## References

- [Summarization patterns, templates, and progressive disclosure](references/summarization-patterns.md)
