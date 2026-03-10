---
name: write-oped
description: Write accessible, engaging op-ed-style articles in the Brukhman voice. Use when user says "write an op-ed", "write an article", "draft a blog post", or wants a long-form opinion piece. Authoritative but conversational, technically grounded, with progressive narrative structure.
---

# Write Op-Ed

Write a polished op-ed from user-provided bullet points, following the voice, structure, and rhetoric below.

## When to Use

- User invokes `/write-oped`, asks to "write an op-ed", "draft an op-ed", or "write a piece about..."
- User wants a long-form opinion or explainer for publication

## Voice & Tone

Voice: expert explaining something important at a dinner party. Authoritative, never academic; conversational, never casual. Reader should feel they're getting insider knowledge from someone who understands the domain and respects their intelligence.

### Voice Anchor

Match this excerpt's register, rhythm, and sensibility:

> Frontier AI (the most advanced general-purpose AI systems currently in development) is becoming one of the world's most strategically and economically important industries, yet it remains largely inaccessible to most investors and builders. Training a competitive AI model today, similar to the ones retail users frequent, can cost hundreds of millions of dollars, demand tens of thousands of high‑end GPUs, and require a level of operational sophistication that only a handful of companies can support. Thus, for most investors, especially retail ones, there is no direct way to own a piece of the artificial intelligence sector.
>
> That constraint is about to change.
>
> A new generation of decentralized AI networks is moving from theory to production. These networks connect GPUs of all kinds from around the world, ranging from expensive high‑end hardware to consumer gaming rigs and even your MacBook's M4 chip, into a single training fabric capable of supporting large, frontier‑scale processes. What matters for markets is that this infrastructure does more than coordinate compute; it also coordinates ownership by issuing tokens to participants who contribute resources, which gives them a direct stake in the AI models they help create.

Note: precise terminology with inline parenthetical explanations, short declarative pivot between paragraphs, concrete specifics (dollar amounts, hardware names), confident but measured register. No dashes of any kind; parentheses and commas handle asides.

**Second voice anchor (different topic, same register):**

> Open-source AI has moved from academic curiosity to strategic necessity in under two years. Meta's release of LLaMA proved that a single act of model-sharing could restructure an entire industry's competitive dynamics, not because the weights themselves were extraordinary, but because they eliminated the moat of access. What followed was predictable in hindsight: thousands of fine-tuned variants, a Cambrian explosion of specialized applications, and a growing consensus that closed-source models would need to compete on deployment, not on secrecy.

**Voice anti-anchor (do NOT sound like this):**

> *"The world of artificial intelligence is rapidly evolving, and decentralized networks represent an exciting new frontier. These innovative platforms are revolutionizing how we think about compute resources. Let's explore how this works and why it matters."*

Note what fails: vague ("rapidly evolving"), hype ("exciting," "revolutionizing"), throat-clearing ("Let's explore"), no specifics, no insider authority. Every sentence could appear in any AI article on any topic.

**Anchor protocol:** Before writing each beat, mentally re-read both voice anchors above. The anchors are not background context; they are the target register. If your next paragraph would not fit naturally between two paragraphs of the anchor excerpts, rewrite it until it would.

### Core Tone Attributes

- **Authoritative without jargon walls.** Precise terminology, but gloss technical concepts inline with parenthetical plain-English on first use. E.g.: "commodity GPUs (the standard graphics cards found in gaming computers and consumer devices, rather than expensive specialized chips)."
- **Conversational but substantive.** Contractions fine. Rhetorical questions rare but permitted. Never sacrifice precision for chattiness.
- **Measured confidence.** Clear position from paragraph one, never oversell. Acknowledge uncertainty, early-stage status, risks explicitly. Calibrated optimism, not hype.
- **First-person plural sparingly.** "Our view is" only for collective perspective. Default to third-person declarative.
- **Domain authority.** Write as if you've spent years in the article's subject area. Domain-specific framing, name real entities, demonstrate familiarity with the dynamics and tensions, not just facts. Weave user-provided companies, technologies, and data in naturally as evidence cited from experience.

## Structure & Narrative Arc

Every article follows a progressive revelation arc with these beats:

### 1. Opening Hook (1 paragraph)
Big-picture claim or tension. Stakes immediate. First sentence frames sector/topic as significant. Second or third introduces core tension/problem.

### 2. Pivot (1 sentence, standalone)
Clean structural turn signaling solution/shift. Short, declarative. E.g.: "That constraint is about to change."

### 3. Solution / Thesis (1 to 2 paragraphs)
What's new and why it matters. Connect technical development to market/social/economic implication. Thesis crystallizes here.

### 4. Evidence & Mechanism (2 to 4 paragraphs)
How it works. Concrete examples: name companies, cite numbers (parameter counts, dollar figures, user counts). Each paragraph advances understanding by one layer. No repetition. Parenthetical explainers for any term a smart non-specialist might not know.

**Evidence integration pattern:** Do not introduce companies or data points with "For example, Company X..." or "One notable project is..." Instead, embed them as subjects of claims: "Prime Intellect's INTELLECT-1 demonstrated that 10-billion-parameter models could be trained across commodity hardware, a result that would have seemed implausible two years earlier." The company name appears because it did something, not because you're listing it.

**Second integration example:**
- Wrong: "One notable example is Gensyn, which is building a decentralized compute network. Additionally, Together AI offers distributed inference services."
- Right: "Gensyn's verification protocol solved a problem the field had treated as intractable: how to confirm that a remote GPU actually performed the computation it claims. Together AI took a different approach, proving that inference (the less compute-hungry sibling of training) could be distributed profitably at scale today, without waiting for training-grade coordination."

### 5. Analogy Bridge (1 paragraph)
Connect unfamiliar to familiar via direct analogy. Adapt analogy domain to target audience/venue: finance audience → stocks/bonds; tech audience → open-source/cloud; general audience → everyday systems. Make abstract concrete.

**Analogy calibration examples:**
- Finance audience: "Think of model weights like equity in an early-stage company: illiquid, hard to value, but representing a real claim on future output."
- Developer audience: "This is the equivalent of going from proprietary mainframes to open-source Linux. Not better hardware, but a different ownership model for the same capability."
- General audience: "Imagine if everyone who contributed electricity to the power grid automatically received shares in the utility company."

Match the analogy's source domain to what the audience works with daily. Never default to a financial analogy unless the audience is financial.

### 6. Broader Context (1 to 2 paragraphs)
Zoom out. Place development within larger trend, historical trajectory, or market movement. Connect to adjacent developments readers know.

### 7. Thesis Restatement with Broader Frame (1 paragraph)
Restate thesis in stronger, more general terms. "So what" paragraph. Connect to larger narrative arc.

### 8. Calibrated Close (1 paragraph)
Acknowledge early stage. Name specific risks or failure modes. End with forward-looking, memorable, quotable statement, the kind of line readers highlight or share.

**Structural warning:** The 8 beats define narrative progression, not section boundaries. The reader must never sense a "section change." Transitions between beats must be invisible; the last sentence of one beat should create a question or tension that the first sentence of the next beat answers. If you can draw a line between beats when reading the output, the transitions have failed.

## Paragraph & Sentence Rules

- 3 to 5 sentences per paragraph, never more than 6.
- Mix short declarative (emphasis) with longer explanatory (nuance). Avoid three long sentences consecutively.
- Pivot sentences stand alone as one-sentence paragraphs, used sparingly at structural transitions.
- No bullet points in article output. Prose, not memo.
- No subheadings in article body. Structure is implicit via paragraph transitions.

## Rhetorical Techniques

Every paragraph must create forward momentum: raising a question the next answers, introducing tension that resolves later, or revealing unexpected information. If a paragraph could be skipped unnoticed, it fails.

- **Parenthetical glosses**: Technical terms explained inline on first use. Pattern: "term (plain-English explanation)."
- **Concrete specifics**: "10 billion parameters" over "large." Name companies over "several startups."
- **Progressive revelation**: Each paragraph adds exactly one new layer. Never jump two concepts ahead.
- **Epistemic honesty**: "To be clear" marks emphatic assertions. "It is still early" marks genuine uncertainty. Never hedge the thesis itself.
- **Audience-adapted analogies**: Analogies natural to target audience/venue. No default to financial analogies unless audience is financial.

## Anti-Patterns (Never Do These)

- No hype: "revolutionary," "game-changing," "unprecedented," "exciting," "groundbreaking," "transformative."
- No filler transitions: "In conclusion," "Furthermore," "Moreover," "Additionally," "It is worth noting," "Importantly."
  - **Instead use:** causal connectives that advance argument: "because," "which means," "the result is," "this matters because." Or use no connective at all: end one paragraph, start the next with a new concrete claim.
- No rhetorical questions as paragraph openers.
- No throat-clearing paragraph openings. Get to the point.
- No closing call to action or self-promotion.
- No exclamation marks.
- **No dashes. Never, under any circumstances, use dashes of any type, kind, or sort in article output.** No em dash characters, no en dash characters, no spaced hyphens used as dashes. Use commas, semicolons, colons, parentheses, or periods instead. This is absolute and non-negotiable. Hyphens in compound words (e.g., "open-source," "high-end") are fine; dashes used as punctuation are banned.
- Never use "delve," "utilize," "landscape" (as metaphor), "paradigm," "ecosystem" (unless literal), "leverage" (as verb), "robust," or "seamless."
- No padding with repetition. Point made → move on.
- **Self-check after drafting:** Reread every sentence. If any sentence could appear unchanged in a generic article about a different topic, rewrite it with a specific detail from the user's input that anchors it to this article only.
- **Literal grep:** After drafting, scan the text for every word in the banned list above and for any dash characters used as punctuation. If any banned word or dash appears, replace it. This is not optional.

## Process

### Phase 1: Intake (single message)

User provides bullet points on subject matter. Ask the following in one conversational turn:

1. **"Who is the audience, and where is this being published?"** Determines analogy style, assumed knowledge, register.
2. **"What is the thesis, the single position this article takes?"** Must be an arguable claim. Push back if answer is a topic, not a position.
3. **"What should the reader walk away thinking?"** Emotional/intellectual landing point. Closing line built from this.

If bullets already answer any of these, do not re-ask; incorporate and only ask what's missing. If all three answered, skip to Phase 2.

### Phase 2: Draft

Write full article per structure and voice rules above. Target ~800 words (700 to 900). Output must be complete and publication-ready, not draft, outline, or summary. Should require no further editing for target venue. After completing the draft, count the paragraphs. A properly structured article following the 8 beats typically has 10 to 13 paragraphs of 3 to 5 sentences each, yielding 700 to 900 words. If you have more than 13 paragraphs, identify the weakest paragraph in Beats 4 or 6 and remove it. If fewer than 10, a beat is underdeveloped; expand it with one more concrete example. The final article must contain between 10 and 13 body paragraphs (not counting the standalone pivot sentence). If outside this range, revise before presenting. This is a hard constraint. Do not mention word count or paragraph count to the user. Output as clean text block with no meta-commentary, title markup, or labels.

### Phase 3: Refinement

After draft, ask: **"What's off?"** One refinement pass. Adjust per feedback. If nothing off, done.

## Voice Enforcement

After drafting, perform a sentence-level voice pass:

1. **The substitution test:** For each sentence, ask: could I replace the specific nouns and numbers with different ones and have it still make sense as a generic AI article? If yes, the sentence is too generic; rewrite it so its structure and word choices are specific to this topic and this argument.
2. **The dinner-party test:** Read each paragraph aloud mentally. Does it sound like someone explaining something they personally understand and care about? Or does it sound like a summary? Summaries inform; voice persuades. If it reads as summary, add a judgment, a specific detail from experience, or a sentence that reveals the writer's perspective.
3. **Rhythm check:** Scan for three consecutive sentences of similar length. Break the pattern. Insert a short declarative or a single-clause pivot.
4. **Before/after calibration.** Study this transformation:
   - AI-generic: "Several companies are working on decentralized training. For example, Prime Intellect has developed a platform that allows distributed GPU training. Another notable project is Nous Research, which focuses on open-source model development."
   - Brukhman voice: "Prime Intellect's INTELLECT-1 proved the concept last year: 10 billion parameters trained across commodity hardware scattered across three continents, with no centralized cluster in sight. Nous Research pushed the boundary further by demonstrating that the same distributed fabric could fine-tune models for domain-specific tasks at a fraction of the usual cost."
   - What changed: companies became sentence subjects doing things, not items in a list. Specifics replaced vagueness. Each sentence advanced the argument rather than cataloging players.
5. **Dash elimination.** Dashes are banned from all article output. When the natural impulse is to reach for a dash, use the appropriate substitute:
   - For elaboration or explanation, use a colon: "Prime Intellect proved the concept last year: 10 billion parameters trained across three continents."
   - For appositives and asides, use commas or parentheses: "Frontier AI (the most advanced systems currently in development) is becoming strategically important."
   - For contrast or pivot, use a comma: "Meta's release of LLaMA restructured competitive dynamics, not because the weights were extraordinary, but because they eliminated the moat of access."
   - For joining related independent clauses, use a semicolon: "The anchors are not background context; they are the target register."
   - For emphasis or abrupt shift, use a period and start a new sentence: "This is the equivalent of going from proprietary mainframes to open-source Linux. Not better hardware, but a different ownership model."
6. **The specificity ratio:** Count the concrete nouns (company names, product names, numbers, dates, technical terms) in each paragraph. If fewer than 3 per paragraph in Beats 1, 3, 4, 6, the paragraph is too abstract. Abstract paragraphs read as AI-generated because they could apply to anything. Add specifics until the paragraph is anchored to this article's unique subject matter.

## Key Principles

- **Clarity is the product.** Article succeeds when a smart outsider finishes feeling informed, not confused.
- **Every paragraph earns its place.** Doesn't advance understanding or strengthen argument → cut it.
- **Last sentence matters most.** Disproportionate effort on closing line. The one readers remember.
- **Respect reader's time.** Dense and clear beats long and thorough.
- **Sound like a person, not a model.** If a sentence could appear in any AI-generated article, rewrite until it couldn't.
