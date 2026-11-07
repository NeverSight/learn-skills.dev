---
name: file-issue
description: "File one GitHub issue: a bug report, feature request, task, or spike, created with `gh`. Use when the user wants to file or open an issue, report a bug, request a feature, write up a chore or a spike, turn a half-formed complaint into something tracked, or write an issue a coding agent can pick up cold. Files exactly one issue: to slice a spec or plan into many linked tickets, use to-tickets instead. Never edits, closes, triages, or ranks existing issues. Beyond creation it only links the new issue to its parent and blockers, then removes the linked entries from the body."
argument-hint: '[what the issue is about | --deep | --fast | --dry-run]'
---

# file-issue

Write one issue a **stranger** can act on: no conversation context, no tacit knowledge of the codebase, no chance to ask a follow-up question. That stranger is often a coding agent, which is the same test with a harder bar. Structure is the easy half and most tooling stops there — every gate in Step 6 is a content gate.

Where a step names a shell command, treat it as the intent and use your native shell or file tools. `gh` executes anything that touches GitHub.

Resolve once per invocation:

- **ASK** — the text following the invocation. (Claude Code exposes this as `$ARGUMENTS`; on other agents it is the rest of the user's message.) When ASK is empty, the issue comes from the conversation so far; name which part you took it from before drafting, so a wrong read is cheap to correct.
- **Flags**, stripped from ASK before anything else reads it: `--deep` pins Depth 2, `--fast` pins Depth 0, `--dry-run` renders and never posts, `--yolo` skips the confirmation.

## Step 1 — Detect and Harvest

Mechanical, no judgment, before any question.

Preflight `gh auth status`. Missing or unauthenticated → say so plainly and continue in dry-run only. A rendered draft must never read as a filed issue.

Template ladder, first hit wins:

1. `.github/ISSUE_TEMPLATE/*.yml` — issue forms. Read [references/issue-forms.md](references/issue-forms.md) and fill the declared fields.
2. `.github/ISSUE_TEMPLATE/*.md` — legacy templates. Same handling.
3. `ISSUE_TEMPLATE/` at the repo root, then the org-level `.github` repo, which supplies defaults to every repo lacking its own.
4. Nothing found → this skill's own templates in `assets/`.

The detected template's sections are the issue's sections, exactly. If the repo asks for four, the issue has four — a repo's own conventions outrank anything you would invent.

Harvest at the same time. This is where the agent-readiness gate gets its answers without spending a question on them:

| Source | Facts |
| --- | --- |
| `gh issue list --limit 10 --state all` | label taxonomy, title prefixes, task-list use, whether issues get assigned to agents |
| `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` | build, test, and convention commands |
| Manifest scripts (`package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`); no manifest → runnable scripts under `tests/` or `scripts/`, then the commands `.github/workflows/` runs, then `absent` | the exact verification command |
| `.github/workflows/`, `CODEOWNERS` | repo complexity |
| `git shortlog -sne --since='90 days ago'` | contributor count |

The verification row is a ladder like the template one, first hit wins. A repo with no manifest still answers mechanically: shell scripts under `tests/` name the command (`bash tests/<component>-smoke.sh`, picking the script named for the component under change), and the steps a CI workflow runs name it where the scripts don't. `absent` is the answer only after every rung misses.

**Done when:** the template source is named and every harvest row holds a concrete value or an explicit `absent`.

## Step 2 — Assign Depth

Arithmetic, announced, overridable in one word.

| Depth | Fires when |
| --- | --- |
| **0** | Mechanical, single site, no behavior change — typo, dead link, dependency bump, comment fix. |
| **1** | Everything not caught by 0 or 2. The default. |
| **2** | Any one of: a breaking change; the ask names two or more components; it touches auth, security, or PII; the issue is destined for a coding agent; the repo has `CODEOWNERS` or ≥5 contributors in the last 90 days. |

Repo complexity sets a floor rather than a ceiling, and the solo-repo cap scopes to it alone: a solo repo with no CI and no templates caps at Depth 1 only when repo complexity was the sole Depth 2 trigger. A breaking change, a multi-component ask, an ask touching auth, security, or PII, or an issue destined for a coding agent fires Depth 2 in any repo—those are properties of the ask and the workflow, and the shape of the tree cannot talk them back down. A repo with `CODEOWNERS` never runs Depth 0 on anything but a genuine typo.

Pick the issue type on the same signals: a defect in existing behavior → bug; new or changed capability → feature; anything else that ships → task; a question to answer rather than work to do → spike. Map "enhancement" and "improvement" to feature unless the repo's labels distinguish them.

Announce the result in one line — `Depth 1 — 4 gaps to fill.` — then keep going. The announcement is the user's correction point.

Depth 2 additionally earns a targeted code probe: locate the component the ask names and capture real file paths. Those paths become the issue's file pointers, and they sharpen every question that follows. The probe also asks what preparatory change would make the work small and verifiable on its own. A prefactor named in the issue is the usual way through gate 6's verify-alone condition; slicing prefactors into issues of their own stays with `to-tickets`.

**Done when:** depth and issue type are both fixed, and the depth line has been said out loud.

## Step 3 — Elicit

**In:** the chosen template's slot list, each slot marked filled or empty; the depth ceiling.
**Out:** the same list, where every slot holds a value, an explicit `n/a — <reason>`, or `unknown — asked, declined`. No blanks.
**Exit:** the moment the rubric in Step 6 becomes satisfiable. Not when a question budget runs out.

Depth 0 asks nothing here. Draft straight from ASK; the one question a Depth 0 run can still put is a gate 7 failure at Step 6, which no draft can close on its own.

Depth 1 asks at most five questions, and only against slots the ask left empty. Treat five as a ceiling, not a target. A gate 7 failure at Step 6 sits outside that count, the same way it sits outside Depth 0's silence, because it is the one gate no draft can close. Depth 2 keeps going past the rubric into edge cases, failure modes, non-goals, and how you would know this was done wrong.

Rules that hold at every depth:

- One question at a time. Batched questions read as a form, and forms get form-quality answers.
- Every question names the empty slot it fills. No named gap, no question.
- Front-load by evidence value, in the order the issue type sets:
  - **Bugs:** steps to reproduce first, then error output, then observed-versus-expected. Reproduction steps are what developers rank highest and what reporters find hardest to supply, so ask for the expensive thing while attention is highest.
  - **Features and tasks:** collisions between stated rules first, then unstated behavior at boundaries, then whatever slots are still empty. To find a collision, take the rules the ask already states and check them in pairs. Where two rules call for different outcomes on one input both govern, ask which rule wins. Each rule reads fine alone, so a collision marks the ask as genuinely incomplete rather than merely terse—the answer changes the design, not the wording.
- Every question is skippable. A declined answer resolves its slot to `unknown` and the interview moves on.
- Never re-ask what Step 1 harvested. The verification command comes from the repo, not from the user.

Run the interview yourself. Delegating it to an external interrogation skill loses the depth governor, which is the whole point, and a client repo may not have that skill installed anyway.

**Done when:** every slot is a value, an `n/a`, or an `unknown`.

## Step 4 — Stop If This Is a Spec

Some asks are not one issue. Check before drafting:

- **≥4 distinct components** named across the answers, or
- **the work does not fit one fresh context** — the files a stranger must read, the change they must make, and the verification they must run add up to more than one cold session can hold. Fit is a property of the work, so no rewording of the criteria moves it.

Either one alone fires. A long acceptance-criteria list is a smell that forces the fit question, never a trigger by itself: seven criteria can be four failure modes of one rule written apart, and whether they collapse on a rephrase says nothing about the size of the work. On a fire, stop at a recommendation: name the spec path (`/to-spec` then `/to-tickets` where installed, otherwise write a spec first and come back per slice) and hand over what the interview already produced so none of it is wasted. Neither compress the ask into one bloated issue nor start decomposing it here.

**Done when:** the ask is confirmed to be a single issue, or the handoff has been offered and nothing has been posted.

## Step 5 — Draft

Fill the detected template. With no template, read exactly one file from `assets/` — `bug`, `feature`, `task`, or `spike` — and keep its section order, which reflects measured developer importance rather than convention.

Strip the templates' HTML comments; they are authoring guidance and do not belong in a posted issue. Drop any heading whose slot resolved to `n/a` — an empty heading is worse than an absent one.

Title follows {component} + {wrong behavior} + {trigger}, matching whatever prefix convention the harvest observed. Acceptance criteria default to a falsifiable checklist; escalate to Given/When/Then only for multi-step stateful behavior in a repo whose tooling actually executes scenarios.

**Done when:** a complete issue body exists, with no placeholders and no orphaned headings.

## Step 6 — Self-Check

Gates block. Defaults get surfaced and never block.

Gates:

1. **Stranger test** — a stranger can act on this draft with no follow-up question available.
2. **Runnable reproduction** — commands or clicks a stranger can follow on a clean checkout, not prose gestures. Bugs only.
3. **Observed and expected stated separately.** Bugs only.
4. **Error output** where the failure produces any. Bugs only; drop it for silent visual defects rather than padding.
5. **At least one falsifiable acceptance criterion.** All types. A criterion a reviewer cannot fail is not one.
6. **Agent-readiness**, when the issue is agent-targeted: single-interpretation problem statement, binary criteria, a runnable verification command, environment pointers, file hints, explicit done-criteria, non-goals. The verification command has to exercise the change, not merely pass beside it—an agent that finishes and cannot verify reports done regardless. A change that genuinely cannot be verified alone passes only by declaring its prerequisite as a blocker, or by naming the issue where verification lands. The same test runs on every named artifact: a verification command or file pointer naming something the repo does not yet hold fails unless that artifact is declared on the Blocked by line—an agent will otherwise try to run a file another ticket has yet to create. That artifact lands on the Blocked by line as text, since a path never resolves to an issue.
7. **Falsifier for a derived rule** — where the body rules that a value "is", "counts as", or "should be marked" something under a stated condition, the ticket states that rule as a property and names the check that would fail it. All types. The question to put is what experiment tells the rule apart from its most plausible wrong neighbor: perturb what the rule keys on and the value has to move, perturb the nearest thing the rule could have keyed on instead and the value has to stay put. Acceptance criteria observe the value and this gate reaches the rule behind it, so a ticket stating no such rule passes untouched, and one stating a rule it cannot falsify owes that sentence rather than a rewrite or the test itself.

Defaults: non-goals when scope is ambiguous; Ko-structured title; labels matching observed repo convention; environment metadata.

Say which items are convention rather than evidence as you surface them, so a user overriding one knows what they are overriding. [references/evidence-map.md](references/evidence-map.md) carries the traceability.

A failing gate means fix the draft, or ask the single question that closes it. Never quietly downgrade a gate to a warning. Gate 7 is the only one a draft cannot close by itself, because inventing the falsifier is the thing it exists to prevent, so its question gets asked even at Depth 0 where nothing else is.

Where the repo's label taxonomy has a ready-for-agent-style label, apply it only after gate 6 passes. The label should mean something.

**Done when:** every gate passes and every unmet default has been named.

## Step 7 — Polish

Depth 0 skips this step entirely. A one-line body does not earn a dispatch and an audit; go straight to the write guard.

At Depths 1 and 2, where the `technical-writing` skill is installed, invoke it via the Skill tool on the drafted issue body and follow what it loads. It supplies instructions, not a rewritten body, so the revision is yours to make. Where it isn't installed, ship the draft unchanged—absence degrades to current behavior, never to an error or a stall. `technical-writing` owns any downstream prose auditor, so never reach past it to one directly.

Keep the body as it entered this step. Without that copy, nothing below is checkable afterward.

The pass changes wording only. Section structure, the title's harvested prefix convention, commands, paths, error output, and every fact the Step 6 gates passed survive it; where a revision would alter one, keep the original. Acceptance criteria may be reworded, but every symbol and condition inside them survives, and a criterion that comes out unfalsifiable has failed the pass rather than passed it. A named falsifier is protected the same way: reword it freely, but what it perturbs and both outcomes it asserts survive the pass.

This is not the delegation Step 3 rules out. The interview carries the depth governor—judgment this skill owns, and lost the moment another skill runs it. A wording pass has no governor to lose. The audit is mechanical, and where the skill is missing the cost is polish, not correctness.

**Done when:** the body has been revised under `technical-writing`, or its absence is noted and the draft stands, or Depth 0 skipped the pass.

## Step 8 — Write Guard

Check for duplicates first, with `gh search issues` against the title terms and any error signature. Rank candidates by error-signature overlap, then title and description similarity, then shared component.

Surface what you find and let the user choose: comment on the existing issue, or file new. Never block — duplicates routinely carry information the original lacks, and refusing them teaches reporters to stop contributing. When the new draft has a better reproduction than the suspected original, say so and recommend appending.

Resolve every Parent and Blocked by entry before rendering. Pass slot entries only, each as a bare reference (`#N`, `owner/repo#N`, or an issue URL) with any commentary kept out of the argument, and nothing taken from the Problem section, a quoted error block, or anywhere else in the body:

```
python3 <skill-path>/scripts/link-issues.py resolve --parent '<entry>' --blocked-by '<entry>' --blocked-by '<entry>' > <resolved.json>
```

Omit a flag whose slot is empty, and pass `--repo` when the issue targets a repo other than the current one. An entry with a `node` becomes a native link; an entry with `node: null` stays text, and its `reason` says why. A Parent in a repository another owner holds is always one of those, since GitHub only accepts a sub-issue under a parent with the same owner. An entry the viewer lacks permission to link is another: a blocker needs TRIAGE or higher on the repo the issue is filed into, a parent needs WRITE or higher on its own repo, and a permission `resolve` cannot read counts as missing. Render every Parent and Blocked by entry as text, resolved or not: a link can still fail once the issue exists, and the text is what survives it. An entry whose link lands leaves the body afterwards, at the strip below.

When the preflight found `gh` unauthenticated, `resolve` cannot run: every entry stays in the body as text, and the dry-run says the links were not resolved.

Then render the full issue as markdown, show it with the links it will set beside the rendered body, and wait for explicit confirmation before `gh issue create`. `--dry-run` renders and stops. Under `--dry-run`, run `resolve`, then `link --dry-run` with no `--issue`, which lists each link it would set and each entry the strip would then remove, and sends no mutation, then stop. `--yolo` skips the confirmation but not the self-check.

`gh issue create` prints the new issue's URL. Capture it and link:

```
python3 <skill-path>/scripts/link-issues.py link --issue <URL> --plan <resolved.json> --out <result.json>
```

Exit 0 means every link was set. Exit 1 means at least one failed: report the issue URL, each `FAILED` line, and the `retry:` command under it; the failed entry's text is still in the body, so nothing is lost. Exit 3 means a usage error, an unreadable plan, or a new issue that could not be resolved, and no link was sent: report the URL and that no links were set. `strip` still runs and, finding nothing linked, writes nothing.

Then strip the linked entries from the body, passing `--agent-targeted` when the issue is agent-targeted so an emptied Blocked by line reads `None` rather than vanishing:

```
python3 <skill-path>/scripts/link-issues.py strip --issue <URL> --plan <resolved.json> --result <result.json> [--agent-targeted]
```

`strip` fetches the body, removes only the entries whose link landed from the Parent and Blocked by lines, and sends one `updateIssue`. A Parent line whose entry linked goes; a Blocked by line left empty becomes `**Blocked by:** None` when agent-targeted and goes otherwise; an entry whose link failed stays where it was. It never adds a reference back and never touches another line, and with nothing linked it writes nothing; the `None` on an emptied agent-targeted Blocked by line is the only text it ever writes. Exit 1 means the body write failed: report the `FAILED strip` line and its `retry:` command and leave the body as filed, since a text entry beside its link is harmless.

Creation only. The rule admits exactly three kinds of write beyond `gh issue create`, each naming the new issue: one `addSubIssue` for the parent, one `addBlockedBy` per blocker, and at most one `updateIssue` that removes only the entries whose link landed from the new issue's own body. It makes no other write to an existing issue, and never edits, closes, relabels, or reassigns one; when that is what the user wants, say that this skill does not do it.

**Done when:** the issue URL has been reported, every link was set or reported with its retry command, and the linked entries were stripped from the body or the strip was reported with its retry command, or the draft and its link list have been rendered under `--dry-run`, or the user chose to comment on an existing issue instead.

## Further Reading

- [references/issue-forms.md](references/issue-forms.md) — issue-form YAML schema, template resolution order, `gh issue create` mechanics
- [references/evidence-map.md](references/evidence-map.md) — every gate and default traced to its claim and evidence tier
- [scripts/link-issues.py](scripts/link-issues.py) — resolves Parent and Blocked by entries to issue nodes, sets them as native links, and strips the linked entries from the body, printing a retry command for any write that fails
- [assets/](assets/) — `bug`, `feature`, `task`, and `spike` bodies, used only when the repo has no template of its own
