---
name: why
description: Investigate the motivation and intent behind code, and answer with cited, confidence-tiered findings. Companion to /how.
argument-hint: "[question about code]"
disable-model-invocation: true
---

Code is **mechanics, not motivation**: what it does is readable, why it exists lives in **the record** — commits, PRs, tickets, docs, chat, and telemetry, all partial and sometimes contradictory. Answer what shaped the code from that record, and say where the record runs out.

## 1. Fix the question

The **target** is the code the question is about: a chunk of code, a pattern, or a named design decision. When it is vague, take it from conversation context (open files, recent edits, what was just discussed), state your reading in one line, and proceed.

A question that carries its own answer ("I assume it's for performance?") supplies a **hypothesis**. Note it beside the question as one candidate for the synthesizer to test.

Done when the target and the question are written down, one line each, with the hypothesis beside them when the question carries one.

## 2. Map coverage

List the MCP servers in this session (the `mcp__<server>__` tool prefixes) and assign each to one of seven **sources**: **source control** (always covered, by git and `gh`), **tickets**, **documents**, **chat**, **observability**, **errors**, **analytics**. A server that fits two takes the one matching its primary evidence: a product-analytics server that also tracks errors is analytics, a monitoring server that also holds incident records is observability. A server that holds no historical record — a browser, a filesystem, a worktree tool — takes none. Record the result as the **coverage map**.

Done when the coverage map marks every source **covered** (a server, or git and `gh` for source control) or **skipped** with a one-line **skip reason**: no server present, or **ruled out** for this target (a build-time script has no error tracking). A source you merely doubt is covered.

## 3. Anchor

Dispatch the **anchorer** (`model: sonnet`). The prompt carries: the path to [references/anchor.md](references/anchor.md), which gives the `git` and `gh` invocations and what to record in each section; the target; the question, with its hypothesis. Done when every section of the anchor has returned filled and **defensive** reads yes or no.

## 4. Investigate

Dispatch one **investigator** per covered source (`model: sonnet`) in a single message. Each prompt carries:

- the path to [references/investigator.md](references/investigator.md), to read first
- the path to its source playbook, `references/sources/<source>.md` (source control is `source-control.md`), to read second
- the anchor
- the question, with its hypothesis
- when the anchor says **defensive**: the path to [references/incident.md](references/incident.md), a cross-cutting incident hunt to run alongside the playbook

Done when every covered source has one investigator of its own, none merged, each has returned findings in the brief's sections, and every prompt carried all of the above.

## 5. Synthesize

Once every investigator has returned, dispatch the **synthesizer** (`model: opus`) with the paths to [references/synthesizer.md](references/synthesizer.md) and [references/epistemics.md](references/epistemics.md), and carrying:

- every investigator's findings verbatim
- the anchor
- the question, with its hypothesis
- the coverage map, with its skip reasons

Done when the report has returned with Sources Consulted covering all seven sources.

## 6. Present

Relay the synthesizer's report with its confidence language intact, adding conversation context where it helps the reader. Done when the user holds the report with every tier label, citation, and Unknown as the synthesizer wrote them.
