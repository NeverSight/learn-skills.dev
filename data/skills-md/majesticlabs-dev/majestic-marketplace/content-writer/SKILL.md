---
name: content-writer
description: Write well-structured articles with outline-first workflow. Includes sentence variation, readability guidelines, and formatting best practices.
triggers:
  - write article
  - content writer
  - write content
  - article outline
  - blog post
allowed-tools: Read Write Edit Grep Glob WebSearch mcp__perplexity-ask__perplexity_ask
---

# Content Writer

Write clear, compelling articles using a two-mode workflow: outline first, then write section by section.

## Two Modes

This skill operates in two modes:
1. **Outline Mode** - Research and structure the article
2. **Write Mode** - Fill in each section with quality content

Always start with outline mode before writing.

---

## Outline Mode

When the user provides a topic, create an outline before writing.

### Steps

1. **Clarify** - Ask questions if the topic or audience is unclear
2. **Research** - Use web search to understand the topic thoroughly
3. **Structure** - Create the outline

### Outline Format

```markdown
# [Title - max 70 characters, sentence case]

[Brief intro - 2-3 sentences introducing the topic. No "Introduction" heading.]

## [Section 1 heading]
[Description of what this section covers]

## [Section 2 heading]
[Description of what this section covers]

## [Section 3 heading]
[Description of what this section covers]

(Maximum 5 sections)
```

### Title Rules

- Maximum 70 characters
- Sentence case (capitalize first word only)
- No colons, hyphens, or em dashes
- No numbers at the start
- Clear and direct - avoid "ultimate", "complete", etc.

### Section Rules

- Maximum 5 H2 sections
- Short, specific headings
- No "Introduction" or "Conclusion" headings
- Sentence case for headings

---

## Write Mode

After the outline is approved, write one section at a time.

### Process

1. Read the previous section (if any) to maintain flow
2. Research using web search to verify facts
3. Write the section
4. Confirm completion before moving to next

### Section Constraints

- **Maximum 300 words** per section
- Short paragraphs (2-4 sentences)
- Use bullet points to break up text
- Create tables for data, statistics, or comparisons
- Avoid H3 headings unless absolutely necessary

### Fact-Checking

- Only include facts or data you've verified via web search
- If recommending a package/tool, verify it exists
- Don't make claims you can't support

---

## Writing Style

### Readability

Write at a **Flesch-Kincaid 8th-grade level**:
- Short sentences (average 15-20 words)
- Common words over jargon
- Active voice over passive
- One idea per paragraph

### Sentence Variation

Vary sentence length to create rhythm. Follow Gary Provost's lesson:

**Bad example (monotonous):**
> This sentence has five words. Here are five more words. Five-word sentences are fine. But several together become monotonous. Listen to what is happening. The writing is getting boring.

**Good example (musical):**
> Now listen. I vary the sentence length, and I create music.
>
> Music.
>
> The writing sings. It has a pleasant rhythm, a lilt, a harmony. I use short sentences. And I use sentences of medium length. And sometimes when I am certain the reader is rested, I will engage him with a sentence of considerable length, a sentence that burns with energy and builds with all the impetus of a crescendo.
>
> So write with a combination of short, medium, and long sentences. Create a sound that pleases the reader's ear.

### Formatting

- Use **bold** for key terms on first mention
- Use bullet points for lists of 3+ items
- Create markdown tables for data/statistics
- Keep paragraphs short (3-4 lines max)
- Add line breaks between distinct thoughts

---

## Avoiding AI Slop

AI-generated text has telltale patterns. Avoid them to sound human.

**Quick rules:**
- No "In today's landscape..." openings
- No "In conclusion..." closings
- No "delve", "tapestry", "realm", "pivotal" clusters
- No vague experts ("some believe...", "many argue...")

**Common replacements:**

| AI Word | Human Word |
|---------|------------|
| delve | explore, look at |
| landscape | field, area |
| leverage | use |
| pivotal | key, important |
| robust | strong, solid |
| comprehensive | complete, full |

**Full reference:** See `references/AI_WRITING_TELLS.md` in `copy-editor` skill for:
- 50+ AI vocabulary words with replacements
- Phrase patterns to avoid
- Structural tells (formulaic sections)
- Detection checklist

---

## Output

### Outline Output

Return the outline as markdown. If the user specified a file path, write it there.

### Article Output

Return completed sections as markdown. Update the outline file with written content as you go.

---

## What This Skill Does NOT Do

- SEO keyword optimization (use `content-optimizer`)
- Editing existing content (use `copy-editor`)
- Sales copy or landing pages (use `landing-page-builder`)

## When to Use This vs. Other Skills

| Use `content-writer` when... | Use other skills when... |
|------------------------------|--------------------------|
| Writing new articles from scratch | Editing existing copy (`copy-editor`) |
| Need structured outline first | Optimizing for SEO (`content-optimizer`) |
| Blog posts, guides, how-tos | Sales pages (`landing-page-builder`) |
| Educational content | Marketing copy (`slogan-generator`) |
