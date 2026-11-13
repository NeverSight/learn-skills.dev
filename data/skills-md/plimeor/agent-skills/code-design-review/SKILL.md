---
name: code-design-review
description: "Assess whether a design holds up against modern software-engineering principles: complexity and cognitive load, change economics, boundary correctness, and agent legibility. Use when the user asks whether a design, module boundary, API, data flow, design doc, or change shape is sound, holds up, or withstands scrutiny — a principle-based judgment, not a merge gate. Near miss: use code-review for exhaustive, coverage-accounted review of a diff, plan, or parity scope."
---

# Code Design Review

Judge whether a design holds up against software-engineering principles, from the one perspective that matters: a future maintainer doing real tasks. This is consulting, not gatekeeping — the deliverable is a verdict with ranked concerns, not a merge decision. Focused examination is allowed; the focus is stated. Report only; no edits without separate authorization.

## Subject

Fix what is being judged before judging it: the design surface — module boundary, API, data flow, state ownership, design doc, or the shape of a change — and the maintainer tasks it must serve (extending it, debugging it, changing it safely, understanding it cold). Every concern anchors to one of those tasks; nothing is judged against taste, symmetry, or fashion. When the artifact is readable, read it — don't judge a design from its author's description alone.

## Core Model

Every concern maps a concrete surface to a **reader task** plus at least one **symptom** and one **cause**:

- **Symptoms** — change amplification (one concept, many edits) · cognitive load (too much non-local knowledge) · unknown-unknown risk (needed information not discoverable, or the maintainer can't know it's needed).
- **Causes** — dependency (the surface can't be understood independently) · obscurity (important behavior, owner, invariant, or coupling isn't obvious).

Style preferences, naming opinions, and unmapped "cleaner" advice do not qualify as concerns. Two further guards:

- **Working code is not design evidence.** Tests passing prove correctness, not maintainability. Ask whether the surface has the shape it would have if the requirement had been known from the start.
- **Principles never override harder contracts**: explicit user scope and authorization, public API / schema / persistence / security / compatibility contracts, regression evidence for behavior changes, and domain constraints (auditability, incident response, distributed consistency, data integrity). When a principle conflicts with a harder contract, report the contract risk first; the principle is supporting context.

## Lenses

Four axes. Select the ones the subject activates and name the ones skipped, with reason. The axes overlap on purpose — a leaked invariant is a complexity fact and a change-cost fact; report the concern once, under the axis with the sharpest vocabulary for it.

### Complexity — can a maintainer understand this, and how much must they hold in their head?

Sources: John Ousterhout, *A Philosophy of Software Design* — https://web.stanford.edu/~ouster/cgi-bin/aposd.php · Artem Zakirullin, *Cognitive load is what matters* — https://github.com/zakirullin/cognitive-load · Dan North, *CUPID* — https://dannorth.net/cupid-for-joyful-coding/

- Apparent complexity is what a maintainer experiences doing a real task, not a property of the text. Line count, file count, and function length measure nothing by themselves.
- Working memory is small — roughly four non-local facts at once. Every fact a reader must import from elsewhere (a flag's meaning, an ordering constraint, another module's internals) occupies a slot; past the limit, reading becomes re-deriving.
- Complexity is incremental. Each tolerated branch / flag / fallback / nullable / wrapper / undocumented invariant compounds. Ask whether a change reduces underlying complexity or adds another tolerated shortcut.
- **Deep modules are about ratio.** Small caller-facing interface relative to hidden useful behavior. Large ≠ shallow; short ≠ deep. Ask what callers must know about ordering, retries, cache, validation timing, storage format, fallback rules.
- **Beware many shallow modules.** Decomposition has a cost: each extra module adds its responsibility and its interactions to the reader's working set. A cohesive large module often reads cheaper than five fragments; "smaller classes and shorter functions" is not a simplification argument.
- **Make the common case simple.** Common callers shouldn't pass options, know internal defaults, or handle rare states. Don't make all callers pay for flexibility only one needs.
- **General-purpose, not speculative.** General enough for known nearby needs; not contaminated by product-specific or one-off policy; not justified by imagined future extension.
- **Information leakage is the primary red flag.** Knowledge that should belong to one owner appears elsewhere — duplicated rules, mirrored validation, exposed data structures, ordering assumptions, generated-artifact coupling, error semantics, comments describing another module's internals. Ask which decision leaks, where it should live, and how many places must change if it changes.
- **Different layer, different abstraction.** A layer that only forwards calls, renames parameters, or wraps lower-layer concepts adds cognitive load without changing the model. Removing it should make the system harder — not easier — to understand.
- **Temporal decomposition is suspicious.** Splitting code by execution order scatters one concept across phases. Group knowledge by ownership and abstraction, not "first do this, then do that".
- **Pull complexity downward.** The owner absorbs complexity so callers stay simple — without hiding important errors or state. The right owner centralizes unavoidable knowledge.
- **Predictable: code does what it looks like it does.** No surprising side effects behind an innocent name, no action at a distance, no behavior depending on invisible state or call order. A deviation from the least-surprise reading is a defect in the interface, not in the reader.
- **Comments are interface tools.** Capture what code can't say: contract, units, invariants, rationale, side effects, concurrency, cross-module coupling. A long comment compensating for a weak abstraction is a smell, not a fix.
- **Names and consistency are cognitive contracts.** Same concept → same name; different concept → different name. Deviation from local convention needs a visible semantic reason.
- **Performance needs measurement.** Optimization-motivated complexity needs evidence of a real bottleneck and should stay behind a simple interface.
- Reject: "fewer lines" or "fewer files" as simplicity proof · "short function" / "small class" as goals in themselves · "large module" as a proxy for shallow · "it follows a pattern" when the pattern isn't local or semantically justified · "add a comment" instead of fixing a weak interface.

### Change economics — what does the next change cost, and is now the time to pay for structure?

Sources: Kent Beck, *Tidy First?* — https://tidyfirst.substack.com/ · Sandi Metz, *The Wrong Abstraction* — https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction · Carson Gross, *Locality of Behaviour* — https://htmx.org/essays/locality-of-behaviour/ · tef, *Write code that is easy to delete* — https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to

- Software design is an investment decision, not a virtue. Coupling is the cost of a change spreading **across** elements; cohesion is the cost of a change **within** one element. Structure is good when it makes the changes that actually arrive cheaper — not when it matches a shape catalog.
- An element can lack cohesion by being too large or too small: a fragment solving part of a problem must be coupled to the elements solving the rest, and changing the solution means changing them all.
- Structure changes and behavior changes are different activities with different risk. A design where behavior can't be changed without restructuring, or restructured without behavior change, has already coupled the two — that is itself a finding.
- **Tidy first only when it pays.** Restructuring is justified by a change it makes cheaper — one that is planned or demonstrably recurring — not by discomfort. "Tidy after" and "don't tidy" are legitimate outcomes of the same calculation.
- **Cohesion follows the domain.** Things that change together belong together; structure should mirror the domain's change patterns, not technical layering. When answering one domain question requires touching N technical layers, the architecture itself is change amplification.
- **Duplication is cheaper than the wrong abstraction.** Abstract when the pattern is understood, not when text repeats — two occurrences form a line that may point the wrong way. A shared abstraction that accumulates parameters and conditional paths for each new caller has already failed; the recovery is re-inlining the duplication and letting it show the right shape.
- **Weigh DRY against locality of behavior.** Extracting shared behavior trades local readability for a new coupling. The behavior of a surface should be understandable at its point of use; ask how far a reader must travel from trigger to behavior before treating deduplication as free.
- **Design for deletion.** The measure of a boundary is the blast radius of removing what's behind it. Code that is easy to delete — isolated, unshared state, countable callers — is cheap to be wrong about; code woven into everything must be right forever. Ease of deletion, not ease of extension, is the default to optimize for.
- Reject: "more DRY" when it creates the wrong shared dependency · "we might need it later" ahead of a demonstrated change pattern · "refactor while we're here" without naming the change it makes cheaper · preserving an abstraction because it exists while it accretes parameters and modes — sunk cost is not cohesion.

### Boundary correctness — can invalid state exist past this boundary, and where do effects live?

Sources: Alexis King, *Parse, don't validate* — https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ · Gary Bernhardt, *Functional Core, Imperative Shell* — https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell

- The strongest correctness is structural: a state that cannot be represented cannot occur, and no downstream code needs to defend against it. Prefer a boundary that transforms less-structured input into a more-structured type once over checks that verify and then forget.
- Stratify the program into a parse phase (all input rejection happens here) and an execute phase (illegal input is impossible here). Failure concentrates where it can be handled; the core is freed from defensive noise.
- **Parse, don't validate.** A check whose result isn't captured in the type or structure will be repeated downstream — or worse, assumed. Ask: after this validation, what stops an unvalidated value from reaching the same code path?
- **Make illegal states unrepresentable.** Nullable-but-never-null fields, paired fields with an implicit invariant ("when status is X, payload is set"), stringly-typed enums, boolean combinations of which only three of four occur. Each representable-but-illegal state is a latent branch every reader must rule out and every agent must rediscover.
- **Functional core, imperative shell.** Decision logic stays pure; effects — IO, clock, randomness, network, persistence — live at the shell. The test: can the interesting logic be exercised without mocks? A design that needs test doubles for its own domain rules keeps effects in the wrong place.
- **Mirrored validation marks a failed boundary.** The same rule enforced in UI, API, and storage layers means the boundary never captured its guarantee in a type or contract; the copies will diverge silently.
- **Define errors out of existence — carefully.** Eliminating an error case is valuable only when the new contract is explicit, safe, observable, and authorized. Not a license to hide security, data integrity, auditability, observability, compatibility, or recovery information.
- Reject: defensive checks scattered "just in case" instead of a boundary that makes them unnecessary · a doc comment promising an invariant a type could enforce · mocking your own domain logic to reach testability — a boundary defect wearing a test harness.

### Agent legibility — can the newest maintainer, human or agent, operate here and verify its own work?

Sources: emerging practice, 2024–2026; e.g. Stack Overflow, *Building shared coding guidelines for AI (and people too)* — https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/

- An agent is a maintainer with extreme versions of ordinary human limits: zero memory of past decisions, a hard working-set budget, and reliable obedience only to what is machine-checked. Design that serves it serves cold human readers too — this axis contradicts none of the others; it re-weights them toward explicitness and verifiability.
- What an agent actually obeys is what fails a check: types, tests, linters, build gates. A prose convention without enforcement is a suggestion.
- **Machine-checkable contracts over prose conventions.** Every convention that matters should have a type, test, or lint rule that fails when violated. Ask which of the repo's stated rules would actually stop a wrong change.
- **Tests are the executable spec.** To the newest maintainer, a behavior without a test is undefined behavior — nothing marks it as intended, so nothing prevents its loss. Tests assert public behavior, not implementation details, or the spec they encode is the wrong one.
- **Self-verification is a design property.** After a change, one discoverable command should answer pass or fail. A repo whose correctness is judged by tribal knowledge or manual poking cannot be safely maintained by an agent — or by a new hire.
- **Greppable, boring, explicit.** Searchable names (no dynamically constructed identifiers), one concept one name, behavior visible at the point of use, no action at a distance via reflection, metaprogramming, or implicit registration. Cleverness that compresses text expands the working set.
- **Context is a budget.** The knowledge needed to change a surface should fit in a bounded neighborhood: the file, its imports, and written-down local rules (`AGENTS.md`, `CLAUDE.md`). Ask what must have been read to make this change without breaking an unstated rule — every unwritten rule is an unknown-unknown planted for the next maintainer.
- Reject: "it's documented in the wiki" — off-repo knowledge is invisible to the newest maintainer · "the team knows" — institutional memory is not a contract · conventions enforced by reviewer vigilance instead of tooling.

## Judgment

Depth follows risk: concentrate where complexity concentrates — the interfaces most callers touch, the knowledge duplicated across owners, the layer whose removal would change nothing. Sampling is legitimate here; what makes it honest is naming what was examined and what was not. For each concern, state the smallest correction that resolves the mapped symptom. When a material design choice is questioned, compare a real alternative owner, representation, or boundary — no strawmen, and no ceremonial alternatives on trivial choices.

## Output

User's primary language for prose; keep code symbols and paths original. Return:

1. **Verdict** — holds up / holds with concerns / does not hold — with the load-bearing reasons.
2. **Concerns**, ranked by impact on maintainer tasks, each naming surface, reader task, symptom, cause, and smallest correction.
3. **Lenses checked and passed**, briefly.
4. **Boundary** — lenses not applicable or not assessed, surfaces not examined, each with its reason.

## Stop Rules

Finish only when the verdict is stated with its reasons, every concern carries the full surface → reader task → symptom → cause mapping, and the examined/unexamined boundary is named. If the subject or its maintainer tasks are too unclear to judge, stop with the clarifying question rather than substituting taste. No edits, commits, or pushes.
