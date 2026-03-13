---
name: openspec-beads-implement
description: Integrates OpenSpec and Beads during implementation. Works on Beads issues and updates OpenSpec tasks automatically. Activates when user wants to implement a change using beads as tracker.
---

# OpenSpec + Beads Implementation Skill

This skill integrates both systems during implementation: uses Beads for work tracking and updates OpenSpec automatically.

## When to Activate

- User runs `openspec apply <change>` AND beads is initialized
- User says "implement this with beads", "work on <change>"
- User asks how to work with both systems

## Main Flow

### 1. Select Change

```bash
openspec status --change "<name>" --json
```

Same as openspec-apply-change.

### 2. Link with Beads

```bash
bd list --labels "spec:<change>" --json
```

**If no issues exist**:

- Run openspec-to-beads first: `Skill: openspec-to-beads`
- Or warn user that there are no beads for this change

### 3. Implementation Loop

For each OpenSpec task:

1. **Find equivalent bead**
   - Search by title containing the task text
   - Use label `spec:<change>` to filter

2. **Update status in Beads**

   ```bash
   bd update <bead-id> --status in_progress
   ```

3. **Implement** the change

4. **Close bead**

   ```bash
   bd close <bead-id> --reason "Completed: <task-text>"
   ```

5. **Update OpenSpec**
   - In tasks.md: `- [ ]` → `- [x]`

### 4. Show Progress

```
## Implementing: <change>

Beads: <in_progress>/<total> | OpenSpec: <complete>/<total>
```

## Key Commands

### Search Issues by Spec

```bash
bd list --labels "spec:<change>" --json
```

### View Issue Details

```bash
bd show <id> --json
```

### Update Status

```bash
bd update <id> --status in_progress
bd update <id> --status open
```

### Close Issue

```bash
bd close <id> --reason "Completed: <desc>"
```

## Common Errors

**No beads for this change:**

```
⚠️  No beads found with label spec:<change>
Run first: Skill openspec-to-beads
```

**Beads not initialized:**

```
⚠️  Beads is not initialized
Run: bd init --prefix <project>
```

**Issue blocked:**

```
⚠️  Issue <id> is blocked by: <blocking-id>
Use: bd show <id> for details
```

## Synchronization

When all tasks are complete:

- Beads issues should be "closed"
- OpenSpec tasks.md should have `- [x]` in all

Recommend to user:

```bash
bd sync  # Sync beads with git
```

## Integration with Other Skills

- **openspec-to-beads**: Creates beads from specs (pre-implementation)
- **openspec-apply-change**: Flow without beads (fallback)
- **openspec-archive-change**: Archive completed change

## Output Example

```
## Implementing: add-auth

Beads: 2/5 | OpenSpec: 2/5

▶ Working on: bead-123 "add-auth: Implement login API"
✓ Completed

▶ Working on: bead-124 "add-auth: Create Login component"
✓ Completed

3 tasks remaining...
```
