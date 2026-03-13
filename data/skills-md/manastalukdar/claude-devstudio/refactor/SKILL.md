---
name: refactor
description: Structured code restructuring preserving functionality with continuous validation
disable-model-invocation: false
---

# Intelligent Refactoring Engine

I'll help you restructure your code systematically - preserving functionality while improving structure, readability, and maintainability.

Arguments: `$ARGUMENTS` - files, directories, or refactoring scope

**Token Optimization:**
- ✅ Session-based state tracking (already implemented)
- ✅ Progressive refactoring (plan → implement → validate → test)
- ✅ Glob-before-Read for target file discovery
- ✅ Incremental refactoring (one change at a time with validation)
- ✅ Early exit on resumed sessions (skip completed changes) - saves 70%
- ✅ Caching project patterns and test commands
- ✅ Git diff to detect what changed (verify refactoring scope)
- **Expected tokens:** 1,500-4,000 (vs. 3,000-6,500 unoptimized) - **50-60% reduction**
- **Optimization status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)

## Token Optimization Strategy

This skill implements comprehensive token optimization achieving **60% reduction** (4,000-6,000 → 1,500-2,500 tokens):

### 1. Focused Refactoring Scope (30% savings)

**Problem:** Reading entire codebase for refactoring wastes 1,500-2,000 tokens
**Solution:** Target specific files/functions with focused analysis

```bash
# ✅ EFFICIENT - Target specific scope (500-800 tokens)
/refactor src/services/UserService.ts
/refactor src/components/Button.tsx --extract-method
/refactor src/utils/validation.ts --simplify

# ⚠️ LESS EFFICIENT - Broad scope (2,000-3,000 tokens)
/refactor src/
/refactor .
```

**Implementation:**
- Parse arguments for specific file paths
- Use `--focus=function_name` to target specific functions
- Grep for code smell patterns before reading files
- Only analyze files matching refactoring criteria

### 2. Grep-Before-Read Pattern (25% savings)

**Problem:** Reading all files to find refactoring candidates wastes tokens
**Solution:** Use Grep to identify code smells, then read only problematic files

```bash
# ✅ Find long functions (code smell)
Grep "function.*{" --output_mode=content -A 50 | head -20

# ✅ Find duplicated code patterns
Grep "duplicate_pattern" --output_mode=files_with_matches

# ✅ Find complex conditionals
Grep "if.*&&.*||" --output_mode=content --glob="*.ts"

# Then read ONLY files with identified smells
Read src/services/ComplexService.ts
```

**Common Code Smell Patterns:**
- Long functions: `function.*{` with high line count
- Deep nesting: Multiple levels of `if.*{.*if.*{`
- Large classes: `class.*{` with high method count
- Duplicated code: Repeated string literals or logic blocks
- Magic numbers: Numeric literals in business logic
- God objects: Classes with too many responsibilities

### 3. Template-Based Refactoring Patterns (20% savings)

**Problem:** Explaining every refactoring technique wastes tokens
**Solution:** Use cached refactoring templates and patterns

**Cached Patterns in `.claude/cache/refactor/patterns.json`:**
```json
{
  "extract_method": {
    "pattern": "Move code block to new method",
    "validation": "Verify same inputs/outputs",
    "test_strategy": "Unit test new method"
  },
  "extract_class": {
    "pattern": "Move related methods to new class",
    "validation": "Verify object encapsulation",
    "test_strategy": "Test class interface"
  },
  "simplify_conditional": {
    "pattern": "Replace complex if/else with guard clauses",
    "validation": "Verify same logic paths",
    "test_strategy": "Branch coverage testing"
  },
  "remove_duplication": {
    "pattern": "Extract common code to utility",
    "validation": "Verify all callsites updated",
    "test_strategy": "Integration testing"
  }
}
```

**Usage:**
- Load pattern template from cache
- Apply to target code
- Skip detailed explanations
- Reference pattern name only

### 4. Git Checkpoint for Safe Rollback (15% savings)

**Problem:** Verbose safety explanations and manual checkpoint creation
**Solution:** Automated git checkpoint with concise reporting

```bash
# ✅ EFFICIENT - Single checkpoint command
git stash push -u -m "refactor: checkpoint before UserService refactoring"

# Report: "Checkpoint created: abc123"
```

**Implementation:**
- Create stash checkpoint at session start
- Store stash reference in `refactor/state.json`
- Skip detailed explanations of git safety
- Provide rollback command only if needed

### 5. Progressive Refactoring (One Smell at a Time) (25% savings)

**Problem:** Attempting multiple refactorings simultaneously increases complexity
**Solution:** Refactor one code smell at a time with validation

```markdown
# ✅ EFFICIENT - Sequential approach

## Refactoring Plan
1. ✅ Extract long methods (Session 1) - COMPLETE
2. 🔄 Simplify conditionals (Session 2) - IN PROGRESS
3. ⏳ Remove duplication (Session 3) - PENDING
4. ⏳ Improve naming (Session 4) - PENDING

Current focus: Simplify conditionals in UserService.ts
```

**Benefits:**
- Smaller validation scope per session
- Early exit if already complete
- Focused analysis and testing
- Clear progress tracking

### 6. Session State for Multi-Step Refactoring (40% savings)

**Problem:** Re-analyzing entire codebase on session resume
**Solution:** Store analysis results and completed work in session state

**Session State Structure (`refactor/state.json`):**
```json
{
  "session_id": "refactor_20260127_1430",
  "scope": "src/services/UserService.ts",
  "code_smells": [
    {
      "type": "long_method",
      "location": "UserService.authenticate:45-120",
      "severity": "high",
      "status": "pending"
    },
    {
      "type": "duplicated_code",
      "locations": ["UserService.ts:89-95", "AdminService.ts:112-118"],
      "severity": "medium",
      "status": "completed"
    }
  ],
  "completed_refactorings": [
    {
      "type": "extract_method",
      "file": "src/services/UserService.ts",
      "method": "validateCredentials",
      "tests_passing": true,
      "timestamp": "2026-01-27T14:45:00Z"
    }
  ],
  "validation_results": {
    "tests_passing": true,
    "build_status": "success",
    "type_check": "clean"
  },
  "checkpoint_ref": "stash@{0}"
}
```

**Resume Optimization:**
```bash
# On resume, read state.json (500 tokens)
# Skip completed refactorings
# Continue from last pending item
# Early exit if all complete

# Savings: 70% on resumed sessions (2,500 → 750 tokens)
```

### 7. Refactoring-Specific Optimizations

#### A. Focus Area Flags (20% savings)
```bash
# Specific refactoring types
/refactor --extract-method    # Only find long methods
/refactor --simplify          # Only find complex logic
/refactor --remove-duplication # Only find duplicates
/refactor --rename            # Only find naming issues

# Skip irrelevant analysis
```

#### B. Incremental Validation (15% savings)
```bash
# ✅ Fast validation after each change
npm test -- --testPathPattern=UserService.test
# Only run affected tests (not full suite)

# Store results in state.json
# Skip validation if cached and unchanged
```

#### C. Git Diff Analysis (25% savings)
```bash
# ✅ See exactly what changed during refactoring
git diff --stat
git diff src/services/UserService.ts

# Verify refactoring scope matches plan
# Detect unintended changes
# Skip reading unchanged files
```

### 8. Bash-Based Operations (30% savings)

**Problem:** Using Read/Write for every operation
**Solution:** Prefer Bash commands for file operations

```bash
# ✅ EFFICIENT - Bash operations
git mv src/old/Service.ts src/new/Service.ts
grep -r "OldService" src/ | wc -l  # Count references
find src/ -name "*.test.ts" -exec npm test {} \;

# ❌ INEFFICIENT - Multiple Read/Write cycles
# Read each file, Edit, Write back
```

### 9. Complete Token Optimization Flow

**New Session (1,500-2,000 tokens):**
```
1. Check for existing session (100 tokens)
   - LS refactor/ || Create new session

2. Focused analysis (600-800 tokens)
   - Grep for code smells in target scope
   - Read only files with identified issues
   - Load cached refactoring patterns

3. Create refactoring plan (400-600 tokens)
   - Write refactor/plan.md
   - Write refactor/state.json
   - Create git checkpoint

4. Execute first refactoring (400-600 tokens)
   - Apply template-based pattern
   - Quick validation (affected tests only)
   - Update state.json
```

**Resumed Session (500-750 tokens):**
```
1. Load session state (200 tokens)
   - Read refactor/state.json
   - Skip completed work (70% savings)

2. Continue from checkpoint (300-400 tokens)
   - Apply next pending refactoring
   - Incremental validation
   - Update state

3. Early exit if complete (50 tokens)
   - All smells addressed
   - Final validation cached
```

### 10. Expected Token Savings

| Operation | Before | After | Savings |
|-----------|--------|-------|---------|
| New session (full project) | 4,000-6,000 | 1,500-2,000 | 60-70% |
| New session (focused file) | 2,500-3,500 | 800-1,200 | 65-70% |
| Resume session | 2,500-3,000 | 500-750 | 70-75% |
| Validation only | 1,500-2,000 | 400-600 | 70% |
| Complete refactoring | 1,000-1,500 | 300-500 | 70% |

**Overall Average: 60% reduction** (4,000-6,000 → 1,500-2,500 tokens)

### 11. Best Practices for Token Efficiency

**For Users:**
```bash
# ✅ Be specific with scope
/refactor src/services/UserService.ts --extract-method

# ✅ Use focused flags
/refactor --simplify src/utils/validation.ts

# ✅ Resume sessions efficiently
/refactor resume

# ✅ Validate incrementally
/refactor validate UserService.ts
```

**For Implementation:**
1. Always check session state first (early exit opportunity)
2. Grep before Read for code smell detection
3. Load cached patterns instead of explaining techniques
4. Use git diff to verify scope and detect changes
5. Validate only affected tests, not full suite
6. Store all analysis results in state.json
7. Prefer Bash for file operations
8. Focus on one smell type at a time
9. Create checkpoint once, reference by ID
10. Update state incrementally after each refactoring

**Caching Behavior:**
- Session location: `refactor/` (plan.md, state.json)
- Cache location: `.claude/cache/refactor/`
- Caches: Refactoring patterns, test commands, validation results
- Cache validity: Until session completed
- Shared with: `/implement`, `/complexity-reduce`, `/test` skills

**Usage:**
- `refactor path/to/file.ts` - Refactor specific file (2,000-3,500 tokens)
- `refactor resume` - Resume session (500-1,500 tokens, skips completed work)
- `refactor --extract-method` - Specific refactoring type (1,500-2,500 tokens)

**KEY FEATURE: Built-in validation and refinement after EVERY change ensures nothing breaks and no code is left behind. The AI will automatically fix its own mistakes during the refactoring process.**

**SESSION FILES LOCATION: Always use refactor/ folder in current directory**

## Session Intelligence

I'll maintain refactoring continuity across sessions:

**Session Files (in current project):**
- `refactor/plan.md` - Refactoring plan with progress tracking  
- `refactor/state.json` - Current state and completed actions

**IMPORTANT:** The `refactor` folder is created in your CURRENT PROJECT directory. Use `refactor/` to access it.

**Auto-Detection:**
- If session exists: Resume from last checkpoint
- If no session: Create new refactoring plan
- Commands: `resume`, `continue`, `status`, `new`

**EXAMPLE OF CORRECT PATH USAGE:**
```
# CORRECT - looks in current project:
Read refactor/state.json
LS refactor

# WRONG - these will fail:
Read ../../../refactor/state.json
Read $HOME/.claude/refactor/state.json
```

## Phase 1: Initial Setup & Analysis

### Extended Thinking for Complex Refactoring

For complex refactoring scenarios, I'll use extended thinking to develop comprehensive strategies:

<think>
When faced with complex architectural refactoring:
- Multi-step transformation paths that preserve functionality
- Risk mitigation strategies for each transformation
- Dependency graph analysis and update ordering
- Performance implications of different approaches
- Backwards compatibility requirements
- Testing strategies for validating each step
</think>

**Triggers for Extended Analysis:**
- Large-scale architectural changes
- Complex dependency untangling
- Performance-critical refactoring
- Legacy system modernization

**MANDATORY FIRST STEPS FOR SESSION CHECK:**
```
Step 1: Check for refactor directory in CURRENT directory
Command: LS refactor

Step 2: If refactor exists, read session files:
Command: Read refactor/state.json
Command: Read refactor/plan.md

DO NOT USE THESE WRONG PATHS:
- ../../../refactor/  (WRONG - goes up directories)
- $HOME/refactor/  (WRONG - home directory)
- ~/refactor/  (WRONG - home directory)

ONLY USE: refactor/ (current directory)
```

**CRITICAL:** The refactor folder is created in the CURRENT WORKING DIRECTORY where user is running the command. NOT in home, NOT in parent directories.

I'll examine your codebase to identify improvement opportunities:

**Analysis Focus:**
- Code complexity hotspots using **Grep** patterns
- Duplication detection across files
- Architecture inconsistencies
- Test coverage for safe refactoring
- Performance bottlenecks

**Smart Scoping:**
- If specific files provided: Focused analysis
- If directory provided: Recursive analysis
- If no arguments: Strategic project-wide scan

## Phase 2: Refactoring Planning

Based on analysis, I'll create a structured plan:

**Refactoring Categories:**
- **Quick Wins**: Variable renames, method extractions
- **Structural**: Pattern applications, dependency improvements
- **Architectural**: Major reorganizations, module boundaries
- **Performance**: Algorithm optimizations, caching strategies

**Plan Structure:**
I'll create a detailed plan in `refactor/plan.md`:

```markdown
# Refactor Plan - [timestamp]

## Initial State Analysis
- **Current Architecture**: [description of existing patterns]
- **Problem Areas**: [specific issues found]
- **Dependencies**: [external/internal dependencies]
- **Test Coverage**: [current coverage %]

## Refactoring Tasks
[Prioritized list with risk levels]

## Validation Checklist
- [ ] All old patterns removed
- [ ] No broken imports
- [ ] All tests passing
- [ ] Build successful
- [ ] Type checking clean
- [ ] No orphaned code
- [ ] Documentation updated

## De-Para Mapping
| Before | After | Status |
|--------|-------|--------|
| OldService.method() | NewService.method() | Pending |
| /api/v1/* | /api/v2/* | Pending |
```

## Phase 3: Incremental Execution

I'll apply refactorings systematically:

**Execution Order:**
1. Create git checkpoint for safety
2. Apply low-risk improvements first
3. Validate after each change
4. Progress to higher-impact refactorings
5. Update plan with completion status

**Continuous Validation & Refinement:**
After EVERY refactoring change:
1. **Immediate Testing:**
   - Run unit tests for modified files
   - Execute integration tests if applicable
   - Verify no test regressions
   
2. **Deep Comparison:**
   - Compare function outputs before/after
   - Validate API contracts maintained
   - Check for missing edge cases
   - Verify error handling preserved
   
3. **Automated Fixes:**
   - Update broken imports automatically
   - Fix reference errors
   - Adjust type definitions
   - Resolve linting issues
   
4. **Quality Gates:**
   - STOP if tests fail - fix immediately
   - STOP if behavior changes - investigate
   - STOP if performance degrades - optimize
   - Only proceed when 100% validated

5. **Continuous Refinement:**
   - Re-scan for missed patterns
   - Update all related files
   - Clean up orphaned code
   - Document breaking changes

## Phase 4: Pattern Application

I'll apply consistent patterns throughout:

**Pattern Recognition:**
- Identify existing patterns in your code
- Detect anti-patterns to eliminate
- Apply design patterns where beneficial
- Maintain architectural consistency

**Code Improvements:**
- Extract duplicated code into utilities
- Simplify complex functions
- Improve naming for clarity
- Reduce coupling between modules

## Phase 5: Quality Metrics

I'll track refactoring impact:

**Measurable Improvements:**
- Complexity reduction percentages
- Duplication elimination count
- Test coverage maintenance
- Performance benchmarks
- Code readability scores

## Context Continuity

**Session Management:**
When you return and run `/refactor` or `/refactor resume`:
- I'll load existing plan and state
- Display progress summary
- Continue from last checkpoint
- Maintain all refactoring decisions

**Progress Example:**
```
RESUMING REFACTORING SESSION
├── Session: refactor_2025_08_02_1430
├── Progress: 12 of 20 tasks complete
├── Last Action: Extract UserService methods
└── Next: Simplify PaymentProcessor logic

Continuing from checkpoint...
```

## Practical Examples

**Start Refactoring:**
```
/refactor                    # Analyze entire project
/refactor src/components/    # Focus on specific directory
/refactor UserService.ts     # Target single file
```

**Session Control:**
```
/refactor resume    # Continue existing session
/refactor status    # Check progress without continuing
/refactor new       # Start fresh (archives existing)
/refactor validate  # Validate completeness and find loose ends
```

**Deep Validation & Enhancement Commands:**
```
/refactor finish    # Complete with full validation & behavior comparison
/refactor enhance   # Deep analysis comparing original vs refactored
/refactor verify    # Run original code, capture behavior, compare with new
/refactor complete  # Ensure 100% migration with behavior preservation
```

## Phase 6: Automatic Final Validation & Refinement

**AUTOMATIC EXECUTION:** This phase runs automatically after all refactorings are complete. You can also trigger it manually with `/refactor validate`.

**Final Validation Process:**

**Deep Validation Analysis:**
1. **Coverage Check** - Find all remaining old patterns
2. **Import Verification** - Detect broken or orphaned imports
3. **Build & Test** - Run full build and test suite
4. **Type Checking** - Verify type safety if applicable
5. **Dead Code Detection** - Identify removable legacy code

**De-Para Mapping:**
```
MIGRATION STATUS REPORT
├── Patterns Migrated: 45/48 (94%)
├── Files Updated: 67/70
├── Tests Status: 3 failing
└── Build Status: Passing

PENDING MIGRATIONS:
- src/legacy/UserHelper.js → Still using old pattern
- api/v1/routes.js → Mixed patterns detected
- tests/old-api.test.js → Needs update

SUGGESTED REFINEMENTS:
1. Remove 12 orphaned files
2. Consolidate duplicate utilities
3. Update 3 missed import paths
4. Optimize bundle size (-15KB possible)
```

**Validation Actions:**
- Generate comprehensive de-para documentation
- Create migration guide for team
- Fix remaining issues automatically
- Ensure 100% pattern consistency

## Deep Validation Commands (All-in-One Process)

**ALL these commands (`finish`, `enhance`, `verify`, `complete`) execute the SAME comprehensive validation process:**

### Complete Validation & Enhancement Process
When you run ANY of these: `/refactor finish`, `/refactor enhance`, `/refactor verify`, or `/refactor complete`

**I will AUTOMATICALLY execute ALL these steps:**

1. **Deep Original Code Analysis**
   - Analyze EVERY function, method and class in detail
   - Document ALL behaviors, patterns and logic flows
   - Map complete code structure and dependencies
   - Create comprehensive understanding in `refactor/original-analysis.md`

2. **Complete Migration**
   - Apply ALL remaining refactorings
   - Find and fix ALL instances of old patterns
   - Update ALL imports and references
   - Clean up ALL orphaned code

3. **Deep Code-to-Code Comparison**
   - Analyze refactored code line by line
   - Verify EVERY behavior is preserved
   - Check ALL logic paths match original
   - Ensure error handling is identical

4. **Comprehensive Analysis**
   - Line-by-line code comparison
   - Complexity metrics (before/after)
   - Performance benchmarks
   - Memory usage analysis
   - Test coverage verification

5. **Automatic Fixes**
   - Fix ANY behavioral discrepancies
   - Update broken references
   - Resolve type issues
   - Correct import paths

6. **Final Validation**
   - Run full test suite
   - Execute integration tests
   - Verify build passes
   - Ensure 100% behavior preservation

7. **Complete Report**
   - De-para mapping of ALL changes
   - Migration guide for team
   - Risk assessment
   - Rollback instructions if needed

**The result:** 100% guarantee that NOTHING was broken, NOTHING was left behind, and the application behaves EXACTLY the same as before refactoring.

## Safety Guarantees

**Protection Measures:**
- Git checkpoints before changes
- Incremental commits at logical points
- Test validation after each step
- Clear rollback strategy

**Important:** I will NEVER:
- Add AI attribution or signatures
- Modify git configuration
- Break working functionality
- Make changes without validation
- Use emojis in commits, PRs, or git-related content

## Skill Integration

When appropriate, I may suggest using other skills:
- `/test` - After major refactoring to verify functionality
- `/commit` - At logical checkpoints in the refactoring process

## Execution Guarantee

**My workflow ALWAYS follows this order:**

1. **Setup session** - Check/create state files FIRST
2. **Deep analysis** - Use extended thinking for complex scenarios
3. **Write plan** - Document all changes in `refactor/plan.md`
4. **Get confirmation** - Show plan summary before starting
5. **Execute incrementally** - Follow plan with checkpoints
6. **Validate completeness** - Run validation phase when requested

**I will NEVER:**
- Start refactoring without a written plan
- Make changes before complete analysis
- Skip session file creation
- Proceed without showing the plan first

I'll ensure perfect continuity between sessions, always resuming exactly where we left off with full context and decision history.