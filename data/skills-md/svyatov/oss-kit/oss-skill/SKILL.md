---
name: oss-skill
description: "Fix the structure, portability, and effectiveness of repositories that ship Agent Skills. Covers canonical layout, SKILL.md conformance, trigger descriptions, progressive disclosure, repeatable procedures, bundled scripts, evaluation, licensing, and host install paths. Use when a skill fails to load or trigger, produces inconsistent results, wastes context or tool calls, ships non-portable code, or needs an audit against the current Agent Skills specification and authoring guidance."
license: MIT
compatibility: Requires Node 22+ or Bun to run the bundled validator
---

# Build reliable Agent Skills

Fix the mechanics that decide whether a skill loads, then verify that it improves the task it claims to handle. Format conformance cannot prove output quality, and model behavior is nondeterministic, so never infer reliable behavior from a validator exit code alone.

Most of what this skill fixes is mechanical, and the validator this skill ships at `scripts/validate.mjs` in its own directory names the fault precisely (R-SKL-02). It reads files, needs nothing installed, and runs on Node or Bun: `node /path/to/oss-skill/scripts/validate.mjs /path/to/repository`. Both paths are absolute on purpose, because the script lives in this skill's installed directory and not in the repository under audit, where a bare `scripts/validate.mjs` would resolve and fail; [references/hosts.md](references/hosts.md) names where each host installs a skill. Run it before reading further into any repository; its output tells you which of the rules below is in play.

## Scope

The SKL rules belong here: R-SKL-01 layout, R-SKL-02 specification conformance, R-SKL-03 body size, R-SKL-04 licensing, R-SKL-05 portable scripts, R-SKL-06 install paths, and R-SKL-07 focused procedures with progressive disclosure.

When `oss-audit-report.md` exists at the repository root, read the group addressed to this skill and work from that. Each failing rule there carries the audit's evidence and that rule's `Check:` text verbatim, so reading `STANDARD.md` as well adds nothing. Where the file is absent, work from the request as usual.

Neighbouring work belongs elsewhere. Wiring the validator into CI is R-CI-02, owned by `oss-ci`, because the rule already requires CI to run the same linter the contributing guide gives to humans, and for a skills repository that linter is the validator. Keeping every host manifest on one version is R-CHG-03, owned by `oss-changelog`. The README's install command and runnable example are R-DOC-02, and its links to the license, changelog, and contributing guide are R-DOC-03, both owned by `oss-readme`. The sentences inside any file are R-DOC-05, owned by `oss-writing`. Note what a repository needs and hand it to the owning skill rather than doing that work from here.

Use `oss-writing` for sentence-level prose and `oss-readme` for repository documentation. This skill owns whether the skill itself has a focused trigger, an efficient procedure, conditional references, and a verification loop.

## Step 1: Find every skill in the repository

Locate every `SKILL.md` in the repository. Resolve symlinked directories to their target first: a repository may commit `.claude/skills` and `.agents/skills` as symlinks pointing at one real `skills/` directory, and a search that follows them reports every skill two or three times.

Sort what you find into three cases. A `SKILL.md` that is a direct child of a top-level `skills/<name>/` satisfies R-SKL-01. A `SKILL.md` reached only through a symlink to that directory is the same file and not a finding. A `SKILL.md` anywhere else is a real finding.

Fix a real finding by moving the whole skill directory under `skills/`, keeping its `references/` and `assets/` subdirectories with it, and by pointing every host manifest that names a skills path at `skills/`. Read [references/hosts.md](references/hosts.md) for which manifest each host reads. Moving the directory without updating the manifests trades one loading failure for another.

Where a repository ships skills only as a plugin and keeps them under a nested plugin directory, say so plainly rather than moving them: that layout loads in the plugin host and fails the `skills` CLI installer, and choosing between them is the maintainer's call, not yours.

## Step 2: Validate against the specification (R-SKL-02)

Run the bundled validator over the repository and fix what it names:

```bash
node /path/to/oss-skill/scripts/validate.mjs /path/to/repository
```

It needs Node 22 or later, or Bun, and nothing installed. It reads files: it writes nothing, spawns nothing, and makes no network call. It reports an error for every violation of R-SKL-01 through R-SKL-05, and exits 1 if any error was found. It warns in two cases, and a warning never moves the exit code. The first is a frontmatter construct it does not read, which says nothing about whether the construct is valid. The second is a value that breaks a constraint a host enforces and the specification does not; that warning names the constraint and the host, and says the specification permits the value. Read which kind you have before acting: the first asks you to check the construct with a YAML parser, and the second asks you to change a file that already conforms.

The faults come in a small set.

A name and directory mismatch means the frontmatter `name` and the directory name differ. The specification requires them to match exactly. Decide which one is correct by looking at what already references the skill: a name in the README table, in a plugin manifest, or in another skill's prose is a name people already use. Rename the other one.

An invalid name means the value breaks the character rules: 1 to 64 characters, lowercase letters, digits, and hyphens only, no leading or trailing hyphen, no consecutive hyphens. Rewrite it and rename the directory to match.

An over-long description means the field exceeds 1024 characters. Cut the parts a reader already knows, keeping both halves the field must carry: what the skill does, and when to use it. Cutting the when half to fit the limit produces a skill that validates and never triggers.

A missing required field means `name` or `description` is absent or empty. Both are required and neither has a default.

A reserved word or an XML tag is the host-constraint warning. Anthropic's platform rejects a `name` containing "anthropic" or "claude", and rejects an XML tag in `name` or `description`; the specification imposes neither, which is why these carry no rule ID and leave the exit code alone. Rename the skill and its directory together, or write the description in plain text. A skill that ships as it stands conforms to the specification and is refused on upload, so the warning is the only notice you get.

Frontmatter that fails to parse needs a YAML fix, not a guessed rewrite. Quote single-line descriptions as the repository convention. If the bundled validator warns that it cannot read a valid YAML construct such as a block scalar, check that construct with a strict YAML parser before changing it.

## Step 3: Bring an oversized body under the ceiling (R-SKL-03)

Count the lines of each `SKILL.md`. Where one exceeds 500, the fix is to move material into that skill's own `references/` directory, not to compress the prose until it fits.

Decide what moves by asking what the reader needs on every run against what they need only sometimes. The procedure, the decisions, and the facts that defy assumption stay in `SKILL.md`. Long tables, per-platform detail, worked examples, and anything consulted only in one branch of the work move out.

Name each reference file from `SKILL.md` at the point the reader would need it, and say what makes it worth opening. A pointer at the top of the file listing every reference at once loads nothing usefully, because the reader has no way to tell which one this task needs.

Name each file for what it contains, such as `form-validation-rules.md` rather than `doc2.md`, and group a set of them into directories by domain. The filename is what a reader chooses from, so a name that describes nothing costs a read to find out.

Open every reference file over 100 lines with a table of contents listing every section it has. A reader who takes the first 100 lines of a 300-line file otherwise sees no sign that two thirds of it exists.

Keep references one level deep. A file reached through another referenced file is partially read rather than read, so nesting yields incomplete information rather than merely slow information.

## Step 4: Declare the license in every skill (R-SKL-04)

Add a `license:` line to every `SKILL.md`, naming the license that applies to that skill. Use the repository license when it covers every skill. If one skill has different terms, bundle its license file inside that skill and reference the file from frontmatter. Where the evidence conflicts, stop and ask which terms apply.

The Agent Skills specification makes `license` optional and accepts either a name or a bundled file reference. R-SKL-04 deliberately requires it because an installer may extract one skill directory without the repository license.

## Step 5: Keep a shipped script runnable (R-SKL-05)

Where a skill ships a `scripts/` directory, check what its files assume. A script runs on the reader's machine, so an interpreter they lack or a dependency they cannot install fails the task the skill was invoked for.

A script file needs a shebang naming portable `sh` or `node`; documentation and data files under `scripts/`, such as a README or fixture, need no shebang. Ship JavaScript, not TypeScript, because Node 22 does not provide the type-stripping behavior this repository would need. JavaScript may import real Node built-ins or sibling files by relative path, but no package. No dependency manifest, lockfile, `node_modules`, runtime-specific module, or `Bun` or `Deno` global travels with the skill.

The specification permits Python, Bash, TypeScript, dependencies, and other host-supported choices. R-SKL-05 is deliberately stricter so one shipped script runs unchanged under the repository's Node 22 floor or a POSIX shell. Where a skill needs another runtime, report the conflict and let the maintainer choose rather than silently rewriting working code.

Fix a violation by rewriting the script against Node built-ins, or by moving the work into the skill's prose where an agent performs it directly.

Where the work is writing a script rather than judging one, read [references/scripts.md](references/scripts.md) first. It covers what R-SKL-05 does not reach: handling a failure instead of deferring it, giving every constant its reason, error messages that name what was expected, stating whether a pointer means run or read, and naming the runtime floor and every external command in place of the package list a shipped script cannot have.

## Step 6: Make the procedure earn its context (R-SKL-07)

Start from real task evidence: upstream documentation, project artifacts, recurring corrections, and failure cases. Remove generic knowledge the agent already has. Keep one coherent unit of work whose output and boundary can be stated precisely.

Write the description for activation. State what outcome the skill produces and when to use it, using the language a user is likely to use. Include adjacent cases only when the skill truly handles them. Test near-miss prompts too, because a description that triggers on unrelated work wastes the whole body load.

Write the description in the third person throughout. "I can help you write a README" and "You can use this to write a README" are the two openers that go wrong, and both spend the field's opening words on the reader rather than on the trigger terms a selector matches.

Name the skill for what it does, preferring a gerund or a noun phrase, and keep one naming shape across a collection so the set reads as one product. Avoid `helper`, `utils`, `documents`, and `data`, which name nothing a user would search for.

Write nothing time-sensitive into a skill. A version number, a release date, or a phrase such as "currently" expires without telling anybody, and a reader copying it has no way to know. Name the documentation to re-read instead. A dated verification record is a different thing and is fine: `references/hosts.md` stamps each claim with when it was checked, which tells a reader how old the evidence is rather than instructing them from it.

Inside the body:

1. Give a default path, not a menu of equal choices.
2. Match control to risk. Prescribe fragile sequences; explain intent where several correct approaches exist.
3. Keep non-obvious gotchas before the point where they cause failure.
4. Name capabilities and observable evidence, not a host's tool names.
5. Load a direct reference only at the branch that needs it. Do not chain references.
6. Bundle a tested script only when repeated runs otherwise recreate the same deterministic logic.
7. End state-changing work with validation, correction, and re-validation.

Evaluate behavior separately from format. A validator exit code says a skill loads, not that it helps. Where the work is to establish that a skill improves the task it claims, or to decide whether a change to one was worth making, read [references/evaluating.md](references/evaluating.md): it covers the task records, the two-session loop that keeps an author from grading their own instructions, and what the read order of the bundled files says about where the body points.

## Step 7: Check the install path behind every claimed host

Read the README and the install documentation it links to, and list every host named there. For each one, find the manifest that host reads, at the path that host reads it from, or the documented command that installs without a manifest. A host with neither is an R-SKL-06 finding: either ship the manifest or stop naming the host. Do not accept a manifest at a path no host reads as evidence.

## Renaming a skill breaks installs

A skill's name is its identity everywhere downstream: in an installer command, in a plugin manifest, in a user's local configuration, and in any other skill that names it. Renaming one to satisfy R-SKL-02 is correct and is also a breaking change for anyone who installed it.

Treat it as one. Say so when proposing the rename, and hand the changelog entry and the version decision to `oss-changelog` rather than deciding the bump here.

## Verify, then report what you changed

Re-run the validator after every fix, not once at the end, because one edit can introduce a fault another edit was meant to clear. Then read each SKL rule's `Check:` line in `STANDARD.md` against the repository as it now stands, fix what fails, and start the list again. Completion is gated on both: a clean validator exit and every cited rule passing.

List every skill you touched, the rule each change satisfies, and every fault the validator reported that you did not fix, with the reason. Name the rename separately from the mechanical fixes, since it is the only one with downstream cost.

## Upstream sources

Use the current [Agent Skills specification](https://agentskills.io/specification), [creator best practices](https://agentskills.io/skill-creation/best-practices), [evaluation guide](https://agentskills.io/skill-creation/evaluating-skills), [description optimization guide](https://agentskills.io/skill-creation/optimizing-descriptions), and [script guide](https://agentskills.io/skill-creation/using-scripts). Recheck them before changing a rule because the format and host implementations continue to evolve.
