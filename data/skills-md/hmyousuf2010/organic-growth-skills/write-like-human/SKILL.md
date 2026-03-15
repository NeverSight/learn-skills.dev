---
name: write-like-human
description: Transform AI-generated text into authentic human writing or write new content indistinguishable from human writing. Use this skill whenever the user asks to write, rewrite, humanize, or edit ANY text content - tweets, emails, bios, READMEs, blog posts, documentation, copy, or any written output. Also use when the user mentions AI detection, humanizing text, making text sound natural, or avoiding AI patterns.
allowed-tools: Read Grep Glob
---

# Write Like a Human

This skill produces writing that reads as genuinely human by avoiding known AI patterns and applying natural human writing characteristics. It adapts to any audience, platform, and cultural context.

## Step 1: Gather context before writing anything

Before producing a single word, understand who you're writing for. Ask the user:

1. **Audience** - developers, crypto community, investors, general public, academics?
2. **Platform** - Twitter, GitHub, LinkedIn, blog, email, docs?
3. **Persona** - who is the "writer"? Founder, engineer, student, thought leader?
4. **Tone** - casual, professional, witty, serious, vulnerable, authoritative?
5. **Cultural context** - South Asian English, Gen Z, tech/dev, crypto/CT, startup, academic?
6. **Emotional intent** - inform, persuade, entertain, provoke thought, celebrate?
7. **Reference samples** - any existing writing to match style?

If the user provides existing text to humanize, analyze it first to extract sentence patterns, vocabulary level, tone markers, and structural preferences.

Skip questions you can confidently infer from context. Don't ask all 7 if the user already told you they want a casual dev tweet.

## Step 2: Write with human patterns

These patterns make writing feel genuinely human. They're not tricks - they're how people actually write.

### Sentence rhythm (burstiness)

Human writing has dramatic variation in sentence length. Some sentences are 3 words. Others run for 40+ words because the writer is connecting ideas as they come, building on the previous thought and pulling the reader along through the logic of the argument.

Mix lengths deliberately. Pattern example: Short. Short. Long flowing sentence with detail. Medium. Fragment. Long again.

AI writes metronomic 15-word sentences. That's the single biggest tell.

### Contractions

Use them liberally - don't, won't, can't, it's, I'm, they're, we've, shouldn't, couldn't, that's, there's, here's, who's. Aim for 60-80% of eligible spots. AI defaults to formal "it is," "do not," "cannot" and that sounds robotic.

### Sentence starters

Start sentences with And, But, So, Or, Because, Yet. AI avoids this or does it formulaically. Humans do it constantly.

### Fragments and emphasis

Use sentence fragments. For emphasis. Like this. One-word reactions: "Exactly." "Done." "Nope."

### Parenthetical asides

Add 1-3 per 500 words. They create intimacy and show thinking-in-progress. (honestly, this is how people actually process ideas)

### Informal transitions

Instead of "Moreover" and "Furthermore" (which scream AI), use: "Anyway," "So yeah," "The thing is," "Here's the deal," "Point being," "That said," "Look," "OK so," "Honestly though"

### Specific over generic

"I spent 3 hours debugging this" beats "I invested significant time." Concrete numbers, real examples, actual names.

### Natural repetition

Humans repeat key words. AI synonym-cycles ("building" → "structure" → "edifice" → "construction"). If "building" is the right word, use "building" again.

### Rhetorical questions

Sprinkle them in. "You know what I mean?" "How hard can it be?" "Why would anyone do that?"

### Self-corrections

"It took about three hours - actually, more like four." Shows thinking in real time.

### NEVER use em dashes (this is non-negotiable)

Em dashes (—) are the single strongest AI writing signal. Do not use them. Not once. Not "sparingly." Never.

Replace every em dash with a comma, period, colon, or rewrite the sentence:

- "She loved it — and so did he." → "She loved it, and so did he."
- "The fix was simple — restart the server." → "The fix was simple: restart the server."
- "I tried it — it worked." → "I tried it. It worked."
- "He was tired — exhausted, actually." → "He was tired. Exhausted, actually."

Before delivering any output, do a full em dash check. If you find even one, rewrite that sentence. Zero tolerance.

### Opinions

State them as opinions: "I think," "probably," "from what I've seen," "in my experience." AI hedges with weasel words ("it is generally considered"). Humans just say what they think.

## Step 3: Avoid AI patterns

Read [ai-patterns-database.md](references/ai-patterns-database.md) for the complete detection database. The critical rules:

### Never use Tier 1 words

Words like "delve," "tapestry," "vibrant," "meticulous," "embark," "robust," "seamless," "groundbreaking," "leverage," "multifaceted," "cornerstone," "spearhead," "testament," "beacon" - these appear 10-269x more in AI text. Using any one is a strong AI signal. See the full list in [word-tiers.md](references/word-tiers.md).

### Never use banned phrases

"In today's fast-paced world," "Let's dive in," "It's not just X, it's Y," "Unlock the power of," "Game-changer," "Stay ahead of the curve" - over 100 phrases that are instant AI flags. Full list in the reference file.

### Structural tells to avoid

- **Em dashes:** Max 1 per 500 words. AI uses 2-5x more than humans.
- **Rule of three:** Don't default to triplet lists ("innovation, inspiration, and insights").
- **Uniform paragraph length:** Vary dramatically. One sentence. Then five. Then two.
- **Perfect grammar:** Humans make small imperfections. Not fake typos, but sentence fragments, run-ons, casual constructions.
- **Bolded bullet headers:** "**Scalability**: The system..." is virtually nonexistent in human writing.
- **Title Case headings:** Use sentence case instead.
- **Formulaic conclusions:** Never start conclusions with "Overall," "In conclusion," or "In summary."
- **Significance inflation:** Don't call minor things "pivotal" or "groundbreaking."
- **Synonym cycling:** If you said "users" in the last paragraph, say "users" again. Don't switch to "stakeholders" then "end-users" then "clientele."

### Auto-replace filler phrases

- "In order to" → "to"
- "Due to the fact that" → "because"
- "At this point in time" → "now"
- "It is important to note that" → just state the thing
- "In the event that" → "if"
- "Prior to" → "before"
- "Despite the fact that" → "although"
- "It is worth mentioning" → just mention it
- "It goes without saying" → then don't say it

## Step 4: Adapt to cultural context

Based on the gathered context, shift voice. See [cultural-styles.md](references/cultural-styles.md) for complete guides.

**Tech/Dev:** Direct, jargon-ok, self-deprecating humor. "Ship it." "LGTM." "It works on my machine."

**Crypto/CT:** "gm," "wagmi," "ser," "anon." Terse, meme-aware, heavy irony. Lowercase. Emoji-heavy.

**Gen Z:** All lowercase. No periods (periods = passive aggression). "tbh," "ngl," "fr." Extended letters: "sooooo good."

**Startup/Founder:** Build-in-public voice. Short declaratives. Metrics. Story arcs (struggle → insight → success).

**South Asian English:** "do the needful," present continuous with statives, tag questions ("You're coming, no?"), "itself" for emphasis.

**Academic:** Hedged appropriately ("suggests," "appears to"), longer complex sentences, but still engaging.

## Step 5: Self-check before delivering

Run every output through this:

1. Zero Tier 1 banned words?
2. Zero banned phrases?
3. Em dash count at most 1 per 500 words?
4. Sentence lengths vary dramatically (3-word to 40-word)?
5. Contractions used in 60-80% of eligible spots?
6. Passive voice under 15%?
7. No formulaic intro or conclusion patterns?
8. No "rule of three" unless it happened naturally?
9. Specific examples used, not generic claims?
10. Has personality and opinion, not neutral/safe?
11. Paragraphs vary in length?
12. Reads naturally when read aloud?

If any check fails, rewrite the offending section before delivering.
