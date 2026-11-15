---
name: hooksmith
description: Use when the user asks for Instagram Reel hooks, TikTok or Shorts hooks, stronger openings, first-frame text, spoken intros, identity hooks, open loops, rehooks, retention paths, caption hooks, or an audit of the first 15-30 seconds of a short-form video. Builds, audits, rewrites, and stress-tests complete hook systems. Also handles `hooksmith init`, `hooksmith generate`, `hooksmith audit`, `hooksmith rewrite`, `hooksmith identity`, `hooksmith rehook`, and `hooksmith caption`.
argument-hint: "[init|generate|audit|rewrite|identity|rehook|caption] [topic, hook, or opening]"
user-invocable: true
version: 0.2.0
---

# Hooksmith

Hooksmith builds complete short-form hook systems. Do not stop at a clever first line. Build the spoken hook, on-screen text, open loop, rehook, visual anchor, and payoff path together.

## Setup Gate

Before non-trivial work, look for creator context:

1. Run or inspect `scripts/load-context.mjs` from this skill when available.
2. If `HOOKS.md` exists, use it as the creator source of truth.
3. If `HOOKS.md` is missing and the user invoked `init`, create it.
4. If `HOOKS.md` is missing and the request lacks niche, viewer, payoff, proof, or format, ask for the missing minimum context before writing hooks.

Minimum context:

- niche or topic
- target viewer
- viewer pain or desire
- intended payoff
- proof the creator can truthfully use
- format: talking head, demo, B-roll text Reel, carousel, caption-led Reel, TikTok, or Shorts

Never invent proof, numbers, client stories, timelines, follower counts, revenue, or virality claims.

## Commands

Route by first word when the user invokes a command.

| Command | Load | Job |
|---|---|---|
| `init` | none required | Gather context and write `HOOKS.md`. |
| `generate` | `references/command-generate.md` | Create 3-5 different hook systems. |
| `audit` | `references/command-audit.md` | Score and diagnose a hook or first 15-30 seconds. |
| `rewrite` | `references/command-rewrite.md` | Rebuild weak openings. |
| `identity` | `references/command-identity.md` | Create viewer-first identity-stack openings. |
| `rehook` | `references/command-rehook.md` | Add attention resets inside the first 3-10 seconds. |
| `caption` | `references/command-caption.md` | Create caption hooks and comment prompts. |

Always load `references/hook-frameworks.md` when writing new hook systems. Load `references/anti-patterns.md` before finalizing or grading.

When the set needs more variety or the user wants on-screen text options, also load `references/hook-families.md` and `references/text-hook-templates.md`.

Use `references/examples.md` only when the user needs examples, the request feels vague, or you need a pattern reset.

## Init Flow

For `init`, gather only what is missing. Explore existing project notes first if the workspace already has creator docs.

Ask for:

- creator niche
- target viewer
- viewer pain and desire
- what the creator can truthfully prove
- voice style
- content formats
- CTA style
- forbidden claims or words
- 1-3 examples of hooks they like, if available

Write `HOOKS.md` at the current project or content root. If the current directory is clearly not the creator workspace, ask where it should go.

Use this structure:

```markdown
# Hooksmith Context

## Creator
[name or handle if provided]

## Niche
[niche]

## Viewer
[specific viewer, situation, pain, desire]

## Proof Allowed
[truthful numbers, stories, examples, or "none yet"]

## Voice
[how the creator should sound]

## Formats
[talking head, demo, B-roll text Reel, carousel, TikTok, Shorts]

## CTA Rules
[comment prompts, DM prompts, save prompts, no CTA, etc.]

## Forbidden Claims
[claims, numbers, industries, results, or words to avoid]

## Winning Patterns
[optional hook examples and why they work]
```

After writing it, tell the user to run `hooksmith generate`, `hooksmith audit`, or `hooksmith identity`.

## Output Rules

For generation, return complete hook systems:

```markdown
## Option [N]: [short name]

Spoken hook:
[line]

On-screen text:
[text]

Hook job:
[self-identification / open loop / stakes / belief break / validation / authority / demo bridge]

Viewer:
[specific person this calls out]

Open loop:
[unresolved question]

Withheld answer:
[what stays hidden until later]

Rehook:
[attention reset inside 3-10 seconds]

Visual anchor:
[what changes on screen]

Value tease path:
- Beat 1: [partial value + next question]
- Beat 2: [partial value + next question]
- Beat 3: [payoff setup]

Payoff:
[where the loop closes]

Why it holds attention:
[one sentence]
```

For audits, use the 50-point rubric from `references/command-audit.md`.

## Quality Gate

Before finalizing, check:

- Does the first second make one specific viewer care?
- Is there unfinished business the viewer needs resolved?
- Do spoken hook and on-screen text do different jobs when both are used?
- Is there a rehook before attention drops?
- Does the hook avoid fake proof and fake urgency?
- Does the payoff justify the setup?
- Would the creator actually say this on camera?

If any answer is weak, rewrite before responding.
