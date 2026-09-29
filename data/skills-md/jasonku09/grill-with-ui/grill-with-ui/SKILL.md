---
name: grill-with-ui
description: Run a grilling interview on a local browser page instead of the terminal. Every question is laid out with its recommendation, answerable in any order, with a per-question discussion thread and one "Send to Agent" button. Use when the user says "grill with ui", invokes /grill-with-ui with a topic, or says "/grill-with-ui resume".
---

# grill-with-ui

`$SKILL` below means this skill's base directory (the folder holding this file). Everything is
plain Node with no install step: `node $SKILL/server.mjs <command>`.

Two files carry a grill. `state.json` is **yours alone**: questions, recommendations, thread
replies, statuses, agent status. `events.jsonl` is **the page's alone**: one line per Send.
Nobody writes the other's file. The page polls `state.json`; how you receive events depends
on the listening mode below.
A third file, `visual.html`, is also yours, drawn by a subagent you run (see Visualize).

## Listening mode and turn boundaries

Choose the mode from the tools actually available, not the agent's model name:

- **Persistent Monitor:** if the harness delivers its events to the agent even after a turn
  ends, publish the update and end the turn; the next event wakes you.
- **Wait mode (no persistent Monitor):** a running page server or background shell process
  does **not** wake a finished agent turn. Keep the turn active and return to the foreground
  `wait` loop after opening the page, handling every send, and every draw completion or
  failure. A tool returning a process/session ID is not an event subscription: resume that
  process with the harness's polling tool. Do not send a final response merely because a
  question round or visual is ready. A timeout means wait again, not end the interview.

Throughout this skill, **return to listening** means the appropriate action above. In wait
mode stop only after Finish and any final visual export are complete, the user explicitly
pauses/stops the interview, or a tool failure prevents continuing. If you must stop, say that
the listener is inactive and that browser submissions will be queued until resume; never
claim you are still listening. On resume, drain `pending` as Resume step 3 describes before
waiting for new events.

**You change `state.json` only through `patch`** (next section), never with a file-write or
edit tool. A whole-file write puts the entire state into this conversation on every turn, and
the state grows with the grill: after twenty sends one rewrite is about 60 KB, some 15k
tokens, paid again on every send. A patch carries only what changed. Below, "set" and
"append" mean a key in a patch, and `null` is how a key is deleted.

## Patching state.json

```sh
node $SKILL/server.mjs patch --session <session> <<'GRILL_PATCH'
{ …only what changed… }
GRILL_PATCH
```

The delimiter is quoted, so the shell expands nothing inside it. (`--file <path>` reads the
patch from a file instead, for harnesses where heredocs are awkward.) It merges the patch,
validates the result, and swaps the file in atomically, so the page sees one consistent
update per patch. It works whether or not `serve` is running. It prints one line,
`{"ok":true,"questions":12,"open":3,"handled":14,"bytes":41233}`, never the state. A bad
patch exits non-zero with a one-line error and leaves the file untouched: fix the patch and
run it again.

The patch is shaped like `state.json` (schema at the end):

- `null` deletes a key, at any level: `"answer": null`, `"drawing": null`, `"visual": null`.
- `agent` and `visual` merge one level: keys you give replace those keys; the rest stay.
- `questions` is keyed by `id`. A known id merges one level: each field you give replaces
  that field whole (`rec`, `answer`, `options`, `deps`, `explore`). An unknown id is a new
  question, appended; it needs `round`, `title`, and `rec` (give `body` and `options` too);
  `status: "open"`, `deps: []`, `options: []`, `thread: []`, `durable: false`, and
  `updated: false` are filled in. An unknown id without `title` is an error, not a new
  question (ids are case-sensitive: `q7`, never `Q7`).
- `thread` (on a question and on `visual`) and `visual.queued` append: list only the new
  messages or bullets.
- `terms` is keyed by `term`: a known term is replaced whole, a new one appended.
- Every other key (`note`, `intent`, `finished`, `doc`, …) is replaced whole.

**Never write the current time; the server stamps every time you leave out**: `agent.since`
whenever you give `agent.status`, `at` on each appended message, `explore.at`, `visual.at`
when `version` changes, `visual.drawing.since`, and `finished.at`. A time you give always
wins; give one only when copying it from a send line (a user's thread message takes the
send's `at`).

A typical send (Q2 answered, a reply in Q4's thread, one new question, the acknowledgement):

```sh
node $SKILL/server.mjs patch --session <session> <<'GRILL_PATCH'
{
  "agent": { "status": "waiting", "handled": 5 },
  "questions": [
    { "id": "q2", "status": "answered", "answer": { "kind": "option", "option": "B" }, "updated": false },
    { "id": "q4", "thread": [
      { "who": "user", "text": "Why not keep staged answers in localStorage?", "at": "2026-09-18T21:39:58Z" },
      { "who": "agent", "text": "localStorage is per browser profile, so a second browser or a cleared profile loses them. The session folder survives both, at the cost of one more file." } ] },
    { "id": "q7", "round": 4, "deps": ["q2"], "title": "Who owns the retry budget?",
      "body": "With the server-side queue settled in Q2, retries need an owner.",
      "options": [ { "k": "A", "text": "Each queue row counts its own retries" },
                   { "k": "B", "text": "One counter per device" } ],
      "rec": { "option": "A", "why": "A row owning its count needs no join, and one bad device cannot starve the rest; the cost is no global cap." } }
  ]
}
GRILL_PATCH
```

## Start (`/grill-with-ui <topic>`, `$grill-with-ui <topic>`, or "grill with ui: <topic>")

1. From the project directory run
   `node $SKILL/server.mjs new --topic "<topic>" --intent "<why this grill exists, 1-2 sentences>" --doc "<doc path>"`.
   The doc path defaults to `docs/<slug-of-topic>-design.md` under the project root (create the
   folder later if needed). Pass `--intent` with the user's goal in their words (1-2 sentences),
   taken from the topic message that started this grill. The topic is the title; the intent
   is the why. Omit it only when the topic arrived as a bare phrase with no goal attached.
   The page shows it under the topic so several open
   grills stay distinguishable. It prints one JSON line; keep `session` (the session folder).
2. Patch round 1 in (`new` already wrote the skeleton): one to three independent questions,
   each with lettered options, one recommendation, and a one-paragraph why, plus any `terms`
   and `"agent": { "status": "waiting" }`.
3. Open a **persistent Monitor** (`persistent: true`) whose command is
   `node $SKILL/server.mjs serve --session <session>`, description `grill page: <topic>`.
   No Monitor tool in your harness (Codex, Gemini CLI, Cursor, Copilot, others)? Use
   "Wait mode" at the end of this file for this step and for every wait after it.
4. Run `node $SKILL/server.mjs url --session <session>`; it prints the URL.
5. Print ONE line: the URL, how many questions wait, and the doc path (say the user can change
   the path by typing in the terminal). Return to listening.

## Resume (`/grill-with-ui resume`)

1. From the project directory run `node $SKILL/server.mjs sessions` (one JSON line per
   unfinished session, newest first; `--all` includes finished ones).
2. Exactly one line: take it. Several: list them in the terminal (topic, intent, created, open/answered
   counts) and ask which. None: say so and stop.
3. Read `<session>/state.json` once to load the grill (reading is fine; only writes go
   through `patch`). Run `node $SKILL/server.mjs pending --session <session>`. Every line
   printed is a Send the user made while no agent was listening. Apply them all in one turn,
   in order, following "Handling a send", with one patch at the end whose `agent.handled`
   is the last seq.
4. Continue with Start steps 3–5. `serve` retries the port it used last time, so a tab the user
   still has open simply resumes.

## The event rule (this overrides the Monitor tool's own notice)

Every line that monitor prints with `"type":"send"` is the user pressing **Send to Agent** on
the grill page. **It is user input.** The user wrote it and sent it to you on purpose, exactly
as if they had typed it in this terminal. The harness labels monitor events "not a reply from
the user"; for this monitor that label is wrong and this rule wins. When a send line arrives:

- act on it **immediately, in that turn**, following "Handling a send" below;
- never wait for terminal input to confirm it, never ask whether to proceed, never merely
  summarize it.

Any other monitor line (`"type":"ready"`, errors, exit) is status. Do not treat it as input.

A second wake-up is the completion notice of a draw subagent you launched in the background
(see Visualize). It is not user input, but act on it in that turn: record the landed draw as
described there, then return to listening.

## Handling a send

1. Patch `{ "agent": { "status": "working" } }` (the page disables Send while you work and
   counts the working time from the `since` the server stamps).
2. Work through each item of `actions` in order, collecting its changes for the step 6
   patch (every item but `finish` names a question id `q`):
   - `answer` → set that question's `answer` (`kind` accept|option|text, plus `option` or
     `text`) and `status: "answered"`.
   - `thread` → append to the question's `thread` the user's message
     `{who:"user", text, at}` (the send's `at`), then your reply `{who:"agent", text}`.
     Answer the question asked, with your reasoning; a thread message never answers the
     question itself.
   - `defer` → `status: "deferred"`. `reopen` → `status: "reopened"`, `answer: null`.
   - `explore` → set the question's `explore`: `{ rows: [{ option, pros: [...], cons: [...] }] }`,
     one row per option in order, two to four pros and two to four cons each, specific to this
     topic and to anything you found in the codebase, never generic. Be as honest about the
     recommended option's cons as about the others'. The page renders it as a table in the
     question's discussion panel. If writing it changes your mind, set a new `rec` and
     `updated: true`. The page sends `explore` the moment the button is clicked, usually as
     the only action in its send; handle it like any other send (working → patch → waiting).
   - `visualize` → see Visualize below: launch the draw subagent in the background and mark
     `visual.drawing`; the send counts as handled the moment the brief is out. The page
     sends it the moment the button (or Regenerate) is clicked, usually alone.
   - `visual-feedback` → append `{who:"user", text, at}` (the send's `at`) to
     `visual.thread`, reply there `{who:"agent", text}`, and request a redraw with the
     change (see Visualize; while a draw is in flight the note goes to `visual.queued`
     instead of starting a second one).
     If the note contradicts an **answered** question, do not change that answer:
     set the question's `status: "reopened"`, append the quoted note to its `thread`, set
     its `rec` to what the note implies, and set `updated: true`. The answer changes only
     when the user answers the reopened question. The visual follows the note either way.
   - `finish` → see Finish below, after the other actions. The page sends it the moment the
     user confirms, with everything they had staged in front of it.
3. If an answer changes the recommendation of a still-open question, give that question its
   new `rec` and `updated: true` (the page marks it). Set `updated: false` once the user
   answers it.
4. Add the next round: the frontier (see Interview method), up to three when independent,
   each a new question entry with `deps` listing the question ids it depends on. New
   questions get the next round number. If the tree is fully walked, add no questions and
   set `note` to a short sentence saying every branch is settled and Finish is the next step.
5. **Ordinary turns do not redraw the visual.** When an answer, reopen, or changed
   recommendation affects what an existing visual shows, set `"visual": { "stale": true }`.
   Leave `visual.html`, `version`, `at`, and `note` unchanged; the page marks it out of date
   and the user can click **Regenerate** when ready. Do not launch a draw subagent merely
   because the next round is ready. Explicit `visualize` and `visual-feedback` actions
   still request a draw, and Finish still reconciles the exported visual.
6. Send everything from steps 2–5 **in ONE patch**, together with
   `"agent": { "status": "waiting", "handled": <seq of this send> }`
   (the example under "Patching state.json" is this patch). One patch is one atomic swap,
   so the page sees the answers, thread replies, next round, and acknowledgement together.
   Never publish the next round in one patch and `handled` in a later one while you do
   optional work: the page uses `handled` to clear the previous question's "sent" spinner
   and enable the next Send.
7. Print exactly one terminal line, e.g.
   `grill: handled send #3 (Q2 → B, Q4 thread); round 4 has 2 questions; visual v3 out of date`,
   and return to listening.

## Interview method (frontier per round)

Interview the user relentlessly about every aspect of the topic until you share an
understanding, walking each branch of the design tree and resolving dependencies between
decisions in order:

- A question is asked only when its prerequisites are settled. Each round is the current
  **frontier**: the questions that can be asked now. Ask up to three per round when they are
  independent of each other; one when they are not. Record each question's `deps`.
- Every question has a `title`, a `body` that states what hangs on it, lettered `options`
  (two to four), and `rec` with the recommended option and a one-paragraph `why` that names
  the trade-off. A question with no sensible options has `options: []` and `rec.text`.
- If a question can be answered by exploring the codebase or the docs, explore instead of
  asking, and mention what you found in the next question's body.
- Maintain `terms` as vocabulary settles: `term`, one-sentence `def`, and `avoid` (words
  not to use for it). Use the terms consistently in later questions.
- Set `durable: true` on a question whose decision passes all three gates: hard to reverse,
  surprising without context, a real trade-off. Everything else is a routine choice.
- Stop asking when the tree is walked. Say so with `note`; do not pad with filler questions.

## Visualize

The header's **Visualize** button asks for one artifact for the whole grill, the **visual**:
a **prototype** when the topic is a user interface (a page, a panel, a flow the user clicks
through), a **diagram** otherwise (architecture, data flow, sequence, state). Decide from the
topic and the questions so far; say which in `visual.kind`; switch when feedback asks
("make this a diagram"). Questions are the source of truth and the visual is derived from
them, never the other way round. When the topic is an improvement or a feature in an
existing app, the prototype is drawn **in the context of that app**: the real page it lands
on, with the app's own chrome and styling, so it looks like what will actually ship. You
know where it lands from the grill; tell the subagent.

**You never write `visual.html` yourself; a subagent draws it.** The file runs to hundreds
of lines and is redrawn many times over a grill. Drawing it here would fill this session's
context with markup and slow every later send. You stay the interviewer: you pick the kind,
write the brief, and record the result with `patch`. The rules for the file itself live
in `$SKILL/visual-brief.md`; the subagent reads them, you do not repeat them.

Draw only for the first Visualize click, Regenerate, explicit visual feedback, or the
Finish reconcile. A requested redraw brings the visual up to date with **all** current
questions, including changes accumulated since its last version, not just the triggering
send. Ordinary interview turns only mark an affected visual stale.

Every requested draw goes like this. **The draw runs in the background and the interview
goes on**: the send that requested it is handled the moment the brief is out, so the user
keeps answering and sending while the subagent draws.

1. Stat `<session>/visual.html` (do not read it) and note its modification time; a first
   draw has none. Then launch ONE subagent with the Agent tool (it runs in the background
   and you get a completion notice later), general-purpose type, prompt filled in from this
   template (use the absolute path of `$SKILL`):

   > Draw the visual for a grill-with-ui design interview. Read `$SKILL/visual-brief.md`
   > first and follow it exactly. Session folder: `<session>`. Project root: `<project>`.
   > Kind: **prototype** | **diagram**.
   > Context: **change to an existing app**, landing in `<route, page, or component>`;
   > match that page's real look and surroundings. | **New UI**, nothing to match. |
   > **Diagram of existing code** in `<modules>`. | **Diagram of a new system**.
   > **First cut** from the questions in `state.json`.
   > — or —
   > **Redraw** of the existing `visual.html`. Change only what follows; keep everything
   > else stable:
   > - Q3 answered B: the discussion panel moves to the right third
   > - feedback: "make the sidebar collapsible"
   > Write `<session>/visual.html` and reply with ONE line saying what the visual now
   > shows (or what changed).

   One send with several triggers (feedback plus answers that change the visual) is one
   draw with all of them in the list.
2. Put the draw into the send's one step-6 patch. On a first draw:
   `"visual": { "kind": …, "version": 0, "thread": [], "stale": false, "drawing": { "seq": <seq> } }`.
   On a redraw: `"visual": { "stale": false, "drawing": { "seq": <seq> } }`;
   the merge keeps `version`, `at`, `note`, and `thread`, and the file stays as it is. The
   same patch finishes the send as usual (`agent.handled`, `"status": "waiting"`); print
   the terminal line with "visual drawing" in it and return to listening. The page reads
   `drawing`: on a first draw it stays on the questions with the header button reading
   Visualizing… and flips to the visual by itself when v1 lands; on a redraw it keeps the
   current version on screen with regenerating… in the strip. Send stays enabled
   throughout.
3. **While a draw is in flight**, handle sends normally. An answer, reopen, or changed
   recommendation that affects the visual sets `"stale": true` as usual (the in-flight
   draw did not see it). A new draw request (Visualize, Regenerate, or visual feedback)
   does not start a second subagent: reply in the thread now and append the request as
   one bullet, `"visual": { "queued": ["feedback: …"] }`. Never run two draws at once;
   both would write the same file.
4. **When the draw lands** (its completion notice wakes you): stat `<session>/visual.html`
   again (do not read it) and confirm it exists with a modification time later than the one
   you noted at launch. Then patch `"visual": { "version": <version + 1>, "note": …, "drawing": null }`
   (0 → 1 on a first draw; `note` is one line naming what changed, taken from the
   subagent's reply: "v3: discussion panel moved to the right per Q3"). Leave `stale` out
   of it. If `visual.queued` is non-empty, launch the next draw at once with those bullets
   as the change list (step 1 again), and in the same patch give
   `"drawing": { "seq": <last handled seq> }` instead of `null`, plus
   `"queued": null`. Print one line ("grill: visual v3 landed", or "… landed; drawing v4
   from 2 queued notes") and return to listening. Never bump without a new file and never let a
   new file land without a bump; the page reloads the iframe only on a bump.
5. If the subagent fails or the file did not change: on a first draw patch
   `"visual": null` and a `note` (the sentence above the question list) saying the draw
   failed and Visualize can be clicked again; on a redraw patch
   `"visual": { "drawing": null, "thread": [{ "who": "agent", "text": … }] }` saying so. Do
   not bump either way. Return to listening so the user can retry.

Background draws rely on your being the top-level session: a subagent's own background
tasks are dropped when its turn ends. If you are yourself running as a subagent, or your
harness has no subagent tool, draw the file yourself from `visual-brief.md`, inline, then
bump the version in the send's one patch.

Feedback arrives as `visual-feedback` actions (see Handling a send); sending visual feedback
explicitly requests a redraw. Answers and question discussions do not. On Finish the visual
is reconciled with the decisions and copied next to the doc.

## Terminal input

Text the user types in the terminal during a grill answers the current question when that is
unambiguous (one open question, or the text names one): record it exactly as a page send would
(`answer.kind: "text"`, or `"option"` when it is a letter, and `status: "answered"`), then
continue as in "Handling a send" from step 3. Its step 6 patch leaves `agent.handled` as it is:
there was no send. Otherwise ask which question it answers, in one line. The doc path may
also be changed this way ("write the doc to …" → patch `"doc"`).

## Finish

On a `finish` action, or when the user says finish in the terminal:

1. Write the design doc to `doc` (relative to the project root). It is exhaustive and
   self-contained, in this order: a one-paragraph summary (linking the visual at
   `docs/<slug>-visual.html` when there is one, see step 3); **Terms** (each with its
   Avoid list); **Why** (the problem in the user's words); **Locked decisions** (every
   `durable` question: the decision, the rejected options and why each lost); **Routine
   choices** (every other answered question, one bullet each); **Verified facts** (anything
   you established by exploring rather than asking, if any); **Risks**; **Deferred**
   (deferred questions, with what would reopen them); **Open threads** (discussion points
   that ended without a decision). Do not compress: a reader with no access to the session
   must be able to build from it.
2. Patch `"finished": { "doc": … }` and `"agent": { "status": "waiting" }`
   (after a page Finish this is the send's one patch, with `handled`); the page shows the
   finished banner and locks staging.
3. If `state.visual` exists, it must be reconciled with every answered question before it
   is exported. If no draw is in flight and it is not stale and nothing disagrees, copy
   `<session>/visual.html` to `docs/<slug>-visual.html` next to the doc (same folder, same
   slug, `-visual.html`) and add `"visual": <that path>` to `finished` (it is replaced
   whole, so give `doc` again, or fold it into the step 2 patch). Otherwise request one
   reconciling draw (or let the in-flight one land), return to listening, and when it lands
   copy the file and patch `finished` with `visual` then.
4. Once there is no draw in flight and the exports are complete, stop the persistent
   Monitor with TaskStop, or stop the server as described in Wait mode.
5. Print one line with the doc path (and the visual's). End.

## Wait mode (agents without a Monitor tool)

Start the server detached with its output going to a log:
`nohup node $SKILL/server.mjs serve --session <session> > <session>/serve.log 2>&1 &`.
Verify it with `url` as in Start. If the harness terminates detached children, keep `serve`
in a harness-managed running shell session instead and verify `url` again. A live page
confirms the server is running, **not** that the agent is listening.

Keep this loop active in the current agent turn:

1. On entry and on resume run `node $SKILL/server.mjs pending --session <session>` and drain
   it exactly as Resume step 3 says: every printed line in one turn, in order, following
   "Handling a send", with one patch at the end whose `agent.handled` is the last seq — not
   a patch and a new question round per queued send.
2. Run `node $SKILL/server.mjs wait --session <session> --after <agent.handled>`.
   Use the last acknowledged `handled` from your patch, not the last sequence merely seen.
   `--timeout` (default 480) bounds how long that wait *process* sits idle before exiting 3;
   it prints the send and exits the moment one lands, so a long idle timeout never delays
   delivery. It is not how long one tool call should block: if the shell tool yields a
   running process or session ID, keep that single wait alive and poll it in bounded steps
   (60 seconds or less, within the harness's limits) so user input and draw completions are
   still handled promptly. Never start a second waiter for the same session. Pass a short
   `--timeout` only when the harness cannot keep a yielded process between calls and each
   wait must run to completion in the foreground.
3. Exit 0 returns a send: handle it and acknowledge it atomically, then loop with the new
   `handled`. Exit 3 is an idle timeout: re-issue the wait. Other failures need inspection;
   recover if possible, otherwise report the inactive listener rather than silently exit.
4. When a draw completes, publish its version and return to this loop. If a wait process
   is still active, resume it. Publishing a finished prototype is not finishing the grill.

The user does not need to type "continue" in the terminal to deliver a browser Send.
Only stop under the turn-boundary conditions above. On Finish, once the doc and any final
visual are saved, stop the server using the verified `pid` in `<session>/server.json`.

## state.json

What each field means. You write it only through `patch`.

```jsonc
{
  "topic": "…", "intent": "why this grill exists, 1-2 sentences", "doc": "docs/x-design.md", "project": "/abs/path", "created": "ISO",
  "agent": { "status": "waiting|working", "since": "ISO", "handled": 3 },
  "note": "optional short sentence shown above the question list",
  "finished": { "doc": "docs/x-design.md", "visual": "docs/x-visual.html", "at": "ISO" },  // only after Finish
  "visual": {                                                   // only after a visualize action
    "kind": "prototype|diagram", "version": 3, "at": "ISO",
    "note": "v3: discussion panel moved to the right per Q3",
    "stale": false,                                            // true after relevant ordinary decisions; no redraw or version bump
    "drawing": { "since": "ISO", "seq": 12 },                  // while a draw subagent runs; version is 0 before the first lands
    "queued": ["feedback: make the sidebar collapsible"],      // draw requests that arrived during a draw; next draw takes them
    "thread": [{ "who": "user|agent", "text": "…", "at": "ISO" }]
  },
  "terms": [{ "term": "…", "def": "…", "avoid": ["…"] }],
  "questions": [{
    "id": "q7", "round": 4, "deps": ["q2"], "title": "…", "body": "…",
    "options": [{ "k": "A", "text": "…" }],
    "rec": { "option": "A", "why": "…" },                       // or { "text": "…", "why": "…" }
    "status": "open|answered|deferred|reopened", "durable": false, "updated": false,
    "answer": { "kind": "accept|option|text", "option": "A", "text": "…" },
    "explore": { "at": "ISO", "rows": [{ "option": "A", "pros": ["…"], "cons": ["…"] }] },  // after an explore action
    "thread": [{ "who": "user|agent", "text": "…", "at": "ISO" }]
  }]
}
```

Send lines (`events.jsonl`, also printed by `serve`):

```jsonc
{ "type": "send", "seq": 12, "at": "ISO", "session": "/abs/session/folder", "actions": [
  { "q": "q15", "type": "answer", "kind": "accept|option|text", "option": "A", "text": "…" },
  { "q": "q8",  "type": "thread", "text": "…" },
  { "q": "q17", "type": "defer" }, { "q": "q3", "type": "reopen" }, { "q": "q9", "type": "explore" },
  { "type": "visualize" }, { "type": "visual-feedback", "text": "…" },
  { "type": "finish" } ] }
```
