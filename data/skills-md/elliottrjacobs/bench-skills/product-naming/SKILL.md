---
name: product-naming
description: Expert naming process for products, companies, and features based on David Placek's methodology. Use when the user says "name this", "brainstorm names", "naming process", or needs to find a name for a product, feature, company, or project.
allowed-tools: ["AskUserQuestion", "Write", "WebSearch"]
argument-hint: "[product or feature to name]"
---

# /product-naming — Expert Naming Process

Structured naming process based on David Placek's methodology (Lexicon Branding — created names for Sonos, Pentium, Blackberry, Swiffer).

## When to Use

- User says "name this", "brainstorm names", "naming process"
- Naming a new product, feature, company, or project
- Evaluating existing name candidates

## Process

### Step 1: Identify — Define the Brand Essence

If `$ARGUMENTS` provides a product or feature description, use it as the starting point. Ask the user to define (or help them articulate):
- **What is it?** (1 sentence describing the thing to be named)
- **Core attributes** (3-5 adjectives that describe the ideal brand feeling)
- **Target audience** (who will use/hear this name most)
- **Competitive context** (what other names exist in this space)
- **Constraints** (domain availability needed? character limit? language considerations?)

### Step 2: Invent — Generate Name Candidates

Generate 50+ name candidates across these categories:

**Descriptive** — Names that say what it is
- Functional descriptors (YouTube, Netflix, Dropbox)
- Compound words (Facebook, WordPress, Snapchat)

**Metaphorical** — Names that evoke a feeling or concept
- Nature metaphors (Amazon, Apple, Sierra)
- Action metaphors (Sprint, Dash, Vercel)
- Quality metaphors (Zendesk, Clarity, Notion)

**Abstract** — Names that are evocative but not literal
- Sound-symbolic (Sonos, Zoom, Slack)
- Portmanteaus (Pinterest = Pin + Interest, Spotify)
- Modified words (Lyft, Flickr, Tumblr)

**Invented** — Completely new words
- Phonetic constructions (Kodak, Xerox, Hulu)
- Latin/Greek roots (Astra, Vero, Luma)
- Generated strings (ASML, Nvidia)

Present candidates organized by category. Aim for quantity — curation comes next.

### Step 3: Evaluate — Score and Rank

Score the top 15-20 candidates on these criteria (1-5 scale):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Memorability** | High | Easy to recall after hearing once |
| **Pronounceability** | High | Obvious pronunciation, works spoken aloud |
| **Distinctiveness** | High | Stands out from competitors |
| **Meaning/Evocation** | Medium | Conveys the right feeling or concept |
| **Domain/Handle** | Medium | .com or reasonable alternative available |
| **Scalability** | Low | Won't constrain future product expansion |

Use AskUserQuestion to have the user react to the top candidates:
- Which names do you gravitate toward?
- Which feel wrong? Why?
- Any you'd like to combine or riff on?

### Step 4: Present — Final Recommendation

Present top 5-10 names with:
- The name
- Category (descriptive/metaphorical/abstract/invented)
- Why it works (connects back to brand essence)
- Potential concerns
- Domain availability (check via WebSearch if requested)

See [references/placek-methodology.md](references/placek-methodology.md) for deeper methodology notes.

## Output

Present recommendations inline in conversation. Optionally save to a file if the user requests.

## Next Steps

- Happy with the name? Document it in the PRD
- Need to formalize the product? → `/product-prd`
