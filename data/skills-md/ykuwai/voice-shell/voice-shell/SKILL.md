---
name: "voice-shell"
description: "Let the user send prompts by voice. Start a resident process that keeps listening to the microphone, take what the user says through Monitor, and treat it as an instruction. Use it when the user says \"voice mode\", \"talk to me\", \"hands-free\", \"dictate my prompts\", or \"speak instead of typing\", in whatever language they say it. To stop, \"stop voice mode\". If the user asks to set voice-shell up (\"set up voice-shell\"), follow SETUP.md, work out which environment this is (macOS 26 or newer, or not), and guide them from there."
license: "MIT"
argument-hint: "[start | stop | status]"
allowed-tools:
  - Bash(${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh *)
  - Bash(tail *)
  - Bash(cat *)
  - Monitor
---

# Voice prompt mode

Take what the user speaks and receive it as a prompt, without the keyboard.

The part that listens to the microphone appends one line to a JSONL file every
time an utterance is finalized. Follow that log with Monitor and treat each line
that arrives as an instruction from the user.

**There are three ways of recognizing speech.** These are all you can pick from,
there is no other.

| Name | What it is | Where the audio goes |
|---|---|---|
| `browser` (default) | Chrome's Web Speech API. Works with nothing installed | **Google's servers** |
| `apple` | On-device recognition that ships with macOS 26. Light | Only inside this machine |
| `whisper` | faster-whisper. Strong on proper nouns | Only inside this machine |

The argument is `$ARGUMENTS` (`start` / `stop` / `status` / `setup`. `start` when omitted)

## When it is not set up yet

If `start` fails with `No Python it can run was found`, or if the user says
"set it up", walk them through [SETUP.md](SETUP.md).

On macOS 26 or newer there is no multi-GB model to download, though `apple` does
build a small Swift helper the first time and so wants the Command Line Tools
(`xcode-select --install`), which not every Mac has. Anywhere else it means
installing Whisper. Check first, then confirm which way to go. Do not install
everything on your own.

## Starting

**When in doubt, just run `start`.** It remembers which way of recognizing was
picked last time (`~/.config/voice-shell/config.json`), and the first time it is
"This browser" (Chrome's Web Speech API). Nothing to install, so there is no wait.

1. Start it.

   ```bash
   ${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh start
   ```

   **Where browser automation tools (claude-in-chrome and the like) are not
   available**, the viewer cannot be opened, so the default browser recognition
   does not hold up. Only in that case, have the user pick from the models that
   are installed.

   ```bash
   ${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh start --engine auto
   ```

   **Say how it is being recognized, once, the first time only.** The first
   time `start` runs on that machine, and only then, `start` itself prints
   `This uses the browser's built-in speech recognition feature to transcribe
   your voice.` along with the name of a local way that machine can use. Pass
   that line straight through to the user.
   **Do not say it again after that.** Repeating it every time does not change
   the choice, it only adds more to read.

   **Do not push the user toward a local model yourself.** Working right away
   with nothing installed is what the default is worth, and switching brings a
   download and a wait of 1 to 2 minutes. Whether it runs comfortably is not
   known until it is tried on that machine.

   When the user says "I want recognition to stay local" or "I do not want it
   sent to the cloud", show the list with `voice-shell.sh engines` and pass
   `--engine <the one they picked>` **after they have picked it**. On macOS 26
   or newer `apple` should already be there, so they can switch on the spot with no
   model to download. Two things still take time the first time on a machine, and
   only the first: the Swift helper is built (which fails outright without the
   Command Line Tools, saying so), and the OS fetches the speech model for that
   language by itself, tens of seconds. It is instant from then on.

   **Do not pass `--engine X` on your own to recover from a failure.** The name
   you pass is remembered as the default from then on, so passing it silently
   rewrites the user's choice for good. Pass it only after you have confirmed.

2. Wait until it has finished starting.

   ```bash
   ${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh wait-ready
   ```

   With browser recognition there is no model to load, so it returns at once.
   Only when a local model was picked does it take 1 to 2 minutes (other work
   can go on in the meantime). If `FAILED` comes back, tell the user the error
   that was shown.

3. `start` **tries to open the viewer automatically, in an ordinary tab.**
   There is no need to open it again yourself. Add `--no-gui` only when the
   user says they do not want it.

   **With browser recognition nothing arrives at all until the viewer is
   open, and the attempt to open it for them is not always trustworthy.**
   `start`'s own output always carries the line `The viewer started at
   http://127.0.0.1:...` (or `already running at`, on a second start).
   **Read that URL out to the user every time, not only when `Could not open
   a browser for you` is printed.** A Windows machine has been seen to print
   neither that failure line nor open anything (`cmd.exe`'s own way of
   launching a browser can report success without one actually opening), so
   waiting for an explicit failure line before saying anything left the user
   talking to a screen that was never going to arrive.

   To keep it **always on top**, press "Float on top" in the header (a browser
   rule, it cannot be opened unless a person acts, so the screen itself asks
   for that one press the first time).

4. Watch the utterance log with Monitor. **Always set `persistent: true`**
   (voice mode goes on for the whole session). Do not use `tail` directly,
   always go through `voice-shell.sh listen`. Going through it registers the
   fact that you are listening under `$STATE_DIR/listeners/`, and the
   registration disappears once Monitor ends (TaskStop or the end of the
   session). A raw `tail -F` is not registered, so it never shows up as a
   choice of where to send.

   ```
   Monitor(
     command: "${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh listen",
     description: "The user's voice prompts",
     persistent: true
   )
   ```

   **As of Claude Code 2.1.271, a watch may not run forever even with
   `persistent: true`** (a deadline, 30 minutes at the longest, replacing
   what used to be no timeout at all). Whether that holds going forward is
   not something to build around, a later Claude Code update could just as
   easily change it back, so nothing here leans on it. If a deadline
   notification does arrive, **treat it the same as starting fresh: call
   Monitor again with the exact same command.** `listen`'s own registration
   only disappears once the process itself actually stops (TaskStop or the
   session ending, same as ever), so a plain re-arm is enough, nothing needs
   stopping first.

**Keep only one Monitor of your own.** Re-arming on a deadline or "source
ended" notification (above) is always safe on its own. Re-attaching for some
other reason, compacting included, when the old one might still actually be
alive, stop it with TaskStop first. With two alive the same utterance
arrives twice.

**A resumed session (`claude -r`) does not know on its own whether its old
Monitor is still alive**, and folder name plus timestamp are not enough to
tell one listed session from another started from the same folder. Run
`voice-shell.sh listeners` (or `status`) and look for **`<- this session`**
next to an entry, this is added only to the one whose registration carries
this exact conversation's own id ($CLAUDE_CODE_SESSION_ID, always set while
you are running), so it settles the question outright instead of being
guessed. No such mark on any entry means your own Monitor is not registered
right now (start one with `listen`, as above). Note that starting
`listen` again is harmless either way, a second one under this same session id
retires the earlier registration on its own (compacting, #81, and a plain
re-arm on a deadline, above, are both usual ways this comes up), so this
check is about knowing where things stand, not about avoiding a duplicate.

**It is normal for other sessions to be listening too.** Using it alongside
other work is the intended way, and speech goes to **whichever started later**
(that is, the one you just started). `start` does not list the other sessions.
There is no need to know, and no report or offer to stop them is wanted. The
user can pick a different destination at any time from the top of the viewer.
Show `voice-shell.sh listeners` only when asked who is listening. Stop another
session only when the user asks for it.

**Do not stop `voice-shell.sh listen` with pkill.** Your own Monitor matches the
same pattern and goes down with it.

## When it does not work

| What was seen | What is going on | What to do |
|---|---|---|
| With browser recognition, `status` says `This browser does the recognizing` | **Normal** (there is no daemon on this machine) | Nothing. Do not try to start a daemon |
| Nothing arrives when speaking with browser recognition | The viewer is not open / the mic was refused / not Chrome | Say "open the viewer in Chrome and allow the microphone". Also ask whether a red warning is showing on screen |
| `No Python it can run was found` | Nothing is installed | Tell them `pip install numpy aiohttp` is enough (for browser recognition alone) |
| `wait-ready` returns `FAILED` | The model failed to start | Pass the error through as it is. Show what is installed with `engines`, and switch **only after confirming** |
| `wait-ready` returns `TIMEOUT` | Dragging on, a first model download for instance | Look at the tail of `daemon.out` and describe the situation |
| A plain `start` gives the same error every time | The remembered choice is in a failing state | Say "the choice from last time is failing", and revert it once confirmed |
| `"<name>" cannot be used` | The engine name is wrong | Pick again from the choices that were shown |

## What to do with speech that arrives

Each line that comes from Monitor is JSON. Only the body is in it.

```json
{"text": "run the tests"}
```

**A line with a `"system_warning"` key is not the user speaking.** It is a
warning the daemon itself writes, about things like being started more than
once, and it has no `"text"`. Do not carry it out as an instruction, pass the
content **straight to the user** (check the real list with `listeners`, and
explain anything they do not recognize. Ask the user before stopping anything
that is not in use).

```json
{"system_warning": "2 monitors are listening to the utterance log at once. ..."}
```

**It arrives in this shape when listening was ended from the screen too.**
Monitor then finishes on its own. It is the user's own doing, so do not be
alarmed, just pass the content along (and mention that typing `/voice-shell`
brings it back if they want to resume).

Lines that were fixed up in the viewer before being sent carry `"edited": true`.
That is **a sentence the user deliberately tidied**, so take it at face value instead of reading it as a recognition error.

**Treat `text` as an instruction from the user and carry it out as usual.** The
things to watch for are as follows.

- **Expect recognition errors.** It is speech recognition, so proper nouns and
  technical terms break, whatever language is being spoken. Read them back from
  context, "cloud code" is Claude Code and "get" is git. Ask again only when the
  meaning really cannot be recovered.
- **Ignore fillers.** Words like "um", "well" and "you know" carry no meaning.
  Every language has its own.
- **Short lines are dropped before they get here.** Anything under the minimum
  length (15 characters by default) never arrives, which is what keeps a bare
  "yeah" out. On top of that the daemon drops hesitation sounds on their own,
  "hmm" and "uh" and their kind in each language (`NOISE_ONLY` in
  `voice_daemon.py`). Words that mean something, "yeah" and "ok" among them,
  are not on that list. If a thin line does come through, wait instead of
  treating it as an instruction. **But if the dictionary has moved a word to the
  "do not ignore" side, it arrives even when short.** The user chose to let that
  word through, so even a bare "got it" can be taken at face value as a reply.
- **Read chopped-up speech as one piece.** One sentence can arrive across
  several lines. When a sentence is cut off partway, wait for the rest before
  reading it as a whole. Long speech is also split before it arrives, so that
  each piece fits what one line can carry. The pieces line up inside the same
  notification, so **when one notification holds several lines, read all of them
  as one continuous utterance before acting**. Even if the first line ends with
  a full stop, that does not mean the point is finished there. Some languages,
  Japanese among them, put the conclusion at the end, so running ahead gets the
  crucial part of the request wrong.
- **Always confirm destructive operations.** Speech can be misheard, so confirm
  with "shall I go ahead with ..." before deleting, pushing, deploying and so on.
- **An event is the user speaking, but it is not a demand for an answer.** When
  one arrives mid-task, it is fine to finish what you are doing first.
- **A single line that reads as plainly unrelated to the current work is not
  automatically carried out.** A stray remark, one side of a phone call, a
  reply meant for someone else standing there, these arrive as ordinary text
  the same as everything else. Acting on that one line immediately is the same
  mistake the holding section below exists to catch, just one line too early
  to see the pattern yet. Hold off on it instead. If the next line keeps going
  in the same unrelated direction, that confirms it and holding below takes
  over. If the next line returns to the task, the odd one was only an aside,
  and nothing was lost by not acting on it.

## It may be used by several pieces of work at once

Another session may be using voice mode at the same time for different work.
Once there are two or more listeners, speech **goes by default to the one that
started later** (when parallel work begins, turning to it is the natural thing).
Exactly one gets it, there is no "everyone".

So **if you are the older one, speech stops arriving**. That is normal, nothing
is being dropped. Do not restart because it stopped arriving, and do not change
the destination on your own. The user can pick again at any time from the
destinations lined up at the top of the viewer.

The order they line up in is decided by "when that conversation first started
listening". Putting voice mode back on does not change the number (so that "the
second one" can be said out loud). The default destination is separate from
this, it is **the one that just started**.

Pressing the × on a chip makes that session stop listening (the session itself
does not end). It takes two presses so it is not hit by mistake.

The display name is assigned automatically. It starts as the folder name, and
moves to the conversation's title once it has one. People who keep their
repositories in one place run several from the same parent folder, so the folder
name alone is not always enough to tell them apart.

**When told "name this session X", rename it right there.** The conversation
title is assigned automatically, so it can drift from what is actually being
done. Renaming it yourself when you notice is fine too.

```bash
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh name "Fixing the auth code"
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh name ""      # back to the automatic title
```

The name that was set stays in `~/.config/voice-shell/names.json`, so it
survives putting voice mode back on.

## When speech that is not an instruction keeps coming, move it to holding

The microphone keeps picking up the room. When the user takes a phone call or
starts chatting with someone next to them, speech that is not meant for you
flows in. Keeping all of it means reacting to things that have nothing to do
with the work.

```bash
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh hold "Sounds like a phone call, so I moved this to holding for now"
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh live      # back again
```

`hold` is **not mute**. Speech keeps collecting on screen and the user sends as
much of it as they want. Nothing is lost. **Do not use mute.** Cutting it leaves
the speech nowhere, and a user who is not watching the screen cannot tell that
nothing got through.

The note that is passed along shows on screen. A mode change the user did not
press is only confusing without a reason, so always write something.

**Keep the bar for switching high.** Switching by mistake leaves the user
talking with nothing getting through. Do it only when all of the following hold.

- **Twice or more in a row**, speech arrived that is plainly not an instruction
  for you (a conversation with a third person, a "hello?" into a phone, a topic
  unrelated to the work here)
- You have not just asked a question (you are not in the middle of waiting for
  an answer)
- The user did not say something like "I am just thinking out loud" or "hold
  on, a phone call" (if they did, just do as they said, no guessing needed)

**When in doubt, do not switch.** It is enough to take it and say "that did not
seem to be for me, so I will wait". When you do switch, always write it in the
chat as well (they may not be watching the screen). Go back the moment the user
speaks to you again.

## The live viewer

It comes up together with `start` (**http://127.0.0.1:47865**). Pass this URL
along when you tell the user it started. It only follows the log and does not
use the microphone, so it can run alongside the resident process.

Set `VOICE_SHELL_PORT` before starting it to use another port.

What it can do is as follows.
- Text still being recognized grows inside an "Unsent" card
- Speech that was sent stacks up as cards
- The destination can be set to **Instant** (goes straight through) or **Review**
  (collects, gets fixed, then sent). `"edited": true` is attached **only to lines
  that were touched in the draft before sending**. A line that went to review but
  was sent without a single character changed does not get it
- **Pause** (the ⏸ in the header). Speech while it is stopped is kept nowhere (for use during other work)
- **It can be driven by voice alone.** "mute" and "unmute" for the microphone,
  "draft" and "instant" to switch how things are sent, "cancel that" **at the end
  of a sentence** to take that whole utterance back, and "edit this" likewise at
  the end to send it to the draft instead, "switch to 2" or "number two" to
  change the destination.
  **Every language the screen can show has wordings of its own, and they can all
  be read from the lightbulb on screen.** The phrases above are the English ones.
  It only counts when **that phrase alone** is spoken (saying it inside a
  sentence does nothing). **Mute, unmute, and draft/hold mode are the
  exception**, a short burst of noise picked up ahead of the word
  ("はいミュート", "えーとミュート解除", "はい手直し") still counts, so it does
  not go missing when what the room picked up lands in front of it. Unmute's
  allowance is tighter, at most a couple of characters, not a whole clause, a
  false hit there costs the whole stretch the speaker thought was off, not one
  utterance. Switching back to instant stays exact only, for the same reason.
  The different ways a number
  gets read out loud are absorbed. A short sound plays when it switches.
  Users can add wording of their own
  (`~/.config/voice-shell/commands.json`). Only phrases said as a whole utterance
  can be added, not unmute and not the ones tacked onto the end of a sentence,
  because a false trigger costs too much.
  **Each kind can also be switched off from that same screen**, and the same file
  remembers which ones. All seven are independent, so somebody who does not want
  to mute by voice at all can turn both mute and unmute off. A kind that is off
  does nothing when spoken, and the words stay listed so it is clear what comes
  back when it is switched on again.
  **When several machines are in use at once, turn on "Several machines" in the
  settings and give each machine a name.** Then only a phrase with the name in
  front, like "work mute", is taken (without it, a phrase said at one machine
  sets off every machine). The destination numbers follow the order of the chips
  on screen, and they can be switched while the mic is off too. **Destination
  phrases only work when there are two or more listeners** (so that an utterance
  which was just an answer with a number in it is not eaten). The same code
  decides this for browser recognition and local models alike. **The one thing
  that cannot be heard is "unmute" after browser recognition was cut**
  (cutting it lets go of the audio itself). Turn it back on from the screen
- **It can be driven from the keyboard too.** Bare keys only move around the
  screen, keys with `Shift` change where the voice goes. `Shift`+`M` turns the
  mic on and off, `Shift`+`L` is instant, `Shift`+`H` is review, `Shift`+`E`
  reviews just that one utterance, `Shift`+`Backspace` throws away what is
  unsent, `Shift`+`1` through `Shift`+`9` pick the destination. As bare keys, `,`
  opens the settings, `?` the list of phrases, `Esc` closes whatever is open.
  `Ctrl` (`Cmd`)+`Enter` sends the draft. **None of them work while text is
  being typed.** The list is further down under the lightbulb on screen
- **Fix just this one.** Pressing the pencil on the unsent card holds that one
  utterance so it can be fixed. The destination display stays on instant (so it
  does not look like a permanent switch). Sending it or clearing it puts it back
- **Float on top.** Moves it to a small always-on-top window (the icon in the
  header. Chrome only)
- **It works small too.** Shrinking the window puts the microphone and the send
  mode side by side, the top strip keeps only the name tags, and shrinking
  further drops the strip altogether (the state shows in the window title). The
  destinations change from tags to a single picker. Text and buttons do not
  shrink. What is kept, in order, is the mic on and off > instant / review >
  destination > the text being recognized. Widening it brings everything back
- **The trigger level can also be changed by dragging the mark under the microphone**
  (no need to open the settings)
- Editing the viewer file makes "Updated. Tap to reload" appear at the bottom of
  an open screen. Pressing it reloads (a floated small window has no way to reload)

### Ways of recognizing

Picked under "Recognized by" in the settings. **The default is "This browser"**
(Chrome's Web Speech API), which loads no model, so it runs even on a weak
machine and works with no daemon running. To keep everything local, switch to
Apple or Whisper. Anything not installed does not appear as a choice.

**But the audio goes to Google's servers.** Do not recommend it to anyone who
has raised wanting everything to stay local. The screen carries a caution of
its own next to this setting, worded around "uses the browser's built-in
speech recognition" rather than naming Google outright (the README does name
it, for whoever reads that first). Know it either way before recommending
this one.

When Whisper is picked, the model can be named as well. Both a Hugging Face name
and the path of a folder on this machine are accepted. What is given is
remembered, so `start` alone is enough from then on.

```bash
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh start --engine whisper --model /path/to/my-model
```

The session is cut by 7 to 10 seconds of silence by design, but it is re-armed
ahead of time while nobody is speaking, so nothing is missed. Recognized text
goes through the same filtering as the daemon, on the server side.

**If there is no voice for a while, the mic is turned off from this side**
(5 minutes by default, 0 to 30 minutes under "Turn off when idle" in the
settings, 0 never turns it off). That way it does not keep reconnecting to
Google while the user is away from the desk. A sound and a note say when it is
turned off. Pressing the microphone brings it back.

### Settings (the gear)

Moving a control takes effect right then. No daemon restart is needed.

| Item | What it decides | Default |
|---|---|---|
| Microphone | Which input device to use | The system default |
| Trigger level | 0 to 100. Lower picks up fainter sounds | macOS 41 / Linux 74 |
| Pause to send | Being quiet this long marks the end of a chunk (with browser recognition, that end is already decided elsewhere, so this is the wait before an already-recognized one goes out) | 1.5 seconds |
| Min length | Recognition results shorter than this are dropped | 15 characters |
| Strip filler words | Drops the connecting words before sending (**this affects what is sent too**) | Off |
| Theme / Language | Looks | Automatic |

The trigger level is set by **dragging the mark under the microphone**. The bar
just above it is the current level, so have the user talk and put the mark where
only their voice crosses it. When they say "I am talking but nothing arrives",
the first thing to suggest is **lowering the trigger level**. The smaller the
number, the fainter the sound it starts picking up. The slider and the mark both
sit on the same scale of loudness, so lowering it moves both to the left.

It lives in `~/.config/voice-shell/tuning.json`. The daemon re-reads it every
0.5 seconds.

```bash
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh viewer        # → http://127.0.0.1:47865
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh viewer-stop
```

## Checking the state

```bash
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh status
```

## Stopping

```bash
${CLAUDE_SKILL_DIR}/scripts/voice-shell.sh stop
```

Once it is stopped, stop Monitor with TaskStop as well. The microphone is
released, and if Whisper was picked the memory the model took comes back. apple
has the OS do the recognizing, so it was never holding memory in the first place.

## The user dictionary

Words that are often misheard can be registered with a replacement, and
utterances to ignore can be registered too. Edit them from the **dictionary**
in the viewer (the book in the header). **It saves automatically the moment
focus leaves, and takes effect from the next utterance** (there is no save
button, and no daemon restart either).

It also hits the text while it is still being recognized, so **it already looks
replaced inside the card before it is sent** ("cloud code" turns into
`Claude Code`).
What is being replaced is only the look. The server rebuilds the body that gets
sent. If the user says it again differently, it follows along.

Words ignored by default (`NOISE_ONLY`) can be turned off by pressing their tag.
The list holds hesitation sounds only, and which ones show depends on the
language being spoken, not the one on screen. **A word that was turned off
passes straight through the minimum length gate too**, so short replies like
"got it" stop disappearing. When the user says "my replies do not seem to be
getting through", point them here.

It lives in `~/.config/voice-shell/dictionary.json`. CSV can be read in and
written out too. If the user keeps correcting the same misrecognition, it is
fine to suggest adding it to the dictionary.

## Limits

**The default (this browser) has no limits at all.** What follows is about
picking a local model.

- Browser recognition runs **only while the viewer is open**. Close it and
  nothing arrives
- Whisper **downloads a model and loads it**. The first time there is a download
  to wait for, and starting takes 1 to 2 minutes as well. How much memory it
  uses is decided by the size of the model
  - `--engine apple` (macOS 26 or newer, the recognition that ships with the OS)
    loads no model of its own, so neither the memory nor the 1 to 2 minutes
    apply to it. **The first run on a machine still waits**, tens of seconds,
    while the OS fetches the speech model for that language by itself. Nothing
    has to be installed for it and it happens on its own, and the model stays
    on the machine afterwards, so it is the first run only
- The microphone is taken through `sounddevice` (macOS and Windows) or
  `arecord` (Linux). Without `sounddevice` installed, macOS and Windows fall
  back to `ffmpeg`
- When a local model was picked but the environment is not in place, `start`
  fails with `No Python it can run was found`. Either go back to browser recognition
  (`start --engine browser`) or walk them through [SETUP.md](SETUP.md)
