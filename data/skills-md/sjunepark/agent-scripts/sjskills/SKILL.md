---
name: sjskills
description: "Operate sjskills to configure project profiles and direct skills, inspect or sync project manifests and the fixed global baseline, or restore named quarantines. Explicit invocation only."
---

# sjskills

Use `sjskills` to reconcile the exact skill state selected by a project's
committed `sjskills.toml` or by the tool's fixed global baseline. The tool owns
verified placement, provenance, quarantine, and restore; it does not publish
source changes or perform ad hoc catalog installs.

Strict sync covers only the selected global or project `.agents/skills` and
`.claude/skills` roots. Undeclared directories move into recoverable quarantine,
including unknown and locally modified copies. Built-in skills, plugin caches,
and legacy Pi copies are outside this boundary.

Keep four states distinct:

1. A source repository's local catalog is editable but not yet published.
2. The registry identifies the published remote content reconciliation can
   consume.
3. A project's committed `sjskills.toml` selects project profiles and direct
   declarations.
4. The registry defines one fixed, machine-independent global baseline.

Prefer `sjskills` on `PATH`. In the tool's source repository, use
`bin/sjskills` when the command is not installed. Do not install the command or
change `PATH` unless the user asks.

Use `sjskills` or `sjskills status` for CLI version and two-scope skill status.
The CLI comparison uses the latest stable published sjskills release, names
unavailable or absent release evidence, and links to updates without installing
them. Version equality does not establish checkout freshness. The report names the
resolved project root, offers setup guidance for a missing manifest, and reports
configuration failures without recommending replacement. It never initializes
or synchronizes. Status exits 0 even when inspection is unavailable; inspect the
findings and freshness rather than treating success as exact state. Cold checks
may take 30 seconds plus cleanup. Stale evidence remains explicitly labeled.

Explicit reports use stdout; other successful commands retain incidental stderr
notices; fresh skill scopes without findings and CLI comparisons without updates
or problems remain silent.
`--json` keeps full skill findings in `advisories` and version evidence in
`cliAdvisory`; status also includes setup metadata under `status`. None grants
apply authority or substitutes for a reviewed plan. Use the same compatible
executable for plan and apply; older loaders may reject the new advisory field.
Use `--no-status-check` to skip discovery, inspection, fetching, and cache writes;
status then reports checks disabled, while other commands retain their primary
verification.

## Classify the request

- **Sync configured state:** An unqualified request to sync or reconcile with
  this skill authorizes both the fixed global baseline and the current project's
  committed `sjskills.toml`, when present. Honor an explicit project-only,
  global-only, machine, or preservation limit. If no project manifest exists,
  reconcile only the global baseline and report that the project is unconfigured;
  do not initialize it or infer profiles from installed copies.
- **Explain or inspect:** Use `status` for both scopes, `profiles` for available
  selections, or `plan` / `plan --global` for a full selected-scope review. These
  preserve managed roots but may fetch expected content temporarily. A bare
  invocation without an action defaults to status inspection.
- **Configure a project:** Create or edit `sjskills.toml` when the user asks to
  adopt managed project skills or change the selection. Use selected profiles,
  direct declarations, or both as described below. Preserve unrelated entries;
  configuration alone does not authorize apply or global changes.
- **Reconcile a project:** Review `plan`, run `apply` only when the user asked
  to install, bootstrap, reconcile, or sync the project, then run `plan` again.
- **Recover project state:** Restore only the exact quarantine identifier the
  user named, and only after confirming every modeled destination is absent.
- **Global reconciliation or restore:** Read
  [references/global-rollout.md](references/global-rollout.md) before global
  mutation. A sync request supplies reconciliation authority; prepare and review
  the required evidence yourself instead of asking the user to approve hashes.
  Restore still requires a request identifying the quarantine.

Use the ordinary Skills CLI workflow to discover source skill names or perform
requested ad hoc installs. For a project managed by `sjskills`, record external
skills in `[[direct]]` and reconcile through `sjskills`; undeclared ad hoc
installs in managed roots become quarantine candidates. Use the repository's
plugin workflow for Codex plugins. Local catalog validation and publication are
not reconciliation.

## Project selections

Profiles are named collections defined centrally in `agent-scripts`'s
`skill-registry.json`; `sjskills profiles` lists them. A project selects those
names, but cannot define new profiles in its manifest. It can independently add
skills from other repositories with `[[direct]]`, without changing the central
registry or publishing those skills in `agent-scripts`.

For example, using a placeholder source and skill name:

```toml
version = 1
profiles = ["dev"]

[[direct]]
name = "team-review"
source = "your-org/team-skills"
```

Use the source's actual skill name, not an alias. Repeat `[[direct]]` for more
skills, sorting entries by name and profile names alphabetically. Direct names
must be unique and cannot overlap selected profiles or the fixed global
baseline. Sources accept Git shorthand (`owner/repo[/path]`) or credential-free
HTTPS; local paths, embedded credentials, URL queries, npm specifiers, and other
schemes are unsupported. Set optional `full_depth = true` only when deeper
source discovery is needed. Direct skills use copy mode and the registry's
default targets, currently project `.agents/skills` and `.claude/skills`;
per-entry manager, mode, target, and workflow fields are unsupported.

For a direct-only project, omit `profiles` or use `profiles = []`, and include
at least one `[[direct]]` entry. Create that manifest directly when adoption is
requested: `sjskills init` requires a profile and cannot initialize this case.
For an existing manifest, edit the requested selection in place rather than
rerunning `init`. Keep the manifest as committed project configuration; commit
only when authorized. Review `sjskills plan` after configuration, and apply
only when installation or synchronization was requested.

## Use configured authority

The request grants authority; the committed manifest and fixed baseline define
the desired set. Proceed with verified installs, updates, provenance migration,
and recoverable quarantine of undeclared copies within that set's managed roots.
Summarize the reviewed operations before applying, without requiring another
user turn. Use `--yes` for an already-authorized apply unless the user requests
an interactive checkpoint. A flag or plan artifact does not create authority.

"Override and sync" can override a redundant approval step; it does not resolve
unmanaged or modified desired copies, corrupt provenance, unsafe boundaries, or
failed materialization. Stop the affected scope on those conflicts and explain
the concrete resolution needed. Do not force-adopt, manually replace roots,
change profiles, or include another machine to make a plan pass. Complete an
independent unblocked scope unless the user required an all-or-nothing result.

## Project workflow

1. Resolve the command and project root. If no `sjskills.toml` exists, stop
   unless the user requested adoption or initialization.
2. For a new manifest with profiles, run `sjskills profiles`, use the user's
   selected profiles, and run `sjskills init <profile> ...`; then add requested
   direct declarations. For direct-only adoption or an existing manifest, use
   the configuration procedure above. Do not infer profiles from installed
   copies or overwrite an existing manifest with `init`.
3. Read the manifest and run `sjskills plan`. Summarize installs, updates,
   quarantines, unchanged placements, manual or workflow-managed entries,
   warnings, and blocks.
   Distinguish desired-state drift or conflict from a failed command, network
   request, or materialization; an operational failure is not a valid plan.
4. Stop before apply when the plan reports an unmanaged or locally modified
   desired copy, malformed or untrusted provenance, an unsafe filesystem
   boundary, an unverifiable extra, failed materialization, or another conflict.
5. For authorized project reconciliation, run `sjskills apply --yes` after the
   plan passes review. Honor any explicit request to stop at a preview or keep
   interactive confirmation.
6. Run `sjskills plan` again. Do not claim exact state while changes or blocks
   remain. Retain every reported quarantine identifier through a normal work
   cycle.

When intended content changed in a registry-backed source, reconciliation can
only consume the published remote content. Do not apply a local-only change.
If publication is requested, follow the source repository's instructions for
validation, review, commit, and publication; those mechanics are outside this
skill. Before reconciling, resolve the registry source and verify that its
pinned remote ref contains each intended skill tree. A local or feature-branch
commit is insufficient when the registry points elsewhere.

## Restore

Treat restore as a separate mutation. Require the user to name the quarantine
identifier, inspect its current state, and confirm that all destinations are
absent. Run:

```text
sjskills restore <quarantine-id>
```

Do not move, delete, or overwrite active destinations to make restore succeed.
If content or provenance changed, preserve both sides and report the conflict.
Restore does not grant ownership to unknown or locally modified copies. Run
`sjskills plan` afterward; a restored undeclared skill is again removal drift.

## Global boundary

Global reconciliation uses the fixed, machine-independent baseline. Profiles
select project skills; do not invent a global profile, infer one from the
hostname, or synthesize Pi-specific copies. An inspection request runs only
`sjskills plan --global`; configured sync continues through verified apply.

The `--approved-plan` and `--approved-plan-sha256` flags bind global apply to
the agent-reviewed evidence. Their names do not require a separate human
approval ceremony: create the artifact, inspect every operation and warning,
compute its digest, and use the same verified executable through apply and the
final plan. A sync request covers this work; an audit, repository validation,
or unrelated setup request does not. Restore and conflict resolution remain
separate from making the configured desired set exact.

## Completion

Report:

- project or fixed-global scope and whether work was read-only or mutating;
- the selected profiles or direct manifest declarations when relevant;
- plan and final-plan results, including remaining extras, blocks, and
  out-of-scope legacy state;
- published-ref evidence when remote-backed local changes were involved;
- every quarantine identifier retained or restored; and
- any mutation still awaiting explicit authority.
