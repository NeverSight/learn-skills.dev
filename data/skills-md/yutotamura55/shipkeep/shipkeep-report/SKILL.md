---
name: shipkeep-report
description: Use after an inspection (shipkeep-publish-check, shipkeep-quality-tools, shipkeep-refactor, or another tool's findings converted to the shipkeep result format) to turn the failed items into GitHub Issues the user approves, without duplicates, and to keep the inspection history and the items the user decided not to fix in the repository's .shipkeep/ directory. Also lists checks that keep failing, as candidates for a machine-checked rule.
---

# Turn inspection results into Issues and keep the record

This skill takes results in the common shipkeep result format
(`references/result.schema.json`) and:

- plans GitHub Issues for the failed items, at most a few per run, and skips
  items that are already filed, closed as not planned, or dismissed;
- creates exactly the Issues of a plan the user approved;
- keeps the history of results and the dismissed items in the target
  repository's `.shipkeep/` directory, reviewed like any other change;
- lists items that failed in several recorded runs, so that a recurring type of
  problem becomes a rule a tool checks.

All steps use `scripts/report.py` with Python 3.10 or newer. Reading and
creating Issues needs an authenticated `gh`. The script never prints a local
path, a secret, or personal data, and it refuses to file or record text that
looks like a personal email address or a home directory path.

Planning only reads GitHub. Creating Issues and writing `.shipkeep/` change
things: do them only after the user approves, and follow
`references/change-principles.md` for the changes to the repository.

## Steps

1. **Get results in the common format.** Run the inspection scripts with
   `--format result` and write each result to a file outside the target
   repository (inspection never changes it), for example:

   ```bash
   python3 <publish-check skill>/scripts/scan.py <repository> --format result > /tmp/scan.json
   ```

   For another tool's findings (for example vibe-code-launch-check or
   prod-readiness), write a result file by hand that follows
   `references/result.schema.json`: one item per finding, a stable `id` (the
   check, then `/` and what it is about), `status` `fail` for a problem,
   `severity` for a fail, `confidence` from how the tool found it, and evidence
   with locations only. Mask every secret and personal value. Then check it:

   ```bash
   python3 <this skill's directory>/scripts/report.py validate <result.json>...
   ```

   Exit code 1 means a file does not match; fix it from the messages.

2. **Plan the Issues.** This reads the repository's Issues and labels and
   writes the plan; it creates nothing:

   ```bash
   python3 <this skill's directory>/scripts/report.py plan <result.json>... \
     --repo OWNER/NAME --output /tmp/plan.json \
     [--dismissed <repository>/.shipkeep/dismissed.json] \
     [--limit 3] [--min-severity medium] [--include-unknown] [--label NAME ...]
   ```

   Defaults: at most 3 Issues per run, failed items of severity medium or
   higher (a fail without a severity counts as medium), labels `shipkeep` and
   `needs-triage`. `--include-unknown` also files checks that could not run.
   The plan lists, for each candidate, either the Issue to create or why it is
   skipped:

   | Reason | Meaning |
   | --- | --- |
   | `dismissed` | Listed in `.shipkeep/dismissed.json` |
   | `already_open` | An open Issue for the same item exists |
   | `closed_as_not_planned`, `closed_as_duplicate`, `closed_without_reason` | The Issue was closed for a reason other than completed; for not planned, suggest recording it with `dismiss` |
   | `blocked_personal_data` | The item's text looks like personal data; the item is shown by its position (`result N item M`), not its id. Mask it in the result and plan again |
   | `over_limit` | More candidates than `--limit`; they are filed in a later run |

   An item whose earlier Issue was closed as completed but still fails is filed
   again, with a link to the earlier Issue. Duplicates are found by a marker on
   the first line of the Issue body, counted only in Issues opened by the
   repository's owner, members, or collaborators, so that a stranger cannot hide
   an item by opening an Issue with a marker. Removing the label does not cause
   a duplicate. The command ends with `plan sha256: <digest>` of the plan file.

3. **Let the user approve.** Show the user the titles to create, the labels to
   create, the skipped items with their reasons, and the plan digest. Show a
   body when the user asks: bodies hold only masked evidence. The user may ask
   for a lower limit or other options: plan again. Create nothing until the
   user approves this plan and its digest.

4. **Create the Issues** of the approved plan, passing the digest the user
   approved:

   ```bash
   python3 <this skill's directory>/scripts/report.py create /tmp/plan.json --repo OWNER/NAME --sha256 <digest>
   ```

   It reads the plan file once and stops when it no longer has that digest.
   It does not post the bodies written in the file: it builds each body again
   from the item stored in the plan, with the same code as `plan`, so that
   every string from a result stays in a code span and cannot mention anyone or
   reference another repository. It stops when an entry's stored body or title
   differs from the rebuilt one, or when a label looks like personal data. It
   creates the missing labels, and stops before any Issue if a label cannot be
   created. Then it creates each Issue, after checking again that no Issue for
   the same item appeared since the plan. Exit code 1 means some creation
   failed; report which entries. Report the created Issue numbers.

5. **Keep the record**, when the user wants it, on a dedicated branch of the
   target repository as `references/change-principles.md` says:

   ```bash
   python3 <this skill's directory>/scripts/report.py record <result.json> --into <repository>/.shipkeep/history
   python3 <this skill's directory>/scripts/report.py dismiss --file <repository>/.shipkeep/dismissed.json \
     --tool TOOL --id ITEM_ID --reason "why it will not be fixed" [--issue N]
   ```

   Record the results of each inspection; recording the same result twice is
   refused. Dismiss an item only when the user decided not to fix it, with
   their reason. Commit `.shipkeep/` and open a
   pull request: a new dismissed entry hides a problem from later runs, so it
   is reviewed like a suppression comment.

6. **Turn recurring problems into rules.** List the items that failed in
   several recorded runs:

   ```bash
   python3 <this skill's directory>/scripts/report.py recurring <repository>/.shipkeep/history [--min-count 2]
   ```

   Each record counts once per item, and the same inspection recorded twice
   counts once. For each listed item, propose a check that a tool runs on
   every change (principle 12 of `references/change-principles.md`): a linter
   rule, an ast-grep or Semgrep rule, a CI check, or a repository setting. Let
   the user decide.

## The files in .shipkeep/

| File | Content |
| --- | --- |
| `.shipkeep/history/<date>-<tool>-<commit>.json` | A result in the common format, as recorded by `record` |
| `.shipkeep/dismissed.json` | `{"format": "shipkeep-dismissed/1", "items": [{"tool", "id", "reason", "dismissed_on", "issue"?}]}` |

## Limits

- Duplicates are found only through the marker that this script writes into
  Issue bodies; Issues written by hand about the same problem are not matched.
- The personal-data check looks for email addresses and home directory paths
  only, with the same allowances as shipkeep-publish-check (GitHub noreply
  addresses, example domains, generic names such as `/home/runner`). Masking
  secrets is the job of the tool that produced the result.
- `validate` hides property names that are not simple identifiers in its
  messages, because a key could hold a path or an address.
- `create` posts with the identity of the signed-in `gh` user. For scheduled
  runs, run `create` in a separate step that has write access, after a person
  or a rule has accepted the plan.
