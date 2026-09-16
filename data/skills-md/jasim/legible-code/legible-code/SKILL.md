---
name: legible-code
description: >
  Diagnose and remedy code legibility problems by introducing domain types in place of
  primitives and booleans, pushing I/O to module edges, naming intermediate pipeline stages,
  reorganizing modules around data types instead of verbs, and consolidating duplicated logic
  into single authoritative definitions. Use when reviewing a PR, planning a refactor,
  designing a module/seam, or when the user signals that code is hard to reason about or asks where to split or merge a system.
license: MIT
metadata:
  author: Jasim A Basheer
  version: "2.3.0"
---

# Legible Code

## How to Operate

**Input:** Source files, a diff/patch, a plan or design document, a PR description, or a user brief — collectively the **subject**.

**Output:** A ranked list of the 2–5 highest-leverage legibility improvements. For each, state:

1. **Where** — exact location (file:lines, function name, or design section). Include the code's context and purpose.
2. **Diagnostic** — the D-number and a one-line summary citing the specific evidence that triggered it.
3. **Remedy** — drawn from the matching `notes/*.md` file. Read the note before recommending; do not paraphrase from memory.
4. **Leverage** — what becomes easier once fixed. If one fix resolves several diagnostics, say so — those rank highest.

Do not produce a generic checklist. Do not rewrite the code unless asked. If nothing fires, say so plainly.

### Procedure

Work in three passes. Do not match diagnostics until Pass 3.

**Pass 1 — Skim (always, orchestrator only).** Read the entire subject end-to-end. Build the cross-cutting map: entry points and data flow (code), types and boundaries (code or design), decisions made vs. deferred (plans). Note suspicious regions — long functions, verb-named modules, scattered conventions, string-flag branching, in-place mutation, deep nesting, tangled I/O, unnamed repeated patterns. Skip boilerplate, generated code, and unrelated parts. Produce a short list of **candidate hot spots**. Do not parallelize this pass; the cross-cutting map requires a single sequential read.

**Pass 2 — Evidence (orchestrator; fan out when needed).** For each hot spot, gather concrete evidence — call sites, type signatures, consumer lists, repeated patterns, implicit-vs-explicit contracts, where data is constructed vs. consumed. If the relevant code fits in context, read it directly. If gathering evidence for a hot spot would blow context, dispatch a single evidence-only `Explore` probe per hot spot (see **Orchestration** below). Subagents do not diagnose, do not name D-numbers, do not propose remedies, do not rank; they return raw evidence and the orchestrator integrates it.

**Pass 3 — Diagnose (always, orchestrator only).** Walk the diagnostics (see `DIAGNOSTICS.md` for D1–D14) in order over the consolidated evidence. A diagnostic fires only if you can point to specific evidence from the "You have this problem if" bullets — not on vibes. When several fire in the same region, prefer the lowest-numbered (upstream, often causes the others). Rank findings by leverage and emit output.

### Orchestration

For subjects too large for a single mind to hold.

**Only the orchestrator names diagnostics.** Subagents gather raw evidence; the orchestrator integrates that evidence and runs diagnostics against it, using its own Pass 1 skim as the cross-cutting map. Several diagnostics are inherently cross-cutting — narrative incoherence (D1) spans entry points to side-effects, missing vocabulary (D6) spans modules, scattered knowledge (D13) is spread by definition, re-litigated invariants (D14) live between a producer and many consumers. A subagent given only a slice would over-flag or under-flag these.

**Dispatch a probe when reading in-place would blow context.** During Pass 1 or Pass 2, if following a hot spot would cost you the rest of the subject, dispatch a single `Explore` subagent for that hot spot. If you can read the relevant code in place, do that instead.

**Evidence-probe prompt template.** Paste into an `Explore` call (use sub-agents if available), filling in the hot spot description:

> You are an evidence-only worker for a legibility review. Gather raw material about the hot spot below: call sites, type signatures, consumer lists, repeated patterns, implicit-vs-explicit contracts, where data is constructed vs. consumed. Return concrete evidence with `file:line` references.
>
> Constraints — load-bearing:
> - **Do not diagnose.** Do not name diagnostics or D-numbers.
> - **Do not propose remedies.** Do not name notes or refactoring strategies.
> - **Do not rank, prioritize, or judge severity.** Just report what is there.
> - **Do not summarize or interpret.** The orchestrator will integrate the evidence; your interpretation would discard the detail it needs.
>
> Hot spot: `{description — file paths, symbols, the specific question to answer}`
>
> Return a structured list of findings, each with file:line citations. Be concrete and exhaustive within the hot spot's scope; do not stray outside it.

**Concurrency.** Independent probes can run in parallel. Cap at 4–6 in flight. Sequential probes are fine when later ones depend on earlier results (e.g. enumerate consumers first, then probe each consumer cluster).

### Scope Rules

- **Diff or PR:** Weight findings toward issues the diff introduces or worsens. Don't pile on pre-existing problems unless they make the diff materially harder to review.
- **Plan or design:** Apply diagnostics to the proposed structure — which decisions are reified, where the seams are, what vocabulary is introduced, what knowledge would be scattered. Flag problems the plan would *bake in* if implemented as-written.
- **Files with no specific question:** Use the user's framing as the signal ("hard to test" → D3/D4/D5; "hard to change" → D7/D8/D13; "hard to follow" → D1/D2/D11).
- **Nothing fires:** "No high-leverage legibility issues found; here's what I checked" is a valid output. Do not invent problems.

---

## Diagnostics

The fourteen recurring legibility problems live in [`DIAGNOSTICS.md`](DIAGNOSTICS.md). Their conceptual reasoning lives in [`INTRODUCTION.md`](INTRODUCTION.md). Each diagnostic points to a remedy in `notes/*.md`. Read the matching note before recommending — do not paraphrase from memory.
