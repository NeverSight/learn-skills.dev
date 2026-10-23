---
name: awesome-design-doc
description: "Writes a design doc or ADR: requirements and scale first, real alternatives with trade-offs, a grounded recommendation, non-goals, migration path; also runs a pre-mortem on a plan. Use when choosing an approach."
license: MIT
metadata:
  author: Khasky
  tags: ["design", "adr", "architecture", "planning"]
  documentation: "https://github.com/khasky/awesome-agent-skills/tree/main/skills/awesome-design-doc"
---

# Design Doc / ADR

Turn a feature request or architectural question into a decision a team can execute and a future reader can retrace. The core discipline: requirements and numbers before components, real alternatives before a recommendation, and a recommendation before the end — a document that tours options without choosing is a meeting agenda, not a design.

## When to Activate

- "Design X", "how should we build Y", "write a design doc / ADR / RFC".
- A reviewer flagged a load-bearing decision that needs an ADR (awesome-code-review hands the format here).
- Two credible approaches exist and the choice is expensive to reverse.

Do not activate for reversible everyday choices (naming, a helper's location) — an ADR for those is noise; the three-condition test below decides.

## When an ADR is warranted

All three, or don't write one:
1. Expensive to reverse — schema, public API shape, persisted format, event name, framework/storage choice, service boundary.
2. Crosses a boundary — more than one module, team, or service must honor it.
3. The context would be lost — six months from now, the "why" is not recoverable from the code.

One-page ADR for a single decision; full design doc when the feature needs a data model, API surface, and rollout plan together.

## Work Process

1. Requirements before components — functional requirements as testable statements, each with a stable label the rest of the document cites and the mandatory ones listed apart from the desirable ones, then the constraints that shape the design: expected scale (users, QPS, data volume and growth), latency targets, consistency needs (what must be read-your-write, what can lag), availability expectations, compliance boundaries, and who will operate and maintain the result — what the team already knows how to run is a constraint like any other. Getting the scope wrong makes a technically impressive design solve the wrong problem — clarify with the user before designing, not after. Read the decisions already recorded (existing ADRs) and the project's own glossary before naming anything: a design that renames a concept the codebase already has costs every reader a translation, and one that silently contradicts an accepted ADR gets re-litigated in review instead of decided here.
2. Back-of-envelope the load — requests/sec, storage/year, working-set size, fan-out per action. Three lines of arithmetic kill more bad designs than any diagram; a design without numbers is a vibe. State the assumptions so a reader can re-run the math when the assumptions age. Close with one line of monthly running cost at that scale and the item that dominates it — an order of magnitude from the same arithmetic, not a price list.
3. Sketch the contract before the internals — the API endpoints or events in/out, and the data model's core entities with their invariants. The contract exposes scope errors while they are still cheap (`awesome-api-design` for HTTP resource detail). Ground it in the code first: find the nearest existing implementation of the same kind, and list by search — not from memory — every caller or consumer the contract change touches. A design that puts a second pattern beside the incumbent says why the incumbent cannot carry it, and every consumer found appears in the rollout.
4. Generate 2–3 genuine alternatives — including the simplest thing that could work ("do nothing" or "a cron job and a table" is often a legitimate contender). An alternative added only to be knocked down is padding; each one gets its honest best case.
5. Evaluate on the trade-off axes the requirements activate — not a fixed rubric: consistency vs availability, sync vs async, SQL vs NoSQL, monolith-extension vs new service, build vs buy, latency vs cost, technology the team already runs vs one new to it. For each active axis, say which side the requirements favor and why; an alternative nobody on the team can operate does not win on the technical axes alone. Skip axes with no tension — padding dilutes the load-bearing analysis.
6. Recommend, grounded in requirements — one recommendation, tied by label to the requirements that drove it ("eventual consistency suffices because the feed tolerates 30s lag — that unlocks the cheaper fan-out-on-read"). State what new information would flip the decision, and the design's ceiling: the number from step 2 at which it stops working, the component that breaks first, and the next move then — one sentence, not a phased roadmap. When an unknown flips the choice between alternatives, do not guess it: the doc prescribes a time-boxed spike — one question, a done criterion, a decision date, and which outcome picks which alternative — and carries it under Open questions until it is answered.
7. Invert before you mitigate, then name non-goals and the path — run the risk pass backwards first: it is a year on, this decision was the wrong one, and the design is being unwound. Name the three things that killed it, in the concrete ("the backfill never finished and writes diverged"), never the abstract ("scaling risk"). Inversion surfaces what a forward pass rationalizes away, because "what would kill this" cannot be answered with "we will be careful". Each named cause then earns an early warning sign a reader could actually observe and either a mitigation or a written acceptance. Then explicit non-goals (what this deliberately does not solve, so scope creep has to argue with a sentence), the top risks with their mitigations, the migration/rollout order for existing data and consumers, and the rollback story (a design that cannot roll out incrementally gets that called out here, not discovered in the PR). The rollback criterion is fixed in advance as a number — the metric, the threshold, the window — with the observable signals to watch in each rollout window, so nobody argues it mid-incident. Name the point of no return: after a contract step (a column dropped, an old path removed) or once the first writes in the new format exist, rollback becomes roll-forward, and the doc says what to do past that point.

## ADR format

```text
# ADR-<n>: <decision, stated as a decision>
Status: proposed | accepted | superseded by ADR-<m>
Date: <date>

Context: <the forces — requirements, constraints, numbers — that make this a decision at all>
Decision: <what we will do, one paragraph, active voice>
Alternatives considered: <each with its honest best case and why it lost against the requirements>
Consequences: <what becomes easier, what becomes harder, what debt is accepted knowingly>
Non-goals: <what this decision deliberately does not cover>
```

## Agent brief (when the decision is handed to an implementer)

A design doc explains a decision to a reader; a brief tells an implementer — a person or an unattended agent — what to build. When the work is handed off rather than built in the same session, add one per unit of work, and write it to survive the wait: the brief may sit for days while the codebase moves under it.

Durability over precision. Describe interfaces, types, config shapes and behavioral contracts; never file paths or line numbers, which go stale and send the implementer to a file that no longer exists. Say *what* the system should do, not *how* to change the code — the implementer explores the current tree and makes its own implementation decisions.

```text
## Brief: <one-line summary of what must happen>

Category:          feature | bug | migration
Current behavior:  <what happens today — the status quo the work builds on>
Desired behavior:  <what happens after, including edge cases and error conditions>
Key interfaces:    <the types, signatures, events or config shapes that change, and how>

Acceptance criteria:
- [ ] <requirement label> <specific, independently verifiable — "returns 409 on a duplicate
      idempotency key", not "handles duplicates correctly">

Out of scope:      <the adjacent thing that must NOT be touched, so gold-plating has to argue>
```

Where the decision splits into several briefs, publish them in dependency order and let each name the briefs that block it, so the ready set is readable without re-reading the doc.

## Output

Full design doc: Title → Problem & requirements (with numbers) → Proposed design (contract first, then internals) → Alternatives & trade-offs → Recommendation → Non-goals → Risks & mitigations → Rollout & rollback → Open questions (marked, not hidden). Deliver as a Markdown file in the repo's docs convention (`docs/adr/`, `docs/design/`, or where existing docs live — discover, don't invent). The filename follows the convention of the folder it joins, so a numbered set takes the next free number rather than a number already on disk, and an existing document is never overwritten by a new one: a design doc that replaces another says so in its own text and leaves the old file where reviewers linked it.

## Self-check before delivering

Settle the mechanical half first, so the reading below is spent on judgement rather than on spotting a placeholder. Each line is a yes or no about the document as it now stands; how you settle it is yours to decide — a read, a search, or a throwaway check you write for this document and throw away after.

Blocking, a document with any of these is not ready to hand over:

- No leftover placeholder anywhere in the body: TBD, TODO, FIXME, a citation-needed marker, lorem ipsum, "fill this in", a bracketed <your thing>, a sentence trailing into a continuation note.
- A full doc carries a section for each of requirements or problem, design or proposal, alternatives, recommendation or decision, non-goals, risks, and rollout or rollback — each with a body under it, not a heading standing alone. An ADR instead carries Status, Context, Decision, Alternatives considered and Consequences, none of them empty.
- An ADR status reads proposed, accepted or superseded, and nothing else.
- Alternatives number two or more, counted as list items or table rows. A paragraph mentioning one option is one alternative however long it runs.
- Where acceptance criteria exist, every requirement label is covered by at least one, and every criterion cites a label the requirements section actually defines.

Warnings, each answered or explicitly waived:

- The opening third carries at least one number. A context with no quantity has not stated the problem.
- The risks (or an ADR's consequences) name an early warning: what a reader would observe if the risk is materialising.
- A full doc has an open-questions section, marked rather than hidden.

Then the judgement, which no check settles:

- The three-condition test verdict is stated in one line — why this decision earned a document at all.
- Every scale number traces to a stated assumption a reader can re-run; a number with no assumption is a vibe with digits.
- A recommendation exists, cites the requirements that drove it by label, states what new information would flip it, and names its ceiling with the component that breaks first.
- Re-read each alternative as its advocate: if one collapses under its own best case, it was a straw man — replace it or drop it.
- The risk list came out of the inversion pass, not out of what was convenient to mitigate: each risk names an early warning a reader could observe, and a risk with no mitigation is written down as accepted rather than dropped.
- The rollback names a numeric trigger (metric, threshold, window) and the point of no return with what happens past it; an unknown that decides between alternatives is a spike with a date, not a guess.
- Non-goals, rollback, and marked open questions are present; any requirement you invented rather than confirmed is moved to Open questions or deleted.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Component shopping — naming technologies before requirements | Requirements and numbers first; technology falls out of them |
| Trade-off tour with no recommendation | End every comparison in a recommendation tied to a requirement |
| Straw-man alternatives | Each alternative argued at its honest best before it loses |
| Invented requirements ("we might need multi-region") | Only stated or confirmed requirements; speculation goes to Non-goals |
| ADR spam — a document per reversible choice | The three-condition test; reversible choices get a code comment |
| Design without a rollout | Migration order, backward compatibility, and rollback in the doc |
| Risks listed forward, each arriving with a reassuring mitigation | Invert first: name what killed it, then mitigate the causes you named |
| Open questions silently resolved by omission | An explicit Open questions section the reader can answer |
