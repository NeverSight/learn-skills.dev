---
name: retro
description: "Look back at a session where the agent went wrong and change the repo's setup so the next session doesn't repeat it."
disable-model-invocation: true
---

# Retro

Look back at a coding session and propose changes to the agent's **environment**, not the code, so the next session avoids the same mistakes.

## 1. Read the session

Call the Skill tool with "writing-for-agents"; it governs every rule and pointer you write.

Default to the current session. If the user names another, find its log on this machine.

List the mistakes, each with its evidence (a quote, a file): every time the user corrected the agent, every finding the review raised, every time the agent spent long finding something or worked without information it needed.

## 2. Find the fix for each

Keep the mistakes that will happen again: one that happened twice, or one the repo's shape invites. Drop one-offs.

Look for candidates in these categories:

- **Automated checks**: a mistake a linter, a type, a test, or a hook could catch. Read the repo's own check commands first (its `lint`/`check` scripts, its CI workflow), so a check that exists but sits unwired or broken is the finding, not a reinvention. A repo with no guardrail at all (no pre-commit hook and no CI job running its lint, typecheck, or tests) is a finding in itself. A **mechanical** mistake (a banned API, an import shape, a file location) always gets a check, never a written rule.
- **Coding standards**: a **judgement call** the review missed, or a rule that misfired. Add, clarify, or remove it in `CODING_STANDARDS.md`.
- **Language**: the agent misused or invented a domain term. Fix `GLOSSARY.md` as the `domain-modeling` skill describes.
- **Navigation**: the agent took long to find something. Add a one-line pointer naming where it lives.
- **Information access**: the agent lacked something it needed, such as dev server logs, a test database, or read access to a third-party service.
- **Tool economy**: an expensive tool call, or a CLI or MCP server that spends tokens it doesn't need to.
- **Steering files**: instructions in `CLAUDE.md` or `AGENTS.md` (the repo's or the user's global one) that change nothing the agent would do anyway, or that belong in a check or `CODING_STANDARDS.md` instead.

## 3. Present

Present the candidates, most severe first. For each: the mistake and its evidence, the fix, and where it goes. Wait for the user to pick.

## 4. Apply what the user picked

- Show each new check failing on the real mistake before you keep it: reintroduce the mistake in a scratch change, run the check, see it fail, then drop the scratch change. A check you have never seen fail proves nothing.
- Commit each fix on its own, on the current branch. If you are on `main`, ask for a branch first.

## Where each fix lives

- **Automated checks**: everything mechanical. Nothing has to remember them.
- **`CODING_STANDARDS.md`**: judgement calls. `/review` reads it; implementation doesn't, so it costs the building agent nothing.
- **`CLAUDE.md` / `AGENTS.md`**: loaded into every session, so only pointers and the few rules every agent must follow before it writes code.
- **`GLOSSARY.md`**: domain terms.
