---
name: document-creation
description: Create structured documents from conversations, summaries, or content in open formats (markdown, PDF, text). Use when the user requests document creation, report generation, content export, conversation summaries, or structured documentation. Triggers include "create a document", "make a report", "summarize this conversation", "export to PDF/markdown", or any request to formalize content into a document. Works independently or integrates with design-assistant skill for polished visual output.
---

# Document Creation

Generate structured documents from conversations, summaries, and content in open formats.

## Core Capabilities

**Supported formats:**
- Markdown (.md) - Structured text with formatting
- PDF (.pdf) - Professional documents with optional visual polish
- Text (.txt) - Plain text for maximum compatibility

**Document types:**
- Conversation summaries - Extract and structure chat content
- Executive reports - Polished summaries for leadership
- Technical documentation - Structured reference materials
- Meeting notes - Organized action items and decisions
- Project briefs - Scoped overviews and requirements

## Workflow

### 1. Determine Document Type

Identify the document's purpose and audience:

**Executive/Client-facing:** Reports, presentations, proposals, executive summaries
→ Use design-assistant skill for visual polish

**Internal/Working:** Meeting notes, drafts, technical docs, quick summaries  
→ Create directly without design enhancement

**Triggers for design integration:**
- User explicitly requests "professional", "polished", or "presentation-ready"
- Document is labeled as executive summary, client report, or proposal
- Context suggests external audience

### 2. Extract and Structure Content

**From conversations:**
- Identify key points, decisions, and action items
- Remove conversational artifacts (greetings, clarifications)
- Organize chronologically or thematically
- Preserve important context and reasoning

**From summaries:**
- Condense while maintaining essential information
- Use clear hierarchical structure
- Highlight critical insights upfront
- Include relevant details without bloat

### 3. Apply Format-Specific Patterns

**Markdown:**
- Use headers (# ## ###) for hierarchy
- Bold for emphasis, italics for nuance
- Lists for structured information
- Code blocks for technical content
- Links for references

**PDF (without design skill):**
- Clean, readable typography
- Adequate whitespace
- Consistent formatting
- Professional but simple appearance

**PDF (with design-assistant):**
- Enhanced visual hierarchy
- Brand-appropriate styling
- Professional layout and graphics
- Executive-ready presentation

**Text:**
- Clear line breaks for readability
- Minimal formatting, maximum compatibility
- Section markers using caps or delimiters

### 4. Structure Guidelines

**Standard document structure:**

```
Title/Header
- Clear, descriptive

Executive Summary (if appropriate)
- 2-3 sentences maximum
- Key takeaway upfront

Body Content
- Logical sections with clear headers
- Scannable with visual hierarchy
- Bullet points for lists
- Paragraphs for detailed explanation

Conclusion/Next Steps (if appropriate)
- Action items
- Decisions required
- Follow-up needed
```

**For conversation summaries:**

```
Summary of [Topic/Meeting]
Date: [date]

Key Decisions:
- [Decision 1]
- [Decision 2]

Discussion Points:
- [Point 1]: [Brief explanation]
- [Point 2]: [Brief explanation]

Action Items:
- [ ] [Action item 1] - [Owner]
- [ ] [Action item 2] - [Owner]

Next Steps:
- [What happens next]
```

## Integration with Design Skill

When visual polish is needed:

1. Create the document content first (markdown or structured text)
2. Invoke design-assistant skill with content and context
3. Specify document type (report, brief, summary)
4. Let design skill handle visual formatting and PDF generation

**Don't trigger design skill when:**
- User requests a "quick summary" or "notes"
- Document is explicitly internal or draft
- User specifies "simple" or "basic" format
- Speed is prioritized over appearance

## Best Practices

**Clarity:**
- Lead with the most important information
- Use active voice
- Avoid jargon unless audience-appropriate
- Define acronyms on first use

**Scannability:**
- Break long paragraphs into shorter ones
- Use headers to create visual hierarchy
- Employ bullet points for lists
- Bold key terms sparingly

**Conciseness:**
- Remove redundant information
- Combine related points
- Eliminate filler words
- Respect the reader's time

**Accuracy:**
- Verify facts from conversation
- Maintain original meaning
- Note uncertainties or assumptions
- Date-stamp when relevant

## Output Location

Save documents to `/mnt/user-data/outputs/` and provide computer:// links for user access.

## Example Triggers

- "Create a document summarizing our conversation"
- "Make a report about [topic]"
- "Export this to PDF"
- "Document this in markdown"
- "Generate meeting notes from this discussion"
- "Create an executive summary of our analysis"
- "I need this formatted as a professional report"
