---
name: substack-publisher
description: "Publish markdown posts to Substack as drafts or articles. Use when the user wants to publish to substack, create a substack draft, post to substack, create a substack newsletter, or convert a post to substack format."
---

# Substack Publisher

Publish markdown posts to Substack as drafts or newsletter articles. Converts markdown to Substack's ProseMirror JSON format.

## Requirements

Set these environment variables (add to `.env`):

- `SUBSTACK_SID` - Your `substack.sid` session cookie value
- `SUBSTACK_SUBDOMAIN` - Your Substack subdomain (e.g., `adrianpetcu`)
- `SUBSTACK_USER_ID` - Your Substack user ID (e.g., `106993810`)

## Quick Start

```bash
python scripts/publish_to_substack.py posts/daily-thoughts/03-context-driven-bug-fixing.md --dry-run
```

## Script Usage

```bash
python scripts/publish_to_substack.py <file.md> [options]
```

**Required:**
- `file` - Path to the markdown post file

**Options:**
- `--title` - Override post title (default: extracted from `# heading`)
- `--subtitle` - Override subtitle (default: extracted from `## Hook` section)
- `--publish` - Publish immediately instead of creating a draft
- `--audience` - Post audience: `everyone` (default) or `paid`
- `--dry-run` - Output ProseMirror JSON to stdout without making API calls

## Workflow

1. **Select the post file** - Choose a markdown post from the repository
2. **Preview with dry-run** - Always run `--dry-run` first to verify the conversion
3. **Create draft** - Run without `--publish` to create a draft on Substack
4. **Review in Substack** - Open the draft URL and verify formatting
5. **Publish** - Either publish from Substack's editor or re-run with `--publish`

## Markdown Format Support

The script handles the repository's post template format:

- **Title**: Extracted from the first `# heading`
- **Subtitle**: Extracted from the `## Hook` section content
- **Body**: All remaining sections converted to ProseMirror nodes

**Included sections**: Key Points, Body Outline, Call to Action, Visual Walkthrough, and any custom sections.

**Excluded sections** (metadata): Status, Hashtags, Notes, Verdict, LinkedIn Assessment.

**Block elements**: Paragraphs, headings (H1-H3), bullet lists, ordered lists, code blocks (with language), blockquotes, horizontal rules, images (HTTP URLs only).

**Inline marks**: **bold**, *italic*, `code`, [links](url).

**Special handling**: Bold labels on standalone lines (e.g., `**Section Name:**`) become H3 headings. Local image paths are skipped with a warning.

## Examples

**Preview conversion:**
```bash
python scripts/publish_to_substack.py posts/daily-thoughts/03-context-driven-bug-fixing.md --dry-run
```

**Create a draft:**
```bash
python scripts/publish_to_substack.py posts/daily-thoughts/03-context-driven-bug-fixing.md
```

**Publish with custom title:**
```bash
python scripts/publish_to_substack.py posts/daily-thoughts/03-context-driven-bug-fixing.md \
  --title "How AI Turns Vague Bugs Into Actionable Tickets" --publish
```

**Paid subscribers only:**
```bash
python scripts/publish_to_substack.py post.md --audience paid
```

## How to Get SUBSTACK_SID

1. Log into Substack in your browser
2. Open DevTools (F12) → Application → Cookies
3. Find `substack.sid` cookie for your subdomain
4. Copy the value and set it: `export SUBSTACK_SID="your-cookie-value"`

Alternatively, inspect any network request in DevTools → Headers → Cookie and copy the `substack.sid=...` value.

**Note:** This cookie expires periodically. If you get a 401/403 error, refresh the cookie.
