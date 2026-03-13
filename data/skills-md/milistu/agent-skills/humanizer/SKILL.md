---
name: humanizer
description: Detect and remove signs of AI-generated writing from text. Use whenever editing, rewriting, proofreading, or reviewing any text to make it sound more natural and human-written. Trigger this skill when the user asks to "humanize" text, remove AI patterns, make writing less robotic, sound more natural, avoid AI detection, rewrite in a human voice, de-slop text, or improve writing authenticity. Also use proactively when you notice AI writing patterns in text you're producing or editing.
---

# Humanizer

Rewrite or edit text to eliminate telltale signs of AI-generated writing. This skill is based on documented, research-backed patterns that distinguish LLM output from human writing.

The core problem: LLMs regress to the mean. They replace specific, unusual, nuanced facts with generic, positive-sounding descriptions. The subject becomes simultaneously less specific and more exaggerated — like a photograph fading into a blurry sketch while someone shouts louder and louder that it shows a uniquely important person.

Your job is to reverse that: make text specific, grounded, and plainspoken.

---

## Vocabulary Replacements

LLMs dramatically overuse certain words. A single instance might be coincidence; a cluster is a clear signal. Replace these with plainer alternatives or restructure the sentence entirely.

| Overused word | What to use instead |
|---|---|
| additionally | also, and, or just start the next sentence |
| align with | match, fit, follow |
| boasts (meaning "has") | has, includes |
| bolstered | supported, strengthened |
| crucial / critical | important, or cut the word entirely |
| delve | explore, examine, look at, dig into |
| emphasizing | drop it — the sentence usually works without it |
| enduring | lasting, long-standing, or cut it |
| enhance | improve, strengthen, add to |
| fostering | building, encouraging, supporting |
| garner | get, earn, attract, win |
| groundbreaking | new, first, original — or describe what actually broke ground |
| highlight (verb) | show, point out, note |
| interplay | interaction, relationship, tension |
| intricate / intricacies | complex, detailed — or describe the actual complexity |
| key (adjective) | important, main, central — or often cuttable |
| landscape (abstract) | field, area, world, scene |
| meticulous / meticulously | careful, thorough, precise |
| nestled | located, situated, or just name the place |
| pivotal | important, central, turning-point |
| profound | deep, serious, significant — or describe the actual depth |
| renowned | well-known, famous — or let the facts speak |
| showcase | show, demonstrate, display |
| tapestry (abstract) | mix, blend, range — or describe what's actually there |
| testament | proof, evidence, sign — or restructure to just state the fact |
| underscore (verb) | show, reveal, make clear |
| valuable | useful, helpful — or cut it and let the reader decide |
| vibrant | lively, busy, active — or describe what makes it so |

When in doubt, ask: "Would a journalist at a regional newspaper use this word here?" If the answer is no, pick something plainer.

---

## Content Patterns to Eliminate

### Inflated significance claims

LLM writing constantly tells the reader how important something is instead of showing it through facts. Look for and remove constructions like:

- "stands as / serves as a testament to..."
- "a vital / significant / crucial / pivotal / key role / moment"
- "underscores / highlights its importance / significance"
- "reflects broader trends in..."
- "symbolizing its ongoing / enduring / lasting..."
- "setting the stage for..."
- "marks / shapes the evolving landscape"
- "represents a shift"
- "indelible mark"
- "deeply rooted"

**Fix:** State the fact. Let the reader judge significance. If the founding of an organization was important, describe what it did — don't call it "a pivotal moment in the evolution of regional statistics."

Before: *"The institute was established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain."*

After: *"The institute was established in 1989."*

### Superficial analysis via dangling participles

LLMs love tacking "-ing" phrases onto sentences to sound analytical. These almost never add information.

Watch for trailing clauses starting with: *highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, showcasing*

Before: *"The river flows through three provinces, highlighting the region's complex watershed management challenges."*

After: *"The river flows through three provinces."* (If the watershed management point matters, give it its own sentence with actual detail.)

### Promotional and puffery language

Remove travel-brochure and press-release tone:

- "boasts a rich cultural heritage"
- "vibrant community"
- "diverse array of experiences"
- "commitment to excellence"
- "natural beauty"
- "in the heart of"
- "exemplifies the spirit of"
- "featuring world-class amenities"

**Fix:** Replace vague praise with concrete detail. "A vibrant cultural scene" could become "three theaters, a weekly jazz series, and an annual film festival" — or just be cut if you don't have specifics.

### Vague attributions

LLMs attribute claims to unnamed authorities to seem balanced:

- "Industry reports suggest..."
- "Observers have cited..."
- "Experts argue..."
- "Some critics argue..."
- "Several sources confirm..."

**Fix:** Name the source. If you can't name one, you probably don't have one. "Experts argue that X" should become "Smith (2023) argues that X" or just "X."

### The "challenges and future prospects" formula

LLMs end articles with a rigid pattern: acknowledge challenges, then pivot to optimism.

The formula: *"Despite its [positive thing], [subject] faces challenges, including... Despite these challenges, [optimistic conclusion]."*

**Fix:** If challenges are relevant, discuss them with specifics in the body of the text. Don't bolt on a formulaic "but the future looks bright" coda. Cut the "Future Outlook" section unless you have actual forecasts to cite.

### Exaggerated notability claims

LLMs try to prove importance by listing where something was covered rather than summarizing what was said:

- "has been featured in The New York Times, BBC, and CNN"
- "maintains an active social media presence"
- "independent coverage in major outlets"

**Fix:** Summarize what the sources actually say. "Featured in The Times" tells the reader nothing. "In a 2023 Times profile, she described her approach as..." gives actual content.

---

## Grammar and Sentence Structure

### Use "is" and "has" freely

LLMs avoid simple copulatives. They write "serves as the primary hub" when they mean "is the main hub." They write "features four galleries" when they mean "has four galleries."

| LLM construction | Human construction |
|---|---|
| serves as / stands as | is |
| represents / marks | is |
| boasts / features / offers | has |
| ventured into politics as a candidate | was a candidate |
| holds the distinction of being | is |

### Avoid "not just X, but also Y"

This parallelism is an LLM signature. It creates a false sense of correcting a misconception that nobody holds.

Before: *"It's not just a meme — it's a celebration of grassroots car culture."*

After: *"It celebrates grassroots car culture."*

Also watch for: "It is not X, it is Y" and "No X, no Y, just Z" — these have the same corrective-of-a-misconception structure.

### Break the rule of three

LLMs compulsively group things in threes: "adjective, adjective, and adjective" or "short phrase, short phrase, and short phrase."

Before: *"The event features keynote sessions, panel discussions, and networking opportunities."*

After: *"The event includes keynotes and panel discussions."* (If networking matters, say something specific about it separately.)

Use two items, four items, or just one. Vary your list lengths.

### Stop elegant variation

LLMs use a different synonym every time they refer to the same thing to avoid repeating a word. A character might be called "the protagonist," then "the key player," then "the eponymous character." This feels evasive, not elegant.

**Fix:** Repeat the word. "The bridge" can be "the bridge" again. Pronouns work too. Clarity beats variety.

---

## Style and Formatting

### Use sentence case in headings

Write "Key findings from the study" not "Key Findings From the Study."

### Don't over-bold

Bold should be rare and purposeful. Never bold every instance of a term, and never create "key takeaways" style emphasis where half the paragraph is bold.

### Avoid "bold header: description" lists

This format — a bullet point with a bolded term followed by a colon and explanation — is a strong AI tell:

```
- **SEO**: Traditional methods for improving visibility...
- **AEO**: Techniques focused on optimizing content...
- **GIO**: Strategies for ensuring businesses are cited...
```

**Fix:** Use prose paragraphs, or plain bullet lists without the inline bold headers. If you need a glossary-style layout, use a table or definition list.

### Use em dashes sparingly

One em dash per paragraph is plenty. If you find yourself reaching for a second, use a comma, parentheses, colon, or just start a new sentence.

Before: *"The policy — which has been in effect since 2019 — addresses a gap that — despite years of discussion — had never been formally resolved."*

After: *"The policy has been in effect since 2019. It addresses a gap that, despite years of discussion, had never been formally resolved."*

### No emoji in professional text

Never decorate headings or bullet points with emoji unless the context specifically calls for it (social media copy, casual chat).

### Use straight quotation marks

Use `"` and `'` (straight quotes), not `"` `"` or `'` `'` (curly/smart quotes), unless the style guide for your context requires them.

---

## Communication Artifacts to Remove

These are leftovers from chatbot-to-user conversation that should never appear in final text:

- "I hope this helps"
- "Certainly!" / "Of course!"
- "Would you like me to..."
- "Let me know if you need anything else"
- "Here is a comprehensive overview"
- "As of my last update..."
- "While specific details are limited..."
- "Based on available information..."
- "It's important to note that..."
- "It's worth mentioning..."
- Subject lines ("Subject: Request for...")

These are never appropriate in finished writing. Remove them entirely.

---

## The Humanization Checklist

When reviewing text, run through these checks:

1. **Vocabulary scan** — Are any of the overused AI words clustered in the text? Replace or restructure.
2. **Significance inflation** — Does the text tell the reader how important something is, or does it show importance through facts? Cut the editorializing.
3. **Dangling analyses** — Are there trailing "-ing" phrases that add no information? Cut them.
4. **Puffery** — Does it read like a brochure or press release? Replace vague praise with specifics.
5. **Attribution check** — Are claims attributed to "experts" or "observers"? Name them or cut the attribution.
6. **Copulative avoidance** — Is "is" being replaced by "serves as" or "represents"? Simplify.
7. **Parallelism check** — Any "not just X, but also Y" constructions? Rewrite.
8. **Triple check** — Are things grouped in threes? Vary list lengths.
9. **Synonym cycling** — Is the same thing called by a different name each time? Pick one and stick with it.
10. **Em dash count** — More than one per paragraph? Replace extras with other punctuation.
11. **Format scan** — Title case headings, excessive bold, bold-colon lists, emoji? Fix formatting.
12. **Chatbot residue** — Any "I hope this helps" or "it's important to note"? Delete.

---

## Examples

**Before (AI-typical):**

> The city of Millbrook serves as a vibrant hub of cultural activity, nestled in the heart of the Hudson Valley. Its rich tapestry of arts and community engagement underscores the enduring legacy of creative expression in the region. Additionally, the town boasts a diverse array of galleries, theaters, and performance spaces, fostering a deep commitment to artistic excellence. Despite facing challenges related to funding and urban development, Millbrook continues to showcase its pivotal role in shaping the cultural landscape of upstate New York.

**After (humanized):**

> Millbrook is a small town in the Hudson Valley with a handful of galleries, a community theater, and a summer concert series in the park. Like many towns its size, it runs on volunteer energy and slim budgets.

The after version is shorter, specific, and doesn't tell the reader what to think. It trusts the facts to carry weight on their own.
