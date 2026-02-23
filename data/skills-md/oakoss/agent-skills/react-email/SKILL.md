---
name: react-email
description: >
  Build responsive HTML emails with React Email components. Covers email structure (Html, Head, Body, Container),
  content components (Text, Heading, Button, Link, Img), layout (Section, Row, Column), styling with inline CSS
  and Tailwind, custom fonts, preview text, and rendering to HTML.

  Use when creating transactional emails, marketing templates, or email design systems.
  Use for email rendering, preview, Tailwind email styling, and provider integration with Resend, Nodemailer, or SendGrid.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://react.email/docs
---

# React Email

## Overview

React Email is a library for building responsive HTML emails using React components. It provides a set of unstyled, accessible components that render to email-client-compatible HTML. Supports inline styles, Tailwind CSS via a wrapper component, custom web fonts, and rendering to both HTML and plain text.

**When to use:** Transactional emails (welcome, password reset, receipts), marketing templates, email design systems, any project that renders emails server-side.

**When NOT to use:** Static HTML email templates with no dynamic content, projects that already use a dedicated email builder (MJML, Maizzle), or when you only need plain-text emails.

## Quick Reference

| Pattern            | API                                      | Key Points                                                  |
| ------------------ | ---------------------------------------- | ----------------------------------------------------------- |
| Document structure | `Html`, `Head`, `Body`                   | `Html` wraps everything, `Head` loads fonts/meta            |
| Content container  | `Container`                              | Centers content, sets `max-width`                           |
| Layout grid        | `Section`, `Row`, `Column`               | Table-based layout for email clients                        |
| Text content       | `Text`, `Heading`                        | `Heading` accepts `as` prop for h1-h6                       |
| Links              | `Link`                                   | Standard anchor, `href` required                            |
| Call-to-action     | `Button`                                 | Renders as link styled as button, `href` required           |
| Images             | `Img`                                    | Always set `width`, `height`, `alt`                         |
| Divider            | `Hr`                                     | Horizontal rule between sections                            |
| Inbox preview      | `Preview`                                | Sets preview text shown in inbox list                       |
| Custom fonts       | `Font`                                   | Place inside `Head`, set `webFont` and `fallbackFontFamily` |
| Tailwind styling   | `Tailwind`                               | Wraps email, inlines Tailwind classes at render             |
| Render to HTML     | `render(<Email />)`                      | Async, returns HTML string                                  |
| Render plain text  | `render(<Email />, { plainText: true })` | Strips HTML, returns text                                   |
| Pretty output      | `render(<Email />, { pretty: true })`    | Formatted HTML for debugging                                |
| Preview server     | `email dev`                              | Local dev server with hot reload                            |
| Markdown content   | `Markdown`                               | Renders Markdown as email-compatible HTML                   |
| Code blocks        | `CodeBlock`                              | Syntax-highlighted code with theme support                  |
| Inline code        | `CodeInline`                             | Monospace inline code spans                                 |

## Common Mistakes

| Mistake                                         | Correct Pattern                                                                           |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Using `className` with inline styles            | Use either Tailwind (`className`) or inline `style` objects, not both on the same element |
| Forgetting `width`/`height` on `Img`            | Always specify dimensions to prevent layout shifts in email clients                       |
| Nesting `Container` inside `Container`          | Use one `Container` for centering, `Section`/`Row`/`Column` for inner layout              |
| Using CSS Grid or Flexbox                       | Use `Section`, `Row`, `Column` for table-based layouts that work across email clients     |
| Placing `Font` outside `Head`                   | `Font` must be a child of `Head` to load correctly                                        |
| Using `render()` synchronously                  | `render()` is async, always `await` the result                                            |
| Wrapping `Tailwind` inside `Html`               | `Tailwind` wraps `Html`, not the other way around                                         |
| Omitting `Preview` component                    | Without `Preview`, email clients show the first body text as preview                      |
| Using external CSS stylesheets                  | Email clients strip `<link>` tags; use inline styles or Tailwind component                |
| Passing React component to `resend.emails.send` | Render to HTML string first, then pass `html` to the send method                          |

## Delegation

- **Email template discovery**: Use `Explore` agent
- **Email styling review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `resend` skill is available, delegate email delivery tasks to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill resend`

## References

- [Built-in components: structure, content, and layout](references/components.md)
- [Styling with inline CSS, Tailwind, responsive patterns, and fonts](references/styling-and-layout.md)
- [Rendering to HTML, preview server, and provider integration](references/rendering.md)
