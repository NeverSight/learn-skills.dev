---
name: positioning-workshop
description: Full structured positioning exercise with competitive research, forced-choice questions, team alignment, and synthesis. Produces a sub-30-word positioning statement. For quick help with taglines, value props, or messaging tweaks, use positioning-messaging instead.
user-invocable: true
---
## [YOUR_PRODUCT] Context

Before helping, read `MEMORY.md` for: current wedge, ICP, competitors, PMF stage, system constraint.
Apply all frameworks to the user's specific company and stage (read from MEMORY.md).
Follow output preferences from USER.md (language, format, platform constraints).
For chat platforms: max 15 lines, no markdown tables, be concrete and actionable.


# Positioning Workshop

Structured positioning statement exercise. Combines deep competitive research with forced-choice strategic questions to produce an honest, compressed positioning statement.

Designed for teams that can't answer "why us?" in one sentence.

## Philosophy

Most positioning exercises produce corporate fluff because they skip the hard questions. This skill forces honesty by:
- Researching competitors BEFORE asking questions (so you can't hide from reality)
- Making every question a forced choice (no "all of the above")
- Requiring the team to write independently, then collide answers
- Compressing the final output to under 30 words

The output is not marketing copy. It's a strategic alignment tool.

## Workflow

### PHASE 1: Context gathering

Collect basic info:

1. "What does the company do? (2-3 sentences, plain language)"
2. "Who is the target customer today?"
3. "What stage? What's the team size?" — Options: [Pre-seed solo/duo, Pre-seed with team (3-8), Seed, Series A+]
4. "Is there an existing website, pitch deck, or memo I should read?"

If the user provides a file path or URL: read it. Extract product description, claimed differentiators, current messaging, pricing, and team.

### PHASE 2: Competitive research

Launch 2 parallel research agents:

**Agent 1: Direct competitors**
```
Research the competitive landscape for: [company description from Phase 1].

Use web search and competitor websites.

Find:
1. The 3-5 closest competitors (same customer, same problem)
2. For each: one-liner positioning, pricing, key differentiator, weakness
3. What do ALL of them say? (common claims = table stakes, not differentiators)
4. What does NONE of them say? (potential white space)

Output as a markdown table + 3 bullet summary.
```

**Agent 2: Adjacent/aspirational competitors**
```
Research companies adjacent to: [company description from Phase 1].

Use web search.

Find:
1. 2-3 companies solving a related problem for the same customer
2. 2-3 companies solving the same problem for a different customer
3. Any company that this team might secretly aspire to be (the "we're like X but for Y" reference)

For each: one-liner, why they matter as context.
```

Launch both agents in parallel. After agents return, present findings and ask:

- "Anything missing or wrong in this competitive picture?" — Options: [Looks right, Let me add/correct]
- "Which competitor do founders most often compare you to?"

### PHASE 3: The four questions

Present four positioning questions. Each question is informed by the competitive research.

Frame questions using SPECIFIC competitor names and findings from Phase 2. Do not use generic placeholders.

**Q1: The customer test**
```
Your ideal customer is evaluating you against [TOP COMPETITOR 1] and [TOP COMPETITOR 2].
They can only pick one. Why do they pick you?

Rules:
- Don't say "price" or "we're cheaper"
- Don't say "better technology" without specifics
- Don't say "customer service" (everyone says this)

Options: [Generate 3-4 options based on research, each a distinct strategic direction] + "Something else"
```

**Q2: The honest gap**
```
What is the single biggest reason your ideal customer says NO today?
Be specific. Not "we're early stage" — that's a cop-out.

Options: [Generate 3-4 options based on competitive weaknesses found in research] + "Something else"
```

**Q3: The core bet**
```
You can only invest in ONE of these directions for the next 6 months. Which one?

Options: [Generate 3-4 options based on white space found in research,
each with a 1-sentence description of what it means concretely] + "Something else"
```

**Q4: Market scope**
```
Which market are you actually in? Pick the one that defines your roadmap.

Options: [Generate 3-4 market definitions from narrow to broad,
based on the company's product and competitive research]
```

**Q5: Your first draft**

After the four questions, immediately ask:
"Now write your positioning statement. Under 30 words. Don't overthink it — gut reaction based on what you just answered."
Template: We help [WHO] achieve [WHAT] through [HOW], unlike [ALTERNATIVE].

Save the user's draft verbatim. In Phase 6, show it side-by-side with the final synthesized version.

### PHASE 4: Team collection

Generate a clean markdown block that the user can copy-paste to their team:

```
# Positioning Exercise — [Company Name]

Answer each question independently. Don't discuss with teammates first.
Spend max 10 minutes total. Gut reactions > polished answers.

## 1. The customer test
[Customized question with competitor names from research]

## 2. The honest gap
[Customized question]

## 3. The core bet
[Customized question with forced-choice options]

## 4. Market scope
[Customized question with scope options]

## 5. Positioning statement
Fill in, keep under 30 words:
We help [WHO] achieve [WHAT] through [HOW], unlike [ALTERNATIVE].

---
Return all answers to [user name] by [user specifies deadline].
```

Ask: "Send this to your team and paste all their replies here when you have them. How many people will respond?"

### PHASE 5: Synthesis

When user pastes team replies, analyze them:

1. **Alignment map** — Where does everyone agree? (These are real. Use them.)
2. **Contradiction map** — Where do people disagree? (These are the strategic decisions that need to be made.)
3. **Surprise findings** — Anything one person said that nobody else did but is clearly right.
4. **Gap analysis** — Questions nobody answered well (signals the team hasn't thought this through).

Present analysis, then ask for each contradiction: which direction do you want to go? (forced binary choice)

### PHASE 6: Final positioning statement

Output format:

```
# [Company Name] — Positioning Statement

## The customer test
[2-3 sentences. Lead with the answer. No fluff.]

## The honest gap
[1-2 sentences. Brutally honest.]

## The core bet
[2-3 sentences. What you're building, what exists today vs. planned.]

## Market scope
[1 sentence. The market you chose and what it excludes.]

## Positioning statement
[Under 30 words]
We help [WHO] achieve [WHAT] through [HOW], unlike [ALTERNATIVE].

## Your first draft vs. final
> **Your draft:** [user's verbatim draft from Phase 3 Q5]
> **Final:** [synthesized version above]
> **What changed:** [1-2 sentences on what shifted and why]
```

**Quality rules:**
- No sentence over 20 words
- No unverifiable adjectives (remove "innovative", "cutting-edge", "world-class", "unique")
- Every claim must be either (a) already true or (b) explicitly marked as a bet
- If aspirational, say "By [date], we plan to..." — not "We are..."
- Total length: under 200 words for all sections combined

Save to: ask the user where they'd like to save the output.

### PHASE 7: Iteration (optional)

If user wants to iterate, identify which section needs work. Re-run only that section's question with tighter constraints.

## Anti-patterns to avoid

- **Don't generate positioning without research.** The competitive context makes questions sharp.
- **Don't let the user skip the team exercise.** Solo positioning statements are echo chambers.
- **Don't use marketing language.** If it sounds like a SaaS landing page, rewrite it.
- **Don't accept "all of the above" answers.** Force choices. The pain of choosing IS the exercise.
- **Don't make the final statement longer than 30 words.** Compression is clarity.

## Related Skills

- positioning-messaging — quick help with taglines, value props, messaging tweaks
- competitive-analysis — strategic competitive frameworks
- brand-storytelling — company narrative and pitch story
- problem-definition — clarify what problem you're solving before positioning
