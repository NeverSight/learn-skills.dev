---
name: work-hours
description: Measure how many hours a person really works per day, per client or project, and at what clock times, from the digital exhaust they already leave — Claude Code transcripts, Slack, WhatsApp, meeting recordings, laptop screen time, browser history and chess games — with leisure subtracted and the idle threshold calibrated against their own stated breaks. Use it whenever someone asks "how many hours do I actually work", "how much time do I spend on client X vs Y", "what are my working hours / routine", "am I overworking", "how much of my day is chess / YouTube", or wants a timesheet reconstructed after the fact. Trigger it even when the word "hours" never appears — "how long are my days", "split my time between customers", "when do I usually start and stop" are this skill.
---

# Work hours

Reconstructs working time after the fact from timestamps the person already produces. The answer is
only as good as two things: **telling the person's own actions from automation**, and **deciding what a
silence means**. Everything below is about getting those two right.

Read `references/methodology.md` before trusting any number — it lists the traps that each moved the answer
by hours. `references/sources.md` has the per-source how-to.

## Ground rules

- **Personal data, temporary by default.** Everything goes in the run dir from the config
  (`run_dir`, default `~/.cache/work-hours/run`). Never write extracted events into a repo. When the person
  says they are done, delete the run dir and every upload (browser histories, chat exports, screen-time
  databases); confirm the paths are gone.
- **Read-only everywhere.** Slack, GitHub, trackers, mail: search and read, never post or react.
- **Throttle.** Transcript folders run to gigabytes: `nice -n 19 ionice -c3`, stream line by line,
  one or two readers, `python3 -I`.
- **Ask for data, don't guess it.** The person can give you things you cannot reach (chat exports, laptop
  files, a chess username, their meeting schedule). Ask early; see "What to ask for".

## Workflow

```bash
S=<this skill>/scripts
# 0. config: copy references/config.example.json to ~/.config/work-hours/config.json and fill it in
#    (timezone, window, customer rules, Slack user id, chess usernames, meeting schedule, categories).
#    The person's real config never lives inside the skill.

python3 -I $S/extract_claude.py                 # human prompts + answers/interrupts from transcripts
# Slack: run the MCP search loop (references/sources.md), then:
python3 -I $S/slack_parse.py <saved result files...>
python3 -I $S/extract_whatsapp.py _chat.txt --me "<name>" --customer <c> --tag <who>
python3 -I $S/extract_chess.py                  # chess.com / lichess → leisure intervals
python3 -I $S/extract_meetings.py               # recordings + recurring calls (run after the point extractors)
python3 -I $S/extract_mac.py <upload-dir>       # laptop presence, foreground apps, browsing
# any other human-only source (PR approvals, tracker moves made in the UI): write events.<name>.ndjson
python3 -I $S/calibrate.py                      # silence survival, bout criterion, ground-truth check
python3 -I $S/model.py --idle 25 --tail 5       # → report.md
```

Point events are `events.<source>.ndjson` (`ts`, `src`, `customer`, `kind`); intervals are
`intervals.<source>.ndjson` (`start`, `end`, `category`). `model.py` picks up every file matching those names,
so a new source is just a new file.

## The model

Two independent methods. Report both; **their agreement is the accuracy claim**.

- **B. Messages:** one merged timeline of every human action across every source. A silence of up to
  `idle` minutes is work; a longer one is a break that still credits `tail` minutes after the last action.
  Leisure intervals (chess games, leisure browsing) are subtracted.
- **A. Presence:** laptop present (unlocked, display-sleep tail removed), minus leisure, plus off-laptop work
  **only where there is evidence**: phone messages while the laptop was away, bridged when under `idle`
  minutes apart, and calls. Do not let the message model's gap-filling run while the laptop says the person
  left — that double-counts about 1.5 h/day.

Measure across all customers combined first; the per-customer split comes from attributing each worked
minute to the nearest action's customer. Cut workdays at a fixed local hour (default 05:00), so a 02:00
session belongs to the day before.

## Choosing the idle threshold (the number that matters most)

On one real dataset the answer swung from 6.0 to 13.9 h/day between a 5- and 60-minute threshold, and
the gap histogram had no natural break. Calibrate it; don't pick it.

1. `calibrate.py` gives the bout criterion: a lower bound, usually around 10 minutes.
2. **Ground truth from the person's own words.** Read their messages for "lunch", "brb", "back",
   "going to sleep", "on the train, working from my phone", in every language they use. Read each hit
   yourself: a word list must not decide meaning. Write `labels.ndjson` with `away` and `phone_work`
   stretches. The right threshold separates the two. In the calibration run, stated breaks always left a
   silence of 27 minutes or more and phone work never exceeded about 26, so the answer was 25 minutes.
3. **Attention check.** In agent-driven work, see whether the person replies seconds after an agent finishes
   (they were watching) or long after (they were away). If replies come about 16 minutes after the agent
   finished and almost never within 2 minutes, a silence is not attentive waiting, so do not stretch the
   threshold to cover it.

## What to ask for

Ranked by value:

1. **Laptop activity.** Send `references/mac-upload-prompt.md` to an agent on their Mac. It uploads browser
   histories, `knowledgeC.db` (screen on, foreground app) and the lock/power logs. This is the strongest
   signal.
2. **Chat exports** with the people they work with (WhatsApp "Export chat").
3. **Usernames for leisure that has an API** (chess.com, lichess).
4. **Recurring meetings:** day, time, length, and when they changed.
5. **Slow exports, if they want more precision:** Google Takeout (YouTube and Maps), Apple Health (sleep).
   iPhone Screen Time only reaches the Mac if "Share Across Devices" is on, and even then it sits in system
   stores that need Full Disk Access.
6. **Vacations and other periods to exclude**, as config `exclude`.

## Reporting

Lead with the combined hours per weekday and weekend day, then the range across methods and thresholds.
Then cover the per-customer split, the clock-time routine (start, meal dips, second shift, end) and how much
leisure was found inside "work". Name what is still invisible: phone screen time, unrecorded calls,
thinking away from the keyboard.
