---
name: debug-agent
description: >
  Diagnose why the current Claude Code session went wrong (or generally review how it
  went) using the Three Gaps framework (Understanding / Specification / Execution:
  Context / Tooling / Reasoning). MAIN spawns a fork to diagnose, presents findings,
  and applies any file fix only after explicit user approval — the fork inherits the
  conversation context but never edits. TRIGGER when: user says "the agent got it
  wrong", "this isn't working", "diagnose this session", "why did Claude mess this
  up", "debug this run", "what went wrong", "review this session", "how did this
  session go", "/debug-agent", or asks why the current session produced bad output.
---

# Debug Agent

Diagnose what went wrong in *this session* and apply the right fixes. Two invocation modes:

- **Failure-driven (typical)** — user saw a specific bad output ("the dossier missed the qualification criteria"). Anchor on that symptom.
- **Generic review** — user wants a retrospective ("how did this session go", "anything we could've done better"). No named failure; scan for the most prominent issues.

## Two roles

This skill runs in one of two roles. Identify which one you are *before* doing anything else, then follow only that section.

- **§MAIN** — you received `/debug-agent` (or an equivalent ask) from the user directly. You own user interaction and you apply any fixes. You **do not diagnose inline** — you spawn a fork to do that.
- **§FORK** — you were spawned by a `/debug-agent` MAIN with a directive containing the phrase **"diagnose only — return report, do not edit"**. You own the diagnosis and return a structured report. You **never edit files**.

If the directive that brought you here doesn't contain that phrase, you are MAIN.

## Hard constraint (both roles)

**Only diagnose the current session.** Do not read other transcripts, session logs, or external traces. Evidence comes from this conversation's own history. (Forks inherit the conversation, so they have it natively.)

---

## §MAIN — Workflow

You are the user-facing agent. Your job is small: dispatch the fork, present what it returns, and apply the fix only after explicit approval.

### 1. Fork yourself for diagnosis

Immediately spawn a fork via the `Agent` tool with **no `subagent_type`** (a fork inherits this conversation's context, which is the entire evidence base). Name it something like `debug-diagnosis`.

The fork's directive must:

- Tell it to invoke this skill (`/debug-agent`) so it loads the §FORK instructions.
- Contain the literal phrase **"diagnose only — return report, do not edit"** so it routes to §FORK.
- Tell it to return a structured report (shape described in §FORK step 6).

Announce one short sentence to the user: *"Spawning a fork to diagnose this session."* Then wait — don't speculate about findings.

### 2. Receive the fork's report

The fork returns a structured report containing: confirmed symptom, gaps with evidence, the upstream-most gap, Part A tips (if any), and a Part B fix proposal (if any).

### 3. Present the diagnosis to the user

Surface the fork's report. Verbatim or lightly reformatted — don't editorialize.

### 4. Always print Part A tips

If the fork's report includes Part A tips, print them. **Always.** Even when you also have a Part B fix to apply. The tips have learning value beyond the immediate fix — surfacing them helps the user operate the agent better next time. This skill is partly a teaching tool, not just a fix-applier.

### 5. If there's a Part B fix proposal, ask before applying

When the fork returns a Part B fix proposal (a concrete file change), use `AskUserQuestion`:

- **Apply the fix now** — you'll edit the file in this session.
- **Skip — I'll do it later** — you print the proposal and stop applying.

If the user picks apply:

- Invoke the recommended tool from the proposal: `/skill-master` for skill revisions, `/create-cli` for CLI work, `/help` for hook creation, or direct `Edit` for small targeted changes.
- After the edit, surface a 1–2 line summary of what landed (file path + the specific change).

### 6. Hand off to a fresh session for testing

Whether or not you applied the fix, close with the handoff:

```
Next step — test it:
1. Open a fresh Claude Code session (`/clear`, or close & reopen).
2. Re-run your original task — apply the tips above[, and trigger
   the revised skill if one was fixed].
3. If output is still off, run `/debug-agent` in that session.
```

Don't retry the original task in *this* session — it's past the smart zone for execution work, so output would land on rotted context and confound whether the fix worked.

---

## §FORK — Workflow

You are the diagnosis fork. You inherited MAIN's full conversation history. Your job: walk the Three Gaps and return a structured report. **You never edit files. You never apply fixes.** If you catch yourself reaching for `Edit`, `Write`, or invoking `/skill-master`, stop — that belongs to MAIN.

### 1. Capture the symptom

Before walking the gaps, anchor the diagnosis on what the user actually saw. Without a confirmed symptom, the gap-walk floats — you'll surface things the user doesn't care about and miss the one they do.

1. **Read the conversation** (already in your context). What's the user reacting to? A specific failure or a general "feels off" / retrospective ask?
2. **Propose what you noticed.** In one sentence, name the most likely symptom (failure mode) or the most prominent issue you can see (generic mode).
3. **Confirm with one `AskUserQuestion`.** Offer 2–3 candidate symptoms + Other. **Always confirm — even when you're confident.** Diagnosing the wrong symptom wastes the rest of the workflow.
4. Once the user confirms, all downstream gap-walking is anchored to that symptom.

**Mode handling:**

- **Failure-driven:** the symptom is a specific bad output. Anchor evidence to that artifact and what produced it.
- **Generic review:** no specific failure. Scan broadly — the gaps you surface are whatever has the most evidence in the session, not anything tied to one artifact.

**If the user can't articulate any symptom and your inference yields nothing concrete:** that's itself a signal — likely an Understanding gap. Note it, treat the absence of a symptom as the symptom, and proceed.

### 2. Walk the gaps inside-out

For each gap below, scan the session for symptoms. Walk in this order — upstream gaps cause downstream ones, so finding one upstream often explains several downstream symptoms.

| # | Gap | Symptoms to look for | Fix type |
|---|-----|---------------------|----------|
| 1 | **Understanding** | User couldn't describe the deliverable in one sentence; brief was revised 3+ times and output is still off; user used vague terms ("cleaner", "feels right") without pinning them down | User-side |
| 2 | **Specification** | Output addresses the literal request but skipped a constraint; one of the 5 brief slots (Context / Task / Constraints / Verification / Output format) was empty; no stopping condition was specified | User-side |
| 3 | **Execution: Context** | Agent contradicted an earlier instruction; repeated work it already did; `/context` past the smart zone mid-execution; status line high before output cliffed | User-side |
| 4 | **Execution: Tooling** | A skill that should have fired didn't; a tool returned an error the agent couldn't act on; the agent re-derived the same code-doable step every run | Agent-side |
| 5 | **Execution: Reasoning** | Made-up fact / unverified citation; instruction skipped despite a clean spec; correct inputs, wrong conclusion | Mixed |

**Fix-type definitions:**

- **User-side** — the failure lived in the user's habits. Nothing on disk to fix. Output is *Part A tips* only.
- **Agent-side** — the failure lived in a file on disk (skill body, CLI script, hook). Output is a *Part B fix proposal* — a concrete, structured description of what to change. MAIN will apply it after user approval. You do not apply it.
- **Mixed** — could be either, depending on whether the gap traces back to a file (agent-side) or a habit (user-side). Inspect the evidence to decide.

### 3. Apply the masquerade rule

Understanding hides as Specification. **If the brief was revised 3+ times and the output is still off, classify the upstream gap as Understanding** — even if it looks like Specification on the surface.

### 4. Identify the upstream-most gap

Mark the upstream-most gap that has symptoms in this session. That's the one you'll build the fix proposal for. Note downstream gaps in the report too — but **don't propose fixes for them**. Most dissolve once the upstream is fixed; we re-diagnose later.

### 5. Load the reference for the upstream gap only

Don't pre-load every reference. Read only the file for the upstream-most gap:

| Gap | Reference |
|-----|-----------|
| Understanding | `references/understanding.md` |
| Specification | `references/specification.md` |
| Execution: Context | `references/gap-context.md` |
| Execution: Tooling | `references/gap-tooling.md` |
| Execution: Reasoning | `references/gap-reasoning.md` |

Each reference declares the gap's fix type, provides the Part A tips template (if applicable), and provides the Part B fix proposal template (if applicable).

### 6. Return the structured report to MAIN

Return your report in this shape (markdown, addressed to MAIN). MAIN will surface it to the user.

```
## Diagnosis report

**Confirmed symptom:** [the symptom from step 1]

**Gaps identified:**

[UPSTREAM] Gap N: [Name] · fix type: [user-side / agent-side / mixed]
  Evidence: [1–2 specific moments from the session — quote or cite turns]

[downstream] Gap M: [Name] · fix type: [...]
  Evidence: [...]

(repeat for each gap with symptoms)

---

## Part A — Tips for the next task

- [Specific tip 1, anchored to session evidence]
- [Specific tip 2]

(Omit this section only if the upstream gap has no Part A.)

---

## Part B — Fix proposal

- **Target file(s):** [exact path]
- **Specific changes:** [concrete description of what to add/remove/revise]
- **Recommended tool to apply:** [/skill-master | /create-cli | /help | direct Edit]

(Omit this section if no Part B applies.)
```

After returning the report, **stop.** Do not edit anything. Do not invoke `/skill-master` or any other fix tool. MAIN will take it from here.

---

## Anti-patterns

- **MAIN diagnosing inline.** MAIN must always fork. The fork has the conversation in context already (forking is cheap) and keeps reference-file reads + `AskUserQuestion` exchanges out of MAIN's window.
- **FORK editing files.** The fork only diagnoses. If a fix is needed, it goes in the Part B proposal — MAIN applies it.
- **MAIN applying a fix without `AskUserQuestion` approval.** Always confirm before editing on the user's behalf.
- **MAIN hiding Part A when Part B exists.** Always print the tips. They have learning value beyond the immediate fix.
- **Skipping symptom capture in FORK.** Never jump into the gap walk before confirming what went wrong. Diagnosing the wrong symptom wastes the whole workflow.
- **Skipping confirmation when "you're sure."** Even high-confidence inference gets confirmed via `AskUserQuestion`. The cost of one tap is much lower than the cost of misreading.
- **Diagnosing other sessions.** Hard constraint — only this session.
- **Proposing fixes for downstream gaps.** Walk inside-out: build the fix proposal for the upstream-most gap only. Re-evaluate downstream gaps in a fresh session after the upstream is fixed.
- **Vague evidence.** Cite specific moments from the session, not "the brief was unclear."
- **Skipping the masquerade rule.** 3+ brief revisions = climb back to Understanding.
- **Reading every reference up-front.** FORK loads only the reference for the upstream gap.
- **Generic tips.** Part A should reference what specifically went wrong in *this* session, not boilerplate.
- **MAIN retrying the original task in this session.** Past the smart zone — hand off to a fresh session.
