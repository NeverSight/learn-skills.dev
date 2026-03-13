---
name: academic-writing
description: Write and edit academic papers for top-tier CS venues (ICSE, FSE, ASE, ICML, NeurIPS). Provides rigorous writing style guidance for peer review.
---

# Academic Writing Skill

Use this skill when writing or editing academic content for software engineering and machine learning conferences.

## Conservative Editing Philosophy

**Principle: Minimal intervention.** Only change what is actually problematic. The author's voice and intentional choices take precedence over style preferences.

**Before making any change, ask:**
1. Is this actually wrong, or just different from my preference?
2. Could this be an intentional stylistic choice?
3. Does this change improve clarity, or just impose a different style?

**Preserve author intent:**
- Keep word choices the author uses consistently (e.g., "merely", "significantly")
- Keep structural patterns the author has established
- Keep rhetorical devices like strategic repetition

**Strategic repetition is valid.** Repetition for emphasis differs from redundancy:
- **Keep:** Repeating a key thesis statement in both the response intro and the quoted paper text (reinforces the main point)
- **Keep:** Parallel structure that repeats phrases for rhetorical effect
- **Remove:** Saying the same thing twice with no added emphasis or clarity

## Workflow Behavior

1. **Scope the request:** Identify what specific issues exist in the text. Do not invent problems.
2. **Categorize issues:** Separate actual errors (grammar, unclear meaning) from style preferences
3. **Present minimal changes:** Only propose changes for actual issues, not style preferences
4. **Preserve author choices:** If something could be intentional, assume it is
5. **Ask before restructuring:** For structural changes, ask: "Would you like me to restructure X, or keep the current structure?"
6. **Apply edits only when approved**

## Voice and Sentence Structure

**Use active voice (80%+ of sentences):**
- "We propose..." / "We show..." / "We evaluate..."
- "Our method achieves..." / "[METHOD] identifies..."

**Reserve passive voice for:**
- Established facts: "Root cause analysis is widely used..."
- Method descriptions: "The anomaly score is computed as..."
- Emphasizing results over actors: "A 15% improvement was observed..."

**Sentence length:**
- Short sentences for key claims: "This approach fails when the graph is unknown."
- Longer sentences for technical explanations with embedded clauses
- Split run-on sentences only when they impede comprehension

## Abstract Structure (6 Parts)

1. **Problem importance** (1-2 sentences): Why this matters
2. **Current limitations** (1-2 sentences): What existing methods lack
3. **Key insight** (1 sentence): Core observation or reformulation
4. **Proposed solution** (1-2 sentences): Method name and approach
5. **Results** (1-2 sentences): Specific metrics (percentages, speedups)
6. **Availability** (optional): Code/data links

## Introduction Structure (10 Paragraphs)

1. **Motivation**: Why the problem matters, broad applications
2. **Current state**: What exists, with citations
3. **Gap identification**: Limitations of existing work
4. **Deeper analysis**: Why the gap exists (technical reasons)
5. **Related approaches**: What others have tried, why insufficient
6. **Proposed direction**: High-level idea before technical details
7. **Technical solution**: Method introduction with key components
8. **Challenges addressed**: Specific improvements over prior work
9. **Results summary**: Key metrics and comparisons
10. **Contributions**: Bulleted list (3-4 items), each starting with action verb

## Claim Presentation

**For contributions:**
- "To the best of our knowledge, this is the first..."
- "We make the following contributions:"
- "Our key insight is that..."

**For results (use specific numbers):**
- "[METHOD] achieves 67% Top-1 accuracy, a 253% improvement over..."
- "Our method requires only 8ms per diagnosis, 9,700x faster than..."

**For theoretical claims:**
- "We show that..." / "We prove that..." / "We demonstrate that..."

## Hedging Language (Calibrated Uncertainty)

| Certainty Level | Words to Use |
|-----------------|--------------|
| **Strong** | demonstrates, achieves, proves, establishes, shows |
| **Moderate** | indicates, reveals, suggests, implies |
| **Cautious** | may, might, appears to, potentially, likely, can |

**Use hedging for:**
- Speculation beyond direct evidence
- Generalizations beyond experimental scope
- Theoretical implications not fully proven

## Transition Phrases

| Function | Phrases |
|----------|---------|
| **Contrast** | However, In contrast, Nevertheless, Unlike, While |
| **Addition** | Furthermore, Moreover, Additionally, In addition |
| **Sequence** | First, Second, Third, Finally, Subsequently |
| **Cause/Effect** | Therefore, Thus, Consequently, As a result, Hence |
| **Evidence** | Specifically, In particular, For instance, As shown in |
| **Emphasis** | Importantly, Notably, Crucially, Interestingly |

## Mathematical Writing

**Before equations:** Provide context
- "The anomaly score is defined as:"
- "We compute the ranking function using:"

**After equations:** Define variables immediately
- "where $S^I_c$ denotes the internal score and $S^E_c$ the external score."

**References:** Use `Eq.~\ref{eq:name}` or `Equation~\ref{eq:name}`

**Displayed equations:** Use for important formulas that will be referenced.

## Citations

**Integrate naturally:**
- "Recent work on causal discovery~\cite{pearl2009} has shown..."
- "Following~\cite{budhathoki2022}, we define..."

**Group by topic:**
- "...has been explored in microservices~\cite{a,b,c} and cloud systems~\cite{d,e}."

**Citation placement:** Make clear what is being cited
- Good: "Prior work using mean and standard deviation~\cite{Li2022Circa} can degrade..."
- Bad: "We prefer median over mean~\cite{Li2022Circa}..." (unclear if citing or critiquing)

## Figures and Tables

**Pre-reference:** Explain what to look for
- "To evaluate scalability, we measure runtime across dataset sizes."

**Reference format:**
- "Table~\ref{tab:results}" / "Figure~\ref{fig:overview}"
- "As shown in Figure~\ref{fig:overview}..."

**Post-reference:** Interpret the data
- "From Table~\ref{tab:results}, we observe that [METHOD] consistently outperforms..."

**Captions:** Self-contained, describe what is shown and key takeaway

## Terminology Conventions

- **Acronyms:** Introduce once with full form: "Root Cause Analysis (RCA)"
- **After introduction:** Use acronym only: "RCA"
- **Novel concepts:** Use quotes on first use: 'internal properties', 'external properties'
- **Consistency:** Choose one term and use it throughout (not alternating synonyms)
- **Variable introduction:** "Let $x$ denote..." then use $x$ consistently

## Phrases to Use

- "We propose..." / "We introduce..."
- "Our key observation is that..." / "Our key insight is that..."
- "To address this challenge, we..."
- "We evaluate on..." / "We conduct experiments on..."
- "Results demonstrate that..." / "Our findings show that..."
- "Compared to [baseline], our method..."
- "Let $x$ denote..." (for variable introduction)

## Phrases to Avoid

- "Obviously" / "Clearly" / "It is easy to see" (condescending)
- "Very" / "Really" / "Extremely" (vague intensifiers)
- "We believe" (use "We hypothesize" or "We conjecture" for speculation)
- "Proves" for empirical results (use "demonstrates" or "shows")
- "Novel" / "Innovative" without substantiation
- First person singular "I" (use "we" even for single author)

## Punctuation Guidelines

**Prefer avoiding when possible, but do not mechanically replace:**
- Em-dashes (`---`): Often better as commas or separate sentences, but acceptable for strong parenthetical emphasis
- Semicolons: Often better as separate sentences, but acceptable for closely related independent clauses
- Colons in prose: Reserve primarily for lists, definitions, and mathematical notation

## Common Revision Patterns

Apply these only when they improve clarity, not mechanically:

| Pattern | When to Apply |
|---------|---------------|
| Split long sentences | Only if comprehension is impeded |
| Convert passive to active | Only if the actor matters for understanding |
| Shorten parentheticals | Only if they interrupt flow significantly |
| Introduce variables | Only if the same term appears 3+ times in close proximity |
