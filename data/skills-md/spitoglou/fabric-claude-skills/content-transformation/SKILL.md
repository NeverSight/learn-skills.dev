---
name: content-transformation
description: Convert content between formats, summarize at different levels, and repurpose for various platforms. Use when asked to convert to markdown, create summaries of varying lengths, make tweets, create flashcards, or process video content. Triggers include "convert to markdown", "summarize in one sentence", "make this a tweet", "create flashcards", "TL;DR", "summarize this video", "export as CSV".
---

# Content Transformation

Convert, summarize, and repurpose content across formats and platforms.

## Pattern Selection

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| Standard summary | `summarize` | Balanced key points extraction |
| Micro summary | `summarize_micro` | Extremely concise (1-2 sentences) |
| 5-level summary | `create_5_sentence_summary` | Progressive: 5 words → 5 sentences |
| Key points | `create_summary` | Bullet-point key takeaways |
| One-liner + bullets | `create_micro_summary` | One sentence + supporting points |
| To Markdown | `convert_to_markdown` | Any format → clean Markdown |
| HTML cleanup | `sanitize_broken_html_to_markdown` | Broken HTML → Markdown |
| To CSV | `export_data_as_csv` | Structured data → CSV |
| To Tweet | `tweet` | Content → tweet-length |
| To Flashcards | `to_flashcards` | Content → Q&A flashcards |
| Create flashcards | `create_flash_cards` | Generate study flashcards |
| Callout blocks | `md_callout` | Create Markdown callouts |
| Video summary | `youtube_summary` | YouTube → key points + timestamps |
| Video chapters | `create_video_chapters` | Video → timestamped chapters |
| Latest video | `extract_latest_video` | Get latest video info |
| Video ID | `extract_videoid` | Extract video IDs from URLs |

## Decision Flow

```
User request
    │
    ├─ Summarization ─┬─ "one sentence/TL;DR" ──→ summarize_micro
    │                 ├─ "5-level/progressive" ──→ create_5_sentence_summary
    │                 ├─ "key points/bullets" ──→ create_summary
    │                 └─ general ──→ summarize
    │
    ├─ Format conversion ─┬─ "markdown" ──→ convert_to_markdown
    │                     ├─ "CSV/spreadsheet" ──→ export_data_as_csv
    │                     ├─ "tweet" ──→ tweet
    │                     └─ "flashcards" ──→ to_flashcards
    │
    └─ Video content ─┬─ "summarize video" ──→ youtube_summary
                      └─ "chapters/timestamps" ──→ create_video_chapters
```

## Pattern References

See `references/` for full patterns:
- [summarize.md](references/summarize.md)
- [summarize_micro.md](references/summarize_micro.md)
- [create_5_sentence_summary.md](references/create_5_sentence_summary.md)
- [convert_to_markdown.md](references/convert_to_markdown.md)
- [tweet.md](references/tweet.md)
- [to_flashcards.md](references/to_flashcards.md)
- [youtube_summary.md](references/youtube_summary.md)

## Output Guidelines

- Preserve essential meaning in all transformations
- Match output format conventions exactly (valid Markdown, proper CSV escaping)
- For summaries: scale detail to requested length
- For social: respect platform character limits
- For study materials: focus on testable concepts
