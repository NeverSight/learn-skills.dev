---
name: aar-loop
description: Run an After Action Review on the task or session that just happened, using the US Army's 4-question AAR method, extract concrete lessons, propose (and on approval, write) durable fixes to the skills and rules files the agent loads next time, and log everything to a persistent LESSONS.md so the next session stops repeating the same mistake. Use when the user says "aar", "after action review", "review this session", "what did we learn", "run an aar", "apply the fix", "fix it", or right after a task that had friction, a surprise, or a failure worth capturing.
---

# AAR Loop

A human-run version of the Army's After Action Review, pointed at an AI agent's own session. Ask the same 4 questions the Army asks after every rotation at the National Training Center, answer them honestly about what the agent just did, and write down what changed as a result. Do this every session and the agent accumulates real, checkable lessons instead of starting from zero each time.

## Where this comes from

The US Army formalized the After Action Review in the mid-1970s, after Vietnam, as a structured debrief for training exercises. It became official doctrine in 1993 with field manual TC 25-20, and the Army still runs one after every rotation at the National Training Center, Fort Irwin: what the unit meant to do, what actually happened, why the two didn't match, and what changes before the next fight. Fifty years of practice on one method because it works on a simple mechanism: separate the debrief from blame, and the same mistake gets caught before it repeats.

This skill borrows that mechanism for AI agent sessions. It has a research parallel too: Reflexion (Shinn et al., 2023, arXiv:2303.11366) showed agents that generate a verbal self-reflection after a failed attempt and carry that reflection into the next attempt outperform agents with no memory of what went wrong. This skill is that idea run by hand: you are the reflection step, and LESSONS.md is the memory Reflexion keeps in an episodic buffer.

## The 4 questions

Ask all four, in order, about the task or session just finished. Answer briefly and honestly, in the agent's own words, not the user's guess at what happened.

1. **What was supposed to happen?** The plan, the instruction, the expected outcome, stated plainly.
2. **What actually happened?** The real outcome, including partial completions, errors, silent failures, and anything the agent had to work around.
3. **Why was there a difference?** The actual mechanism, not a mood. "The API caps batch writes at 100 and returns 200 OK on a partial write" is a why. "I should have been more careful" is not.
4. **What do we do the same or differently next time?** The concrete rule that would have prevented the gap, or the thing that worked and should be repeated.

If the answer to question 3 is "nothing went wrong, this worked exactly as planned," that is a valid AAR. Write down what worked as a lesson too. Most of AAR's value on a bad day is catching a bug; most of its value on a good day is locking in a pattern that isn't obvious yet.

## Extracting a concrete lesson

Question 4 only pays off if the lesson is specific enough to check later. Test every lesson against this: could a different agent, six months from now, read this line and know exactly what to do or not do, with no judgment call required?

Concrete, checkable (ship these):
- "Batch size over 100 rows fails with a silent timeout; cap batch writes at 100 and check the actual row count returned, not the status code."
- "A retry loop with no backoff hammers the API on every failure and gets the whole client rate-limited for an hour; add exponential backoff and cap retries at 5."
- "The scheduled job compared timestamps in local time across a daylight-saving change and fired an hour early; store and compare everything in UTC."

Vague, do not ship (kill these on sight):
- "Write better code."
- "Be more careful with APIs."
- "Communicate more clearly."
- "Double check things before finishing."

A lesson that names no specific tool, number, file, command, or condition is not a lesson yet. Push on it until it is, or drop it.

## Turning a lesson into a durable fix

Not every lesson needs to change a file. Some are just context worth remembering, like "this vendor's API is slow on Mondays, that's expected, don't treat it as a bug." Those only need to live in LESSONS.md. Others point at something that will keep failing quietly unless a rule, checklist, or skill actually changes. For each lesson, ask one question: will the next session make this same mistake again unless something it loads is different? If yes, it needs a fix plan, not just a log line.

A fix plan names the exact target and the exact edit, the same specificity bar as the lesson itself:

- **Target:** the file that will actually get loaded next time. A project's CLAUDE.md or AGENTS.md for a rule, a specific SKILL.md for a workflow step, a checklist file, or a config file.
- **Edit:** the literal line or rule to add, not a description of the general idea. "Add a step to the deploy checklist: after any deploy, query the running version of every service it touched" is an edit. "Improve the deploy process" is not.

Present the fix plan as a short numbered list before touching anything:

```
FIX PLAN
1. Target: CLAUDE.md
   Add rule: "After any deploy, verify the running version on every service
   it touched. Do not trust the deploy script's exit code alone."
2. Target: skills/deploy/SKILL.md, step 6
   Insert a post-deploy check: query each service's running version and
   compare it against the build hash before reporting the deploy as done.
```

Wait for approval before editing anything, unless the user already invoked this AAR with "apply" or "fix it" in the same request, in which case apply the plan directly and report what changed. If the user says nothing about a presented plan, treat that as "not yet," not as a yes, and leave the files alone. When approved, make the edits the same way any other file edit gets made, then confirm each one landed.

If a lesson doesn't clear the bar for a fix plan, say so and move straight to writing it to LESSONS.md. Forcing a file edit for every lesson turns useful context into noise and makes the real fixes harder to find later.

## Writing the lesson

Use `scripts/append_lesson.py` (stdlib only, no install) to append a dated entry to LESSONS.md:

```
python3 scripts/append_lesson.py \
  --lesson "Batch size over 100 rows fails with a silent timeout; cap writes at 100." \
  --expected "Bulk upload of 500 rows would complete in one call." \
  --actual "Call returned 200 OK but only 100 rows were written; the rest silently dropped." \
  --why "The API caps batch writes at 100 and does not error on a partial write." \
  --tags "api,timeouts"
```

Each entry gets a date and, optionally, tags for later filtering. List what is already recorded before adding more, so the same lesson doesn't get written twice with different wording:

```
python3 scripts/append_lesson.py --list
python3 scripts/append_lesson.py --list --tag api
```

Default file is `./LESSONS.md` in the current project. For a lesson that applies everywhere, not just this project, pass `--file ~/.claude/AAR_LESSONS.md` instead and note that in the entry.

Every lesson gets written to LESSONS.md whether or not it also got a fix plan. If a fix was proposed and applied, say so in the `--why` field or `--tags` (for example `--tags "deploy,fix-applied"`) so a later read of LESSONS.md shows whether the underlying file was actually changed or the lesson is still just logged.

## Loading lessons next session

Writing the file only helps if it actually gets read. Two ways to make that automatic:

1. **Project-local:** put a pointer line in the project's CLAUDE.md or AGENTS.md: "Read LESSONS.md before starting work." Any agent that reads project instructions at session start picks it up for free.
2. **On demand:** before a task that resembles a past one, run `python3 scripts/append_lesson.py --list --tag <relevant-tag>` and skim it. Cheap, and it catches the mistake before it happens instead of after.

A lessons file nobody loads is a diary, not a loop. The loop only closes when the next session actually reads it before acting.

## What this is, and what it is not

This is a disciplined reflection-and-write step, not an automatic improvement mechanism. It proposes, and on approval writes, changes to the skills, rules, and lessons files the agent loads, not the model itself. Nothing here retrains anything or changes model weights, and a proposed fix only helps once it is actually applied and actually loaded by a future session. It runs after the task or session ends; the fix takes effect starting next time, not mid-session and not in real time.

It works only if three things all happen: the lesson is written specifically enough to be checkable, a fix plan (when one applies) names an exact file and an exact edit instead of a vague intention, and the resulting file is actually loaded and read before the next relevant task. Skip any one of these and this is either a file that grows and never gets consulted, or a pile of proposed fixes that never got applied, both of which are worse than nothing, because they create the appearance of a system that's learning when nothing is.

Run it honestly. An AAR that only ever says "everything went great" is not doing its job. Push for the real friction point, even on a task that mostly succeeded, and don't invent a fix plan where the lesson was only ever context.

## Workflow

1. Finish the task or session.
2. Ask and answer the 4 questions in chat, out loud, briefly.
3. Extract 1 to 3 concrete, checkable lessons from the answers. Zero is fine if nothing checkable came out of it; do not force one.
4. For each lesson, decide whether it needs a durable fix. If yes, write a fix plan (exact target file, exact edit) and present it as a numbered list. Apply it on approval, or immediately if the user invoked this with "apply" or "fix it". If no, skip straight to logging it.
5. Check existing lessons first (`--list`) to avoid duplicates.
6. Write each lesson with `scripts/append_lesson.py`, noting whether a fix was applied.
7. If this is a new lessons file, add the pointer line to the project's CLAUDE.md or AGENTS.md so it loads automatically next time.
8. Report back in chat: the 4 answers, the fix plan and its status (proposed or applied), the lesson(s) written, and the file path.

## Rules

- Every lesson names a specific tool, command, number, file, or condition. No vague lessons.
- Every fix plan names an exact target file and an exact edit. No vague plans like "improve the process."
- Never apply a fix plan without approval, unless the user already said "apply" or "fix it" for this AAR.
- Not every lesson gets a fix plan. Context-only lessons go straight to LESSONS.md.
- Run the AAR honestly, including on tasks that went fine. Locking in what worked is half the value.
- Check for duplicates before writing.
- Keep this skill's own writing clean: no em dashes, no inflated claims about what an AAR loop can do on its own.
