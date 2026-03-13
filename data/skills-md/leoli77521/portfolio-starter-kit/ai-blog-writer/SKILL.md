---
name: ai-blog-writer
description: AI programming blog writing skill for tolearn.blog, targeting English-speaking audiences in Europe and America. Use this skill when creating blog posts, tutorials, or articles about AI, machine learning, LLMs, programming, and related tech topics. Triggers on keywords like "write blog", "blog post", "article", "tutorial", "tolearn", "AI programming", or content creation for technical audiences.
---

# AI Programming Blog Writer

专为 tolearn.blog 设计的博客写作技能，帮助创建面向欧美读者的高质量 AI 编程内容。

## Core Writing Principles

### Target Audience
- English-speaking developers and tech enthusiasts in US/Europe
- Skill levels: beginner to intermediate
- Interest areas: AI tools, LLMs, practical programming tutorials

### Voice & Tone
- Conversational but professional
- First-person perspective ("I discovered...", "Let me show you...")
- Avoid overly formal academic language
- Use humor sparingly and appropriately
- Be direct and actionable

### Content Structure

```
1. Hook (1-2 sentences) - Grab attention with a problem or question
2. Introduction (2-3 paragraphs) - Context and what reader will learn
3. Main Content - Step-by-step with code examples
4. Practical Tips - Real-world applications
5. Conclusion - Summary + Call to action
```

## SEO Optimization

### Title Guidelines
- Length: 50-60 characters (optimal for search)
- Format: `[Action Verb] + [Topic] + [Benefit/Year]`
- Examples:
  - "Build Your First AI Chatbot with Claude API in 2026"
  - "Master Prompt Engineering: 7 Techniques That Actually Work"

### Meta Description
- Length: 150-160 characters
- Include primary keyword naturally
- End with call-to-action or benefit

### Keyword Strategy
- Primary keyword in: title, H1, first paragraph, URL slug
- Use 2-3 related keywords naturally throughout
- Include long-tail variations

### Internal Linking
- Link to 2-3 related posts on tolearn.blog
- Use descriptive anchor text (not "click here")

## Writing Workflow

### Step 1: Topic Analysis
1. Identify the core problem/question
2. Research current trends and competitors
3. Find unique angle or fresh perspective

### Step 2: Outline Creation
Create structured outline before writing:
```markdown
# [Title]

## Introduction
- Hook: [attention grabber]
- Problem: [what reader struggles with]
- Promise: [what they'll learn]

## Section 1: [Foundation]
- Key concept
- Code example

## Section 2: [Implementation]
- Step-by-step guide
- Common pitfalls

## Section 3: [Advanced Tips]
- Pro techniques
- Real-world examples

## Conclusion
- Key takeaways (3-5 bullets)
- Next steps / CTA
```

### Step 3: Draft Writing
- Write first draft without editing
- Focus on teaching, not impressing
- Include code snippets with comments
- Add screenshots/diagrams where helpful

### Step 4: Polish
- Check for clarity and flow
- Verify all code examples work
- Add transition sentences
- Optimize for SEO

## Code Examples Best Practices

### Formatting
```python
# Always include comments explaining what the code does
# Use realistic variable names
# Show complete, runnable examples

from anthropic import Anthropic

client = Anthropic()

# Create a simple chat completion
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(response.content[0].text)
```

### Code Block Guidelines
- Specify language for syntax highlighting
- Include expected output when helpful
- Break long code into digestible chunks
- Explain BEFORE showing code, not after

## Content Categories

### Tutorial Posts (How-to)
- Step-by-step instructions
- Prerequisites clearly stated
- Expected time to complete
- Troubleshooting section

### Explanation Posts (What/Why)
- Concept breakdown
- Real-world analogies
- Comparison tables
- Visual diagrams

### News/Analysis Posts
- Timely topics
- Personal perspective
- Implications for readers
- Actionable takeaways

## Quality Checklist

Before publishing, verify:

- [ ] Title is 50-60 characters and compelling
- [ ] Meta description is 150-160 characters
- [ ] First paragraph hooks the reader
- [ ] All code examples are tested and working
- [ ] Headings follow logical H2 → H3 hierarchy
- [ ] Images have alt text
- [ ] Internal links to 2-3 related posts
- [ ] Call-to-action in conclusion
- [ ] No grammar/spelling errors
- [ ] Reading time is appropriate (5-10 min ideal)

## Reference Files

- For detailed SEO guidelines: See [references/seo-guide.md](references/seo-guide.md)
- For content templates: See [references/templates.md](references/templates.md)
- For writing style examples: See [references/style-examples.md](references/style-examples.md)
