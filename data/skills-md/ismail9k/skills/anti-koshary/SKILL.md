---
name: anti-koshary
description: >
  Two-pass audit and cleanup for a codebase that has started to congeal —
  spaghetti code, or "koshary code," where the layers have collapsed:
  business logic lives in the controller, the same validation sits in five
  files, and nobody wants to open the 800-line one. Pass 1 reports layer
  collapse, duplication that will drift, functions nobody reads, and dead
  code as a prioritized list and changes nothing; Pass 2 fixes in a safe
  order once the user approves. Security holes and vulnerable dependencies
  are covered too, as a later section rather than the headline. Use this
  whenever the user asks to audit, review, or clean up a codebase — and
  also when they say "this codebase is a mess," "spaghetti code,"
  "technical debt," "this is unmaintainable," "duplicated logic," "dead
  code," "what's wrong with my code," or ask for a security review.
  Trigger it even when they never use the word "audit."
---

# Anti-Koshary

Koshary is rice, pasta, and lentils in one bowl. Each is good; once mixed,
you will never separate them again. Koshary code is the same failure — a
sound stack whose layers have been stirred together until no piece can be
lifted out on its own.

That stirring is what this skill is for. You are looking for its symptoms:

- business logic living in controllers, components, and route handlers
- the same validation or formatting copy-pasted across several files
- functions and files that grew past the point anyone reads them
- abstractions that never paid for themselves, coupling callers that had
  every reason to stay apart

And, further down the report, the problems that tend to accumulate in the
same bowl but are not what the user came here for:

- secrets, missing auth checks, and unvalidated input that nobody revisited
- dependencies pinned years ago and quietly carrying CVEs

## Standalone by design

This skill depends on nothing else. No companion skill, no config file, no
issue tracker, no prior setup step — it runs on any repository, in any
stack, cold. Keep it that way when editing: everything it needs lives in
its own directory.

## When this applies

The user wants to know what is wrong with an existing codebase, or wants it
cleaned up. It does **not** apply when they are asking you to build a new
feature — that is forward work, and an audit mid-feature just adds noise.
Nor does it apply to "refactor this one function," which is a request to do
the work, not to survey it.

## The two-pass rule

**Pass 1 reports. Pass 2 fixes. Nothing from Pass 2 happens until the user
says go.**

Hold this line even when a fix is obvious and one line long. The report is
the deliverable the user is actually buying: a finding they never saw is a
finding they never got to weigh, and a fix applied before review is a fix
they have to reverse-engineer from a diff. Their approval is also the
moment they decide which findings are real — you will be wrong about some
of them, and Pass 1 is where that gets caught cheaply.

## Step 0 — Orient before looking for anything

Four questions, answered out loud to the user in a few lines:

1. **What is the stack?** Language, framework, package manager (read the
   lockfile, not just the manifest — it tells you which manager is real).
2. **How much are we auditing?** The whole repo, one directory, or the
   recent diff. On anything large, agree a boundary before you start —
   an unbounded sweep either sprawls or silently samples, and a silent
   sample reads like a clean bill of health.
3. **Do tests exist, and do they pass?** Run them. This determines what you
   are allowed to claim later.
4. **Is the working tree clean?** `git status --porcelain`. If it is dirty,
   say so and ask the user to commit or stash before Pass 2 — their ability
   to `git reset` is the entire safety net under the fixing pass.

If there are no tests, say so plainly and carry the consequence through the
whole audit: **do not describe any change as "safe" or "functionally
equivalent."** Without tests, "it still builds" proves the code parses and
the imports resolve — nothing about behavior. Instead, name the two or
three riskiest changes and say where a single quick test would buy back
most of the confidence before touching them.

## Pass 1 — Find and report

Work through the seven sections below, in this order, and report each as a
small table. For every finding give: **what it is**, **where** (file +
line, as a clickable path), **why it matters**, and **the fix you'd
apply**.

Report each finding once, in the earliest section it fits. A duplicated
validator belongs to sections 2, 4, and 5 at the same time; listing it
three times is padding wearing a table.

Prioritize by consequence, not by how easy it is to spot:

| Priority | Means |
| --- | --- |
| **Critical** | A live credential, or a hole someone can exploit now. The one class that still outranks everything else. |
| **High** | One rule implemented in several places that will drift, or a collapse that already forces the same logic to be rewritten elsewhere — a bug that has not happened yet. Also a real vulnerability. |
| **Medium** | Costs maintenance time on every change, or hides bugs — the koshary itself. |
| **Low** | Tidiness. Worth doing while you are already in the file. |

A finding earns its place only if you can name the consequence. "This
function is long" is not a finding; "this 400-line handler mixes auth,
validation, and the DB write, so the auth check at line 210 is easy to miss
when editing" is. If you cannot finish the sentence "which means…", drop
it — a padded report trains the user to skim the whole thing.

Read `references/structural-decay.md` before sections 1–5. It carries the
tests that separate duplication that costs money from duplication that is
coincidence, and the tells for a layer that has collapsed.

### 1. Layer collapse — the koshary proper

The thing the skill is named for. Look for a single file or function doing
more than one of: transport (parsing the request, status codes), business
rules (what is allowed, what gets computed), persistence (queries, writes,
cache), presentation (rendering, formatting).

The tells: ORM calls inside a React component or route handler; a request
object reaching a function that is supposed to be a pure rule, so it can no
longer be called from a job or a test; business rules in the UI, so the API
accepts what the UI forbids; a `utils` module everything imports that
imports everything back.

Report by consequence: *"the price rule lives in the checkout component, so
the mobile client and the admin panel each reimplement it"* lands.
*"This violates separation of concerns"* does not.

### 2. Duplicated logic

The test is not "these look similar." It is: **if this rule changed, how
many places would have to change together, and would someone miss one?**
Three copies of a validation regex is a bug generator. Two functions that
both happen to loop over an array is nothing.

Quantify it — *"this regex appears in 4 files; changing the rule means
editing all 4"* — and see the reference for the coincidental-versus-coupled
distinction, which is the call models get wrong most often.

### 3. Functions and files that stopped being read

Length is a symptom, not the finding. What to look for: more than one
reason to change; nesting past three levels; boolean parameters that switch
behavior; a comment marking the boundary of a function that wants to exist.

The reference has the size-and-churn commands. Report the intersection
first — a big file that changes constantly is where the pain is, and a big
file nobody has touched in two years usually is not worth the risk.

### 4. Dead code and obvious refactors

Unused imports and locals, unreachable code, names that mislead. Verify
before deleting: string-keyed lookups, reflection, DI containers, route
manifests, and a library's public exports all make code look unused when it
is not. Only the obvious wins — if a finding requires a design discussion,
it belongs in section 6 as a flag, not here as a fix.

### 5. Reusable pieces — only if obvious

UI or logic repeated often enough that pulling it into one component, hook,
or function clearly pays for itself. If you have to argue for it, skip it.
A premature abstraction is its own kind of koshary: it couples callers that
had no reason to move together.

### 6. Quick health checks

Missing error handling around network and I/O calls. Obvious performance
traps — N+1 queries, unpaginated list endpoints, work inside a loop that
belongs outside it. Then anything else genuinely risky you happened to
notice, kept to a line each.

### 7. Security and dependencies

Last, and deliberately so — but a live credential is still Critical, and
Pass 2 fixes it before anything else. Report the two halves separately;
they are different decisions.

**Security.** Read `references/security-checks.md` first. It carries the
grep patterns worth running, the false positives that make a naive secret
scan useless, and what to check per stack. Cover: hardcoded secrets in code
or committed config; injection paths where user input reaches an
interpreter unescaped; missing or bypassable auth; sensitive data in logs,
`localStorage`, or URLs; unsafe execution and wide-open CORS. Check git
history as well as the working tree — a key deleted in the last commit is
still a live key.

**Dependencies.** Run the bundled script, which detects the package manager
from the lockfile and runs both the outdated report and the vulnerability
scan:

```bash
bash scripts/dep_audit.sh [project-dir]
```

The path is relative to this skill's own directory — the one you loaded
`SKILL.md` from, not the project being audited. The project directory is
the optional argument and defaults to the current one, so run it from
anywhere. If it does not recognize the stack it exits 2, says what it
looked for, and changes nothing — fall back to that ecosystem's own
outdated and audit commands, and say in the report that you did.

Triage the vulnerability output before reporting it. A scanner counts
advisories, not exposure: separate what ships to production from what only
runs in the build or test chain, and say which. A CVE in a runtime
dependency is a finding with a deadline; twelve advisories deep in a build
toolchain usually are not, and reporting them as equals is how the real one
gets ignored. Being three minor versions behind is not a security finding
at all.

### Closing Pass 1

End with a short summary — counts by priority — and ask the user which
sections they want fixed. Do not proceed on silence or on a vague "looks
good."

## Pass 2 — Fix, after approval

Fix in this order, and stop after each group to confirm the project still
builds and runs (and that tests still pass, if there are any). Commit each
group separately, so a bad fix can be dropped without losing the good ones.
**If a group breaks the build or the tests, revert that group, report what
broke, and stop** — do not debug your way forward through the rest of the
list with the tree in an unknown state.

1. **Anything Critical.** A live credential or an exploitable hole goes
   first regardless of where it sat in the report. These change behavior
   deliberately — that is the point — so state exactly what now behaves
   differently, in the terms the user cares about: which requests start
   failing, which users get logged out, what has to be rotated.
2. **Structural cleanups.** Layer collapse, duplication, dead code,
   extractions — the koshary itself, and the reason the user is here. Only
   the ones they approved. These must **not** change behavior. Show
   before/after for each, and prefer several small commits to one large
   one; a collapsed layer is usually pulled apart in steps.
3. **Dependencies.** Bump patch and minor freely; update the lockfile;
   build and test after. Do **not** apply major-version upgrades — list
   each one separately with a one-line migration note and let the user
   decide.
4. **Remaining security fixes.** The High and Medium ones, same rule as
   step 1: say what behavior changes for each.

Then give a closing summary: what was cleaned up, what security issues were
fixed, packages updated (old → new), and what still needs the user's
decision.

## Rules

- Prefer the smallest change that resolves the finding.
- Don't touch business logic without asking — you can see what the code
  does, not what it is supposed to do.
- If a fix needs a rewrite or a breaking upgrade, flag it with a
  recommendation and stop there.
- Don't add abstractions, config, or tooling the user didn't ask for. The
  goal is a codebase that is easier to change, not one that is more
  impressive.

## What NOT to do

- Don't fix anything during Pass 1, however trivial.
- Don't let this become a security audit. Security is section 7 because the
  user asked about the shape of their code; a page of dependency advisories
  in front of the finding they actually needed is a worse report, not a
  more thorough one.
- Don't pad the report to look thorough — findings without a consequence
  are noise, and they cost the real findings their attention.
- Don't report the same finding in three sections because it fits all of
  them.
- Don't call a change "safe" or "functionally equivalent" in a repo with no
  tests. Say what you actually verified.
- Don't rewrite working code because it offends you stylistically.
- Don't merge duplication that is only coincidental — that is how you
  create the next koshary.
- Don't apply a major-version dependency upgrade on your own initiative.
- Don't report a secret's value back in the summary — reference the file
  and line, and tell the user to rotate it.

---

## Non-Claude-Code version (plain prompt)

For tools without skill discovery, paste this once, in a committed repo:

> Act as a senior engineer reviewing a codebase that has become hard to
> change. Audit it in two passes and change nothing until I approve.
>
> First tell me the stack (language, framework, package manager), how much
> of the repo we're covering, and whether tests exist. If there are none,
> don't call any change "safe" — tell me the riskiest ones and where a
> quick test would help.
>
> **Pass 1 — report only.** A prioritized table per section, each finding
> given once, with what it is, file and line, why it matters, and your
> suggested fix: (1) layer collapse — business rules, queries, transport or
> rendering stirred into one file or function; (2) duplicated logic, but
> only where one rule changing would force edits in several places at once;
> (3) functions and files nobody reads — more than one reason to change,
> deep nesting, boolean mode flags — prioritized by which ones churn;
> (4) dead code and obvious refactors — unused imports, unreachable code,
> misleading names, verified against reflection and dynamic lookups;
> (5) reusable pieces, only if obvious; (6) missing error handling around
> network/IO and obvious performance traps like N+1 queries or unpaginated
> lists; (7) last, security and dependencies — hardcoded secrets (check git
> history too), injection, missing auth, sensitive data in
> logs/localStorage/URLs, `eval`/`dangerouslySetInnerHTML`/open CORS, plus
> outdated packages and the vulnerability scan for my package manager, with
> runtime and build-only advisories separated.
>
> Skip anything you can't name a consequence for.
>
> **Pass 2 — after I confirm.** Fix anything critical first — a live
> credential or an exploitable hole — saying what behavior changes. Then
> the structural cleanups I approved, which must not change behavior. Then
> dependencies (patch/minor only — list major upgrades separately with a
> migration note). Then the remaining security fixes. Confirm the app still
> builds and runs after each group, and commit each separately; if a group
> breaks something, revert it and stop. Prefer the smallest change that
> works; don't touch business logic without asking; flag anything needing a
> rewrite instead of doing it.
