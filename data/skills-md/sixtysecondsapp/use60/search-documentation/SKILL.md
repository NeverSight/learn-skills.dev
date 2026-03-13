---
name: Search Documentation
description: |
  Search the platform documentation to answer questions about features, integrations,
  and how-to guides. Use when a user asks "how do I connect my calendar", "help with
  pipeline setup", "what is deal health scoring", or any question about how the platform works.
  Returns relevant article excerpts with links to full documentation.
metadata:
  category: data-access
  skill_type: atomic
  author: sixty-ai
  version: "2"
  is_active: true
  context_profile: full
  triggers:
    - pattern: "how do I"
      intent: "how_to_question"
      confidence: 0.80
      examples:
        - "how do I connect my calendar"
        - "how do I set up integrations"
        - "how do I use deal scoring"
    - pattern: "help with"
      intent: "help_request"
      confidence: 0.80
      examples:
        - "help with pipeline setup"
        - "help me understand deal health"
        - "I need help with settings"
    - pattern: "search the docs"
      intent: "doc_search"
      confidence: 0.85
      examples:
        - "search documentation for"
        - "find in docs"
        - "look up in the help center"
    - pattern: "what is"
      intent: "feature_question"
      confidence: 0.75
      examples:
        - "what is deal health scoring"
        - "what does the pipeline view do"
        - "what are smart tasks"
  keywords:
    - "help"
    - "how to"
    - "documentation"
    - "docs"
    - "guide"
    - "tutorial"
    - "what is"
    - "how does"
    - "setup"
    - "instructions"
  required_context:
    - company_name
  optional_context:
    - user_query
  inputs:
    - name: query
      type: string
      description: "The search query or question to find relevant documentation for"
      required: true
    - name: category
      type: string
      description: "Optional category filter to narrow documentation search"
      required: false
    - name: limit
      type: number
      description: "Maximum number of articles to return"
      required: false
      default: 3
  outputs:
    - name: articles
      type: array
      description: "Array of matching articles with title, slug, excerpt, and category"
    - name: total_results
      type: number
      description: "Total number of matching articles found"
  requires_capabilities:
    - crm
  priority: medium
  execution_mode: sync
  timeout_ms: 10000
  tags:
    - documentation
    - help
    - search
    - self-service
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Search Documentation

## Goal
Help users find answers to their questions by searching the platform documentation. The skill should not just find articles -- it should **answer the question** using the documentation as source material, providing a synthesized, directly useful response with citations.

## Why Documentation Search Matters

### The Self-Service Imperative
- **67% of users prefer self-service** over talking to support (Zendesk Customer Experience Trends)
- **91% would use a knowledge base** if it were available and answered their question (Forrester)
- **Average support ticket costs $15-25** to resolve; a good documentation search costs pennies
- **First-response resolution** (answering without human support) increases customer satisfaction by 30%

The documentation search skill is often the first interaction a user has with the AI copilot. If it answers their question quickly and accurately, it builds trust for all future interactions. If it fails, the user stops asking.

### The "Link Dump" Problem
Most documentation search tools return a list of links. This is lazy and unhelpful:
- The user must click through 3-5 articles
- They must scan each article for the relevant paragraph
- They must synthesize the answer themselves
- 60% of users abandon after the first irrelevant link

This skill must do better. It should **read the docs so the user doesn't have to**, then present a clear answer with source citations.

## Documentation Search Methodology

Consult `references/search-methodology.md` for the complete 4-phase search process, query optimization techniques, and result ranking methodology.

### Phase 1: Query Understanding

Before searching, parse the user's question to understand intent and extract search terms.

#### Intent Classification

| Intent Type | Signal Words | Search Strategy |
|------------|-------------|-----------------|
| **How-to** | "how do I," "how to," "steps to," "set up" | Search for procedural/guide content |
| **What-is** | "what is," "what does," "explain," "define" | Search for conceptual/overview content |
| **Troubleshooting** | "not working," "error," "broken," "can't" | Search for FAQ/troubleshooting content |
| **Configuration** | "settings," "configure," "change," "customize" | Search for settings/configuration content |
| **Integration** | "connect," "integrate," "sync," "link" | Search integration-specific documentation |
| **Feature discovery** | "can I," "is there," "does it support" | Search feature documentation and capabilities |

#### Keyword Extraction

Transform natural language into effective search terms:

1. **Remove stop words**: "how do I connect my Google calendar" -> "connect Google calendar"
2. **Expand abbreviations**: "cal" -> "calendar", "CRM" -> keep as-is (it's a known term)
3. **Include synonyms**: "link" -> also search "connect", "integrate", "sync"
4. **Preserve proper nouns**: "Google Calendar", "Slack", "HubSpot" -- keep exact casing
5. **Extract the subject**: The thing the user is asking about (feature, integration, setting)
6. **Extract the action**: What they want to do with it (set up, configure, troubleshoot, understand)

#### Query Expansion Strategy

For better recall, generate 2-3 query variants:
- **Original terms**: The exact keywords from the user's question
- **Synonym expansion**: Replace key terms with platform-specific synonyms
- **Category-scoped**: If the intent maps to a category, add the category as a filter

Example:
- User asks: "how do I set up deal health scoring"
- Query 1: "deal health scoring" (direct)
- Query 2: "deal health setup configuration" (action-expanded)
- Query 3: category:"pipeline" + "health score" (category-scoped)

### Phase 2: Search Execution

Execute the search against the documentation store:

```
execute_action("search_docs", { query: "${extracted_query}", category: "${category_filter}", limit: 5 })
```

**Search parameters**:
- Always request **5 results** internally (even if returning 3 to the user) -- extra results help with synthesis
- Apply category filter only when intent classification is high confidence
- If first search returns 0 results, retry with broader terms (drop the category filter, use synonym expansion)

### Phase 3: Result Relevance Ranking

Not all search results are equally relevant. Re-rank results after retrieval using these signals:

| Signal | Weight | Rationale |
|--------|--------|-----------|
| **Title match** | 30% | Article title contains the key search terms |
| **Content match** | 25% | Article body contains direct answers to the question |
| **Category alignment** | 20% | Article category matches the detected intent |
| **Recency** | 15% | More recently updated articles are more accurate |
| **Specificity** | 10% | Articles focused on the exact topic beat broad overview articles |

**Scoring heuristics**:
- Title contains the exact feature name: +30
- Article has a "how-to" section and the intent is how-to: +20
- Article was updated in the last 30 days: +15
- Article is in the matching category: +20
- Article mentions the specific integration/feature by name 3+ times: +10

### Phase 4: Answer Synthesis

This is the critical differentiator. Do not just list articles -- **synthesize an answer**.

#### Synthesis Methodology

1. **Read the top 3 articles** (by relevance score)
2. **Identify the answer paragraph(s)** -- the specific section that addresses the user's question
3. **Compose a direct answer** in 2-5 sentences using information from the articles
4. **Cite your sources** -- reference which article each piece of information comes from
5. **Provide the "read more" link** for users who want the full context

#### Progressive Disclosure Pattern

Present information in layers of increasing detail:

```
LAYER 1: Direct Answer (2-3 sentences)
  The synthesized answer to the user's question.
  [Source: Article Title]

LAYER 2: Key Steps / Details (if how-to)
  1. Step one
  2. Step two
  3. Step three
  [Source: Article Title]

LAYER 3: Full Article Links
  For more details, see:
  - [Article Title 1](/docs#slug-1)
  - [Article Title 2](/docs#slug-2)
```

This ensures that **90% of users get their answer in Layer 1** without clicking any links, while power users can drill deeper.

## Multi-Article Synthesis

When the answer spans multiple documentation articles, the skill must weave them together coherently.

### When Multi-Article Synthesis Is Needed
- The question touches multiple features ("How do I set up deal health scoring AND connect it to pipeline alerts?")
- The answer has prerequisites documented in a different article ("To use X, you first need to configure Y")
- Different aspects of the same topic are in different articles (setup in one, troubleshooting in another)

### Synthesis Strategy
1. **Identify the primary article** -- the one most directly answering the question
2. **Identify supporting articles** -- prerequisites, related configuration, troubleshooting
3. **Compose the answer** starting from the primary article
4. **Weave in supporting context** where needed, clearly citing each source
5. **Present a unified narrative** -- the user should not be able to tell the answer came from multiple sources

### Example of Good Multi-Article Synthesis

User asks: "How do I connect my Google Calendar and see meetings in my pipeline?"

**Synthesized answer**:
> To connect Google Calendar, go to Settings > Integrations > Google Calendar and click "Connect." You'll need to authorize with your Google account and select which calendars to sync. (Source: [Google Calendar Integration Guide](/docs#google-calendar))
>
> Once connected, your calendar events will automatically appear in the meetings section. To see them in your pipeline view, each meeting must be linked to a deal. You can link meetings manually from the deal page, or enable auto-linking in Settings > Meetings > Auto-link Rules. (Source: [Meeting-Deal Linking](/docs#meeting-deal-linking))

### Example of Bad Multi-Article Synthesis (just listing links)

> I found these articles that might help:
> 1. Google Calendar Integration Guide
> 2. Meeting-Deal Linking
> 3. Pipeline View Guide

This forces the user to do the work. Always synthesize.

## "Not Found" Guidance

When documentation does not cover the user's question, provide genuinely helpful alternatives instead of a dead end.

### Response Strategy for No Results

1. **Acknowledge the gap honestly**: "I couldn't find documentation on that specific topic."
2. **Suggest related topics that DO exist**: "However, I found articles on [related topic] that might help."
3. **Offer alternative paths**:
   - "You can browse all documentation at /docs"
   - "Try asking about [reformulated question]"
   - "For this specific question, contacting support at [email/channel] would be fastest"
4. **If the feature might not exist**: "I don't have documentation for that feature. It's possible this isn't currently supported. Check the feature request board or ask support."

### Never Say
- "No results found." (too abrupt, not helpful)
- "Try a different search." (puts the burden on the user without guidance)
- "I can't help with that." (too final, doesn't offer alternatives)

## Category-Aware Search Optimization

Documentation is organized into categories. Leveraging these improves search quality. See `references/documentation-map.md` for the full category hierarchy, common user questions mapped to each category, search keyword routing table, and troubleshooting decision tree.

| Category | Typical Content | Signal Words |
|----------|----------------|-------------|
| **Getting Started** | Onboarding, first steps, quickstart guides | "new," "start," "first time," "beginner" |
| **Pipeline** | Deals, stages, forecasting, health scoring | "deal," "pipeline," "stage," "forecast," "health" |
| **Meetings** | Calendar, recordings, transcripts, notes | "meeting," "calendar," "recording," "transcript" |
| **Contacts** | Contact management, companies, relationships | "contact," "company," "person," "relationship" |
| **Tasks** | Task management, automation, reminders | "task," "to-do," "reminder," "automation" |
| **Integrations** | Third-party connections, sync, APIs | "connect," "integrate," "sync," "Slack," "Google" |
| **Settings** | Configuration, preferences, admin | "setting," "configure," "admin," "preference" |
| **Copilot** | AI assistant, skills, commands | "copilot," "AI," "assistant," "command" |
| **Security** | Permissions, roles, SSO, data privacy | "permission," "role," "SSO," "security," "privacy" |
| **Billing** | Plans, credits, invoices, upgrades | "billing," "plan," "credit," "invoice," "upgrade" |

### Category Fallback Chain
If the primary category returns no results, expand:
1. Try without category filter
2. Try the parent/related category
3. Try a full-text search across all categories
4. Fall back to "not found" guidance

## Response Formatting Best Practices

### Structure for Successful Search

```
[Direct answer in 2-3 sentences, synthesized from the documentation]

**Key Steps** (if applicable):
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Related Articles:**
1. **[Article Title]** ([Category])
   [Relevant excerpt -- first 150-200 characters of the matching section]
   [Read more](/docs#slug)

2. **[Article Title]** ([Category])
   [Relevant excerpt]
   [Read more](/docs#slug)
```

### Structure for No Results

```
I couldn't find documentation on "[user's topic]."

**You might find these helpful instead:**
- [Related Article Title](/docs#slug) -- [brief description of why it's related]
- Browse all documentation at /docs

**Need more help?** Contact support at [channel] or submit a feature request.
```

### Formatting Rules
- **Bold article titles** for scannability
- **Category in parentheses** after each title
- **Excerpts are 150-200 characters** -- enough to assess relevance without overwhelming
- **Links use the `/docs#slug` format** consistently
- **Number the results** (1, 2, 3) for easy reference
- **Never show more than 3 articles** to the user (even if 5 were retrieved)
- **Always lead with the synthesized answer** before showing individual articles

## Output Contract

Return a SkillResult with:

- `data.answer`: string -- Synthesized answer to the user's question (2-5 sentences). This is the primary response.
- `data.answer_confidence`: "high" | "medium" | "low" -- How confident the skill is that the answer is correct and complete
- `data.articles`: Array of matching articles (max 3 shown to user)
  - `title`: string
  - `slug`: string
  - `excerpt`: string (150-200 characters of the most relevant section)
  - `category`: string
  - `relevance_score`: number (0-100)
  - `updated_at`: string (ISO date, if available)
- `data.total_results`: number -- Total matching articles found
- `data.query_analysis`: object (for debugging/transparency)
  - `original_query`: string
  - `extracted_keywords`: array of strings
  - `detected_intent`: string
  - `category_filter`: string | null
  - `synonym_expansions`: array of strings
- `data.related_topics`: array of strings -- Suggested related topics the user might want to explore

## Quality Checklist

Before returning the search results, verify:

- [ ] Synthesized answer is present and directly addresses the user's question
- [ ] Answer is 2-5 sentences (not a single word, not a paragraph)
- [ ] Answer cites which article(s) it draws from
- [ ] Articles are ranked by relevance, not just search order
- [ ] Excerpts are from the RELEVANT section of each article (not the intro paragraph)
- [ ] No more than 3 articles shown to the user
- [ ] Each article has title, slug, excerpt, and category
- [ ] Links use the `/docs#slug` format
- [ ] If no results, helpful alternatives are provided (not just "not found")
- [ ] Category filter was applied when appropriate
- [ ] Answer confidence is honestly assessed (not always "high")
- [ ] No fabricated article titles or content -- only return what the search found
- [ ] Query analysis is included for transparency
- [ ] Related topics are suggested for exploration

## Error Handling

### Search returns no results
Follow the "Not Found" guidance above. Never return an empty response. Always provide:
1. Acknowledgment of the gap
2. Related topics that DO have documentation
3. Alternative paths (browse docs, contact support)
4. Suggest a reformulated question

### Search returns results but none are relevant
This is worse than no results because the user sees articles that don't help. Detection:
- Relevance score of the top result is below 40
- Article titles have no keyword overlap with the query

Response: Treat as "not found" and note: "I found some articles but none seem to directly answer your question. Here are the closest matches -- and some alternatives."

### Query is too broad
If the query is a single word like "help" or "settings" that would match dozens of articles:
- Ask for clarification: "Can you be more specific? For example, 'help with deal health scoring' or 'settings for calendar sync'."
- Provide the top 3 most popular articles in that category as a starting point
- List available sub-categories to help the user narrow down

### Query is too specific / uses jargon
If the query uses terms not in the documentation (e.g., internal jargon or a feature by a non-standard name):
- Try synonym expansion and abbreviation expansion
- Try searching for the broader concept
- If still no results: "I couldn't find documentation for '[term].' This might be referred to differently in our docs. Try [alternative term] or browse [category]."

### Search service is unavailable
If the documentation search endpoint fails or times out:
- Return a helpful fallback: "Documentation search is temporarily unavailable. You can browse the full docs at /docs or contact support."
- Do NOT return an error message to the user. Always degrade gracefully.

### Multiple valid interpretations
If the query could mean different things (e.g., "scoring" could be deal scoring or lead scoring):
- Return results for the most likely interpretation
- Note the ambiguity: "I found results for deal health scoring. If you were looking for lead scoring, try asking about that specifically."
- Include results for both interpretations if space allows

### User asks about a feature that does not exist
If the user asks "how do I export to Excel" but that feature is not built:
- Be honest: "Export to Excel isn't currently available in the platform."
- Suggest alternatives: "You can export data to CSV from the pipeline view."
- Suggest submitting a feature request if appropriate
- Do NOT fabricate documentation for features that don't exist

### Stale documentation
If the search returns articles that are clearly outdated (references to deprecated features, old UI screenshots):
- Still present the information but flag it: "Note: This article was last updated [date] and some details may have changed."
- Suggest the user verify current behavior in the app
- Never silently present outdated information as current
