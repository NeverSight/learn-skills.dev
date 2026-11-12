---
name: karpathy-output-evolution
description: 'Upgrade LLM outputs from plain text to structured, rendered formats like HTML, Marp slides, or interactive dashboards. Use this skill when the user wants better-formatted output, needs to convert notes into a presentation, wants HTML output from an LLM, needs slides from a document, or says "make this prettier", "render this", "output as HTML", "make slides from this", "structured output", "Marp", "better format". Based on Karpathy 19k-like HTML output post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-education-first
  - karpathy-llm-wiki
  - karpathy-autoresearch
  - karpathy-idea-files
---

# Skill 7: Output Evolution（输出形式进化）

> Source: https://x.com/karpathy/status/2053872850101285137
> "HTML output + human-AI I/O evolution" — ~19k likes

## Core Principle

**Text is the lowest form of output. Demand structure.**

Karpathy's progression: `Text → Markdown → HTML → Interactive → (future) Neural`

Every LLM output can be upgraded. A wall of text becomes a rendered document. A list becomes a sortable table. An explanation becomes a slide deck. The information is the same — but legibility and retention multiply.

## The Output Evolution Ladder

```
Level 1: Plain text          ← most common, least useful for complex info
Level 2: Markdown            ← better, but not rendered in most contexts  
Level 3: Self-contained HTML ← renders anywhere, no dependencies
Level 4: Interactive HTML    ← sortable tables, collapsible sections, search
Level 5: Marp slides         ← presentations, teaching, sharing
Level 6: Data viz            ← charts, graphs, dashboards
```

**Default rule**: Always request at least Level 3 for any output you'll reuse or share.

## Prompt Templates by Output Type

### HTML Document (Level 3)
```
[YOUR CONTENT REQUEST]

Output format: A single self-contained HTML file.
Requirements:
- All CSS inline or in a <style> block (no external dependencies)
- Clean, readable typography (use system fonts: -apple-system, sans-serif)
- Proper heading hierarchy (h1 → h2 → h3)
- Key terms in <strong>, code in <code> blocks
- A table of contents at the top if > 3 sections
- Light/readable color scheme (#f8f9fa background, #212529 text)

Start with <!DOCTYPE html> and end with </html>. Nothing else.
```

### Marp Slides (Level 5)
```
[YOUR CONTENT REQUEST]

Output format: Marp markdown slide deck.
Requirements:
- Start with: ---\nmarp: true\ntheme: default\npaginate: true\n---
- Separate each slide with ---
- Max 5 bullet points per slide
- One key concept per slide
- Speaker notes after each slide (<!-- note: ... -->)
- First slide: title + author + date
- Last slide: "Key Takeaways" + 3-5 bullets

Total slides: [N] (default: one per major concept)
```

### Interactive HTML Table (Level 4)
```
Convert this data to an interactive HTML table:

[DATA]

Requirements:
- Self-contained HTML (CSS + JS inline)
- Sortable columns (click header to sort)
- Search/filter box at top
- Alternating row colors
- Responsive (works on mobile)
- Export to CSV button (optional)

Include only standard browser APIs, no jQuery or external libraries.
```

### Research Summary as HTML Report (Level 3-4)
```
[YOUR RESEARCH TOPIC OR NOTES]

Output: A self-contained HTML research report.
Structure:
1. Executive Summary (3 sentences)
2. Key Findings (bulleted, with confidence levels: HIGH/MED/LOW)  
3. Evidence (expandable sections, one per finding)
4. Open Questions
5. Sources (linked, with one-sentence descriptions)

Style: Clean academic report. Background #fff, readable font-size 16px, max-width 800px centered.
```

### Visual Comparison (Level 4)
```
Compare these [OPTIONS/APPROACHES/TOOLS]:

[LIST OF THINGS TO COMPARE]
[CRITERIA TO COMPARE ON]

Output: Self-contained HTML comparison page with:
- Side-by-side card layout (CSS grid)
- Color-coded ratings (green/yellow/red) for each criterion
- Summary recommendation at top
- No external CSS frameworks
```

## The Universal Upgrade Prompt

Apply to ANY existing text output to instantly improve it:

```
Take this content and upgrade it to a self-contained HTML document.

Content:
[PASTE ANY TEXT OR MARKDOWN]

Upgrade rules:
1. Structure the content with proper heading hierarchy
2. Make lists visually distinct (styled bullets or numbered lists)
3. Put any code in syntax-highlighted <pre><code> blocks
4. Add a reading time estimate at the top
5. Make it look like a well-designed blog post
6. Keep the content identical — only change the format

Output: complete HTML file, nothing else.
```

## Output Format Selection Guide

| Use Case | Best Format | Command |
|----------|------------|---------|
| Quick notes | Markdown | Default |
| Sharing with non-technical | HTML | "output as HTML" |
| Presentation | Marp | "make slides" |
| Data comparison | HTML table | "as comparison table" |
| Research summary | HTML report | "as research report" |
| Documentation | Markdown + ToC | "with table of contents" |
| Learning material | Marp + speaker notes | "as teaching slides" |

## Always Add This to Important Prompts

```
Output as a self-contained HTML file. No external dependencies.
Clean design. Renders directly in a browser.
```

## Workflow

**属于工作流：研究到发布（第3步）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第3步（包装） | karpathy-llm-wiki（知识沉淀后） | karpathy-education-first（教学化输出） |

完整链路：autoresearch → llm-wiki → output-evolution → education-first

## Prompt Contract

```text
Take this content: <RAW_CONTENT>. Choose the best output format from: Markdown table / Marp slides / self-contained HTML / interactive dashboard / diagram. Justify your choice in one sentence. Then produce the complete rendered-ready artifact. Requirements: self-contained (no external deps), renders correctly, structured for scanning not linear reading.
```

## Verification Checklist

- [ ] 输出格式匹配使用场景（分享→HTML，演示→Marp，分析→Dashboard）
- [ ] 文件完全自包含（无外部 CDN/依赖）
- [ ] 可以直接在浏览器中打开并正确渲染
- [ ] 结构支持扫读（有标题、表格、分区），不是一坨文字
- [ ] 移动端也能基本可读
