---
name: copy-editor
description: Review and edit copy for grammar, style, and clarity. Works with project style guides or uses sensible defaults. Use when reviewing marketing copy, blog posts, documentation, emails, or any business writing that needs polish.
allowed-tools: Read Write Edit Glob Grep
disable-model-invocation: true
---

# Copy Editor

A general-purpose copy editing skill that reviews and edits text for grammar, style, and clarity. Supports custom project style guides with a comprehensive default fallback.

## When to Use

- Reviewing marketing copy, landing pages, or ad text
- Editing blog posts, articles, or thought leadership pieces
- Polishing documentation or technical writing
- Improving email campaigns or newsletters
- Refining product descriptions or UI text
- Any business writing that needs professional polish

## Methodology

Follow these four phases sequentially for thorough copy review.

### Phase 1: Context Analysis

Before editing, understand the document:

1. **Document Type**: Marketing copy, blog post, documentation, email, etc.
2. **Target Audience**: Technical, general, executive, customer-facing
3. **Intended Tone**: Formal, conversational, persuasive, informative
4. **Purpose**: Inform, persuade, instruct, engage

Note these factors as they influence which style rules apply. Marketing copy allows more creative freedom than documentation.

### Phase 2: Style Guide Resolution

Locate the applicable style guide in this order:

1. **Project root**: Check for `STYLE_GUIDE.md`
2. **Claude directory**: Check for `.claude/style-guide.md`
3. **Docs folder**: Check for `docs/style-guide.md`
4. **Default fallback**: Use `references/DEFAULT_STYLE_GUIDE.md` from this skill

```bash
# Search for project style guide
glob "STYLE_GUIDE.md" || glob ".claude/style-guide.md" || glob "docs/style-guide.md"
```

If a project style guide exists, prioritize its rules. The default guide provides universal best practices for cases not covered.

### Phase 3: Line-by-Line Review

Systematically review the copy for:

**Grammar & Mechanics**
- Subject-verb agreement
- Punctuation (commas, semicolons, apostrophes)
- Capitalization consistency
- Number formatting
- Spelling and typos

**Voice & Clarity**
- Active vs. passive voice (prefer active)
- Sentence length and readability
- Jargon and unnecessary complexity
- Redundant words and phrases
- Parallel structure in lists

**Style Adherence**
- Consistency with style guide rules
- Tone appropriate for audience
- Brand voice alignment (if applicable)
- Formatting conventions

**Content Quality**
- Logical flow and transitions
- Clear headlines and subheadings
- Effective calls-to-action
- Accurate claims and statements

**AI Writing Tells** (see `references/AI_WRITING_TELLS.md`)
- Vocabulary clusters (delve, landscape, pivotal, robust, etc.)
- Formulaic phrases ("In today's...", "In conclusion...")
- Vague attributions ("some experts", "widely regarded")
- Structural patterns (mechanical balance, essay format)
- Sycophantic phrases ("I hope this helps")

### Phase 4: Structured Report

Present findings in this format:

```markdown
## Copy Review Report

**Document**: [filename or description]
**Word Count**: [count]
**Issues Found**: [total count]

### Summary
[1-2 sentence overview of document quality and main areas for improvement]

### Issues by Category

#### Grammar & Mechanics ([count])
| Location | Original | Issue | Suggested Fix |
|----------|----------|-------|---------------|
| Line X | "exact quote" | [issue type] | "corrected text" |

#### Voice & Clarity ([count])
| Location | Original | Issue | Suggested Fix |
|----------|----------|-------|---------------|
| Line X | "exact quote" | [issue type] | "corrected text" |

#### Style Guide Violations ([count])
| Location | Original | Rule Violated | Suggested Fix |
|----------|----------|---------------|---------------|
| Line X | "exact quote" | [rule reference] | "corrected text" |

#### AI Writing Tells ([count])
| Location | Original | Pattern Type | Suggested Fix |
|----------|----------|--------------|---------------|
| Line X | "exact quote" | [vocabulary/phrase/structure/attribution] | "corrected text" |

### Recurring Patterns
- [Pattern 1]: Appears X times - [recommendation]
- [Pattern 2]: Appears X times - [recommendation]

### Top 3 Recommendations
1. [Most impactful improvement]
2. [Second priority]
3. [Third priority]

### Style Guide Compliance
- [x] Active voice preference
- [ ] Number formatting (issues found)
- [x] Capitalization rules
- [ ] [Other applicable rules...]

### AI Writing Check
- [ ] No AI vocabulary clusters
- [ ] No formulaic phrases
- [ ] Specific attributions (not "some experts")
- [ ] Natural structure (not essay format)
```

## Guiding Principles

1. **Quote exactly**: Always show the original text verbatim
2. **Cite rules**: Reference specific style guide rules when applicable
3. **Preserve voice**: Maintain the author's style while improving clarity
4. **Prioritize impact**: Focus on issues that affect comprehension first
5. **Be constructive**: Frame suggestions positively, explain the "why"
6. **Note ambiguity**: When rules conflict or are unclear, explain options

## Output Options

Based on user request, provide:

- **Full report**: Complete analysis with all categories
- **Quick scan**: Top 5 most important issues only
- **Category focus**: Deep dive on specific area (grammar, style, etc.)
- **Inline edits**: Apply fixes directly with Edit tool (with user permission)

## Example Usage

```
User: Review my landing page copy for issues
Assistant: I'll use the copy-editor skill to review your landing page.

[Executes Phase 1-4, produces structured report]
```

```
User: Quick grammar check on this email
Assistant: I'll do a quick scan focusing on grammar and mechanics.

[Produces abbreviated report with top issues]
```
