---
name: create
allowed-tools: Read, Write, Edit, Bash(node:*), Bash(git:*), Bash(npm:*), Bash(ls:*), Bash(mkdir:*), Grep, Glob, TodoWrite, TodoRead, AskUserQuestion, Skill, Task
argument-hint: "[plugin-name] (optional - will prompt if not provided)"
description: "Create a new plugin for Claude Code marketplace with validation, ADR, and release automation. TRIGGERS - create plugin, new plugin, scaffold plugin, add plugin, plugin-dev create."
---

<!-- ⛔⛔⛔ MANDATORY: READ THIS ENTIRE FILE BEFORE ANY ACTION ⛔⛔⛔ -->

# ⛔ Create Plugin — STOP AND READ

**DO NOT ACT ON ASSUMPTIONS. Read this file first.**

This is a structured workflow command for creating a new plugin in a Claude Code marketplace.

Your FIRST and ONLY action right now: **Execute the TodoWrite below.**

## ⛔ MANDATORY FIRST ACTION: TodoWrite Initialization

**YOUR FIRST ACTION MUST BE the TodoWrite call below.**

DO NOT:

- ❌ Create any directories before TodoWrite
- ❌ Read marketplace.json before TodoWrite
- ❌ Ask questions before TodoWrite
- ❌ Jump to any phase without completing Step 0

### Step 0.1: Detect Marketplace Root

Before executing TodoWrite, verify you're in a marketplace directory:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Check for marketplace.json in cwd
if [ -f ".claude-plugin/marketplace.json" ]; then
  echo "✅ Marketplace detected: $(jq -r .name .claude-plugin/marketplace.json)"
else
  echo "❌ Not a marketplace directory. Run from a marketplace root."
  exit 1
fi
PREFLIGHT_EOF
```

### Step 0.2: Execute MANDATORY TodoWrite

**Execute TodoWrite NOW with this template:**

```
TodoWrite with todos:

- "[Plugin] Phase 0: Detect marketplace root" | in_progress
- "[Plugin] Phase 0: Interactive prompts (name, category, components)" | pending
- "[Plugin] Phase 0: Confirm plugin doesn't exist" | pending
- "[Plugin] Phase 1: Skill → plugin-structure (scaffold)" | pending
- "[Plugin] Phase 1: Create plugin directory + plugin.json" | pending
- "[Plugin] Phase 1: Skill → implement-plan-preflight (ADR)" | pending
- "[Plugin] Phase 2: Skill → skill-architecture (if has-skills)" | pending
- "[Plugin] Phase 2: Skill → hook-development (if has-hooks)" | pending
- "[Plugin] Phase 2: Skill → command-development (if has-commands)" | pending
- "[Plugin] Phase 2: Skill → agent-development (if has-agents)" | pending
- "[Plugin] Phase 2: Agent → skill-reviewer (if skills created)" | pending
- "[Plugin] Phase 3: Add to marketplace.json" | pending
- "[Plugin] Phase 3: Run validate-plugins.mjs" | pending
- "[Plugin] Phase 3: Skill → code-hardcode-audit" | pending
- "[Plugin] Phase 3: Agent → plugin-validator" | pending
- "[Plugin] Phase 4: Git commit (conventional format)" | pending
- "[Plugin] Phase 4: Push to remote" | pending
- "[Plugin] Phase 4: Skill → semantic-release" | pending
```

**After TodoWrite completes, proceed to Phase 0 section below.**

---

## Quick Reference

### Skills Invoked (Optimized Sequence)

| Order | Skill                    | Phase | Purpose                           | Invocation                              |
| ----- | ------------------------ | ----- | --------------------------------- | --------------------------------------- |
| 1     | plugin-structure         | 1     | Directory & manifest              | `Skill(plugin-dev:plugin-structure)`    |
| 2     | implement-plan-preflight | 1     | ADR + Design Spec + Diagrams      | `Skill(itp:implement-plan-preflight)`   |
| 3     | skill-architecture       | 2     | Create skills (if has-skills)     | `Skill(plugin-dev:skill-architecture)`  |
| 4     | hook-development         | 2     | Create hooks (if has-hooks)       | `Skill(plugin-dev:hook-development)`    |
| 5     | command-development      | 2     | Create commands (if has-commands) | `Skill(plugin-dev:command-development)` |
| 6     | agent-development        | 2     | Create agents (if has-agents)     | `Skill(plugin-dev:agent-development)`   |
| 7     | code-hardcode-audit      | 3     | Quality audit                     | `Skill(itp:code-hardcode-audit)`        |
| 8     | plugin-validator         | 3     | Silent failure audit              | `Skill(plugin-dev:plugin-validator)`    |
| 9     | semantic-release         | 4     | Version & publish                 | `Skill(itp:semantic-release)`           |

### Skills EXCLUDED (Redundant)

| Skill                        | Reason Excluded                                        |
| ---------------------------- | ------------------------------------------------------ |
| plugin-dev:skill-development | Use skill-architecture instead (3x more comprehensive) |
| plugin-dev:plugin-settings   | Merged into hook-development                           |
| itp:adr-graph-easy-architect | Invoked BY implement-plan-preflight (not separately)   |

### Agents Spawned

| Phase | Agent            | Purpose                  | Invocation                          |
| ----- | ---------------- | ------------------------ | ----------------------------------- |
| 2     | skill-reviewer   | Review skill quality     | `Task(plugin-dev:skill-reviewer)`   |
| 3     | plugin-validator | Validate final structure | `Task(plugin-dev:plugin-validator)` |

### File Locations

| Artifact         | Path                                    | Notes                      |
| ---------------- | --------------------------------------- | -------------------------- |
| Plugin Directory | `plugins/{name}/`                       | Main plugin folder         |
| Plugin Manifest  | `plugins/{name}/plugin.json`            | Required manifest          |
| Plugin README    | `plugins/{name}/README.md`              | Documentation              |
| Marketplace JSON | `.claude-plugin/marketplace.json`       | Must add plugin entry      |
| ADR              | `docs/adr/YYYY-MM-DD-{name}.md`         | Created by preflight skill |
| Design Spec      | `docs/design/YYYY-MM-DD-{name}/spec.md` | Created by preflight skill |

---

## Phase 0: Discovery & Validation

Detect marketplace root, gather plugin name/category/components via interactive prompts, confirm the plugin does not already exist.

**Detailed steps**: [Phase 0 Reference](./references/phase0-discovery.md)

### Phase 0 Gate

- [ ] Marketplace root detected (`.claude-plugin/marketplace.json` exists)
- [ ] Plugin name collected (kebab-case, no spaces)
- [ ] Category selected
- [ ] Components selected (skills/hooks/commands/agents)
- [ ] Plugin directory does NOT exist
- [ ] Plugin NOT in marketplace.json

---

## Phase 1: Scaffold Plugin

1. **Invoke `Skill(plugin-dev:plugin-structure)`** -- directory & manifest patterns
2. **Create plugin directory** with component subdirs based on user selections
3. **Generate `plugin.json`** using marketplace version
4. **Invoke `Skill(itp:implement-plan-preflight)`** -- creates ADR + Design Spec + diagrams

**Detailed steps**: [Phase 1 Reference](./references/phase1-scaffold.md)

### Phase 1 Gate

- [ ] Plugin directory exists: `plugins/$PLUGIN_NAME/`
- [ ] plugin.json created with marketplace version
- [ ] ADR exists: `docs/adr/$ADR_ID.md`
- [ ] Design spec exists: `docs/design/$ADR_ID/spec.md`
- [ ] Both diagrams in ADR (Before/After + Architecture)

---

## Phase 2: Component Creation (Conditional)

Execute ONLY the skills for components the user selected:

| Component | Skill Invocation                        | Then                                    |
| --------- | --------------------------------------- | --------------------------------------- |
| Skills    | `Skill(plugin-dev:skill-architecture)`  | Spawn `Task(plugin-dev:skill-reviewer)` |
| Hooks     | `Skill(plugin-dev:hook-development)`    | --                                      |
| Commands  | `Skill(plugin-dev:command-development)` | --                                      |
| Agents    | `Skill(plugin-dev:agent-development)`   | --                                      |

**Detailed steps**: [Phase 2 Reference](./references/phase2-components.md)

### Phase 2 Gate

- [ ] All selected components created
- [ ] If skills: skill-reviewer agent completed review
- [ ] Files follow plugin-dev patterns

---

## Phase 3: Registration & Validation

1. **Add plugin to `marketplace.json`** (include `hooks` field if hooks exist)
2. **Run `node scripts/validate-plugins.mjs`** -- expect all-pass
3. **Invoke `Skill(itp:code-hardcode-audit)`** -- quality audit
4. **Run silent failure audit** on all hook entry points
5. **Spawn `Task(plugin-dev:plugin-validator)`** -- structural validation

**Detailed steps**: [Phase 3 Reference](./references/phase3-validation.md)

### Phase 3 Gate

- [ ] Plugin added to marketplace.json
- [ ] validate-plugins.mjs passes
- [ ] code-hardcode-audit passes
- [ ] silent-failure-audit passes (no errors)
- [ ] plugin-validator agent approves

---

## Phase 4: Commit & Release

1. **Stage changes**: plugin dir, marketplace.json, ADR, design spec
2. **Conventional commit**: `feat($PLUGIN_NAME): add plugin for [brief description]`
3. **Push to remote**
4. **Invoke `Skill(itp:semantic-release)`** -- tag, changelog, GitHub release

**Detailed steps**: [Phase 4 Reference](./references/phase4-release.md)

### Phase 4 Success Criteria

- [ ] All changes committed with conventional commit
- [ ] Pushed to remote
- [ ] semantic-release completed
- [ ] New version tag created
- [ ] GitHub release published

---

## Troubleshooting

See [Troubleshooting Reference](./references/troubleshooting.md) for common issues and fixes.
