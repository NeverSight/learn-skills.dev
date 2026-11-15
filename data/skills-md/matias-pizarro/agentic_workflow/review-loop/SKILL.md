---
name: review-loop
description: Loop until Codex has no findings. Each turn commits pending work, sends it to a Codex review, commits the review, grills the user through each finding, records and commits the response.
disable-model-invocation: true
---

# Review loop

A design loop: commit what is pending, ask Codex for a second-model review of one topic's artefacts, commit the review, walk the user through every finding with the grilling discipline, record what was decided beside the review, commit that, and go again until a review comes back with no findings.

A **turn** is one pass through the three phases, **submit**, **discuss** and **close**. Phases follow each other without pausing; the only waits are the approval of a new topic brief in submit and the per-finding questions in discuss.

## Prerequisites

- A git repo that keeps work under `.scratch/<topic>/`.
- A reviewer: `codex`, logged in, or `pi` with `OPENAI_API_KEY` set. tmux is optional.
- The `grilling` and `domain-modeling` skills, which discuss loads.
- A backlog, `.scratch/backlog.md`, created by discuss the first time a finding goes there.
- Commit subjects below are conventional commits; where the project's commit style differs, follow the project.

## Invocation

- `/review-loop`: run turns until a review has no findings, at most five.
- `/review-loop <n>`: the same, with the cap at round `<n>` of the loop, the k in the titles, however many invocations the loop has taken. `once` is the spelling for one turn.
- `/review-loop [<n>] auto`: unattended discuss; see the discuss phase for what auto does and where it still waits.
- `/review-loop submit`, `/review-loop discuss`, `/review-loop close`: one phase, then stop.

A turn whose review has any finding, low included, is followed by another turn; a review with none ends the loop. The cap counts per loop, never per topic. When the cap is reached with findings still open, say the loop has not converged and stop; the next invocation continues from the last close.

## Vocabulary

- **Topic**: a directory under `.scratch/` holding one set of artefacts, such as a spec and its tickets. Named by the user, or inferred from the artefacts touched since the last review; ask when two topics are touched.
- **Review file**: `.scratch/<topic>/reviews/review-codex-<YYYYmmddHHMM>-<hash>[-<suffix>]-findings.md`, written by Codex. The suffix names the artefact kind when a topic has more than one (`spec`, `tickets`); design docs carry none.
- **Response file**: the review file's path with `-response` in place of `-findings`, written in discuss. The prior response is the newest `*-response.md` in the topic's `reviews/`. Review and response files live in `reviews/`; the topic brief stays at the topic's top level. The two words are chosen so the review sorts before its response by filename.
- **Loop**: the run of turns on one artefact of a topic that ends with a review without findings. Named by the suffix, or `design` when there is none, or by the user (`code`, `DAG check`).
- **Round number**: N, the topic's round count including this turn: one more than the highest number in the H1s under the topic's `reviews/`. The review's H1 starts `# Na. ` and the response's `# Nb. `, so a listing by title reads 1a, 1b, 2a and so on.
- **Loop round**: k, the loop's round count including this turn: one more than the k in the newest review H1 naming this loop, or 1 when there is none or that review had no findings. Review and response H1s end with ` (<loop> round <k>)`: `# 23a. Cloud-sandbox code review (code round 7)`.
- **Topic brief**: `.scratch/<topic>/review-brief.md`, the durable part of the review prompt. Created from [`brief-template.md`](brief-template.md) on a topic's first run.
- **Finding**: one numbered item in a review.
- **Deliberate choice**: a finding the user resolves by accepting the risk or cost.
- **Impact**: high, medium or low, by what goes wrong, and for whom, if the finding stays. The Pareto few, the findings carrying most of the harm, are the important ones.
- **Effort**: very low, low, medium or high, by what fixing the finding costs. Very low is a word or a line, cheaper than writing its backlog entry.
- **Backlog**: `.scratch/backlog.md`, the project's visible list of parked items, one entry each: the date, the item, its impact, its source (the review file and finding number) and the user's words with their time.
- **Drift**: a finding in lines an earlier round of this loop added or changed, or two rounds of this loop finding gaps in the same check. A loop that drifts has likely lost its way; drift is a signal to bring to the user, never to suppress.

## submit

1. If the tree is dirty, commit it with a one-line subject and a short body; a review or response file waits for its own commit.
2. Identify the topic and suffix. If the topic brief is missing, create it from the template, filling the scope, sources and checks from the artefacts you can see, and leaving out the lines about a prior review. Show it to the user and wait for their approval.
3. Build the prompt from the brief, adapting it to this turn:
   - the commit hash and `git show --stat <hash>` line;
   - the prior response file by path and its finding count, read from the file, with the disposition-table instruction naming that count; on a first run, omit both;
   - the brief's do-not-re-raise list plus any deliberate choice recorded in the prior response and any finding this loop sent to the backlog;
   - a check for whatever this turn changed that the brief's standing checks do not name;
   - these two checks, verbatim, beside the brief's standing checks:
     ```
     - over-build, a finding of the same weight as a gap: code, a check, an option, a test or a criterion that the scope the user asked for, or a simpler design, makes unnecessary, above all a check of state before a step that is already idempotent; name what to delete;
     - for every finding, its impact, high, medium or low, by what goes wrong and for whom if it stays; and drift: whether it sits in lines an earlier round of this loop added or changed, or in a check an earlier round of this loop also found a gap in, naming that round;
     ```
   - the round number, with the instruction to title the report `# Na. <title> (<loop> round <k>)`, N and k written out;
   - the brief's Sources section, its `Read them against:` line and list kept as they are.

   The prompt always ends with these three lines, verbatim:
   ```
   If nothing is above low severity, say so plainly.
   Do not edit files.
   Produce a markdown report ordered by severity, citing every file as the Citations section says.
   ```
4. Write the prompt to a temporary file and run the review as a subagent with [`run-review`](run-review), which sits beside this file, from the repo root:
   ```
   <this skill's directory>/run-review <review file> <prompt file>
   ```
   Run it with a tool timeout of at least thirty-two minutes, since the script enforces thirty itself. `run-review` refuses to start, with exit 2, a prompt lacking the title instruction, the Sources list or the three closing lines; fix the prompt and run it again. After a review it strips trailing whitespace and ends the file with a newline. Any other non-zero exit (124 for the time limit) means no review: report the exit status and stop the turn.
5. Before the first commit, check the review's first line is an H1 starting `# Na. ` and ending ` (<loop> round <k>)`; if Codex wrote none or left either off, add it. Commit the review file alone: `docs: record codex <topic> review`. If a commit hook refuses it for a link, bring the link to the brief's citation format and the citation rules in the project's `AGENTS.md`, changing only its target, plus the line number in its text when the target carried one the text lacks. Commit again.
6. Completion: the review file exists, is committed, and has been read; report its finding count and severities in one line.

## discuss

Load the `grilling` and `domain-modeling` skills.

### Summary rules

Every summary of a round follows these four rules, in this order: the summary printed after the last finding, and any summary that carries the round's questions to the user or to whoever relays them, before they are answered.

1. **Tally first.** The summary's first line is the loop's running cost: `<topic> · <loop> round k · findings so far F · questions so far Q`, F and Q counted over this loop's reviews and responses, this round included.
2. **Drift next.** Check this round's findings for drift before asking about any of them. When any drifts, the first question is `❓ DRIFT-Qn`: which findings drift and the earlier rounds they trace to, then three options, the recommended one first: step back and delete or simplify the code the rounds keep returning to, saying what goes; stop, sending the open findings to the backlog; continue. A stop answer writes a backlog entry and a response entry for each finding, then goes to close, which commits and ends the loop.
3. **Impact, effort and Pareto.** Rate every finding's impact and effort (see Vocabulary). Recommend fix for the important ones; fix now for a finding of low impact and very low effort; the backlog only for the rest, low impact with real effort.
4. **Delete offered.** Every finding's question offers three answers: fix; delete, which removes the code, check or option the finding sits in and says what that removes, or says why nothing can go; backlog. Recommend delete over fix wherever deleting answers the finding as well.

### Per finding

For each finding in severity order, once DRIFT-Qn is answered or there is none:

1. State in one or two sentences whether the finding is right, and the fact that settles it, then its impact and effort.
2. Put exactly one question in the grilling format, offering fix, delete and backlog as the summary rules say, with a recommended answer the user can accept with "yes". When two findings share one root cause, one question may cover both and must say so.
3. Wait. Edit nothing before the answer. In `auto` mode, do not wait: take the recommended answer as the answer and say so in the response entry. The exceptions are a recommended answer that is a deliberate choice or the backlog; auto mode stops at that finding and waits, because a recorded acceptance of a risk or cost, and a backlog entry, carry the user's words and an edit does not.
4. Apply the answer to every file it touches, a backlog answer as an entry in the backlog, then append the finding's entry to the response file, created with an H1 starting `# Nb. ` and ending ` (<loop> round <k>)`: its number and title, what was decided, and where it landed.
5. Sweep the class: after fixing a finding, search the code for other instances of its class (a failed read taken as absence, a missing rollback, a quoting error) and fix them in the same turn; name them in the response entry.
6. A finding that is a transcription error against a decision already made is applied without a question and reported as such.

After the last finding: check each finding's class was swept as in step 5, run a grep for wording the round made stale, fix what it finds, end the response file with a one-line agreement or disagreement with the review's disposition table, and summarise by the summary rules: the tally line, then one bullet per finding with its impact, effort and answer, nothing committed, the next phase named. Print it and continue into close without waiting.

Completion: drift was checked, and DRIFT-Qn asked when any finding drifts; every finding has a response entry, every edit the entries name exists in the tree, every backlog answer has its backlog entry, each finding's class has been swept, the stale-wording grep is clean, the response file ends with its disposition line, and the summary is printed, following the summary rules.

## close

1. Commit everything the discuss phase touched, response file included: `docs: respond to the Codex <topic> review of <hash>`, body one line per finding.
2. If the review just closed had no findings, say the loop has converged and stop. If the user answered stop to DRIFT-Qn, say the loop stopped on drift, name the backlog entries, and stop. Otherwise, if the turn cap is not reached, print the commit line and start the next turn's submit without waiting. If it is reached, or the invocation was a single phase or `once`, print the next `/review-loop` command for this topic, ready to paste, and stop.

## Guardrails

- Review and response files are committed in separate commits, never together with design edits, so `git log` shows what Codex said and what was decided as two events.
- The prompt names files, never pastes them; Codex reads the tree.
- A finding is resolved by a change, by a deliberate choice written, marked as such, where the project records decisions (the ticket or ADR it concerns), or by a backlog entry, as well as in the response. Rewording alone resolves nothing.
