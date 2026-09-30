---
name: how
description: Explain how something in the codebase works, at the depth a senior engineer needs to start working in it.
argument-hint: "[question]"
disable-model-invocation: true
---

The deliverable is a **mental model**: an explanation pitched at a senior engineer onboarding onto the subsystem, stopping short of annotated source. Every claim in it is **traced** to the implementation.

## 1. Frame the question

Take the question from the invocation, or from the subject under discussion this session. When its scope is ambiguous, state your reading in one line and proceed.

Cut the question into **angles**, each a distinct slice of the subsystem: one angle for a single module or function, two to four for a subsystem spanning files or services. When in doubt, take fewer.

Done when every angle names a file or symbol to start from, and every part of the question sits inside one of them.

## 2. Explore

Dispatch one **explorer** per angle in a single message (`subagent_type: Explore`, `model: sonnet`, search breadth `very thorough`). Each prompt carries the path to [references/explorer-brief.md](references/explorer-brief.md), the question, and that explorer's angle.

Done when every return traces its angle to code, a file path behind each component and each flow step. Re-dispatch an explorer that came back on names alone.

## 3. Explain

Synthesise the findings into one **mental model**. Where explorers overlap, merge; where they contradict, settle it by reading the code yourself. Write per `/humanize`, and:

- Name the real things: "`UserService` calls `AuthClient.refresh()`", not "the service delegates to the client".
- Where something is complex, explain why; where it is simple, give it one sentence.
- Draw a Mermaid diagram when the flow crosses components, or when data changes shape through stages.

Use these sections, dropping one only when nothing the explorers returned belongs in it:

- **Overview**: one or two paragraphs. What it is, what it does, why it exists. Enough to decide whether to keep reading.
- **Key concepts**: the types, services, and abstractions the rest depends on, each defined in a line.
- **How it works**: the longest section. What triggers it, what happens step by step, where data goes, where the decisions are. Prose with file and function references; a code snippet only when the point needs it.
- **Where things live**: the two or three files someone opens first, and why each matters.
- **Gotchas**: the non-obvious findings that would trip someone new here.
- **Open questions**: the links no explorer could trace, named as unknowns rather than filled with a guess.

Done when every explorer finding is accounted for: used, merged with another, or dropped as detail a senior engineer starting here would not need.
