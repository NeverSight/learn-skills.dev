---
name: distill-to-skill
description: >-
  Distill knowledge from any source — blog posts, articles, documentation, GitHub repos,
  video transcripts, books, papers — into a well-structured agent skill. Use when the user
  shares a URL, article, repo, or body of knowledge and wants it turned into a reusable skill.
  Triggers on: "make a skill from this", "distill this into a skill", "create a skill from
  this article", "turn this repo into a skill", "extract patterns from", "convert to a skill".
  This skill complements the `skill-creator` skill — skill-creator handles the mechanics
  (frontmatter, packaging, init scripts), this skill handles the distillation process.
---

# Distill to Skill

Turn any source of knowledge into a well-structured agent skill. This is the process
skill — it covers how to extract, filter, restructure, and encode knowledge. For the
mechanical aspects of skill creation (directory structure, frontmatter format, validation,
packaging), use the `skill-creator` skill.

## The Distillation Mindset

A skill is not a summary. It's a **decision-making tool** for an agent working on a task.

When distilling, constantly ask:
- "Would an agent mid-task benefit from knowing this?" → Keep it
- "Is this background context or motivation?" → Cut it
- "Is this specific to one language/framework but the idea is universal?" → Translate it
- "Could an agent figure this out on its own?" → Cut it
- "Does this change how the agent would write code or make decisions?" → Keep it

The goal: an agent loads this skill and immediately writes better code or makes better
decisions, without having read the original source.

## Workflow

### Step 1: Absorb the Source

Read the full source material thoroughly. For repos, explore the architecture, key files,
and patterns. For articles, read end to end. Don't skim — the best insights are often
buried in asides, footnotes, and "by the way" paragraphs.

**For articles/blog posts:**
- Fetch the URL and read the full content
- Note the core thesis (usually 1-2 sentences)
- Identify the actionable rules vs the explanatory prose
- Note any concrete code examples or patterns

**For repos:**
- Explore directory structure, entry points, key modules
- Read the core implementation files (not the tests or config)
- Identify the design patterns, not the specific implementation
- Note the TypeScript/type tricks, architectural decisions, and utility patterns
- Look at what's deliberately *absent* — that's often the most interesting insight

**For multiple sources on a theme:**
- Find the common thread across sources
- Note where sources agree (high-confidence patterns)
- Note where they diverge (context-dependent decisions)

### Step 2: Extract the Transferable Core

Separate the essence from the packaging:

| Keep | Cut |
|---|---|
| Universal principles | Author's personal journey |
| Concrete patterns with code | Motivational framing |
| Decision rules ("when X, do Y") | Background on why the field exists |
| Anti-patterns and pitfalls | Comparisons to other approaches |
| Copy-paste utilities | Historical context |
| Checklists | "Further reading" recommendations |

**The litmus test:** If you removed the original source from existence, would this
skill still be useful on its own? If yes, you've extracted the core correctly.

### Step 3: Decide the Skill Shape

**Single concept, self-contained → SKILL.md only (no references)**

Use when the idea can be fully expressed in ~100-250 lines. The concept is
cohesive enough that splitting it would lose the thread.

Examples from today's work:
- `parse-dont-validate` — One core idea (parse > validate) with practical rules
- `karpathy-guidelines` — A set of behavioral rules
- `agents-md` — How to write one specific file type

**Broad topic with depth → SKILL.md + references/**

Use when there are multiple distinct sub-topics that an agent might need
independently. SKILL.md carries the principles and quick-reference; references
carry the deep dives.

Examples:
- `lean-ts-patterns` — 7 principles in SKILL.md, 5 reference files by domain
- `agent-first-repo` — 3 pillars in SKILL.md, 3 reference files for each pillar

**Multiple independent ideas → Split into separate skills**

If the source contains 2+ concepts that would trigger in different contexts,
make separate skills. They can cross-reference each other.

Example: The OpenAI harness engineering article → split into `agents-md` (how to
write the file) + `agent-first-repo` (broader repo structure) because they trigger
in different contexts.

**Decision heuristic:**
```
Does this source contain one core idea?
  YES → Single SKILL.md
  NO → Are the ideas used together?
    YES → SKILL.md + references/
    NO → Separate skills that cross-reference
```

### Step 4: Translate to the User's Ecosystem

The source may be in Haskell, Rust, Go, or plain English. The skill should use
the user's preferred language and ecosystem.

- **Code examples:** Rewrite in the target language (typically TypeScript/Bun)
- **Library references:** Map to the target ecosystem's equivalents
- **Idioms:** Use the target language's patterns (e.g., branded types instead of newtypes)
- **Keep it runnable:** Code in the skill should be copy-pasteable and work

If the original insight is language-agnostic, use the target language for examples
but keep the prose universal.

### Step 5: Structure the Skill

Follow this template for SKILL.md:

```markdown
---
name: skill-name
description: >-
  [What this enables]. [When to use it — specific scenarios].
  Triggers on: [concrete trigger phrases].
---

# Title

[1-2 line summary. Source attribution if from a specific article/repo.]

## [Core Concept / Principles]

[The distilled rules. Concise. Imperative voice. Code examples inline.]

## [Practical Patterns / Copy-Paste Code]

[Things the agent can use immediately. Concrete, not abstract.]

## [Anti-Patterns / What to Avoid]

[Common mistakes. What NOT to do is often more valuable than what to do.]

## [Checklist / Code Review Guide]

[Verification points. Things to check when reviewing code.]
```

**For reference files**, each should:
- Start with a 1-2 line summary of what it covers
- Be self-contained — readable without SKILL.md for context
- Include the relevant companion skill name-drops (not full content)
- Stay under ~300 lines

### Step 6: Write the Description (Most Important Line)

The YAML `description` field is the **only thing** that determines whether the skill
triggers. It's loaded into context permanently. Write it carefully:

- Start with what the skill enables (not what it is)
- List specific scenarios and file types
- Include concrete trigger phrases the user might say
- Keep it to 3-5 lines of YAML

Bad: `"Patterns from a blog post about types."`
Good: `"Type-driven design: transform unstructured data into precise types at
system boundaries. Use when writing input validation, designing data types, or
reviewing code with redundant null checks. Triggers on: 'parse don't validate',
'make illegal states unrepresentable', 'input validation'."`

### Step 7: Validate

Before finishing, check:

- [ ] Could an agent use this skill without reading the original source?
- [ ] Is every section actionable (rules, patterns, code) not explanatory (history, motivation)?
- [ ] Are code examples in the user's preferred language and copy-pasteable?
- [ ] Is SKILL.md under ~300 lines? (Move depth to references/ if over)
- [ ] Does the description include concrete trigger phrases?
- [ ] Is there a checklist or code review guide for verification?
- [ ] Are companion skills referenced by name (not duplicated)?
- [ ] Would removing any section make the skill less useful? If not, cut it.

## Distillation Patterns

### The Inversion

Many articles explain bottom-up: problem → exploration → solution.
Skills should be top-down: **rule → example → anti-pattern**.

The agent doesn't need to be convinced. It needs to know what to do.

### The Translation

Academic/theoretical sources often use abstract examples. Translate to concrete,
real-world scenarios in the user's domain:

- "NonEmpty list" → `[T, ...T[]]` tuple type in TypeScript
- "Sum types" → discriminated unions with `kind` field
- "Smart constructor" → branded type with parse function
- "Monad" → async pipeline / Result type

### The Compression

A 5,000-word article typically distills to ~150-250 lines of skill. The compression
ratio is roughly 10:1 to 20:1. If your skill is approaching the same length as the
source, you're summarizing, not distilling.

### The Cross-Reference

When distilling a source that touches on ideas already captured in other skills,
don't re-explain — reference. Write 2-3 sentences of context for how the idea
applies here, then point to the companion skill for depth.

```markdown
Parse data at system boundaries into precise types — don't let raw/untyped data
flow deep into business logic. For the full treatment of branded types, smart
constructors, and the shotgun parsing anti-pattern, see the `parse-dont-validate` skill.
```

## Source-Specific Tips

**Blog posts:** Usually one core idea with 60% motivation, 30% examples, 10% actionable rules. Extract the 10%, expand it with your own examples.

**GitHub repos:** The code IS the content. Focus on architectural patterns, utility functions worth copying, TypeScript tricks, and what's deliberately absent. Ignore CI config, test infrastructure, and build tooling unless that's the point.

**Documentation:** Already structured, but optimized for lookup, not for decision-making. Restructure around "when to use X" rather than "what X does."

**Papers:** High insight density but buried in formalism. Extract the key theorem/insight, translate to practical code patterns, drop the proofs.

**Video transcripts:** Extremely low density. Scan for the 2-3 key moments where the speaker says something prescriptive, ignore the rest.

For concrete before/after examples of distillation, see
[references/examples.md](references/examples.md).
