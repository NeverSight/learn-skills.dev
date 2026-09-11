---
name: hrt-dark-mode-routing
description: "Single source of truth for where an escalation-worthy finding goes when tempa-spec's dark mode is active (dark.md exists). Each of proposal, specs, design, align, and apply points here instead of inlining its own dark-mode carve-out. Says which findings route to hrt-dark-mode-decision-gate, which still go to the user, and which dark.md section records the result."
---

# hrt-dark-mode-routing

`dark.md` existing is the only signal dark mode is active (created by `hrt-dark-mode-opt-in`). This skill holds the routing rules that were previously copied into every phase instruction. A phase instruction points here with one line; the rules live here.

If `dark.md` does not exist, this skill does nothing — every finding follows its normal path to the user.

## The rule, by calling phase

A finding that would normally escalate to the user is routed as below. Everything that auto-resolves outside dark mode still auto-resolves — dark mode never changes the auto-resolve rule, only where the *non*-auto-resolved findings go.

| Phase | Routes to `hrt-dark-mode-decision-gate` | Still goes to the user | `dark.md` section |
| --- | --- | --- | --- |
| `proposal` (`hrt-adversarial-authoring`, artifact: proposal) | a single-reviewer UNANCHORED finding | everything the security skills decided; the `hrt-change-size-gate` "one change or several?" question | Proposal |
| `specs` (`hrt-adversarial-authoring`, artifact: specs) | a single-reviewer UNANCHORED finding | everything the security skills decided | Specs |
| `design` (`hrt-adversarial-authoring`, artifact: design) | a single-reviewer UNANCHORED finding | everything the security skills decided | Design |
| `align` (`hrt-align-consistency-review`) | every ALIGN DECISION and HIGH finding | nothing extra — but VERIFY and WALKTHROUGH are unchanged, and WALKTHROUGH stays the mandatory closing review; the user is also shown `dark.md` | Align (tag each entry with its cycle number) |
| `apply` Phase 1 (`tdd` loop) | a seam-mismatch blocker (the gate can weigh an alternative seam against code, design, and specs) | any other Phase 1 blocker | Apply |
| `apply` Phase 2 (`hrt-apply-code-review`) | every finding that would otherwise surface to the user | nothing extra | Apply |

## Invariants across all phases

1. ANCHORED findings, and findings both independent reviewers raised, auto-resolve in the calling skill and never reach this routing at all.
2. A finding that is a security requirement or mitigation already decided by `stride-analysis-patterns` / `threat-mitigation-mapping` / `security-requirement-extraction` ALWAYS goes to the user, never to `hrt-dark-mode-decision-gate`. That decision is a hard constraint, not an opposing case to weigh.
3. The `hrt-change-size-gate` "one change or several?" question ALWAYS goes to the user. The answer depends on the user's capacity and priorities, which no grounding artifact holds.
4. WALKTHROUGH in `align` stays mandatory and fully manual in every dark-mode variant.
5. `hrt-dark-mode-decision-gate` is always a fresh subagent, always writes its reasoning to the matching `dark.md` section, and never escalates to the user from within itself — it always produces a decision. See that skill for the steel-manning procedure.

## Planning-only vs +implementation

`dark.md`'s header names the variant.

- **planning-only**: routing applies through `align`. `apply` is out of scope — if `dark.md`'s header is planning-only, `apply` STOPS and tells the user planning-only dark mode ends at WALKTHROUGH.
- **+implementation**: routing also applies to `apply` Phase 1 and Phase 2 as in the table. After Phase 2, `dark.md` is presented in full alongside the code diff as a second closing review before the user commits.
