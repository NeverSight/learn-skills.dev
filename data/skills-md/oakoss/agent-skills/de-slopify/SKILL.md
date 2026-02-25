---
name: de-slopify
description: >
  Removes AI writing artifacts from documentation and code.
  Use when editing LLM-generated prose, reviewing READMEs, polishing docs before publishing, or cleaning up AI-generated code.
  Use for emdash cleanup, formulaic phrase removal, tone calibration, over-commented code, verbose naming, and AI code smell detection.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# De-Slopify

## Overview

De-slopify is a methodology for removing telltale signs of AI-generated content from documentation, prose, and code. LLMs produce statistically regular output with characteristic vocabulary, punctuation habits, and structural patterns that make text and code feel inauthentic. Some patterns appear over 1,000x more frequently in LLM output than human writing.

**When to use:** Before publishing READMEs, after AI-assisted writing sessions, during documentation reviews, when reviewing AI-generated code for over-engineering, before committing prose or code that an LLM touched.

**When NOT to use:** On code logic or algorithms where correctness matters more than style. On technical specifications where precision outweighs voice. On content that was already human-written and reads naturally.

## Quick Reference

| Category    | Pattern                                         | Fix                                                        |
| ----------- | ----------------------------------------------- | ---------------------------------------------------------- |
| Punctuation | Emdash overuse                                  | Semicolons, commas, colons, or split into two sentences    |
| Phrase      | "Here's why" / "Here's why it matters"          | Explain why directly without the lead-in                   |
| Phrase      | "It's not X, it's Y"                            | "This is Y" or restate the distinction                     |
| Phrase      | "Let's dive in" / "Let's get started"           | Delete; just start the content                             |
| Phrase      | "It's worth noting" / "Keep in mind"            | Delete the hedge; state the fact                           |
| Phrase      | "At its core" / "In essence" / "Fundamentally"  | Delete; say the thing directly                             |
| Vocabulary  | "delve", "tapestry", "landscape", "nuanced"     | Replace with plain, specific language                      |
| Vocabulary  | "revolutionize", "cutting-edge", "game-changer" | Replace with concrete claims or delete                     |
| Structure   | Uniform sentence length throughout              | Mix short (5-word) and long (20+ word) sentences           |
| Structure   | Perfectly balanced lists of exactly 3 items     | Vary list length; humans use 2, 4, or odd counts           |
| Structure   | Generic claims without specifics                | Add names, dates, numbers, or first-person detail          |
| Sycophancy  | "Great question!" / "Absolutely!"               | Delete; answer the question directly                       |
| Meta        | "Let me break this down..." / "Let me explain"  | Delete the preamble; just break it down                    |
| Structure   | Numbered lists where a sentence suffices        | Use a sentence; reserve lists for genuinely parallel items |
| Closer      | "In conclusion" / "To summarize"                | Delete or replace with a specific takeaway                 |
| Code        | Over-commented trivial functions                | Remove comments that restate the code                      |
| Code        | Unnecessary abstractions and design patterns    | Flatten to the simplest working solution                   |
| Code        | Verbose or overly descriptive variable names    | Use domain-appropriate concise names                       |
| Code        | Defensive error handling on every operation     | Handle errors only where failure is realistic              |

## Common Mistakes

| Mistake                                        | Correct Pattern                                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Replacing every emdash mechanically            | Evaluate context; sometimes an emdash is the right choice                                  |
| Editing code blocks for style                  | Focus on prose; leave code examples and technical syntax untouched                         |
| Removing all structure to sound casual         | Keep headers, tables, and lists intact; rewrite prose only                                 |
| Over-correcting into choppy fragments          | Read aloud after editing; recombine sentences that lost flow                               |
| Applying fixes without defining target voice   | Set persona, tone, and audience before starting edits                                      |
| Running regex replacements instead of reading  | Manual line-by-line review is required; context determines fixes                           |
| Ignoring AI code smells                        | Review AI-generated code for over-engineering, verbose names, and unnecessary abstractions |
| Removing all LLM-typical words unconditionally | Some flagged words are perfectly natural in context; use judgment                          |

## Delegation

- **Scan a repository for documentation files that need de-slopifying**: Use `Explore` agent
- **Rewrite an entire documentation site to remove AI artifacts**: Use `Task` agent
- **Plan a documentation voice guide and editorial workflow**: Use `Plan` agent
- **Review AI-generated code for slop patterns**: Use `code-reviewer` agent

> For systematic quality auditing across 12 dimensions (architecture, security, testing, performance, etc.), use the `quality-auditor` skill.

## References

- [Prose patterns: emdash alternatives, phrase replacements, and voice calibration](references/prose-patterns.md)
- [Before-and-after examples of common AI writing fixes](references/before-and-after.md)
- [AI slop vocabulary: words and phrases that signal LLM authorship](references/slop-vocabulary.md)
- [Code slop: detecting and fixing AI-generated code smells](references/code-slop.md)
- [Review workflow: prompts, checklists, and integration](references/review-workflow.md)
