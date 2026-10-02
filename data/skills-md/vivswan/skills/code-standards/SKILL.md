---
name: code-standards
description: Use when writing code changes, sweeping or shortening comments (including file-size or comment-cap findings), or asked to apply house code standards.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Code Standards

House standards for code and the artifacts around it. Apply them while writing. Check them while reviewing.

Where a standard has a canonical case (the specimen that set the rule), it is stated inline or in the standard's `references/` file. The concrete case recalls better than the rule. The `references/` file named under each standard carries the full detail: the why, the how-to-apply list, and the boundaries and exceptions.

## The Standards

### Fix the class, not the instance

A systemic problem gets a root fix that makes recurrence impossible, never only a fix of the case at hand. The `/never-twice` skill owns this rule and its response ladder. Specimen and full detail in `references/design.md`.

### Guard recurring problems with tests

A problem that recurs, or plausibly will, ships with a test, tripwire, or pipeline fix that catches it at the source. This is rung 2 of the `/never-twice` ladder. Full detail, including the guard-outside-your-reach case, in `references/design.md`.

### General-purpose over special-case

Parameterize the axis that keeps changing instead of hardcoding today's instance.

Specimen: a safety classifier whose rulebook kept changing was built as a classifier FACTORY with the rubric as an input. Any rubric change produces a new classifier for free, and the same machinery serves uses beyond safety.

Full detail, including the one-pipeline-per-concept rule (the page that grew three visibly diverging error-band renderers) and where DRY stops: `references/design.md`.

### Maintainability over effort

Code quality outweighs diff size and effort spent. A big refactor is always better than a fix done the wrong way: wrong-shaped fixes compound into tech debt.

- Take the larger refactor when it is cleaner, and reduce complexity.
- Enforce invariants in types rather than repeated checks (see the `/no-invalid-states` skill).
- Use assertions to pin invariants the type system cannot carry: one assertion at a boundary removes whole families of downstream edge-case handling.

Specimen: a documented workaround hybrid was reworked outright rather than kept. Never preserve a workaround to keep a diff small.

Full detail: `references/design.md`.

### Prefer a library over hand-rolling

Never hand-roll what a good library already does: the hand-rolled version is maintained for as long as the code lives, the library by its authors. A large library, or a fit that is unclear, is a question to the owner before the work. Otherwise the library wins.

Specimen: an audit of one repository's CI scripts found five whose whole job existing tooling already did. A published package covered four (two schema fetchers, an events enum, generated action docs). A build followed by `git diff --exit-code` covered the drift check.

Full detail, including what makes a library good and the one exception (a library that needs a runtime or API the repository has dropped): `references/design.md`.

### Minimum standard for tests

A floor every test clears, not a recipe for which tests to write. Fuzzing, property-based, integration, and other richer tests are welcome, and each of them still meets this bar. A test asserts a whole outcome, not one field of it.

Agents drift toward many small weak tests. The fix is tests that each pin a whole outcome, which leaves fewer of them as a side effect, not a goal.

- **The drift question.** Every test answers "what would drift silently without this?" in its name or first line. Three answers count: an external fact the platform does not enforce for us, a cross-file consistency the source cannot express, or a regression with a named incident. "The source says so" means no test.
- **A constant is the source.** A test of a single constant restates the source and grows with it. So does a test of a variable that is itself the source of its value (a default, a key name, an argv literal, a path).
- **Pin the value where it leaves the program** (the bytes written to a file, the line printed, the request sent), and only when that boundary is an external contract.
- **Shape-only tests go.** Delete tests that only assert a shape, a type, or that something exists. If that fact matters, assert it inside a test that also checks the value.
- **Parametrize one axis.** When hand-written cases differ only along one input axis, replace them with one parametrized case list.
- **Prove each guard test:** show it failing on the bug it guards, and for that reason. Reintroducing the bug is the standard form, and a pre-fix red run is the same control. Run that test file alone, not the suite.
- **Red-then-green is for behavior changes,** a fix made by deleting code included. A deletion with no behavior of its own (an unused setting, a dead path) proves itself with a census (grep counts before and after), never with a test manufactured so that something goes red. The census goes in the PR body, or in the landing report with no PR.
- **Fixtures are hand-authored,** never recorded from real data: a file measured or copied from the author's real environment identifies the author with no name in it. A tool that measures real data requires an explicit output path outside the repository and refuses one inside it.

Specimen: an extractor had fifteen tests each asserting one key of the returned dict. Folded into one parametrized test pinning the whole dict per scenario, the file went from 81 test functions to 44.

Every one of the seven bugs the suite existed to catch still failed when reintroduced. A test that ignores a column cannot catch a regression in it.

Specimen: builders on a workflows repository shipped eleven PRs in one day of shape tests that restated the yaml they had just read. Two examples: a census that no workflow sets `cancel-in-progress: false`, and a pin that a job's `needs` equals the list in the file. Such a test changes in the same commit as the source, so nothing can drift under it: delete it.

Specimen: a test audit found `expect(DEFAULT_HOME).toBe("~/.local/share/app")`. Deleted. Its replacement runs the installer with no home override and reads back the file it wrote under that path, because the path is where the value reaches the user's disk.

Specimen: a statistical profile measured from its author's real sessions sat committed as a test fixture with a comment saying so. Replaced by a hand-written fixture. Every figure of the old file was grepped out of the replacing PR, and the history was rewritten to drop the original.

Full detail: `references/tests.md`.

### Comments carry only what the code cannot show

A comment is read by humans and agents, the human first. The code is the single source of truth.

- **Content**, the kinds a comment may carry:
  - the reason a choice was made when the obvious choice was rejected
  - an invariant another file relies on, naming the file
  - an external system's quirk and what breaks without the workaround
  - a consequence of changing the line that is not visible here
  - the one input that motivated a guard
- **Never a comment:** what the code does, its types, its control flow, its history, the alternatives. History and alternatives go in the commit message.
- **Tell first, then show.** One or two sentences say what the code cannot show. A block follows only when it shows the fact faster: an arrow flow for a sequence, aligned rows for facts that share a shape.
- **Uniform shape is the wall:** a paragraph, or every fact as its own line with nothing shown. Past the two sentences, a fact is shown or cut.
- **No limits here.** Length and width caps are the fleet's file-size check. Never pack prose to fit a cap: cut honestly.
- **Test, before writing or keeping one:** "What does this say that the code does not?" and "Could a tired human read it in one pass?" Fail either: rewrite or delete.

Specimen, a stack of eight one-fact sentences rewritten as tell, then rows:

```ts
/**
 * The ONE "entry uses this credential field" judgment; it judges the ENTRY alone, so it errs toward "uses it".
 * Wire narrowing still drops what cannot ride, so consumers gate refusals, never the send.
 *
 * Authorization-named header resolved  -> skips the OAuth exchange
 * X-API-Key-named header resolved      -> owns that carrier
 * declared header, value unknown       -> lowers no other field's judgment
 */
```

Full detail, the before/after specimens, and the TODO ban: `references/comments.md`.

### No barrel files or pass-through functions

Delete these and repoint the importers or callers at the defining module or real function:

- an import-only index file
- a "keep old importers compiling" re-export left after a move
- a function whose whole body forwards to another function without adding anything

A wrapper earns its existence only by adding something real (a default, a conversion, error mapping, an injected dependency, a narrowed type). In Python, `__init__.py` stays EMPTY unless absolutely necessary: re-exports there are the same barrel.

Full detail, including the migration-staging exception and what is not a barrel: `references/structure.md`.

### No planning references in code

Code and comments never reference planning artifacts: work-package names, spike or phase labels, plan codenames, audit finding numbers. The next reader has the code, not the plan.

Specimen: a comment like "WP-B spike, part 2:" has no meaning outside the planning. Comments describe purpose and constraints, not where the code came from.

Full detail: `references/comments.md`.

### Lean AGENTS.md

AGENTS.md (and CLAUDE.md) holds the project's guiding principles and nothing an agent can deduce elsewhere. Code is the source of truth, and implementation detail lives there. README, CONTRIBUTING, and the rest of the repository's documentation are the `/docs-discipline` skill's pages.

- **Keep:** what the project is, the conventions the owner wants kept, safety constraints, the toolchain entry points, and pointers.
- **Cut:** anything a specific file answers, even when essential. That means layout trees, the commands block (the manifest and hooks are the source), naming conventions a linter carries, checklists a test enforces, and per-module behavior. A one-line pointer replaces each.
- **Shape:** short bullets a human skims. No long paragraphs, no walls of text.
- **No tests pin it.** A test asserting AGENTS.md text turns guidance into a fixture. Delete it.
- **No review loop.** A change touching only AGENTS.md or CLAUDE.md gets no codex or Copilot round and is committed with `git commit --no-verify`. The PR opens ready and its CI is the only gate.
- **Already lean:** leave it alone and say so.

Specimen: a tail of 66 lines (a layout tree, a 17-item authoring checklist the smoke test enforced, release notes) became 15: one line on what the repo is, five principles, two working rules. The checklist moved to the authoring doc it was duplicating.

Full detail: `references/artifacts.md`.

### Commit messages carry content only

Commit and PR messages state what changed and why, following the repo's subject conventions.

No AI or tool attribution lines. No hard wrapping of the body at 72 columns: a wrapped body renders as ragged mid-sentence breaks in GitHub's soft-wrapping UI. No PII, nothing that tells a reader who the author is, how they work, or how their machine is set up (the `/pr-and-issue-discipline` skill's rule).

Specimen of the one sanctioned attribution, human community credit in repos that take contributions: `fix: ... (#NN, thanks @user)` in the subject, `Co-authored-by:` trailers for humans whose code landed. Credit for people, never for tools.

Full detail, including the email-patch exception: `references/artifacts.md`.

### No blobs of text

Anything a human skims uses scannable structure: paragraphs of 1 to 3 sentences, and when the content is enumerable, enumerate it. The shape rules and the paragraph probe live in the `/docs-discipline` skill. PR bodies follow the `/pr-and-issue-discipline` skill's Readability rules.

## Workflow

1. **Writing code:** apply the standards as you go. They are cheaper at write time than at review time.
2. **Reviewing:** check the Review Criteria, cite the specific standard in each finding, and prefer suggesting the class fix over the instance patch.
3. **Boundaries:** when a standard needs its boundaries (what counts, what is exempt, how far to take it), load the matching `references/` file before acting on it.
4. **Type-level fixes:** when a finding calls for enforcing invariants in the type system (lifecycle flags, must-call-X-before-Y ordering, fields that must appear together), apply the `/no-invalid-states` skill for the refactor itself.
5. **Conflicts:** when a standard conflicts with an explicit user or project decision, follow the decision and record which standard was consciously set aside.

## Review Criteria

- Instance-only fixes: does the change prevent recurrence (test, type, tooling), or just patch the case at hand?
- A recurring or recurrence-prone problem fixed again without a guard test, tripwire, or pipeline fix (or a proposal to the user when the pipeline is out of reach).
- Tests that assert only a shape, a type, or that something exists.
- Hand-written test functions that differ only along one input axis and should be one parametrized case list.
- A guard test never seen failing on the bug it guards.
- A new test that restates the source it reads (a workflow test pinning `needs` to the list in the yaml, a constant pinned to its own literal), or whose name or first line does not say what would drift silently without it.
- A test manufactured for a deletion with no behavior of its own in place of a census in the PR body or landing report.
- A fixture recorded from real data, a provenance comment saying so, or a tool that measures real data with a default output path or one inside the repository.
- Special-casing: a new near-copy of existing logic where the varying axis should be a parameter.
- Complexity added to keep a diff small: flags, nesting, or repeated checks where a cleaner refactor or a stronger type was available (the `/no-invalid-states` skill covers the type-level fix).
- Hand-rolled code whose whole job a good library already does. The finding names the library and what it covers.
- Comments that say what the code shows: what it does, its types, its control flow, its history, the alternatives.
- Comments a reader cannot take in one pass: uniform shape (a paragraph, or every fact as its own line with nothing shown past a two-sentence tell), several ideas in one sentence, prose packed to fit a cap.
- Paragraph-long comments justifying workarounds (flag the underlying code, not the comment alone).
- Barrel files, re-export shims, or pass-through functions that only forward to another function or module.
- Planning artifacts (work packages, phases, codenames, finding numbers) referenced in code or comments.
- AGENTS.md or CLAUDE.md carrying anything deducible from the code or another doc (layout trees, enforced checklists, module behavior), a long paragraph, or a test that pins its text.
- Attribution lines or hard-wrapped bodies in commit messages and PR descriptions.

Triage findings against the standards above. Each criterion maps to one.

## References

- `references/design.md`: fix the class, general-purpose over special-case (one pipeline per concept, DRY boundaries), maintainability over effort
- `references/tests.md`: the minimum standard for tests, what counts as weak, the drift question every test answers, proving a guard test with a negative control, the census rule for deletions, hand-authored fixtures and the output-path rule for tools that measure real data
- `references/comments.md`: what a good comment carries, tell then show, the two-question test, the specimens, the TODO ban, planning references
- `references/structure.md`: barrels, compatibility re-exports, escort functions, migration staging
- `references/artifacts.md`: lean AGENTS.md, content-only commit messages and their two exceptions
