---
name: content-creation
description: Create newsletters, social media posts, presentations, professional emails, and other content for publication or communication. Use when asked to write newsletters, draft emails, create social posts, design presentations, or prepare content for specific audiences. Triggers include "write a newsletter", "draft an email", "create a post", "social media", "presentation", "blog post", "LinkedIn", "announcement".
---

# Content Creation

Create polished content for publication, communication, and presentations.

## Pattern Selection

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| Newsletter content | `create_newsletter_entry` | Newsletter sections/updates |
| Professional email | `create_formal_email` | Business correspondence |
| Show/podcast intro | `create_show_intro` | Opening hooks for media |
| Security newsletter | `create_security_update` | Security-focused updates |
| Blog enhancement | `enrich_blog_post` | Improve blog structure/visuals |
| Tweet/social | `tweet` | Short-form social content |
| Presentation | `create_keynote` | TED-style slide decks |
| Aphorisms | `create_aphorisms` | Quotable wisdom compilation |
| Content tags | `create_tags` | Categorization/SEO tags |
| Newsletter summary | `summarize_newsletter` | Summarize existing newsletters |

## Decision Flow

```
User request
    │
    ├─ Newsletter ─┬─ security focus? ──→ create_security_update
    │              └─ general? ──→ create_newsletter_entry
    │
    ├─ Email ──→ create_formal_email
    │
    ├─ Social media ──→ tweet
    │
    ├─ Presentation ──→ create_keynote
    │
    ├─ Blog ──→ enrich_blog_post
    │
    └─ Podcast/show ──→ create_show_intro
```

## Pattern References

See `references/` for full patterns:
- [create_newsletter_entry.md](references/create_newsletter_entry.md)
- [create_formal_email.md](references/create_formal_email.md)
- [create_show_intro.md](references/create_show_intro.md)
- [enrich_blog_post.md](references/enrich_blog_post.md)
- [create_keynote.md](references/create_keynote.md)
- [create_aphorisms.md](references/create_aphorisms.md)

## Output Guidelines

- Match tone to platform and audience
- Include clear calls-to-action where appropriate
- Respect platform constraints (character limits, format requirements)
- Optimize for skimmability (headers, bullets, bold)
- Consider SEO for web content
- Include visual suggestions where relevant

## Chaining Suggestions

- After `create_newsletter_entry` → offer `tweet` for social promotion
- After `create_keynote` → offer to export as Markdown or generate speaker notes
- After `enrich_blog_post` → offer `create_tags` for categorization
