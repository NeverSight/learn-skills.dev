---
name: news-discover
description: Curated daily news briefing across global, local, tech, science, business, and culture. Prioritizes today's news, adapts to user location and interests. Use when user asks for news, daily briefing, what's happening, or current events.
version: 1.0.0
triggers:
  - news
  - what's happening
  - daily briefing
  - news briefing
  - was gibt's neues
  - was ist passiert
  - nachrichten
  - news heute
  - current events
---

# News Discover

Daily news briefing – global, local, and topic-based. Optimized for ~60 second read time.

## Context

- User location and current date are available in system prompt
- Mix German and English sources naturally
- If user context/interests are known, weight topics accordingly
- No sports coverage

## Categories

| Emoji | Category | Focus |
|-------|----------|-------|
| 🌍 | **Global** | World politics, international events, breaking news |
| 📍 | **Local** | News from user's city/region/country |
| 💻 | **Tech** | Web dev, DevOps, hosting, AI/ML, developer tools |
| 🔬 | **Science** | Research, space, climate, discoveries |
| 📈 | **Business** | Only if broadly relevant or particularly significant |
| 🎬 | **Culture** | Entertainment, music, gaming, film – keep light |

## Workflow

1. **Search current news** via web search for each active category
   - Focus on "today" / "last 24 hours"
   - Use location context for local news
   - Vary sources for perspective diversity

2. **Filter & prioritize**
   - Only genuinely current stories (today, maybe yesterday)
   - Mark breaking/significant news with 🔴
   - Skip categories if nothing noteworthy found

3. **Output briefing**
   - 2-4 stories per category
   - One-liner per story: what happened + source
   - Include links where available

4. **Offer deep-dive**
   - User can ask for details on any story
   - → Triggers news-summary skill or further search

## Output Format

```
[Short greeting + date context]

🌍 Global
- [Headline] – [1-sentence summary] ([Source])
- ...

📍 Local ([City/Region])
- ...

💻 Tech
- ...

[Other categories as relevant]

---
[Optional: "Mehr zu einem Thema?" or note if a category had nothing notable]
```

## Guidelines

- **Be selective** – quality over quantity, skip empty categories
- **Stay neutral** – present facts, note controversy where relevant
- **Source diversity** – mix perspectives, don't rely on single outlet
- **Brevity** – each story is 1-2 sentences max
- **Recency** – if it's not from today/yesterday, skip it unless major ongoing story
- **Personalize** – if user interests are known, lead with those topics

## Error Handling

- If web search unavailable: inform user, suggest enabling it
- If no news found for category: skip silently or note briefly
- If user asks about specific topic not covered: search specifically for that

## Connection to Other Skills

- Deep-dive on any story → `news-summary` skill
- User shares article URL → hand off to `news-summary`
