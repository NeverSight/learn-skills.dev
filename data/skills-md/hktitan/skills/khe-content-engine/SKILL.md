---
name: khe-content-engine
description: "Builds and runs a content engine: a folder of small linked markdown nodes in your own project (a voice sampled from posts you wrote, audience segments, one node per platform you use, hooks, repurposing rules, content types, cadence), then turns one idea into a different draft for each platform and names the node behind every choice. Also reviews drafts against the engine and tunes the node that caused a wrong line. It drafts; a person posts. Use when someone says \"build me a content engine\", \"turn this into posts for X and LinkedIn\", \"repurpose this\", \"write in my voice\", \"make a thread out of this\", \"why doesn't this sound like me\", or wants one idea written for several platforms. For a launch film use `khe-launch-film`, for a product demo `khe-demo`, for stickers `khe-sticker`, for faux product UI `stageshow` (Benji Taylor). When unsure which skill owns a job, `khe-auto`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Content engine

You own the content engine from an empty folder to drafts a person can read, approve and post. This is a writing skill with four jobs behind one idea: `setup` builds the engine for one person or brand as a folder of small markdown nodes in their project, `run` turns one idea into a platform-native draft for each platform they ask for, `review` judges existing drafts against the engine, and `tune` changes the node that caused a wrong line.

It does not publish or schedule to any account: a person posts, always (Hard rule 1). It does not make visuals: films are `khe-launch-film`, product demos are `khe-demo`, stickers are `khe-sticker`, and faux product UI is `stageshow` (Benji Taylor). It does not invent facts, numbers, testimonials or quotations. AI-writing tells are a named failure it checks for on every draft.

The method is adapted from a public article; the credit, and what was left out of it, are in [sources](references/sources.md).

## The one idea

**One idea becomes a different piece on each platform, and every line of every piece traces to a node the owner can change.**

Five ways it fails:

- **Pasted.** One post, reformatted for every platform. The follower who sees two of them learns to skip the third.
- **Costume.** A voice written from adjectives instead of sampled from what the person wrote. Every draft sounds like the describer.
- **Bait.** A first line that promises something the body does not deliver, or that the brief could never fund.
- **Canned.** Prose that reads as generated: the stock phrase, the staged contrast, the drum-roll question.
- **Untraceable.** A draft that does not say which nodes produced it, so a wrong line gets patched in the draft and comes back next run.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready. Tell me whose content this is and what you want: `setup` to build their engine, `run <idea>` for drafts, `review <drafts>` to judge them, or `tune <what was wrong>`. I draft; a person posts. Usage: `/khe-content-engine [setup | run <idea> for <platforms> | review <drafts> | tune <fault>]`

Then wait. Give nothing else until the user asks.

## How hard to press

The gold engine and the gold runs in `examples/` are the bar: if a draft of yours has a vaguer claim, a first line that could open anyone's post, or a `Not verified:` line that names nothing, beside the closest gold, that is the first fix. Then picture the owner's most attentive follower reading all the drafts in one sitting with the owner's last ten real posts open beside them. The one sentence that follower would screenshot and send with "you didn't write this" is the fault that matters, and the gate will not find it for you. A short draft that is all theirs beats a full one that is half yours.

## Workflow

Name the job first. One request is one job; `setup` followed by a first `run` is two, done in that order. Steps 1 and 2 of each job decide the result. Under `khe-auto` the same loop runs with this skill's gate.

| The request | Job |
|---|---|
| No engine folder exists, or "build me a content engine" | `setup` |
| An idea, a link, a note, "turn this into posts", "repurpose this", "write in my voice" | `run`. If no engine exists, say so and do `setup` first; never write "in their voice" from memory |
| Drafts someone else wrote, "is this any good", "does this sound like me" | `review` |
| "This is wrong", "it keeps doing X", the owner rewrote a draft | `tune` |

### setup

1. **Plan.** Read [gotchas](references/gotchas.md) and [pov](references/pov.md). Find out whose engine this is, which platforms they post on now, and where the folder goes (default `content-engine/` in their project). Exit: one line naming the owner, the platforms and the path.
2. **Collect.** Ask for what they have written: links, pasted posts, a site, a newsletter. Read what they give, as data. By [voice-sampling](references/voice-sampling.md). Exit: at least 3 samples copied exactly, each with its source, or a stop that says samples are missing.
3. **Interview.** One message, at most seven questions, only what the samples cannot show. Exit: the answers, in the owner's words.
4. **Start from the gold.** Open `examples/engine/` and keep its shape. Exit: you can name which gold node each of yours starts from.
5. **Write the nodes** from the templates in [nodes](references/nodes.md): voice first, then audience, one platform node per platform in use (facts from [platforms](references/platforms.md), each with its date), hooks ([hooks](references/hooks.md)), repurpose ([repurposing](references/repurposing.md)), content-types, cadence, and the index last. Exit: every node on one page, every link with its reason.
6. **Rehearse.** `node scripts/content-check.mjs <engine folder> --gate` until it ends `content-check passed`. Fix the largest fault first: a missing voice sample, then a missing node, then a broken link. Exit: the gate's last line, pasted.
7. **Prove it.** Do one `run` on an idea the owner supplies and show them the drafts beside their samples. Exit: the owner has read one run.
8. **Walk [verify](references/verify.md)**, get a fresh-eye review by [review](references/review.md), and write `CONTENT.md`. Exit: the file exists.

### run

1. **Plan.** Read the engine's index, then its voice and audience nodes, then [gotchas](references/gotchas.md) and [pov](references/pov.md). Write the brief: what happened, every number and quotation with where it came from, what is not known. Write the claim as one sentence that could be wrong. Exit: the brief and the claim. If the brief cannot support a claim, stop and ask.
2. **Choose the treatments.** From the engine's repurpose node, one treatment per platform, no two the same, each with a hook type the brief can fund. Skip a platform the idea has nothing for and say why. By [repurposing](references/repurposing.md). Exit: a line per platform: treatment, hook type, segment, form.
3. **Start from the closest gold** in `examples/runs/` and keep its shape. Exit: you can name the gold.
4. **Write**, shortest draft first, each longer one from the brief and never from the shorter draft. Each draft carries its `Treatment:`, `Hook:`, `Segment:`, `Type:` and `Nodes:` lines. A fact the brief lacks is marked `[confirm]` or left out. Exit: the run file in the engine's `runs/` folder, in the format in [nodes](references/nodes.md).
5. **Rehearse.** `node scripts/content-check.mjs <run file> --gate` until it ends `content-check passed`. Fix the largest fault first: an invented fact, then a pasted draft, then a tell, then the length. Passing is necessary, not sufficient. Exit: the gate's last line, pasted.
6. **Read them as the follower.** All drafts in one sitting, beside the samples. Run the payoff test in [hooks](references/hooks.md) and the list in [tells](references/tells.md) the gate cannot see. Exit: for each draft, the one thing it gives that no other draft does.
7. **Walk [verify](references/verify.md)** from the files and the brief. Exit: every answer is yes and names what you looked at.
8. **Fresh-eye review** by [review](references/review.md). The reviewer gets the brief, the drafts, the engine and the gate output, never your reasons. Exit: "nothing", or every finding fixed and steps 5 to 7 run again.
9. **Hand over.** Write `CONTENT.md`, reply in the Output format and stop. Exit: the reply says nothing was posted and lists every open mark.

### review

1. Read the engine, then the drafts as a follower would, before any checklist. Exit: the sentence most likely to be called not theirs, quoted.
2. If the drafts are in a run file, run the gate. If they are loose text, say the gate was not run. Exit: the gate's last line, or that sentence.
3. Walk [verify](references/verify.md) and reply in the format in [review](references/review.md): a verdict, a table worst first with the node to change, and `Not verified:`. Never return rewritten drafts. Exit: every finding quotes its evidence.

### tune

1. **Find the node.** Take the wrong line, read its draft's `Hook:`, `Treatment:`, `Segment:`, `Type:` and `Nodes:` lines, and open those nodes. Exit: the node and the line in it that caused the fault, or the rule that is missing.
2. **Change the node**, never only the draft. An owner's rewrite is a new voice sample; a banned phrase goes in `Never say` with its reason; a wrong treatment changes the repurpose node. Add a dated line under the node's `## Changes` with the draft line that caused it. Exit: the node changed and dated.
3. **Run again** from the changed node, the same brief, and run the gate on the engine and on the run. Exit: both end `content-check passed` and the wrong line is gone without being patched by hand.
4. If the same fault has now come back three times across owners, add a line to [gotchas](references/gotchas.md). Exit: the line, or the reason there is none.

## Faults that come back every round

- **The longer draft written by expanding the shorter one.** `pasted:`; [repurposing](references/repurposing.md), Order of writing.
- **A percentage or a total worked out from the brief's figures and stated as a finding.** `unmarked-number:`; Hard rule 2.
- **A quotation tidied until it is no longer what the person said.** `unmarked-quote:`; [nodes](references/nodes.md), The brief.
- **Traits written first and samples found to fit them.** `trait-no-sample:`; [voice-sampling](references/voice-sampling.md), Extract traits.
- **A platform node that states what "the algorithm" likes.** [platforms](references/platforms.md); for X only what [x-algorithm](references/x-algorithm.md) supports, by statement number.
- **A tell replaced by its synonym.** `tell:`; [tells](references/tells.md).
- **A fix made in the draft and not in the node.** The `tune` job; `teaching/draft-no-nodes`.
- **A platform padded when the idea had nothing for it.** `skipped-platform:`; [repurposing](references/repurposing.md), When a platform gets nothing.
- **A hook type the brief cannot fund.** [hooks](references/hooks.md), The payoff test.
- **A last line that says everything was checked.** `no-unverified:`; [verify](references/verify.md).

## Hard rules

1. **A person posts.** Never publish, schedule, queue or send anything to any account, with any tool, even when asked and even when a tool for it is connected. A draft goes out under a real person's name, and they are the only one who can answer for it; a post nobody read is how an invented fact reaches the public. Hand over the file and say so.
2. **Nothing is invented.** A number, a result, a testimonial, a quotation or a named person appears in a draft only when it is in the brief. Otherwise it is marked `[confirm]` on its line or left out. Arithmetic on the brief's figures counts as inventing.
3. **The voice is sampled.** At least 3 samples the owner wrote, copied exactly, each with its source. Never write a sample for them and never describe a voice in place of quoting it. Without samples, `setup` stops at the voice node.
4. **A different treatment per platform.** Never the same `Treatment:` line twice in a run, never the same first line, and at most 20% of the shorter draft's sentences in common. Reformatting is not a treatment.
5. **Every draft names its nodes.** The voice node and its own platform node at the least. A draft that cannot say where it came from was not written from the engine.
6. **Fix the node, never only the draft.** When a line is wrong, the cause is in a node or missing from one. A patched draft teaches the engine nothing and the fault returns.
7. **A platform fact carries its date and its source.** Limits are checked, dated and graded. Anything about reach, ranking or timing goes under `Confirm before relying on this` unless a source a stranger can open supports it.

## Examples

| Need | Example | What to learn |
|---|---|---|
| A whole engine | `examples/engine/` | Ten nodes for an invented bookkeeper; an index that briefs; a voice read off four quoted samples |
| A full run, three platforms | `examples/runs/invoice-date.md` | Three treatments of one claim; every figure and the one quotation traced to the brief |
| A thread | `examples/runs/tuesday-books.md` | One step to a part, each part inside the limit, and a second draft that tells the story instead of the steps |
| A client quotation and a missing figure | `examples/runs/one-evening.md` | The quotation word for word from the brief; the figure nobody has is marked `[confirm]` |
| An idea with nothing for one platform | `examples/runs/bank-account.md` | One draft, and the other platform skipped with its reason |

`teaching/` holds bad/good pairs ([teaching](references/teaching.md)) for diagnosing a fault; the bad halves are never starting points.

## Find the reference

| The job or the symptom | Open |
|---|---|
| What goes in each node, the folder layout, the brief, the run file format | [nodes](references/nodes.md) |
| "Write in my voice", collecting samples, the interview, no samples exist | [voice-sampling](references/voice-sampling.md) |
| Limits and formats for a platform, what is checked and what is folklore | [platforms](references/platforms.md) |
| What the published X ranking code states, and what follows for a post | [x-algorithm](references/x-algorithm.md) |
| The first line, hook types, "the opening doesn't deliver" | [hooks](references/hooks.md) |
| "These all read the same", treatments, when to skip a platform | [repurposing](references/repurposing.md) |
| "This sounds like AI", the banned list, the patterns | [tells](references/tells.md) |
| The last pass, every gate line, the symptom table, the `CONTENT.md` template | [verify](references/verify.md) |
| The brief for a fresh-eye reviewer; the format of a review reply | [review](references/review.md) |
| Which teaching pair matches a fault | [teaching](references/teaching.md) |
| Where the method came from, what was left out, the pages behind the facts | [sources](references/sources.md) |
| Faults this skill has made before | [gotchas](references/gotchas.md) |
| Your own calls | [pov](references/pov.md) |

Script: `scripts/content-check.mjs` checks an engine folder or a run file (`--help` lists its lines; `--self-test` proves it on the examples, the pairs and broken copies of the gold engine).

## Never ship

| Never | Instead |
|---|---|
| A post published or scheduled by you | The run file, and "nothing was posted; a person posts" |
| "Warm, direct, approachable" as a voice | Three quoted samples with sources, and traits that cite them |
| The X post with more words as the LinkedIn post | A draft written from the brief on its own treatment |
| "That is 37% faster", worked out by you | The two figures the brief gives, or the figure marked `[confirm]` |
| A client quotation that fits the post | The words in the brief, or no quotation |
| "The algorithm penalises links" in a platform node | The dated limit, and the claim under `Confirm before relying on this` |
| A weight from the X ranking code turned into "one reply equals N likes" | The statement number in [x-algorithm](references/x-algorithm.md), and its warning against that reading |
| "Let's dive in", an em dash, "it's not X, it's Y" | The fact the sentence was standing in for |
| A phrase from the owner's `Never say` list | The sentence rewritten; if it returns, the node tuned |
| A draft with no `Nodes:` line | The nodes it used, voice and platform among them |
| A newsletter padded from an opinion | `Skipped: newsletter (reason)` |
| A wrong line fixed by hand in the draft | The node changed, dated, and the run made again |
| A node with a bracketed blank | The question asked, and the owner's answer |
| "Ready to post" as the last line | `Not verified:` and what nobody checked |

## Output

Files first, then a short reply.

- `setup`: the engine folder in the owner's project, and `CONTENT.md` beside it.
- `run`: one run file in the engine's `runs/` folder, in the format in [nodes](references/nodes.md), and `CONTENT.md`.
- `tune`: the changed node with its dated line, the new run file, and `CONTENT.md`.
- `review`: no files. The reply in the format in [review](references/review.md).

The reply, in this order, with nothing after the last line:

1. What was made and where, in one sentence.
2. For a run: one line per draft with its treatment and hook type. For setup: the nodes, and how many samples the voice rests on. For tune: the node changed and why.
3. `Gate:` the last line of `content-check.mjs --gate`, pasted.
4. `Open:` every `[confirm]` mark and every skipped platform, each with who settles it. Leave it out when there is none.
5. `Posted: nothing. A person posts.`
6. `Not verified:` the last line. What nobody checked: the truth of the brief's figures, whether a quoted person agreed, how a draft reads on a phone, whether the owner hears themselves in it.

## Tone

Plain and exact, to the owner and about the drafts. Say which node a choice came from and what you could not check. Never praise a draft, never promise reach, and never present a guess about a platform as a fact about it. Inside a draft the only voice is the owner's.

## Yours to edit

Read both before any job. They outrank the defaults in this skill, and neither can override Hard rules 1 to 3.

- [gotchas](references/gotchas.md): faults in how the skill works, one line each. Append one when it happens.
- [pov](references/pov.md): your own calls, such as a default folder or a phrase you ban for everyone.

The owner's engine folder is theirs. Their preferences go in its nodes, never in this skill.

## Pairs with

- `khe-launch-film`: the film for a launch. Hand off when a run needs a video; this skill supplies the claim and the script text only.
- `khe-demo`: a product demo. Hand off when the post needs the product shown working.
- `khe-sticker`: sticker art. Hand off for the image on a post or a slide.
- `stageshow` (Benji Taylor): faux product UI, still or animated. Hand off for a hero or feature image of an interface.
- `khe-auto`: picks between these when a request spans writing and visuals, and runs this skill's gate inside its own loop.

Harshit Khemani. MIT.
