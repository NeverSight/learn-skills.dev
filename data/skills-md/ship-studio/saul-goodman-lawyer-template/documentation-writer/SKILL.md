---
name: documentation-writer
description: Maintain clear, non-technical documentation for website projects. Use this skill after ANY code change to update SITE.md with what changed. Triggers on file edits, new pages, component changes, or when the user asks about their site. Essential for keeping non-developers informed about their project.
---

# Documentation Writer

This skill ensures documentation stays current and accessible for non-technical users. SITE.md is the single source of truth for what a website contains.

## Core Principle

**Update documentation immediately after every change.** Non-developers rely on SITE.md to understand their site. Outdated docs cause confusion and frustration.

## SITE.md Structure

```markdown
# [Site Name]

## What's On Your Site

### Pages
- **Homepage** (`/`) - What visitors see first. Contains [describe sections].
- **About** (`/about`) - Information about [topic].

### Shared Elements
- **Navigation bar** - Links to [list pages]. Appears on every page.
- **Footer** - Contains [describe content].

## Recent Changes
- [Date]: [What changed in plain English]
- [Date]: [What changed in plain English]

## Quick Guide
- To change the site name: [simple instruction]
- To add a new page: [simple instruction]
- To change colors: [simple instruction]
```

## Writing Style Rules

1. **No jargon**: Say "the main page" not "the root route"
2. **No code terms**: Say "the top menu" not "the nav component"
3. **Be specific**: Say "Added a blue Contact button" not "Updated CTA"
4. **Use familiar words**: "section", "button", "link", "picture", "menu"
5. **Explain what users see**: Describe visual elements, not implementation

## When to Update

Update SITE.md after:
- Creating or deleting a page
- Adding or removing sections
- Changing navigation or footer
- Modifying colors, fonts, or layout
- Adding images or media
- Any visible change to the site

## Example Updates

**Good:**
> Added a "Contact Us" section at the bottom of the homepage with an email form.

**Bad:**
> Implemented ContactForm component with useState for form handling.

**Good:**
> Changed the button colors from blue to green across the site.

**Bad:**
> Updated primary color CSS variable in globals.css.

## After Every Task

1. Make the code changes
2. Open SITE.md
3. Update the relevant section
4. Add entry to "Recent Changes" with today's date
5. Tell the user what changed in simple terms
