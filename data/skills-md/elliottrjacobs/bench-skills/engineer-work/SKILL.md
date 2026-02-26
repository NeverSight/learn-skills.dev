---
name: engineer-work
description: Execute implementation plans with git branching, progress tracking, quality checks, and PR creation. Use when the user says "build this", "implement this", "start working", "execute the plan", or provides a plan file to execute.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task", "TodoWrite", "AskUserQuestion"]
argument-hint: "[plan-path]"
disable-model-invocation: true
---

# /engineer-work — Plan Execution

Execute implementation plans task-by-task with structured progress tracking, incremental commits, quality checks, and PR creation.

## When to Use

- User says "build this", "implement this", "start working"
- After completing `/engineer-plan` and ready to execute
- User provides a plan file to implement

## Process

### Step 1: Setup

**Locate the plan:** Use `$ARGUMENTS` as the plan path, or check `docs/plans/` for the most recent plan, or ask the user.

**Create a branch:**
```bash
git checkout -b feature/<plan-name>
```

**Initialize tracking:** Create a TodoWrite with all tasks from the plan. Mark Task 0 (setup) as in_progress.

### Step 2: Execute Tasks

Work through each task in dependency order.

**Per-task loop:**
1. Mark task `in_progress` in TodoWrite
2. Read the task — review acceptance criteria, key files
3. Implement — follow existing codebase patterns, keep changes minimal
4. Self-check — verify acceptance criteria are met
5. Commit — one commit per logical unit of work
6. Mark task `completed` in TodoWrite

**Implementation rules:**
- Follow existing patterns (don't introduce new conventions)
- Keep changes minimal — implement what the task says, nothing more
- Run `npx tsc --noEmit` after significant changes
- Fix lint errors as you go
- If stuck, check `docs/solutions/` for relevant past solutions
- If a task reveals a plan problem, note it and adapt

**Commit format:**
```
type(scope): description
```
Types: `feat`, `fix`, `refactor`, `chore`, `test`, `docs`
- Imperative mood: "add" not "added"
- Under 72 characters
- One commit per task (split large tasks into multiple)

### Step 3: Quality Checks

After all tasks complete, detect the tech stack and run appropriate checks.

**Always run:**
```bash
npx tsc --noEmit          # TypeScript type check
npm run lint              # or project-specific lint command
```

**Stack-adaptive checks** (detect from config files):
- Next.js (`next.config.*`): `npm run build` to catch build errors
- Expo (`app.json`): `npx expo lint`
- Tests: `npm test` if test scripts exist

**Fix any issues found**, commit as `fix: address lint/type issues`, and re-run checks.

### Step 4: Create PR

```bash
gh pr create --title "[type]: [feature name]" --body "$(cat <<'EOF'
## Summary
- [Primary change]
- [Secondary change]

## Plan Reference
[Link to docs/plans/ file]

## Testing
- [ ] Type check passes
- [ ] Lint passes
- [ ] [Feature-specific verification]
EOF
)"
```

### Step 5: Handoff

Use AskUserQuestion:
- "PR is ready. What's next?" (header: "Next step")
  - "Run a full review (`/engineer-review`)" — Comprehensive code review
  - "Document learnings (`/knowledge-compound`)" — Capture patterns
  - "Done" — Close out

## Output

- Feature branch with incremental commits
- Pull request on GitHub

## Next Steps

- Want a thorough review? → `/engineer-review`
- Security check needed? → `/security-audit`
- Capture what you learned? → `/knowledge-compound`
