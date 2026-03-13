---
name: mobile-compaction
description: Context compaction strategies for large Android codebases. Optimize token usage while preserving critical context.
---

# Mobile Compaction Skill

Strategic context compaction for large Android projects to optimize token usage while preserving critical information.

## When to Compact

Compact context when:
- Token usage exceeds 100,000
- Working on large refactors spanning many files
- Switching between unrelated features
- Session becomes unfocused
- Context contains resolved discussions

## Compaction Strategies

### 1. Module-Level Compaction

Focus on a single Android module:

```bash
/compact --module=feature:auth
```

**What happens:**
- Retain: All files in feature:auth module
- Summarize: Other modules to high-level description
- Drop: Resolved discussions about other modules

**Use when**: Deep work on a specific feature

### 2. Layer-Based Compaction

Focus on architecture layer:

```bash
/compact --layer=ui
/compact --layer=data
/compact --layer=domain
```

**What happens:**

| Layer | Retain | Summarize |
|-------|--------|-----------|
| UI | Composables, ViewModels, navigation | Repository details, data models |
| Data | Repositories, data sources, models | Compose code, UI state |
| Domain | Use cases, domain models | Implementation details |

**Use when**: Working on cross-cutting concerns in a layer

### 3. Build Variant Focus

Narrow to specific build variant:

```bash
/compact --variant=debug
```

**What happens:**
- Retain: Debug-specific configurations, test code
- Summarize: Release configurations, ProGuard rules

**Use when**: Debugging or test development

### 4. Test Isolation

Compact around failing tests:

```bash
/compact --test=AuthViewModelTest
/compact --test-failing
```

**What happens:**
- Retain: Test file, related source files
- Summarize: Unrelated test discussions
- Drop: Resolved test fix discussions

**Use when**: Fixing specific test failures

### 5. Pattern-Based Compaction

Compact based on architectural patterns:

```bash
/compact --pattern=compose
/compact --pattern=mvi
/compact --pattern=koin
```

**What happens:**
- Retain: Files matching the pattern
- Summarize: Non-matching files to pattern names only

**Use when**: Pattern-specific work (e.g., Compose optimization)

## Compaction Levels

| Level | Retention | Token Savings | Use Case |
|-------|-----------|---------------|----------|
| **Lite** | Current task only | 70-80% | Deep focus work |
| **Medium** | Current + related | 50-60% | Feature development |
| **Standard** | Project summary | 30-40% | Default compaction |
| **Minimal** | Essential only | 80-90% | Context at limit |

## What Gets Preserved

### Always Preserve (Critical)
- Active task context (what we're doing now)
- Recent code changes (last 5-10 files)
- Current errors/failures
- Mobile memory context
- High-confidence instincts (>0.7)
- Unresolved questions

### Usually Preserve (Important)
- Architecture decisions
- Recent discussions (last 50 messages)
- Related file contents
- Test states

### Summarize (Compressible)
- Completed features
- Resolved bugs
- Working code explanations
- Background discussions

### Drop (Disposable)
- Successful build outputs
- Trivial operations
- Duplicated information
- Off-topic discussions

## Compaction Commands

### Basic Compaction

```bash
/compact                      # Auto-select strategy
/compact --level=medium       # Specify level
/compact --focus=compose      # Focus on specific area
```

### Smart Compaction

```bash
/compact --smart              # AI chooses strategy
/compact --adaptive           # Adjusts based on usage
```

### Manual Compaction

```bash
/compact --keep=file1.kt,file2.kt   # Keep specific files
/compact --drop=discussion-1        # Drop specific discussion
/compact --summarize=feature-x      # Summarize specific topic
```

## Compaction Workflow

### Before Compaction

```bash
1. /memory-save all              # Save current state to memory
2. /mobile-checkpoint save pre-compact  # Optional checkpoint
3. /compact --strategy=module --focus=feature:auth
```

### After Compaction

```bash
1. /memory-summary              # Verify memory preserved
2. /instinct-status             # Verify instincts preserved
3. Continue work...
```

## Integration

### With Checkpoints

```bash
# Pre-compact hook automatically saves checkpoint
# Restore to recover if compaction removes needed context
```

### With Memory

```bash
# Memory survives compaction
# Query memory to recover details:
/memory-query "What was the auth flow architecture?"
```

### With Instincts

```bash
# Instincts survive compaction
# High-confidence instincts always retained
# Low-confidence may be summarized
```

## Anti-Patterns

### Don't Compact When:
- In the middle of debugging
- Unresolved errors exist
- Active discussion ongoing
- Task almost complete

### Do Compact When:
- Starting new task
- Switching context
- Token limit approaching
- Task completed, keeping summary

## Recovery

If compaction removed needed context:

```bash
1. /memory-query <topic>        # Query memory
2. /mobile-checkpoint list      # Check for checkpoints
3. /mobile-checkpoint restore <name>  # Restore if needed
4. Git history for file diffs
```

## Examples

### Example 1: Feature Development
```
Context: Working on auth feature, context contains old home feature discussions
Action: /compact --module=feature:auth
Result: Retains auth files, summarizes home feature
```

### Example 2: Test Fixing
```
Context: Many files, focus on fixing LoginTest
Action: /compact --test=LoginTest
Result: Retains LoginTest, related auth files, summarizes rest
```

### Example 3: Compose Optimization
```
Context: Large project, optimizing Compose performance
Action: /compact --pattern=compose --level=medium
Result: Retains Compose files, summaries of data/network layers
```

---

**Remember**: Compaction is reversible via checkpoints and memory. When in doubt, checkpoint first.
