---
name: spec-traceability
description: Keeps spec IDs traced in tests, code, commits and reports; flags dangling or untraced IDs. Use when a task cites a spec ID (REQ-4, SCR-2), asks what is required or in scope, or hits a spec gap. Not for screens (screen-contracts).
---

# Spec traceability

The app's spec says what to build, and every piece of work can prove which part of it it serves: each
requirement, screen, decision and non-negotiable has a stable ID in a markdown spec folder; the first
failing test, the code comment, the end-to-end flow, the commit body and the report quote that ID;
and two scripts print any entry verbatim and prove that every citation in the repo and its history
resolves. Works the same for iOS and Android; an app without a spec gets a clean NOT APPLICABLE.

## Rules that must hold

1. **The spec decides what; its non-negotiables never bend.** If a task, a design, a library or another
   requirement would break a non-negotiable (`NN-` entries), stop and ask before writing code. Why: a
   silently traded rule passes every test of the new work and is caught by nobody.
2. **Quote the spec, never paraphrase it from memory.** Print the entry with
   `spec-lookup.mjs <id>` and put the ID and the rule in the first failing test's title or the comment
   above it, and in the commit body. Why: a misremembered number (4 seconds instead of 5, 4 free lists
   instead of 3) is the bug no test catches, because the test asserts the same wrong number.
3. **Cite IDs exactly as the spec defines them, and name screens by title and ID together:**
   "Task list (SCR-1)". The prefixes come from the app's `contracts/spec.json` (default `NN-`, `SCR-`,
   `REQ-`, `DEC-`, `OOS-`). Why: a cited ID that does not exist, or a name paired with the wrong ID,
   sends the reader to the wrong requirement (`dangling-id`, `unknown-spec-section`,
   `screen-name-mismatch`).
4. **When the spec is silent, ambiguous or contradicts itself about anything a user would see, stop
   and ask:** quote the lines, give two or three options with a recommended default, and keep working
   on everything else. Never invent product behaviour; never ask what the spec already answers. Why:
   an agent's guess ships as a product decision nobody made.
5. **Use the documented default of an open decision and say so in the report;** ask only when the
   default stops working. Every open decision carries `Default:`, a settled one `Decided:`, and a
   settled decision is never asked again. Why: an open decision without a default blocks work, and a
   re-asked one wastes the reviewer's time (`entry-field-missing`).
6. **Build nothing the spec puts out of scope, and treat its numbers as limits, not targets.** A test
   or flow that cites an `OOS-` entry or a dropped requirement fails. Why: agents over-deliver, and
   every extra is code to test, translate, declare to the stores and maintain
   (`out-of-scope-traced`).
7. **IDs are stable forever.** A new entry takes the next free number; an entry is never renamed,
   renumbered or reused, and a dropped one stays with `Status: dropped`. Why: old commits, tests and
   reports cite it (`duplicate-spec-id`, `malformed-heading`, `invalid-field`).
8. **A built requirement is traced by a test or flow.** Mark a requirement or screen `Status: built`
   in the commit that adds its green test citing it, and a built screen's `Route:` names a file that
   exists. Why: "built" with no test is a claim, not evidence (`untraced-requirement`,
   `route-missing`).
9. **Traced IDs fit the commit and test reference patterns.** The commit-msg hook
   (`contracts/commits.json` `requirementRef`, else `scripts/git/requirement-ref.json`) and
   tdd-workflow's `requirementIdPattern` must accept every traced ID. Why: an ID the hook rejects
   makes the commit that cites it impossible (`ref-pattern-mismatch`).
10. **Platform differences are written down, never assumed.** When iOS and Android behave differently
    (a permission prompt, back navigation, a widget), the entry says so with `Platforms:` or splits
    into one child per platform, each traced by its own test or flow; a spec that describes one
    platform only is silent about the other (rule 4). Why: the platform nobody specified ships
    whatever the library does by default.
11. **Behaviour several features need is built once, in the shared layer,** and cited where that
    shared piece is tested, never copied inside one feature. Why: copies drift, and the spec describes
    the behaviour once for the same reason.

## Workflow

1. **Find out whether the app keeps a spec:** `node ${CLAUDE_SKILL_DIR}/scripts/spec-lookup.mjs . --list`.
   `NOT APPLICABLE: the app keeps no requirement spec` means requirements come from the issue or the
   acceptance criteria: quote them with their key (`TASKS-12`, `#41`) and skip to step 6. Start a spec
   (step 9) only when the developer wants one.
2. **Print the entries the task serves:** `node ${CLAUDE_SKILL_DIR}/scripts/spec-lookup.mjs . REQ-4 SCR-2`
   (`--list --kind screen` lists one kind, `--brief` prints headings only, `--from <file>` reads IDs
   from a file). An entry marked dropped or out-of-scope prints a NOTE: do not build it.
3. **Read the non-negotiables the task touches** (`--list --kind non-negotiable`): any network, data,
   layout, text, accessibility or permission work touches at least one. Plan so none bends (rule 1);
   [references/questions-and-decisions.md](references/questions-and-decisions.md) lists the typical
   collisions.
4. **Check decisions and scope:** `--list --kind decision` and `--kind out-of-scope`. Use each open
   decision's default and note it for the report; build nothing out of scope.
5. **If the spec is silent, ambiguous or contradicts itself** on anything a user would see, or covers
   one platform only, write the requirement question (quoted lines, options, default) as
   [references/questions-and-decisions.md](references/questions-and-decisions.md) describes, send it
   in git-commits-and-reporting's request format, and keep working on the rest.
6. **Write the IDs into the work,** as [examples/spec-citations.md](examples/spec-citations.md) shows:
   the first failing test's title or comment quotes the rule (`it('moves the task to Done (REQ-2)')`),
   a constant that holds a decision's default cites it, flows name screens as "Task list (SCR-1)", the
   commit body names the IDs, the report names screens by title and ID.
7. **Update the spec in the same commit:** set `Status: in-progress` when a slice starts and
   `Status: built` when its citing test is green. When a changed requirement changes a test
   expectation, that commit updates the entry, says why in its body and carries
   `Spec-Change: <ID> <what changed>` (git-commits-and-reporting owns the format); a spec edit with no
   test change carries no trailer.
8. **Run the check** from the repo root: `node ${CLAUDE_SKILL_DIR}/scripts/check-spec-refs.mjs .`, and
   for the session's commits `node ${CLAUDE_SKILL_DIR}/scripts/check-spec-refs.mjs . --range <base>..HEAD`
   (`--trace` adds the requirement-to-test matrix for the report). Fix every `FAIL` line and rerun
   until it prints `RESULT: PASS`.
9. **Starting a spec** (once per app): copy [templates/docs/spec/](templates/docs/spec/) to
   `docs/spec/` and [templates/contracts/spec.json](templates/contracts/spec.json) with its schema to
   `contracts/`, replace the Tasks examples with the app's own entries (all `planned`), and keep the
   default prefixes unless the app already has IDs. [references/spec-format.md](references/spec-format.md)
   has the heading grammar, the fields, every contract key and what counts as a citation. If the
   commit contract sets its own `requirementRef` pattern, make it accept the spec's IDs (rule 9).
   When the app had no `docs/` before, the root tooling treats it as pre-existing: in the same commit
   add `docs/` to `.prettierignore` and `'docs/**'` to `PRE_EXISTING` in `eslint.config.mjs` (with a
   `Gate-Change:` trailer), or declare `"docs"` in `rn-skills.config.json` `"layoutEntries"` when the
   team wants Prettier to format the spec.

## Definition of done

- [ ] The entries the work serves were printed with `spec-lookup.mjs` and are quoted in the first
      failing test (title or comment) and in the commit body.
- [ ] No non-negotiable was traded away; any collision was raised before building.
- [ ] Every open decision the work relied on is named in the report with the default used, and every
      spec gap was asked about with quoted lines and a default.
- [ ] Nothing out of scope was built; numbers from the spec were used as limits.
- [ ] Entries finished by this work are `Status: built`, each cited by a test or flow; behaviour that
      differs by platform is specified and traced per platform.
- [ ] The check prints no SKIP line; an app with no spec prints
      `NOT APPLICABLE: the app keeps no requirement spec (...)`, which passes.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-spec-refs.mjs . --range <base>..HEAD` prints `RESULT: PASS`
      (before the session's first commit the range is empty: it prints one `NOTE --range ... holds no
      commit yet` line and checks the files only)

## Anti-patterns

- **Citing from memory** ("REQ-2 says Undo lasts 4 seconds"). Print the entry: the time lives in
  DEC-1, and its default is 5 seconds.
- **Inventing an ID for a new idea** (`// Leaderboard (SCR-16)`). A new screen is a product decision:
  the entry is added to the spec with the reviewer's agreement first; until then the checker reports
  `dangling-id`.
- **Renumbering the spec to tidy it up.** Every old commit, test and report now points at the wrong
  entry. Add, drop, never reuse.
- **Marking an entry built because the code exists.** Built means a test or flow cites it and passes.
- **Asking the reviewer how to build something.** Architecture and libraries are engineering
  questions; the reviewer answers what the user gets.
- **Asking about something the spec or a default already answers.** Read the entry first; ask only
  about real gaps.
- **"Helpful" extras** (a widget, a sign-in for later sync, sample data beyond the stated count).
  Out of scope means not built.
- **Writing the iOS behaviour into the spec and letting Android do whatever the library does.**
  Split the entry per platform and trace each.
- **Silencing a real citation with `spec-refs-ignore`.** The marker is for test data that names a
  missing ID on purpose.
- **Bare short codes as IDs** (`S7`, `D4`). They collide with crypto names, model numbers and data;
  keep a prefix that ends in `-`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/spec-format.md](references/spec-format.md) | The spec folder, heading grammar, fields and statuses, every `contracts/spec.json` key, what counts as a citation, tracing, agreement with the commit and test patterns, every rule, adopting a spec, when multi-package | Workflow step 9, and whenever the checker reports something unexpected |
| [references/questions-and-decisions.md](references/questions-and-decisions.md) | What the spec decides, non-negotiables and their collisions, when and how to ask, open decisions and defaults, out of scope and content caps, changing the spec, shared behaviour | Workflow steps 3 to 5 |
| [examples/spec-citations.md](examples/spec-citations.md) | One requirement followed from `spec-lookup` through the test, a constant, a flow, the commit, the report and a question, with what the checker flags | Once, before the first slice in an app with a spec |
| [templates/docs/spec/README.md](templates/docs/spec/README.md) | `docs/spec/README.md`: how the spec folder is organized and changed | Workflow step 9 |
| [templates/docs/spec/non-negotiables.md](templates/docs/spec/non-negotiables.md) | `docs/spec/non-negotiables.md`: four Tasks-app non-negotiables, each with `Enforced by:` | Workflow step 9 |
| [templates/docs/spec/screens.md](templates/docs/spec/screens.md) | `docs/spec/screens.md`: three screens with actions, states and routes | Workflow step 9 |
| [templates/docs/spec/requirements.md](templates/docs/spec/requirements.md) | `docs/spec/requirements.md`: Tasks requirements, including a per-platform child (iOS and Android notification permission) | Workflow step 9 |
| [templates/docs/spec/decisions.md](templates/docs/spec/decisions.md) | `docs/spec/decisions.md`: an open decision with options and default, and a settled one | Workflow step 9 |
| [templates/docs/spec/out-of-scope.md](templates/docs/spec/out-of-scope.md) | `docs/spec/out-of-scope.md`: what this version does not build | Workflow step 9 |
| [templates/contracts/spec.json](templates/contracts/spec.json) | `contracts/spec.json`: the ID scheme, filled with the defaults | Workflow step 9, or when the app uses other prefixes |
| [templates/contracts/spec.schema.json](templates/contracts/spec.schema.json) | `contracts/spec.schema.json`: JSON Schema of the contract | With the contract |
| `scripts/spec-lookup.mjs` | Prints spec entries verbatim (`REQ-4 SCR-2 spec 1.1`), `--list [--kind]`, `--brief`, `--from`; fails on unknown IDs with the nearest ones | Workflow steps 1 to 4, whenever a spec line is quoted |
| `scripts/check-spec-refs.mjs` | Checks the spec (headings, unique IDs, fields, routes, defaults, reference patterns) and every citation in files and commits (dangling IDs, sections, name pairs, tracing, excluded work) | Workflow step 8 and the definition of done |
| `scripts/lib/spec-model.mjs` | Reads the contract and the spec entries (shared by both scripts) | When changing a script |
| `scripts/selftest.mjs` | Proves both scripts pass the shipped templates and catch each planted bug | After changing a script or a template |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `assets/requirement-ref.json` | The default requirement-reference pattern of the commit rules, synced from git-commits-and-reporting's `scripts/git/requirement-ref.json`; used when the app has no copy and no `requirementRef` | Never by hand (synced) |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/bases/app/` | A minimal Tasks app the fixtures add to the shipped templates | When changing the fixtures |
| `tests/fixtures/` | Overlay cases on the templates: good, pass, bad (one per rule) and error | When adding a rule to a script |

## Related skills

- `tdd-workflow` - turns a quoted entry into the first failing test; its history check reads the same IDs.
- `git-commits-and-reporting` - commit bodies, `Spec-Change:` trailers, reports and the request format for questions.
- `screen-contracts` - how each screen named in the spec is built (states, testIDs).
- `design-visual-parity` - proves a built screen matches its approved design baseline; the spec says what it shows.
- `navigation-and-routing` - the route files that screen entries name.
- `e2e-maestro` - the flows that trace screens and requirements on both platforms.
- `react-native-conventions-index` - which skill to load for a task.
