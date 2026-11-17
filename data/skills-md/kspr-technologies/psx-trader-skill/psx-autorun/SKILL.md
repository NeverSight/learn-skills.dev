---
name: psx-autorun
description: >-
  Auto-run for the PSX pack, on a Mac. After a one-time install, the Mac runs the
  pack's own tools on a timer, with no Claude window open: a morning check before
  the Pakistan Stock Exchange (PSX) opens, the alert checks every 5 minutes while
  PSX is open, the scan and the long-term signals after the close, and a week
  report on Saturday. It tells you with a Mac message and a short report. Every
  time comes from the pack's PSX clock, so Fridays, Ramadan and holidays count.
  It never places an order and never runs psx-broker, psx-budget or psx-risk.
  Use when the user asks "will it auto run", "do I have to ask you to run the
  scan again", "check my stop while I am away", "set up auto-run", "is auto-run
  working", "pause auto-run", or "why did I get no message".
argument-hint: "[status | plan | tick --dry-run | run JOB | pause | resume]"
---

# psx-autorun

After a one-time install, your Mac runs the PSX tools by itself, on a timer.
You do not need to open Claude and ask.

- launchd (the Mac's own timer) starts a small app, "PSX Autorun", every 5 minutes.
- The app runs a plain Python runner. No AI model runs on the timer.
- The runner runs a fixed list of the pack's own tools. It writes a short report and sends Mac messages.
- Claude is still needed for plans, for explaining signals, and for every order. Each order needs your yes.

## What it does

- **Morning check** (before the open): the daily scan, the trading folder's alerts check (every closing
  file not checked yet, and the ex-dates of your swing shares), news, insider notices, and the long-term
  signals (psx-invest), news and notices.
- **Price checks** (while PSX is open, every 5 minutes): the alerts of the trading folder first, then the
  long-term folder. Your swing stop, target, trend and time rules are checked here.
- **After-close check**: it waits for the PSX closing file. Then the scan for the next session, the alerts
  on the close, the long-term signals and the news. It also lists each buy with no fill recorded, and each
  buy of that day filled in part.
- **Week report** (Saturday): the share list, the results of your long-term shares, the PSX days of the
  next week, and the cash in both folders.
- Each report says "Paper trading is on" or "Paper trading is OFF" for the trading folder.

## What it never does

- It never places an order. It has no broker link.
- It never runs psx-broker, psx-budget or psx-risk. An order needs your own yes in the chat.
- It never runs `invest.py orders`, `cash`, `ack` or `backfill`, or `alerts.py add` or `reset`.
  The code refuses them, whatever the settings file says.
- It never writes psx/orders.json and never touches a ticket.
- It never gives advice. A setup, an alert or a signal is a rule that matched. You decide.
- It reads the PSX site only when `"psx_site": true` is in that folder's psx/config.json:
  plain page reads, one tool at a time.

## What you need

- A Mac that is on, with the lid open and on power, in market hours. A shut lid sleeps. When the Mac is
  off, nothing runs.
- Python 3.8 or newer.
- About 5 minutes to install.

## Install (you do it, in Terminal)

Claude shows you the line. You run it yourself:

```bash
bash "<pack>/psx-autorun/install.sh" --trading "<folder that holds psx/>" --longterm "<folder that holds psx/>"
```

- `--trading` is needed. `--longterm` is for your long-term folder; leave it out if you have none.
- `--reports "<folder>"` puts the reports somewhere else (default: `<trading folder>/autorun`).
- No admin password. It only changes your own user's files.

What happens:
1. A test run starts. macOS asks you two things. Click **Allow** for both:
   - "PSX Autorun would like to access files in your Documents folder."
   - Notifications from PSX Autorun.
2. A message shows: "PSX auto-run works".
3. The installer asks: "Did you see the message "PSX auto-run works"? (y/n)". If you say n, it shows how
   to turn the messages on. Your files still work.
4. It turns the schedules on, then tests the real scheduled run (up to 60 seconds).
   If that run cannot write your reports folder, it turns everything off again and says how to fix it.
5. It prints today's plan. macOS may say "Background Items Added". That is auto-run. Leave it on.

## When it runs (Karachi time)

| day | morning | price checks | last checks | after-close |
| --- | --- | --- | --- | --- |
| Monday to Thursday | 8:15 AM | 9:40 AM to 3:30 PM | 3:40 PM | 4:10 PM, tries again to 7:30 PM |
| Friday | 8:00 AM | 9:25 AM to 12:00 PM, 2:40 PM to 4:30 PM | 12:10 PM, 4:40 PM | 5:10 PM, tries again to 8:30 PM |
| Ramadan, Monday to Thursday | 8:00 AM | 9:25 AM to 1:30 PM | 1:40 PM | 2:10 PM |
| Ramadan, Friday | 8:00 AM | 9:25 AM to 12:30 PM | 12:40 PM | 1:10 PM |
| weekend or PSX holiday | none | none | none | none |

- Checks are allowed from 7 minutes after the open (9:37 AM). The timer ticks at minute 0, 5, 10 and so on,
  so the first check is at 9:40 AM (9:25 AM and 2:40 PM on Fridays). After a wake it can come a bit earlier.
- The week report runs on Saturday at 10:00 AM (later if the Mac was off; never in market hours).
- Every time comes from the pack's PSX clock, and holidays come from the trading folder's
  psx/config.json (`"holidays"`, `"open_days"`, `"ramadan"`). Keep the long-term config the same.
- **A moon holiday** (expected, not fixed): the evening before, a message says the day may move. On the
  day, with the site on and a share held, auto-run takes one look at 10:00 AM. If PSX looks open, a
  message says so. Auto-run then checks nothing that day until you add the day under `"open_days"` in
  psx/config.json. It sees the change at the next tick.
- The after-close check waits for the closing file (out 30 to 40 minutes after the close). After 4 hours
  it says the file was not found. Was PSX closed that day? Then add the day under `"holidays"`.

## If the Mac was asleep

- When the Mac wakes, auto-run runs what it missed. A late report says "This ran late".
- A missed after-close check runs first, outside market hours, up to 4 days back.
- For a swing position with its plan in psx/portfolio.json, no close is lost: psx-alerts reads every
  closing file it has not checked yet, so a late check still rings what Friday's close showed.
- Rules you added by hand in psx/alerts.json (in either folder), and every rule in a day-style folder, use
  today's prices only, never a closing file. So a close the Mac slept through is not checked for them. The
  report then says the share "has no price from today". The first price check of the next session uses the
  new price.
- Such rules also see only the price at each check. So a dip under the stop between two checks is missed too.
- A share you hold with no swing plan (a day trade, or a share you bought before the switch to swing) has
  only such rules. See "If you already hold shares" in the README.
- So after a sleep, check those shares in your broker app. For example, a hand stop on a share you hold
  is not checked against the close you missed.

## Reports

In your reports folder (default `<trading folder>/autorun/`):
- `LATEST.md`: the newest report. Open this one first. When an alert rings (or a problem comes) in a price
  check, LATEST.md becomes the day's price checks page, so a click on the alert shows it.
- `STATUS.md`: when each job last ran, the alerts that rang today, problems now, and today's plan.
- `reports/<date>/morning.md`, `checks.md` (only alerts that rang, and problems), `after-close.md`.
  Each has a `-full.txt` file with every command, exit code and all output.
- `reports/weekly/week-of-<date>.md`.

Each report has "In short" bullets (setups, news, notices, alerts, signals, problems) and this footer:
"A setup, an alert or a signal is a rule that matched. It is not advice. Nothing was bought or sold.
Auto-run never places an order."

## Messages

- "PSX alert": each alert as it rings, with a sound. "PSX auto-run: problem": something failed.
- "PSX: Morning check done", "PSX: After-close check done", "PSX: Week report ready": counts only.
- A met swing rule of a share you still hold rings once a day. After it rang, the report still names it,
  never just "no new alert". The message counts it: "Swing rules still met: 1."
- "PSX signal" (long-term) and "PSX swing" (trading): a tool asked to tell you.
- Alerts and problems come first. More than 4 at once: the first 3, then "N more messages".
- A click opens the newest report.
- Set PSX Autorun to the **Alerts** style (System Settings, Notifications, PSX Autorun), so messages stay
  until you close them. Allow it in each Focus too, or a Focus hides them.

## Commands

Run them in Terminal, from `~/Library/Application Support/psx-autorun/`:

```bash
python3 autorun.py status            # when each job last ran
python3 autorun.py plan              # today's times (--now "YYYY-MM-DD HH:MM" for another day)
python3 autorun.py tick --dry-run    # what is due now, without running it
python3 autorun.py run morning       # run a job now (morning, after_close, weekly)
python3 autorun.py pause checks      # no price checks today, so no stop either, until resume
python3 autorun.py pause all         # stop everything until resume
python3 autorun.py pause all --minutes 10   # stop everything for 10 minutes, then go on by itself
python3 autorun.py resume
python3 autorun.py selftest          # install.sh runs this through the app
python3 autorun.py open-latest       # open LATEST.md
```

## Settings

The settings file is `~/Library/Application Support/psx-autorun/autorun.json`, made from
`autorun.example.json` by install.sh. The pack ships no paths of your own.

| key | default | what it means |
| --- | --- | --- |
| `morning_lead_min` | 75 | the morning check starts this many minutes before the open |
| `check_every_min` | 5 | minutes between two price checks |
| `after_close_delay_min` | 40 | the after-close check starts this many minutes after the close |
| `weekly` | Saturday 10:00 | `weekday` 0 is Monday, 5 is Saturday |
| `price_source` | `psx-screener` | one PSX page for all prices; `psx-company` reads one page a share |
| `tape` | `false` | `true` records the market every 2 minutes (day style only); then every check reads the tape |
| `keep_awake` | `true` | no idle sleep from the morning check to after the close (a shut lid still sleeps) |
| `notify` | all on | turn each kind of message on or off |

## Wake the Mac (optional)

This needs your admin password. It is your choice. It wakes the Mac at 7:55 AM, Monday to Friday:

```bash
sudo pmset repeat wakeorpoweron MTWRF 07:55:00
```

- It works when the Mac sleeps with the lid open, on power. With the lid shut, it may not wake fully.
- Only one repeat wake can be set on a Mac. To remove it: `sudo pmset repeat cancel`

## Turn it off

```bash
bash "<pack>/psx-autorun/uninstall.sh"
```

- It stops both schedules, removes them and the app, and resets the app's macOS permissions.
- `--all` also deletes auto-run's settings, state and logs.
- Your reports and your psx/ folders stay. A tape you started by hand is left alone.

## Problems and fixes

A problem is never silent: it shows in the report and as a "PSX auto-run: problem" message.

- **A price check failed 3 times in a row** (15 minutes): one message, then at most one an hour.
  "Working again" comes when it is fixed: at a check in the session, never at the last check after the
  close (PSX is closed then, so that check proves nothing).
- **"the DEMO stop was not checked for 15 minutes"**: a swing share you hold had no price newer than 15
  minutes in the session. Check the price in your broker app. With `"psx_site": false` auto-run cannot see
  prices in the session, so a held swing share gets this message (at most once an hour after the first).
  The closing files are still checked after the close.
- **"the DEMO alerts had no new price for 15 minutes"**: the trading folder's alerts saw only old prices in
  the session. This comes when another PSX tool runs (an entry watch saves no market prices), or with the
  site off. Check the price in your broker app.
- **"psx/portfolio.json in the trading folder is not valid JSON"** (or psx/config.json, or
  psx/state/broker.json): a file you edited by hand has a typo. Auto-run never moves or changes your files.
  Fix the file. Until then auto-run cannot read it (for the ledger: the report does not show what you hold).
  "Working again" comes when it reads.
- **"macOS blocks PSX Autorun from your Documents folder"**: open System Settings, Privacy & Security,
  Files and Folders, and turn on Documents Folder for PSX Autorun. Still blocked? Add PSX Autorun under
  Full Disk Access (the app is in `~/Library/Application Support/psx-autorun/`). Last: move the work
  folders out of Documents. Until then the reports go to `reports-fallback/` there.
- **"no Python at ..."** or **"The tick job did not run"**: Python moved (a pyenv update, for example).
  Run install.sh again. It keeps your settings. This message comes at most once an hour.
- **"no PSX tools at ..."**: the pack moved. Edit `"pack"` in autorun.json, or delete autorun.json and
  run install.sh again.
- **No message by 9:15 AM on a market day** (9:00 AM on Fridays and in Ramadan): something is off. Open
  System Settings, General, Login Items & Extensions, and check that PSX Autorun is allowed. Run
  `autorun.py status`. The logs are in `~/Library/Logs/psx-autorun/`.
- **No messages at all, but the reports are there**: macOS hides them. Turn on notifications for PSX
  Autorun, use the Alerts style, and allow it in each Focus.
- **A buy has no fill recorded** (after the close): record the fill (`ticket.py fill`), or record it
  expired (`ticket.py result --fingerprint FP --status expired`). New swing buys wait until then.
- **A buy is filled in part** (after the close, on that day only): if more of it filled, record that too
  (`ticket.py fill`). If not, the rest ended at the close with no fill. To record that:
  `ticket.py result --fingerprint FP --status expired`. psx-risk counts the rest only on that day.
- **"Cash: ... Does this match your broker app?"** (week report): one broker account holds both folders'
  cash. If a number is wrong: `ticket.py cash --set N` (trading) or `invest.py cash --set N` (long-term).

## Rules for Claude

- Never install or uninstall auto-run. Show the user the exact line; the user runs it in Terminal.
  Never run launchctl, osacompile or pmset for the user.
- Never add a step with an order tool to autorun.json (the code refuses it anyway).
- When the user asks about auto-run, read `LATEST.md` and `STATUS.md` in the reports folder first.
- Claude may run `status`, `plan`, `tick --dry-run`, `pause` and `resume` when the user asks, and
  `run JOB` when the user asks.
- One tool on the site at a time (the same rule as in the README):
  - A tape or an entry watch in the chat: auto-run sees it by itself. Then auto-run reads no PSX page, and
    its checks read only the prices saved on your computer. Do not pause auto-run for it. A tape saves new
    prices, so the checks go on. An entry watch saves no market prices: the trading folder's alerts then
    get no new price, and after 15 minutes auto-run sends a problem message. While a watch runs, tell the
    user to check the stop in the broker app.
  - Before your own alerts loop (a `/loop` or a scheduled task in Claude): run `autorun.py pause checks`.
    The pause lasts the rest of the day.
  - Until `autorun.py resume`, the price checks of both folders are off, so no stop is checked while PSX is
    open. The after-close job still runs. So run `autorun.py resume` as soon as the loop ends, and tell
    the user: until then auto-run checks no stop.
- Two writers, one file: auto-run's checks write psx/state/alerts.json, and its signals write
  psx/state/invest.json. So before `invest.py ack`, `invest.py backfill --forget-no-session`, `alerts.py add`
  or `alerts.py reset` in a folder auto-run watches, run `autorun.py pause all --minutes 10`, then
  `autorun.py resume` when done. A forgotten resume ends by itself after 10 minutes.
- Quote the report's own words and numbers. A rule that matched is not advice: say "the rule says ...
  you decide".
- Your broker app is where the user places orders (for example FS EDGE). Auto-run never does.

## Safety

- Education and tooling, not financial advice.
- Nothing in this pack places an order.
- Auto-run has no broker link.
- It never runs psx-broker, psx-budget or psx-risk.
- PSX prices here are about 5 minutes late.
- A stop is a plan, not a promise.
- Auto-run cannot see a market halt in late data.
