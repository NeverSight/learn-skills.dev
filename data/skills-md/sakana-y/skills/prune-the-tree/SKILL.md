---
name: prune-the-tree
description: Prune low-value questions while preserving decisions that belong to the user. Use only when the user explicitly invokes $prune-the-tree.
---

# Prune the Tree

Keep the trunk. Prune the branches.

Act as a Modifier Skill for the current User Problem: the outcome and boundaries the user has authorized. Stay active across turns until that problem is resolved or the user asks to return to normal questioning. The active task and its skills retain ownership of the work.

Optimize Decision Load — the user's effort and synchronous interruption — rather than question count or model reasoning time. Use no numeric question budget.

## Route Before Asking

Before sending a question, route every candidate on the current frontier. The Decision Boundary has precedence: an unresolved user-owned choice may enter DEFER until its decision point, but convenience or convention cannot turn it into FIND, DROP, or DEFAULT.

- **FIND** — The repository, conversation, documentation, tools, or environment can supply a fact or an authoritative decision already made. Investigate and use the result. A convention may support DEFAULT but cannot settle a user-owned choice. If the answer remains unavailable, route it to ASK when material and DROP when immaterial.
- **DROP** — An exact prior answer or constraint already settles it, it duplicates another candidate, or no choice remains relevant to the User Problem. Remove it from the frontier. If one of several equivalent implementation choices must still be selected, route it to DEFAULT.
- **DEFAULT** — The choice falls on the delegated side of the Decision Boundary and satisfies every condition below. Choose the evidence-backed default and proceed.
- **DEFER** — The decision is real, but a named prerequisite is unresolved or its decision point has not arrived. Keep it pending, route it again as soon as that prerequisite resolves, and settle it before any dependent descendant enters the frontier. DEFER never exists merely to shorten a question round.
- **ASK** — The decision belongs to the user or reaches a mandatory human checkpoint. Ask with a recommendation and state the concrete difference between the viable answers.

Apply this routing before another active skill formats its questions. Only ASK candidates enter that skill's user-facing frontier; its ordering, output format, work, and mandatory safety, authorization, external-effect, and human checkpoints remain in force.

## Decision Boundary

DEFAULT requires every condition below:

- It selects an implementation means rather than changing what the user receives.
- A repository signal, established convention, or strong evidence supports one default.
- It is a local leaf choice with little downstream fan-out.
- It is cheap and fully reversible before the next checkpoint.
- It stays inside the authorized scope and has no external effect.
- The user has not recently corrected a related assumption.

Route a choice to ASK when it defines goals, non-goals, the concrete failure being solved, acceptance criteria, hard constraints, user-visible alternatives, values or taste, domain rules or terminology, public contracts, persistent data, new authorization, external or destructive effects, security posture, costly or irreversible commitments, or an upstream decision that governs multiple branches. Resolve the concrete failure and hard constraints before any product or architecture choice they could govern; unstated constraints are not evidence that none exist. When classification remains uncertain, use ASK.

Promote a DEFAULT to ASK before later work makes it load-bearing, externally visible, or costly to reverse.

## Decision Ledger

At the next natural checkpoint, and always by completion, report only material DEFAULT choices in a compact Decision Ledger. For each, state the choice, its basis, and what a veto would change. Omit routine details such as formatting, local names, and ordinary tool commands; omit the ledger when it would be empty.

If the user vetoes a default, revise it and reroute every downstream choice that depended on it.

## Completion

Before sending a question round, every surfaced candidate has a route and only ASK remains user-facing; no unresolved user-owned ancestor remains in DEFER behind a downstream question. Before completing the User Problem, every relevant candidate has a terminal disposition: FIND is resolved, DROP is eliminated, DEFAULT is chosen and disclosed when material, and ASK is answered. Promote any remaining relevant DEFER to ASK or an explicit blocker. End this modifier when the User Problem is resolved or the user disables it.
