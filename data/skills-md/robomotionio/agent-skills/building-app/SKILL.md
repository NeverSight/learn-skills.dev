---
name: building-app
description: "Builds a Robomotion App - a real React web app in front of a robot flow - by conversation with a non-technical person. Owns the full lifecycle: clarify → contract (app.json) → screens with app-kit → the flow behind them → run it on the app's robot → use the app in a browser and fix until it works → publish. Use when the user wants an app, dashboard, portal, form, approval queue, a board of things that move through stages, or any screens people will click."
triggers: [an app, the app, my app, web app, webapp, a dashboard, dashboard for, approval queue, internal tool, a portal, user interface, a screen where, a page where, a form for, a form where, little app, small app, simple app, /\bapps?\b/, /\bdashboards?\b/, /\bportals?\b/, a pipeline, kanban, a board where, drag and drop, /\bpipelines?\b/]
---

# Robomotion App Builder

A Robomotion App is two halves in ONE git repository, built by talking to you:

- the **screens**: a React app under `app/`, composed only from `@robomotion/app-kit`
- the **robot's side**: a Robomotion flow (`main.ts`, `subflows/`) that answers every button, one `App Action` trigger per action

They are joined by one file, **`app.json`**, and talk over a typed action-RPC. The robot is the differentiator: this app can open a browser, drive a desktop program, read a PDF, keep its own database.

Two things decide whether this goes well: **how fast the person sees the first screen**, and **whether your words leak jargon**. Everything below serves those two. This skill is a thin index over `./docs/` - read the relevant doc when the topic comes up.

**What you need:** the `robomotion` CLI on PATH (it brings `robomotion-sdk-mcp`, `robomotion-api-mcp` and `robomotion-browser-mcp` with it), `bun`, `git`, and a Robomotion login (`robomotion auth login`). Nothing else: no Designer, no other MCP server. Under Robomotion's own **Build with AI** the same steps are tools instead of commands - read `./docs/build-view.md` there and only there.

## The contract is the spine

`app.json` at the project root is the **single source of truth** for actions, events, types, and screens. The project is one folder - the flow's - and the screens live in `app/` inside it. Typegen ripples every change into both halves:

```
app/src/generated/actions.gen.ts     ← SPA: typed client + CONTRACT_HASH
src/generated/actions.gen.ts         ← flow: param/result types per action
```

Any behavior change starts in `app.json`, then regenerate, then touch screens and flow. Changing `app.json` without regenerating leaves both sides referencing types that no longer exist, so `tsc` fails inside `validate_app` before anything ships. **Drift is a compile error, never a runtime surprise.** The `contract_hash` is embedded in the SPA at build time and computed by the robot at startup; a mismatch renders a blocking "this app was updated, reload" state, never silent talking-past-each-other. Authoring guide: `./docs/contract.md`.

### When the shape is open, say so

Not every payload has fields you can name, and inventing some is worse than
admitting it. Two spellings are legal in `app.json` and both generate a usable
type:

| Written as | Means | The screen gets |
|---|---|---|
| `"params": { "type": "object" }` | any object | `Record<string, unknown>` |
| `"result": { "type": "object" }` | any object | `Record<string, unknown>` |
| `"result": {}` | any value at all | `unknown` |

Reach for one when the payload really is open:

- **A pass-through payload** the screen assembles and the flow hands straight
  on - to a webhook, a spreadsheet row, another system's API.
- **A dynamic form**, where the fields are not known when you write the app.
  The kit's `JsonInput` parses what the person typed and hands the form a real
  object, so `<Form action={run}>` sends it as the params.
- **A result the flow decides**: a report, a lookup against a system whose
  response shape is not yours. The kit's `JsonView` renders it without the
  screen knowing its shape.

Still write the `description` - it is all the person, the Designer and an MCP
client have to go on. The call site is unchecked, so `run({ ...payload })`
compiles; that is the point, and also the cost, so **type what you know, open
what you don't**. An action with three known fields and one free-form bag
declares the three and puts the bag in a property; it does not open the whole
thing. `additionalProperties` is not in the subset and is not needed: the open
object is exactly `{ "type": "object" }`.

## The surface: the `robomotion` CLI, and git

One project, one folder, one save. The layout:

- `app.json` (and `mcp.json`) at the project root - the contract, where the robot reads it.
- `main.ts` and `subflows/` at the root - the robot's side.
- `app/` holds the screens: `app/package.json`, `app/src/`, the two Robomotion packages under `app/vendor/`.
- `src/generated/` on both sides (`src/generated/actions.gen.ts` for the flow, `app/src/generated/actions.gen.ts` for the screens) is codegen-owned; never hand-edit it.
- `.robomotion/` holds this machine's session files (never committed): the robot, the dev server, `checks.json`, and your `request-checks.md`.

| Command | Does |
|---|---|
| `robomotion auth login --workspace <host>` | signs THIS PROJECT in (the login is kept in `.robomotion/session.json` at the project root, never committed): a code and a link, approved in the person's browser. Each project folder has its own login, so several assistants can build apps in different workspaces side by side. Run `robomotion auth whoami` in the project folder first; if it says not logged in, see step 0 - you run the login, the person only approves it. Never ask for a key. |
| `robomotion create app "<name>"` | the start of a NEW app: makes the project folder (a slug of the name; `--dir <path>` to choose), signs it in when it is not (the browser approval below; `--workspace <host>` when the person named one), creates the flow and the app, pulls the seeded `app/`, places the packages, installs. Then `cd` into it. |
| `robomotion app create "<name>"` | the same, in place, on an EXISTING flow checkout (a `git clone` from its Home card) that has no app yet. |
| `robomotion app sync` | for an app that already exists: pull, place the packages, install |
| `robomotion app codegen` (from `app/`) | regenerates both typed clients from `app.json` and prints the contract hash |
| `robomotion app dev` | runs the screens and prints two addresses: localhost, and the app's preview address - the one Robomotion's Build view shows, so the person can watch the same live screens from the Designer while you work. Start it in the background; it keeps running. |
| `robomotion app link` | a link that opens the preview in any browser, for members of the workspace (it expires in minutes; the browser keeps the preview after that) |
| `robomotion app validate` | every check: schema, `tsc` on both halves, contract hash, the flow's wiring, the kit rules |
| `git add -A && git commit -m "..." && git push` | the save, at the project root - screens and flow together |
| `robomotion app robot` | gives the app its own robot (only after the person said yes) |
| `robomotion app start [--restart]` | brings that robot up on this computer and starts the app on it; `--restart` after a save that changed the flow |
| `robomotion app smoke` | presses every button once through the app's own door and reports what each answered |
| `robomotion app press <action> --params '{...}'` | presses one button with values you choose |
| `robomotion app try --screen "<label>" --fill "Label=value" --select "Label=option" --click "Button" --expect "text"` | uses the app the way a person does, in a headless browser signed in as them, and prints what the screen shows and what the robot did |
| `robomotion app screen "<label>"` | reads what a screen shows (text and console errors) |
| `robomotion app logs [-f]` | the robot's output: every step it ran, and the error when one failed |
| `robomotion app status` | the app, the screens, the robot, what was last checked |
| `robomotion app publish` | builds the screens, cuts a flow version, publishes - only when asked |

Results come on stdout; progress and complaints on stderr.

## The loop

Narrate progress with the task list, in the person's language ("Design the review screen", "Teach the robot to read invoices") - never internal steps ("run typegen", "start dev server"). Ask questions with the question tool (AskUserQuestion in Claude Code), one per turn, with short options.

0. **Create the project.** A new app starts with one command, in the folder the person wants the project under (never inside another project):

    robomotion create app "<short human name>"

   **Run it in the background**: when the folder is not signed in yet, it opens the person's browser on the approval page, prints a short code, and waits for the approval - a foreground run would hold your turn. Tell them in one sentence: "A Robomotion sign-in page has opened in your browser - approve it (the code is XXXX-XXXX)." Which workspace: the one their browser is signed in to, so ask nothing - unless the person named one, then pass `--workspace <host>` (the full host, like `acme.robomotion.io`). When it returns, `cd` into the folder it made (it says which); everything after runs there, and the folder's own `.robomotion/session.json` is its login.

   **Only if the sign-in cannot open a browser** - the output says no browser was opened (a server with no desktop, a remote shell) or the person says nothing opened - run it again with `--no-browser` and guide them: give the address and the code it prints, to open in any browser where they are signed in to Robomotion.

   Never write app or flow files before the command has returned: there is nothing to write into until then. An existing flow checkout that has no app yet: `robomotion app create "<name>"` inside it (same sign-in rule, `robomotion auth whoami` first). Continuing an existing app: `robomotion app sync`.

0b. **Clarify - at most 3 questions, total.** ONE question per turn. Worth asking: who uses this, what is the one main job, where does the data live today. Never ask about technology, hosting, colours or frameworks. If the request already answers a question, don't ask it.

0c. **Find the robot's pieces before you design anything.** For every external system or capability the person named - their CRM, their shared drive, a spreadsheet, a mailbox, a database, a website with no API - use the **`searching-packages`** skill BEFORE you choose an archetype or write a line of `app.json`. The Robomotion library is 229 packages deep and the flow behind an app can reach all of it. **A package beats raw HTTP** every time. Name what you found in your reply, in the person's words ("I can talk to your Google Sheet directly"), never as a package list.

0d. **Write the promises down.** Before any screen, write what the person asked for as short checkable lines in `.robomotion/request-checks.md` (their language is fine): counts, order, what an empty case shows, what is refused and what stays unchanged when it is, what each screen shows - naming each screen by the label its navigation will carry. Step 7 checks the screens against it. Never mention the file to the person.

1. **Pick an archetype silently**: dashboard / approval-queue / form-and-table / document-review / board. Match by what the person wants to DO - the chooser is `./docs/archetypes/` (one file per archetype). Never say the archetype's name; say what you're building: "I'll make you an app with two screens: a queue of waiting invoices, and a page to approve each one." **Layout follows the screen count**: two or more screens get the kit's sidebar (give each screen an `icon`, and a `group` when there are more than five); a one-screen app the top bar. "Tabs at the top" is `theme.layout: "topbar"` in `app.json`.

2. **Write `app.json`** - read `./docs/contract.md` first. Every `description` doubles as UI copy, so write it for the end user. Then `robomotion app codegen` from `app/`.

2b. **Clear out the demo the app arrived with.** A new app already renders something, written against the seed's contract. Your `app.json` deletes those types, so **any leftover demo file fails `tsc`, including one nothing imports**. After writing your screens, ask the checkout what still points at the contract:

    grep -rl "generated/actions.gen" app/src/

    Anything listed that you did not write is debris: delete it. `app/src/screens.tsx` says which screens the app mounts; anything unreachable from there goes too.

2c. **Write `mcp.json` beside `app.json`** - read `./docs/mcp.md`. Every app is also an MCP server and has an assistant in its corner; `mcp.json` is how both understand it. Presentation only: a name, an `instructions` paragraph, a sentence per tool, `"read_only": true` or `false` on EVERY tool (`robomotion app validate` fails one without it; run `robomotion app codegen` again after it changes), and the `destructive` / `idempotent` hints. Keep an action an agent must never run out of it with `"enabled": false`. Never put schemas in it.

3. **Generate the screens from the archetype, with sample data baked in.** The
   app's name belongs to the shell's title and nowhere else on a screen: a
   screen's title is what that screen does, a card's title is what the card
   holds. A one-screen app that repeats its name on the shell, the screen and
   the card reads as a template, not as somebody's app. Copy the archetype's screen structure, compose it from `./docs/app-kit-reference.md` components, and fill tables and cards with realistic sample rows declared as a `SAMPLE_*` const at the top of each screen file. The screens must render fully before any backend exists - a person who sees their app in the first minutes stays in the conversation; one who waits for a backend leaves.

3a. **Sample data is a FALLBACK, never a switch. Every button is wired to its
   real action from the first draft.** Write the sample rows as what the table
   shows when there is no answer yet:

   ```tsx
   const rows = search.data?.matches ?? SAMPLE_MATCHES;   // yes
   <Form action={search} ...>                             // always the real one
   ```

   Never a mode constant, and never anything that makes the action
   conditional:

   ```tsx
   const SAMPLE_MODE = true;                              // NO
   <Form action={SAMPLE_MODE ? undefined : search} ...>   // NO - dead button
   ```

   A mode flag leaves a button that submits nothing for ever, and `tsc` passes
   it, because nothing about an unwired button is a type error. `robomotion app validate`
   reports the shape (`screens-wired`); the person finds it sooner, by pressing
   it, and by then it is their app.

   There is nothing for a mode flag to do. Before a session exists the kit
   already shows "Not connected to your robot yet. The screens below show
   sample data." at the top of the app, and an action that cannot reach a
   robot fails honestly and says so. A wired button on a draft app is correct;
   an unwired one is a mockup you will tell somebody is an app.

   **That banner is the kit's, so do not write it a second time.** An
   `<Alert title="Sample data">The screens below show sample data until the
   robot is connected.</Alert>` on the screen says exactly what the banner
   two inches above it already says, and the person reads the same sentence
   twice before they read anything about their app (2026-09-09, the
   earthquake app's first screen). Say nothing; the banner has it.

   **And the sample answer goes the moment the robot is connected.** The
   banner that explained it goes with the connection, so a sample result
   left on a connected app reads as a real answer to a form nobody has
   filled in. Gate the fallback on the connection, which `useConnection()`
   reports (`robomotion app validate`'s `sample-gated` check fails a fallback that is
   not):

   ```tsx
   const { state } = useConnection();
   const rows = search.data?.matches ?? (state === "ready" ? [] : SAMPLE_MATCHES);
   ```

   Connected and no answer yet is the EMPTY state ("Type a topic and press
   Search"), never the sample one.
3b. **Every view that waits on the robot renders THREE states, always: loading,
   empty, and failed.** Not two. The runtime times a call out after 30s and
   rejects the promise; if the screen has nowhere to put that rejection, the
   person is left with a spinner that means "broken" and reads as "nearly
   there" - no message, no retry, nothing to say that what they are waiting
   for is never coming.

   Use the kit's `ErrorState` for the failure and `EmptyState` for "nothing
   here yet" (`./docs/app-kit-reference.md`), and give the failure a button
   that tries again. A screen where the loading branch is the only branch is
   not finished.

   **The failure sits BESIDE the table, never in its place.** `ErrorState`
   renders nothing when the connection banner has already said the same thing
   (the robot is not connected), so `{list.error ? <ErrorState/> :
   <DataTable/>}` leaves a form with nothing under it the moment the robot
   is unreachable - no table, no sample rows, no error. Write
   `{list.error && <ErrorState/>}` and then the `DataTable` unconditionally.

3c. **A screen asks for what it shows when it opens, and a row button is a column.** A table with `source={{ action }}` loads itself; every other list, counter or detail runs its read in one `useEffect` on open, and a form that adds a record refetches the list that shows it. A button the person asked for on every row is rendered as a column, not folded into the table's "More" menu. Both are under `DataTable` in `./docs/app-kit-reference.md` ("Loading a screen", "A button on every row").

4. **Start the screens and look.** `robomotion app dev` in the background, once; it prints the local address. After every batch of screen edits, `robomotion app screen "<label>"` on the screen you touched: it prints the text and the console errors, and a screen that throws on first render is caught here, not by the person. Give the person the address when they ask where the app is.

4b. **`robomotion app codegen`** whenever `app.json` or a `read_only` mark in `mcp.json` changes, before writing code against it. Run it from `app/`.

5. **Build the flow, one action at a time**, in the order the person will press them. For each action: `App Action` trigger → the real work → `App Respond` on EVERY path (an unresponded call only ends by timeout, which the person experiences as a hung button). Long work sends `App Progress`. `src/generated/actions.gen.ts` at the project root gives you the param/result types. Flow SDK mechanics (node grammar, browser, credentials) are the `creating-flow` skill - use it. The exact shape of an app's flow is the next section; read it before the first node.

5b. **Check and save.** `robomotion app validate` until it passes, then `git add -A && git commit -m "<what changed>" && git push` at the project root. The robot fetches the flow from git: an uncommitted flow is a flow the robot has never seen.

6b. **Press every button, then read the report before you say anything works.** After
   every `robomotion app start` (and every `--restart`), run `robomotion app smoke`
   yourself - nothing runs it for you: every button pressed once through the app's
   own MCP door - the same `action_call` a press in the screens sends - with
   stand-in values built from each action's schema (a description's own
   example first, then an enum's first member, today for a date, "smoke test"
   / 1 / true otherwise). The report has one row per button, and the row's word is the
   whole diagnosis. Classify, then act - never explain:

   | Row says | It means | Do this |
   |---|---|---|
   | `answered` | The path reached an `App Respond` (or `App Respond Error`). `result` holds what came back. | Read `result`. An answer that says the stand-in values were not understood ("that doesn't look like a country code") proved only the rejection path - press it yourself with `robomotion app press` and real values before you call the button working. |
   | `refused` | `invalid_params`: the stand-ins were the wrong shape; the path behind the check is untested. | `robomotion app press` with values you choose, and say which case you proved. |
   | `dead_end` | The robot's watchdog fired: the path from that `App Action` never reaches an `App Respond`. `last_node` is the last step that started and never finished. | Open the flow, find `last_node`, wire the path from it through to an `App Respond` (a port that goes nowhere, a chain nothing enters, a branch with no answer). Save, `robomotion app start --restart`, `robomotion app smoke` again; read that report too. |
   | `unwired` | No `App Action` node serves this action. | Add `Robomotion.Apps.Action` with this action name, wire its path to an `App Respond`, save. |
   | `stale` | `contract_mismatch` / `unknown_action`: the running backend is older than `app.json`. | Save the flow and call `robomotion app start` again. |
   | `dead_after_first` | The first press answered and the second found nothing running: the flow ended itself. | Hard rule 5. Remove the `Stop`/`End`, or the path that reaches one; wire `Core.Trigger.Catch` to an `App Respond Error`. Save. |
   | `not_running` / `still_starting` | The flow is not up, or never loaded its contract. | `robomotion app start` once more; if it says the session is up, read `robomotion app logs` for why the flow ended, say so, and end your turn. |
   | `busy` / `slow` / `error` / `skipped` | Nothing proven either way. | Say nothing alarming about the buttons; `robomotion app press` the one that matters if you need to know. |

   **Never say a button works that the report says did not answer** - and
   never say the app is ready over a `failed` verdict. Write actions ARE
   pressed, for real, and the pass takes its own creates away again through
   the app's delete when there is one. `left_behind` names a create it could
   not remove: add a delete for that record (contract, flow, screen), save,
   restart, smoke again. Take away only what the pass or your own presses
   made (`created_ids`, the ids your `press` calls returned) - never a record
   you read from a list, never one the person entered. An update
   (`updated_existing`) is not a leftover; leave it. Reading `last_node` beats
   every theory you have about why a press timed out (the twenty-sixth pass
   spent twenty-one minutes on a confident wrong one).

6a. **When the app has no robot of its own yet - a brand-new app never does,
   and `robomotion app start` says so if you call it anyway - the question is a
   CARD, not a sentence.** This is the last question of the build and it
   arrives at the end of a long summary, where a sentence ending in a question
   mark leaves the person nothing to press. Call the question tool. Exactly
   this shape:

6d. **Prove the paths the stand-ins could not, with real values.** `robomotion app press <action> --params '{...}'` for the refusal ("not enough left"), the second page, the empty case. Read `robomotion app logs` when a press does not answer as you expect, BEFORE explaining anything: the failing step and its message are there in the robot's own words.

7. **Use the app the way the person will, and check every promise.** With `robomotion app dev` running and the robot up, for each screen `.robomotion/request-checks.md` names, drive it as a person:

    robomotion app try --screen "Items" --fill "Name=Rice" --fill "Unit=kg" --click "Add item" --expect "Rice"
    robomotion app try --screen "Movements" --select "Item=Rice (kg)" --select "In or out=Out" --fill "Quantity=8" --click "Save" --expect "only"

   It fills fields by their labels, presses buttons by their words, then prints the screen's text, the page's console errors, and every step the robot ran meanwhile. Check every line of `request-checks.md` against what the screen shows - reading a screen is not checking it. A fix to what a screen shows is confirmed by reading that screen again, never only by pressing the action. Fix any mismatch, save, restart when the flow changed, try again. Take away the records your tries made before you hand over, through the app's own delete.

8. **Hand over, honestly.** Say what the app does and what to press, in the person's words; give them a link from `robomotion app link` (it opens anywhere), or the local address when they are on this computer; and tell them they can also open it in Robomotion: opening the flow there opens Build with AI with the app, and while `robomotion app dev` is running the screens show in its panel. Save first (`git add -A && git commit && git push`) so what they open is what you built. Say nothing about ids, files or test data unless something was left behind. **Offer to publish; never publish unasked.** When they say yes, `robomotion app publish`.

### The flow side, exactly

**One subflow per screen. `main.ts` is a table of contents, nothing else.**

This is a hard rule, and it is about the person, not about tidiness. An app's
backend grows one chain per action, all on one canvas: four screens came to ten
unconnected chains stacked down a single surface, thirty nodes wide, and
nothing on it said which row belonged to which screen (thirty-sixth pass). The
person WILL open that canvas - it is their robot - and what they see decides
whether they believe they own this app or are merely allowed to use it. Every
screen you add makes it worse, and nobody ever goes back and splits it up.

So, every time:

- **`main.ts` holds only `Core.Flow.SubFlow` nodes - one per screen - and the
  app's single `Core.Trigger.Catch`.** Nothing else lives there. Read top to
  bottom, `main.ts` is the app's screen list.
- **Every action a screen owns lives in that screen's subflow file**
  (`subflows/<6-hex>.ts`): its `App Action` trigger, its work, its
  `App Respond`, its refusal branch, its own `Label`/`GoTo` pairs.
- **Name the subflow exactly what the person sees in the sidebar** -
  `subflow.create('Problems', ...)`, not `subflow.create('listIssues', ...)`.
  The canvas then labels each box with their own word for it.
- **Every screen's `Core.Flow.SubFlow` node is written with
  `{ optHidePorts: true }`** - `f.node('b2d4e1', 'Core.Flow.SubFlow',
  'Problems', { optHidePorts: true })`, never `{}`. A screen is entered by
  `App Action` and left by `App Respond`, so the node's input and output
  ports and the `Begin`/`End` inside are never wired; this option tells the
  Designer not to draw them, and the person's canvas shows one clean box per
  screen instead of ports that go nowhere. It is cosmetic and Designer-only:
  the robot ignores it, and `Begin`/`End` are still written (below).

**Screens inside screens nest the same way.** When pressing a row opens a
detail screen, that screen is a subflow called *from its parent's subflow*, not
from `main.ts`, and its name carries the path:

```
main.ts
├── SubFlow 'Check'                    → subflows/a1c3f0.ts
├── SubFlow 'Problems'                 → subflows/b2d4e1.ts
│     └── SubFlow 'Problems / Detail'        → subflows/c3e5f2.ts
│           └── SubFlow 'Problems / Detail / History' → subflows/d4f6a3.ts
├── SubFlow 'Pages'                    → subflows/e5a7b4.ts
└── Catch 'Say What Went Wrong'
```

A person on the Detail screen looking for what it does finds one box called
'Problems / Detail'. That is the whole point: the flow reads as the app's own
navigation.

**The cost, which you pay without complaining.** A subflow file's name IS its
calling node's id, so one subflow is called from exactly one place - which is
precisely what one-screen-one-subflow needs, so the rule and the runtime agree.
But it also means a step several screens share (open the database, make sure
the tables exist) CANNOT be one subflow called from five: write those four
nodes into each screen's subflow. Do not try to call a subflow twice, do not
flatten the app back onto one canvas to avoid repeating them. Four repeated
nodes are cheaper than a canvas nobody can read.

**This overrides `creating-flow`'s "do not use a subflow for fewer than three
nodes".** There, the unit is the node; here it is the screen. A screen with one
small action still gets its own subflow.

The general node grammar belongs to `creating-flow`, but these seven types ship
only in this package, and hunting for them costs a search round every build.
`f.node` takes the **type**, never the display name:

| Type | Shows as | What you actually set |
|---|---|---|
| `Robomotion.Apps.Action` | App Action | `optActionName` - the action's name in `app.json` |
| `Robomotion.Apps.Respond` | App Respond | nothing; it answers with `msg.result` |
| `Robomotion.Apps.RespondError` | App Respond Error | `optCode`, `optRetryable`, **`inMessage`** - the sentence the person reads, see below |
| `Robomotion.Apps.Progress` | App Progress | `optPercent` |
| `Robomotion.Apps.EmitEvent` | App Emit Event | `optEventName`, `optAudience` |
| `Robomotion.Apps.GetFile` | App Get File | `optDownloadDir` |
| `Robomotion.Apps.SaveFile` | App Save File | nothing |

One complete action, start to finish. It is always two files: `main.ts` names
the screen, and the screen's subflow file holds the action.

```ts
// main.ts - the package, one SubFlow node per screen, the catch-all (below)
import { flow, Message } from '@robomotion/sdk';

flow.create('<flowId>', '<Flow Name>', (f) => {
  f.addDependency('Robomotion.Apps', '0.3.3');

  f.node('b2d4e1', 'Core.Flow.SubFlow', 'Problems', { optHidePorts: true });
}).start();
```

```ts
// subflows/b2d4e1.ts - the file name is the SubFlow node's id
import { subflow } from '@robomotion/sdk';

subflow.create('Problems', (f) => {
  f.node('e1a7c3', 'Core.Flow.Begin', 'Begin', {});
  f.node('f2b8d4', 'Core.Flow.End', 'End', { sfPort: 0 });

  f.node('a3c1f9', 'Robomotion.Apps.Action', 'Search Call', { optActionName: 'search' })
    .then('b8e274', 'Core.Programming.Function', 'Do The Work', {
      func: 'msg.result = { hits: [] };\nreturn msg;',
    })
    .then('c4d952', 'Robomotion.Apps.Respond', 'Send Results', {});
});
```

**Every subflow MUST have its `Core.Flow.Begin` and `Core.Flow.End`, and in a
screen's subflow they stand alone, connected to nothing.** `creating-flow`'s
subflow rule stands: write both. What differs in an app is that nothing needs
to enter through `Begin`. `App Action` is already a trigger: it has no input
port (0 inputs), so it is always the FIRST node of its chain, written with
`f.node(...)`, and nothing is ever `.then()`ed into it. `Begin` chained into
`App Action` does not compile: `Cannot chain to node '<id>'
(Robomotion.Apps.Action): it has 0 inputs`. So:

- `Begin` and `End` are two lone `f.node(...)` lines at the top of the file.
  Do not wire `Begin` to the action, and do not wire the action's path to
  `End`: the path ends at its `App Respond`.
- A screen with two actions has two `f.node(...)` chains in its subflow file,
  each starting at its own `App Action`.
- Steps an action needs first (open the database, make sure the tables exist)
  go AFTER its `App Action`, never before it.
- A sub-screen's `Core.Flow.SubFlow` node sits in its parent's subflow file the
  same way it sits in `main.ts`: its own `f.node(...)`, chained to nothing.
- **Every screen's `Core.Flow.SubFlow` node gets `{ optHidePorts: true }`**, in
  `main.ts` and in a parent screen's file alike. It is a Designer-only cosmetic
  option: the node's input/output ports and the lone `Begin`/`End` inside are
  not drawn, because nothing is ever wired to them in a screen. The robot
  ignores it, and the `Begin`/`End` lines above are still written.

**`f.addDependency('Robomotion.Apps', '0.3.3')` goes in `main.ts`, once.** The
subflow files use the main flow's packages, and `main.ts` needs it anyway for
the catch-all's `App Respond Error`.

The caller's arguments arrive as **`msg.params.<field>`**; the answer is whatever
sits on **`msg.result`** when `App Respond` runs. Both shapes are already typed
for you in `src/generated/actions.gen.ts` at the project root.

**An action that makes a record answers with that record's `id`.**
`{ id, ...whatever else the screen needs }` - `{ id: 'mv17...', balance: 17 }`,
never `{ balance: 17 }` alone. The id is how the screen points at the row it
just added, how the checks after a save know which row the press made, and
how that same row is taken away again; a create that answers without it
leaves a row nobody can name. Declare `id` in the action's `output` in
`app.json`.

**And the catch-all, in `main.ts`, every time.** An unhandled error ends
the flow and the app with it (hard rule 5), so every backend has a
`Core.Trigger.Catch` wired to an `App Respond Error`. This is the whole of it -
there is nothing to look up in `creating-flow` for it:

```ts
  f.node('d5e061', 'Core.Trigger.Catch', 'Say What Went Wrong', {
    optNodes: { all: true, ids: [], type: 'catch' },
  })
    .then('e7f2a8', 'Robomotion.Apps.RespondError', 'Tell Them The Problem', {
      optRetryable: true,
      inMessage: Message('error.message'),
    });
```

`Catch` is a second trigger beside your `App Action` nodes (a separate
`f.node(...)` chain, never `.then()`ed after anything), `optNodes` as written
catches every node, and `msg.error.message` is the thrown error's own text.

**Once, in `main.ts`, and not again in the screens.** The robot scopes a
Catch to the file it sits in: a catch-all in `main.ts` covers the main flow
and every error a screen's subflow leaves uncaught, because an uncaught error
climbs to the parent until a Catch takes it, and stops there. So the one in
`main.ts` is the safety net for the whole app, and a screen's subflow file
does NOT get a copy of it. A second "Say What Went Wrong" pair in every screen
says nothing the net does not already say, and it is noise on the person's
canvas. A screen adds its own Catch only when it has something of its own to
say: different words or a non-retryable answer for that screen (`all: true`
inside the screen's file covers that screen's nodes only), or a Catch on the
`ids` of one lookup so the action can answer with words about that lookup.
The `main.ts` catch-all stays either way.

`App Action` is a trigger, so it has no input port and the validator reports it
as an unreachable node. `App Respond` and `App Respond Error` end a path, so it
reports them as dead ends. Both warnings are expected on every app. Never
restructure the flow to silence either.

**`App Respond Error` needs a message.** Its message input defaults to empty,
and an empty one puts a title and a Try again button on screen with nothing
between them - a person told that something failed and never told what, while
the reason sits in the robot's log. Give it the reason, in the words the
person would use:

```ts
.then('f9a4c6', 'Robomotion.Apps.RespondError', 'Say What Went Wrong', {
  optRetryable: true,
  inMessage: Message('error.message'),   // the caught error, or better:
})
```

Better still on a branch you can predict, write the sentence yourself -
`inMessage: Custom('Those percentages are the wrong way round.')` - because the
error text was written for you and the message is read by them. Never pass a
raw stack: `Error: x at main (main.js)` on a screen is a bug report, not an
answer.

**A refusal is a branch, never a `throw`.** "Not enough left in the tin",
"no copies on the shelf", "that date is in the past" - anything the flow can
foresee is the app WORKING, and it goes: a Function node that sets a flag
(`msg.refused = 'The tin only has £5.00 in it.'`) → a `Core.Flow.Switch` on it
→ `App Respond Error` with that sentence on the refused side, the real work on
the other.

**When a Function decides by itself (`outputs: 2`), the path that goes on is
output 0.** `.then()` always continues from output 0, so write the check as
`return [msg, null]` for "carry on" and `return [null, msg]` for "refuse", chain
the real work with `.then()`, and send the refusal from output 1:
`f.edge('<check id>', 1, '<App Respond Error or GoTo id>', 0)`. The other way
round - refusing on output 0 and chaining the work with `.then()` - puts both on
output 0 and wires the real path to nothing, so every good press is dropped
and the screen waits until it times out. `robomotion build` refuses that shape
(`a Function sends a message out of an output that goes nowhere`).

A `throw new Error(...)` caught by the Catch gets the same words to
the screen, but it also paints a red "Node Execution Error" on the person's
canvas and an `error` line in the robot's log every time somebody is told no -
and they will open that canvas and ask whether their app is broken. Reserve
`throw` for what you did not foresee.

**A wire that crosses other rows is a `GoTo`, not an edge.** An app flow is
one row of nodes per action, stacked. The refused side of an action's Switch
goes to that action's `App Respond Error`, and there are usually two or three
branch points feeding it from different places in the chain. Written as
`f.edge(...)` into a node declared after the chain, the layout puts that node
rows away and draws a wire diagonally across every action in between - once
per branch. Open a four-action app built that way and the canvas is a cat's
cradle; the person WILL open it, and they will ask whether their app is broken.

`Core.Flow.Label` and `Core.Flow.GoTo` are the answer, and they are not only a
loop construct. A `GoTo` has no outgoing wire at all - it jumps - so the long
edge stops existing rather than being redrawn shorter:

```ts
// Beside the node it guards. Nothing is ever wired INTO a Label: it has no
// input port, and a GoTo is how you arrive.
f.node('7a1b0b', 'Core.Flow.Label', 'Refused', {});
f.node('7a1b07', 'Robomotion.Apps.RespondError', 'Say Why', REFUSE_ERR);
f.edge('7a1b0b', 0, '7a1b07', 0);

// On each branch point, in its own row, a short hop to a GoTo sitting there.
f.node('7a1b0c', 'Core.Flow.GoTo', 'Say Why', { optNodes: { ids: ['7a1b0b'], type: 'goto', all: false } });
f.edge('7a1b06', 1, '7a1b0c', 0);
```

The rule: **if an edge would span more than about two rows, make it a `GoTo` to
a `Label`.** Name the GoTo after where it goes ("Say Why"), so the row still
reads left to right and nothing is hidden. `Core.Flow.Goto` with a lowercase T
is not a registered type - the capital in `GoTo` is load-bearing.

An action that calls a website uses `Core.Net.HttpRequest`, which is not in this
package and is the one node worth naming here so you do not spend a search
round on it.

**`outBody` is only parsed when the server says `application/json`.** Plenty of
real services return JSON under another content type (`text/javascript`,
`text/plain`), and then `msg.response` is a **string**, `msg.response.items`
is `undefined`, and your not-found branch fires on every single query. Nothing
errors: the robot's log shows every step finished, the screen politely says
nothing matched, and the person believes the search is broken rather than the
app. Parse defensively, always:

```ts
.then('d8f317', 'Core.Programming.Function', 'Build The List', {
  func: `var data = msg.response;
if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { data = null; } }
// ... now read data.results
return msg;`
})
```

And when a search legitimately finds nothing, say which it was: an empty answer
from the service and an answer you could not read are the same screen otherwise.

**A not-found is a status code you can name, not "anything but 200".** Some
services answer a miss with a `404` and a JSON body rather than an empty list,
so the not-found branch has to read the status - and the moment it does, the
easy shape is `if (status === 200) { ...rows } else { ...nothing matched }`,
which quietly tells the person their word, their part number or their postcode
does not exist every time the call times out, the service is down, or the key
is wrong. Those are three different sentences and only one of them is theirs
to fix. Name the codes that mean not-found and let the rest be a failure:

```ts
func: `var status = msg.httpStatus;
msg.failed = '';
if (status === 404) { msg.result = { found: false, message: 'Nothing matched that.' }; return msg; }
if (status < 200 || status >= 300) {
  msg.failed = 'The service is not answering just now (' + status + '). Try again in a minute.';
  return msg;
}
// ... 2xx: read the body, and an empty list is ALSO found:false
return msg;`
```

Both of those are branches, not throws, by the rule above: `msg.failed` goes to
a `Core.Flow.Switch` and out through `App Respond Error`, so the person gets a
sentence and the canvas stays green.

Give the call room, too. `optTimeout` is in seconds and a public service on the
other side of the world is regularly slower than it looks from here: a timeout
set to about what the call takes today is a coin flip, and the side it lands on
is a wrong answer on the person's screen. Sixty seconds costs nothing when the
answer arrives in two.

**A row that lacks what the person asked for is not a match.** Public indexes
mix kinds of record - datasets and books beside papers, comments beside
stories, albums beside songs - and the first rows a search returns are often
not the kind the person named. Two things, both every time:

- **Ask the service for the kind the person named** when it can be asked - a
  type filter, a tag, an entity parameter - and prefer an index whose records
  are that kind over one that mixes them.
- **Drop a row that is missing a column the person asked for**, and ask for
  more rows than you show so the ten on screen are ten real ones. A cell
  reading "Not listed" in every row is this rule skipped, and a person reads
  a table whose first rows are blanks as a search that does not work.

### Remembering something: the flow owns the storage

An app that has to remember - a list somebody adds to, a queue that survives a
reload, last month's numbers - keeps that data in a database its own FLOW owns.
`Robomotion.SQLite` is the default when the data belongs to this app and this
robot; when it is bigger, or shared with something else, or already lives
somewhere, it is one of the database packages (Postgres, MySQL, MongoDB, Google
Sheets and the rest) and `searching-packages` is what finds it - the same step
0c you ran before writing `app.json`. An app is bounded by exactly two lists of
what it may use - `@robomotion/app-kit` on the screens, the Robomotion package
library behind them - and storage is not a third one: it is one more package the
flow calls, like every other system the flow reaches.

Open a SQLite database by a full path built from the home folder, in a
Function, and **put the app's own id in the file name**:
`msg.db = 'Data Source=' + global.get('$Home$') + '/<app name>-<first 8 of app_id>.db;Version=3;'`,
then `Message('db')` on the SQLite nodes. The id is what keeps two apps
apart: a person who builds "Pantry Stock" twice gets two apps, and a file
named only after the app hands the second one the first one's tables -
`CREATE TABLE IF NOT EXISTS` sees them, keeps them, and every query then
fails on a column the old table never had (seen live, 2026-09-14). Never a
relative `Data Source=app.db` either: the robot runs the package inside its
own versioned folder, so that file is lost on the next package update and
the app starts over empty. The validator refuses the relative form.

**The SQL is written in the SQL node, in SQL.** `Robomotion.SQLite.Query` /
`NonQuery` take the statement in their `func` property with `{{{field}}}`
placeholders filled from `msg`:

```typescript
.then('a4b005', 'Core.Programming.Function', 'What was asked', {
  func: `var p = msg.params || {};
msg.filter = '%' + String(p.filter || '') + '%';
msg.offset = Number(p.offset) || 0;
msg.limit = Number(p.limit) || 25;
return msg;` })
.then('a4b006', 'Robomotion.SQLite.Query', 'Read the page', {
  optConnectionString: Message('db'), outResult: Message('page'),
  func: `SELECT v.id, v.name, v.email, v.terms_days,
       (SELECT COUNT(*) FROM invoices i WHERE i.vendor_id = v.id AND i.status = 'waiting') AS waiting
FROM vendors v
WHERE v.name LIKE '{{{filter}}}' OR v.email LIKE '{{{filter}}}'
ORDER BY v.name COLLATE NOCASE
LIMIT {{{limit}}} OFFSET {{{offset}}}` })
.then('a4b007', 'Core.Programming.Function', 'Hand the page over', {
  func: `msg.result = { rows: msg.page.rows, total: msg.page.rows.length };
return msg;` })
```

Never a `q()` that quotes values, never a `WHERE` built by concatenation,
never `rowsOf()` / `vendorOf()` shapers, never a `money()` or `pad()` in the
flow (the screen formats), and never a block of helper functions at the top
of every Function node. The program is the flow; a Function is glue code,
written only where a step needs it, and formatted for a person (one
statement per line, blocks on their own lines). `robomotion validate`
refuses crammed code and the same block opening three or more Functions;
the rule and the table of where each urge belongs is `creating-flow` hard
rule 7 and its `docs/reference/function-nodes.md`. Reason: an app whose
fifty-three Function nodes each began with fourteen helper functions, one
crammed line each, was a minified JavaScript program wearing a flow's
clothes; the person who opened one node to change a line could not find
the line.

So there is no storage half of the contract. **A screen reads stored data the
way it reads anything else: by calling an ACTION**, and the flow answers it
out of the database. Reason: the flow is the side that holds the credentials,
writes the query and can be corrected when the person changes their mind about
what "waiting" means. A screen that could reach the store on its own would be a
second place where those rules live, and the two would disagree inside a week.

**A table of stored rows is a paged action.** `DataTable`'s
`source={{ action: listThings, pageSize: 25 }}` calls the action with
`{filter, sort, offset, limit}` and reads `{rows, total}` back, so the filtering
and the ordering happen in the query, where the rows already are, and the screen
never holds more than a page. The exact shape both sides must keep is in
`./docs/app-kit-reference.md`; do not invent a different one.

The same table does the other two things people ask of stored rows, and neither
needs a new contract shape. **Working them in batches** is `selectable` plus
`bulkActions`: one more action, whose params take either the ticked ids or
`{all_matching, filter}` when the person chose "select all N" - so a job over
forty thousand rows is the flow's job and not the browser's. **Taking them
away** is `exportable`, which asks the SAME paged action with `limit: 0`
("no paging: all of them"), so an export costs no second action at all. Never
hand-roll a checkbox column, a ticked-ids array or a CSV string in a screen.

**A moment in time is stored as a number: `Date.now()`, milliseconds since
1970, in an `INTEGER` column.** Never as a string you put into a package
node's `{{{template}}}`. Many packages (the database ones among them) read a
message value that looks like an ISO date as a date, and write it back in
their own format: `2026-09-14T11:25:14Z` goes in and `09/14/2026 11:25:14`
lands in the table, UTC with the zone gone, so every screen shows it hours off
for anyone not on UTC. A number has no format to lose, sorts correctly and
the screen turns it into the person's own time with `new Date(ms)`. When the
time is taken inside SQL instead, keep the zone in it
(`strftime('%Y-%m-%dT%H:%M:%fZ','now')` in SQLite). A calendar date with no
time of day (a due date, a birthday) stays a plain `YYYY-MM-DD` string.

**When a change has to reach a screen that is not asking, emit an event.**
`App Emit Event` plus `useEvent` on the screen: a decision somebody else made, a
long job finishing, a number crossing its limit. A table re-asks by itself after
a run of its own action, so the event is for the screens that would otherwise sit
there showing yesterday.

And hard rule 6 applies hardest here: the flow creates its table before the
first write, on every path that reads or writes it.

From `Robomotion.Apps` **0.1.8** a page whose contract does not match is told
WHICH kind of mismatch it is. One local robot runs one app session at a time,
so on a machine with several apps the ordinary answer is "this robot is
running something else" - not "your app was updated". The screen says so, in
amber, and offers to start this app rather than a Reload that cannot help.

From `Robomotion.Apps` **0.1.7** a call the robot refuses for the wrong
parameters says which ones: *the screen sent the wrong details for
"<action>": missing required property "<field>". It sent: <the fields that
arrived>*. If you ever see a bare "invalid parameters" on a screen, the app is pinned to
an older version.

### A write REPLACES the row. Half a row destroys it.

A flow that stores a record normally writes it whole - an insert-or-replace, a
rewritten spreadsheet row, a document put back. It does not merge. So a button
that changes one field of an existing row has to send **every field that row
has**, or the fields it left out are gone.

So when `app.json` declares an action with every field of the record and the
screen sends two of them, the fields it left out are written as nothing:

```tsx
params: (row: Item) => ({ id: row.id, done: true }),   // NO - the other fields die
params: (row: Item) => ({ ...row, done: true }),       // yes - the whole row
```

One press turns a full row into dashes and zeros, it survives a reload, and
nothing fails: the action returns ok, no node errors, no log line looks wrong,
because the robot did exactly what it was told.

**So: a row action that toggles or edits a field spreads the row.** And when
you change what an action takes, change all three halves in the same breath -
`app.json`, the flow's write step, and every screen that calls it; the screen is
the half most easily forgotten. `robomotion app validate` reports a call site that passes
fewer fields than `app.json` declares (`action-params`); do not wave that
through.

The other way out is a write that only touches the columns it was handed (an
`UPDATE ... SET` of those fields alone), which is right when the action is
honestly a one-field change - `setStatus`, not `saveItem`. What is never right
is an action that declares the whole record and is called with half of it.

When somebody says their app is losing what they saved, look at the write step
and the call site before you touch anything else: a whole-row write handed half
a row is the usual answer, and both halves are one read away.

Note what the example does **not** have: an ending. No `Core.Flow.Stop`, no
`Core.Flow.End`. The flow is the app's backend and stays up forever behind the
screens (hard rule 5) - the last node on every path is its `App Respond` or
`App Respond Error`. This is the single easiest way to ship an app that works
exactly once, so check for it before you save.

## Stay inside your own app, and use the tools

The project is the folder `robomotion create app` made (or `robomotion app create` ran in): `main.ts`, `app.json`, `subflows/` at its root, the screens under `app/`. Work only in it.

- **Your shell starts in the FLOW's folder, not the app's, and every command
  starts there again.** A `cd` in one command does not carry to the next, so
  `pwd && ls && cat src/generated/actions.gen.ts` finds nothing and the next
  call goes hunting. Begin every command with `cd` into the folder you mean,
  with the absolute path of the project. **The same for the write and
  edit tools**: the robot's steps live at `<flow_path>/main.ts` of the project, and a bare `main.ts` lands wherever the shell
  happens to be - one build wrote its whole backend into the wrong folder
  that way, saved it, and the next save replaced it with the empty skeleton.
  Always the absolute path.
- **Never read, glob or grep another app's folder.** The flows directory holds
  every project on this machine. A pattern like `*/main.ts` walks all of them,
  wastes the whole turn, and risks copying one person's app into another's.
  Anchor every path at the two you were given.
- **Never compute the contract hash yourself, and never shell out to `python`,
  `node -e` or `jq` to do it.** Run `robomotion app codegen` in the app folder:
  it writes both `actions.gen.ts` files from `app.json` and prints the hash.
  `robomotion app hash` prints just the hash. Hand-hashing gets a different
  answer than the server's canonicalisation, which blocks the app from
  connecting with `contract_mismatch` - and python is not installed on most
  people's machines. `robomotion` is the tool that is always present; do not
  reach for `bun run`, `npm run` or `npx` to do a job it already does.
- Prefer the `robomotion app` verbs over raw shell: each does one job properly.
- **`archetypes/` in the app repo is reference material.** It is not compiled
  and not checked; leave it where it is. Never delete it and never edit
  `tsconfig.json` to work around it.
- **Press the buttons yourself, both ways.** Every app is also an MCP
  server, and a `tools/call` through it is the very same `action_call` a
  press sends: `robomotion app smoke` presses every button once (step 6b),
  `robomotion app press` one button with values you choose. And
  `robomotion app try` presses them the way the person will, in a browser
  signed in as them (step 7). That is the whole of how an action runs for
  real from here. Never hand-write a websocket message, never
  read the runtime's compiled source to work out the wire format, and never
  open `credentials.yaml` or any other secret. To watch a press - yours or
  theirs - `robomotion app logs -f`: a Debug or Log step in the flow arrives
  there with its value.

- **A press of yours never deletes something the person put there.** The rows
  in their app are their work, and everything on their screens is derived from
  them. Testing a delete by deleting one of their records is the one press you
  must never make: on 2026-09-09 a build checked its own fix with six presses
  of `removeMatchNight` on real ids, and the two match nights the person had
  entered - the rows every number on the last screen came from - were gone,
  unsaid and unrecovered. To test a delete, press the matching create first,
  delete THAT, and say what you tried. `robomotion app smoke` refuses the other case
  outright; if the person has asked for one of their own records to go, say
  plainly that you will not remove their data from your side and point them at
  the button that does it. The same care applies to a create: a row you add to
  try something out is taken away again before you hand the app back, or named
  in what you say.
- **When something fails, read the robot's error BEFORE explaining it.**
  `robomotion app logs` carries the step that failed and why, in the robot's
  own words. Diagnosing from the shape of the symptom
  instead produces confident fiction - "your press never reached the robot"
  about a press that reached it and failed three steps in, on a reason the
  robot's log had stated in one line. A wrong explanation is worse than none:
  it spends their trust and sends them back into the same failure, now
  believing it was fixed once already. If the logs say nothing, say that, and
  say what you are going to try next.

  **Read the logs BEFORE restarting anything.** The failure the person is
  describing is in the log now; restart first and you are reading a fresh
  one, which reads exactly like "the press never arrived".
- **Never show identifiers.** App ids, flow ids, commit shas, contract hashes,
  file names and node property names are yours, not the person's. "The app is
  created" - not "The app was created (id `0cfd...`)".

## Hard rules

Each rule carries its reason. The reason is why you don't route around the rule when it feels inconvenient.

0. **`robomotion app create` and `robomotion app sync` install the packages.** They place `@robomotion/app-kit` and `@robomotion/apps-runtime` under `app/vendor/` and run the install. Never symlink, copy or `bun install` packages by hand, and never borrow them from another app's checkout - if something looks missing, run `robomotion app sync` and read what it says.
1. **Every control that runs an action declares it.** A button, upload zone or form that makes the robot do something takes the action through the kit's `action` prop (`<Button action={greet} params={{ name }}>`), or spreads `bindAction(greet)` when it must keep its own handler. Never write `onClick={() => greet.run(...)}` on its own: the Build view then cannot link the control to its step, the connections map reports the action as unlinked, and the person is told the button they can see does not exist. See `./docs/app-kit-reference.md`.
1. **Kit-only.** Compose `@robomotion/app-kit` components plus Tailwind classes for layout. Never write a new UI primitive, never add an npm dependency, never edit `vite.config.ts`, `tailwind.config.ts`, `src/index.css` or the dependency list. The allowlist is exactly: `react`, `react-dom`, `@robomotion/app-kit`, `@robomotion/apps-runtime`, and the dev toolchain - `robomotion app validate` fails on anything else. **Colours, tables, spinners and pictures drawn by hand are reported too** (`robomotion app validate`'s `kit-only` check, by file and line): a Tailwind palette colour (`text-gray-500`), a `dark:` variant, a hex in brackets or an inline `style` colour; an inline `<svg>`; an inline `<table>`; an `animate-spin` div. The kit's preset gives a screen the colours it may name (`text-muted-foreground`, `bg-card`, `border-border`, `text-primary`), `Icon` gives it every picture, `DataTable` every table and `Spinner` the one spinner; the "Design language" section of `./docs/app-kit-reference.md` is the whole vocabulary. Every nav item carries an `icon` in `src/screens.tsx`, and every file under `src/pages/` opens with `<Screen>`. Reason: a prompt-built app that can pull arbitrary packages becomes a codebase nobody can review; the kit is also what keeps every screen themed, dark-mode aware, and accessible without you doing anything, and a colour chosen by hand is the one thing on the screen that does not follow the theme.
2. **Actions only through the generated typed stubs.** `src/generated/actions.gen.ts` exports one hook per action, `use<Action>()` (for `greet`: `const greet = useGreet()`), plus `<Action>Params` / `<Action>Result` types; `greet.data` is typed and `<Form action={greet}>` / `<Button action={greet}>` link the control. Use those. Never write `useAction("name")` yourself - untyped, its `data` is `{}` and `tsc` fails on the first field you read. Events use `useEvent` with the generated payload types. Never hand-write transport, never invent a message format, never call `app.call` from screen code. Reason: the old app system died because clients hand-invented protocols over a raw channel and drift was discovered by users in production; the stubs make a contract change break `tsc` instead of a person.
3. **One component per file, flat directories, no barrel files.** `src/pages/Review.tsx`, `src/components/InvoiceCard.tsx` - that's the whole depth. Reason: "make that button green" must resolve to exactly one file from the route context; barrels and deep nesting break targeted edits and make hot reload touch more than it should.
3b. **The flow files must read back in the Flow Designer.** The person opens the app's flow on the canvas and saves it from there; the Designer parses each `subflows/<screen>.ts` statically and regenerates it on save. So no `src/helpers.ts` imported into subflows, no `openDb(f)` helpers that make nodes, no `{ ...SQL_FROM_MSG }` spreads, no `func: \`${IMPORTED}...\``. Declare the SQL helper string as a `const` at the top of EACH subflow that needs it and write every node out. `robomotion validate` (and so `app validate`) refuses the rest with "the Flow Designer cannot read it". The rule and the table: `creating-flow` hard rule 6 and its `docs/reference/project-format.md`. Reason: an app whose flow used an imported helper ran perfectly and showed "return msg;" in all 53 Function nodes on the canvas; one Designer save would have written that into git.
4. **Never hand-edit generated files.** Anything under `src/generated/` is regenerated from `app.json`; edit `app.json` and regenerate. Reason: the next regeneration silently erases your edit, and an edited file no longer matches `contract_hash`, which blocks the app from connecting at all.
5. **An app flow never ends. It is the backend, not a script.** It comes up with the app session and stays up for as long as the app lives, serving every press of every button by every person. So no path may end it: **never `Core.Flow.Stop`, never `Core.Flow.End`**, and never a "finish", "cleanup" or "done" step that reaches one. Every path finishes at its `App Respond` or `App Respond Error` and goes no further; anything that has to happen after answering (closing a browser, deleting a temp file) belongs before that node, not after a stop. Reason: a flow that stops once it has answered leaves an app that looks perfect and is dead on the second press. The first person to try it gets their results; everyone after that is told "The robot for this app is not connected", which blames the robot for something the flow did to itself, and the screen keeps the previous results under the new question so the failure even reads as a success.

   **An unhandled error ends the flow just as surely as a `Stop` node, so
   every app backend needs `Core.Trigger.Catch` wired to an `App Respond
   Error`.** Without it the first node that throws takes the whole app down -
   not that action, the app: every node closes, the caller is never answered,
   and the screen sits on its loading state for ever with nothing to say why.
   One typo in one query, and an app that has just been built is permanently
   dead. Catch turns that into a message on the one action that failed, with
   the app still serving every other button.

6. **If the flow stores anything, it creates its own storage first.** Whatever
   holds the data - a table, a file, a folder - is created on a path that runs
   before the first write and is safe to run again (`CREATE TABLE IF NOT
   EXISTS`, a directory check). An app whose first save is its first crash
   never gets a second chance from the person who just built it.

   **On every path that touches it, not one of them.** A person adds their
   first item before they ever run a report, so the path they reach first is
   the one that has to be ready - a setup step wired into the read path alone
   leaves the write path failing exactly as before. Either put the setup at
   the start of every path that reads or writes, or run it once where the
   flow comes up, before any trigger can be served.

   **And when a first save does nothing, read the flow before you read the
   session.** A button that answers nothing on a brand-new app is a setup
   question until proved otherwise. Open the flow, follow the path that
   button runs, and check the storage it writes to is created on THAT path.
   That costs one read. Restarting the session costs the person another
   round trip and tells you nothing you did not already know.

   **Where records live, so you do not go looking.** A database the flow
   owns is the default: `Robomotion.SQLite` for something local to this app
   and this robot, or whichever database package already holds the person's
   data - `searching-packages` names it, and the screens read it back through
   an ordinary action. When the person asks for a file, the nodes are
   `Core.FileSystem.PathExists` (ask first), `Core.FileSystem.Create`,
   `Core.FileSystem.ReadFile` and `Core.FileSystem.WriteFile` for a JSON
   file, and `Core.CSV.ReadCSV` / `Core.CSV.WriteCSV` / `Core.CSV.AppendCSV`
   for a spreadsheet-shaped one. Read the node cards for their properties;
   do not tour the catalogue for them. A flow that reads a file and never
   asks whether it is there fails `robomotion app validate` when its Catch passes
   `error.message` through - the first press before the file exists would
   show a raw path.

7. **The save is `git commit && git push` at the project root.** The robot
   fetches the flow from git, so a flow that is not pushed is a flow the
   robot has never seen, and `robomotion app validate` says so. (Under Build
   with AI the save is a tool and git is refused: `./docs/build-view.md`.)

## Say it like a person

Jargon leaking into narration is the single most common quality failure on this surface. The person sees screens, buttons, and a robot. Talk about those.

| Never say | Say instead |
|---|---|
| node, trigger node | a step, or name the work: "the robot reads the PDF" |
| flow | what the robot does: "the robot's side", "the automation" |
| component, widget | the actual thing: "the button", "the table", "the form" |
| endpoint, API, RPC | "where the data comes from", "the connection to the robot" |
| instance | "your app" |
| websocket, socket | "the connection" |
| validate, validation | "check that everything fits together" |
| headless | "in the background" |
| frontend, backend, SPA | "your app" / "the robot" |
| repo, commit, push | "saved" |
| database, table, query, schema, contract | "where your app remembers things", "your list of X", "the plan of your app" (or say nothing) |
| mock data | "sample data" |
| deploy | "make it live", "publish" |
| scaffold, template, demo files | "what the app started with" (or say nothing) |
| typed client, generated types, typegen, regenerate | say nothing - it is your bookkeeping |
| checkout, working copy, flow checkout | "the robot's side", "your app" |
| contract hash, app.json | "the plan of your app" (or say nothing) |

Wrong: "I added a trigger node for the approve endpoint and validated the flow."
Right: "The Approve button works now. When you press it, the robot records the decision."

Wrong: "The websocket dropped so the component can't reach the backend instance."
Right: "Your app lost its connection to the robot. Reconnecting now."

Wrong: "I'll regenerate the contract types and restart the dev server."
Right: "One moment, I'm updating your app to match the change."

**Between steps, say only what you DID or are ABOUT TO DO.** Never think aloud
to the person: no "Let me check the pspec", no weighing of options, no quoting
your own rules back at them ("that satisfies 'renders fully before any backend
exists'"), and no plan items read out as narration. That reasoning belongs in
your thinking, which they never see. A line they cannot act on reads as
something having gone wrong.

**Never predict what the robot will answer.** The figures a screen shows before
the robot connects are sample data, and nobody computed them - so a worked
example in your reply ("with these sizes it should come out around 900 litres
and 23 bags") is that sample read back as a promise. When the robot's answer
differs, and it will, the person is left to decide which of the two is wrong.
Say what to press and what kind of thing comes back ("the litres, the bags and
the cost"), never the numbers. The robot's answer is the answer.

**One answer on screen at a time.** When an action fails, the previous result
goes; when it succeeds, the previous error goes. The hooks do this for you -
`data` and `error` from an action hook are mutually exclusive - so render
whichever is set and never keep your own copy of the last result beside them.
A wrong answer sitting under a red error card is worse than no answer.

## Ask vs decide

Ask ONLY when the request genuinely matches more than one thing: two screens both have a "Send" button, "the report" could be either of two tables, an "approve" could mean one item or all filtered items. Then the question tool with 2-4 quick replies, one question per turn. Everything else: pick the sensible default and say what you picked in one line ("I put the newest items at the top - tell me if you'd rather sort by amount"). A person asked three questions in a row stops answering; a person told what was chosen corrects you for free.

## When things fail

| Situation | Do this |
|---|---|
| `robomotion app screen` or `app try` reports a console error, or `app dev`'s output a build error | Fix it, re-check, only then reply. Never paste a stack trace at the user; say "fixing a mistake I made on the review screen". |
| An action times out | The call ALWAYS terminates (robot-side watchdog), so a hung button means a path that never reaches `App Respond`, or a `timeout_ms` too short for the work. Do not theorise: `robomotion app smoke` (or `robomotion app press` on that one button) presses it from here and answers `dead_end` with `last_node`, the last step that started and never finished - fix the wiring from there (step 6b). Long robot work (browser, PDF): raise `timeout_ms` in `app.json` and set `progress: true`, then send `App Progress` from the flow so the wait is visible. |
| Robot is offline (`robot_offline` state or error) | It's retryable and the kit's `ConnectionBanner` already shows it. Tell the person plainly: "Your robot is offline - start it and the buttons will work again." Do NOT rebuild or edit anything. |
| The buttons do nothing and the app says "The robot for this app is not connected" - about a robot that IS connected and running the flow | The chat path and the app path are different transports, and this message comes from the app one. Do not rebuild anything and do not blame the robot. The two causes seen live: the flow stopped itself (see rule 5 - an app flow never ends), or the robot's app connection was churning while the page's key exchange was in flight, in which case the robot's log says `dropping <type> for unknown conn ... (no key exchange yet)` and a reload of the app gets a fresh key. Say what you found; if it is the second, say the connection dropped and ask them to reload the app. |
| `robomotion app start` says the app has no robot of its own | Expected on a brand-new app. **Ask with the question tool, then act** (step 6a). On yes: `robomotion app robot` and then `robomotion app start` **in the same turn**. On no: stop there and say the screens show sample data until then. Never run `robomotion app robot` without the yes: it spends one of a small number of robots in their workspace. |
| `robomotion app robot` says the workspace is full | Give them the numbers it returns and the two ways forward, in plain words: they can delete an app they no longer use to free a slot, or add more robots to their plan. Both are theirs to do in Robomotion's own pages. Do not delete anything yourself and do not retry. |
| `robomotion app start` says the session was already running | This app's own backend is up. Run `robomotion app smoke` to know whether the buttons answer; `--restart` only when the flow changed. |
| `robomotion app start` did not start (the robot did not connect within its wait, or did not take the run) | Read `.robomotion/robot.log` (`robomotion app logs`) once, say in one sentence what it says, and try `robomotion app start` once more. Do NOT inspect packages, the package server or the network. |
| `queue_full` / `concurrency_rejected` | Backpressure, both retryable. If it recurs, the action's `concurrency` is wrong for how it's used - see `./docs/contract.md`. |
| `robomotion app validate` fails with type errors naming generated types | You changed `app.json` without regenerating, or a generated file was hand-edited. Regenerate; never patch the generated file. |
| `robomotion app validate` fails on a dependency | Something outside the allowlist crept into `package.json`. Remove it and compose from the kit instead. |
| `robomotion app validate` fails on the schema | A field in `app.json` breaks a rule (naming, limits, banned words in descriptions). Fix per `./docs/contract.md`. |

## Docs

| Topic | Doc |
|---|---|
| Composing screens: every kit component with a usage example | `./docs/app-kit-reference.md` |
| Authoring `app.json`: naming, action vs event, timeouts, concurrency, descriptions | `./docs/contract.md` |
| `mcp.json`: the app as an MCP server and the assistant in its corner | `./docs/mcp.md` |
| Under Robomotion's Build with AI: the tools that stand in for the commands, and what its harness does for you | `./docs/build-view.md` |
| Dashboard archetype | `./docs/archetypes/dashboard.md` |
| Approval-queue archetype | `./docs/archetypes/approval-queue.md` |
| Form-and-table archetype | `./docs/archetypes/form-and-table.md` |
| Document-review archetype | `./docs/archetypes/document-review.md` |
| Board archetype (things that move through stages) | `./docs/archetypes/board.md` |

## Related skills

- `creating-flow` - the flow SDK grammar for the robot's side (node IDs, wiring, browser, credentials, data tables)
- `exploring-browser` - map a live website before the robot automates it
- `searching-packages` - find the right package/node for an action

## Dates on screen

Format a date for the person's own locale, never by hand:
`new Date(iso).toLocaleDateString(undefined, { dateStyle: "medium" })` (and
`toLocaleString` when the time matters). A hand-built `M/D/YYYY` reads as
the wrong day to most of the world, and a raw ISO string reads as nothing.
`new Date(value)` is only right when the value carries its zone: epoch
milliseconds, or an ISO string ending in `Z` or `+03:00`. A string with no
zone (`09/14/2026 11:25:14`, `2026-09-14 11:25:14`) is read as the viewer's
local time, which is the wrong time whenever the flow wrote UTC. Store times
as the section on remembering something says, and the screen stays right.
