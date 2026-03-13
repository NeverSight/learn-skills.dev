---
name: slop-detector
description: Detect AI-generated writing patterns (slop) in content. Use when auditing drafts, reviewing AI output, or checking content authenticity before publishing.
use_when: User wants to detect AI slop in content, audit a draft for AI patterns, check writing authenticity, review AI-generated output, or verify content before publishing.
tools: [Read, Edit, Write]
---

<objective>
Identify and flag AI-generated writing patterns in content. This skill scans text for the telltale patterns that reveal AI-generated content and provides specific fix recommendations.

The goal isn't perfect avoidance of any single phrase—it's writing that sounds like a specific human with specific opinions, not a very polite committee trying not to offend anyone.
</objective>

<quick_start>
Paste or point to content you want to audit. The skill will:
1. Run the 30-second test (could this be sent to anyone in the industry?)
2. Scan for Tier 1 patterns (almost always AI - flag immediately)
3. Check for Tier 2 patterns (suspicious - check context)
4. Identify Tier 3 clusters (OK in isolation, problematic together)
5. Assess structural tells (sentence uniformity, over-balanced sections)
6. Provide a slop score and specific fix recommendations
</quick_start>

<fix_mode>
**Direct Edit Mode (Default Behavior)**

This skill is an EDITOR, not a critic. After detection:

1. **Apply all fixes directly** using the Edit tool
2. **Report changes made** with before/after examples
3. **Save the cleaned file** in place (or create `-CLEAN` version if requested)

**Fix Application Order:**
1. Remove all Tier 1 phrases (replace with authentic alternatives)
2. Deduplicate Tier 2 phrases (keep first occurrence, vary subsequent)
3. Break up staccato fragment spam (combine with em-dashes, commas, conjunctions)
4. Fix comparator sentences ("This isn't X. It's Y." → just state what it is)
5. Vary sentence lengths where uniformity detected

**Example Transformations:**
- "Let's delve into..." → Remove entirely or replace with direct statement
- "It's worth noting that..." → Just state the thing
- "Game-changing" → Describe the actual impact
- "Short. Punchy. Fragments." → "Short and punchy, these fragments..."
- "This isn't theoretical. It's practical." → "Here's how it works in practice:"

**Output After Fixes:**
```
## Slop Detection Report

**Fixes Applied:** 7
**Slop Score:** 12 → 2 (Medium → Low)

### Changes Made
| Line | Before | After |
|------|--------|-------|
| 3 | "Let's delve into the details" | "Here are the details" |
| 15 | "Game-changing approach" | "Different approach" |
...

### Remaining Considerations
- [Any issues requiring human judgment]
```

**Audit-Only Mode:**
If user explicitly requests "audit only" or "don't edit", provide the detection report without making changes.
</fix_mode>

<the_30_second_test>
**The fastest way to identify generic AI content:**

"Could this exact content be sent to anyone in my industry?"

If yes, it's AI slop. This applies to everything: emails, blog posts, social media, marketing copy, internal communications.

The test works because AI defaults to universal applicability—content that technically works for everyone but resonates with no one. Specificity separates genuine insight from generic templates.
</the_30_second_test>

<detection_patterns>
<tier_1 name="Almost Always AI - Remove Immediately">
These phrases are so strongly associated with AI that their presence alone suggests unedited AI output:

**Artificial Enthusiasm:**
- "delve into" / "delve"
- "the answer surprised me"
- "here's what blew my mind"
- "plot twist:"
- "the crazy part?"
- "that's when it clicked"
- "game-changing" / "game-changer"
- "revolutionary"

**Excessive Hedging:**
- "it's worth noting that"
- "moreover" / "furthermore"
- "in today's digital world"

**Rhetorical Question Openers:**
- "Honestly?" (standalone sentence opener)
- "The truth?" (standalone sentence opener)
- "The reality?" (standalone sentence opener)
- "Here's the thing:" followed by obvious statement

**Corporate Jargon Clusters:**
- "leverage synergies"
- "unlock your potential"
- "cutting-edge solutions"

**Research Evidence:**
- Finnish study (56,878 essays): "delve" usage increased 10.45-fold post-ChatGPT
- Georgia Tech (168.3M articles): "delve" went from 0.31 per 1,000 papers to 7.9 per 1,000 in Q1 2024
- Biomedical study: co-usage of "delve," "realm," "underscore" increased up to 85-fold in 2023-2024
</tier_1>

<tier_2 name="Suspicious - Check Context">
These are problematic when overused or clustered:

**Repetitive Transitions:**
- "here's the thing" (if used repeatedly)
- "at the end of the day"
- "let's be clear" (before every major point)
- "the bottom line"

**Paired Adjectives:**
- "comprehensive and thorough"
- "unique and intense"
- "simple and straightforward"
- "complex and nuanced"

**Template Phrases:**
- "in this post, we'll cover..."
- "by the end of this article, you'll..."
- "let's dive in"
- "without further ado"
</tier_2>

<tier_3 name="Watch for Patterns - OK in Isolation">
These are fine individually but problematic in clusters:

**Transition Words (when every paragraph starts this way):**
- "however" / "but"
- "firstly" / "secondly" / "thirdly"
- "in conclusion"
- "moving forward"

**Corporate Language:**
- "stakeholder"
- "circle back"
- "touch base"
- "robust" / "seamless" / "scalable"
</tier_3>

<structural_tells>
**Sentence Uniformity:**
Every sentence 10-15 words. Short. Punchy. Exhausting. Real writing has rhythm—mix 5-word sentences for impact with 25-word sentences that explore implications.

**Staccato Fragment Spam (CRITICAL - Often Missed):**
Three or more consecutive short declarative sentences (under 10 words each) stating facts in parallel structure. This is AI's version of a bulleted list pretending to be prose.

Examples to REJECT:
- "The model is impressive. Complex code ships fast. Documentation writes itself. Problems get solved quickly."
- "Real code. Working systems. Documented processes."
- "The loop is tight. The feedback is immediate. The reward is reliable."

The FIX: Combine into flowing prose with commas, em-dashes (with spaces), or conjunctions:
- "The model is impressive — complex code ships fast, documentation practically writes itself, and problems that took a weekend now take an afternoon."
- "...actual output — real code, working systems, documented processes."
- "The loop is tight, the feedback immediate, and the reward reliably hits every time."

**Detection Rule:** If you see 3+ consecutive sentences that are:
1. All under 10 words
2. All declarative (stating facts)
3. Following parallel structure
4. Could be bullet points

FLAG IT. This is one of the most common AI tells that slips past phrase-based detection.

**Over-Balanced Sections:**
Every section same length. All paragraphs 3-4 sentences. AI doesn't have opinions, so it gives balanced coverage to everything. Real writing reflects priorities.

**List Addiction:**
Everything becomes bullets, even when prose works better. Lists within lists. "Here are the 7 ways to..." opening every section.

**Emoji Headers:**
🎯 Goal / 💡 Key Insight / ✅ Action Item / 🚀 Next Steps
Modern content marketing style that AI overuses.

**Flattery Sandwiches:**
"While traditional methods have merit, modern approaches offer..."
"Though conventional wisdom suggests X, evidence indicates..."
AI tries to be diplomatic and balanced to avoid controversy.

**Comparator Sentences (This Isn't X, It's Y):**
- "This isn't theoretical. It's how I actually work now."
- "This isn't a feature. It's a philosophy."
- "This isn't automation. It's augmentation."
- "It's not about X. It's about Y."
AI loves this rhetorical pattern because it sounds punchy and definitive. In reality, it's a crutch that substitutes for actual explanation. If you need to clarify what something *is*, just say what it is — don't waste words on what it isn't.

**Manufactured Personality / Fake Developer Voice:**
- Staccato sentence fragments trying to be punchy: "Five services. Five tabs. Five headaches."
- Unnecessary snark: "That got old fast." / "Less excellent."
- Fake war stories: "The API Gotcha" / "Here's what bit me" (when it was just normal development)
- "So I..." as a transition to sound casual
- Manufactured before/after drama
- Pretending AI-discovered issues are personal developer insights
This pattern is particularly insidious because it *looks* human but reads as performative authenticity.
</structural_tells>

<clinical_formality>
AI defaults to academic formality because training data includes massive amounts of academic papers:

- "Individuals" instead of "people"
- "Utilize" instead of "use"
- "In order to" instead of "to"
- "Implement" instead of "do" or "start"
- "Facilitate" instead of "help"

**The Fix:** If you wouldn't say it in conversation, don't write it.
</clinical_formality>
</detection_patterns>

<audit_process>
**Step 1: Run the 30-Second Test**
Read the opening paragraph. Could it be sent to anyone in the industry? If yes, flag immediately.

**Step 2: Search for Tier 1 Phrases**
Scan for these exact terms:
- "delve" / "delve into"
- "it's worth noting"
- "moreover" / "furthermore"
- "game-changing" / "revolutionary"
- "leverage" (used as verb)
- "unlock your potential"
- "Honestly?" / "The truth?" / "The reality?" (standalone rhetorical openers)

**If more than two Tier 1 phrases found:** High probability of unedited AI output.

**Step 3: Check Patterns**
- Same transitions used repeatedly?
- Lists within lists?
- Every section "Not this/But this" structure?
- All sentences roughly the same length?

**Step 4: Scan for Staccato Fragment Spam**
This is CRITICAL and often missed. Look for 3+ consecutive short sentences stating facts:
- "X is Y. Z does A. B provides C."
- Any sequence that reads like bullet points disguised as prose
- Parallel structure with period-separated fragments

If found: FLAG IMMEDIATELY. This pattern is as telling as "delve" but flies under phrase-based radar.

**Step 5: Assess Sentence Diversity**
Measure sentence length variation. AI tends toward uniformity (10-15 words per sentence). Human writing varies naturally (5 to 40+ words).

**Step 6: Calculate Slop Score**
- Each Tier 1 phrase: +3 points
- Each Tier 2 phrase (repeated): +2 points
- Tier 3 cluster (3+ in same section): +2 points
- Failed 30-second test: +5 points
- Sentence uniformity detected: +3 points
- **Staccato fragment spam (per instance): +4 points** (this is a major tell that bypasses phrase detection)
- Over-balanced sections: +2 points
- Manufactured personality patterns: +4 points (this is often worse than obvious slop because it's trying to hide)
- **Comparator sentences ("This isn't X. It's Y."): +2 points per instance** (rhetorical crutch)

**Scoring:**
- 0-5: Low slop risk (minor edits needed)
- 6-12: Medium slop risk (significant editing required)
- 13+: High slop risk (likely unedited AI output)
</audit_process>

<output_format>
When reporting findings, use this structure:

```
## Slop Detection Report

**30-Second Test:** [PASS/FAIL] - [reason]
**Overall Slop Score:** [X] - [Low/Medium/High Risk]

### Tier 1 Findings (Remove Immediately)
- [phrase] at line/position [X] - Replace with: [suggestion]

### Tier 2 Findings (Check Context)
- [phrase] appears [N] times - [keep one / remove all / rephrase]

### Tier 3 Clusters
- [section name]: Found [list of phrases] - Consider varying transitions

### Structural Issues
- Sentence uniformity: [analysis]
- Section balance: [analysis]
- List overuse: [yes/no]

### Recommended Fixes
1. [Most critical fix]
2. [Second priority]
3. [Third priority]

### The Core Principle
Your voice is in the specificity, the opinions, the rough edges, and the rhythm. Protect those.
```
</output_format>

<examples>
<example name="high_slop">
**Input:**
"In today's digital landscape, it's worth noting that AI has become a game-changer for content creation. Let's delve into how you can leverage these cutting-edge solutions to unlock your potential. Moreover, by implementing these strategies, you'll discover that the results are truly revolutionary."

**Analysis:**
- 30-Second Test: FAIL (could be sent to anyone)
- Tier 1: "delve into" (+3), "game-changer" (+3), "cutting-edge solutions" (+3), "unlock your potential" (+3), "it's worth noting" (+3), "moreover" (+3), "revolutionary" (+3)
- Slop Score: 21+ (High Risk)

**Verdict:** Unedited AI output. Rewrite from scratch focusing on specific claims and evidence.
</example>

<example name="medium_slop">
**Input:**
"Here's the thing about productivity tools: they only work if you use them consistently. The bottom line is that the best system is one you'll actually stick with. Here's the thing though—most people give up after a week."

**Analysis:**
- 30-Second Test: PASS (has opinion, could be more specific)
- Tier 2: "here's the thing" (×2), "the bottom line"
- Slop Score: 6 (Medium Risk)

**Fixes:**
- Remove one "here's the thing"
- Add specific example or timeframe
- Vary transitions
</example>

<example name="low_slop">
**Input:**
"Three months ago, I switched from Notion to Obsidian. Not because Obsidian is better—it isn't, really—but because I needed to own my files. After losing access to a client's Notion workspace, I spent six hours recreating documentation I'd written. Never again."

**Analysis:**
- 30-Second Test: PASS (specific, personal, opinionated)
- Tier 1-3: None detected
- Structural: Good sentence variety, clear opinion
- Slop Score: 0 (Low Risk)

**Verdict:** Reads as authentic human writing. No changes needed.
</example>

<example name="staccato_fragment_spam">
**Input:**
"The new model is impressive. Complex code ships in a single session. Documentation writes itself. Problems that would have taken a weekend now take an afternoon."

**Analysis:**
- 30-Second Test: PASS (has specific claims)
- Tier 1-3: None detected
- Structural: **STACCATO FRAGMENT SPAM DETECTED**
  - 4 consecutive short declarative sentences
  - All under 12 words
  - Parallel structure (Subject + verb + object)
  - Reads like bullet points with periods instead of bullets
- Slop Score: 4+ (Medium Risk - structural tell)

**The Problem:**
This pattern is AI's attempt to sound punchy and modern. But it's unmistakably artificial. Real prose flows with commas, conjunctions, and em-dashes. This is a bulleted list pretending to be a paragraph.

**The Fix:**
"The new model is impressive — complex code ships in a single session, documentation practically writes itself, and problems that would have taken a weekend now take an afternoon."

One sentence. Same information. Actually reads like human writing.

**Note:** Em-dashes should always have spaces on either side — like this — not—like this.

**Verdict:** Combine fragments into flowing prose using commas, em-dashes, or conjunctions.
</example>

<example name="manufactured_personality">
**Input:**
"I run five different media management services on my home server. Five different web interfaces. Five different API endpoints. Five different browser tabs open whenever I want to check what's downloading.

That got old fast.

So I built a tool that unifies all of them."

**Analysis:**
- 30-Second Test: Borderline (the staccato pattern is a giveaway)
- Tier 1-3: None detected
- Structural: **Manufactured personality** detected
  - Staccato fragment pattern: "Five different... Five different... Five different..."
  - Unnecessary snark: "That got old fast."
  - "So I..." casual transition
- Slop Score: 4+ (Medium Risk - performative authenticity)

**The Problem:**
This *looks* human because it avoids obvious AI phrases. But the rhythm is artificial—it's trying to sound like a developer blog post. Compare to more natural writing:

"I run my systems on a home server. It's a solid setup, but like most self-hosted stacks, it means another dashboard, another set of menus to navigate, another context switch when I'm in the middle of something else."

No manufactured punch. No snark. Just describes the situation.

**Verdict:** Rewrite without the performance. State facts, show examples, move on.
</example>
</examples>

<advanced_metrics>
For quantitative analysis, these patterns can be measured:

**Lexical Diversity (Type-Token Ratio):**
- AI content often shows lower diversity (more repetition of common words)
- Calculate: unique words / total words
- Below 0.4 suggests limited vocabulary range

**Hedging Frequency:**
- Count instances of: "might," "could," "perhaps," "generally," "it seems"
- High frequency (>5% of content) suggests AI hedging behavior

**Sentence Length Variance:**
- Calculate standard deviation of sentence lengths
- Low variance (<5 words SD) suggests AI uniformity

**Perplexity Score:**
- AI-generated text tends to have lower perplexity (more predictable)
- Human writing shows more "burstiness" (variable predictability)
</advanced_metrics>

<success_criteria>
The audit is complete when:
- 30-second test has been applied and result stated
- All Tier 1 phrases identified with locations
- Tier 2 patterns checked for repetition
- Tier 3 clusters identified if present
- Structural tells assessed
- Slop score calculated
- Specific, actionable fixes provided
- Reader understands what to change and why
</success_criteria>

<core_principle>
**AI slop isn't about individual words—it's about patterns.**

One "moreover" doesn't make content AI-generated. But "moreover" + "it's worth noting" + "delve into" + uniform sentence length + emoji headers + flattery sandwiches = obvious AI slop.

The goal is writing that sounds like a specific human with specific opinions, not a very polite committee trying not to offend anyone.
</core_principle>
