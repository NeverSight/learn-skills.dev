---
name: blog-to-obsidian
description: "A tool to automatically scrape foreign blog articles, summarize them, translate them paragraph by paragraph, and save them as Markdown files with profuse Obsidian bidirectional links. Trigger when users want to process, translate, or summarize a web article/blog into their Obsidian vault (e.g., 'help me read this article', 'translate this blog to obsidian')."
---

# Blog to Obsidian

This skill defines the exact workflow and prompting strategy you must use when a user asks you to translate and summarize a blog post into their Obsidian vault.

**You will perform this task yourself** using your web fetching capabilities and LLM reasoning, rather than relying on external python scripts. This allows for much higher quality and nuance in the translation.

## The Workflow

When triggered with a URL, follow these steps exactly:

### Step 1: Scrape the Content
1. Use the `webfetch` tool (or similar capability) to read the content of the provided URL.
2. Only focus on the main article body. Ignore comments, sidebars, and navigation elements.

### Step 2: Analyze and Summarize
Read the entire article carefully. You need to extract:
1. **Tags**: Relevant keywords (e.g., `AI`, `TechBubbles`). **IMPORTANT: Do NOT use the `#` prefix for tags in the YAML frontmatter.**
2. **Executive Summary (中文)**: A single sentence capturing the absolute core point of the article.
3. **Objective Opinion (中文)**: Your objective, unbiased analysis of the article's perspective.
4. **Key Arguments & Evidence (中文)**: A bulleted list of the main arguments, and the evidence/logic used to support them.
5. **Golden Sentences (中英双语)**: The most impactful quotes from the article. Provide the original English, followed immediately by the Chinese translation.

### Step 3: Paragraph-by-Paragraph Translation with Bidirectional Links
This is the most critical step. You must translate the article body into Simplified Chinese, paragraph by paragraph.

**Rules for Translation:**
- **Format**: Original English paragraph first, followed by the Chinese translation paragraph.
- **Bidirectional Links (`[[...]]`)**: In the **Chinese translation only**, you MUST profusely inject Obsidian internal links.
    - Link every **Named Entity** (People, Companies, Places, Software, Technologies).
    - Link key **Abstract Concepts** (e.g., `[[人工智能]]`, `[[供应链]]`, `[[心流]]`, `[[认知负荷]]`).
    - Link specific **Dates** or **Events**.
    - *Goal*: Maximize the potential for future creative connections in a Zettelkasten. Be aggressive with linking nouns and concepts.
    - *Format*: `...提到了[[OpenAI]]的最新模型...`

### Step 4: Format and Save
Format your output exactly according to the template below and use the `write` tool to save it.

- **Directory**: `<YOUR_OBSIDIAN_VAULT_ABSOLUTE_PATH>/Inbox` (Note: Always use forward slashes `/` for paths to avoid AI processing overhead. The directory already exists, DO NOT call `mkdir` or any bash tools to verify or create it. Write the file directly.)
- **Filename Format**: `YYYY-MM-DD_文章中文标题.md` (e.g., `2026-02-28_这次不一样.md`). Use the article's publication date if available, otherwise use today's date. Remove any invalid characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) from the title before saving.

---

## Output Template

Your final output to be written to the file MUST follow this exact structure:

```markdown
---
created: YYYY-MM-DD
url: <Original_URL>
tags:
  - Input/Blog
  - <Tag1>
  - <Tag2>
  - <Tag3>
---

# <文章中文标题>

> [!abstract] Executive Summary
> **核心主旨**: <一句话总结，必须是中文>
>
> **Objective Opinion**: <客观评价，必须是中文>

## 💡 核心论点与论据 (Key Arguments)
- **<论点1（中文）>**
    - *Evidence*: <支持该论点的证据/逻辑（中文）>
- **<论点2（中文）>**
    - *Evidence*: <支持该论点的证据/逻辑（中文）>

## ✨ 金句摘录 (Highlights)
> "<Original English Quote 1>"
> —— <中文翻译 1>

> "<Original English Quote 2>"
> —— <中文翻译 2>

---

## 📝 中英对照阅读 (Bilingual Read)

<Original English Paragraph 1>

<包含大量[[双向链接]]的中文翻译段落 1>

<Original English Paragraph 2>

<包含大量[[双向链接]]的中文翻译段落 2>

... (continue for all main paragraphs)
```