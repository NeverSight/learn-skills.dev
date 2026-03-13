---
name: architecture-guard
description: Validates file placement against architecture.md before creating new files or modules. Use when creating files or when unsure where code should go.
version: 1.0.0
---

# Architecture Guard

Validates that new files and modules are placed correctly according to `.context/architecture.md`. Prevents architectural drift by catching misplacements before code is written.

## When to Use This Skill

- Before creating a new file or directory
- When moving or renaming files
- When a user asks "where should I put this?"
- During code review to validate file placement

## Validation Process

### Step 1: Read Architecture Definition
Read `.context/architecture.md` to understand:
- The directory structure
- Module boundaries and responsibilities
- Import rules between modules

### Step 2: Classify the New File
Determine which module the new file belongs to based on its purpose:

| File Purpose | Likely Module | Examples |
|---|---|---|
| Business logic, domain models | `core/` | validators, services, entities |
| API calls, DB queries, file I/O | `adapters/` | repositories, clients, providers |
| UI components, pages, layouts | `ui/` | components, screens, hooks |
| Shared utilities, types, constants | `shared/` | helpers, types, config |
| Tests | `tests/` | mirrors the module being tested |

### Step 3: Validate Placement
Check if the proposed path matches the architecture:

**✅ Valid placement:**
```
Creating: src/core/auth/validate-token.ts
Module:   core/ (business logic → correct)
Result:   APPROVED
```

**❌ Invalid placement:**
```
Creating: src/utils/auth-service.ts
Module:   utils/ (not defined in architecture.md)
Expected: src/core/auth/ (services belong in core/)
Result:   REJECTED — suggest correct path
```

### Step 4: Check Import Rules
If the new file imports from other modules, validate against the "May Import From" rules:

```
File:     src/core/auth/validate-token.ts
Imports:  from '../../adapters/db/user-repo'
Rule:     core/ may only import from shared/
Result:   ❌ VIOLATION — core/ cannot import from adapters/
Fix:      Inject the dependency via interface in core/, implement in adapters/
```

## Response Format

### Approval
```
✅ ARCHITECTURE CHECK PASSED
File: src/adapters/api/payment-client.ts
Module: adapters/ — External integrations ✓
Imports: shared/types ✓
```

### Rejection with Guidance
```
❌ ARCHITECTURE CHECK FAILED

File: src/helpers/format-date.ts
Issue: "helpers/" is not a defined module

Recommended path: src/shared/format-date.ts
Reason: Utility functions belong in shared/ per architecture.md

Should I create the file at the recommended path instead?
```

## Edge Cases

### New Module Needed
If the file doesn't fit any existing module, propose updating `architecture.md`:

```
⚠️ NO MATCHING MODULE

File: src/workers/email-queue.ts
Analysis: Background workers are not covered in architecture.md

Proposal: Add "workers/" module to architecture.md:
| workers/ | Background jobs, queues, scheduled tasks | core/, shared/, adapters/ |

Proceed with creating the module? [Y/N]
```

### Test File Placement
Test files should mirror the source structure:
- Source: `src/core/auth/validate-token.ts`
- Test: `tests/core/auth/validate-token.test.ts`

## Integration
- Triggers `context-sync` when a new module is proposed
- Works alongside `spec-lifecycle` to validate that spec-related files go in the right place
