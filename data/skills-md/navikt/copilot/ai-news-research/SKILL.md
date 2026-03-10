---
name: ai-news-research
description: Research and write monthly AI coding news summaries in Norwegian with working source links. Use when asked to write news, summarize AI coding trends, create a monthly update, or research what's new in GitHub Copilot, coding agents, AGENTS.md, skills, memory, agentic workflows, or developer experience.
---

# AI News Research

Research AI coding agent news and write a monthly summary in Norwegian. Output: `docs/news/<month>.md`.

## Step 1: Search

Run web searches (adjust month/year):

- `GitHub Copilot news [month] [year]`
- `AI coding agent trends [month] [year]`
- `AI coding agent hardening readiness enterprise [year]`
- `Reddit AI coding agents AGENTS.md skills context [year]`
- `site:github.blog copilot`

## Step 2: Fetch sources

For each hit, fetch the full page and extract facts, numbers, quotes, and the exact URL.

| Source | What to look for |
| --- | --- |
| github.blog | Official announcements, feature launches, deep-dives |
| Hacker News | Community reactions, real-world experiences |
| Reddit | Practitioner sentiment, pain points, success stories |
| LinkedIn | Thought leaders, experience reports |
| Anthropic, OpenAI, Google | Competing platforms, trend reports |

## Step 3: Write the summary

Cover these topics when relevant news exists:

- **Platform updates**: Copilot, Agent HQ, competing platforms
- **Agent context**: AGENTS.md, skills, instructions, prompts
- **Memory**: Cross-agent memory, session persistence
- **Agentic workflows**: CI/CD, background agents, continuous AI
- **Security**: Sandboxing, safe outputs, access controls
- **Readiness**: Enterprise adoption, maturity models
- **SDK/extensibility**: Copilot SDK, MCP servers, custom agents
- **Community sentiment**: What developers actually experience

Write in Norwegian (bokmål), direct tone, short sentences. Use English tech terms where developers do (e.g. "public preview", "PR", "repo"). See [OUTPUT-FORMAT.md](./references/OUTPUT-FORMAT.md) for the exact document structure and source citation rules.

## Step 4: Nav relevance

End with a "Relevans for Nav" table. Nav context:

- GitHub Copilot as sanctioned AI coding tool, ~500 tech professionals
- Nais platform (Kubernetes/GCP), Kotlin/Ktor, Next.js
- Strong security/privacy/accessibility requirements
- Measures developer experience (SPACE framework, DORA metrics)

## Example output

See [docs/news/february.md](../../../docs/news/february.md).
