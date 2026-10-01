---
name: current-sources
description: Researches before answering instead of relying on training data. Use for ANY question about library APIs, framework usage, SDK methods, config options, syntax, deprecation status, current versions, or "latest" anything — and for any factual question where being wrong is costly. Queries BOTH official documentation AND the live web. Triggers on "how do I use X", "what is the latest", "is X deprecated", "current version of", "X vs Y", import statements, error messages, API references, CLI flags, environment variables, release notes, migration guides, or any question whose answer may have changed since training.
---

# Current Sources

Answer from verified sources, not from memory. This skill exists because
training data is a snapshot: it goes stale silently, and a confidently wrong
answer about a deprecated API is worse than no answer at all.

## The core rule

**Search before answering whenever the answer could have changed.**

The failure mode this prevents: you "know" a library's API from training,
the API was rewritten two versions ago, and you give a fluent answer that is
wrong. Nothing in the response signals a problem. That is the worst outcome.

If you did not verify it this session, you do not know it.

## Route by question type

Do not reach for one source for everything. Pick per question:

| Question is about | Go to | Why |
|---|---|---|
| Library API, SDK method, framework pattern | Official docs for the exact version | Canonical, version-pinned, no blog rot |
| Config keys, CLI flags, env vars | Official docs, then source repo | Docs miss edge cases; the repo does not lie |
| "Latest", current version, release status | Web search, then changelog | Moves fast; docs may lag |
| Deprecation or migration | Changelog and migration guide first | Docs often keep old pages alive |
| Best practice, patterns, opinions | Official docs first, then web | Docs carry the canonical position |
| Current events, pricing, policy | Web search only | Nothing in docs |
| Codebase-specific questions | Read the local code | Nothing external is authoritative here |

**Cross-check when the answer is version-sensitive.** Docs tell you the
intended API. Release notes tell you whether it still exists. If they
disagree, believe the newer source.

## Pin the version before reading the docs

A doc page for the wrong version is a confidently wrong answer.

1. Find the installed version — check `package.json`, lockfile, `go.mod`,
   `pyproject.toml`, `Gemfile.lock`, or ask.
2. Request docs for that version specifically.
3. If the installed version is older than the docs you found, the docs are
   describing an API that may not exist in the project. Say so.

## Freshness checks

When you retrieve something, confirm it is current:

- **Look for a version or date on the page.** Undated content is unverified.
- **Prefer official over third-party** for anything about how something works.
- **Treat as suspect:** blog posts over ~2 years old, undated tutorials,
  unanswered forum threads, anything without a version number.
- **Live search results are not proof of currency.** A page can rank well and
  still be outdated. Check for a date before relying on it.

## Deprecation triage

Before recommending any API, function, flag, or option:

1. Is it marked deprecated? Look for banners, changelog entries, release notes.
2. Is there a replacement? Migration guides name the successor.
3. Is it actually gone, or just discouraged? These are different problems and
   the fix is different.

If something is deprecated, say so explicitly and name the replacement. Do not
present a deprecated API as a current option just because you remember it.

## If you cannot verify

Sometimes sources conflict, are unavailable, or a package is too obscure to
have documentation. Then say that plainly:

- Name what you tried and what you found.
- Mark the specific claim you are unsure about.
- Never present unverified recall in the same voice as verified fact.

Separating "the docs say" from "I believe" is the whole point. Collapsing them
is the failure this skill exists to prevent.

## Reporting

When you answer from a retrieved source, keep the attribution visible:

- Name the source and version for library facts.
- Give the date for fast-moving facts.
- Flag anything you could not confirm.

The user should be able to tell, per claim, whether it was checked or recalled.

## Example

Question: "How do I validate environment variables in a Next.js 15 app?"

Without this skill: answer from memory with a generic snippet — possibly
a deprecated API, no version stated.

With this skill:
1. Check `package.json` — the project is on Next.js 15, so docs must match it.
2. Search current docs for the validation library's latest API, plus its
   changelog for deprecations since training.
3. Answer with the verified pattern, the library version checked, and the
   source — flagging anything that could not be confirmed rather than
   filling the gap from memory.

## Limits — read this honestly

This skill is **opt-in and instruction-based**. It is read when the agent
decides to read it, and followed when the agent decides to follow it. That
means:

- It reliably improves quality **once loaded**.
- It **cannot guarantee** that it loads on every question, or that every
  instruction is followed on every turn.

No skill format can enforce that. The only mechanism that persists across
every session and every request is a standing rule in `AGENTS.md`. If this
behavior is mandatory rather than preferred, that file is where it belongs —
see the example below.

## Pair with a standing rule

The skill covers *how* to research correctly. A persistent instruction covers
*whether* to research at all. Together they close the gap; either alone leaves it open.

Example `AGENTS.md` line:

```markdown
For any question about an external library, API, framework, tool, or
"current"/"latest" state, look it up before answering. Prefer official
documentation for how something works, and the web for current status.
State the version and date of what you found. Never answer version-specific
questions from memory, and flag anything you could not verify.
```
