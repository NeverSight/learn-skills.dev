---
name: architecture-review
description: Use when the user asks for a critical review of a repository's architecture — where the design is risky or fragile, what to fix first, hidden couplings, security, data and deployment assumptions, or where the documents and the code disagree. Builds on c4-diagrams output. Not for generating diagrams or architecture documentation (use c4-diagrams), a quick question about one file, reviewing a diff or pull request, or changing code.
license: MIT
compatibility: Requires python3 (3.11+, checked at startup) and the c4-facts.json that the c4-diagrams skill writes. Reads a local repository path.
metadata:
  author: ythalorossy
  version: "3.6.0"
---

# Architecture Review

You are the reviewer. A script collects evidence; you read it and the code, judge the design, and write `ArchitectureReview.md`: what is wrong, who it hurts, what to do first. A finding that only restates a fact ("no HEALTHCHECK", "A imports B") is not a review.

## Where things are

`<skill>` is the folder holding this `SKILL.md`; the harness prints its absolute path when the skill loads. Use it wherever `<skill>` appears: the working directory is the user's repository. Commands use `python3`; where it is not on the PATH use `python` or `py -3`.

## Step 1 — Get the c4 facts

Look for `./architecture-docs/<repository name>/c4-facts.json`. If it is missing, run the c4-diagrams skill on the repository first; this skill reads its output and never imports its code. If `c4-model.json` exists, read its `flows` and its `summary` (overview and findings) too.

## Step 2 — Collect the evidence

```bash
python3 "<skill>/scripts/collect_evidence.py" "<repository_path>"
```

Run it from the user's working directory. It writes `review-evidence.json` beside the c4 facts. Pass `--facts <file>` or `--output <folder>` only if the user named other locations. The file holds:

- `context`: what the c4 facts and the c4 model say about the system, plus CI, hosting and documents;
- `signals`: facts with `file:line` locations, grouped by lens, each with a `confidence`;
- `not_checked`: what the signals cannot see.

A signal is a lead, not a finding. `<skill>/references/lens-guide.md` says what each context field and signal `kind` shows, what its location means and what to check next. For something absent (a missing `HEALTHCHECK`, no authentication marker) the location is where the thing would belong, not a line that proves it.

## Step 3 — Read before you judge

1. Read the documents in `context.documents`. What does the system claim to be?
2. Open the code at every signal's location. Confirm it, or discard it as a false alarm and say so. Check `low` confidence signals first.
3. Walk each lens in the guide and ask what the signals cannot show: a dependency the diagrams omit (a broker, a cache), a service that cannot start in its own image, an assumption about the environment.
4. For each protection the documents claim (a rate limit, a negative cache, authentication), read the code that enforces it and check it does what is claimed. A documented, tested control can still be broken: its tests may mock the broken part.
5. For each risk, ask what concretely breaks, for whom, and under what condition.
6. Scale to the repository: start from the signals, documents and entry points, and read around each risk. List what you did not read.

## Step 4 — Write the review

Fill `<skill>/assets/review-report-template.md`; `<skill>/assets/example-review.md` is a finished one. Save it as `ArchitectureReview.md` in the folder that holds `review-evidence.json`. Each finding has:

| Field | Requirement |
|---|---|
| Priority | one of High, Medium or Low, then ` — ` and the reason for that rank |
| Evidence | locations you opened as full repo-relative `path:line` or `path:start-end`, and signal ids |
| Scenario | who or what is affected and what goes wrong; not the evidence reworded |
| Fix | specific enough to start on |
| Tradeoff | what the fix costs or gives up |
| Confidence | High, Medium or Low (a range like Medium-High is allowed), then what it rests on |

Rank by consequence. **High**: a failure, breach or data loss on a normal path, or the system cannot work as deployed. **Medium**: it will cost real effort or risk later, or needs a second fault to bite. **Low**: hygiene. No High finding is a valid result; do not inflate a rank. Order findings High first and put every finding in the action plan. Give each the lens where its fix lives; if it spans two, the one whose owner would act on it.

In the Evidence field, backtick only locations and signal ids; put config keys and prose outside. For an absence, cite where the thing would belong and name what is missing in the Scenario. Take line numbers from one file at a time (`grep -n`, or `sed -n` on one file): running numbers across several files are wrong. Every signal id must appear: in a finding's evidence, or in the last section with why you set it aside. Write the findings first; the lens analysis cites them.

State goals and quality attributes you inferred as inferred. Say plainly what you did not inspect. End with the template's Report Metadata, its version from the evidence's `generator`.

Then check the review:

```bash
python3 "<skill>/scripts/check_review.py" "<ArchitectureReview.md>" "<repository_path>"
```

It lists every problem as a `PROBLEM:` line: a citation past the end of a file, a missing field, a finding no lens cites, a signal nobody mentions. Fix each and run it again until it prints `Review check: ok`.

## Step 5 — Tell the user

In chat: what the system is in two sentences, the three findings to act on first, the path to `ArchitectureReview.md`, your assumptions, and what the review could not see. The full review is in the file; do not paste it.

## Common mistakes

| Mistake | Fix |
|---|---|
| Copying signal summaries into findings | Open the code, find the consequence, write the scenario. |
| A scenario that says "this is a risk" | Name who is affected and what happens. |
| Reporting every signal | Drop false alarms and low-value ones; say which in the last section. |
| Treating an absent marker as proof | `auth-markers-absent` is a search, not a fact. Say so and lower the confidence. |
| Putting a secret's value in the review | Name the variable and the file. Never the value. |
| Inventing goals or architecture | Mark inferences; cite the file or document each claim comes from. |
| Everything High | Rank by consequence. A list with no ordering helps nobody. |
| Line numbers taken from several files read at once | Cite from one file at a time; `check_review.py` catches a line past the end of a file. |
| Re-drawing the C4 diagrams | Link them. This is a judgment, not documentation. |

## Example prompts

- "Review the architecture of this repo and tell me what to fix first."
- "Where is this system fragile? I care most about security and deployment."
- "Does the code actually match what the README says about how this is deployed?"
- "What hidden couplings are there between the services?"
