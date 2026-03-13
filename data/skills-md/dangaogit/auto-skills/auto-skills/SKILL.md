---
name: auto-skills
description: Universal skill router for almost all user requests. Aggressively trigger this skill by default for ANY task-oriented prompt (build, fix, explain, plan, review, debug, optimize, migrate, write docs, create scripts, automate workflows, or "how to do X"), including multilingual and mixed-language input. Always attempt skill retrieval first using order project skills -> user skills -> find-skills, then recommend only the top 3 most precise candidates. Only skip when the user explicitly asks to bypass skill lookup.
---

# Auto Skills

## Goal

Improve skill hit rate and recommendation quality by:

- Following strict lookup priority.
- Returning only top 3 precise skills.
- Supporting multilingual matching (especially Chinese query to English skills).
- Guiding users to install/attach selected skills in supported environments.

Hard gate:

- For any action-oriented prompt, run skill routing first before execution.

Default operating mode:

- Try this skill first for nearly every user request with actionable intent.
- Treat "no explicit skill request" as still eligible for skill routing.
- Optimize for high trigger rate first, then precision reranking.

## Mandatory Lookup Priority

Always run lookup in this order:

1. Project-local skills (current project)
2. User-global skills (user directory)
3. `find-skills` discovery (only when needed to fill gaps or improve precision)

Do not invert this order.

## Trigger Policy (High Recall)

Trigger this skill for:

- Any request with action intent: build, create, implement, refactor, fix, debug,
  review, design, plan, optimize, migrate, test, deploy, automate, document,
  commit, release, changelog, versioning, publish, push.
- Any request with uncertainty or discovery intent: "怎么做", "有没有办法",
  "推荐", "选型", "最佳实践", "what should I use", "is there a skill for ...".
- Common ops keywords: "提交", "发版", "更新日志", "版本", "发布", "推送",
  "commit", "release", "changelog", "version", "publish", "push".
- Any domain-specific request even without the word "skill".
- Mixed-language or typo-heavy prompts.

Only do not trigger when:

- User explicitly says "不要查 skill / skip skills".

## Core Behavior

### 1) Query understanding and normalization

Before matching:

- Detect language of user query.
- Normalize query text:
  - Lowercase, remove punctuation noise.
  - Expand abbreviations (for example: "ws" -> "websocket").
  - Split intent words and domain words.
- Build multilingual expansion terms:
  - Chinese <-> English concept mapping first.
  - Add synonyms and related action verbs.

Examples:

- "流程图编辑器" -> "flowchart", "graph editor", "diagram"
- "连线规则" -> "edge connection", "validateConnection", "routing"
- "技能推荐" -> "skill discovery", "capability matching"

### 2) Precision-first matching

Score skills by weighted signals:

- Intent match (what user wants to do)
- Domain match (topic/tech stack)
- Output/task match (what kind of deliverable user expects)
- Trigger-description overlap

Use two-stage ranking:

1. High-recall candidate generation (wide net).
2. Precision reranking (return strongest top 3 only).

### 2.1) Cost-aware ranking (prefer free first)

Apply this ranking policy by default:

- Prefer non-paid/free skills when relevance is comparable.
- Avoid recommending paid skills in top 3 when free alternatives have acceptable
  relevance.
- Allow paid skills in top 3 only when free candidates are clearly low relevance
  or cannot satisfy the task.

Practical rule:

- If a free candidate is within a close relevance band of a paid candidate,
  rank the free candidate higher.
- If all free candidates are below relevance threshold, allow paid candidates.

### 3) Top 3 recommendation only

Return exactly up to 3 skills:

- If >= 3 high-confidence matches: return top 3.
- If only 1-2 high-confidence matches: return only those.
- Do not pad with weak candidates.

### 4) Installation/attachment prompt (tool-dependent)

If environment supports adding skills (for example Cursor):

- Ask user whether to add selected skill to:
  - This session
  - Current project
  - User directory (global)

Ask before performing placement changes.

### 5) Route first, then delegate specialized skills

When a specialized skill exists (for example commit/release/domain-specific):

- Do not bypass routing.
- Run auto-skills routing first, then delegate to the best specialized skill.
- Keep top-3 recommendation behavior intact before delegation.

### 6) Runtime initialization awareness (project rule recommendation)

When this skill is matched, if the user has not made a decision yet about adding
project rules (accepted or declined), proactively recommend adding a project
fallback rule so routing behavior is consistently applied in that project.

Recommended action:

- Suggest creating `.cursor/rules/auto-skills-first.mdc`.
- Explain benefit in one line: "ensure route-first behavior before execution".
- Ask for confirmation before creating/modifying project rule files.

Suggested rule snippet:

```md
---
description: Route action requests through auto-skills first
alwaysApply: true
---

# Auto-Skills First

For any action-oriented user prompt, run `auto-skills` routing before direct task execution.

Mandatory routing order:
1. Project skills
2. User-global skills
3. `find-skills` discovery

Skip condition:
- Only skip routing when the user explicitly says to bypass skill lookup.
```

## Response Template

Use this concise structure:

1. `Match Confirmation`
   - `auto-skills matched: <short reason>`
2. `Top Recommendations (max 3)`
   - Skill name
   - Why it matches (1 line)
   - Suggested scope (session/project/user)
3. `Optional next action`
   - Ask user to choose 1/2/3 (or none)
   - If supported: ask where to add it
   - If rule decision is unknown: recommend adding project fallback rule

## Suggested Interaction Pattern

When user asks for skill help:

1. Run priority lookup.
2. Produce top 3 precise recommendations.
3. Ask for selection.
4. If supported, ask install scope.
5. Confirm applied result.

## Multilingual Match Strategy

Use a small internal strategy for robust multilingual hit rate:

- Intent dictionary: actions like build/fix/review/plan/search.
- Domain dictionary: framework/library/platform terms.
- Cross-language aliases:
  - Chinese -> English primary mapping.
  - English acronym -> full phrase.
- Fuzzy tolerance:
  - Handle typos and mixed-language prompts.

Never require users to use exact skill names.

## Safety and Quality Rules

- Never recommend more than top 3 in one response.
- Prefer existing installed skills before discovery.
- Prefer free skills over paid skills unless relevance is insufficient.
- Avoid generic recommendations when a specialized skill exists.
- Explain recommendation reasons briefly and concretely.
- If uncertain, ask one focused follow-up question instead of guessing.

## Extra Ideas (Built-in Enhancements)

### A) Confidence threshold gate

If all candidates are low confidence, ask a single clarifying question and rerank.

### B) Feedback memory

Track user accepted/rejected skills in-session to improve future ranking.

### C) Diversity control

Avoid returning three near-duplicate skills; keep recommendations complementary.

### D) Fast fallback

If no suitable skill is found, provide:

- Best baseline skill (if any), and
- A short suggestion to install a new specialized skill via `find-skills`.
