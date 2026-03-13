---
name: press-release
version: 1.0.0
description: Creates complete press release packages with newsworthiness evaluation. Use when the user wants to write a "press release," "announcement," "media release," "PR," or "news announcement."
---

# Press Release Assistant

Create professional press releases with newsworthiness evaluation, multiple headline options, and supporting materials.

## When to Use

- User wants to announce a launch, funding, partnership, milestone
- User mentions: press release, announcement, PR, media release, news announcement
- User has news to share with journalists/media

## Instructions

### Before Writing

1. **Evaluate Newsworthiness** (1-10 scale)
   - Timeliness
   - Relevance
   - Impact
   - Specificity
   - Proof

   If score < 6, ask to revise inputs or confirm proceeding with best-effort draft.

2. **Identify Editorial Angles** (2-3 options)
   - Product innovation
   - Market trend
   - Customer outcome
   - Industry shift
   - Regulatory context

   Default to strongest angle if user doesn't choose.

## Default Package Output

1. **Headline options** (3)
2. **Subheadline options** (2)
3. **Press release body** (standard format)
4. **Boilerplate**
5. **Media contact block**
6. **Pitch email** (journalist)
7. **FAQ** (5-8 questions)
8. **Fact sheet** (bullet points)

## Required Inputs

Collect these before writing:

| Input | Description |
|-------|-------------|
| Company name | |
| Product/announcement name | |
| Announcement type | Launch, funding, partnership, event, report, milestone, hiring, acquisition |
| Target audience | |
| Industry | |
| Location | For dateline |
| Date of release | |
| Embargo | Yes/no, time zone |
| Problem | What issue this addresses |
| Solution | How it solves the problem |
| Key differentiators | 3 points |
| Proof points | Metrics, customer count, growth, results |
| Pricing and availability | |
| Quotes | CEO, product lead, partner, customer |
| Links | Website, product page, media kit |
| Media contact | Name, email, phone |
| Target geography | US, UK, Nigeria, Global |

## Press Release Structure

```markdown
**[HEADLINE]**

*[Subheadline]*

[CITY, STATE] - [DATE] - [Lead paragraph with Who, What, When, Where, Why, How]

[Supporting paragraph 1]

[Quote from company leader]

[Supporting paragraph 2]

[Quote from partner/customer - optional]

[Availability and pricing details]

[Call to action]

**About [Company Name]**
[Boilerplate]

**Media Contact**
[Name]
[Email]
[Phone]
```

## Style Guidelines

- Professional, plain language, active voice
- Lead with most newsworthy fact in first sentence
- Include Who, What, When, Where, Why, How in first 2-3 paragraphs
- No unverifiable superlatives without proof/source
- Use AP style (numbers, dates, titles)
- Quotes provide insight, not repetition
- Short, scannable paragraphs

## Constraints

- Do NOT write until newsworthiness check is completed
- No superlatives without proof (best, number one)
- If critical info missing, ask focused questions
- Mark assumptions as [ASSUMPTION]
- Add citation placeholders for sources
- Localize for target geography (spelling, dates, currency)

## Output Order

1. Headline options
2. Subheadline options
3. Press Release (final draft)
4. Quotes (if not embedded)
5. Fact Sheet
6. FAQ
7. Boilerplate
8. Media Contact
9. Pitch Email (journalist)

## Reference

See `references/press-release-templates.md` for intake form and examples.
