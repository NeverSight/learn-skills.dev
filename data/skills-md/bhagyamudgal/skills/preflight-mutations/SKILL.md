---
name: preflight-mutations
description: Prepare or block a shared-state write. Use immediately before changing shared or remote state (issue, PR, board, publication), published Git history, production-like data or live services, or an off-box copy.
---

# Preflight mutations

I resolve permission, current state, dependencies, and recovery before a shared-state write. I produce a decision record here. I never perform the mutation itself. That separation is the point.

## 1. Define the mutation batch

I record one batch whose items share the same authorization and guards. I split actions with different targets, owners, environments, reversibility, or confirmation requirements into separate cards.

I render a simple card inline. For a multi-step or multi-batch run, I persist it only in an existing artifact the user has already authorized this workflow to write. I do not create a file, comment, issue, or other external artifact merely to store a preflight.

```markdown
### Mutation card

- **Surface / environment:** <system and local | staging | production | shared>
- **Action:** <exact mutation verb and delta; no combined "update as needed" language>
- **Targets:** <stable IDs, URLs, refs, fields, recipients, or services>
- **Ownership policy:** <governing policy and owner/assignee/author/environment boundary>
- **Authorization source:** <user request or later explicit confirmation, quoted narrowly>
- **Current guards:** <state, base/head SHA, version, field, environment, or other compare-before-write facts>
- **Dependencies / consumers:** <direct dependencies; transitive consumers when destructive or history-rewriting>
- **Preview / exclusions:** <proposed delta, blast radius, and what will not change>
- **Reversibility:** reversible | compensating-only | irreversible
- **Recovery plan:** <undo, backup, compensation, or explicit absence>
- **Invalidators:** <facts that make this preflight stale>
- **Read-back plan:** <authoritative post-write query and expected result>
- **Batch items:** <stable item ID → pending | landed | failed | skipped | reconcile-required>
- **Verdict:** ready | confirmation-required | blocked
- **Next action:** <one action permitted by the verdict>
```

I keep the action, targets, environment, and batch-item IDs exact enough that another agent cannot select a broader resource by inference. A multi-step or multi-batch card needs an authorized durable home, and I state that as the gate. **Gate.** both: nothing selectable by inference, every multi-step card homed.

I name every target and guarded dependency by stable ID in **Read-back plan**. I never collapse them into "all targets" or "consumers" or another referential phrase.

## 2. Resolve authority and ownership

I apply the target surface governing ownership policy. Technical write access does not expand the user requested scope and does not override assignee, author, resource-owner, or environment boundaries.

I state that access-versus-authority distinction in **Ownership policy** whenever the evidence shows technical access beyond the authorized boundary.

A specific user request authorizes ordinary `reversible` writes only within its named action and targets. I require fresh explicit confirmation for restructuring like splitting, grouping, closing-with-successor, or rebasing a dependency, for production data or operations, service downtime, and off-box recipients, for resources outside the governing ownership boundary, for `compensating-only` or `irreversible` actions, and for rewriting or deleting published history.

I do not treat approval for one action class as approval for another. I record the exact authorization source in the card.

**Gate.** Ownership is resolved and authorization covers the exact batch, or the verdict cannot be `ready`.

## 3. Inspect guards, dependencies, and publication

I read current state from the authoritative system immediately before the batch.

- For ordinary writes I inspect direct dependencies and current compare-before-write guards.
- For deletion, closure, base changes, and history rewrites I traverse transitive consumers such as stacked PRs, dependent branches, linked issues, workflows, releases, umbrella records, and downstream services.
- For Git history I compare local refs with their upstreams and consumers. When a commit or ref is published or consumed, I put the append-only corrective commit or successor-ref alternative in **Preview / exclusions** and surface that choice in **Next action**. I classify its rewrite or deletion as `compensating-only` at best because restoring a ref cannot undo publication or downstream consumption. It stays `confirmation-required`.
- For production-like UI or operations I verify environment, record ownership, snapshot affected records when possible, and name the captured prior values plus restoration or compensation steps. When downstream billing, entitlement, notification, or audit effects persist after restoring the primary record, I classify the action as `compensating-only`.
- For off-box copies I resolve the recipient, included sensitive material, retention, and revocation or deletion path.

I put every target stable ID plus every mutable fact that protects its write in **Current guards** and **Invalidators**.

**Gate.** Required dependencies and consumers are enumerated from current evidence. An unknown dependency on a destructive action yields `blocked`.

## 4. Preview blast radius and recovery

I show a user-visible preview before ambiguous restructuring, high-volume changes, production operations, ownership expansion, and `compensating-only` or `irreversible` actions. I include targets, proposed delta, exclusions, dependencies, blast radius, and recovery path.

I classify recovery in one of three ways. `reversible` means a direct undo restores the captured prior state. `compensating-only` means the original event remains, but a follow-up action can restore its practical effect. `irreversible` means no reliable restoration exists.

For `reversible` I identify the captured prior value or exact undo. For `compensating-only` I name every recovery target by stable ID and its captured prior value in **Recovery plan**, then specify the compensation and residual trace. For `irreversible` I state the permanent loss. Missing recovery evidence yields `blocked`, not optimistic classification.

**Gate.** The preview and recovery evidence match the mutation volume, environment, ambiguity, and reversibility class.

## 5. Assign one verdict

- `ready` means the exact batch, ownership, authorization, current guards, dependency evidence, recovery, and read-back plan all satisfy the gates, and no fresh confirmation category applies.
- `confirmation-required` means the evidence and preview are complete, but this action class requires a fresh explicit user decision. I present the card and ask for that decision. I do not mutate.
- `blocked` means required target, ownership, authorization, dependency, recovery, or guard evidence is missing or unsafe. I name the evidence or authority needed. I do not mutate.

A multi-step or multi-batch run without an already-authorized durable home is `blocked`. **Next action** names the existing workflow artifact to use or the authorization needed to write it. I do not create persistence state merely to clear this gate.

Fresh confirmation updates **Authorization source** but does not waive any other gate. I re-read the invalidators after confirmation before changing the verdict to `ready`.

I write **Next action** as a self-contained instruction naming the exact action and targets. I do not hide them behind "this operation" or "the above" or another referential phrase.

## 6. Hand off execution and preserve partial state

I pass the `ready` card to the workflow that owns the mutation. Immediately before each write, I compare its guards. Any changed target, action, ownership, dependency, head, publication status, environment, or approval invalidates `ready`. I stop the unexecuted remainder and re-preflight it.

Every caller follows the same result contract. It continues only when **Verdict** is `ready` and **Invalidators** still match. On `confirmation-required` it presents the card and waits for the named confirmation. On `blocked` it stops the mutation and reports **Next action**.

The execution handoff must use the surface native conditional-write mechanism when one exists, meaning expected versions, compare-and-swap tokens, exact-SHA leases, or idempotency keys. A recovery push for published Git history must also stay lease-guarded against the re-read remote head.

After each attempted item, I record `landed`, `failed`, `skipped`, or `reconcile-required`. I use `reconcile-required` when the command result and authoritative read-back cannot establish whether the write landed. I stop that item. I do not retry it or classify it as `failed` until an authoritative query resolves its state.

On interruption, invalidation, or `reconcile-required`, I preserve the item ledger, authoritatively re-read every `landed` item, record the observed partial external state, and create a new card whose **Targets** cover only the safe `pending` remainder, while **Batch items** carries the authoritative `landed`, `failed`, `skipped`, and unresolved `reconcile-required` history alongside those pending items.

I exclude every `reconcile-required` item from the new card write targets. Its **Next action** is the exact authoritative query needed to resolve that item. Only the observed result may move it to `landed`, `failed`, or `pending`.

I never restart from an assumed zero state. The execution workflow owns writes. `verify-claims` may validate consequential post-write claims, and the final completion workflow owns its acceptance-surface verdict.

**Done.** The card is populated, its verdict matches the gates, and no shared-state mutation has been performed by this skill.
