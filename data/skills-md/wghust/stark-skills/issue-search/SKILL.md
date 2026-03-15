---
name: issue-search
description: |
  Search related GitHub issues when encountering problems. Analyzes user questions to identify relevant open-source libraries, searches their GitHub issues using gh CLI, and returns relevant issue links with titles and status.
  搜索相关的 GitHub issues。分析用户问题以识别相关开源库，使用 gh CLI 搜索其 GitHub issues，并返回相关 issue 链接、标题和状态。
triggers:
  - github issue
  - search issue
  - find issue
  - related issue
  - 搜索 issue
  - 查找问题
  - github 问题
---

# issue-search Skill

> **Language**: Respond in the same language as the user (中文提问则中文回答).

Search related GitHub issues across multiple repositories based on user questions.

---

## Execution Flow

### Step 0 · Check gh CLI

Verify `gh` CLI is available:

```bash
command -v gh
```

If not available, provide fallback web search URLs.

---

### Step 1 · Analyze Question

Extract keywords and identify relevant repositories:

**Technology mapping:**
- react → facebook/react
- next, nextjs → vercel/next.js
- typescript, ts → microsoft/TypeScript
- vue → vuejs/core
- tailwind → tailwindlabs/tailwindcss
- vite → vitejs/vite
- webpack → webpack/webpack
- eslint → eslint/eslint
- prettier → prettier/prettier
- node, nodejs → nodejs/node

Extract error messages and technical terms from user question.

---

### Step 2 · Search GitHub Issues

**Method A: gh CLI (Primary)**

For each identified repository (max 3), try `gh` CLI first:

```bash
gh issue list --repo <owner/repo> --search "<keywords>" --limit 5 --json number,title,state,url
```

**Method B: WebFetch (Fallback)**

If `gh` CLI fails or is unavailable, use WebFetch to access GitHub search page:

1. Construct search URL:
```
https://github.com/<owner/repo>/issues?q=<keywords>
```

2. Use WebFetch tool:
```
WebFetch(url, prompt="Extract GitHub issues from this search page. For each issue, provide: issue number, title, state (open/closed), and full URL. Return up to 5 issues.")
```

3. Parse response to extract:
   - Issue number (e.g., #69064)
   - Issue title
   - Issue state (open/closed)
   - Full URL (e.g., https://github.com/vercel/next.js/issues/69064)

---

### Step 3 · Present Results

展示每个 issue 的关键信息：**标题、状态、可点击链接**。具体呈现格式由 AI 根据上下文自主决定。

---

## Error Handling

| Error | Action |
|---|---|
| `gh` not installed | Use WebFetch fallback |
| `gh` not authenticated | Use WebFetch fallback, suggest `gh auth login` |
| WebFetch fails | Provide search URL as last resort |
| No results found | Suggest broader search terms |
| API rate limit | Suggest trying again later |

---

## Examples

### Example A — React error

**Input:** "Why does my React component re-render unexpectedly?"

**Actions:**
1. Identify repository: facebook/react
2. Extract keywords: "component re-render"
3. Search: `gh issue list --repo facebook/react --search "component re-render" --limit 5`
4. Display results with links

### Example B — Next.js error (Chinese)

**Input:** "Next.js 出现 hydration 错误怎么办？"

**Actions:**
1. 识别仓库: vercel/next.js
2. 提取关键词: "hydration 错误"
3. 搜索: `gh issue list --repo vercel/next.js --search "hydration error" --limit 5`
4. 用中文展示结果
