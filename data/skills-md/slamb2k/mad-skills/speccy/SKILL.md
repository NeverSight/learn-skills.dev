---
name: speccy
description: Deep-dive interview skill for creating comprehensive specifications. Reviews existing code and docs, then interviews the user through multiple rounds of targeted questions covering technical implementation, UI/UX, concerns, and tradeoffs. Produces a structured spec in specs/. Use when starting a new feature, system, or major change that needs a spec.
argument-hint: Goal, feature, or high-level description to specify
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, Skill
---

# Speccy - Interview-Driven Specification Builder

When this skill is invoked, IMMEDIATELY output the banner below before doing anything else.
Pick ONE tagline at random — vary your choice each time.
CRITICAL: Reproduce the banner EXACTLY character-for-character. The first line of the art has 4 leading spaces — you MUST preserve them.

```
{tagline}

⠀   ██╗███████╗██████╗ ███████╗ ██████╗ ██████╗██╗   ██╗
   ██╔╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝╚██╗ ██╔╝
  ██╔╝ ███████╗██████╔╝█████╗  ██║     ██║      ╚████╔╝
 ██╔╝  ╚════██║██╔═══╝ ██╔══╝  ██║     ██║       ╚██╔╝
██╔╝   ███████║██║     ███████╗╚██████╗╚██████╗   ██║
╚═╝    ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═════╝   ╚═╝
```

Taglines:
- 🔍 Tell me everything...
- 🧠 Let's think this through!
- 📋 Spec it before you wreck it!
- 🎤 Interview mode: ACTIVATED
- 💡 Great specs start with great questions!
- 🏗️ Measure twice, code once!
- 📝 No assumption left behind!
- 🎯 Precision engineering starts here!

---

## Output Formatting

After the banner, display parsed input:
```
┌─ Input ────────────────────────────────────────
│  {Field}:  {value}
│  Flags:    {parsed flags or "none"}
└────────────────────────────────────────────────
```

Pre-flight results:
```
── Pre-flight ───────────────────────────────────
  ✅ {dep}           {version or "found"}
  ⚠️ {dep}           not found → {fallback detail}
  ❌ {dep}           missing → stopping
──────────────────────────────────────────────────
```

Stage/phase headers: `━━ {N} · {Name} ━━━━━━━━━━━━━━━━━━━━━━━━━`

Status icons: ✅ done · ❌ failed · ⚠️ degraded · ⏳ working · ⏭️ skipped

---

Interview the user through multiple rounds of targeted questions to build
a comprehensive specification, then write it directly using the spec template
in `references/spec-template.md`.

Interview prompts and question guidelines: `references/interview-guide.md`
Spec template and writing guidelines: `references/spec-template.md`

## Pre-flight

Before starting, check all dependencies in this table:

| Dependency | Type | Check | Required | Resolution | Detail |
|-----------|------|-------|----------|------------|--------|
| prime | skill | `~/.claude/skills/prime/SKILL.md` or `~/.claude/plugins/marketplaces/slamb2k/skills/prime/SKILL.md` | no | fallback | Context loading; falls back to manual project scan |

For each row, in order:
1. Test file existence (check both paths for symlinked skills)
2. If found: continue silently
3. If missing: apply Resolution strategy
4. After all checks: proceed to context gathering

---

## Stage 1: Context Gathering

Before asking any questions, build a thorough understanding of the project:

1. **Capture GOAL** — the user's argument describing what needs to be specified
2. **Load project context** — invoke `/prime` to load domain-specific context
   (CLAUDE.md, specs, memory). If /prime is unavailable, fall back to
   the manual scan below.
3. **Scan the project** (skip items already loaded by /prime):
   - Read `CLAUDE.md` if present (project conventions, structure, domain)
   - Scan `specs/` directory for existing specifications
   - Scan existing design docs for context
   - Read relevant source code that relates to the GOAL
   - Check memory for prior decisions or open questions related to the GOAL
3. **Identify knowledge gaps** — what must you learn from the user to write
   a complete, unambiguous specification?

Group gaps into interview categories:
- **Architecture & Technical Design** — stack, patterns, data flow, integrations
- **Requirements & Scope** — what's in, what's out, must-haves vs nice-to-haves
- **UI & UX** — user flows, interaction patterns, accessibility, responsive
- **Security & Auth** — authentication, authorization, data protection
- **Infrastructure & Deployment** — hosting, CI/CD, environments, IaC
- **Data & Storage** — schemas, persistence, migrations, caching
- **Testing & Quality** — test strategy, coverage, acceptance criteria
- **Concerns & Tradeoffs** — known risks, alternatives considered, constraints

---

## Stage 2: Interview Rounds

Conduct multiple rounds of questions using `AskUserQuestion`. Continue until
all knowledge gaps are resolved.

### Question Rules

1. **4 questions per round maximum** (AskUserQuestion limit)
2. **Non-obvious questions only** — don't ask things you can determine from
   reading the code or docs. The user's time is valuable.
3. **Recommendations** — where you have an informed opinion based on the
   codebase, project conventions, or industry best practice, mark one option
   as recommended by listing it first and appending `(Recommended)` to its label.
   At least one question per round should have a recommendation where possible.
4. **Concise options** — 2-4 options per question, each with a clear
   description of implications and tradeoffs
5. **Progressive depth** — start with high-level architecture and scope,
   then drill into implementation details in later rounds
6. **Build on answers** — use previous round answers to inform next questions.
   Don't re-ask decided topics.
7. **Track decisions** — maintain a running list of all decisions made.
   Present this list at the start of each round so the user can see progress.

### Round Structure

Each round follows this pattern:

1. **Progress update** — brief summary of decisions made so far (after round 1)
2. **Category label** — which interview category this round covers
3. **Questions** — 3-4 targeted questions via AskUserQuestion
4. **Evaluate** — after answers, determine if more questions are needed

### Completion Criteria

Stop interviewing when ALL of the following are true:
- All identified knowledge gaps have been addressed
- No answer has raised new unresolved questions
- You have enough information to write every section of the spec template
- The user has confirmed scope boundaries (what's in and what's out)

When complete, briefly present a **Decision Summary** — a numbered list of
all decisions made across all rounds — and confirm with the user before
proceeding to spec generation.

---

## Stage 3: Generate Specification

Once the interview is complete and decisions are confirmed:

1. **Create `specs/` directory** if it doesn't exist:
   ```
   mkdir -p specs
   ```

2. **Read the spec template** from `references/spec-template.md`

3. **Generate the spec** by filling the template with:
   - The original GOAL as the introduction and purpose
   - All decisions from the interview rounds, mapped to the appropriate sections
   - Code/architecture context discovered in Stage 1
   - Acceptance criteria derived from requirements decisions
   - Test strategy aligned with the project's existing patterns

4. **Write the spec file** to `specs/{name}.md` where `{name}` is a
   kebab-case slug derived from the GOAL (e.g., `specs/user-auth.md`,
   `specs/payment-integration.md`). Use the Write tool directly.

5. The `specs/` directory is the standard location — `/build` and `/prime`
   both scan it automatically.

---

## Output & Handoff

After the spec is created, report to the user:

```
┌─ Speccy · Report ──────────────────────────────
│
│  ✅ Spec complete
│
│  📄 File:       {spec file path}
│  📋 Sections:   {count}
│  💬 Rounds:     {interview rounds conducted}
│  ❓ Questions:  {total questions asked}
│
│  📝 Key decisions
│     • {decision 1}
│     • {decision 2}
│     • {decision 3}
│
│  🔗 Links
│     Spec: {spec file path}
│
│  ⚡ Next steps
│     1. Review the spec: {path}
│     2. Run `/build {spec path}` to implement (reads the file automatically)
│
└─────────────────────────────────────────────────
```

Then **immediately** ask the user via AskUserQuestion:

   Question: "Spec written to {spec file path}. Ready to build?"
   Options:
   - "Build now (Recommended)" — invoke `/build` with the spec file
   - "Review first" — stop here so the user can review the spec before building
   - "Done" — stop here, no build

If the user selects **"Build now"**:
1. Invoke `/build` using the Skill tool:
   ```
   Skill(skill: "build", args: "{spec file path}")
   ```
2. `/build` will read the spec file via Plan Resolution and execute the full
   pipeline. **Do not** attempt to implement the spec yourself — always
   delegate to `/build`.

If the user selects **"Review first"** or **"Done"**, stop and display:
```
⚡ To build later, run: /build {spec file path}
```

**IMPORTANT:** After generating the spec, do NOT enter plan mode, do NOT
start implementing directly, and do NOT offer to execute the plan yourself.
The only path to implementation is through `/build`.
