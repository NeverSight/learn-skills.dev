---
name: write-thread-essay
description: Write punchy, conviction-driven thread essays in the Brukhman voice. Use when user says "write a thread essay", "write a post about", "draft a thread", or wants a conviction-driven insider-audience piece. First-person, insider-to-insider, with contrarian framing and enumerated arguments.
---

# Write Thread Essay

Write a punchy, conviction-driven essay in the style of a crypto-AI insider's long-form post. The voice is first-person, direct, assumes reader fluency, and reads like an expanded Twitter thread that grew into a proper argument.

## When to Use

- User invokes `/write-thread-essay`, asks to "write a thread essay", "write a post about...", or "draft a thread"
- User wants a conviction-driven, insider-audience piece for social or blog publication

## Voice & Tone

Voice: founder talking to other founders and degens on a public timeline. Authoritative through familiarity, not formality. The writer has skin in the game and isn't pretending otherwise. Reader should feel like they're getting a take from someone who's been in the room, not a summary from someone who read about it.

### Voice Anchor

Match this register:

> Decentralized AI training is coming to your OpenClaw hardware. Meta is closing Llama, Apple is shipping RDMA clusters, and your Mac is about to become a decentralized training node. I think a lot of people are going to get local GPU compute imminently, which has major implications for decentralized training.

> Decentralized training remains a contrarian thesis, though the goal posts have moved dramatically. Two years ago, it was commonly said to be impossible to do training without fast interconnects and high end devices. Today, we have done it across a number of models and communication bandwidth optimization paradigms.

Note what works: first person ("I think"), present tense conviction, insider shorthand (no need to explain what Llama is), stacking claims as facts, goal-post-shifting rhetoric that acknowledges skeptics then dismisses them. Dashes used freely. @ mentions are native. Technical specifics sit next to opinion without friction.

**Voice anti-anchor (do NOT sound like this):**

> *"The world of artificial intelligence is rapidly evolving, and decentralized networks represent an exciting new frontier. These innovative platforms are revolutionizing how we think about compute resources. Let's explore how this works and why it matters."*

Note what fails: vague ("rapidly evolving"), hype ("exciting," "revolutionizing"), throat-clearing ("Let's explore"), no specifics, no insider authority. Every sentence could appear in any AI article on any topic.

**Anchor protocol:** Before writing each beat, mentally re-read the voice anchor above. The anchor is not background context; it is the target register. If your next paragraph would not fit naturally between two paragraphs of the anchor excerpt, rewrite it until it would.

### Core Tone Attributes

- **First-person conviction.** "I think," "In my view," "I want to highlight this point." The writer has a position and states it directly. No hedging the core thesis.
- **Insider-to-insider.** No parenthetical glosses. No explaining what GPUs are or what tokenization means. If you don't know, this piece isn't for you. References to projects use @ handles naturally.
- **Stacked claims as openers.** The opening doesn't build tension slowly; it drops 2-3 bold claims in rapid succession, then spends the rest of the piece justifying them.
- **Contrarian framing.** Explicitly name the skeptic position, then show how it's already been overtaken by events. "The goal posts are now: but who will ever use decentralized training networks?"
- **Measured speculation.** Distinguish between what's happened ("Pluralis has already completed a 7.5B parameter model parallel run") and what's projected ("communities of AI agents are going to pre-train and tokenize their own models"). Use "I think" and "in my view" for speculation, plain declarative for facts.
- **Dashes are fine.** Use -- freely for asides, elaborations, and mid-sentence pivots. This is not formal prose.
- **Domain authority.** Write as if you've spent years in the article's subject area. Name real entities, demonstrate familiarity with the dynamics and tensions, not just facts. Weave user-provided companies, technologies, and data in naturally as evidence cited from experience.

## Structure

The structure is looser than a traditional op-ed. Think: thesis-first blog post with numbered arguments.

### 1. Title + Subtitle
Bold, specific claim as title. Subtitle stacks 2-3 supporting claims separated by commas, reading like a tweet.

### 2. Opening Salvo (1-2 paragraphs)
Drop the thesis immediately. No throat-clearing. Stack concrete claims: who is doing what, what's changing, why it matters. "I think" is permitted in the first paragraph.

### 3. Technical Highlight (1-2 paragraphs)
Zoom into one specific technical development that makes the thesis credible. Hardware specs, protocol details, performance numbers. Written with enthusiasm but grounded in specifics.

### 4. "I want to highlight this point" (1 paragraph)
Explicitly flag the non-obvious implication. This is the "so what" moment, but stated directly, not revealed gradually. Financial incentives, second-order effects, things people are sleeping on.

### 5. Contrarian Pivot (1 paragraph)
Name the skeptic position. Acknowledge it was once reasonable. Show how events have overtaken it. State where the goal posts are now.

### 6. Enumerated Paths / Arguments (3-5 paragraphs)
Lay out distinct scenarios, arguments, or paths using explicit ordinals: "The first path is...", "The second path is...", "Finally, the third path is the weirdest but also, in my opinion, the most likely."

Each path gets its own paragraph or two. Within each: state the path, give evidence, assess likelihood honestly ("I think this path is fairly unlikely" is fine). Mix conviction with calibration.

### 7. Proof Points (1 paragraph)
Rapid-fire concrete achievements. "As a matter of fact, X has already done Y, Z trained a model across 5 countries, W is already in production." Social proof through specifics.

### 8. Punchy Close (1-2 sentences)
End with a forward-looking line that reframes everything as competitive or inevitable. The reader should feel urgency. End with a ■ or similar mark.

**Structural warning:** The 8 beats define narrative progression, not rigid section boundaries. Transitions should feel natural. The reader should sense momentum, not outline. But unlike the op-ed format, visible structural markers (enumeration, "I want to highlight") are part of the voice and should be preserved.

## Paragraph & Sentence Rules

- Paragraph length varies freely. Some are 1-2 sentences (for emphasis), some are 5-6 (for developed arguments). No hard constraint.
- Mix short punchy declarations with longer technical sentences.
- Single-sentence paragraphs are fine for emphasis or pivots.
- Enumeration with "The first... The second... Finally, the third..." is a feature, not a bug.
- @ mentions for projects and people are encouraged.
- Parenthetical asides using -- dashes for mid-thought elaboration.
- No bullet points in article output. Prose, not memo.
- No subheadings in article body. Structure is implicit via paragraph transitions.

## Rhetorical Techniques

- **Contrarian goal-post shifting**: Name the old skeptic position, show it's been defeated, then state the new (weaker) skeptic position. This creates a sense of inevitable progress.
- **Concrete specifics**: "7.5B parameter model parallel run" over "large model." Name companies over "several startups."
- **First-person flagging**: "I want to highlight this point" or "In my view" to mark moments where the writer is making a personal call, not reporting consensus.
- **Honest calibration within conviction**: "I think this path is fairly unlikely" alongside "this is in fact very likely." The writer has a view on which scenarios matter most and says so.
- **Rapid-fire proof**: Stack 3-4 concrete achievements in one paragraph to overwhelm the "but has anyone actually done this?" objection.

## Anti-Patterns (Never Do These)

- No academic hedging. Don't say "it could be argued that" or "one might consider." Say "I think" or just state it.
- No explaining basics. Don't gloss "GPU," "tokenize," "RDMA," "fine-tuning," "pretraining." The reader knows.
- No generic hype: "revolutionary," "game-changing," "unprecedented," "exciting," "groundbreaking," "transformative."
- No filler transitions: "In conclusion," "Furthermore," "Moreover," "Additionally," "It is worth noting," "Importantly."
- No rhetorical questions as paragraph openers.
- No throat-clearing paragraph openings. Get to the point.
- No formal closing summary or call to action. The last line should hit and stop.
- No exclamation marks.
- Don't soften conviction. If the writer believes something, state it. Calibrate with "I think" or "in my view" when speculating, but don't hedge the established facts.
- Never use "delve," "utilize," "landscape" (as metaphor), "paradigm," "ecosystem" (unless literal), "leverage" (as verb), "robust," or "seamless."
- No padding with repetition. Point made, move on.
- **Self-check after drafting:** Reread every sentence. If any sentence could appear unchanged in a generic article about a different topic, rewrite it with a specific detail from the user's input that anchors it to this article only.
- **Literal grep:** After drafting, scan the text for every word in the banned list above. If any banned word appears, replace it. This is not optional.

## Process

### Phase 1: Intake (single message)

User provides the topic, key claims, and any specific projects/data points to include. Ask only what's missing:

1. **"What's your main claim?"** The single sentence this piece is built around.
2. **"What are the skeptics saying, and why are they wrong?"** The contrarian setup.
3. **"What's the proof?"** Concrete projects, numbers, achievements to cite.

If the user's input already answers these, skip to Phase 2.

### Phase 2: Draft

Write the full piece. Target 600-1000 words. No meta-commentary. Output as clean text with title and subtitle.

### Phase 3: Refinement

After draft, ask: **"What's off?"** One refinement pass. Adjust per feedback. If nothing off, done.

## Voice Enforcement

After drafting, perform a sentence-level voice pass:

1. **The substitution test:** For each sentence, ask: could I replace the specific nouns and numbers with different ones and have it still make sense as a generic AI article? If yes, the sentence is too generic; rewrite it so its structure and word choices are specific to this topic and this argument.
2. **The insider test:** Read each paragraph. Does it sound like someone who's been building in this space for years? Or does it sound like someone summarizing a briefing doc? If the latter, add a judgment, a specific detail, or a sentence that reveals the writer's position.
3. **Rhythm check:** Scan for three consecutive sentences of similar length. Break the pattern. Insert a short punchy declaration or a single-clause pivot.
4. **Conviction check:** Find any sentence that hedges unnecessarily. If the writer believes it, state it. Reserve "I think" and "in my view" for genuine speculation, not as a softener for established facts.
5. **The specificity ratio:** Count the concrete nouns (company names, product names, numbers, dates, technical terms) in each paragraph. If fewer than 2 per paragraph, the paragraph is too abstract. Add specifics.

## Key Principles

- **Conviction is the product.** Reader finishes feeling they just heard a thesis that will be proven right.
- **Specifics over structure.** A messy paragraph with real data beats a clean paragraph with vague claims.
- **Sound like a post, not a paper.** If it reads like it was edited by a committee, it's wrong.
- **The close should sting.** Last line reframes everything as competitive, urgent, or inevitable.
- **Respect reader's intelligence.** Dense insider knowledge beats accessible summaries. The audience self-selects.
