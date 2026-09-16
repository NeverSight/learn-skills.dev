---
name: stay-awake
description: "Keep this Mac awake for a stated period using miserlymouse, replacing whatever timed assertion is already running without letting the machine sleep during the handover, and without disturbing an assertion held on behalf of a running job. Use when asked to keep the machine or laptop running, awake, or alive for another hour or two, to keep it from sleeping or going to sleep for a while, to stay awake until some clock time, or to check how much longer the machine will stay awake."
---

## Staying awake

miserlymouse holds a `caffeinate` assertion for a human-readable duration.

It lives at /Users/mtm/pdev/taylormonacelli/miserlymouse and runs from that checkout.

```sh
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/miserlymouse miserlymouse for 2h
```

The duration and clock-time grammars are documented in /Users/mtm/pdev/taylormonacelli/miserlymouse/README.md, so read that rather than guessing at a format.

## The default span is two hours

A request that names no span, such as a bare "stay awake", means `2h`.

Start it the same way any other request is started, since the default is a duration like any other and carries no special handling.

Nothing in miserlymouse supplies this, as the tool requires a duration and has no default of its own, so the default lives here and nowhere else.

Do not mention the default in the reply, because the one line already says how long the machine stays awake.

## Requests are a replacement, never an addition

"Keep this machine running for two hours longer" means the machine should be awake until two hours from now.

It does not mean two hours on top of whatever is already scheduled.

So the new end time is always the moment of the request plus the span asked for, regardless of what was already running.

This shortens as readily as it extends, and asking for `20m` while an eight-hour assertion is up correctly brings the end time forward.

The one thing it never shortens is an assertion held on behalf of a running job, which is covered below.

## Two shapes of miserlymouse run

Everything in this skill turns on telling these apart, so classify before acting.

A timed run was given only a duration, and it is the kind this skill starts and replaces.

A wrapping run was given a command to run as well, as in `miserlymouse 30m make build`, and this skill never touches one.

The supervisor processes are the ones whose argv contains `bin/miserlymouse`:

```sh
pgrep -f bin/miserlymouse
```

Ask each supervisor for its direct child, then ask what that child actually is:

```sh
pgrep -P 22088
```

```sh
ps -o comm= -p 22089
```

A direct child named `caffeinate` means a timed run, and that child is the assertion this skill may replace.

A direct child named anything else means a wrapping run, where the child is the job itself and the assertion is a grandchild beneath it.

## Why a wrapping run is off limits

`caffeinate` forks a child to hold the assertion and then execs the job over its own process, so the job keeps the PID the supervisor spawned and the assertion sits underneath the job rather than beside it.

When a job is wrapped, `caffeinate` ignores `-t` entirely, so the assertion lasts exactly as long as the job and has no scheduled end time to compare a request against.

Killing that assertion does not stop the job, it only strips the job of the thing keeping the machine awake, and the job then runs on toward a machine that is free to sleep.

Because the assertion is a grandchild, `pgrep -P` from the supervisor does not reach it, which is the safeguard, and it must stay that way.

Never search for `caffeinate` by name across the process table and kill what comes back, because that reaches straight past this safeguard and into a running job's assertion.

## Only a timed run's assertion is ever killed

Reach every assertion by `pgrep -P` from a supervisor that classified as a timed run.

A `caffeinate` that no such walk arrives at belongs to a wrapping run or to some other tool entirely, and it is not this skill's to end.

## Answering how much longer

A question about how long the machine stays awake is answered from the whole picture, and it starts and kills nothing.

List every assertion on the machine:

```sh
pgrep -l caffeinate
```

Then take each one in turn:

```sh
ps -o pid=,ppid=,lstart=,command= -p 22089
```

Walk each one up by parent to see whether it belongs to a miserlymouse supervisor, directly for a timed run or through the job for a wrapping run.

For a timed run, the end time is the `lstart` value plus the seconds given to `-t`, and the time remaining is those seconds minus `etime`.

For a wrapping run, say the assertion lasts as long as the job and name the job, because there is no end time to give.

For anything else, name it as another tool's assertion and leave it at that.

Report the latest end time among them as the answer, phrased as the section on speaking an end time requires, and say plainly if a job or a foreign assertion is what carries the machine past the timed run.

If nothing is holding an assertion, say the machine is free to sleep whenever it likes.

## The reply is one line

The whole reply is the span and the end time, and nothing else.

"1h from now, at Tuesday 1:30 AM" is a complete answer to a request to stay awake longer.

Say nothing about supervisors, assertions, PIDs, or which step of the procedure is underway, because the steps are how the answer is reached rather than part of it.

Do not narrate between tool calls, since a running commentary on classification and handover is the same verbosity spread across more messages.

Do not explain that the request replaced an existing assertion rather than adding to it, because that is how the tool always behaves and saying so every time teaches nothing.

Do not report the absence of other assertions, since the one line already accounts for the whole machine.

A second line is warranted only when something changes the answer, meaning a wrapping run or a foreign assertion carries the machine past the stated end time, or the new assertion failed to start and the old schedule still stands.

## How an end time is spoken

Every end time reported to the user is a friendly day and clock phrase rather than a timestamp.

Say "Saturday at 12:40 AM", never "00:40:04" and never "2026-08-29T00:40:04".

Write the meridiem as AM or PM, and never spell it out as "in the morning", "at night", or any similar phrase.

Give the span remaining alongside the clock time, as in "30m from now, at Saturday 12:40 AM", so the answer needs no arithmetic to be useful.

Write that span compactly, as hours and minutes squashed against their units, `2h30m` or `30m`, rather than spelling out "30 minutes" or "two and a half hours".

That is the same duration grammar miserlymouse accepts as input, so a span read back out of a report can be handed straight to the tool.

Drop a component that is zero rather than padding it, so ninety minutes is `1h30m` and one hundred twenty minutes is `2h`.

Measure that span from the moment of the report rather than from the moment the assertion started, since those differ once a few tool calls have gone by.

Drop the seconds, since no one schedules a laptop to the second.

Name the day of the week whenever the end time falls outside the current day, which a late night request usually does.

The ISO 8601 form that `--json --dry-run` prints is an input to this translation, not something to hand over as is.

## Starting or replacing

The order of these steps is the whole point of the skill.

A new assertion has to be live before the old one dies, or the machine is briefly free to sleep in the gap.

Step one, classify every supervisor as above, and record the assertion PIDs of the timed runs only.

Wrapping runs are recorded too, but as things to report rather than things to kill.

Step two, start the new one detached, so it outlives this session:

```sh
nohup uv run --no-active --project /Users/mtm/pdev/taylormonacelli/miserlymouse miserlymouse for 2h > /dev/null 2>&1 &
```

Step three, find the new supervisor by listing supervisors again and taking the PID that was not there in step one.

Differencing the PID sets is what identifies it, because two runs of the same duration are indistinguishable by argv.

Step four, confirm the new supervisor has actually acquired its assertion:

```sh
pgrep -P <new supervisor PID> caffeinate
```

If that prints nothing, run it again in a fresh call, up to about ten seconds in total, because a cold `uv` start is not instant.

If it never appears, stop and report the failure, leaving the old assertion untouched.

The machine stays awake on the old schedule in that case, which is the safe outcome.

Step five, and only now, kill each timed assertion PID recorded in step one:

```sh
kill 22089
```

Step six, confirm that the new supervisor is present and that no timed supervisor other than it survives.

Any wrapping run recorded in step one is expected to still be there, and its survival is success rather than failure.

Report the new end time in the spoken form above, and add that a job is holding its own assertion whenever one is, since the machine will then stay awake until the later of the two.

## Kill the assertion, never the supervisor

Killing the `uv` wrapper or the Python supervisor orphans `caffeinate`, which then holds the machine awake for the entire original span with nothing supervising it.

Killing the `caffeinate` child instead is a complete teardown, because the supervisor sees its child exit and shuts itself down, taking the `uv` wrapper with it.

One `kill` on the assertion PID removes the whole tree.

## Until a clock time

A request phrased against the clock keeps the same six steps and only changes the tail of the command:

```sh
nohup uv run --no-active --project /Users/mtm/pdev/taylormonacelli/miserlymouse miserlymouse until 5pm > /dev/null 2>&1 &
```

Pass the time through to miserlymouse rather than converting it to a duration, because it already resolves a time to its next occurrence.

## Warnings before the end

miserlymouse pushes an ntfy warning to the phone as the end of an assertion approaches, unasked, so no flag for it belongs in the command this skill runs.

The offsets and the topic are documented in /Users/mtm/pdev/taylormonacelli/miserlymouse/README.md, so read that rather than restating them.

Never pass `--no-notify`, because the warning exists precisely to reach someone who is not watching the terminal.

A replacement takes the old warning schedule down with the assertion it belonged to, which is correct, since a warning about an end time that no longer applies is worse than no warning.

Report the new end time as always, and leave the warnings unmentioned unless asked, since they need nothing from the user beyond a subscription already in place.

A wrapping run pushes nothing at all, having no scheduled end to count down to, which is one more reason it is never a substitute for a timed run.

## Reference

`nohup` and the trailing `&` are both required, and the process reparents to PID 1 and survives the session ending.

Sending `SIGINT` to a detached supervisor does nothing at all, because the backgrounding shell sets that signal to ignore and Python inherits it, so the tool's Ctrl-C teardown never runs.

The progress bar suppresses itself when detached, since stderr is not a terminal, so `--no-progress` is unnecessary.

`pgrep -f bin/miserlymouse` matches only the Python supervisor and not the `uv` wrapper, whose argv spells the project path without a `bin` component.

Adding `--json --dry-run` prints the exact end time as ISO 8601 and runs nothing, which is a way to state the resulting schedule before committing to it.
