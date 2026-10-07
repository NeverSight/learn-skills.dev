---
name: melech-tidy
description: Adaptive diff reduction — prune dead code residue, shake prompt bloat, remove cosmetic diff noise, and propose edge-case trades that drop rare-case handling for a smaller diff before opening a PR.
disable-model-invocation: true
---

# Tidy

You just finished coding with an AI agent. The feature works and tests might pass, but `git status` shows a messy diff: orphaned helpers from earlier prompts, dead types, bloated prompt instructions, cosmetic churn that obscures the real change, or retries and special cases for situations that almost never happen.

**`melech-tidy` is the universal, adaptive diff reduction engine.**

Instead of forcing you to diagnose whether your diff suffers from dead code, prompt bloat, cosmetic noise, or rare-case handling that costs more than it buys, `melech-tidy` audits your diff, categorizes findings into **four mutually exclusive reduction lanes**, presents a concrete evidentiary table, and executes surgical cleanups with your approval. Every lane only recommends; you choose what gets tidied.

Tidy subtracts; it does not move code between seams or re-architect.

---

## The 4 Mutually Exclusive Reduction Lanes

The agent reads the requested outcome and surrounding code, decomposes the diff into findings, and evaluates each reducible finding against one strictly delineated engine. Not every changed hunk needs a recommendation.

```text
                              Incoming Working Diff
                                        │
                         Decompose into isolated findings
                         (semantic edits absorb inseparable
                              cosmetic surroundings)
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
          Canonical artifact unchanged?              Semantic change
                    │                                       │
                    ▼                         ┌─────────────┴─────────────┐
              Diff noise                 [Code / Config]       [Prompt / Rules]
          (Cosmetic-only churn)                 │                      │
                                  Does deleting it change              ▼
                                  observable behavior in any case?   Prompt bloat
                                     ┌──────────┴──────────┐
                                     ▼ no                  ▼ yes, a rare case
                                 Dead code           Edge-case trade
```

Lanes are mutually exclusive by **what the proposed action changes**, not by what the code looks like:

| Proposed action | Lane |
|---|---|
| Restores representation; canonical artifact unchanged | **Diff noise** |
| Deletes or collapses code; nothing observable changes | **Dead code** |
| Edits prompt or instruction text | **Prompt bloat** |
| Deletes or simplifies code and changes behavior in a rare case | **Edge-case trade** |

When the same lines allow two actions (replacing hand-written code with a sibling helper that differs in one rare case), report one finding under the lane of the recommended action and name the alternative in its evidence.

User-facing labels (always lead with these — never "Lane 1/2/3" in reports, approval options, or summaries):

| Short label | Full name |
|---|---|
| **Dead code** | Dead Code & AI Residue |
| **Prompt bloat** | Instruction & Prompt Bloat |
| **Diff noise** | Cosmetic Diff Noise |
| **Edge-case trade** | Edge-Case Trades (80/20) |

Lane numbers below are internal section anchors only.

---

### Lane 1: Dead Code & AI Residue (Garbage Collection)
* **Target**: Code added or modified during AI iteration that is uncalled, orphaned, or unneeded.
* **Core Philosophy**: **Inverted Burden of Proof**. Every added symbol is assumed guilty (residue/dead code) until proven innocent.
* **The 4 Evidentiary Proofs**:
  1. **Reachability Proof**: Can runtime execution actually reach this from an active entrypoint (route, UI component, CLI command, export, or event handler)? If not → **Purge**.
  2. **Requirement Proof**: Which explicit user prompt required this? If the answer is *"in case we need it later"* → **Strip YAGNI**.
  3. **Non-Duplication Proof**: Does an existing helper, sibling feature, standard library utility, or dependency option already do this? Search by purpose, not only by name, and read dependency source when a branch guards against something the dependency may already handle. If so → **Collapse**.
  4. **Breakage Proof**: If deleted right now, does any test or behavior break? If nothing fails and no behavior shifts → **Remove**.
* **Action**: **Subtraction only** (delete dead functions, types, props, imports, and zombie chains).
* **Deep playbook**: [`references/lane-1-dead-code.md`](references/lane-1-dead-code.md) — inverted burden of proof, the 4-tier residue classification, and call-graph/zombie-chain tracing.

---

### Lane 2: Instruction & Prompt Bloat (Prompt Shake)
* **Target**: System prompts, skill files (`SKILL.md`), rule instructions (`.cursorrules`, `AGENTS.md`), and markdown prompt docs in the diff.
* **Core Philosophy**: **Minimal-that-covers beats maximal**. Every line is guilty until proven load-bearing. Subtraction, not redesign.
* **The 5 Prompt Proofs**:
  1. **Coverage**: If cut, does a real required case fall through? If not → **Cut**.
  2. **Redundancy**: Is this already stated elsewhere in the instruction? If so → **Collapse**.
  3. **Subsumption**: Is this rule a subset of a broader rule present? If so → **Fold in**.
  4. **Default Knowledge**: Would a competent model do this unprompted? If so → **Cut**.
  5. **Load-Bearing**: Does agent output actually degrade without this line? If not → **Cut**.
* **Action**: **Subtraction inside the diff window** (strip filler, redundant edge cases, and over-explanation).
* **Deep playbook**: [`references/lane-2-prompt-shake.md`](references/lane-2-prompt-shake.md) — the targets it hunts, the 5 proofs in full, and the leanness-≠-lossy guardrails.

---

### Lane 3: Cosmetic Diff Noise (Canonical-Equivalence Cleanup)
* **Target**: Standalone, cosmetic-only findings whose representation changed but whose canonical artifact and intended meaning did not.
* **Core Philosophy**: **Context first, proof or keep**. A moved line is not noise merely because it moved. Read the requirement and surrounding code, then prove canonical equivalence with repository-appropriate tools. If proof is unavailable or the change mixes with a semantic edit, keep it out of this lane.
* **The 4 Evidentiary Proofs**:
  1. **Intent Proof**: Is the change unrelated to the required behavior or instruction effect? A declaration moved to fix scope, timing, or ordering is semantic and does not qualify.
  2. **Canonical-Equivalence Proof**: Are the before/after artifacts structurally identical after only safe normalization (for example, the same parsed code structure, Markdown structure plus instruction text, or resolved dependency graph)?
  3. **Significance Proof**: Is the changed whitespace, order, line ending, or metadata inert for this language and repository? Never assume imports, indentation, file modes, comments, snapshots, or generated output are cosmetic.
  4. **Revert-Safety Proof**: Can the cosmetic delta be restored to the base representation while required formatter, generator, build, and test checks remain green?
* **Action**: **Restore representation only** (revert cosmetic hunks or regenerate with the repository's expected tool). Never rewrite semantics or hand-edit generated output under this lane.
* **Deep playbook**: [`references/lane-3-diff-noise.md`](references/lane-3-diff-noise.md) — finding decomposition, canonical proofs by artifact type, mixed-hunk ownership, and fail-closed traps.

---

### Lane 4: Edge-Case Trades (80/20)
* **Target**: Live, working code in code/config files whose only job is a rare case: retries for rare races, special-case error messages, defensive try/catch around recoverable steps, and guards stricter than the repo's precedent.
* **Core Philosophy**: **Name the loss, then let the user trade**. Find code that can go if we accept losing a rare case, so the diff shrinks where it buys the least. Never present a trade as equivalent.
* **The 5 Trade Proofs** (all must hold):
  1. **Frequency**: What triggers the case, and how rare is it? Unknown frequency raises the risk.
  2. **Consequence**: Without the handling, does the user see a visible, recoverable error? Silent wrong results, data loss, duplicate charges, or leaks are not tradable.
  3. **Recovery**: Is there a cheap way out, such as retrying or pasting again?
  4. **Precedent**: How do sibling features handle the same case? Handling above precedent is tradable; below it is not, and handling required by a repo rule stays.
  5. **Savings**: Which lines, tests, constants, helpers, and concepts disappear? Small savings with a real loss is not worth recommending.
* **Hard floor**: Security and auth, tenant or user isolation, data integrity, money, and privacy may only come down to the repo's precedent, never below it, and the finding says a security reviewer should confirm.
* **Action**: **Recommend the trade with its loss stated**; once approved, delete the handling and everything that only served it, and update docs that describe the dropped case.
* **Deep playbook**: [`references/lane-4-edge-case-trade.md`](references/lane-4-edge-case-trade.md) — targets, the 5 proofs, the hard floor, and example rows.

---

## Workflow

```text
1. Resolve Scope  ──►  2. Adaptive Diagnosis  ──►  3. Present Evidence  ──►  4. Ask Approval  ──►  5. Tidy & Verify
  (Prompt or Flag)      (Route by lane name)        Unified Table             (ask_question)       (Tests green)
```

---

### Step 1: Resolve Scope

Confirm the diff boundary before auditing. Default to uncommitted changes unless specified:

* **Uncommitted working tree** (staged + unstaged git diff) — *default*
* **Branch vs base** (e.g. `origin/main...HEAD` or `main...HEAD`)
* **Last N commits** (e.g. `HEAD~2..HEAD`)
* **Specific file or path**

If the target is ambiguous, prompt the user with `ask_question`.

---

### Step 2: Adaptive Diagnosis & Lane Routing

Inspect the requested outcome, surrounding context, and diff. Route **reducible findings**, not files blindly:

1. **Decompose the diff**:
   - Use `git diff` hunks as input, then separate independent findings when safe.
   - If cosmetic lines are inseparable from a semantic edit, the semantic lane owns the whole finding.
   - Keep intentional, necessary, well-placed changes without manufacturing a tidy recommendation.
2. **Check standalone cosmetic candidates across all file types**:
   - Compare base and changed artifacts with repository-appropriate parsers, formatters, or normalized representations.
   - Route to **Diff noise** only when all 4 proofs hold. No proof means keep it out of this lane.
3. **For semantic changes in code/config files (`.ts`, `.py`, `.go`, `.rs`, etc.)**:
   - Trace the call graph upwards to find callers. Flag unreferenced symbols and zombie chains under **Dead code**.
   - Search sibling features, the standard library, and dependency options by purpose for anything new code reimplements. Flag duplicates under **Dead code**.
   - List the cases each branch, catch, retry, fallback, special message, and extra check exists for. Run the 5 trade proofs and flag rare-case handling worth giving up under **Edge-case trade**. Run this lane on every tidy, even when the user did not ask for trade-offs.
4. **For semantic changes in prompt/instruction files (`.md`, `.prompt`, `.cursorrules`, etc.)**:
   - Audit changed lines against the 5 prompt proofs under **Prompt bloat**.

---

### Step 3: Present Unified Evidence & Diagnosis Table

Output a clean, scannable table grouped by lane before modifying any code. In the Lane column, use the short labels (**Dead code**, **Prompt bloat**, **Diff noise**, **Edge-case trade**) — never lane numbers. **What we lose** is `—` for every lane except **Edge-case trade**, where it states the lost case from the user's side.

```markdown
### 🧹 Tidy Audit Results (Scope: uncommitted diff)

| Lane | Target | Issue / Evidence | Proposed Action | What we lose | Risk |
|---|---|---|---|---|---|
| **Dead code** | `src/utils/date.ts:L40` (`formatDateV2`) | **Reachability**: 0 callers across repo. | Delete dead helper | — | Low |
| **Dead code** | `src/types/user.ts:L15` (`DraftRole`) | **Breakage**: Unreferenced enum variant. | Delete variant | — | Low |
| **Prompt bloat** | `skills/deploy/SKILL.md:L18` | **Default Knowledge**: Explains how git commit works to the model. | Cut line | — | Low |
| **Diff noise** | `src/routes/admin.ts:L20-L45` | **Canonical equivalence**: Formatter-only delta; parsed structure is unchanged and format check passes after restore. | Restore base formatting | — | Low |
| **Edge-case trade** | `src/connect/service.ts:L120-L134` (retry on 400) | **Frequency**: only when two users connect the same site within a second. **Recovery**: connecting again succeeds. **Precedent**: no other connector retries. | Drop retry, `RETRY_DELAY_MS`, `delay()`, and its test | One of two simultaneous connects fails and must be retried | Low |
```

If no rare-case handling passes the 5 trade proofs, say so in one line under the table instead of omitting the lane silently.

---

### Step 4: Request Explicit User Approval

**Never alter files or delete code without human sign-off.**

Prompt the user using `ask_question`:
* **Question**: "How would you like to proceed with the tidy recommendations?"
* **Options**:
  1. `(Recommended) Apply all recommendations (dead code, prompt bloat, diff noise, and edge-case trades)`
  2. `Apply only behavior-preserving cleanup (dead code + prompt bloat + diff noise; skip edge-case trades)`
  3. `Let me select specific items from the table`
  4. `Cancel (Keep working tree unchanged)`

Omit option 2 when there are no edge-case trades.

---

### Step 5: Surgical Tidy & Verification

Once approved:
1. **Apply diff noise**: Restore approved cosmetic-only findings to their base representation; use the expected generator/formatter instead of hand-editing generated files.
2. **Apply dead code**: Delete dead functions, types, and unreferenced imports.
3. **Apply prompt bloat**: Strip bloat from prompt/instruction docs within the diff window.
4. **Apply edge-case trades**: Delete the approved handling and everything that only served it (constants, helpers, imports, tests). Keep a test that the main path still works, and update docs and comments that describe the dropped case.
5. **Preserve Load-Bearing Context**: Keep load-bearing comments and intent notes intact.
6. **Run Verification**:
   - Run tests (`npm test`, `pytest`, `cargo test`, `go test`).
   - Run type checks / builds (`tsc`, `mypy`, `cargo check`).
   - If tests fail, fix immediately or revert the offending change.
7. **Report Summary** (lead with lane names, not numbers):
   - What changed under **Dead code**, **Prompt bloat**, **Diff noise**, and **Edge-case trade**
   - For each applied trade, the case the code no longer handles
   - Lines removed / added
   - Files cleaned or reverted to clean state
   - Verification status (e.g. `All 36 tests passing green`)

---

## Do / Don't

- **Do** treat dead-code deletion (**Dead code**), prompt shaking (**Prompt bloat**), cosmetic restoration (**Diff noise**), and rare-case trades (**Edge-case trade**) as distinct, mutually exclusive disciplines.
- **Don't** rewrite a working architecture; tidy subtracts.
- **Do** prove reachability with a concrete call graph before claiming code is dead.
- **Don't** say "this looks unneeded" without citing callers and requirements.
- **Do** search sibling features by purpose before keeping new code that solves a problem the repo already solved.
- **Don't** cut behavior outside **Edge-case trade**, and never call a trade equivalent or "minimized"; every trade names what is lost.
- **Don't** trade security, isolation, data integrity, money, or privacy below the repo's precedent.
- **Do** read why a line moved and prove canonical equivalence before calling it cosmetic.
- **Don't** classify imports, declaration moves, whitespace, generated files, or file modes as noise from appearance alone.
- **Do** fail closed: uncertain cosmetic candidates stay in the diff and out of **Diff noise**.
- **Do** require explicit human approval via `ask_question` before modifying code.
