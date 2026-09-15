---
name: om-mockup-prototype
description: Build a neutral clickable low-fi prototype from a product brief during discovery, after the first synthetic panel and before refreshing the brief or drafting a backlog. Preserve business rules and explicit assumptions, simulate the chosen flow locally, and verify navigation and relevant states in a browser. Use for discovery wireframes or testing a flow before detailed design.
---

# Discovery prototype

Turn a selected flow from the product brief into neutral screens a person can
operate. The result is self-contained local HTML with simulated data, a context
record and browser evidence. It tests the sequence, labels, choices and recovery
paths before detailed visual design. It works with or without a design system.

In the discovery hand-off, this step follows the first `om-synthetic-users`
panel. The user may then walk the prototype with another panel before
`om-discover --refresh` incorporates the observations and checks readiness for
`om-backlog`. A direct invocation can use a brief without a panel report.

<HARD-GATE>
Keep the brief's business rules, non-goals, scope and owned decisions intact.
Mark missing facts and proposed flow changes as assumptions; never turn a
synthetic suggestion into an accepted requirement. A prototype or its approval
does not prove user demand or satisfy the Definition of Ready. Write only new
files in the selected prototype revision. Keep application code, the brief and
`.uxproof/` unchanged; preserve previous revisions and manual work.
</HARD-GATE>

## Arguments

- `{brief}` (optional): a repository-relative product-brief path. Default `${SPECS_DIR}/product-brief.md`.
- `--flow <name-or-id>` (optional): the Key flow to simulate. Use the flow already chosen in the current conversation; otherwise propose one from the brief and confirm it.
- `--panel-report <path>` (optional): a repository-relative report from the first synthetic panel. With none supplied, use the report returned by the current discovery hand-off; otherwise proceed without one and say so.
- `--slug <slug>` (optional): a lowercase kebab-case output name, proposed from the flow without a setup question.
- `--refresh <revision-dir>` (optional): revise a previous output of this skill by writing the next new revision. Keep its slug and link the previous revision; never replace existing files.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-mockup-prototype/SKILL.md` when present; safety rules still win.

0. **Load context and safety rules.** Follow `references/agentic-setup.md` and read `references/rules.md` on every run. Resolve optional config and safe local paths, apply the repository's instructions and permitted override, and load a configured browser descriptor when available. Missing config never starts delivery setup.

1. **Select the flow and preserve its constraints.** Read the brief's Key flows, Product, Scope, Business rules, Non-goals, Decisions, Domain glossary and relevant open questions. Read the optional panel report as synthetic hypotheses. Record source paths, relevant stable rule/decision IDs and their status, and what remains unknown. If the brief or a usable flow is missing, stop with the precise missing input. For `--refresh`, inspect the earlier context and ownership record before drafting a new revision (`references/prototype-format.md`).

2. **Confirm the simulation boundary.** Show the actor, starting point, success outcome, screen/state list, preserved rules and any assumptions the interaction would require. Ask only for information unavailable in the context and for unresolved product choices. Existing explicit authorization for that exact scope stands. A rule conflict needs the human's decision through the brief's required change path; do not resolve it in prototype code. Confirmation approves a simulation and its stated assumptions, not the truth of those assumptions.

3. **Build the clickable revision.** Follow `references/prototype-format.md`: create a fresh revision directory, write the context record, and construct static HTML, CSS and small local event handlers. Use neutral wireframes, accessible controls and simulated data. Wire the selected journey, relevant edge states, back navigation and reset; represent excluded destinations honestly. Record assumptions in the context file without putting panel conclusions or expected reactions into the simulated interface.

4. **Verify the artifact.** Run `references/quality-gate.md`: check scope, offline operation and required interactions, then exercise the local HTML through the browser provider's named operations. Capture actual evidence, close the session, fix failed interactions within the new revision, and recheck affected states. An unresolved static failure means `Verification: incomplete`, even when it prevents opening the browser. When static review passes but browser access is unavailable, record `Verification: not-run`; do not claim a browser walk. Failed or partial browser checks also mean `incomplete`.

5. **Record and report the result.** Finalize `prototype.json` with the file inventory, context sources, previous revision and verification result. Report through `references/report-templates.md`, with the artifact, limitations and exact Output contract lines. Return to the calling discovery hand-off when present; this skill does not invoke a panel, refresh the brief, file a backlog or start implementation. A direct user may choose a later exact invocation, recorded in `Next:` without executing it.

## Output contract

End with these exact, undecorated lines when an artifact was written:

```text
Prototype: <repo-relative path to revision/index.html>
Prototype context: <repo-relative path to revision/README.md>
Verification: passed | incomplete | not-run
Next: none | om-<skill> <exact user-approved arguments>
```

Consumers parse `^Prototype: (\S+)$`, `^Prototype context: (\S+)$`,
`^Verification: (passed|incomplete|not-run)$` and
`^Next: (none|om-[a-z-]+.*)$`. Emit only one final `Next:` line. It names an
explicitly chosen, still-unexecuted action; otherwise emit `Next: none`.
Do not emit artifact paths when no files were written. A declined follow-up or
completed operation belongs in the prose, not in `Next:`.

## Rules

- Interactive only. A missing human decision is a stop; no autonomous mode or implicit choice of business policy.
- Use the existing UI language and the brief's terminology. Neutral styling does not remove accessibility, meaning or useful recovery text.
- `.uxproof/` is read-only context. This skill creates no brand, moodboard, tokens, design contract or production component, and does not require a design system to be extracted first.
- All displayed records are fictitious simulation data. Never reuse personal interview details, credentials or production records.
- Keep `[SYNTHETIC]` and `[ASSUMPTION]` labels in the context record. Preserve confirmed decisions with their source and owner. Browser checks verify prototype behavior only.
- Preserve old revisions and manual files. A refresh writes a fresh revision after validating the prior ownership record and its path.
- Perform no tracker mutations, publishing, dependency installation or application boot. Invoke no unavailable companion skill; report the missing capability instead.
- Read `references/rules.md` for the shared writing rules, output markers and evidence distinctions; they always apply.
