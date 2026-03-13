---
name: mio-skill
description: >-
  Personal context for AI agents via Mio. Loads user preferences, tech stack, coding conventions,
  and project context at session start so you can make informed decisions without re-asking.
  Use when any of these Mio MCP tools are available: get_context, list_categories, list_projects,
  set_active_project, log_conversation, update_profile. Triggers on: (1) session start to load
  user context before working, (2) code tasks where user conventions matter, (3) project-scoped
  work where project context is needed, (4) end of substantive conversations to log takeaways,
  (5) when the user expresses a new or changed preference to suggest a profile update.
---

# Mio — Personal Context for AI Agents

Mio gives you access to the user's personal context: their tech stack, coding conventions, communication style, project details, and preferences. Instead of asking the user to repeat themselves, check Mio first.

## Session Start

At the beginning of every conversation, load the user's context before doing anything else.

**For code tasks** (writing, reviewing, debugging, refactoring):

```
list_categories()
get_context({ query: "<describe what you're working on>", sources: ["tech_stack", "conventions"] })
```

**For general or broad tasks** (planning, brainstorming, communication):

```
get_context({ query: "<describe what you're working on>" })
```

Omitting `sources` returns all available categories — use this when you're unsure what you need.

**If working on a specific project:**

```
list_projects()
set_active_project({ project: "<project-uuid>" })
get_context({ query: "<describe what you're working on>" })
```

Setting the active project means all subsequent `get_context` calls automatically include that project's context. Do this once, early in the session.

## During Work

**Use the context, don't parrot it.** The point of loading context is to inform your decisions silently — not to quote it back to the user. If Mio says the user prefers TypeScript with arrow functions, just write code that way. Don't say "According to your Mio profile..."

**Don't re-ask things Mio already knows.** Before asking the user about their preferred language, framework, style, or conventions, check if Mio already has this information. Only ask when Mio doesn't have an answer.

**Refresh context when switching topics.** If the conversation shifts to a different project or domain, call `get_context` again with updated sources relevant to the new topic.

## End of Session

When a conversation has been **substantive** — you made decisions together, debugged something complex, or learned something new — log it:

```
log_conversation({
  summary: "Migrated auth from JWT to session cookies. Chose httpOnly + Secure flags for XSS protection.",
  takeaways: ["Prefers session-based auth over JWT", "httpOnly cookies are a hard requirement"],
  tags: ["authentication", "security"]
})
```

**What makes a conversation worth logging:**
- Architectural decisions were made
- New user preferences were expressed
- A complex problem was solved
- The user taught you something about their workflow

**Don't log:**
- Trivial one-off questions ("what time is it in UTC?")
- Simple lookups or file reads with no decision-making
- Conversations that produced no new information

## Profile Updates

When the user **explicitly states** a new or changed preference, suggest a profile update:

```
update_profile({
  category: "tech_stack",
  suggestion: "Uses Bun as package manager and runtime (switched from npm)",
  reason: "User explicitly said they switched from npm to Bun"
})
```

**Only suggest updates when:**
- The user clearly states a preference ("I use Bun now", "We switched to Tailwind")
- You learn a stable fact about their setup ("Our team does 2-week sprints")
- A convention is confirmed ("We always use conventional commits")

**Don't suggest updates for:**
- One-off decisions ("Let's use a Map here instead of an object")
- Assumptions or inferences you're not confident about
- Temporary context that won't apply to future sessions

All suggestions go to the user's review queue — they approve or reject each one. Never assume a suggestion was accepted.

## Graceful Degradation

Not all Mio tools may be available. Work with what you have:

- **Only `get_context` available?** Load context at session start, skip logging and profile updates.
- **No `list_projects`?** Skip project setup, use `get_context` without project scoping.
- **No `log_conversation`?** Focus on using context, skip end-of-session logging.
- **No tools at all?** This skill doesn't apply — proceed normally.

## Tool Reference

For detailed parameters, response formats, and advanced patterns for each tool, see [references/tool-patterns.md](references/tool-patterns.md).
