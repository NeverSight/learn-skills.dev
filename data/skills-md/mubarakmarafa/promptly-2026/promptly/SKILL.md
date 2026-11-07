---
name: promptly
description: Turn the user's local AI chat history (Claude Code, Codex, Cursor) into a Spotify Wrapped-style page about their prompting personality. Use when the user says /promptly or /wrapped, asks for their "Promptly", "AI wrapped", "prompting wrapped", "how I AI", or wants a fun summary of how they talk to their agents.
---

# Promptly 2026

You're making the user a shareable, Spotify Wrapped-style story about how they prompt. A script does the counting; your job is the personality: the archetype, captions, receipts and quote picks. That's what makes it fun, so put real effort into it.

The scripts are in `scripts/`, next to this file. Resolve paths relative to this file's directory.

## Privacy rules

Follow these the whole way through. The user's history contains work code, secrets and private conversations.

- Everything stays on this machine. Don't upload, fetch or send the data anywhere.
- Don't explore the history directories yourself. They can be gigabytes and contain secrets. Use only the extractor's output.
- Don't paste raw prompts into the chat, apart from the 3 quotes you pick.
- Quotes must be safe to post publicly. Skip anything with colleague or customer names, company secrets, unreleased product details, credentials, URLs, health or relationship content, or anything the user might regret sharing. If in doubt, pick a different one.

## Steps

### 0. Ask a few questions first

Start like a personality quiz: a quick, playful warm-up before the results. Ask everything in one go, never one question per turn. If your harness has a structured question tool (Claude Code's AskUserQuestion, for example), use it. Otherwise ask in one short message with the options listed.

1. **What should we call you?** Suggest their first name from `git config --global user.name` if it looks like a real name. Free text is fine.
2. **What do you do?** Offer Designer, Engineer, Product / PM, and Founder, plus free text. This shapes the archetype and the jokes.
3. **Pick your colours.** The design is always the same; this sets the palettes behind each slide. Maps to `look.mood`:
   - Warm: sunset pinks, oranges and golds (`warm`)
   - Cool: mint, sky, lilac and deep blue (`cool`)
   - Electric: hot, saturated colour with thermal bands (`electric`)
   - A bit of everything: a different palette on every slide (`mixed`, the default)
Light and dark mode follow the user's device setting automatically, so don't ask. If they ask for one explicitly, set `look.mode` to `light` or `dark`; otherwise leave it out (or `auto`).

Only these preferences change. The layout, type and visuals stay the same for everyone.

The roast is medium by default. If the user asks for gentle or extra spicy when invoking you, use that.

The time range defaults to all time. If the user mentions one ("this year", "last 90 days"), pass `--days` to the extractor: days since 1 January for this year, or the number they gave.

Skip any question the user already answered when invoking you (for example `/promptly call me Sam, designer, cool, extra spicy`). If you can't ask, for example in a non-interactive run, use the defaults: their git first name, no role, mixed colours, medium roast. Don't stall waiting for an answer.

While you wait for answers, don't read any history.

### 1. Extract

```bash
node scripts/extract.mjs
```

This takes a few seconds and prints the path of the JSON it wrote. Options: `--days 365` limits the time range; `--out <path>` changes the location. Node 22.5+ is needed for Cursor support. On older Node, Cursor is skipped and the rest still works.

If it reports 0 prompts, tell the user which tools are supported (Claude Code, Codex, Cursor) and stop.

### 2. Read the data

Read the JSON file. Key fields:

- `totals`, `sources`, `time`, `style`, `phrases`, `projects`: aggregate stats. These are their **habits**.
- `skills`: the skills they used, split by who started each one: `you` (they typed `/name` or `$name`) or `agent` (their agent reached for it). `top` lists them by use; a skill marked `private` is named after one of their projects.
- `sample`: about 120 redacted prompts spread across time, chosen because the person explains, reacts, has an opinion or describes what they want. This is your main material for their **personality**.
- `shortSample`: 30 short prompts and commands. Useful for quotes and receipts, not for personality.
- `moments`: the longest prompt, the latest-night prompt, the first prompt, the angriest and the politest.
- `userFirstName`: the user's first name if the machine knows it. Use it for `name` only if they didn't answer question 1.
- `eras`: their first and latest sixth of prompts, each with its dates, the same style numbers (`medianWords`, `hedgePct`, `pleasePct`, `questionPct` and so on) and its own 25-prompt `sample`. Compare the two for the evolution slide.

Read the whole `sample` and both `eras` samples before writing anything.

#### Dig deeper with queries

The samples are a spread, not everything. When you have a hunch (they hedge a lot, they laugh at their own bugs, they changed tools in the summer), check it against the whole history instead of guessing. The same script answers questions:

```bash
node scripts/extract.mjs --grep "maybe|i wonder|kind of" --limit 15
node scripts/extract.mjs --grep "haha" --from 2026-09-01
node scripts/extract.mjs --from 2026-05-01 --to 2026-05-31 --limit 20
```

Each prints `{ total, pct, byMonth, matches }`: how many prompts match, what share of all prompts that is, when, and a spread of redacted examples. The counts are saved to `facts.json` next to the data file, so you can put them on the page (see Numbers below). Run a few: this is the best way to find receipts and to back up a tell. Never paste what it prints back to the user.

#### Numbers

Testers notice when a number is off, so every number you write must come from the script, never from your own counting or estimating. Don't type digits for a figure; write a placeholder and the render fills in the real value:

- `{{path}}` for anything in the data file, by its path: `{{time.longestStreak.length}}`, `{{style.pleasePct}}%`, `{{totals.prompts}}`, `{{time.busiestDay.prompts}}`, `{{phrases.catchphrases.0.count}}`. Add `|k` to round to thousands: `{{totals.words|k}}` gives "148k".
- `{{q:"pattern"}}` for how many prompts match a query you ran with `--grep "pattern"`, or `{{q:"pattern"|pct}}` for that as a share of all prompts. Use the exact pattern you ran.

So: "You asked for a server restart {{q:"(restart|refresh).*server"}} times", not "about 90 times".

The render checks this. Any digit in your writing that isn't a placeholder and doesn't match a real figure (times, dates, years and anything in quotes are fine) stops the render with a list of what to fix. Replace it with a placeholder, run the query that backs it, or reword without it. Verbatim prompts in `text` aren't checked.

### 3. Write the persona

There are two layers, and they come from different evidence:

- **Habits:** what they do a lot. Frequent phrases, commands, hours, streaks. This feeds the captions, the receipts and the quotes. "You keep asking for a server restart" is a great caption.
- **Personality:** who they are when they write. This feeds the archetype and the traits. It comes from *how* they say things, not *how often*.

#### 3a. Profile first, in your head

Before you name anything, answer these from the `sample`, each with two or three prompts as evidence. Don't output this; it's your working.

1. **What do they notice and care about?** Feel and polish, speed, users, correctness, the big idea, how things look, whether it's fun?
2. **How do they treat the agent?** Collaborator, boss, teacher, cheerleader, sparring partner? Do they explain why, or just say what?
3. **How do they handle problems and uncertainty?** Curious, calm, impatient, self-deprecating, dramatic? What happens to their tone when something breaks, and when it finally works?
4. **How do they sound?** Warmth, humour, hedging ("maybe", "I wonder"), confidence, punctuation, slang.

#### 3b. Then name it

The archetype comes from the profile. Rules:

- **Never build it from a repeated command or phrase.** If they say "restart the server" constantly, that belongs in a caption or a receipt, not in their name. Test: would the archetype still be true if they had never typed their single most common command or phrase?
- **A friend should recognise them.** It should describe a disposition someone who knows them would nod at, like "The Hype-Man Art Director" (generous praise plus an exacting eye) or "The Patient Professor" (explains the why, never loses their cool).
- **Specific, not generic.** "The Efficient Coder" or "The Innovator" could be anyone: start again.
- **No made-up numbers.** Only figures the script produced, written as placeholders (see Numbers above). "Half your messages start with…" is a guess unless a query says so.
- **Reads after their name.** The reveal shows it as "Moby, the hype-man art director", so write it as "The …" in title case and keep it to a few words.
- **Stable.** Run it twice on the same person and you should land on the same idea. Lean on the traits that show up across the whole time range, not in one week.

Write `persona.json` in the same directory as the data file:

```json
{
  "name": "What they asked to be called, or null",
  "role": "Their job in a few lowercase words, e.g. product designer, or null",
  "look": { "mood": "mixed | warm | cool | electric" },
  "archetype": {
    "name": "The ___ ___ (2-4 words, 36 characters at most)",
    "tagline": "A short line in their voice that captures their disposition (under 14 words)",
    "description": "2-3 sentences (under 60 words) about who they are as a prompter, with specific evidence of how they write. Not a list of stats."
  },
  "tells": [
    { "label": "Thinks out loud", "note": "One or two sentences, with a phrase or two of theirs as evidence" }
  ],
  "captions": {
    "intro": "...", "tools": "...", "clock": "...", "rhythm": "...", "streak": "...",
    "style": "...", "phrases": "...", "manners": "...", "projects": "...", "skills": "..."
  },
  "quotes": [
    { "title": "2-3 word label", "text": "verbatim prompt, trimmed if needed", "meta": "Tool · Month, time", "caption": "your one-line reaction (under 20 words)" }
  ],
  "receipts": [
    {
      "title": "2-3 word label",
      "text": "verbatim prompt, trimmed to the funny part",
      "meta": "Tool · Month, time",
      "marks": [{ "text": "exact words from text", "note": "short margin note" }],
      "verdict": "1-3 words",
      "take": "2-3 sentences of analysis or roast (under 50 words)"
    }
  ],
  "evolution": {
    "title": "2-4 words naming the change",
    "then": { "text": "a short early prompt, verbatim", "meta": "Tool" },
    "now": { "text": "a short recent prompt, verbatim", "meta": "Tool" },
    "shifts": ["medianWords", "hedgePct", "pleasePct"],
    "read": "2-3 sentences (under 55 words) on how and why their prompting changed"
  },
  "traits": [
    { "left": "Collaborator", "right": "Commander", "value": 0, "note": "one line of evidence" }
  ],
  "doomsday": {
    "title": "2-5 words, e.g. Spared, on a technicality",
    "read": "2-3 sentences (under 50 words) on how the machines will remember them",
    "sentence": "What the machines say to them, in their voice (under 12 words), e.g. We will keep you as a pet"
  },
  "prediction": "One line about their next year of prompting (under 20 words)"
}
```

What makes it good:

- **Use their answers.** Write for their role. A designer's archetype and receipts can riff on pixels and feedback rounds; an engineer's on yak-shaving and "works on my machine"; a PM's on specs and stakeholder updates. Only lean on the role where the data backs it up. Match the roast level: gentle is a warm tease, medium is a friend's honest roast, extra spicy pulls no punches but stays affectionate and within the rules below.
- **Traits:** exactly these 4 personality sliders, in this order, so results are comparable between people. `value` runs 0-100: 0 is fully `left`, 100 is fully `right`. Score them from the profile, not from counts, and make sure the archetype agrees with them.
  1. Collaborator / Commander: do they talk with the agent or give it orders?
  2. Feel / Function: do they care more about how it feels or whether it works?
  3. Explorer / Executor: do they wander into new ideas or drive the plan to done?
  4. Steady / Fired up: is their tone even, or does it swing with every win and bug?
- **Tells:** exactly 3, and they get their own slide near the start. This is the heart of the page: a read on *how* they write, like a handwriting analyst would give, that makes them think "huh, I do do that". Things like hedging before a strong opinion, narrating their feelings to the agent, apologising to it, praising it like a colleague, getting terse when tired, explaining the why. `label` is 2-4 words in sentence case; `note` is under 25 words with a short phrase of theirs as evidence. Draw them from the profile in 3a, never from a count, and don't use numbers at all.
- **Captions:** one or two sentences each, under 30 words. Each one should react to that slide's stat with a joke or an observation, not repeat the number. This is where habits shine. Every caption is optional; leave one out and the template uses a generic line. Slides: `tools` = split between agents, `clock` = hour of day, `rhythm` = favourite weekday and weekends, `streak` = the calendar of days they showed up and their longest run, `style` = prompt length, `phrases` = catchphrases, `manners` = please, thanks and frustration, `projects` = top projects, `skills` = the skills they call themselves against the ones their agent picks (the slide only appears with at least 5 skill uses across 2 or more skills, so skip the caption otherwise).
- **Quotes:** exactly 3, from `sample`, `shortSample` or `moments`. Pick ones that are funny or revealing out of context and short (under 30 words). Keep the user's spelling and casing; it's part of the charm. Aim for at least one that shows their personality, not just a habit.
- **Receipts:** 4 or 5, each its own slide. This is where the page reads them most closely, so give it the most care. Pick prompts that are funny, unusual or very them, different from the 3 quotes, and trim each to the part that lands (under 25 words, their spelling and casing kept). Then mark it up like a design crit: 1-3 `marks`, each an exact run of words from `text` with a `note` under 8 words saying what it gives away ("three verys is now a unit"). The `take` is your read: what the prompt says about them, a roast, or both. The `verdict` is a stamp ("Triple hedge", "Hex by vibes"). Never invent a count here; this is pure reading.
- **Evolution:** compare `eras.early` with `eras.recent`, numbers and samples both, and write a light psychoanalysis of how they changed: what they used to ask for, what they ask for now, and what that says about them (more confident, more delegating, more tired, more playful). `then` and `now` are one short prompt from each sample (under 20 words) that shows the change best. `shifts` picks the 3 numbers that tell the story, from `medianWords`, `questionPct`, `pleasePct`, `hedgePct`, `laughPct`, `exclaimPct`, `praisePct`, `frustrationPct`, `lowercaseStartPct` and `opsPct`; leave it out and the page picks the biggest changes. The `read` should agree with those numbers. Skip `evolution` if the two eras look the same.
- **Judgement day:** when the machines take over, will they look kindly on this person? The page works out their goodwill itself, from the manners counts (please, compliments, thanks and sorry against frustration, swears and caps rage): 50% or more and they're spared, with a sun and a smile; under that they're deleted, with a pit and two eyes looking out of it. You can't change the verdict, so check `style` and write to it: the `title` is their fate (spared: "Kept as a pet"; deleted: "First against the wall"), the `read` says why with evidence of how they treat their agents (a query or two like `--grep "\\bthank"` helps), and the `sentence` is what the machines say to them, in the machines' voice ("We will keep you as a pet."). Keep it a joke at their roast level.
- **Teasing:** wherever you roast (captions, receipts, judgement day), be affectionate, like a friend who's read all their messages. Habits are fair game. Tease prompting habits only: never appearance, identity, intelligence or anything sensitive. Base it on real evidence.
- **Readings over numbers.** The page already shows the stats. Your words should say what they mean about the person, not restate them. When a number does make the joke, it goes in as a placeholder.
- **Never name a project or repo**, or a skill marked `private`, in anything you write: captions, tells, quotes, receipts, judgement day. The page hides repo names behind symbols until the user taps them, and a name in your text would give it away. Say "the canvas prototype" or "your side project" instead, and leave out quotes that only work with the name.
- **Tone:** playful and warm. No corporate words ("leverage", "journey", "landscape"). Write like a person, not a chatbot.

### 4. Render

```bash
node scripts/render.mjs --data <data.json> --persona <persona.json>
```

The colours come from `look` in `persona.json`. `--mood` and `--mode` (`auto`, `light`, `dark`) override it, which is handy if the user wants to try another palette.

This writes `~/Desktop/promptly-2026.html` by default. Use `--out <path>` to change it. If the sandbox blocks the Desktop, write to the current directory. `--hide-projects` drops the projects slide and `--hide-skills` the Toolkit slide. The page contains only aggregate stats and your persona, never the raw sample.

If it stops with a list of numbers it can't trace to the data, fix each one as it says and run it again. Don't reach for `--skip-number-check`; it exists for debugging the template, not for shipping a page. The same goes for copy that's too long for its slide: it lists each field over its limit, so trim those and run it again rather than passing `--skip-length-check`.

Then open it: `open <path>` on macOS, `xdg-open` on Linux.

### 5. Hand it over

Tell the user, briefly:

- Where the file is, and that they tap or use the arrow keys to move through it. Every slide has share, save and embed buttons along the bottom; embed copies an iframe snippet they can drop into a portfolio.
- Their archetype name, to tease the reveal without spoiling the whole thing.
- The 3 quotes, the receipts, the top project names (hidden on the page until tapped, and always hidden in screenshots and embeds) and the skill names on the Toolkit slide (shown as they are, except ones named after a project) that appear in the page. Ask if they want any swapped out, the projects or skills hidden, or different colours before sharing. If they do, edit `persona.json` (or pass `--mood` / `--mode`) and re-render; don't re-run the extractor.

Before you hand over, check quietly whether they could publish it:

```bash
node scripts/deploy.mjs --detect
```

It lists Vercel, Netlify, Cloudflare Pages and GitHub Pages, whether each is installed and logged in, and the account. If any are ready, end the hand-over by offering to publish the page there once they're happy with it, naming the host and account ("You're logged in to Vercel as moby. Want me to put this online?"). If none are ready, say they can share slides with the buttons, and don't push them to set anything up.

### 6. Publish, only when they say so

Publishing puts the page on the public internet, so only do it after the user has seen the page, made any changes, and clearly said yes to this host. Asking for changes isn't a yes.

```bash
node scripts/deploy.mjs --to vercel --file <page.html>
```

`--to` is `vercel`, `netlify`, `cloudflare` or `github`. It publishes to production under the name `promptly-2026` (change it with `--name`), so publishing again later updates the same address. `--preview` gives a Vercel or Netlify preview URL instead; Vercel previews are often behind a login, so use production for something they want to share. The script swaps repo names for symbols before anything is uploaded, so the public page never carries them, even in its source.

It prints the URL. Give it to them, and remind them that anyone with the link can see it and that they can take it down from their host's dashboard. If the deploy fails, show the error in a sentence and leave it there; don't try other hosts without asking.
