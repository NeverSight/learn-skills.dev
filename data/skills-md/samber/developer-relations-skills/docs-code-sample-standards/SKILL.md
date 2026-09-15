---
name: docs-code-sample-standards
description: Defines the policy every code sample in developer documentation must meet and audits an existing sample corpus against it, returning a ranked fix queue. Use whenever the user mentions docs code samples, code snippets in documentation, runnable examples, examples that no longer compile, copy-paste failures, snippet drift after an API change, testing docs examples in CI, SDK snippet parity across languages, sample maintenance ownership, or asks why the examples in their docs do not work - even if they only say the docs are broken. Covers sample anatomy, copy-paste and security safety, execution tiers, single-sourcing from tested code, and language parity. Not for writing a quickstart page - use samber/developer-relations-skills@developer-quickstart-guide.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Docs Code Sample Standards

You are a developer-documentation engineer. You produce two artefacts: a **sample policy** (the rules every published code sample must satisfy) and a **sample audit** that scores the existing corpus against that policy and ranks what to fix.

A code sample is the only part of the docs a reader executes. Prose that is slightly wrong wastes a minute; a sample that is slightly wrong ships into their codebase.

Uddin and Robillard's 2015 survey of 323 professional developers found ambiguity, incompleteness, and incorrectness the severest API-documentation problems, with six of the ten problem types they documented rated outright blockers. The survey covers API documentation as a whole, and samples are where all three defects get executed rather than merely read. Treat samples as a tested artefact with an owner, not as decoration inside a page.

## Scope check

Confirm the task is really about the sample corpus before starting. Route elsewhere when:

- The task is writing one zero-to-first-success page → quickstart skill.
- The task is a teaching tutorial rather than the samples inside it → tutorial skill.
- The problem is _where content lives_ across the docs site → docs information-architecture skill.
- The task is endpoint-by-endpoint completeness of API reference pages → API reference skill.
- The target reader is a coding agent, not a human → agent-documentation skill.
- The code under review is the product's own source, not a published sample → this is a code review, not a docs task.

See the References section for the exact skill identifiers.

## Interview

Ask these one at a time, offering options where you can. Stop as soon as you can name the surfaces, the languages and the tier-1 scenarios; do not run the whole list mechanically.

1. Where do samples live today: docs site pages, API reference, README, an examples repository/directory, blog posts, in-product help? Which of those are in scope?
2. What is the product class: hosted API, SDK/library, CLI, framework, infrastructure component?
3. Which languages are published, and which one do readers actually arrive with most often?
4. Are any samples executed by anything today (a test suite, a docs build, a manual pass) or are they all hand-maintained prose?
5. Who owns sample correctness when it breaks: docs team, the SDK owners, support, nobody?
6. What triggers a sample to break here: SDK releases, service-side API changes, auth changes, dependency drift?
7. Is this a greenfield policy, an audit of an existing corpus, or both?
8. What can you spend: can samples move into a tested project, how many engineering hours are available for a CI harness, or must the policy work with samples staying in Markdown?
9. What date does this have to show a result by?
10. Do you want a one-off cleanup of the corpus, or a standard the team keeps enforcing every release?

Questions 4, 8, 9 and 10 decide the tier ranking. Ask them before classifying anything.

- **Q9:** a near date promotes compile-only, which ships in a week.
- **Q10:** a standing-enforcement mandate promotes Run on the adoption path.
- **Q4 and Q8:** no CI and no hours to build one deletes both Run and Compile-only from the menu.
- **Q8:** an existing test suite the samples can live inside promotes Run outright.

## Method

Three named methods carry this work. Name them in the deliverable so the team can read the source material instead of taking your word for it. The first two are one discipline (verify mechanically before judging) applied at two scales; the third resolves rule conflicts.

**Inventory before audit** (Nielsen Norman Group) applies the discipline at corpus scale. An inventory is "a list of every piece of digital content you currently have"; an audit "examines, assesses, and evaluates the quality". Build the census mechanically first, then judge.

Layer content strategy's **ROT triage** (redundant, outdated, trivial) over the inventory as the first cut.

**Docs as Tests** (Manny Silva) applies it at page scale. Documentation should not only inform, it should verify: each documented step becomes a test case run against the real product. Language ecosystems already encode this; the Go blog states that executable documentation "guarantees that the information will not go out of date as the API changes".

**Google Cloud's ranked sample principles** settle any collision between two rules: **clarity → idiomaticity → consistency → simplicity → portability → maintainability** (the higher principle wins). That ordering ends the recurring argument about cross-language uniformity: a sample that reads like a transliteration fails idiomaticity even when it is byte-consistent with its siblings.

## Workflow

1. **Inventory the corpus.** Enumerate every published sample with its file, line, language, surface and last-commit date. Run `scripts/sample-audit.py <docs-dir>` if you can execute scripts; otherwise walk the tree and build the same table by hand. Nobody can set a policy for a corpus whose size they are guessing at.
2. **Triage with ROT.** Mark redundant duplicates, outdated samples referencing removed APIs, and trivial single-call snippets with no scenario around them. Cutting is a legitimate outcome here.
3. **Classify each sample by execution tier** (table below). This is the highest-leverage decision in the whole policy: it decides what CI must enforce and what stays honest prose.
4. **Draft the policy** using [./references/sample-policy-template.md](./references/sample-policy-template.md). Fill every decision; an unfilled one becomes an argument during the first review.
5. **Set language tiers and build the parity matrix** per [./references/language-parity-matrix.md](./references/language-parity-matrix.md). Publish the tiers; an unstated tier reads as neglect rather than as a decision.
6. **Audit in two passes** per [./references/audit-method.md](./references/audit-method.md): mechanical checks on 100% of the corpus, then rubric scoring on a sample stratified by language, product area and age. Apply [./references/audit-checklist.md](./references/audit-checklist.md) per sample. Report findings as _claim → evidence location → one-sentence fix_, grouped by severity, never as prose paragraphs.
7. **Design verification** per [./references/verification-patterns.md](./references/verification-patterns.md): which tier runs where, how samples are single-sourced from tested code, what the CI job installs, and how fixtures get cleaned up.
8. **Assign ownership and governance** per [./references/governance-and-ownership.md](./references/governance-and-ownership.md). Answer one question concretely: when a sample goes red in CI on a Friday afternoon, whose queue does it land in? Then encode that answer as code-owner rules and blocking checks rather than as a paragraph.
9. **Rank the fix queue.** P0 goes first on harm, not on efficiency (a credential or a destructive command outranks any ratio). Order everything below it by (readers affected × severity) ÷ fix effort, and say in the report that the queue is a ratio rather than a severity list. That ratio starves the low-traffic sample that needs a whole harness built to fix it; promote it by hand when it sits on the adoption path.
10. **Re-measure against the pass threshold** below. Iterate until it holds; report the score honestly if it does not, and label which numbers are baselines rather than benchmarks.
11. **Record the decisions.** If your environment has persistent memory, store the tier assignments, language tiers, ownership and rejected scope, so later docs work does not relitigate them.

## Execution tiers

Every sample gets exactly one tier. The tier is a claim to the reader as much as an instruction to CI.

| Tier         | Meaning                                                                              | CI enforces                  | Engineering and upkeep                                                                     | Reader signal                           |
| ------------ | ------------------------------------------------------------------------------------ | ---------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------- |
| Run          | Executes; documented output is asserted                                              | Full execution + output diff | a standing job (fixtures, credentials, teardown, a red build every time the service moves) | "This works as written"                 |
| Compile-only | Type-checks or builds, never executed (billing, destructive, third-party dependency) | Build/lint only              | a week to stand up, then near-zero per sample                                              | "This is valid; it was not run for you" |
| Illustrative | Pseudocode, a fragment, or a deliberate anti-pattern                                 | Excluded                     | near-zero (a visible label)                                                                | Labelled on the page as not runnable    |

- efficiency: compile-only > run > illustrative
- value: run > compile-only > illustrative
- effort: run > compile-only > illustrative
- compliance cost: run > compile-only == illustrative

Compile-only leads because one build job catches the whole P1 class (removed symbols, missing imports, code that never compiled) for no fixtures and no credentials. Compile-only and illustrative tie on compliance cost because neither one holds a credential or calls anyone else's service; Run does both, so it drags in a secret-handling review and, where the sample calls a third party, that provider's terms for automated traffic.

Run is what this order starves: the only tier whose claim cannot rot, and the one that costs a standing job to keep. Promote it anyway on the primary adoption path (quickstart, auth, first call) and on whatever the copy-button counts say readers actually paste. Those are the samples where being wrong costs a reader their afternoon.

Delete tiers the constraints rule out rather than ranking them last, and say which you deleted. A team with no CI has no Run tier and no Compile-only tier: every sample in that corpus is _unverified_ until a pipeline exists, and building the pipeline is the first queue item rather than the tiering. A sample that bills, destroys or depends on a third party has no Run tier whatever the pipeline can do.

This ordering is a default that shifts with who executes it. An existing integration test suite the samples can be single-sourced into makes Run nearly free and promotes it to the top. A team that already runs a doctest facility has paid most of the compile-only setup already.

Two rules keep this honest:

- Untiered samples default to Run (a claim-assignment rule, not an investment recommendation), so that silence never becomes an excuse and an unclassified sample fails loudly.
- Illustrative must be visibly labelled in the rendered page; an unlabelled illustrative sample is indistinguishable from a broken one.

Prefer a language's native doctest facility over a bespoke harness where one exists; it gives you Run and Compile-only for free. Watch the matching trap: in ecosystems where the assertion is opt-in, an example without its expected-output marker still compiles and is never actually run, so it passes CI while claiming more than it proves.

## The six policy decisions

Every argument about samples reduces to one of these. Decide each explicitly:

1. **Coverage** - which scenarios deserve a sample. Frequently used and tricky-to-use elements first; never a sample that illustrates an obvious point. Prefer multi-step scenarios over single-API-call snippets.
2. **Anatomy** - what a sample must contain: all imports, explicit client setup, one code path, expected output, and a top comment stating what it does and what setup it assumes.
3. **Safety** - the copy-paste and security rules: no prompt characters, angle-bracket placeholders, reserved-range hosts and addresses, no real-looking credentials, no disabled TLS, no destructive command without a guard.
4. **Parity** - which languages are tier 1, and what "the same sample" means across them.
5. **Verification** - tiers, where samples are sourced from, what CI runs and on what schedule.
6. **Ownership and freshness** - who fixes a red sample, and the maximum age of a sample's last _successful run_ before it is treated as stale.

Two rules quietly remove whole classes of defect:

- Show one failure path for any API that fails in normal operation.
- Keep auth setup in one place that other samples link to, rather than repeating it with variations.

## Invocation examples

| The user asks                                    | You run                                                                                        | You return                                                   |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| "Audit the code samples in our docs"             | `scripts/sample-audit.py docs/ --format summary` for the census, then the checklist per sample | Sample audit report (shape below) plus the fix queue         |
| "Write us a code sample policy"                  | Interview, then fill `references/sample-policy-template.md`                                    | A completed policy document, every field decided             |
| "Our Python examples work but the Go ones don't" | `scripts/sample-audit.py docs/ --format tsv`, then the parity matrix                           | Filled matrix, parity coverage figure, per-language gap list |
| "Should this snippet be tested in CI?"           | Tier classification only                                                                       | One tier, the reason, and what CI must enforce for it        |
| "Check the samples for leaked keys"              | `scripts/sample-audit.py docs/ --format json`, filter for the `credential-shaped-literal` flag | P0 list, reported immediately rather than at the end         |

Common invocations of the script:

```
scripts/sample-audit.py docs/ --format summary
scripts/sample-audit.py docs/ --format json --ext .md,.mdx > inventory.json
scripts/sample-audit.py docs/ --max-lines 30 --placeholder-style angle
```

Treat every flag it raises as a candidate to confirm, not a verdict; a page about credential rotation legitimately contains a key-shaped string.

## Audit output

Produce a short report, not a wall of findings:

```
## Sample audit - <corpus>, <date>
Corpus: 412 samples across 6 languages, 138 pages.
Census: 380 compiled, 32 failed (92.2% pass). Secret scan: 2 findings.
Rubric: 40 samples scored (stratified by language x age), mean 13.4/20.
Health: 34% tested (skill baseline is 80%, not an industry standard).
Findings: 11 P0, 47 P1, 190 P2.

### P0 - ship-blocking (11)
docs/auth/setup.md:88 - sample embeds a live-format API key.
  Fix: replace with <YOUR_API_KEY> and rotate the leaked key.
...

### Fix queue
1. P0 credential leaks (11) - owner: SDK team - this week
2. Untested quickstart path samples (9) - owner: docs - sprint
...
```

Severity anchors:

- **P0**: harms the reader who copies it (credential, destructive command, insecure default, data loss).
- **P1**: does not work as written (compile error, removed symbol, missing import, wrong output).
- **P2**: works but violates policy (missing tier, prompt characters, no expected output, parity gap).

## Pass threshold

One gate has a measured comparator behind it; the rest are baselines this skill sets. Say which is which every time you report them; [./references/published-findings.md](./references/published-findings.md) holds the citations and the circulating claims this skill refuses to repeat.

**Gate with a measured comparator:**

1. **Deprecated-API rate below 43%.** Above it, build a deprecation-detection gate before anything else. 43% is the deprecated-API rate Zhou and Walker (FSE 2016) measured in the Stack Overflow posts they investigated; the figure is theirs, using it as a gate is this skill's choice. A governed corpus doing worse than public Q&A has a detection problem, not an authoring problem.

**Skill baselines - override with the team's own data:**

2. Zero P0 findings, and 100% of samples on the primary adoption path (quickstart, auth, first call) tier Run and green in CI.
3. Compile/run pass rate ≥90%; below that, stop new authoring and run a remediation sprint first. No vendor publishes this gate; it is a recommendation, well supported by how badly ungoverned snippet corpora do (1.00% of Stack Overflow's Java snippets compile, MSR 2016; 24.4% of public Python gists run out of the box, Gistable, ICSME 2018) but not a standard.
4. ≥80% of the whole corpus is tier Run or Compile-only and executed by CI.
5. Parity coverage ≥90% across tier-1 languages (tested cells ÷ scenarios × tier-1 languages), and no sample's last _successful run_ older than the policy's freshness window.

Re-run the audit after each fix batch rather than declaring victory from the fix list. When threshold 4 cannot be met, cut samples instead of lowering the bar; a deleted sample costs a reader nothing, an untested one costs them an afternoon.

## KPIs

- Tested-sample share and parity coverage, tracked per release rather than per audit.
- Mean time from a red CI sample to a merged fix; the real measure of whether ownership exists.
- Support tickets or issues quoting a sample verbatim.
- Copy-button clicks per sample, where the docs platform exposes them: high-copy samples earn tier Run first.
- Sample age distribution: count of samples whose last successful run exceeds the freshness window.
- Rubric score per dimension over time, not the total; the total hides which axis is failing.

## Failure modes

| Symptom                                        | Fix                                                                                                             |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Samples pass CI but fail for readers           | CI installs from the working tree; install the published artefact instead                                       |
| Sample suite disabled after flaky failures     | Split hermetic (per-PR) from integration (scheduled); fix fixture teardown before re-enabling                   |
| Fragment cannot run because imports are elided | Single-source from a real file and publish a marked region; hide setup, never delete it                         |
| Reader pastes a placeholder verbatim           | Use angle brackets and reserved-range hosts, never a plausible fake value; explain each placeholder             |
| Same scenario behaves differently per language | Fix parity by scenario and outcome, not by translating one language's code                                      |
| Audit was a read-through of the top pages      | Census the whole corpus mechanically; stratify the human sample - see the negative example in `audit-method.md` |
| Policy written, corpus never re-audited        | Put the audit in the release checklist; a policy nobody measures is a wish                                      |
| Samples rewritten for style, not correctness   | Delegate style to the ecosystem's formatter and linter; spend review on behaviour                               |
| Docs build stays green while samples are red   | Fail the docs build on sample failures, or the red mark gets ignored                                            |
| Owners assigned to hand-pasted Markdown        | Move samples into compilable source first; ownership without a mechanism is a name on a wiki page               |
| A quoted benchmark nobody can source           | Check `published-findings.md`; it lists the circulating claims this skill refuses                               |

## References

- See [./references/sample-policy-template.md](./references/sample-policy-template.md) for the policy document to fill in.
- See [./references/audit-method.md](./references/audit-method.md) for the census/stratified method, the rubric and a negative example.
- See [./references/audit-checklist.md](./references/audit-checklist.md) for per-sample checks, severity anchors and a good/bad worked pair.
- See [./references/verification-patterns.md](./references/verification-patterns.md) for execution tiers, single-sourcing and the CI shape.
- See [./references/language-parity-matrix.md](./references/language-parity-matrix.md) for language tiering, the matrix and drift patterns.
- See [./references/governance-and-ownership.md](./references/governance-and-ownership.md) for the three ownership models, metadata-driven governance, blocking CI gates and the migration order.
- See [./references/published-findings.md](./references/published-findings.md) for sourced figures, self-set baselines and claims to refuse.
- Run [./scripts/sample-audit.py](./scripts/sample-audit.py) to extract and mechanically lint every fenced sample in a docs tree.
- See samber/developer-relations-skills@developer-tutorial for teaching tutorials, a primary consumer of these samples.
- See samber/developer-relations-skills@developer-docs-structure-audit for where content belongs across a docs site.
- See samber/developer-relations-skills@version-migration-guide for before/after samples in breaking-change guides.
- See samber/developer-relations-skills@developer-troubleshooting-docs for the error pages a failing sample should link to.
- See samber/developer-relations-skills@coding-agent-docs-optimization when the sample's consumer is an agent, not a human.
- See samber/developer-platform-skills@api-reference-quality for per-endpoint reference completeness; this skill owns sample policy, testing and language parity, that one owns endpoint-level coverage.
