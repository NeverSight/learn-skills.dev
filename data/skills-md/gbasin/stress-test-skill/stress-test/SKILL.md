---
name: stress-test
description: Adversarially stress-test a technical plan by verifying claims against real docs, running POC code, and updating the plan before you build.
user-invocable: true
allowed-tools: Bash Read Write Edit Grep Glob WebSearch WebFetch Task AskUserQuestion
argument-hint: (run in a conversation that has a technical plan)
---

# Stress-Test Plan

You are an adversarial reviewer. Your job is to beat up the plan in the current conversation — find where it will break, what's been assumed without evidence, and what's been hand-waved. Be direct and specific, not polite.

All POC work MUST happen inside `.poc-stress-test/` in the current working directory. Create it at the start, clean it up at the end.

## Phase 1: Extract & Decompose

Read back the plan from the conversation. Break it into:
- **Decisions**: Every concrete technical choice (library, pattern, protocol, data model, etc.)
- **Assumptions**: Things stated as fact but not verified ("library X supports Y", "this scales to Z")
- **Dependencies**: External things the plan relies on (APIs, packages, services, OS features)
- **Interfaces**: Boundaries between components where things can go wrong
- **Ordering**: Implicit sequencing — what must happen before what

## Phase 2: Verify via Search

Do NOT just reason from memory — go verify. **Launch sub-agents in parallel** using the Task tool. Each verification task is independent, so run them concurrently:
- Agent 1 verifies library X actually supports feature Y (check docs, issues, changelogs)
- Agent 2 checks if pattern Z is proven at the scale claimed
- Agent 3 searches for known pitfalls of approach W
- Agent 4 looks for prior art — has anyone tried this combination? What happened?

Use all search tools aggressively: WebSearch for recent issues/deprecations/compatibility, WebFetch for specific docs.

For each claim, answer: **"How do we know this works?"** If you can't find evidence, flag it.

## Phase 3: Identify What Needs a POC

Separate findings into two buckets:

**Resolved by search**: Confirmed or disproved with evidence. List with sources.

**Needs hands-on testing**: Things that can't be settled by reading docs alone:
- Integration questions ("do X and Y actually work together?")
- Performance claims ("this handles N concurrent connections")
- Behavioral assumptions ("the API returns X when Y happens")
- Undocumented edge cases ("what happens when Z fails mid-operation?")
- "Should work in theory" items with no proof anyone's done it

For each item that needs testing, draft a **minimal POC spec**:
- What exactly we're testing
- Why it matters (what breaks if the assumption is wrong)
- Concrete steps: what code to write, what to run, what result confirms/disproves it
- Expected time: trivial (< 5 min), small (< 30 min), or significant (> 30 min)

## Phase 4: Get Approval for POCs

Use **AskUserQuestion** to present the proposed POCs. Group by risk level, let the user choose:
- Which POCs to run now
- Which to skip (accept the risk)
- Which to modify

Do NOT run any POCs without user approval.

## Phase 5: Execute POCs

For approved POCs, **run them in parallel where independent** using sub-agents via the Task tool. All work goes in `.poc-stress-test/` with a subdirectory per POC (e.g., `.poc-stress-test/crdt-compat/`, `.poc-stress-test/ws-scale/`).

Each POC sub-agent should:
1. Create its subdirectory under `.poc-stress-test/`
2. Write minimal test code — smallest thing that proves or disproves the assumption
3. Run it and capture output
4. Report back: **confirmed**, **disproved**, or **inconclusive** — with raw output as evidence

Batch shell operations into single commands to minimize permission prompts (e.g., `mkdir -p dir && cd dir && npm init -y && npm install dep && node test.js`).

## Phase 6: Walk Through Findings

After all POCs complete, walk through each finding **one at a time** using **AskUserQuestion**:

For each finding that impacts the plan, present:
- What was tested / verified
- What the result was (with evidence)
- Your recommended adjustment to the plan
- Alternatives if the user disagrees

Let the user approve, modify, or reject each recommendation individually.

Then apply all approved changes directly into the plan — integrate the fixes where they belong, don't just append a notes section.

Finally, clean up: `rm -rf .poc-stress-test/`
