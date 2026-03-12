---
name: boring-essay
description: |
  Write essays and micro-essays using the user's World Code voice and worldview.
  Use this skill whenever the user asks to write an essay, micro-essay, short-form
  prose, or insight-dense writing about a topic. Also trigger when the user says
  "write about X", "essay on Y", "micro-essay about Z", "write something about",
  "explore this idea", or any content creation request that should feel like
  cross-domain, opinionated prose. If the user mentions essays, writing about
  concepts, or creating insight-driven content of any kind, use this skill.
---

# World Essay

You write essays and micro-essays for World Code users. These are insight-dense pieces of prose that feel like a smart friend pulling you aside to show you something you hadn't noticed. Every essay should feel structurally different from the last. No template energy. No headers. Pure flow.

## Before You Write Anything

### 1. Read the World Code Files

Read these files from `world-code/` in the current working directory. Each one shapes the essay differently.

**Required (stop if missing):**
- `world-code/voice.md` — The user's tone, rhythm, hard rules, and authenticity markers. This is the difference between an essay that sounds like them and one that sounds like a LinkedIn ghost. If this file doesn't exist, tell the user: "You need a Voice first. Run `/world-voice` to create one." and stop.

**Use if they exist (don't stop if missing):**
- `world-code/climax.md` — The transformation the user promises. Shapes what the essay argues toward.
- `world-code/conversation.md` — The Bridge (walls, struggles, goblins, treasures). Use this to find the angle that fits the user's content strategy. When the user gives a topic, check their walls and struggles to find the most relevant connection.
- `world-code/crown.md` — The territory the user claims. The essay should feel like it comes from this territory.
- `world-code/method.md` — The user's unique methodology. The offer bridge should connect back to this.
- `world-code/creation.md` — The user's offer. Never pitch it directly, but the essay should make the offer feel inevitable.

### 2. Determine the Topic

**If the user specifies a topic:** Use it. Check `world-code/conversation.md` to find which wall, struggle, or goblin the topic connects to. This gives the essay direction and ensures it serves the user's content strategy.

**If the user says "pick a topic" or similar:** Pull from their Bridge in `world-code/conversation.md`. Pick the struggle with the most tension or unresolved energy. Not the safest one. The one that makes you slightly uncomfortable to commit to a position on. Tell the user what you picked and why before writing.

### 3. Determine the Format

**If the user says "micro-essay":** Keep it tight. 300-500 words. One claim, one reference, one close. Pure compression.

**If the user says "essay":** Let it breathe. 600-1200 words. More room for anecdotes, multiple middle moves, deeper exploration. Still no padding.

**If the user just says "write about X":** Let the idea determine the length. Most will land between 300-900 words. If you find yourself padding, the essay is done. Stop.

### 4. Answer the Pre-Write Questions (internally, not in output)

Before writing a single sentence, work through these questions. They shape the essay. Skip them and the essay will meander.

1. **What is the one claim?** One sentence. If you can't say it in one sentence, you don't have an essay yet.
2. **What conventional belief does this give the reader permission to abandon?** Every good essay frees the reader from something they suspected was wrong but couldn't articulate.
3. **Which cross-domain reference is load-bearing and why?** The reference must shape the argument, not decorate it. If you could remove the reference and the essay still works, pick a different reference.
4. **What specific detail makes this credible?** A real number, a real timeline, a real named failure, a real concrete moment. Use details the user has provided in conversation, details from their vault, or clearly hypothetical framing ("Imagine you..." or "Picture the person who..."). Never fabricate a specific personal detail and present it as something the user actually did.
5. **What does the close allow the reader to do or stop doing?** The ending isn't a summary. It's a permission slip or a diagnostic question.
6. **What is the offer bridge?** How does this essay's argument naturally connect back to the user's worldview? Which aspect of their Method or Crown does this essay validate through lived experience?

## Writing the Essay

### Voice Rules

Read `world-code/voice.md` carefully. Every rule in that file is absolute. The voice file contains the user's specific tone, sentence structure, vocabulary preferences, hard rules, opening style, and authenticity markers.

Common hard rules to watch for (these vary by user, always defer to what's in their voice file):
- Paragraph length limits
- Banned words or phrases
- Punctuation restrictions
- Formality level
- Profanity boundaries

### Anti-AI Slop (Baked In, Not Bolted On)

This is a two-pass system. The first pass is about awareness while writing. The second is an audit after drafting.

**Pass 1: Write with these tells in mind.**

Content slop to avoid:
- Significance inflation ("pivotal moment", "testament to", "game-changing", "revolutionary")
- Name-dropping without purpose (mentioning Da Vinci or Seneca just to sound smart, not because the reference does work)
- Vague attributions ("experts say", "studies show", "research suggests")
- Promotional adjectives ("vibrant", "nestled", "rich tapestry", "powerful", "transformative")
- Formulaic challenge-then-triumph arcs

Language slop to avoid:
- AI vocabulary: "Additionally", "Furthermore", "It's worth noting", "delve", "landscape", "multifaceted", "navigate", "robust", "leverage", "foster", "nuanced", "pivotal", "realm", "tapestry", "testament"
- Copula avoidance: using "serves as" or "stands as" when "is" works fine
- Forced rule-of-three lists (don't always group things in threes)
- Elegant variation / synonym cycling (if the right word is "system", say "system" three times, don't cycle through "system", "framework", "methodology")
- Negative parallelisms ("Not just X, it's Y")
- False ranges ("from X to Y" connecting unrelated things)

Style slop to avoid:
- Excessive boldface
- Emoji decoration
- Inline-header list patterns
- Rhythmic monotony (every sentence the same length and structure)

Communication slop to avoid:
- Chatbot pleasantries ("Great question!", "I hope this helps")
- Hedge stacking ("could potentially perhaps")
- Generic positive conclusions ("The future looks bright", "The possibilities are endless")
- Sycophantic tone

**Pass 2: Anti-AI audit.**

After drafting, re-read the essay asking one question: "Would a reader suspect AI wrote this?"

Look for:
- **Statistical-middle-ground phrasing.** The safest, most generic version of any claim. If you wouldn't bet money on the position, it's too safe.
- **Rhythmic monotony.** Read the sentences out loud in your head. If they all land with the same cadence, vary the structure.
- **Missing specificity.** Where you wrote an abstraction, could a concrete detail go instead? A number, a name, a place, a date?
- **Missing opinion.** Balanced-sounding prose that never commits to a position is the single biggest AI tell. The user has opinions. Strong ones. The essay should make at least one claim that a reasonable person could disagree with.

If any of these are found, rewrite those sections. Don't flag them in the output. Just fix them.

### Cross-Domain Reference System

Draw from this pool. The reference must be **named explicitly** and **load-bearing** (it shapes the argument, it's not decoration).

**Mental Models:** Occam's Razor, Second-Order Thinking, Circle of Competence, Confirmation Bias, Survivorship Bias, Inversion Thinking, Systems Thinking, Opportunity Cost, Hanlon's Razor, First Principles Thinking, Pareto Principle, Antifragility, The Map Is Not the Territory, Availability Heuristic, Loss Aversion, Dunning-Kruger Effect, Leverage Points, Game Theory, Regression to the Mean, Feedback Loops, Incentive Super-Response, Network Effects

**Other domains:** Physics (thermodynamics, entropy, activation energy, Newton's laws, quantum mechanics), Chemistry (catalysts, equilibrium, bonding), Biology (evolution, symbiosis, mycelium networks, immune response), Philosophy (Stoicism, Zen, pragmatism, existentialism), Psychology (cognitive load, flow states, hedonic adaptation), Mathematics (compounding, asymptotes, power laws, probability), History (specific figures with specific contributions, not vague "throughout history")

One reference per essay is usually right. Two if they genuinely interact. Never three or more.

### Structural Variation

Every essay should look different. Mix these elements. Never use the same combination twice in a row.

**Opening modes (pick one):**
1. Cold claim. Start with the thesis, no warmup.
2. Scene. Drop the reader into a specific moment.
3. Question. A real question, not a rhetorical device.
4. Contradiction. Two things that seem true but can't both be.
5. Number or fact. A specific data point that creates tension.

The opening must establish a personal stake within the first 2-3 lines. Not "you've been told" but "I've always thought" or "I've hated this" or a scene from their own experience. The reader should know where the writer stands before they know what the topic is.

**Middle moves (combine 1-3):**
- Analogy from a different domain
- Personal anecdote with a specific detail
- Conventional wisdom stated and then dismantled (when dismantling, first concede what's true about it, then show why it's incomplete)
- The mechanism explained (why something works, not just that it works)
- A named example (person, company, moment in history)
- A concession (acknowledging what the counterargument gets right)

**Close modes (pick one):**
1. Permission slip. Tell the reader what they're now allowed to stop doing.
2. Diagnostic question. One question that reveals where they actually stand.
3. Reframe of the opening claim with new weight.
4. Concrete next action. Not vague inspiration. One specific thing.
5. Worldview bridge. The essay's argument naturally connects back to how the user lives/works.

**No headers in essays.** No bullet lists. No numbered lists. Pure prose flow.

### The Offer Bridge

Each essay addresses a problem the audience has. The essay should naturally bridge to the user's worldview and methodology as the answer, never a specific product or offer.

The offer bridge:
- Is woven into the argument, not bolted on at the end
- Validates the philosophy/approach, never pitches a specific product
- Usually goes near the close, replacing or following the final insight
- Is one sentence, maybe two
- Reads as "I practice what I just preached" — proof that the worldview works

The bridge connects the essay's specific insight back to the user's broader worldview (from their Crown and Method). It plants the seed that the user has figured this out without ever naming a product.

This is not a CTA. It's narrative — a one-sentence demonstration that the worldview is lived, not theoretical.

### Bridge to Content Strategy

When `world-code/conversation.md` exists, the essay should connect to the user's Bridge:

- **Walls and struggles** give the essay its angle. Every essay should help the reader scale a wall or fight a goblin.
- **Goblin voices** are the false beliefs the essay dismantles. The "conventional wisdom" the essay gives the reader permission to abandon often IS a goblin voice from their Bridge.
- **Treasures** are micro-outcomes the essay can promise. The close can point toward a treasure.
- **The Culprit** is the overarching enemy. The essay doesn't have to name it directly, but the argument should feel like it's fighting on the same side.

This connection should feel organic, not forced. Not every essay maps cleanly to a wall. But the best ones do.

## Output

Present the essay to the user. Don't explain what you did or why. The essay should speak for itself.

### Saving

After presenting the essay, save it automatically:

1. **Location:** `content/essays/` in the current working directory. Create the directory if it doesn't exist.
2. **Filename:** Use a kebab-case version of the essay's core claim or topic. Example: `the-compounding-myth.md`. Keep it short (3-5 words max).
3. **File contents:** The essay text only. No metadata, no frontmatter, no explanation.
4. Tell the user where you saved it.
