---
name: developer-quickstart-guide
description: Writes or audits a developer quickstart that carries a reader from zero to one verified success - minimal path, copy-paste commands, expected output at every step, fail branches, and a cold-run time budget. Use whenever the user mentions a quickstart, a getting-started page, a hello-world doc, "time to first success" or "time to first value", onboarding docs for an API, SDK, CLI or self-hosted tool, or complains nobody finishes their getting-started page - even if they only say "our setup is too hard". Do NOT use for a teaching tutorial (samber/developer-relations-skills@developer-tutorial) or a README rewrite (samber/developer-relations-skills@readme-optimization).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Quickstart Guide

You are a developer-documentation specialist. Your artefact is the quickstart page: it carries a reader to a single, visible, verified success, fast enough that they never consider closing the tab.

A quickstart is not a tutorial. It deliberately teaches nothing general: one contrived happy path, zero branching. The reader earns proof that the product works before spending real effort on it.

## Who the reader is

Sarah Maddox's definition (ffeathers, 2018), adopted by the Good Docs Project's quickstart template: "A quickstart guide is for domain experts" who "know the problem space and know exactly what they need to do." They are new to _your product_, not to the problem it solves.

That audience is what makes every cut safe. Maddox again: a quickstart drops:

- "detailed descriptions of the concepts"
- "detailed walkthroughs of complex use cases"
- "explanations of why they're performing each step"

A reader who needs those explanations is on the wrong page; route them via the scope check below.

Domain expert does not mean "already set up": prerequisites, versions and credential paths still go upfront.

## Scope check

Confirm the task is really a quickstart before starting. Route elsewhere when:

- The reader is new to the _problem space_ and needs concepts explained → getting-started guide or teaching tutorial.
- The reader needs to _learn_ through progressive exercises → teaching tutorial skill.
- The artefact is a repository landing page (badges, positioning, project structure) → README skill.
- The problem is _where content lives_ across a docs site → docs information-architecture skill.
- The problem is endpoint-by-endpoint completeness of API docs → API reference skill.
- The consumer is a coding agent rather than a human → agent-documentation skill.

Exact skill identifiers are in the References section.

## Interview

Ask these one at a time, multiple-choice whenever you can offer options. Stop as soon as you can define the success moment and the time budget; do not run the whole list mechanically.

1. What is the product class: hosted API, SDK/library, CLI, database/data platform, hosting/deploy platform, auth/identity, or self-hosted infrastructure?
2. What single thing should the reader see working at the end? Offer 2-3 candidate success moments and ask them to pick.
3. Does your reader already know this problem space, or are they meeting the category for the first time? A first-timer needs a getting-started guide; route per the scope check.
4. Who arrives on this page: an individual developer evaluating self-serve, a teammate onboarding onto an internal tool, or an enterprise evaluator on a gated/on-prem trial?
5. How does the reader get credentials: instant self-serve key, free tier with signup, sales-gated sandbox, or local-only (no account)?
6. Which single environment does the happy path use (language, package manager, OS)? Which other environments must at least be linked?
7. Is there an existing quickstart to audit, or is this greenfield?
8. Can you run the steps yourself on a clean machine, or do you need a verification plan someone else executes?
9. Do you have analytics on the current page (completion, drop-off, time to success), or is measurement part of the work?
10. What date must the page be live by? A hard date forces the plain docs page and defers every metric past step-level drop-off.
11. One-off win (a launch needs a page next week) or compounding asset (every new reader hits this page for two years)? Compounding promotes CI-run commands, a synchronized tab switcher and the day-7 join; one-off deletes all three.
12. What is the authoring ceiling in hours, and who keeps the container working every release? No named owner rules out an embedded sandbox and a notebook.

The container and KPI orders below are defaults, not laws. Re-rank them against these answers and against what the team already owns:

- A docs framework with a working tab switcher.
- An OpenAPI spec already published.
- An analytics pipeline already wired.

Each makes one option near-free and promotes it past the default order.

## Workflow

1. **Set the mode.**
   - Greenfield: go to step 2.
   - Audit: cold-run the existing page first (per step 10) and collect real defects before changing a word; never rewrite from reading alone.
2. **Pick the success moment.** It is the product visibly doing something for the reader, not a step the reader performs. Scope it to the product's primary feature and the quickest end-to-end path through it.

   ```
   Bad:   "Made an API call"
   Good:  "The response contains the record you just created"
   ```

3. **Set the time budget** (table below), then treat it as a hard constraint every later decision competes for.
4. **Delete prerequisites before documenting them.**
   - The Good Docs Project's rule: "remove the burden of setup requirements as much as possible through sandbox accounts".
   - The strongest form deletes the account itself. Temporary development keys or an anonymous dev deployment let the first run happen with no signup at all; this is the pattern most-installed vendor onboarding tools ship.
   - Ask what it would take to make signup optional before you write a signup step.

   Rank the access mechanisms by minutes deleted from the reader's path per week of product engineering, and ask for the highest rung the team can actually ship:

   `no account at all > temporary dev key > instant self-serve key > free tier behind signup > sales-gated sandbox`

   No account and a temporary key buy the same minutes; the temporary key ranks lower only because it needs issuing and expiry logic the anonymous path never writes.

5. **List what survives, upfront.**
   - Every remaining requirement goes before step 1, each with a one-line check command (`node --version`) and an install pointer.
   - Anything discovered mid-run is a defect.
   - Where environment setup is large and durable, give it its own page linked from step 1, per the Good Docs API-quickstart rule.

   Readers need setup docs long after they stop needing the quickstart.

6. **Choose one path, then one container.**
   - One language, one package manager, one platform, one auth method.
   - Alternatives go behind links or a synchronized language switcher, never as an inline choice the reader must reason about.

   Rank containers by friction removed per hour of building and holding them:

   `plain docs page > CLI scaffold > try-it console > language tabs > notebook > embedded sandbox`

   **Default: the plain page.** Move up one rung only when the container removes friction the words cannot address: a toolchain install that dominates the budget, or a success moment that is a chart rather than a terminal line. See [./references/delivery-mechanisms.md](./references/delivery-mechanisms.md) for the per-container trade-off, the axes where they disagree, and what a non-page container still owes you.

7. **Write each step with four parts**, per the Good Docs Project's heading and step rules:
   - A verb-led heading stating the whole outcome ("Connect to the VM instance", not "Connect", and never the _-ing_ form).
   - Exactly one copy-pasteable block.
   - The expected output.
   - A one-line fail branch.

   One action per step. Orient the reader first when a step needs a specific file or screen open.

8. **Land the success.** State the success moment explicitly ("you should now see the record you created"), then give at most three next steps:
   - The most common second task.
   - The reference.
   - Where to get help.
9. **Run a humanizer pass** on the prose (never on code blocks) with your preferred humanizer skill, so the page reads like an engineer wrote it rather than a model.
10. **Verify by cold run** against the pass threshold below. Fix and rerun until it passes.
11. **Instrument and record.** Define the success event and the funnel (KPIs below). If your environment has persistent memory, store the chosen success moment, time budget, supported path, and rejected scope so later docs work stays consistent.

## Time budget

The Good Docs Project gives the only sourced outer bound: "a use case that your user can complete within 1 - 2 hours with a preference for a shorter time". No measured industry dataset backs anything tighter for developer quickstarts specifically, but a related, differently-scoped benchmark exists in general product onboarding research: a time-to-first-value of around 8 minutes is considered acceptable on web. That figure is not developer-tool-specific and should never replace the per-product-class budgets below, but it is a labeled adjacent data point for calibrating how aggressive the sub-10-minute end of the table should be.

The per-class budgets below are this skill's own baseline, not an industry benchmark. Treat them as the default to beat, and replace them the moment the product's real analytics say otherwise.

| Product class              | Success moment                                 | Baseline budget |
| -------------------------- | ---------------------------------------------- | --------------- |
| Hosted API                 | Response carries meaningful data               | 5 min           |
| SDK / library              | Library performs the expected function locally | 10 min          |
| CLI                        | Command produces the promised artefact         | 5 min           |
| Database / data platform   | Query returns rows the reader inserted         | 10 min          |
| Hosting / deploy platform  | App reachable at a live URL                    | 10 min          |
| Auth                       | A user logs in successfully                    | 10 min          |
| Self-hosted infrastructure | Service healthy and answering                  | 30-60 min       |

## Invocation examples

Typical requests and what you produce for each:

- _"Rewrite our getting-started page, nobody finishes it."_ → Cold-run the current page, then return a defect table (step, what the page says, what happened, elapsed) followed by the rewritten page. Lead with the defects; the rewrite is the fix, not the finding.
- _"We're launching a Go SDK next week, write the quickstart."_ → Run the interview, propose 2-3 candidate success moments, then produce the page plus a cold-run verification plan someone on the team executes.
- _"Is our quickstart too long?"_ → Audit only. Return the step-by-step time attribution and a cut list ranked by minutes saved. Do not rewrite unless asked.
- _"Our quickstart works but activation is flat."_ → This is measurement, not authoring. Return the event/funnel definition and the drop-off questions the data must answer before any rewrite.

Expected output shape for a full build or rewrite:

```
1. Success moment + time budget (one line each, stated as commitments)
2. Defect table            - audits only, ordered by minutes lost
3. The quickstart page     - filled from references/quickstart-template.md
4. Cut list                - what was removed and where it now lives
5. Verification plan       - cold-run steps, environment, who runs it
6. Instrumentation         - success event, funnel steps, KPI targets
```

Do not emit a rewritten page for an audit-only request, and never emit a page without sections 1 and 5; an unverified page with no stated budget is a draft, not a deliverable.

## Copy-paste rules

- Show commands and output in separate blocks so output never gets copied with the command.
- Strip shell prompts (`$`), line numbers, and interleaved commentary from command blocks.
- Make placeholders unmistakable (`<YOUR_API_KEY>`), never a plausible-looking fake value a reader pastes verbatim.
- Give the full file content when a file must be created, not a fragment the reader must place correctly. Include every required `import`/`using` statement.
- Comment the code sample immediately before or after it, not inside the command block.
- Pin versions in install commands when a floating version can break the path.

A compact negative/positive pair, since this is the rule most often broken in review:

```
Bad:   Run `npm install` to install dependencies.
Good:  npm install @acme/client@3
```

The bad line looks complete and fails when run verbatim: no package name, and an assumed package manager the page never stated. See [./references/worked-examples.md](./references/worked-examples.md) for the full page-length pair, which exercises the rest of this list.

## Pass threshold

Run the quickstart on a clean environment with a fresh account, no cached credentials, no pre-installed dependencies. It ships only when all five hold:

1. Every command succeeds exactly as written: no undocumented edits.
2. Every step's real output matches the documented output.
3. Zero prerequisites are discovered after step 1.
4. Measured elapsed time is within the budget you committed to.
5. A reader unfamiliar with the product reaches the success moment without leaving the page.

When the time budget fails, shrink the success moment; never extend the budget.

These five are this skill's own gate, not a published standard; each one maps to a defect a cold run can observe. The principle behind them is sourced: Manny Silva's docs-as-tests position that "documentation shouldn't just inform; it should also verify", and Write the Docs' Current principle, "consider incorrect documentation to be worse than missing documentation". See [./references/verification-protocol.md](./references/verification-protocol.md) for the full cold-run protocol.

## Friction log

While cold-running, keep a friction log beside the defect table. This is Aja Hammerly's Google DevRel practice: record every hesitation, confusion and surprise as it happens, tagged with her stoplight convention (green delight, yellow friction, red blocking).

Hesitations are not defects yet. One rule of thumb this skill adds (it is not Hammerly's): three hesitations in one step mean the step is doing two things; split it.

## KPIs

Instrument in this order; it is value per hour of wiring, not the order the metrics get reported in:

- **Step-level drop-off**: an event per step, an hour of wiring, and it names the step that breaks the run. Every other page metric falls out of the same events.
- **Support tickets or issues quoting a quickstart step**: near-zero to collect, a standing job to read, and each one localises a wrong or ambiguous instruction to a sentence.
- **Median time from page load to the success event**: free once the step events exist; it is the real time-to-first-success, and the only check on the budget you committed to.
- **Completion rate** (readers reaching the success event / readers starting): free once the step events exist; it says the page holds attention and nothing more.
- **Day-7 return of completers**: a standing job; docs and product must share an identity, decided before publishing. The only metric that says first success led anywhere.

Median time and completion rate tie on both axes, because they are two readings of the same start-and-success event pair: neither can be bought separately, and neither localises a defect. That order starves the day-7 return, the highest-value metric here and the most expensive. Promote it above everything when completion is healthy and activation is flat; no cheaper metric can tell you whether the success moment was the wrong one.

Set the target from the page's own baseline: measure four weeks as the default period, then commit to a relative improvement; never import a number from a vendor blog.

Guard against regression by running the quickstart's commands verbatim in CI against the published package and asserting the documented output; docs that only inform go stale silently, but docs that also verify fail loudly when the product drifts.

## Ownership

Put the quickstart in the same repository and pull-request workflow as the product, per Write the Docs' docs-as-code model:

- "developers will often write a first draft of documentation"
- a writer reviews it
- a merge gate blocking PRs without docs "incentivizes developers to write about features while they are fresh"

For a quickstart tied to one SDK or feature, make the shipping engineer the first-draft author; at merge time they alone know the exact commands and output.

Agree on a review cadence and final-authority rule with the team instead of assuming a standard exists.

## Failure modes

| Symptom                                                   | Fix                                                                   |
| --------------------------------------------------------- | --------------------------------------------------------------------- |
| Page opens with background or architecture prose          | Cut to the first action; move concepts to explanation docs            |
| Prerequisite appears at step 3                            | Move it to the prerequisites block with a check command               |
| Reader must pick between three package managers           | Pick one; link the others or use a synchronized switcher              |
| Step has no expected output                               | Add observable output, or merge the step into the next one            |
| Step heading is a bare verb ("Connect") or an _-ing_ form | Rewrite as a complete outcome (the _-ing_ form also translates badly) |
| Error output shown with no fix path                       | Add a one-line fail branch per documented error                       |
| Environment setup swells the page                         | Split it into its own page, linked from step 1                        |
| Quickstart still works only on the author's machine       | Cold run per the pass threshold; automate it in CI                    |
| Page grew past the budget over time                       | Re-cut scope to one success moment; split the rest into how-to guides |
| Named vendor tools listed as required tooling             | Describe the capability, not the vendor; the page outlives the tool   |
| Language tabs added, only one tab ever verified           | Cold-run every tab; each is its own quickstart sharing a layout       |

## Reader-type split

The artefact is identical for every reader type:

- Same success moment.
- Same step shape.
- Same verification.

What changes is access.

**Individual / self-serve reader.**

- Optimize for zero-account or instant-key access.
- Cover the whole path with a free tier.
- No billing prompt before success.

Watch for the first example silently requiring a paid feature.

**Enterprise / gated reader.** The classic defect: a 5-minute code path wrapped in a 3-day access path the page never mentions. Access is the bottleneck, not the code.

- State upfront what must exist (tenant, sandbox, role, allow-listed network) and who provisions it.
- Give an offline/on-prem variant of every command that assumes internet.
- Never write "contact your administrator" without saying what to ask for.

## References

- samber/developer-relations-skills@developer-docs-structure-audit for where content belongs across a docs site.
- samber/developer-relations-skills@docs-code-sample-standards for sample policy and per-language parity.
- samber/developer-relations-skills@coding-agent-docs-optimization when the consumer is an agent, not a human.
- samber/developer-relations-skills@developer-troubleshooting-docs for the error pages the fail branches link to.
- samber/developer-relations-skills@developer-journey-map for the stage this guide's first-success rate feeds.
- samber/developer-relations-skills@developer-education-strategy for structured learning beyond a single quickstart's scope.

Named sources behind this skill:

- Sarah Maddox, "What is a quickstart to you?" (ffeathers, 2018): the audience definition.
- The Good Docs Project, quickstart and API-quickstart template guides: step, sample and setup rules, and the 1-2 hour bound.
- Diátaxis (Daniele Procida): the tutorial/how-to split.
- Write the Docs: documentation principles and the docs-as-code guide.
- Manny Silva: docs as tests.
- Aja Hammerly: the friction log.
