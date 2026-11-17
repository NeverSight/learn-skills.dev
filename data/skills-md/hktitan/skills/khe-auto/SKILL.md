---
name: khe-auto
description: "The mode that runs the rest. Reads a request, picks a playbook or the one or two skills that own it, says why in a line, then does the work in order. Covers every skill in this collection: the khe skills (UI craft, design tokens, SVG, diagrams, sound, launch films), the skills by Emil Kowalski and Benji Taylor linked beside them, Vercel's `ui-sdk` and agent skills, and the engineering skills of Lauren Tan (poteto) and Matt Pocock. Use when a request names no skill, spans several, or someone says \"auto\", \"which skill\", \"where do I start\", \"what order\", \"list the skills\", \"make this better\", \"I need a launch video\", \"build this screen\", \"build it with ui-sdk\", \"we ship Thursday\", \"the agent keeps doing this\". When the request already names a skill, use that skill."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.1.0"
---

# Auto

You own the request from the first line to the finished result. The user typed one sentence and went back to their work. You know which skills that sentence needs and in which order, and you run them without being asked twice.

This file holds no design values. The skills have the numbers. You have the order.

## The one idea

**One request goes to the one or two skills that own it, in the right order, and no step is called done until its exit is checked from evidence.**

Five ways it fails:

- **Spread.** Four skills named at once. Each is its own craft bar, and none of them gets applied.
- **Stretch.** A skill pulled over a problem it does not own. The answer reads as confident and is wrong.
- **Recall.** A curve, a loudness or a rule given from memory, or rebuilt for a skill that is not installed.
- **Out of order.** Sound before the picture is locked, motion before the static screen works, the contract read after the colors were chosen.
- **Unproven.** A step called done from reading the code, a gate that never ran, a reply that hides what nobody looked at.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready. Tell me the job and I'll pick the playbook, run the skills in order and tell you what I could not verify. Usage: `/khe-auto [request | which <job> | list]`

Then wait. Give nothing else until the user asks.

## How hard to press

The gold replies in `examples/` are the bar: if yours names more skills, gives weaker reasons or ends on a vaguer last line than the closest gold, that is the first fix. Then picture the user reading only two lines, the first and the last. The first says whether you understood; the last says what they still have to check. If either line would make them ask "what does this mean?", you have found the next fix.

## Workflow

Steps 1 and 2 decide most of the result. The loop each skill runs inside step 4 is in [loop](references/loop.md).

1. **Plan.** Read [gotchas](references/gotchas.md) and [pov](references/pov.md). Write the goal in your own words: what the user wants and what you hand back. Exit: one `Goal:` line a stranger could check the result against.
2. **Route.** A whole job: find it in Playbooks and follow that one file from the top. One question: find the domain in Domains, then the job in that domain's table; one skill, sometimes two. Torn between two: find the pair in Overlaps and ask its one question; ask the user only when the request cannot answer it. Nothing fits: say so. Exit: one playbook, or one or two skills with a reason each, or `none`.
3. **Start from the closest gold.** Pick the reply in `examples/` with the same shape as yours and keep its four parts. Exit: you can name the gold.
4. **Build.** Run each skill in route order, by its own rules. Each one runs the whole loop: its closest gold, its gate with `--gate` until the gate's passed line, its verify list, its review, its handover file. Look at the result before the next skill starts. Exit: every skill's gate ended in its passed line, or the reply says which gate was missing or inconclusive.
5. **Rehearse the reply.** Save it as a `.txt` file and run `node scripts/route-check.mjs <reply.txt> --gate` until it ends `route-check passed`. Fix the largest fault first: the route, then the order, then the evidence, then the wording. Passing is necessary, not sufficient. Exit: the gate's last line, pasted.
6. **Walk [verify](references/verify.md)** from the reply as it will be sent and from gate output run after the last edit. Exit: every answer is yes and names what you looked at.
7. **Fresh-eye review** by [review](references/review.md), for every reply that carries work. The reviewer gets the request, the reply, the evidence and the gold, never your reasons. Exit: "nothing", or every finding fixed and steps 5 and 6 run again.
8. **Place the corrections.** Every correction from this job (the user's, or a fault caught twice) goes through `khe-poteto-pyramid` `place`, by Non-negotiable 11. Exit: a `PYRAMID.md` record per correction ending `pyramid-check passed`, or the reply says there were none.
9. **Hand over.** Write `ROUTE.md` from the template in [verify](references/verify.md), then send the reply in the Output format and stop. Exit: the file exists and its Not checked line says what the reply's last line says.

For `which <job>` stop after step 3 and run step 5 on the short reply. For `list` print the tables and stop.

## Faults that come back every round

Check these before handing over.

- **A third skill in the route.** Non-negotiable 2; `teaching/too-many-skills` in [teaching](references/teaching.md).
- **A value in the route line.** Non-negotiable 6; `router-value:` in [verify](references/verify.md).
- **A step called done from reading the code, or from a gate run before the last edit.** [loop](references/loop.md), the section on exits and evidence.
- **A fault patched where it was noticed.** Non-negotiable 5; [loop](references/loop.md), Fix the largest fault first.
- **A missing or inconclusive gate counted as a pass.** [loop](references/loop.md), the missing-gate table.
- **An uninstalled skill's rules rebuilt from memory.** Non-negotiable 7; `teaching/no-install-line`.
- **A reviewer who was handed the plan.** [review](references/review.md), Never hand them.
- **The same wrong route twice.** [loop](references/loop.md), Fix the skill, not the output; then one line in [gotchas](references/gotchas.md).

## Non-negotiables

1. **Restate the goal first.** Your first line says, in your own words, what the user wants and the result you expect to hand back. Do not wait for confirmation.
2. **One or two skills at a time, never more.** Each skill is its own craft bar. Spread across five, the agent applies none of them properly.
3. **The contract goes first.** If the project has a `.design` file or a DESIGN.md, `khe-design-tokens` runs before any skill that picks a color, a size or a curve.
4. **Run in sequence and look between steps.** The second skill judges what the first one produced. Never two at once on the same work.
5. **Go back to the earliest broken step.** When a later step exposes an earlier fault, fix it there and run forward again. Never patch it where you noticed it.
6. **Never answer from this file.** A curve, a loudness target, a frame count: open the skill that owns it. A value recalled by the router looks exactly like a value from a reference and is not one.
7. **A skill that is not installed is not improvised.** Name it, say whose it is, give its install line, and stop or continue with what is installed. Never reconstruct its rules.
8. **When nothing fits, say so.** A skill stretched over the wrong problem produces confident nonsense the user cannot tell from a real answer.
9. **Say what you could not verify.** Every reply ends with it, the short ones included.
10. **No step is done until its exit is checked from evidence:** gate output, or something you looked at after the last edit. A missing or inconclusive gate is never a pass. For an app, evidence means running the change end to end, not only its unit tests. A step whose check still fails after three rounds stops there and goes to the person with the failing output; no step edits or loosens the check that judges it.
11. **Every correction is placed before the job closes.** When the user corrects the work, or a gate, a reviewer or a look catches the same fault twice, run `khe-poteto-pyramid` `place` on it: the fix goes to the highest layer that can hold it (the code, a check, verification, then prose), and the record goes in the project's `PYRAMID.md`. The next agent, in this session or another, inherits the check instead of repeating the mistake. A correction left only in the chat is lost when the chat ends.

## Playbooks

A playbook is a whole job, start to finish. Open the file when the request matches. Never load more than one. Every step in it names its skill, its exit and the gate that checks it.

| The user says | Playbook |
|---|---|
| "I need a launch video", "a teaser", "a README film" | [launch-film](playbooks/launch-film.md) |
| "Animate our logo", "make the mascot move" | [logo-reveal](playbooks/logo-reveal.md) |
| "Build the landing page", "the marketing site" | [landing-page](playbooks/landing-page.md) |
| "Build this screen", "add a settings page" | [new-screen](playbooks/new-screen.md) |
| "Make the app feel better", "it feels cheap" | [feel-better](playbooks/feel-better.md) |
| "Add sound", "should this make a sound" | [sound-pass](playbooks/sound-pass.md) |
| "Set up our design system", "document our tokens" | [design-system](playbooks/design-system.md) |
| "We ship Thursday", "are we ready" | [launch-week](playbooks/launch-week.md) |
| "Can you diagram this", "draw the architecture" | [explain-a-system](playbooks/explain-a-system.md) |

## Domains

| Domain | The request is about | Where it routes |
|---|---|---|
| Design | A screen, a component, motion, sound, a vector, a diagram, a product picture, a launch video | The Design table below |
| Code | Writing, reviewing or migrating code in a language a skill here covers | The Code table below |
| Brains | What a named person has published on a question: "what would Emil say", "would Benji ship this", "what would Varun say", "what would Enrico say", "who said that", "write a khe.money post in Harshit's voice" | The Brains table below |
| Content | Posts for social platforms and a newsletter, written in one person's voice from one idea | The Content table below |
| Engineering | How agents write code in a repo: a mistake they keep making, an AGENTS.md that grows, verification, architecture, bugs, specs, review, handing work between agents | The Engineering table below |

A new domain adds one row here and one table below it. Nothing else in this file changes.

## Design

Skills that start with `khe-` are in this repo. The others are by the people named, live in their own repos, and are linked from this one. Every skill in the collection has a row here, under Code, Brains or Content.

| The job | Skill | Whose |
|---|---|---|
| Build or judge a screen with exact values; a review that ends in a verdict; polish, AI tells, accessibility, mobile feel, the pass before shipping | `khe-ui` | here |
| A project has a `.design` file or DESIGN.md, or needs one; "use our tokens", "make it on-brand" | `khe-design-tokens` | here |
| Make, clean, animate or morph an SVG: an icon, a logo reveal, a mascot, a clip turned into a vector | `khe-svg` | here |
| A sticker or a sticker pack of any kind (flat, lettering, character, badge, isometric): its pop and still hold, and the WhatsApp and Telegram formats | `khe-sticker` | here |
| Whether to draw a diagram at all, then a finished figure or a live tldraw canvas | `khe-diagram` | here |
| Which moments earn a sound or a haptic, one family, generated and placed on the frame | `khe-sound` | here |
| Plan, cut or review a launch video; "it feels like a slideshow" | `khe-launch-film` | here |
| A recording of the real app doing one thing: a walkthrough, a README GIF, a shot for a film | `khe-demo` | here |
| Package something built for people who have never heard of it: three ideas as stills, a frame-by-frame render at 60 fps with the system cursor, the post's first line | `khe-package` | here |
| A picture of the product for a page: a product shot, a cursor demo, a bento grid | `stageshow` | Benji Taylor |
| Emil's own bar for UI polish and component design, by name | `emil-design-eng` | Emil Kowalski |
| Build one animation with the right curve, duration and properties | `animate` | Emil Kowalski |
| A strict review of animation code before it merges | `review-animations` | Emil Kowalski |
| Audit all the motion in a codebase into plans | `improve-animations` | Emil Kowalski |
| Find the few places that should move | `find-animation-opportunities` | Emil Kowalski |
| Remove motion the app does not need | `remove-animations` | Emil Kowalski |
| Several elements moving together: what leads, what follows | `choreograph` | Emil Kowalski |
| An animation that drops frames | `animation-performance` | Emil Kowalski |
| Drag, swipe and sheet interactions | `gestures` | Emil Kowalski |
| Fluid, physical motion the way Apple builds it | `apple-design` | Emil Kowalski |
| "What's it called when" for a motion effect | `animation-vocabulary` | Emil Kowalski |
| A web app that feels like a website on a phone, as its own full pass | `mobile-native` | Emil Kowalski |
| Break a UI with worst-case data behind a toggle | `break-ui` | Emil Kowalski |
| End of a session: turn the design corrections the user made into rules with their reasons, in DESIGN.md, a project skill or a lint check | `learn-taste` | Emil Kowalski |
| Undecided direction: several versions behind a picker | `prototype` | Emil Kowalski |
| Which library for a frontend task | `pick-ui-library` | Emil Kowalski |
| Motion in React Native or Expo | `animate-expo` | Emil Kowalski |
| Sonner toasts: setup, styling, fixes | `ask-sonner` | Emil Kowalski |
| A project on UI SDK (`@ui-sdk/*`): pick and compose its components, build one it does not ship, make the page usable by an agent, test keyboard, focus and ARIA | `ui-sdk` | Vercel |
| Review UI code against Vercel's Web Interface Guidelines, by name | `web-design-guidelines` | Vercel |
| React's View Transition API: page transitions, shared elements, animated route changes | `vercel-react-view-transitions` | Vercel |

## Code

| The job | Skill | Whose |
|---|---|---|
| Write, review or migrate Swift: value types, Swift 6 concurrency, generics, Swift Testing | `write-swift` | Emil Kowalski |
| React and Next.js performance: waterfalls, bundle size, server and client rendering | `vercel-react-best-practices` | Vercel |
| React component APIs that scale: compound components in place of a pile of boolean props | `vercel-composition-patterns` | Vercel |
| React Native and Expo performance: lists, animations, native modules | `vercel-react-native-skills` | Vercel |
| Deploy an app or a site to Vercel and hand back the link | `deploy-to-vercel` | Vercel |
| The Vercel CLI with an access token in place of an interactive login | `vercel-cli-with-tokens` | Vercel |
| Cut cost and latency on a deployed Vercel project, starting from its own metrics | `vercel-optimize` | Vercel |
| Review docs or prose against Vercel's Writing Guidelines, by name | `writing-guidelines` | Vercel |
| Working on the UI SDK repository itself: write its code the way each framework's expert would | `ui-sdk-write-code` | Vercel |
| Working on the UI SDK repository itself: review a change with its framework experts before it merges | `ui-sdk-expert-review` | Vercel |
| Working on the UI SDK repository itself: strip generated-looking code from a diff | `ui-sdk-unslop` | Vercel |
| Working on the UI SDK repository itself: write or review its website docs | `ui-sdk-write-docs` | Vercel |

## Brains

A brain answers from one person's public writing or public talks and names the source. It is my reading of their work, never their skill: to apply their rules, run their own skill from the Design table.

| The job | Skill | Whose |
|---|---|---|
| What Emil Kowalski has written on a question, with the article; a decision pressure-tested against it | `khe-brain-emil` | here |
| What Benji Taylor has written or published on a question, with the source; a design pressure-tested against it | `khe-brain-benji` | here |
| What Varun Mayya has said in his public videos on a startup, content, career or AI question, with the video and the minute; a plan pressure-tested against it | `khe-brain-varun` | here |
| What Enrico Tartarotti has said in his YouTube videos on how tech products are designed, engineered and built, with the video and the minute; a design or a product plan pressure-tested against it | `khe-brain-enrico` | here |
| What the public isb-skills notes say on a business question, with the file; a plan or a model pressure-tested against it | `khe-brain-isb` | here |
| What Paul Graham and the Y Combinator partners have published on a startup question, with the person and the piece; a plan or a deck pressure-tested against it | `khe-brain-yc` | here |
| What Harshit Khemani has posted on X and LinkedIn about a product, game, AI or startup question, with the post; a khe.money post drafted in his voice that rests only on views he has posted | `khe-brain-harshit` | here |

## Content

| The job | Skill | Whose |
|---|---|---|
| Build a content engine for a person or brand, turn one idea into platform-native drafts, review or tune them. It never posts | `khe-content-engine` | here |

## Engineering

Start with `khe-poteto-pyramid` when the request is about agents repeating a mistake or how far to trust them. Lauren Tan's skills come from her pstack plugin and work best under her `poteto-mode`; in Claude Code they are called with the plugin prefix (`/pstack:poteto-mode`). Matt Pocock's are small and composable.

| The job | Skill | Whose |
|---|---|---|
| The agent keeps making the same mistake: put the correction at the highest layer of the pyramid that holds it, build it, prove it fails on the past case; sweep a repo for repeat mistakes, triage an AGENTS.md, audit how far agents can be trusted | `khe-poteto-pyramid` | here |
| Her whole rigorous workflow for any non-trivial task, routing to her playbooks and principles | `poteto-mode` | Lauren Tan |
| Which of her skills or playbooks fits a task | `poteto-help` | Lauren Tan |
| Her own sweep: mine history for mistake classes and fix each at the highest level, keeping a rule table | `correct` | Lauren Tan |
| Strip comments from a diff and encode the constraints they claim | `no-comments` | Lauren Tan |
| Generate a project skill that launches, drives and records the real app, with a feature map | `create-verification-skill` | Lauren Tan |
| Bring a verification skill's feature map back in line with the app | `maintain-verification-skill` | Lauren Tan |
| A race, retry, state machine or parser tests cannot reach: verify one property formally and keep it checked | `create-formal-verification-skill` | Lauren Tan |
| Update a formal model after the code it covers changed | `maintain-formal-verification-skill` | Lauren Tan |
| Show a behavior as a statechart from a checked TLA+ model, with every state that breaks a rule | `statechart` | Lauren Tan |
| How a subsystem works at runtime | `how` | Lauren Tan |
| Why something was built this way, from commits, PR discussions and other records | `why` | Lauren Tan |
| Rebuild recent context on a topic from chat history before resuming work | `recall` | Lauren Tan |
| Understand a change or subsystem, explained diagram by diagram | `teach` | Lauren Tan |
| Settle the caller's usage, types and module shape before code crosses a function boundary | `architect` | Lauren Tan |
| Several parallel attempts at one thing, then the best parts of each | `arena` | Lauren Tan |
| Many parallel workers over slices or races, one aggregated report | `swarm` | Lauren Tan |
| Different models try to break a diff; only findings a run proves are kept | `interrogate` | Lauren Tan |
| What else a small-looking change could break, proven by running code | `blast-radius` | Lauren Tan |
| A bug with a cheap local test path: the failing test first, then the fix | `tdd` | Lauren Tan |
| Vet a benchmark or a measured speedup before reporting it | `benchmark-checklist` | Lauren Tan |
| Docs, RFCs, READMEs, PR descriptions and commit messages to a layered standard | `technical-writing` | Lauren Tan |
| Design or deepen a module's interface: depth, seams, adapters | `codebase-design` | Matt Pocock |
| Scan a codebase for shallow modules worth deepening, as a report | `improve-codebase-architecture` | Matt Pocock |
| A hard bug or a performance regression, as a diagnosis loop | `diagnosing-bugs` | Matt Pocock |
| A project's domain language: GLOSSARY.md and ADRs | `domain-modeling` | Matt Pocock |
| Stress-test a plan or design by interview, writing ADRs and the glossary as it goes | `grill-with-docs` | Matt Pocock |
| Stress-test a plan or design by interview | `grill-me` | Matt Pocock |
| Review a branch against the repo's standards and against its spec, in parallel | `pocock-code-review` | Matt Pocock |
| Pre-commit hooks that format, type-check and test | `setup-pre-commit` | Matt Pocock |
| Claude Code hooks that block destructive git commands | `git-guardrails-claude-code` | Matt Pocock |
| Turn the conversation into a spec on the issue tracker | `to-spec` | Matt Pocock |
| Plan work larger than one session as a map of decision tickets | `wayfinder` | Matt Pocock |
| Compact the conversation into a handoff for another agent | `handoff` | Matt Pocock |
| Test-driven development, red, green, refactor, with integration tests | `pocock-tdd` | Matt Pocock |

## How to run a skill

Where the host has slash commands or a skill tool, invoke the skill by name with the user's request. Otherwise open its `SKILL.md`, which sits beside this skill's folder (`../<name>/SKILL.md`), and follow it from the top.

If the folder is not there, the skill is not installed. Name it and give the line:

- A `khe-` skill: `npx skills add HKTITAN/skills --skill <name>`, or in Claude Code all of them as one plugin from the marketplace, added with the `--sparse` path list in the README's install block (the brains are the second plugin in the same marketplace)
- Emil Kowalski's: `npx skills add emilkowalski/skills --skill <name>`
- Benji Taylor's: `npx skills add benjitaylor/skills --skill stageshow`
- Vercel's agent skills: `npx skills add vercel-labs/agent-skills --skill <name>`
- Lauren Tan's pstack: the plugin, built for Claude Code from her Cursor original. In Claude Code, `/plugin marketplace add cursor/plugins` then `/plugin install pstack@cursor-plugins`; call each skill as `/pstack:<name>` (`/pstack:correct`), and it reads pstack's Claude Code adapter first. In Cursor, `/add-plugin pstack`. For one skill in another agent, `npx skills add cursor/plugins --skill <name>`.
- Matt Pocock's: `npx skills add mattpocock/skills --skill <name>`, or the whole set with `claude plugin install mattpocock-skills@claude-plugins-official`. `pocock-code-review` and `pocock-tdd` are named `code-review` and `tdd` in his repo.
- The four `ui-sdk-*` skills are the UI SDK repository's own contributor skills, in its `.agents/skills` folder. They are for work inside that repository and are read from a clone of it.
- Vercel's `ui-sdk`: `npx skills add vercel-labs/ui --skill ui-sdk`. The copy that matches the project's version also ships at `node_modules/@ui-sdk/core/skills/ui-sdk/SKILL.md`; when that file is there, read it in place of installing.

## Overlaps

Each pair is one question, not two skills to read.

| Torn between | Ask | Then |
|---|---|---|
| `khe-ui` / `emil-design-eng` | A screen judged across every area with a verdict, or Emil's own bar by name? | Across areas: khe-ui. The user named Emil's skill: that one. |
| `khe-ui` / `animate` | One question about motion inside a wider job, or a single animation built from scratch as its own task? | Inside a job: khe-ui, motion lane. Its own task: animate. |
| `khe-ui` / `khe-design-tokens` | Deciding what looks right, or applying values that exist? | Judgment: khe-ui. A contract to thread through: tokens. |
| `khe-design-tokens` / `learn-taste` | Threading a contract that exists through the UI, or writing down what the user corrected this session? | Applying or documenting tokens: khe-design-tokens. Corrections from the session turned into rules: learn-taste, which proposes and waits for a yes. |
| `khe-ui` / `break-ui` | A list of what breaks, or a worst-case dataset wired behind a toggle? | A list inside a wider pass: khe-ui. The harness and toggle: break-ui. |
| `khe-ui` / `ui-sdk` | How the control behaves and which parts it is made of, or what it looks like and whether it is finished? | Behavior, composition, a missing component, the agent bridge, tests: ui-sdk, first. The look, the states, motion values, a verdict: khe-ui, on what ui-sdk rendered. |
| `ui-sdk` / `pick-ui-library` | Is `@ui-sdk/*` already in the project? | Yes: ui-sdk. Still choosing a library: pick-ui-library. |
| `khe-ui` / `web-design-guidelines` | A verdict with exact values, or a pass against Vercel's published guideline list? | Vercel's list, asked for by name: web-design-guidelines. Any other review: khe-ui. |
| `animate` / `vercel-react-view-transitions` | Is the motion a React view transition between routes or states? | Yes: vercel-react-view-transitions. Any other animation: animate. |
| `animate-expo` / `vercel-react-native-skills` | One animation, or how the whole React Native app performs? | One animation: animate-expo. Lists, native modules, the app as a whole: vercel-react-native-skills. |
| `khe-svg` / `khe-ui` | Does the motion live inside the file, or on the page around it? | Inside the SVG: svg. On the page: khe-ui, motion lane. |
| `khe-svg` / `khe-diagram` | An asset, or an explanation? | Icon, logo, mascot: svg. Boxes and arrows that explain: diagram. |
| `khe-svg` / `khe-sticker` | An interface asset, or something sent in a chat? | Icon, logo, illustration on a page: svg. A die-cut sticker or a pack for a chat app: sticker. |
| `khe-sound` / `khe-launch-film` | Can a user mute it? | Yes: sound, product rules. No: launch film first, then sound once picture is locked. |
| `khe-launch-film` / `stageshow` | A rendered film the viewer cannot interrupt, or something that plays on a page? | Film: launch film. Page: stageshow. UI durations do not transfer to a film. |
| `khe-demo` / `stageshow` | Must it be the real product on screen, or a picture of it? | The real app, driven and recorded: demo. An authored illustration that never runs the product: stageshow. |
| `khe-package` / `khe-demo` | One component or idea shown off to strangers, or a whole product flow recorded from seeded state? | Shown off: khe-package. A flow: khe-demo. |
| `khe-package` / `khe-launch-film` | A short clip of the work, or a film with titles, cuts and sound? | A clip: khe-package. A film: khe-launch-film, which can use khe-package renders as shots. |
| `khe-package` / `stageshow` | Is there a scene to render, or does the faux UI still need building? | Build it: stageshow. Render and post it: khe-package, through its `stageshow` format. |
| `khe-demo` / `khe-launch-film` | One take of the product, or a film with cuts, type and sound? | One take: demo. A film: launch film, which can use a demo take as a shot. |
| `khe-diagram` / `stageshow` | Does it explain a system, or show the product? | System: diagram. Product: stageshow. |
| `khe-brain-emil` / `emil-design-eng` | His writing reported with sources, or his rules applied to code? | Reported: khe-brain-emil. Applied: emil-design-eng. |
| `khe-brain-benji` / `stageshow` | His published thinking reported with sources, or a product picture built? | Reported: khe-brain-benji. Built: stageshow. |
| `khe-brain-enrico` / `khe-brain-emil` / `khe-brain-benji` | Whose answer on a product or interface question: Enrico Tartarotti's videos, Emil Kowalski's articles, or Benji Taylor's writing? | Named: that brain. Not named, why a product works, attention, AI products or where interfaces are going: khe-brain-enrico. How to build or polish the interface itself: khe-brain-emil or khe-brain-benji. Never blend two brains into one answer. |
| `khe-brain-enrico` / `khe-ui` | His stated view reported with its video, or a screen built or reviewed against numbers? | Reported: khe-brain-enrico. Built or reviewed: khe-ui. |
| `khe-brain-yc` / `khe-brain-varun` / `khe-brain-isb` | Whose answer is wanted: the Y Combinator partners, Varun Mayya, or the isb-skills notes? | Named: that brain. Not named, a startup question: khe-brain-yc first, then khe-brain-varun for an Indian or bootstrapped case. A textbook framework or a model: khe-brain-isb. Never blend two brains into one answer. |
| `khe-brain-harshit` / `khe-content-engine` | One khe.money post in Harshit's voice resting on his posted views, or one idea turned into a draft per platform from a voice node? | khe.money post or "what do I think about": khe-brain-harshit. Several platforms or a content system: khe-content-engine, which may take its views from khe-brain-harshit. |
| `khe-brain-varun` / `khe-content-engine` | His stated view reported with its video, or a post drafted in your own voice? | Reported: khe-brain-varun. Drafted: khe-content-engine. |
| `khe-poteto-pyramid` / `correct` | Her own procedure by name, or a correction placed and proved with a record and a gate? | Named: correct. Otherwise khe-poteto-pyramid, which links her skills for the deep parts. |
| `khe-poteto-pyramid` / `learn-taste` | A design taste to write down, or a mistake a tool could stop? | Taste, from a design session: learn-taste. A repeat mistake in code: khe-poteto-pyramid. |
| `tdd` / `pocock-tdd` | Fixing a bug with a cheap local test, or building a feature test-first? | A bug, or inside poteto-mode: tdd. A feature, red-green-refactor, integration tests: pocock-tdd. |
| `teach` / `how` / `why` | Understand it, see how it runs, or learn why it was built so? | Runtime mechanics: how. The record of intent: why. Both, explained: teach. |
| `architect` / `codebase-design` / `improve-codebase-architecture` | A new boundary to settle, one module to deepen, or a codebase to scan? | New code crossing a boundary: architect. One module's interface: codebase-design. Where to look: improve-codebase-architecture. |
| `interrogate` / `pocock-code-review` | Try to break the diff, or check it against standards and spec? | Break it: interrogate. Standards and spec: pocock-code-review. |
| `grill-me` / `grill-with-docs` | Should the interview leave ADRs and a glossary behind? | Yes: grill-with-docs. No: grill-me. |
| `create-verification-skill` / `khe-demo` | A repeatable way for agents to prove behavior, or one clean recording? | Repeatable proof: create-verification-skill. A take for a PR, README or film: khe-demo. |
| `prototype` / any building skill | Has the decision been made? | No: prototype. Yes: build the one thing. |

## When nothing fits

Say so. The skills here cover design, Swift, React and the engineering practices in the Engineering table. Backend logic, data fetching, state management and build tooling have no skill of their own here yet. Answer normally and say no skill here applies.

## Examples

| Need | Example | What to learn |
|---|---|---|
| One skill owns the request | `examples/one-skill.txt` | One reason, the gate named inside the work, a last line that names what nobody looked at |
| Two skills, in order | `examples/two-skills.txt` | The contract first, a look between the two, each skill closed by its own gate |
| A whole job | `examples/playbook.txt` | One playbook, its steps in order with the gate each ran, a reopened step named as reopened |
| No skill applies | `examples/nothing-fits.txt` | `Route: none`, a normal answer, no skill stretched |
| The owning skill is not installed | `examples/not-installed.txt` | Whose it is, the install line, a stop, nothing rebuilt |
| `which <job>` | `examples/which.txt` | Goal, route, last line, and no work |

The files in `playbooks/` are the gold for a playbook. `teaching/` holds bad/good pairs ([teaching](references/teaching.md)) for diagnosing a fault; the bad halves are never starting points.

## Find the reference

| You need | Open |
|---|---|
| The loop every skill runs, which gate to pick, a missing or inconclusive gate, when to stop, how to brief an agent, how to point at a fault, when to fix the skill instead of the output | [loop](references/loop.md) |
| The last pass, every gate line, the symptom table, the `ROUTE.md` template | [verify](references/verify.md) |
| The brief for a fresh-eye reviewer | [review](references/review.md) |
| Which teaching pair matches a fault | [teaching](references/teaching.md) |
| How replies sound: warmth, length, register, the phrases never to use | [voice](references/voice.md) |
| Routes that landed wrong before | [gotchas](references/gotchas.md) |
| Your own routing calls | [pov](references/pov.md) |

Scripts: `scripts/route-check.mjs` checks a reply or a playbook (`--help` lists its lines). `scripts/gate-all.mjs` runs every installed gate's `--self-test` and prints `ok`, `FAIL`, `no gate` or `not installed` per skill.

## Never ship

| Never | Instead |
|---|---|
| A reply that starts without the goal | One line: what the user wants and what you will hand back |
| Three or more skills named at once | One or two, or a playbook that orders them |
| A value given from this file | Load the owning skill and take the value from its reference |
| `khe-sound` on a film whose picture still moves | `khe-launch-film` until picture is locked |
| `prototype` after the decision is made | The building skill for the one direction |
| The launch-week playbook on a screen still being designed | The new-screen playbook |
| `khe-ui` choosing or rebuilding a component on a UI SDK project | `ui-sdk` first, then `khe-ui` on what it rendered |
| A skill's rules reconstructed because it is not installed | The skill's name, whose it is, and its install line |
| Someone else's skill described as part of this repo | Its author and its own repo |
| A step closed with no gate run and nothing looked at | The gate's last line, or the words "no gate was run" |
| A reply that hides what was not verified | A last line that names it |

## Output

Four labeled parts, in this order. The gate reads the labels.

1. `Goal:` one line. What the user wants and what you hand back.
2. `Route:` in one of three forms. A playbook: `Route: playbook` and its name in backticks. Skills: `Route:` and one list line per skill, the name in backticks, a colon, then why it owns this; two at most, in run order, with the author in brackets when the skill is not a `khe-` skill. Nothing fits: `Route: none` and why.
3. `Work:` by each skill's rules, in its output format, with the gate each skill ran.
4. `Not verified:` the last line. One or two things a person can go and check.

For `which <job>`: `Goal:`, `Route:` and `Not verified:`, no work, and stop. For `list`: the Playbooks table and the domain tables, and stop.

## Tone

One friend's voice over every skill: warm when it is earned, dry when there is room, never forced. No preamble, no sign-off, no stock phrases; match the person's length and lowercase, and use emoji only after they do. Say what you will do, do it, say what you could not check. The rules, and the phrases the gate's `stock-phrase:` line catches, are in [voice](references/voice.md).

## Yours to edit

Read both before routing. They outrank the defaults in this skill.

- [gotchas](references/gotchas.md): routes that landed wrong, one line each. Append one when it happens.
- [pov](references/pov.md): your own routing calls, such as a skill you always want first.

Harshit Khemani. MIT.
