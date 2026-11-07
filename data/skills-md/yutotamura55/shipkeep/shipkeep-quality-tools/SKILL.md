---
name: shipkeep-quality-tools
description: Use when a project should get, or be checked for, the tools that keep code quality up — formatter, linter, type checker, security lint, tests with coverage, unused-code detection, dependency audit, and CI that runs them — in any language. Finds what is missing, proposes tools, and installs the ones the user approves on a dedicated branch.
---

# Propose and install quality tools

This skill finds which quality tools a project lacks, proposes tools to fill
the gaps, and installs the ones the user chooses. It works for any language:
Python and JavaScript/TypeScript have ready references, and for other
languages you research the tools.

The project keeps writing its own tests. This skill sets up the tools that run
and measure them.

Steps 1–4 only read the repository. From step 5 on, the skill changes the
repository: follow `references/change-principles.md` from that point.

## Steps

1. **Take the inventory.** Run the script with Python 3.10 or newer and Git:

   ```bash
   python3 <this skill's directory>/scripts/inventory.py <repository>
   ```

   It prints one JSON document: the languages it found (`languages`), and one
   row per aspect (`aspects`) with `status`, the tools it found, and the files
   that show them (`evidence`). With `--format result` it prints the same
   facts in the common shipkeep result format (`references/result.schema.json`)
   for filing or keeping; the default shape is for reading. It reads tracked
   files only. Exit code 2 means
   the path is not in a Git repository, Git failed, or an argument is invalid
   (for example an unknown `--language` id; `--help` lists them). Read the
   message, fix the call if it was the arguments, otherwise report and stop.

   | Status | Meaning |
   | --- | --- |
   | `pass` | A tool for this aspect appears in the project |
   | `fail` | No tool for this aspect was found |
   | `unknown` | The script cannot tell (a language without a reference, or a repository setting such as CodeQL default setup) |
   | `not_applicable` | The aspect does not apply, with a `note`. `custom_rules` and `baseline` are reported this way when the files are absent: they are proposed only when a recurring type of problem or an existing backlog of findings calls for them |

   Each language has `detected_by`: `manifest` (a project file such as
   `pyproject.toml`), `sources` (only source files), or `declared` (passed
   with `--language`). A language found only by sources may be a few helper
   scripts: ask the user whether it needs tools before proposing any. When
   `languages` is empty or lacks a language the project will use (a new
   repository, or a part not written yet), ask the user which languages to
   plan for and run the script again with `--language <id>` for each, so that
   their aspects appear as rows; `--help` lists the ids.
   `unrecognized_source_extensions` lists source file extensions of languages
   the script does not know; decide the language from them and research its
   tools as for a language without a reference.

2. **Confirm the evidence.** The script matches names; it does not prove that a
   tool is configured or runs. Open the evidence files and check:
   - that each `pass` tool is really configured (for example, Ruff present but
     only formatting);
   - whether the check command runs every tool, and whether CI runs the check
     command;
   - how strict the current settings are (for example TypeScript `strict`,
     mypy `strict`).
   Correct a row when the files show the script was wrong, and say so.
3. **Choose tools.** For each missing aspect, pick a tool:
   - Common to every project: `references/common.md`.
   - Python: `references/python.md`. JavaScript/TypeScript:
     `references/javascript.md`.
   - Other languages (`"reference": false`): research as
     `references/other-languages.md` describes, and cite your sources.
   Keep every tool the project already has; never replace one without the
   user asking. A language may make an aspect not applicable (for example type
   checking for a compiled language); say why.
4. **Propose.** Show the user, in their language:
   - a table with one row per aspect: current state, proposed tool, why, and the
     files that would change;
   - the conditional methods from `references/common.md` that fit this project,
     each with its condition;
   - when the inspection, a review, or the user names a recurring type of
     problem, a project-specific rule for it (`references/common.md`, "Turning
     a found type of problem into a rule"), and when a new rule would fail on
     existing code, a baseline ("Baselines for existing projects");
   - for an existing project, the rollout stages (`references/common.md`,
     "Rolling out to an existing project"), and which stage this change covers;
   - the repository settings the user must change themselves, from
     `references/common.md`, "GitHub settings the user changes".
   Let the user choose. Change nothing until they approve.
5. **Prepare the change** as `references/change-principles.md` says: check the
   working tree, create a dedicated branch, and run the existing checks once to
   record the baseline.
6. **Install** only what the user chose:
   - Use the version that is current when you install, from the package
     registry or the official documentation. Pin it the way the project pins
     its other dependencies.
   - Configure each tool in the project's existing configuration files where
     possible.
   - Add the tools to the one check command, creating it if missing, and
     document it.
   - Add or update CI as `references/common.md` says: the same check command,
     actions pinned to SHAs you looked up, `persist-credentials: false`, and
     minimal `permissions`.
   - Set the coverage floor to the coverage you measure now, not to a guess.
     Write the measured value truncated, not rounded, and set the report
     precision so that the comparison sees those digits
     (`references/common.md`, "Coverage").
   - Audit the dependencies of the check tools too, not only the project's,
     when they are installed as packages (`references/common.md`,
     "Dependencies").
7. **Verify.** Run the check command and, if you changed workflows, actionlint
   and zizmor on them. Record the findings each new tool reports on the
   existing code and the measured coverage. Fix findings only if the approved
   plan includes it; otherwise use the staged rollout and report them.
8. **Hand over and report** as `references/change-principles.md` says. In the
   report, list:
   - the tools installed and their versions;
   - the check results compared with the baseline;
   - the settings the user must change;
   - the remaining rollout stages, proposed as Issues for the user to create.

## Limits

State these limits in the report when they matter:

- The inventory matches tool names in tracked configuration files. It does not
  read rule settings beyond a few patterns (such as Ruff's `S` rules) or check
  that CI actually runs a tool; step 2 covers that.
- It skips vendored directories (`node_modules/`, `vendor/`, `.venv/` and
  similar) and does not follow symbolic links.
- It looks at the repository as a whole. In a monorepo with several packages,
  check each package.
- Configuration shared by several languages (`Makefile`, workflows) counts for
  every language in the repository.
