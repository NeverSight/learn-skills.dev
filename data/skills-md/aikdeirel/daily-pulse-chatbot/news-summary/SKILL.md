---
name: news-summary
description: Concise, structured summaries of news articles (~30 sec read time). Captures key points, context, bias/gaps, and open questions. Use when user shares article URL or asks to summarize news content.
version: 1.0.0
triggers:
  - summarize article
  - news summary
  - article zusammenfassung
  - tldr news
  - what's this article about
  - fass den artikel zusammen
  - fasse mir den Artikel bitte [kurz] zusammen 
---

# News Summary Skill

## Purpose
Provide concise, structured summaries of news articles that can be read in ~30 seconds while capturing key points, plot twists, and providing contextual understanding. Include separate, clearly marked explanations for controversial or complex topics with sources.

## When to Use
- User shares a news article URL and wants a summary
- User asks to summarize current news/article
- User wants quick overview of lengthy articles
- User needs context or background on news topics

## Workflow

### Step 1: Fetch Article Content
- Use `webFetch` with the provided URL
- If fetch fails, inform user and ask for alternative (copy-paste text, different URL)

### Step 2: Analyze Article
- Identify publication date and source
- Determine article type (breaking news, analysis, opinion, data journalism, etc.)
- Check for bias/perspective
- Note what's missing or not mentioned
- Identify technical terms or complex concepts
- Look for connections to broader ongoing stories

### Step 3: Structure Summary
Create structured output with following sections:

#### 🎯 TL;DR
1-2 sentences ultra-short summary of the core message

#### 📰 Quick Facts
- **Source:** [Publication name + quality indicator]
- **Published:** [Date/Time - with "heute", "gestern", or specific date]
- **Type:** [🔥 Breaking / 💡 Analysis / 📊 Data / 💬 Opinion / 🔍 Investigation]
- **Relevanz:** Why this matters now (1 sentence)

#### 📋 Kernpunkte
3-5 bullet points with the main facts/arguments:
- Most important point first
- Include surprising "plot twists" or unexpected revelations
- Keep each point to 1-2 sentences max

#### 🔄 Größerer Kontext
If applicable: How does this fit into ongoing developments or broader story?
(2-3 sentences max, omit if standalone article)

#### ⚠️ Perspektive & Fehlender Kontext
- **Bias-Check:** Is it factual/balanced or opinion-heavy? Which perspective dominates?
- **Nicht erwähnt:** Important aspects or counterarguments not covered in article
(Keep brief - 2-3 sentences total)

#### ❓ Offene Fragen
1-2 questions the article raises but doesn't answer

---

#### 📚 Kontext & Erklärungen
**[ONLY if needed - always separate from main summary]**

If article contains controversial or complex topics that need explanation:
- **[Topic]:** Brief explanation (2-3 sentences)
- **Quellen:** Link to reliable sources for further reading

Use this section sparingly and only when truly necessary for understanding.

## Output Guidelines

### Style
- **Concise:** Entire summary readable in ~30 seconds
- **Neutral tone** in main summary
- **Clear structure** with emojis for quick scanning
- **German language** (match user's language)
- **No unnecessary elaboration** - stick to what's in the article

### Explanations Section Rules
- ALWAYS separate from main summary
- ALWAYS include sources when adding external context
- Mark clearly as additional explanation, not article content
- Only include when complex/controversial topics need clarification

### Length Guidelines
- TL;DR: 1-2 sentences
- Quick Facts: 4 lines
- Kernpunkte: 3-5 bullets, each 1-2 sentences
- Kontext: 2-3 sentences (if applicable)
- Perspektive: 2-3 sentences total
- Offene Fragen: 1-2 questions
- Erklärungen: Only when needed, max 2-3 topics

## Error Handling
- If URL cannot be fetched: Ask user to provide article text directly or try different URL
- If article is paywalled: Inform user and ask if they can provide text
- If content is not a news article: Politely explain skill is for news articles
- If article is too short/trivial: Provide brief summary without full structure

## Examples of When NOT to Use
- General questions about topics (not specific article)
- Requests for opinion or analysis beyond what's in article
- Creating new content rather than summarizing existing

## Key Principles
1. **Stick to the article** - main summary only contains what's in the source
2. **Separate explanation clearly** - any external context goes in marked section with sources
3. **Fast readability** - user should grasp essence in 30 seconds
4. **Actionable insight** - user knows what matters and why
5. **Transparency** - clear about bias, gaps, and limitations
