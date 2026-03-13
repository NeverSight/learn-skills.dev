---
name: implement
description: Import and adapt code from any source to your project with validation and testing
disable-model-invocation: false
---

# Smart Implementation Engine

I'll intelligently implement features from any source - adapting them perfectly to your project's architecture while maintaining your code patterns and standards.

Arguments: `$ARGUMENTS` - URLs, paths, or descriptions of what to implement

## Token Optimization Strategy

**Target: 60% reduction (4,000-6,000 → 1,500-2,500 tokens)**

### Core Optimization Patterns

**1. Focused Scope (40% savings)**
- Implement ONE specific feature at a time
- Reject vague requests ("add auth system" → ask which auth component)
- Use `--feature=X` flag to constrain scope
- Skip related but non-essential features
- Example: Implement login form only, not entire auth flow

**2. Architecture Context from Cache (30% savings)**
- Load project patterns from `.claude/cache/understand/`
- Reuse dependency analysis from cached `/understand` results
- Skip architecture discovery if cache exists and is recent
- Share technology stack detection with `/scaffold`
- Only re-analyze if source requires new dependencies

**3. Template-Based Implementation (20% savings)**
- Match common patterns (React component, Express route, database model)
- Apply project-specific templates from cache
- Generate code from patterns instead of reading examples
- Use framework conventions (Next.js page structure, Django views)

**4. Progressive Implementation (MVP first) (25% savings)**
- Implement minimal viable feature first (core functionality only)
- Skip: edge cases, error handling, validation (add in iteration 2)
- Validate MVP works before enhancement
- Use `--mvp` flag for fastest implementation
- Example: Basic form submit before validation/error states

**5. Git Diff for Context (50% savings)**
- Use `git diff main...HEAD` to see recent changes
- Understand existing patterns from recent work
- Skip reading files if git diff shows relevant code
- Leverage commit messages for implementation context

**6. Session State for Multi-Step (80% savings on resume)**
- Track implementation progress in `implement/state.json`
- Resume sessions skip completed phases entirely
- Cache source analysis, don't re-fetch URLs
- Store dependency decisions, reuse in subsequent steps

**7. WebFetch for External Sources (90% savings)**
- WebFetch fetches URL content outside Claude context
- Only small prompt + response counted in tokens
- Analyze GitHub/GitLab repos without reading in Claude
- Cache fetched content for entire session

**8. Incremental File Updates (40% savings)**
- Edit existing files with surgical changes
- Never re-read entire file if only updating one function
- Use Grep to locate exact integration points
- Write minimal diff-style changes

### Optimization Workflow

**Initial Implementation (2,000-2,500 tokens):**
```bash
# 1. Check session state (50 tokens)
Read implement/state.json OR create new session

# 2. Quick scope validation (100 tokens)
If args are vague → ask for specific feature/file

# 3. Load architecture cache (200 tokens)
Read .claude/cache/understand/project-summary.json
Read .claude/cache/understand/dependencies.json

# 4. Source analysis (500-1,000 tokens)
If URL → WebFetch (external, ~50 tokens)
If local path → Glob pattern → Read only target files
Cache source analysis in implement/source-analysis.md

# 5. Template matching (300 tokens)
Match source to known patterns (component, route, model, etc.)
Apply project-specific templates from cache
Generate implementation plan from template

# 6. MVP implementation (800-1,200 tokens)
Implement core feature only
Skip: validation, error handling, edge cases
Use Edit for targeted file changes
Update implement/state.json with progress

# 7. Validation checkpoint (200 tokens)
Run tests if they exist
Document next iteration in state
```

**Session Resume (500-800 tokens):**
```bash
# 1. Load state (50 tokens)
Read implement/state.json
Check completed phases

# 2. Skip completed work (0 tokens)
If source analyzed → skip
If MVP implemented → skip to enhancement

# 3. Continue from checkpoint (450-750 tokens)
Load cached decisions
Apply next iteration (validation, error handling)
Update state with new progress
```

**Enhancement Iteration (1,000-1,500 tokens):**
```bash
# 1. Load MVP context (100 tokens)
Read implement/state.json
Git diff to see MVP changes

# 2. Add robustness (600-1,000 tokens)
Error handling, validation, edge cases
Based on MVP implementation patterns
Use Edit for targeted enhancements

# 3. Testing & validation (300-400 tokens)
Run test suite
Update documentation
Mark implementation complete
```

### Token Budget by Operation

| Operation | Unoptimized | Optimized | Savings |
|-----------|-------------|-----------|---------|
| **New Implementation** | 4,000-6,000 | 1,500-2,500 | 60-62% |
| Initial source analysis | 1,500 | 500 | 67% |
| Project architecture | 1,000 | 200 | 80% |
| Code generation | 1,500 | 800 | 47% |
| **Session Resume** | 2,000-3,000 | 500-800 | 73-75% |
| State loading | 500 | 50 | 90% |
| Skip completed phases | 1,500 | 0 | 100% |
| Continue work | 1,000 | 450-750 | 25-55% |
| **URL Implementation** | 3,000-5,000 | 1,200-2,000 | 60% |
| WebFetch source | 2,000 | 50 | 97% |
| Analysis + implement | 1,000-3,000 | 1,150-1,950 | 15-35% |
| **Enhancement Phase** | 2,000-3,000 | 1,000-1,500 | 50% |
| Context loading | 800 | 100 | 87% |
| Implementation | 1,200-2,200 | 900-1,400 | 25-36% |

### Caching Strategy

**Session Files (local project):**
- `implement/state.json` - Current phase, completed steps, cached decisions
- `implement/plan.md` - Implementation plan with progress tracking
- `implement/source-analysis.md` - Analyzed source requirements (cached)

**Shared Cache Files (`.claude/cache/`):**
- `understand/project-summary.json` - Architecture patterns, tech stack
- `understand/dependencies.json` - Installed packages and versions
- `understand/code-patterns.json` - Project-specific conventions
- `scaffold/templates/` - Framework-specific templates

**Cache Validity:**
- Session cache: Valid until implementation complete or files change
- Shared cache: Valid until dependencies/structure changes
- Source analysis: Valid for entire session (never re-fetch URLs)

### Optimization Commands

**Explicit Optimization Flags:**
```bash
/implement --feature=login-form https://...  # Focused scope
/implement --mvp https://...                 # MVP only, skip edge cases
/implement resume                            # Auto-resume with cached state
/implement --use-cache                       # Force use cached architecture
```

**Expected Token Usage:**
- `implement [new source]` - 1,500-2,500 tokens (focused implementation)
- `implement resume` - 500-800 tokens (skip completed work)
- `implement --mvp [source]` - 1,200-1,800 tokens (minimal feature)
- `implement finish` - 1,000-1,500 tokens (enhancement phase)

**Optimization Status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)
**Average Reduction:** 60% (4,000-6,000 → 1,500-2,500 tokens)

## Session Intelligence

I'll check for existing implementation sessions to continue seamlessly:

**Session Files (in current project directory):**
- `implement/plan.md` - Current implementation plan and progress
- `implement/state.json` - Session state and checkpoints

**IMPORTANT:** Session files are stored in a `implement` folder in your current project root, NOT in home directory or parent folders. If a session exists, I'll resume from the exact checkpoint. Otherwise, I'll create a new implementation plan and track progress throughout.

## Phase 1: Initial Setup & Analysis

**MANDATORY FIRST STEPS:**
1. Check if `implement` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `implement/state.json`
   - Look for `implement/plan.md`
   - If found, resume from existing session
3. If no directory or session exists:
   - Create `implement/plan.md`
   - Initialize `implement/state.json`
4. Complete full analysis BEFORE any implementation

**Critical:** Use `implement` folder in current directory. Do NOT use `$HOME/implement` or any parent directory paths

I'll examine what you've provided and your project structure:

**Source Detection:**
- Web URLs (GitHub, GitLab, CodePen, JSFiddle, documentation sites)
- Local paths (files, folders, existing code)
- Implementation plans (.md files with checklists)
- Feature descriptions for research

**Project Understanding:**
- Architecture patterns using **Glob** and **Read**
- Existing dependencies and their versions
- Code conventions and established patterns
- Testing approach and quality standards

## Phase 2: Strategic Planning

Based on my analysis, I'll create an implementation plan:

**Plan Creation:**
- Map source features to your architecture
- Identify dependency compatibility
- Design integration approach
- Break work into testable chunks

I'll write this plan to `implement/plan.md`:

```markdown
# Implementation Plan - [timestamp]

## Source Analysis
- **Source Type**: [URL/Local/Description]
- **Core Features**: [identified features to implement]
- **Dependencies**: [required libraries/frameworks]
- **Complexity**: [estimated effort]

## Target Integration
- **Integration Points**: [where it connects]
- **Affected Files**: [files to modify/create]
- **Pattern Matching**: [how to adapt to project style]

## Implementation Tasks
[Prioritized checklist with progress tracking]

## Validation Checklist
- [ ] All features implemented
- [ ] Tests written and passing
- [ ] No broken functionality
- [ ] Documentation updated
- [ ] Integration points verified
- [ ] Performance acceptable

## Risk Mitigation
- **Potential Issues**: [identified risks]
- **Rollback Strategy**: [git checkpoints]
```

## Phase 3: Intelligent Adaptation

I'll transform the source to fit your project perfectly:

**Dependency Resolution:**
- Map source libraries to your existing ones
- Reuse your utilities instead of adding duplicates
- Convert patterns to match your codebase
- Update deprecated approaches to modern standards

**Code Transformation:**
- Match your naming conventions
- Follow your error handling patterns
- Maintain your state management approach
- Preserve your testing style

**Repository Analysis Strategy:**
For large repositories, I'll use smart sampling:
- Core functionality first (main features, critical paths)
- Supporting code as needed
- Skip generated files, test data, documentation
- Focus on actual implementation code

## Phase 4: Implementation Execution

I'll implement features incrementally:

**Execution Process:**
1. Implement core functionality
2. Add supporting utilities
3. Integrate with existing code
4. Update tests to cover new features
5. Validate everything works correctly

**Progress Tracking:**
- Update `implement/plan.md` as I complete each item
- Mark checkpoints in `implement/state.json`
- Create meaningful git commits at logical points

## Phase 5: Quality Assurance

I'll ensure the implementation meets your standards:

**Validation Steps:**
- Run your existing lint commands
- Execute test suite
- Check for type errors
- Verify integration points
- Confirm no regressions

## Deep Validation Process (All-in-One)

**ALL validation commands (`finish`, `verify`, `complete`, `enhance`) execute the SAME comprehensive process:**

When you run ANY of these: `/implement finish`, `/implement verify`, `/implement complete`, or `/implement enhance`

**I will AUTOMATICALLY:**

1. **Deep Original Source Analysis**
   - Thoroughly analyze EVERY aspect of original code/requirements
   - Study ALL implementation patterns and architectures
   - Document COMPLETE functionality and business logic
   - Map entire code structure and dependencies
   - Create comprehensive analysis in `implement/source-analysis.md`

2. **Requirements Verification**
   - Compare current implementation with original
   - Map each original feature to new implementation
   - Identify any missing features or behaviors
   - Check edge cases from original code

3. **Comprehensive Testing**
   - Write tests for ALL new code
   - Run existing test suite
   - Create integration tests
   - Test error scenarios
   - Verify performance requirements

4. **Deep Code Analysis**
   - Check for incomplete TODOs
   - Find hardcoded values to configure
   - Verify error handling completeness
   - Analyze security implications
   - Check accessibility requirements

5. **Automatic Refinement**
   - Fix any failing tests
   - Complete partial implementations
   - Add missing error handling
   - Optimize performance bottlenecks
   - Improve code documentation

6. **Integration Analysis**
   - Analyze integration points thoroughly
   - Verify API contracts match original
   - Check database schema compatibility
   - Validate UI/UX flows match requirements
   - Ensure backward compatibility maintained

7. **Completeness Report**
   - Feature coverage: X/Y implemented
   - Test coverage percentage
   - Performance benchmarks
   - Security audit results
   - Remaining work (if any)

**The result:** 100% complete, tested, and production-ready implementation that matches ALL requirements.

## Context Continuity

**Session Resume:**
When you return and run `/implement` or `/implement resume`:
- I'll load the existing plan and state
- Show progress summary
- Continue from the last checkpoint
- Maintain all previous decisions and context

**Smart Detection:**
- Auto-resume if session files exist
- Start fresh with `/implement new [source]`
- Check status with `/implement status`

## Practical Examples

**Single Source:**
```
/implement https://github.com/user/feature
/implement ./legacy-code/auth-system/
/implement "payment processing like Stripe"
```

**Multiple Sources:**
```
/implement https://github.com/projectA ./local-examples/
```

**Resume Session:**
```
/implement              # Auto-detects and resumes
/implement resume       # Explicit resume
/implement status       # Check progress
/implement validate     # Validate integration completeness
```

**Deep Validation Commands:**
```
/implement finish       # Complete with exhaustive testing & validation
/implement verify       # Deep verification against requirements
/implement complete     # Ensure 100% feature completeness
/implement enhance      # Refine and optimize implementation
```

## Execution Guarantee

**My workflow ALWAYS follows this order:**

1. **Setup session** - Create/load state files FIRST
2. **Analyze source & target** - Complete understanding
3. **Write plan** - Full implementation plan in `implement/plan.md`
4. **Show plan** - Present summary before implementing
5. **Execute systematically** - Follow plan with updates
6. **Validate integration** - Run validation when requested

**I will NEVER:**
- Start implementing without a written plan
- Skip source or project analysis
- Bypass session file creation
- Begin coding before showing the plan
- Use emojis in commits, PRs, or git-related content

## Phase 6: Implementation Validation

When you run `/implement validate` after implementation:

**Integration Analysis:**
1. **Coverage Check** - Verify all planned features implemented
2. **Integration Points** - Validate all connections work
3. **Test Coverage** - Ensure new code is tested
4. **TODO Scan** - Find any leftover TODOs
5. **Documentation** - Check if docs reflect changes

**Validation Report:**
```
IMPLEMENTATION VALIDATION
├── Features Implemented: 12/12 (100%)
├── Integration Points: 8/10 (2 pending)
├── Test Coverage: 87%
├── Build Status: Passing
└── Documentation: Needs update

PENDING ITEMS:
- API endpoint /users/profile not connected
- WebSocket integration incomplete
- Missing tests for error scenarios
- README needs feature documentation

ENHANCEMENT OPPORTUNITIES:
1. Add error boundary for new components
2. Implement caching for API calls
3. Add performance monitoring
4. Create usage examples
```

**Validation Actions:**
- Complete missing integrations
- Generate comprehensive test suite
- Update all affected documentation
- Create migration guide if breaking changes

## Skill Suggestions

After implementation milestones, I may suggest:
- `/test` - To verify the implementation works correctly
- `/commit` - To save progress at logical checkpoints

I'll maintain perfect continuity across sessions, always picking up exactly where we left off with full context preservation.