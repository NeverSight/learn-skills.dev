---
name: distill
description: Turns a vague software request into a compact implementation brief with actors, triggers, preconditions, behavior, failures, permissions, data effects, edge cases, and observable acceptance conditions. Use before planning when product intent or scope is ambiguous.
---

# distill: weak request in, sharp brief out

A great brief removes ambiguity. It does not add volume. Your output should
be executable by a weaker model without access to this conversation: every
fact it needs is on the page, and nothing on the page is filler.

## When to use

- "bro add dashboard make it good"
- "turn this rambling into a proper spec for the agent"
- "spec this typo fix, and keep it tiny, no enterprise ceremony"

## When NOT to use

- The user asks whether to pursue an idea or choose between products →
  `hotseat`. An uncritiqued idea alone does not require debate.
- The request is already precise → the current owner can execute it; use
  `masterplan` only when complexity warrants planning.
- The task is a small mechanical fix ("rename this variable") → just do it.

## Prerequisites

The triggering request. A quick look at the repository for context (what
exists, what conventions apply): lighter than a `spelunk` pass; read only
what the request names or obviously touches.

## Evidence, authority, and assumption model

Distill clarifies intent; it does not silently become a product owner,
architect, security approver, or implementation agent. Separate all brief
content into these classes:

| Class | Meaning | Treatment |
| --- | --- | --- |
| Confirmed fact | user statement or observed repository evidence | cite compactly |
| Constraint | explicit requirement, policy, compatibility, budget, or authority limit | preserve verbatim when material |
| Assumption | reasonable choice that does not need user input yet | number it and make it falsifiable |
| Open decision | plausible answers materially change outcome | ask or route to hotseat |
| Suggestion | non-binding improvement beyond the request | isolate; never smuggle into scope |

Never infer permission to delete data, break a public contract, change pricing,
send external communication, access production data, spend money, or deploy.
Those are explicit approval boundaries in the brief when relevant.

## Brief decision framework

Distill only the ambiguity that matters to a downstream implementer. For each
candidate detail, ask: does an alternative change user outcome, scope, data,
permission, compatibility, risk, verification, cost, or release behavior? If
not, omit it or make a narrow assumption. If yes, decide it, ask it, or record
it as a deliberately unresolved decision with a safe discovery step.

Write observable requirements as behavior under conditions:

| Situation | Requirement form (EARS: While, optional; When, optional; system; shall) |
| --- | --- |
| Ubiquitous behavior | The system shall <response> |
| Triggered behavior | When <trigger>, the system shall <response> |
| Conditional behavior | While <condition>, the system shall <response> |
| Optional-feature behavior | Where <feature is included>, the system shall <response> |
| Failure/exception | If <failure>, then the system shall <safe response> |
| Prohibition/invariant | The system shall not <forbidden outcome> |

The form is a tool, not a ritual. Pair each material requirement with an
oracle: visible result, returned contract, persisted state, log/audit event, or
testable absence of a forbidden side effect. "Intuitive", "fast", "secure",
and "production-ready" are labels until their observable condition is named.

## Scale the brief to the request

| Request type | Brief shape |
| --- | --- |
| **tiny task** (button rename, copy fix) | goal + acceptance criterion + where + one-line Non-goals + one numbered assumption (A1:): 7-12 lines, no other ceremony |
| **feature** | full template below |
| **large feature / migration** | full template + NFRs, rollout constraints, backward-compatibility and data-migration notes |
| **bug/change request** | reproduction facts + expected behavior + scope guard (what NOT to fix along the way) |
| **greenfield product** | full template + target user + success metric; defer tech choices to `masterplan` unless the user named them |

A brief for a button rename that mentions "non-goals" and "rollout" is
enterprise cosplay: match depth to blast radius.

## Workflow

### 1. Extract the goal

Restate the request as one sentence: *what* will be true after the work
that isn't true now, *for whom*. If you cannot write this sentence, that's
a clarifying question, not a brief.

### 2. Ground in the repo first (lightly)

Before drafting a single question, confirm the surfaces the brief touches
actually exist: the page/module named, the data involved, the commands
available. Briefs referencing nonexistent files are how hallucinated work
starts. Most "ambiguities" die here: what remains is genuinely missing.

### 3. Ambiguity detection (max 5 questions)

Actively scan the request for linguistic, semantic, and functional
ambiguities. List what's genuinely blocking:
- Undefined boundaries ("make it fast" → what is the target metric?)
- Contradictory constraints
- Missing definitions of "good" or failure states

For each candidate question, apply the materiality test: name the two most
plausible answers and what each would change about implementation, security,
data handling, or UX. If nothing material changes, it is not a question,
it becomes an explicit numbered assumption in the brief.

Ask **only blocking questions, max 5, in one batch**. Anything non-blocking
becomes an explicit numbered assumption in the brief. Never run a
back-and-forth interrogation.

### 4. Write the brief

Use the template in `references/brief-template.md` (it includes a filled
example). Core sections:

- goal (one sentence) + user outcome;
- context: relevant existing pieces, with file paths;
- constraints and conventions to respect;
- scope: what's in;
- non-goals: what's explicitly out (as valuable as scope);
- agent-executable specifications: statements another agent can objectively verify without human judgment;
- edge cases: empty/loading/error/malformed states worth handling;
- non-functional requirements **only when they bite** (performance
  budget, accessibility bar, i18n, security constraint): omitted means
  "nothing beyond the project's existing bar";
- backward compatibility / migration notes when existing data or users
  are affected;
- UX expectations (only if user-facing);
- verification: how "done" gets **proven**: which commands must pass,
  what a human/browser check confirms;
- known unknowns + numbered assumptions.

### 5. One-pass confirmation

Show the brief with unresolved decisions distinguished from safe assumptions.
If the user authorized implementation and no material decision remains, proceed
within that scope; a brief is not a new approval gate. If the user requested
only requirements, deliver them and stop. Ask only for a load-bearing answer.

### 6. Run the implementation-readiness review

Read the finished brief as an implementer with no conversation history and
apply the review in `references/brief-template.md` (Implementation-readiness
review): every item must pass before the brief ships.

If a missing item would change implementation substantially, ask the compact
question batch or return a conditional brief. Do not conceal ambiguity in
polished prose.

## Failure handling and scope change

- **Conflicting user statements:** quote the conflict neutrally and ask for the
  decision; do not choose the more convenient interpretation.
- **Repository contradicts request:** preserve the request, report the observed
  conflict and path, then offer a revised scope or discovery task.
- **Unsettled product tradeoff:** frame options, consequences, and evidence
  needed; route to hotseat instead of pretending it is a requirement.
- **Insufficient repository access:** emit a provisional brief with every
  path/command marked assumption, then name the minimum inspection needed.
- **Mid-implementation scope change:** update the goal, scope, non-goals,
  affected acceptance criteria, and assumptions together. Do not patch only a
  task line while leaving the original definition of done misleading.
- **Approval-bound action:** stop at a precise decision/authorization request.
  The brief may specify preparation but not authorize execution.

## Anti-bloat rules

- Every line must remove ambiguity or it gets deleted.
- No restating general knowledge ("React is a component library"): the
  reader is a coding agent, not a student.
- No invented requirements the user never implied. Suggestions go in a
  clearly marked non-binding suggestions list.
- Stop when the brief removes implementation-blocking ambiguity; brevity is a
  quality signal, not a fixed line target.

## Tool selection / fallback

- Repository artifacts and the user's words outrank generic templates.
- Ask only when alternatives materially change behavior, data, permissions, or risk.
- Without repository access, produce a provisional brief and label path or command assumptions.

## Quality gates

- A reader who never saw this chat could implement without guessing on
  scope: test your draft against this before showing it.
- Every agent-executable specification is objectively checkable by another agent without human intervention.
- The verification section names real commands/checks (that exist in this
  repo or are standard).
- Assumptions are numbered and falsifiable ("A1: single-user, no roles").
- Marker floor (applies at every scale, including compact briefs): the
  brief contains a literal `Non-goals` line and at least one numbered
  assumption (`A1:`), even if each is a single line. A brief without
  these markers is incomplete, not concise.
- Auth-bites rule: when the request touches login, identity, per-user
  data, sessions, tokens, passwords, or money, the brief names that
  surface explicitly (one line suffices, e.g. under Scope or NFRs).
  Omitting it because the brief is short is a miss, not brevity.

## Stop conditions

- Brief removes blocking ambiguity → deliver for a requirements-only request;
  otherwise continue the already-authorized next action. Use `masterplan` only
  when the implementation needs it.
- The request reveals an unsettled product decision → stop and route back
  to `hotseat` for that decision.

## Output contract

In chat: the brief. On disk (when the task will span sessions or feed
planning): `docs/briefs/<slug>.md` with provenance header
(`<!-- generated by distill on YYYY-MM-DD -->`).

`<slug>`: short kebab-case text derived from the task title.

## Research basis

Read [references/research.md](references/research.md) when a decision depends on
an external standard, a numerical claim, or a fast-moving practice. The ledger
records what the source supports, what it does not support, and when to reverify.
