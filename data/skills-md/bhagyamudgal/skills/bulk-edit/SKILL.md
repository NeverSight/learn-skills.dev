---
name: bulk-edit
description: Plan and run one mechanical edit across a whole population of records. Use when reformatting, renaming, retagging or stripping a field across dozens or thousands of issues, rows, files or board items, and whenever a mass edit needs a dry run, a rollback or proof that it did not touch anything else.
---

# Bulk edit

I turn "change this field on all of them" into a transform that refuses what it cannot prove, a run that survives interruption, and a verification that also covers the records I was never meant to touch. `preflight-mutations` authorizes the writes; I own everything around them.

The failure I exist to prevent is not a crash. It is a run that reports success while having silently flattened a distinction the population depended on. Every gate below exists because that failure is quiet.

`${CLAUDE_SKILL_DIR}/references/worked-example.md` walks one real 638-record run, including the four near-misses that put these gates here. Read it when a gate below looks like overhead.

## 1. Fix the population and the field

I state the population as a query someone else can re-run, and I resolve it against the system rather than against the requester's phrasing. "Every ticket on the board" and "every ticket in the repo" are different sets, and the difference is a number I report before anything else. I edit exactly one field. A run that touches two fields is two runs with two ledgers.

I count the population and the candidate subset separately. Most requests name the population but mean the subset that actually changes, and those two numbers rarely match.

**Gate.** The population is a re-runnable query with a count, the candidate subset has its own count, and the field is named and singular.

## 2. Characterize every variant before I write the transform

The example in the request is one variant, never the specification. I dump the whole population locally, once, and enumerate the real shapes by frequency. I do not sample, and I do not eyeball.

I count the separators, delimiters, prefixes and joiners that actually occur, then read the long tail. The frequent shapes are the ones I already knew about. **The rare shapes are the ones that break the transform**, and they are invisible in a sample: a joiner appearing four times in three thousand records is exactly the case whose meaning differs from the common one.

For each distinct shape I ask what it means, not what it looks like. Two shapes that render similarly and mean differently are the trap. A chain arrow and an ampersand can sit in the same position and read as "then" and "and", and collapsing both the same way destroys the second.

**Gate.** I can state the count of every distinct shape in the population, I have looked at the rarest, and I have written down which shapes carry a meaning the transform must preserve.

## 3. Write a transform that refuses

I anchor the transform structurally rather than by pattern search. A rule that matches from a fixed edge and stops at a defined boundary cannot reach data elsewhere in the record; a rule that hunts for anything resembling the pattern eventually finds one in the middle of real content.

Every record gets classified `OK` or `HOLD` with a reason. `HOLD` is an output of the run, not a failure of it. I refuse whenever the shape carries a meaning I cannot prove, and I refuse whenever a wrong guess would be unrecoverable in the record itself.

I never widen the transform to reduce the hold count. A hold list I hand back is cheap; a flattened distinction is permanent.

**Gate.** Every record in the population is `OK` or `HOLD`-with-a-reason, those two counts reconcile to the population count, and the hold list is written where the requester can read it.

## 4. Snapshot, then dry run against the live system

I take a fresh snapshot of the whole population's current value immediately before the run, and I store it outside the working tree so a clean or a checkout cannot reach it. The exploration dump from section 2 is not the snapshot; it is minutes or hours stale, and the difference is exactly the records someone else edited while I was planning.

I dry run against the live system, not against the dump. The dry run's job is to prove the transform still applies to what is actually there.

Whitespace and encoding drift will show up here as false mismatches. When a record fails an equality check against the dump, I re-derive the transform from the live value and compare the *result*. If the result matches the plan, the record is fine and my guard was too strict. That check is better than equality anyway: it validates against what exists rather than against what I remember.

**Gate.** The snapshot is timestamped, stored outside the working tree, and covers the whole population. The dry run ran against live values and its counts reconcile with section 3.

## 5. Authorize the batch

I hand the batch to `preflight-mutations` and do not write until its verdict is `ready`.

I check the platform's own history before planning recovery. Many systems retain the prior value permanently and for free: an issue tracker that records renames, a table with an audit trigger, a filesystem with snapshots. That retention hands me the captured prior value a restoration needs, so I verify it on one real record rather than assuming it and record the exact query that reads the old value back.

Retention proves the compensation is possible. It does not change the reversibility class. `preflight-mutations` owns that classification, and an edit whose original event or downstream effects outlive the restoration stays `compensating-only` however cleanly the old value reads back. I supply the evidence and let that skill classify, because upgrading the class myself would skip the fresh confirmation it requires.

I also write the restore path as a runnable script, not a described procedure. It reverts from the section 4 snapshot, and it refuses any record whose current value is neither my new value nor the original, so a colleague's later edit survives the rollback.

**Gate.** Verdict is `ready`, the recovery path has been demonstrated on one real record, and the restore script exists and runs in dry-run mode.

## 6. Execute

I write one canary record first and verify it through every independent path I have: the write response, a fresh read, and the platform's history. Only then do I run the rest. A canary costs one record and catches the whole class of error that would otherwise land on all of them.

I pick the cheapest write path the API offers, and I check which quota it spends. Systems commonly split their budget across buckets that fail independently, so the obvious client command and the underlying REST call can differ by several times in cost. Where the write response returns the updated record, the write and its verification are one call rather than three. `references/github.md` carries the worked numbers for GitHub.

I pace the loop and probe the remaining budget periodically, sleeping when it runs low rather than discovering the limit by being refused. A rejection partway through a population leaves a half-edited set, which is the expensive failure.

The ledger is keyed by record ID, appended after every attempt, and flushed immediately. A resumed run reads it and skips what landed. I never restart from an assumed zero state.

**Gate.** The canary verified through at least two independent paths, the ledger accounts for every record in the candidate set, and every error carries its response text rather than a count.

## 7. Verify the whole population, including what I did not target

I re-read the whole population from the authoritative source. Search indexes and list endpoints commonly lag writes by minutes and will report a clean run as broken, or a broken one as clean. I read objects, not search results.

I report three numbers, not one:

| Check | Question | Failure means |
|---|---|---|
| Targets | Do all `OK` records now hold the planned value? | The run is incomplete |
| Holds | Are all `HOLD` records unchanged? | The transform reached further than designed |
| Collateral | Did any record outside the candidate set change value? | Something else edited concurrently, or my anchor leaked |

The collateral check is the one that gets skipped and the only one that catches an over-broad transform. A run that reports "638 of 638 succeeded" without it has not shown that it changed only 638 records.

I expect a small number of survivors that look like failures and are not, where the record held the pattern in a position the transform deliberately does not reach. I show the before and after for each and say why it is correct rather than burying it in a total.

**Gate.** All three checks are reported with numbers, and every apparent exception is shown with its before and after.

## 8. Find the producer that will undo this

A field maintained by a recurring job regrows after I clean it. Before reporting the work as finished I ask what writes this field on an ongoing basis, and I test the answer rather than accepting it.

Edit history carries the evidence. I pull the change events for a few representative records and cluster their timestamps by weekday and hour in the relevant timezone. A weekly job produces an unmistakable spike; human maintenance scatters.

The account behind the writes tells me a job exists, not where it runs. A machine-regular schedule under an ordinary user account is consistent with an off-platform cron and equally consistent with a scheduled workflow authenticating as that user through a stored token. So I search the repository's own automation configuration and the hosts it could run on as two independent checks, and I rule out neither on the strength of the account type.

When someone names the job's location, I verify the location separately from the schedule. Those two claims fail independently, and the schedule being right is not evidence that the path is. A recalled path from an unavailable memory system is a hypothesis.

**Sequencing matters more than speed here.** If the producer rewrites records whose field disagrees with some source of truth, then an edit that makes *every* record disagree hands that job the largest possible batch. The cleanup and the producer change have an order, and doing them backwards costs more churn than doing nothing. I say so plainly rather than proceeding.

**Gate.** I have named the producer with evidence, or stated that I looked and found none. If a producer exists and is still live, I report the sequencing constraint before recommending any follow-up edit.

## Reporting

I report what ran, the three verification numbers, the hold list with its reasons, the backup location with its restore command, and anything I deliberately left undone. A hold count without its reasons is a number the requester cannot act on.

**Done.** The candidate set is edited and verified, the holds are reported unedited, the collateral check is clean, and the rollback path is runnable.
