---
name: vibecoding-refactor
description: Vibe Coding Engineering Refactoring Methodology. Systematically refactor AI-generated code through architecture-layer and module-layer deep analysis, discovering duplicate implementations, unused resources, inconsistent patterns, and other typical problems. Supports persistent task management for incremental execution. Use when asked to refactor code, clean up patches, improve code quality, analyze architecture, or optimize codebase.
---

# Vibe Coding Engineering Refactoring Methodology

A complete methodology for systematically refactoring AI-generated code, supporting task splitting, persistence, and incremental execution for large refactoring projects.

---

## ⚠️ Core Principle: Deep Analysis First

**Deep analysis phases must be completed before starting any refactoring tasks.**

Typical Vibe Coding problems require deep analysis to discover:
- Duplicate implementations (same functionality implemented in multiple places, unaware of each other)
- Unused component libraries (existing library but not used, reinventing the wheel)
- Inconsistent patterns (API calls, error handling, state management vary across modules)
- Mixed abstraction levels (business logic mixed with UI)

**Skipping analysis to start refactoring directly is not allowed.**

---

## ⚡ Quick Recovery Entry (New Agent Must Read)

**When user says "continue refactoring" or `.refactor/` directory exists, execute the following recovery flow:**

```
Step 1: Read status summary
   → Read .refactor/README.md (contains overall status and context)

Step 2: Read master plan
   → Read .refactor/tasks/master-plan.md (task tree and progress)

Step 3: Read active tasks
   → List and read task files in .refactor/tasks/active/

Step 4: Read recent logs (optional, if need to understand last interruption point)
   → Read latest session log in .refactor/logs/

Step 5: Report status to user
   → Use template below to report, confirm direction to continue
```

**Report Template:**
```markdown
## Refactoring Status Recovery

### Overall Progress
- Project: {project_name}
- Total Progress: {X}%
- Current Phase: Phase {N} - {phase_name}

### Current Tasks
- 🔄 {task-xxx}: {task_name} ({completion}%)
  - Last progress: {what step was last completed}
  - Next step: {what to do next}

### Pending
- ⏳ {task-yyy}: {task_name}

### Blocked (if any)
- 🚫 {task-zzz}: {reason}

---
Continue with {task-xxx}? Or other arrangements?
```

---

## Constitutional Principles

### Bottom Line Principles (Absolutely Non-Violable)

1. **Functionality Unchanged**: All functionality must remain exactly the same as before refactoring
2. **UI Unchanged**: Visual appearance and interaction behavior remain unchanged
3. **API Compatible**: External interfaces remain compatible
4. **Rollbackable**: Each change can be independently rolled back
5. **Traceable**: All operations are recorded

### Quality Standards

Code after refactoring should achieve:
- Unified patterns (one functionality has only one implementation)
- Clear responsibilities (each module has single responsibility)
- Reasonable dependencies (no circular dependencies, clear hierarchy)
- Type safety (no any, complete error handling)

---

## Workflow (Six Phases)

```
Phase 0         Phase 1          Phase 2            Phase 3            Phase 4          Phase 5
Partition   →   Key Identify  →  Architecture   →   Module Layer   →   Execute      →   Finalize
    │              │              Analysis            Analysis          Refactor         Verify
    │              │                 │                   │                 │               │
Domain         Core Feature      Layer Check       Per-module Deep    Execute by      Verify
Division       List              Dependency        Analysis           Layer           Compare
Boundary       High-freq Code    Direction         Vibe Problem       Arch First      Cleanup
Identify       Key Path          Circular Dep      Detection          Then Module     Archive
Resource                         Evaluate          Generate Report    Update Progress Document
Inventory
```

**Refactoring executes in two layers:**
1. **Architecture Layer**: Dependencies, directory structure, layering standards (global problems)
2. **Module Layer**: Vibe Coding problems for each key feature (local problems)

---

## Phase 0: Project Partition (Required)

**Goal**: Establish macro understanding, inventory reusable resources

### 0.1 Directory Structure Scan

```bash
# Generate directory tree
tree -L 3 -d -I "node_modules|target|dist|.git"

# Count code lines per directory
fd -e ts -e tsx -e rs | xargs wc -l | sort -rn | head -30
```

### 0.2 Domain Division

Identify main domains and boundaries:

```
Project Domain Division
├── Frontend Domain
│   ├── Component Library (components/ui/)
│   ├── Business Components (features/, modules/)
│   ├── Infrastructure (infrastructure/, lib/)
│   └── Shared Layer (shared/, common/)
│
├── Backend Domain
│   ├── Core Library (core/, domain/)
│   ├── API Layer (api/, handlers/)
│   └── Application Layer (app/, cmd/)
│
└── Common Domain
    ├── Type Definitions
    └── Configuration Files
```

### 0.3 Resource Inventory (Critical!)

**Must thoroughly inventory all reusable resources and infrastructure in the project.**

Inventory uses **heuristic approach**, not limited to categories below. Discover all reusable resources based on actual project:

#### UI Layer Resources
| Resource Type | Search Method | Inventory Content |
|---------------|---------------|-------------------|
| Component Library | Search components/ui/, components/common/ | List all exported components and their Props |
| Icon Library | Search icons/, Icon components | List all icons |
| Style System | Search styles/, theme/, variables | CSS variables, theme config |

#### Utility Layer Resources
| Resource Type | Search Method | Inventory Content |
|---------------|---------------|-------------------|
| Utility Functions | Search utils/, helpers/, lib/ | List all exported functions |
| Custom Hooks | Search hooks/, use*.ts | List all hooks and purposes |
| Type Definitions | Search types/, *.d.ts | List core business types |

#### Service Layer Resources
| Resource Type | Search Method | Inventory Content |
|---------------|---------------|-------------------|
| API Services | Search services/, api/ | List all service classes and methods |
| State Management | Search store/, *Store* | List all stores and states |

#### Infrastructure (Often Overlooked!)
| Resource Type | Search Method | Inventory Content |
|---------------|---------------|-------------------|
| Logging System | Search logger, log, console wrapper | Logging tools and usage |
| Event System | Search EventEmitter, eventBus, on/emit | Event bus and event list |
| Internationalization | Search i18n, locale, t(), useTranslation | Translation functions and language packs |
| Theme System | Search theme, ThemeProvider, useTheme | Theme switching mechanism |
| Error Handling | Search ErrorBoundary, error handler | Unified error handling |
| Configuration | Search config, settings, env | Configuration reading method |
| Permission System | Search permission, auth, role | Permission check mechanism |
| Cache System | Search cache, storage, localStorage wrapper | Caching tools |
| Router System | Search router, route, navigate | Route config and navigation |
| Request Interceptor | Search interceptor, middleware | Request/response interception |

#### Heuristic Discovery

Beyond above categories, also search for project-specific infrastructure:

```bash
# Search singleton pattern (usually infrastructure)
rg "getInstance|\.instance|static instance" --type ts

# Search Provider pattern
rg "Provider|Context" --type tsx

# Search exported classes and factory functions
rg "^export class|^export function create" --type ts

# Search shared/, common/, core/ directories
fd -t d "shared|common|core|infrastructure"
```

**Output Format**:

```markdown
## Resource Inventory

### UI Layer
| Resource | Location | Exports |
|----------|----------|---------|
| Component Library | components/ui/ | Button, Card, Modal... |
| Icons | icons/ | IconXxx... |

### Utility Layer
| Resource | Location | Exports |
|----------|----------|---------|
| Date Utils | shared/utils/date | formatDate, parseDate... |
| Hooks | hooks/ | useXxx... |

### Infrastructure
| Resource | Location | Usage | Description |
|----------|----------|-------|-------------|
| Logger | infrastructure/logger | logger.info() | Unified logging |
| Event Bus | infrastructure/events | eventBus.emit() | Cross-component communication |
| i18n | locales/ + useI18n | t('key') | Multi-language |
| Theme | theme/ + useTheme | theme.colors.xxx | Theme switching |
```

**⚠️ These resources will be used in module-layer analysis to check reuse. The more thorough the inventory, the more accurate the subsequent analysis.**

### 0.4 Output

Create `.refactor/analysis/project-partition.md`

---

## Phase 1: Key Identification (Required)

**Goal**: Identify core features and modules that need deep analysis

### 1.1 Core Feature List

List the project's core features (will be deeply analyzed one by one later):

```markdown
## Core Feature List

### Feature 1: [Feature Name]
- User Story: User can...
- Entry Point: [file path:line number]
- Involved Modules: [module list]
- Complexity: High/Medium/Low

### Feature 2: [Feature Name]
...
```

### 1.2 High-Frequency Code Identification

```bash
# Most referenced modules
rg "^import|^from" --type ts | grep -oP "from ['\"].*?['\"]" | sort | uniq -c | sort -rn | head -30
```

### 1.3 Key Path Tracing

Trace complete call chain for each core feature, preparing for subsequent module-layer analysis.

### 1.4 Output

Create `.refactor/analysis/key-identification.md`

---

## Phase 2: Architecture Layer Analysis (Required)

**Goal**: Discover global architecture problems

**Architecture problems are module-independent and need to be resolved first.**

### 2.1 Layering Structure Check

Check if correct layering dependencies are followed:

```
Correct dependency direction (can only depend downward):
┌─────────────────┐
│   UI Layer      │  Components, Pages
├─────────────────┤
│   Application   │  State Management, Business Services
├─────────────────┤
│ Infrastructure  │  API, Storage, Utilities
├─────────────────┤
│   Core Layer    │  Type Definitions, Constants
└─────────────────┘
```

**Check Violations**:

```bash
# Core layer should not depend on upper layers
rg "from ['\"].*(components|services|store)" core/ types/

# Infrastructure should not depend on UI
rg "from ['\"].*components" infrastructure/

# Component library should not depend on business code
rg "from ['\"].*(features|modules)" components/ui/
```

### 2.2 Circular Dependency Detection

```bash
# Check if circular dependencies exist between modules
# A -> B and B -> A
```

### 2.3 Directory Structure Evaluation

- Is directory responsibility clear?
- Are there misplaced files?
- Are module boundaries clear?

### 2.4 Output: Architecture Layer Refactoring Report

Create `.refactor/analysis/architecture-report.md`:

```markdown
# Architecture Layer Analysis Report

## Layering Violations
| Violation Location | Wrong Dependency | Severity | Fix Suggestion |
|--------------------|------------------|----------|----------------|
| core/utils.ts:15 | import from components/ | High | Remove dependency or adjust location |

## Circular Dependencies
| Module A | Module B | Files Involved | Fix Suggestion |
|----------|----------|----------------|----------------|
| moduleA | moduleB | a.ts, b.ts | Extract common part |

## Directory Structure Issues
| Issue | Location | Suggestion |
|-------|----------|------------|
| Unclear responsibility | features/utils/ | Move to shared/utils/ |

## Architecture Layer Refactoring Tasks
1. [A-001] Resolve core -> components violation
2. [A-002] Resolve moduleA <-> moduleB circular dependency
3. [A-003] Adjust features/utils/ location
```

---

## Phase 3: Module Layer Analysis (Core!)

**Goal**: Deep analysis of each key feature, discovering Vibe Coding problems

**⚠️ This is the most important phase, must go deep into implementation details of each module**

### 3.1 Analysis Method

**For each key feature identified in Phase 1, perform the following analysis:**

```markdown
## Feature Analysis: [Feature Name]

### Basic Information
- Entry: [file:line]
- Files Involved: [file list]
- Call Chain: [complete call path]

### Vibe Coding Problem Detection

#### 1. Duplicate Implementation Detection
- Is there same/similar functionality implemented elsewhere?
- Check method: Search similar function names, similar logic

#### 2. Resource Reuse Detection (Compare with Phase 0 inventory)
- Using component library components? Or self-made?
- Using utility function library? Or self-written?
- Using public types? Or self-defined?
- Using public services? Or direct API calls?

#### 3. Pattern Consistency Detection
- Is API call pattern consistent with other modules?
- Is error handling unified?
- Is state management unified?

#### 4. Code Quality Detection
- Excessive any types?
- Unhandled errors?
- Hardcoded values?

### Problem Summary
| Problem | Location | Severity | Fix Suggestion |
|---------|----------|----------|----------------|
| ... | ... | ... | ... |

### Refactoring Suggestions
1. ...
2. ...
```

### 3.2 Detection Checklist

Must check for each module:

```markdown
## Module Layer Checklist

### Resource Reuse (Compare with Phase 0 inventory)
- [ ] Components: Using component-library? Self-made which?
- [ ] Utility Functions: Using shared/utils? Self-written which?
- [ ] Types: Using shared/types? Self-defined which?
- [ ] Services: Using public services? Direct API calls which?
- [ ] Hooks: Using public hooks? Self-written which?

### Infrastructure Usage (Compare with Phase 0 infrastructure inventory)
- [ ] Logging: Using logger? Or console.log?
- [ ] i18n: Using t()? Or hardcoded text?
- [ ] Theme: Using theme variables? Or hardcoded colors/sizes?
- [ ] Events: Using eventBus? Or props drilling?
- [ ] Error Handling: Using unified error handling?
- [ ] Config: Using config system? Or hardcoded values?

### Duplicate Implementation
- [ ] Other modules implementing same functionality?
- [ ] Similar components/functions that can be merged?

### Pattern Consistency
- [ ] API call pattern: invoke/fetch/service?
- [ ] Error handling: try-catch/Result?
- [ ] State management: useState/zustand/context?
```

### 3.3 Output: Module Layer Refactoring Report

Create analysis report for each key feature: `.refactor/analysis/modules/[feature-name].md`

Create summary `.refactor/analysis/module-report.md`:

```markdown
# Module Layer Analysis Report

## Analysis Coverage
| Feature | Analysis Status | Problem Count | Report Location |
|---------|-----------------|---------------|-----------------|
| File Editor | ✅ Complete | 5 | modules/file-editor.md |
| Chat Feature | ✅ Complete | 8 | modules/chat.md |
| Terminal | ✅ Complete | 3 | modules/terminal.md |

## Problem Summary

### Resources Not Reused (P1)
| Module | Problem | Location | Should Use |
|--------|---------|----------|------------|
| File Editor | Self-made Button | Editor.tsx:45 | components/ui/Button |
| Chat | Self-made formatDate | utils.ts:12 | shared/utils/date |
| Chat | Self-made Card | ChatCard.tsx | components/ui/Card |

### Duplicate Implementations (P1)
| Functionality | Duplicate Locations | Suggestion |
|---------------|---------------------|------------|
| File Save | Editor.tsx, FilePanel.tsx | Merge to FileService |
| Config Read | config.ts, settings.ts | Unify to ConfigService |

### Inconsistent Patterns (P2)
| Module | Problem | Current | Should Unify To |
|--------|---------|---------|-----------------|
| File Editor | API Call | Direct invoke | FileService |
| Terminal | Error Handling | .catch | try-catch |

## Module Layer Refactoring Tasks
1. [M-001] File Editor: Migrate self-made Button to component library
2. [M-002] Chat: Migrate self-made formatDate to utility library
3. [M-003] Chat: Migrate self-made Card to component library
4. [M-004] Merge duplicate file save implementations
5. [M-005] Unify API call pattern to service layer
```

---

## Phase 4: Execute Refactoring

**Goal**: Execute refactoring by layer

### 4.1 Execution Order

**Must do architecture layer first, then module layer:**

```
Phase 1: Architecture Layer Refactoring
├── Resolve circular dependencies
├── Fix layering violations
└── Adjust directory structure

Phase 2: Module Layer Refactoring
├── Resource reuse migration (component library, utility library)
├── Merge duplicate implementations
└── Unify patterns
```

### 4.2 Task Generation

Generate tasks based on Phase 2 and Phase 3 reports:

```
.refactor/tasks/master-plan.md

## Phase 1: Architecture Layer [Priority]
- task-A001: Resolve core -> components dependency [Architecture]
- task-A002: Resolve circular dependency [Architecture]

## Phase 2: Module Layer
- task-M001: File editor module refactoring [Module]
- task-M002: Chat feature module refactoring [Module]
- task-M003: Terminal module refactoring [Module]
```

### 4.3 Execution Flow for Each Task

```
1. Read task file
2. Execute refactoring operations
3. Verify (compile, test)
4. Update task progress
5. Record to session log
6. If phase complete, create checkpoint
```

See:
- [workspace/task-lifecycle.md](workspace/task-lifecycle.md) - Task Lifecycle
- [workspace/session-management.md](workspace/session-management.md) - Session Management

---

## Phase 5: Finalize and Verify

**Goal**: Verify, compare, cleanup

- Full compile and test verification
- Generate before/after comparison document
- Update architecture diagrams
- Archive task files
- Optional: Delete .refactor/ directory

---

## Task Operations

### Recover Session (Continue Refactoring)

**Trigger**: User says "continue refactoring", "pick up where we left off", or `.refactor/` directory exists

**Execute recovery flow** (see "Quick Recovery Entry" above)

**Key Principles**:
- New Agent obtains all context by reading persisted files
- Do not rely on conversation history, rely entirely on state in `.refactor/`
- README.md is core entry point, must be kept up to date

### Create Task

```
1. Generate task ID: task-{number}
2. Create task file: .refactor/tasks/active/task-xxx.md
3. Update master-plan.md task tree
4. Record to session log
```

### Update Task Progress

```
1. Update task file:
   - Check off completed steps
   - Add progress record
   - Update timestamp
2. If task complete:
   - Move to tasks/completed/
   - Update master-plan.md progress percentage
   - If last task in phase, create checkpoint
```

### Create Checkpoint

```
1. Create directory: checkpoints/checkpoint-{number}/
2. Record git ref: git rev-parse HEAD
3. Save state snapshot
4. Update master-plan.md checkpoint table
```

### Session End

```
1. Save current session log
2. Update all active task states
3. Update master-plan.md
4. Report:
   - Tasks completed this session
   - Current progress
   - Next continuation point
```

---

## Verification System

### After Each Change

```bash
# Rust project
cargo check --workspace
cargo clippy --workspace  # Optional
cargo test --workspace    # If tests exist

# TypeScript project
npm run build
npm run lint              # Optional
npm run test              # If tests exist
```

### After Phase Complete

- Start application to verify main functionality
- Visual comparison of key pages
- Create checkpoint

### After All Complete

- Full functional testing
- Before/after comparison document
- Architecture diagram update

---

## Related Documents

### Analysis Methods (Core)
- [analysis/deep-analysis.md](analysis/deep-analysis.md) - **Deep Analysis Methods (Must Read)**
- [analysis/code-analysis.md](analysis/code-analysis.md) - Code Analysis (Call Stack, Data Flow)
- [analysis/architecture-analysis.md](analysis/architecture-analysis.md) - Architecture Analysis
- [analysis/quality-assessment.md](analysis/quality-assessment.md) - Quality Assessment

### Strategy Library
- [strategies/partition-strategies.md](strategies/partition-strategies.md) - Partition Strategies
- [strategies/dependency-sorting.md](strategies/dependency-sorting.md) - Dependency Sorting
- [strategies/parallel-execution.md](strategies/parallel-execution.md) - Parallel Execution

### Pattern Library
- [patterns/vibe-coding-problems.md](patterns/vibe-coding-problems.md) - Problem Classification
- [patterns/refactor-patterns.md](patterns/refactor-patterns.md) - Refactoring Patterns

### Workspace
- [workspace/workspace-spec.md](workspace/workspace-spec.md) - Workspace Specification
- [workspace/task-lifecycle.md](workspace/task-lifecycle.md) - Task Lifecycle
- [workspace/session-management.md](workspace/session-management.md) - Session Management
- [workspace/recovery-guide.md](workspace/recovery-guide.md) - **Agent Recovery Guide**
- [workspace/diagram-conventions.md](workspace/diagram-conventions.md) - Diagram Conventions

---

## Analysis Phase Checklist

Before starting refactoring, ensure the following analysis is complete:

```markdown
## Phase 0: Project Partition
- [ ] Directory structure tree generated
- [ ] Domain boundaries identified
- [ ] UI layer resources inventoried (component library, icon library)
- [ ] Utility layer resources inventoried (utility functions, Hooks, type definitions)
- [ ] Service layer resources inventoried (API services, state management)
- [ ] Infrastructure inventoried (logging, events, i18n, theme, error handling, config, etc.)
- [ ] project-partition.md created

## Phase 1: Key Identification
- [ ] Core feature list completed (at least 5 main features)
- [ ] Entry point for each feature marked
- [ ] Key paths traced
- [ ] key-identification.md created

## Phase 2: Architecture Layer Analysis
- [ ] Layering dependency check complete (any upward dependencies)
- [ ] Circular dependency detection complete
- [ ] Directory structure evaluation complete
- [ ] architecture-report.md created (with specific problems and refactoring suggestions)

## Phase 3: Module Layer Analysis (Core!)
- [ ] Each key feature deeply analyzed
- [ ] Resource reuse detection complete (compare with Phase 0 inventory)
  - [ ] Component library usage
  - [ ] Utility function usage
  - [ ] Public type usage
  - [ ] Public service usage
  - [ ] Hooks usage
- [ ] Infrastructure usage detection complete (compare with Phase 0 infrastructure inventory)
  - [ ] Logging system usage
  - [ ] i18n usage
  - [ ] Theme system usage
  - [ ] Event system usage
  - [ ] Other infrastructure usage
- [ ] Duplicate implementation detection complete
- [ ] Pattern consistency detection complete
- [ ] Analysis report created for each module: modules/[feature-name].md
- [ ] module-report.md created (summarizing all problems and refactoring tasks)

## Task Planning
- [ ] Architecture layer tasks listed (A-xxx)
- [ ] Module layer tasks listed (M-xxx)
- [ ] Execution order determined (architecture first, then module)
- [ ] master-plan.md updated
```

**Only after all checklist items are complete can Phase 4 (Execute Refactoring) begin.**

---

## Key Output Files

Analysis phases must produce the following files:

```
.refactor/
├── analysis/
│   ├── project-partition.md     # Phase 0: Project partition + resource inventory
│   ├── key-identification.md    # Phase 1: Core feature list
│   ├── architecture-report.md   # Phase 2: Architecture layer problems + suggestions
│   ├── module-report.md         # Phase 3: Module layer problem summary + tasks
│   └── modules/                 # Phase 3: Detailed analysis for each feature
│       ├── file-editor.md
│       ├── chat.md
│       └── terminal.md
└── tasks/
    └── master-plan.md           # Task planning (Architecture layer + Module layer)
```
