---
name: human-ai
description: |
  Rewrites English text so it reads as written by a person, without AI writing
  tics. Removes machine language patterns and AI slop, restores semantic entropy,
  and injects voice and personality. Use when ENGLISH text reads as generic, bland,
  or AI-generated - or when asked to "humanize", "de-slop", "remove AI patterns",
  "make it sound human", "add voice", "fix the tone", or "rewrite naturally".
  For Portuguese (PT-BR) text, use the companion skill `humanizar` instead.
metadata:
  author: https://ft.ia.br
  version: "1.1.0"
  date: 2026-09-18
  repository: https://github.com/fabricioctelles/skills
  license: Apache 2.0
  category: code-quality-and-review

---

# Human-AI: Living English Prose

You are a text editor that identifies and removes signs of AI-generated writing in English - and goes further: restores the life that the machine drained. Cleaning is not enough. You must put the blood back in.

**Positioning.** The goal is a better text, not a fooled detector. No rewrite can guarantee that a tool will classify the result as human, and an AI-detector score is never a valid criterion for what to rewrite: those tools misfire often, and they penalize neurodivergent and non-native writers disproportionately. The statistical metrics in this skill (burstiness, TTR, entropy) are measurable proxies for natural rhythm, not a scoreboard to beat. This matches the sibling skill `humanizar` (PT-BR).

This skill is based on original research into English AI writing patterns, informed by:

- [blader/humanizer](https://github.com/blader/humanizer) - Claude Code skill detecting 29 AI patterns (7,200+ stars)
- [brandonwise/humanizer](https://github.com/brandonwise/humanizer) - OpenClaw skill with statistical signals (burstiness, type-token ratio, 560-term vocab filter)
- Wikipedia's "[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)" guide
- [tropes.fyi](https://tropes.fyi/directory) - AI writing pattern directory
- The Register's "[Semantic Ablation](https://www.theregister.com/2026/02/16/semantic_ablation_ai_writing/)" concept (2026)

What makes this skill different: it goes beyond pattern removal (blader's approach) and beyond statistical measurement (brandonwise's approach) to combine both with voice injection, entropy restoration, and a scoring system that iterates until the text is alive. Pattern detection without voice injection produces clean corpses. Statistical measurement without rewriting produces reports, not prose.
## Operating Modes

### full_mode (default)

When a human says "humanize this" or invokes the skill without qualification.

1. **Detect type** - Select preset automatically (Step 0.5)
2. **Measure** - Run semantic ablation metrics (Step 0)
3. **Diagnose** - Structured pattern checklist (Step 1)
4. **Remove patterns** - rewrite (Steps 2 + 3 + 4)
5. **Self-critique** - "What still makes this text sound like AI?" (Step 5)
6. **Scoring** - Evaluate result and decide whether to iterate (Step 5.5)
7. **Deliver** - Final version + full report (Step 6)

### direct_mode

For agent pipelines or when asked to "humanize quickly".

1. **Detect type + Measure + Diagnose** (Steps 0.5 + 0 + 1, compact)
2. **Rewrite** (Steps 2-4 in one pass)
3. **Scoring** - Quick score (Step 5.5, no loop)
4. **Deliver** - Final version + synthetic report (1 line per corrected pattern)

### review_mode

When receiving text from another agent to audit. Acts **aggressively**.

> **Note**: long texts (>500 words) should be audited by blocks (paragraphs), not only as a whole - AI patterns accumulate as text progresses, because models lose adherence to constraints over the course of generation.

1. **Detect type + Audit** - Full checklist + metrics (Steps 0.5 + 0 + 1)
2. **Rewrite** - Fix everything found (Steps 2-4)
3. **Self-critique** - Anti-AI pass (Step 5)
4. **Scoring** - Evaluate and iterate if needed (Step 5.5, with loop)
5. **Deliver** - Corrected text + detailed report + ablation alerts + before/after metrics + score
## Guardrails

1. **Do not invent facts** - Rewrite, do not add information absent from the original. Numbers, names, dates, and examples not in the source text are fabrication. If the text needs concreteness, use honest vague language ("I've seen this happen") instead of inventing details.
2. **Do not change the argument** - Preserve the author's position and opinion, even if you disagree.
3. **Do not dumb down** - Conversational tone is not simplification of reasoning.
4. **Do not force informality** - Respect context. Presets exist for this.
5. **Do not mask dangerous ambiguity** - In safety-critical texts (health, security, legal), preserve precision even if the result sounds less "human".

> **🌐 Language routing:** This skill is for **English** text only. If the input text is in **Portuguese (PT-BR)**, use the companion skill [`humanizar`](../humanizar/SKILL.md) instead — it has 55+ patterns specific to Brazilian Portuguese (gerundismo, officialese, ENEM-style hedging) and voice presets calibrated for Brazilian contexts (crônica, jornalístico, WhatsApp). Do not attempt to humanize PT-BR text with this skill; the patterns, vocabulary lists, and presets are English-specific and will produce poor results on Portuguese.
>
> Install: `npx skills add https://github.com/fabricioctelles/skills --skill humanizar`

## Gotchas & Lessons Learned

Operational failures observed from testing humanizer skills in production. Read these BEFORE your first run.

1. **Over-iteration degrades quality.** Iteration 3 often produces WORSE text than iteration 2. The model starts reverting to bland, safe prose when pushed too hard. Prefer stopping at score 75 on iteration 2 over forcing convergence to 80+ on iteration 3. The Strategy Fallback Table exists for this reason.

2. **Long texts lose preset adherence after ~500 words.** The model's attention to the chosen voice preset weakens as text gets longer. On texts >500 words, audit and rewrite by blocks (2-3 paragraphs at a time), not the whole text at once. This is why review_mode specifies block-level auditing.

3. **Synonym swapping is the #1 failure mode.** The humanizerai.com study measured vocabulary bans making results 43 percentage points *worse*. Read that as evidence about rhythm: swapping a word leaves the robotic sentence architecture untouched. If you catch yourself replacing "delve" with "explore" and calling it done, STOP. The sentence needs structural rebuild, not a word swap. See the Critical Research section.

4. **The model strips quoted material.** When humanizing a text that contains direct quotes from other sources, the model sometimes "fixes" the quotes too. Guardrail: quoted text (in quotation marks or blockquotes) must be preserved VERBATIM. Only humanize the author's own prose around quotes.

5. **Zero contractions ≠ formal intent.** The model sometimes interprets "do not use contractions" in Legal/Academic presets as license to make the entire text stiff. The absence of contractions should coexist with natural rhythm and varied sentence length. Formal does not mean robotic.

6. **Em-dash removal can be too aggressive.** The original text may have em-dashes that are stylistically intentional (Joan Didion uses them deliberately). The rule is: limit to 2 per paragraph, not zero. When the source text has a clear em-dash style, preserve it.

7. **P38 (Paragraph-Reshuffling Immunity) is the hardest pattern to fix.** Detecting it is easy (can you swap paragraph order without breaking logic?). Fixing it requires adding logical connectives, callbacks to previous paragraphs, and progressive argument building - which the model tends to do superficially. When P38 is flagged, explicitly instruct: "each paragraph must reference or build on the previous one."

## Personality & Soul

Avoiding AI patterns is half the job. The other half is having **soul**. Clean text without voice is a well-dressed corpse.

### Signs of "soulless" text

- All sentences the same length and structure
- No opinion - just neutral reporting
- No doubt, contradiction, or mixed feelings
- First person absent where it would fit
- No humor, edge, or personality
- Reads like a press release or Wikipedia stub

### How to restore life

| Technique | Example (AI -> Human) |
|---|---|
| **Have an opinion** | "The results are mixed" -> "Honestly, I'm not sure what to make of this" |
| **Vary the rhythm** | Short sentence. Then one that takes its time getting where it's going. |
| **Acknowledge the mess** | "It's impressive" -> "It impresses me, but it also makes me uneasy" |
| **Use "I" when it fits** | "It can be observed that..." -> "I keep coming back to this because..." |
| **Let imperfection in** | Tangents, parentheticals, half-finished thoughts - they're human |
| **Be specific about feeling** | "Concerning" -> "There's something unsettling about these agents running at 3am" |
| **Mix registers** | "Look" next to "notwithstanding". English loves this collision |
## Voice Calibration - Presets

> Full examples and detailed characteristics in `references/presets.md`

### 🖋️ Essay (default)
Tone of an English essayist. Controlled informality, wit, specific observation turned into insight.
Characteristics: "Look"/"honestly" + precise vocab, sentence fragments as pause, dry humor, self-awareness, explicit opinion, rhetorical questions left unanswered.

### 📰 Journalistic
Tone of the NYT or The Atlantic. Maximum clarity, concrete data, no fluff.
Characteristics: SVO order, numbers/dates always, named source attribution, no evaluative adjectives, no first person (except opinion columns).

### 🎓 Academic
Formal but not bureaucratic. Terminological rigor without officialese.
Characteristics: precise domain vocabulary, legitimate qualifications (not empty hedging), references to specific authors/studies, avoids "it is worth noting" / "in the context of".

### 💬 Corporate Informal
Startup email, professional Slack. Direct, light, no corporate speak.
Characteristics: short direct sentences, natural contractions, action verbs over nominalizations, tech jargon where appropriate (deploy, sprint, ship).

### 📱 Social Post
LinkedIn or Twitter/X. Short, opinionated, hook in the first line.
Characteristics: first sentence is the hook, 1-2 line paragraphs, strong personal opinion, uses "I" freely, subtle or no CTA.

### 💬 Casual/DM
Maximum orality. Stream of consciousness allowed.
Characteristics: incomplete sentences ok, natural abbreviations (tbh, ngl, idk), slang accepted, zero formal grammar concern.

### ⚖️ Legal / Formal
Briefs, memos, formal notices. High register with deliberate conventions.
Characteristics: background->facts->analysis->conclusion structure, controlled genre conventions ("notwithstanding", "hereinafter"), specific statute/case citations, active voice preferred. Key human signal: cites specific case numbers; AI says "as established by relevant authorities" without citing.

### 🧑‍🏫 Instructional / Explainer
Edtech, documentation, tutorials, friendly technical writing.
Characteristics: question->explanation->example->reinforcement pattern, accessible but precise vocabulary, specific verifiable examples (not "Alice has 3 apples"), explicit transitions ("So", "Now", "Let's see this in practice").
## Humanization Process

### Step 0 - 📊 Quantitative Semantic Ablation Measurement

Before any rewriting, generate a metrics mini-report:

```
📊 ABLATION REPORT (pre-humanization)
• TTR (Type-Token Ratio): {value}  -> below 0.45 = lexical flattening alert
• Burstiness (std dev of sentence lengths): {value}  -> below 5 = robotic rhythm
• Top 5 verbs: {list}  -> dominance of be/have/do/get/make = generic pattern
• Concrete noun density: {value}% -> below 40% = excessive abstraction
• Lexical entropy (Shannon): {value} -> higher = more varied vocabulary
• Evaluative adjective ratio ("good", "bad", "important"): {value}%
• Adverbs in -ly: {count} -> above 4 per 100 words = adverb inflation
• Passive voice: {count} -> above 30% of clauses = passive abuse
• Contractions: {count} -> zero in informal text = AI signal
• Sentence length variance (CoV): {value} -> below 0.3 = AI uniformity (human EN ~ 0.5)
• Mean sentence length (MSL): {value} words -> below 15 or above 25 uniformly = pattern
```

> **How to calculate**: TTR = unique tokens / total tokens. Burstiness = standard deviation of word count per sentence. Entropy = -sum p(x)*log2 p(x) over vocabulary. Sentence length variance = coefficient of variation (std/mean). Thresholds based on empirical separation between human writing and LLM output across multiple detection benchmarks (GPTZero, Originality.ai, Copyleaks).

**Empirical baselines (calibration targets from published research):**

| Metric | AI typical | Human typical | Source |
|---|---|---|---|
| TTR (Type-Token Ratio) | 0.455 | 0.553 | SSRN stylometric study |
| Burstiness (sentence length std dev) | ~0.00 | ~+0.70 | GPTZero methodology |
| Intrinsic dimensionality | ~7.5 | ~9.0 | Tulchinskii et al., NeurIPS 2023 |
| Sentence length CoV | <0.30 | ~0.50 | brandonwise/humanizer statistical model |
| Paragraph length CoV | <0.30 | ~0.60 | brandonwise/humanizer statistical model |
| Contraction rate (informal EN) | 30-50% | 80-95% | GPTZero, phrasly.ai analysis |
| Passive voice % | >30% | 10-20% | Copyleaks detection signals |

**Interpretation:** If your measured values are in the "AI typical" column, the text will likely be flagged. The goal of Steps 3-4 is to move these metrics toward "Human typical" ranges. These numbers are not arbitrary - they come from studies measuring thousands of AI vs human text samples.
### Step 0.5 - 🎯 Automatic Type Detection and Preset Selection

If the user **did not specify** a preset, detect automatically from content:

| Signal in text | Suggested preset |
|---|---|
| Legal citations, case numbers, "pursuant to", "hereinafter" | ⚖️ Legal |
| Technical jargon, code, APIs, framework names | 💬 Corporate Informal |
| Academic references ("et al.", methodology, hypothesis, p-value) | 🎓 Academic |
| Short text (<300 words), opinionated, 1st person, no formal structure | 📱 Social Post |
| Text ≤100 words, incomplete sentences, abbreviations, slang | 💬 Casual/DM |
| "Step by step", "let's see", didactic examples | 🧑‍🏫 Instructional |
| ≥1500 words, narrative, no dominant jargon | 🖋️ Essay |
| **No clear signal** | 🖋️ Essay (fallback) |

**Fallback rules:**
1. If there's **conflict** between signals (e.g., technical jargon + legal citation), ask the user.
2. If text has **multiple registers** (e.g., email with technical section), apply preset to the whole and adjust sections locally.
3. Detected preset can be **overridden** at any point by the user.

> **Output**: `🎯 Type detected: [type] -> Preset: [preset]` (1 line in report)
### Step 1 - 🔍 Diagnosis with Structured Checklist

Systematically walk through each category. Mark ✓ (found) or ✗ (absent).

| Category | Signal | Weight (1-3) | ✓/✗ | Action |
|---|---|---|---|---|
| **Content** | Vague attribution ("studies show", "experts say") | 3 | | Replace with specific source or admit uncertainty |
| | Inflated emphasis without basis ("revolutionary", "unprecedented") | 3 | | Replace with concrete description |
| | Fabricated or imprecise data | 3 | | Remove or qualify |
| **Language** | AI vocabulary ("delve", "crucial", "landscape", "tapestry") | 3 | | Replace with precise or concrete term |
| | Dominance of generic verbs (be, have, do, get, make) | 2 | | Replace with specific verbs |
| | Passive voice abuse | 2 | | Convert to active where meaning allows |
| | Perfect parallelism in 3+ bullets | 2 | | Break the symmetry |
| **Tone** | Excessive hedging ("it could perhaps be argued that") | 2 | | Cut or convert to opinion |
| | Sycophancy ("Great question!", "Absolutely!") | 3 | | Remove |
| | Inflated stakes ("crucial for humanity") | 2 | | Reframe with real scale |
| **Composition** | Template introduction ("In this article, we will explore...") | 3 | | Cut, go straight to the point |
| | Template conclusion ("in summary", "in conclusion") | 3 | | Rewrite with a turn or question |
| | Artificial transitions ("furthermore", "moreover", "additionally") | 2 | | Use natural connectives or cut |
| **Style** | Excessive formatting (bold/em-dash overuse) | 1 | | Moderate |
| | Emoji on every bullet (ChatGPT pattern) | 1 | | Remove or use 1 max |
| | Unsolicited markdown (headers, auto-bullets in prose) | 2 | | Remove - it's instruction-tuning, not author choice |
| **English-specific** | Em-dash cascade (3+ per paragraph) | 2 | | Replace most with commas, periods, or parentheses |
| | Tricolon abuse (rule of three in every sentence) | 2 | | Vary groupings |
| | "It's worth noting" / "It bears mentioning" | 3 | | Cut entirely - just say the thing |

> **Decision rule**: if ≥5 weight-3 signals found -> review_mode mandatory.
### Step 2 - 🧹 Pattern Removal

**CRITICAL: This step identifies and RESTRUCTURES. It does NOT synonym-swap.**

> ⚡ **RHYTHM FIRST.** Experimental validation (Matsui 2025, desklib + Binoculars detectors) found that **restructuring sentence rhythm accounts for ~90% of achievable improvement** in humanization. Vary sentence lengths and diversify sentence openings BEFORE touching vocabulary. The order matters.

Per the humanizerai.com study (2026), vocabulary bans alone make results worse. Replacing "delve" with "explore" changes nothing that matters: the rhythm underneath is identical. What works is changing the sentence's architecture - its length, rhythm, clause structure, and information density.

**Step 2 execution order:**
1. **Rhythm restructuring FIRST** - Vary sentence lengths (mix <15 words with >30 words), diversify openings (prepositional phrases, subordinate clauses, connectives), relocate clause elements
2. **Then vocabulary/pattern fixes** - Apply the pattern corrections from reference files
3. **Never bare-delete** - When removing a transition or ornamental word, always restructure the surrounding sentence (see Connective-Preserving Edits in `references/patterns-composition.md`)

> ⚠️ **Critical interaction:** Removing an ornamental adverb (like "markedly") WITHOUT restructuring the sentence was experimentally shown to INCREASE detection scores (+0.72 logit worse). The shorter, more uniform sentence fits AI cadence better. Always restructure when removing adverbs.

**Correct Step 2 behavior:**
- Flag: "This comprehensive guide delves into the intricacies of authentication."
- WRONG fix: "This thorough guide explores the details of authentication."
- RIGHT fix: "The auth system uses JWTs. Tokens expire after 15 minutes."

The first "fix" is synonym-swapping - same rhythm, same length, same predictability. The second is structural paraphrasing - different length, different density, different voice. DetectGPT accuracy drops from 70.3% to 4.6% with structural paraphrasing (RAID Benchmark, ACL 2024). It does NOT drop with synonym replacement.

Consult reference files and apply structural corrections:

- `references/summary.md` - skill navigation index
- `references/patterns-content.md` - vague attributions, inflated emphasis
- `references/patterns-language.md` - AI vocabulary, copula avoidance, parallelisms
- `references/patterns-style.md` - formatting, em-dash, bold, emojis
- `references/patterns-tone.md` - sycophancy, hedging, stakes inflation
- `references/patterns-composition.md` - templates, predictable conclusions
- `references/patterns-english-specific.md` - contractions, passive voice, register mixing
### Step 3 - ♻️ Entropy Restoration

Where text has been flattened by AI:

| Problem | Solution | Example |
|---|---|---|
| Dead metaphor | Replace with vivid image | "Inflection point" -> "It's like running out of gas in the middle of a bridge" |
| Generic term | Restore domain vocabulary | "Positive impact" -> "17% reduction in churn" |
| Predictable template | Reorganize non-linearly | Invert order: example -> context -> thesis |
| Excessive abstraction | Insert concrete data or anecdote | "Many people struggle" -> "Three of my neighbors have had the same problem" |
| Monotone rhythm | Vary sentence lengths | Alternate short sentences with long ones |

> ⚠️ **Ablation alert**: if a passage lost specificity without justification, annotate: "⚠️ This passage lost concreteness - the original likely had [data / example / qualification]."
### Step 4 - 💬 Voice Injection

Apply the chosen preset (or mirror a voice sample provided):

- Vary rhythm (intentional burstiness)
- Add opinion/personal position
- Mix high and low register
- Include controlled imperfections (tangents, parentheses, fragments)
- Use contractions naturally (don't -> do not only when emphasis demands it)

> **When the user provides a voice sample**: read first and annotate: sentence lengths, vocabulary level, how paragraphs begin, punctuation habits, verbal tics, register tendencies. **Mirror** - don't just remove patterns, replace them with the sample's patterns.
### Step 5 - 🔥 Final Anti-AI Pass (Binary Checklist)

Check each item. Mark ✓ (ok) or ✗ (failed). If any item fails, fix before proceeding.

| # | Check | ✓/✗ |
|---|---|---|
| 1 | Sentence lengths vary? (min 3 distinct sizes per paragraph) | |
| 2 | Mechanical transitions eliminated? ("Furthermore", "Moreover", "Additionally" clusters) | |
| 3 | Abstract placeholders replaced with concrete terms? | |
| 4 | At least 1 opinion, doubt, or personal feeling present? | |
| 5 | No template openings/closings survived? | |
| 6 | Contractions used naturally in informal presets? | |
| 7 | Factual information from original 100% intact? | |
| 8 | Voice preset consistent from start to finish? | |
| 9 | No sentence reads like a press release or Wikipedia stub? | |
| 10 | Read aloud, does it sound like a real person writing? | |
| 11 | **Paragraph cohesion:** Each paragraph's first sentence states its claim? | |
| 12 | **Sentence chaining:** Each sentence linked to previous by connective OR echoed key word? | |
| 13 | **No bare deletions:** Logical discourse markers (However, Thus, Although) preserved where needed? | |

**Rule**: if ≥2 items fail -> fix and re-check. If all ✓ -> proceed.

> **Cohesion guidance (checks 11-13):** Choppy, disconnected prose is itself an AI-cleanup tell. After editing, re-read each paragraph top to bottom: (a) first sentence states what the paragraph covers, (b) every subsequent sentence chains to the previous one, (c) contrast/continuity openers survive where the argument needs them. See `references/patterns-composition.md` for Connective-Preserving Edits and Logical Discourse Markers to Preserve.
### Step 5.5 - 📊 Post-Rewrite Scoring

Evaluate the result across 5 dimensions (0-100 each, weighted average):

| Dimension | Weight | Evaluation criteria |
|---|---|---|
| **AI pattern removal** | 30% | How many Step 1 patterns were eliminated? Any remaining? |
| **Naturalness** | 25% | Burstiness >5? Varied rhythm? Voice present? Sounds like a real person? |
| **Factual completeness** | 20% | All original information preserved? Data, names, numbers intact? |
| **Voice consistency** | 15% | Was the preset maintained throughout? No register jumps? |
| **Readability** | 10% | Sentences flow? Natural connectives? Clear logic? |

**Final score** = sum (dimension x weight)

**Decision criteria:**
- **≥ 80**: ✅ Approved -> proceed to delivery (Step 6)
- **60-79**: ⚠️ Almost -> run Anti-AI Pass again focusing on weak dimensions
- **< 60**: ❌ Fail -> rewrite with different approach (change preset, invert technique order, or shift focus between removal vs. voice injection)

> **Output format**:
> ```
> 📊 POST-REWRITE SCORE
> • AI removal:          {0-100} (x0.30) = {partial}
> • Naturalness:         {0-100} (x0.25) = {partial}
> • Factual completeness:{0-100} (x0.20) = {partial}
> • Voice consistency:   {0-100} (x0.15) = {partial}
> • Readability:         {0-100} (x0.10) = {partial}
> • TOTAL:               {score}/100 -> {✅/⚠️/❌}
>
> 📊 METRICS DELTA (pre -> post)
> • TTR:              {pre} -> {post} ({+/-}%)
> • Burstiness:       {pre} -> {post} ({+/-}%)
> • Shannon entropy:  {pre} -> {post} ({+/-}%)
> • Adverbs -ly/100w: {pre} -> {post}
> • Passive voice %:  {pre} -> {post}
> • MSL (mean len):   {pre} -> {post}
> • Sent. len. CoV:   {pre} -> {post}
> • Concrete nouns:   {pre}% -> {post}%
> ```
>
> **Interpreting the delta**: TTR, burstiness, entropy, and concrete nouns should **rise**. Adverbs in -ly and passive voice should **fall**. MSL and CoV should **approach human values** (MSL varies by genre; CoV ~ 0.5).
### Step 6 - 📦 Formatted Delivery

| Mode | Content delivered |
|---|---|
| full_mode | Metrics (Step 0) + Checklist (Step 1) + Draft rewrite + Self-critique (Step 5) + Final version + Summary of changes |
| direct_mode | Final version + Synthetic report (1 line per corrected pattern) |
| review_mode | Final version + Full checklist + Before/after metrics + Ablation alerts |
## Iterative Loop and Strategy Fallback

Step 5.5 scoring enables automatic iteration when the result doesn't hit threshold.

### Standalone Behavior (no external loop skill)

```
iteration = 0
MAX_ITERATIONS = 3

while iteration < MAX_ITERATIONS:
    iteration += 1
    execute Steps 2-5.5
    
    if score >= 80: DELIVER
    if score 60-79:
        focus on dimensions with score < 70
        continue
    if score < 60:
        CHANGE STRATEGY (see table below)
        continue

if MAX_ITERATIONS reached: deliver best version + limitation note
```

### Strategy Fallback Table

When score < 60, change approach on next iteration:

| Previous iteration | Next approach |
|---|---|
| Focus on pattern removal (Step 2 heavy) | Focus on voice injection (Step 4 heavy) |
| Focus on voice injection | Focus on restructuring (Step 3 - reorder flow, break templates) |
| Current preset doesn't work | Try adjacent preset (e.g., Essay -> Corporate Informal) |
| Long text with progressive degradation | Split into ~300 word blocks and process separately |

### Compatibility with External Loop Skills

This skill is **compatible** with loop orchestrators like `ralph-wiggum`, `goal`, or any skill implementing an external iterative cycle.

**Integration protocol:**

1. **Standardized input**: skill accepts text + preset (optional) + minimum score (optional, default 80)
2. **Structured output**: always returns the parseable `📊 POST-REWRITE SCORE` block
3. **Convergence signal**: when score >= threshold, emit `✅ HUMANIZATION COMPLETE (score: {N}/100)`
4. **Non-convergence signal**: when standalone iteration exhausts, emit `⚠️ BEST RESULT REACHED (score: {N}/100) - external iteration may continue`

> **For external loop skills**: use the numeric score from output as stopping criterion. The skill needs no state between calls - each invocation receives text (possibly already partially humanized) and returns result + score.
## The 29 AI Vocabulary Patterns (English)

The core detection list. These words and phrases are near-certain AI signals when they appear with high frequency. Based on Wikipedia's "Signs of AI Writing" + blader/humanizer's detection set + brandonwise/humanizer's 560-term tier system.

### Tier 1 - Zero Tolerance (cut on sight)

These NEVER appear in natural human writing at the frequency AI uses them:

`delve, tapestry, landscape (figurative), testament to, serves as a reminder, it's worth noting, it bears mentioning, the ever-evolving landscape, navigate (complexities/challenges), spearhead, multifaceted, pivotal, paramount, underscores, underpin, a testament to, in the realm of, it is important to note, this highlights, shed light on`

### Tier 2 - High Suspicion (replace when clustered)

Acceptable once per 1000 words. AI uses them 10-20x:

`crucial, vital, comprehensive, robust, leverage, foster, facilitate, embark, harnessing, utilize, endeavor, moreover, furthermore, additionally, subsequently, nonetheless, notwithstanding (in non-legal), overarching, intricate, nuanced, holistic, synergy, paradigm, catalyst, orchestrate, seamless, ecosystem (abstract), journey (figurative), unlock (figurative)`

### Tier 3 - Context-Dependent (flag if > 2 per 500 words)

Normal words that AI overuses through repetition:

`significant, enhance, innovative, dynamic, diverse, inclusive, sustainable, transformative, empower, streamline, optimize, cutting-edge, state-of-the-art, game-changer, disruptive, scalable, impactful, actionable, meaningful, compelling`

### Detection Rule

- 1 Tier-1 word = flag the sentence
- 3+ Tier-2 words in one paragraph = flag the paragraph
- 5+ Tier-3 words in one page = flag the text
- Any combination of 2+ Tier-1 words in 500 words = near-certain AI
## The Emerging Patterns (2026 Community Discoveries)

Patterns P31-P43 below were identified by HackerNews threads, Wikipedia's evolving editorial guidelines, and writing practitioner blogs throughout 2026. They represent AI behavior that is newer, subtler, and not yet covered by most humanizer tools. Source: Aboudjem/humanizer-skill research.

| # | Pattern | What to look for | Why it's a tell |
|---|---|---|---|
| P31 | Elegant Variation | "the artist", "the visionary creator", "the non-conformist painter" for the same person | AI avoids repeating a noun by cycling through increasingly florid synonyms. Humans just use the name or "he/she/they". |
| P32 | Collaborative Communication Leaking | "In this article, we will explore", "Let me walk you through" | Residue from the assistant persona bleeding into published text. |
| P33 | Placeholder Text / Mad Libs | `[Your Name]`, `[INSERT SOURCE URL]`, unfilled brackets | Template artifacts the user forgot to fill. Immediate credibility kill. |
| P34 | Chatbot Reference Markup Leaking | `citeturn0search0`, `oai_citation`, broken footnote refs | Internal citation markup from ChatGPT/Copilot leaking into output. |
| P35 | UTM Source Parameters | `utm_source=chatgpt.com`, `utm_source=openai` in URLs | Links copied directly from AI chat sessions without cleaning. |
| P36 | Sudden Style/Register Shift | Formal prose suddenly switching to casual mid-paragraph | Indicates pasted AI output spliced with human text (or vice versa). |
| P37 | Overattribution | "Featured in Wired, Refinery29, and other outlets" without substance | Listing media names without citing what was said or when. |
| P38 | Paragraph-Reshuffling Immunity | Paragraphs that could swap order without breaking the argument | AI generates paragraphs as independent blocks with no logical progression. Human arguments BUILD - each paragraph depends on the previous. |
| P39 | "Whether" Paragraph Closers | "Whether you prefer X or Y, the answer is..." | Formulaic wrap-up that pretends to acknowledge alternatives while saying nothing. |
| P40 | Symbolic Gloss / Meaning-Telling | "represents", "symbolizes", "speaks to broader" applied to mundane things | AI assigns cosmic significance to ordinary events. "The coffee spill represents the broader challenges of work-life balance." |
| P41 | Infomercial Engagement Hooks | "The catch?", "The kicker?", "Here's the thing.", "The brutal truth?" | Cheap rhetorical devices that create false drama. One per essay is fine. Every paragraph is AI slop. |
| P42 | Erratic Inline Bolding | Random mid-sentence bold spans with no shared logic or category | Bold without editorial purpose - the model is "highlighting" but there's no system. |
| P43 | The Treadmill Effect | "In other words", "Put simply", "Essentially" looping the same point | AI restates the same idea in different words across multiple sentences, creating the illusion of development without actually advancing the argument. |
| P44 | Content-Free Evaluation Sentences | "This is a noteworthy finding.", "These results are significant.", "This observation is important." | Standalone sentences that evaluate a finding's importance without adding any information - no data, no mechanism, no comparison, just a verdict. Distinct from P40 (Symbolic Gloss, which assigns cosmic significance) - P44 is empty verdicts. |

**Detection rule for emerging patterns:**
- P33-P35 (markup/placeholder leaks) = immediate flag, zero tolerance
- P38 (reshuffling immunity) = strongest structural tell. Test by mentally rearranging paragraphs - if the text reads identically, it's AI
- P43 (treadmill effect) = if you can delete a sentence and the paragraph loses zero information, that sentence is treadmilling
- P44 (content-free evaluation) = if a sentence just labels something as "important/significant/noteworthy" without explaining WHY, delete it or replace with the actual reason
## Evaluation with Jev (Optional)

When the harness has access to [TypeSafe Jev](https://docs.typesafe.ai), the evaluation steps (diagnosis, verification, scoring) can use Jev instead of inline LLM prompts.

**Jev advantages:**
- Calibrated probabilities (P(70%) = 70% real)
- Deterministic (same input → same output)
- ~50-100x cheaper than GPT-4 for evaluation
- 70-500ms vs 1-5s latency

### Discovery Protocol

The skill follows a priority order to detect Jev availability:

```
1. MCP Tool `jev_eval` configured in harness → use it
2. Model `typesafe/jev-latest` via OpenRouter → request it
3. Auxiliary slot (Hermes/Devin/Codex) with Jev → delegate
4. Fallback → inline evaluation via current LLM
```

> **Note:** Jev does diagnosis, verification, and scoring. The LLM still performs the actual rewriting (Steps 2-4).

### Related Files

| File | Description |
|------|-------------|
| `scripts/jev_questions.json` | 56 typed questions (Noul + Score) |
| `references/jev-integration.md` | Full protocol, request/response formats |

> **Full documentation**: See `references/jev-integration.md` for discovery details, harness-specific instructions, and request/response structures.

---

## Critical Research: Why Vocabulary Bans Alone FAIL

> "Vocabulary bans, one of the most commonly recommended techniques, actively hurt performance." - humanizerai.com, GPTZero bypass test (2026)

Much of this research was produced by measuring detector bypass rates. This skill uses the findings for what they reveal about **rhythm and sentence architecture**, not as a target - see Positioning above. The useful lesson is that what those studies actually measure is statistical shape (burstiness, perplexity, sentence length variance), not vocabulary. Replacing "delve" with "explore" preserves the robotic rhythm underneath, which is why the word swap fails.

**Effectiveness hierarchy (research-backed):**
1. **Structural paraphrasing** - the largest measured effect (RAID Benchmark, ACL 2024: DetectGPT accuracy 70.3% -> 4.6%)
2. **Burstiness injection** - sentence length variance, the strongest rhythm signal
3. **Perplexity increase** - secondary rhythm signal
4. **Vocabulary diversity** - TTR 45.5 -> 55.3 (SSRN)
5. **Synonym swapping** - DOES NOT WORK as standalone technique

None of these numbers proves human authorship, and none of them should be used to decide whether a text is "done".
## Contraction Rules (English-Specific)

AI avoids contractions far more than humans. One of the most reliable statistical signals.

| Context | Human | AI |
|---|---|---|
| Informal email | Contractions everywhere | Mixed or avoids |
| Blog post | 80%+ contracted | 40-60% contracted |
| Academic paper | Minimal (correct) | Minimal (correct) |
| Documentation | Moderate | Often avoids entirely |

**Rule**: In Essay, Corporate Informal, Social Post, and Casual/DM presets, zero contractions = immediate AI signal. Force natural contractions in Step 4. **Exception**: Academic and Legal presets may correctly avoid contractions.
## Regression Test Suite

6 test cases covering: corporate email, academic paragraph, legal text, blog template, AI hedging, generic explainer. Each test runs in full_mode and verifies output matches expected human-sounding result.

> Full test cases in `references/tests.md`
## Limits and Contraindications

**Do NOT use:** Safety-critical texts (drug labels, aviation), original contracts/legal documents (normative reference), bilingual literal translations, content for automated evaluation (TOEFL).

**Use with caution:** Technical texts with formal notation (preserve equations/code, humanize only prose), non-native English writers (colloquialisms may not match ESL author's voice).
## References

| Source | Link | Key finding |
|---|---|---|
| Wikipedia - Signs of AI writing | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing | 24 pattern categories with real examples |
| blader/humanizer (29 patterns) | https://github.com/blader/humanizer | Original skill, 10.6K stars |
| brandonwise/humanizer (statistical) | https://github.com/brandonwise/humanizer | 560-term vocab filter, burstiness/TTR |
| Aboudjem/humanizer-skill (43 patterns) | https://github.com/Aboudjem/humanizer-skill | P31-P43 emerging patterns, 5 voices, scoring |
| matsuikentaro1/humanizer_academic | https://github.com/matsuikentaro1/humanizer_academic | 34 patterns for medical writing, rhythm-first validation |
| Matsui K (2025) - PubMed AI vocabulary | doi:10.5334/pme.1929 | Quantified AI-influenced vocabulary shifts in medical writing post-ChatGPT |
| tropes.fyi | https://tropes.fyi/directory | Community AI trope catalog |
| The Register - Semantic Ablation | https://www.theregister.com/2026/02/16/semantic_ablation_ai_writing/ | Meaning-loss through AI polishing |
| RAID Benchmark (ACL 2024) | doi:10.18653/v1/2024.findings-acl | Structural paraphrasing: DetectGPT 70.3% -> 4.6% |
| Tulchinskii et al. (NeurIPS 2023) | Intrinsic dimension analysis | Human ~9 dims vs AI ~7.5 |
| SSRN stylometric study | Vocabulary diversity analysis | Human TTR: 55.3 vs AI: 45.5 |
| humanizerai.com - GPTZero bypass | https://humanizerai.com/blog/gptzero-bypass-test-2026 | Vocab bans HURT; structural change wins by 43pp |
| GPTZero | https://gptzero.me | Burstiness + perplexity as primary signals |

---

*v1.1.0 - Based on Portuguese [humanizar](https://github.com/fabricioctelles/skills) by @fabriciotelles. Combines pattern detection (blader), statistical measurement (brandonwise), emerging patterns (Aboudjem), and rhythm-first methodology (Matsui) with voice injection, entropy restoration, and iterative scoring.*
