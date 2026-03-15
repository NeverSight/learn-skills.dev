---
name: vm-planning
description: Comprehensive planning for features, implementations, and tasks. Analyzes user requirements, cross-references with codebase, applies best practices, and generates detailed implementation plans. Ensures plans are accurate and actionable.
---

# VM Planning Skill

Professional-grade planning for any development task, feature, or implementation with codebase awareness and best practices.

## When to Use

- "Create a plan for..."
- "I need to plan..."
- "Help me plan the implementation of..."
- "Generate an implementation plan for..."
- "Plan a new feature"
- "Break down this task into steps"
- "Create a roadmap for..."
- "I need a detailed implementation strategy"

## Workflow

### Step 1: Initial Confirmation

**ALWAYS start by asking:**

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "Do you want to proceed to create a plan?",
      "type": "single_select",
      "options": [
        "Yes! Let's plan it!",
        "No, Thanks."
      ]
    }
  ]
})
```

**If "No, Thanks."** → Stop with:
```
No problem! Let me know when you need help planning something. 📋
```

**If "Yes! Let's plan it!"** → Proceed to Step 2

### Step 2: Analyze User Request

**Read and understand what the user wants to achieve:**

- Extract the main goal/feature
- Identify technical requirements
- Understand constraints (time, technology, scope)
- Detect dependencies
- Clarify ambiguities (ask follow-up questions if needed)

**Example Analysis:**

```
User Request: "Add user authentication with OAuth"

Analysis:
✓ Main Goal: Implement OAuth authentication
✓ Requirements: OAuth providers (Google, GitHub?), JWT tokens, session management
✓ Dependencies: Need auth library, database for users
✓ Scope: Login, logout, protected routes, user profile
✓ Questions: Which OAuth providers? Existing user system?
```

### Step 3: Codebase Context Selection

**Prompt for analysis depth:**

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "How would you like to proceed with codebase analysis?",
      "type": "single_select",
      "options": [
        "Check entire codebase + AGENTS.md, package.json and README.md (Recommended)",
        "Quick"
      ]
    }
  ]
})
```

**Option 1: Comprehensive (Recommended)**
```
Analyzing codebase... 🔍

Reading:
✓ AGENTS.md - Team conventions, workflows
✓ package.json - Dependencies, scripts, tech stack
✓ README.md - Project overview, setup
✓ Source files - Architecture, patterns, existing code
✓ Config files - Build, lint, test setup

Framework Detected: Next.js 14 + TypeScript
State: Redux Toolkit
Database: PostgreSQL + Prisma
Auth: Currently using email/password only
API: RESTful + tRPC

Cross-referencing with best practices...
```

**Option 2: Quick**
```
Quick analysis... ⚡

Detected:
- Framework: React 18
- Language: TypeScript
- Package Manager: npm

Proceeding with general best practices...
```

### Step 4: Generate Plan

**Create comprehensive plan covering:**

1. **Overview** - What we're building and why
2. **Technical Approach** - How to implement it
3. **Architecture** - Components, modules, data flow
4. **File Structure** - New files and modifications
5. **Implementation Steps** - Ordered tasks with details
6. **Dependencies** - Packages, APIs, services needed
7. **Testing Strategy** - How to validate
8. **Edge Cases** - Potential issues and solutions
9. **Timeline** - Realistic time estimates
10. **Checklist** - Tasks to complete

**Display progress:**
```
Creating plan... 📝

✓ Analyzed requirements
✓ Cross-referenced codebase
✓ Identified architecture patterns
✓ Planned implementation steps
✓ Added testing strategy
✓ Estimated timeline

Plan complete!
```

### Step 5: Export or Implement

**Prompt for next action:**

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "Where would you like to export the plan?",
      "type": "single_select",
      "options": [
        "Custom path and name (I'll specify)",
        "Proceed with the plan!",
        "Cancel"
      ]
    }
  ]
})
```

**Option 1: Custom path and name**
- Ask user: "Please provide the path and filename (e.g., docs/AUTH_PLAN.md or ./FEATURE_PLAN.md):"
- Validate path is valid
- Export plan to specified location
- Respond: `Plan exported to {path}! 📋`

**Option 2: Proceed with the plan!**
- Show confirmation prompt:

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "Are you sure you want to proceed with implementing the plan?",
      "type": "single_select",
      "options": [
        "Yes.",
        "No."
      ]
    }
  ]
})
```

- **If "Yes."** → Start implementation following the plan
- **If "No."** → Export to default location and stop

**Option 3: Cancel**
- Stop with: `Plan not exported. You can generate it again anytime! 📋`


## Planning Principles

### 1. Accuracy & Feasibility

**DON'T mislead:**
- ❌ Suggest impossible timelines
- ❌ Recommend unavailable libraries
- ❌ Ignore existing architecture
- ❌ Skip critical steps
- ❌ Assume user knowledge

**DO ensure:**
- ✅ Realistic time estimates
- ✅ Compatible with existing stack
- ✅ Follow project conventions
- ✅ Include all necessary steps
- ✅ Explain technical decisions

**Example - Bad Plan:**
```markdown
## Implementation Plan
1. Add authentication (30 minutes)
2. Done!
```
**Why bad:** No details, unrealistic timeline, missing steps

**Example - Good Plan:**
```markdown
## Implementation Plan

### Phase 1: Setup (2 hours)
1. Install dependencies
   - npm install next-auth @prisma/client bcrypt
   - npm install -D @types/bcrypt
   
2. Configure Prisma schema
   - Add User model with authentication fields
   - Create migration: npx prisma migrate dev
   
3. Set up environment variables
   - NEXTAUTH_SECRET, NEXTAUTH_URL
   - OAuth credentials (GOOGLE_ID, GOOGLE_SECRET)

### Phase 2: Implementation (4 hours)
[... detailed steps ...]
```
**Why good:** Specific commands, realistic time, detailed steps

### 2. Context Awareness

**Analyze existing codebase:**

```typescript
// Detected pattern: Using custom API wrapper
// File: src/lib/api.ts
export async function apiRequest(endpoint: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  return response.json();
}

// Plan should use this pattern, not fetch directly:
✅ "Use existing apiRequest() helper"
❌ "Use fetch() directly"
```

**Respect conventions:**
```javascript
// Detected: Project uses named exports
export const UserService = { ... }; // ✅ Existing style

// Plan should follow:
export const AuthService = { ... }; // ✅ Consistent
export default AuthService; // ❌ Inconsistent
```

### 3. Completeness

**Include ALL necessary aspects:**

✅ **Setup Requirements**
- Environment variables
- API keys / credentials
- Database migrations
- Configuration files

✅ **Implementation Details**
- File-by-file breakdown
- Code snippets for complex logic
- Integration points with existing code

✅ **Testing Strategy**
- Unit tests to write
- Integration tests needed
- Manual testing steps
- Edge cases to verify

✅ **Documentation**
- README updates
- API documentation
- Inline code comments
- Usage examples

✅ **Deployment Considerations**
- Environment setup
- Build configuration
- Migration scripts
- Rollback plan

## Plan Template

```markdown
# [Feature Name] Implementation Plan

**Created**: YYYY-MM-DD
**Estimated Time**: X-Y hours
**Complexity**: Low/Medium/High
**Impact**: Low/Medium/High

## Overview

### Goal
[Clear description of what we're building]

### Why
[Business value, user benefit, or technical necessity]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Approach

### Architecture Decision
[Chosen approach and why]

**Alternatives Considered:**
1. Alternative 1 - Rejected because...
2. Alternative 2 - Rejected because...

### Technology Stack
- Framework: Next.js 14
- Language: TypeScript 5.0
- Database: PostgreSQL + Prisma
- Authentication: NextAuth.js
- State: Redux Toolkit

### Integration Points
- Existing user management system
- Payment processing module
- Email notification service

## Current State Analysis

### Existing Code
```
src/
├── app/
│   ├── api/ (REST endpoints)
│   └── (routes)/
├── components/ (React components)
├── lib/
│   ├── db.ts (Prisma client)
│   └── api.ts (API wrapper)
└── types/ (TypeScript types)
```

### Identified Patterns
- Using server components by default
- API routes in app/api/
- Shared utilities in lib/
- Type definitions in types/

### Gaps to Fill
- ❌ No authentication system
- ❌ No protected route middleware
- ❌ No user session management

## File Structure

### New Files to Create
```
src/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth]/
│   │           └── route.ts (NEW)
│   ├── login/
│   │   └── page.tsx (NEW)
│   └── dashboard/
│       └── page.tsx (NEW)
├── lib/
│   ├── auth.ts (NEW)
│   └── authOptions.ts (NEW)
├── middleware.ts (NEW)
└── types/
    └── auth.ts (NEW)
```

### Files to Modify
```
- prisma/schema.prisma (Add User, Account, Session models)
- package.json (Add dependencies)
- .env.example (Add auth variables)
- README.md (Add auth setup instructions)
```
```

## Best Practices

✅ **Do:**
- Break down into phases
- Include time estimates
- Add code examples
- Plan for edge cases
- Document decisions
- Include rollback plans
- Add success criteria
- Consider testing early

❌ **Don't:**
- Skip prerequisites
- Underestimate time
- Ignore existing patterns
- Assume knowledge
- Forget error handling
- Overlook edge cases
- Rush into implementation

## Output Messages

**After plan creation:**
```
✅ Plan Created Successfully!

Summary:
- Phases: 5
- Total Steps: 28
- Estimated Time: 12-15 hours
- Complexity: Medium
- Files to Create: 8
- Files to Modify: 4

Plan includes:
✓ Detailed implementation steps
✓ Code examples
✓ Testing strategy
✓ Edge cases & solutions
✓ Timeline with phases
✓ Success criteria
```

**After export:**
```
✅ Plan Exported!

Location: {path}
Size: 15.2 KB
Sections: 10

Next steps:
1. Review the plan
2. Gather team feedback
3. Start with Phase 1
4. Track progress with checklist

Good luck! 🚀
```

**After implementation start:**
```
✅ Implementation Started!

Following plan: {plan_name}
Current Phase: Phase 1 - Setup & Configuration
Next Step: Install dependencies

Progress will be tracked automatically.
Let's build this! 💪
```

## Framework-Specific Adjustments

### React/Next.js
- Focus on component structure
- Consider server vs client components
- Plan for state management
- Include routing strategy

### Node.js/Express
- Plan middleware order
- Structure route handlers
- Plan error handling
- Consider validation layer

### Python/Django
- Plan models and migrations
- Structure views and serializers
- Plan URL patterns
- Include admin integration

### Go
- Plan package structure
- Consider interfaces
- Plan error handling
- Include testing approach

## Integration with Existing Code

**Always:**
1. Read existing code first
2. Match naming conventions
3. Follow established patterns
4. Respect architecture decisions
5. Maintain consistency
6. Reuse existing utilities
7. Update related documentation

**Example:**
```
Detected: Project uses custom logger in lib/logger.ts
Plan: Use existing logger instead of console.log
✅ import { logger } from "@/lib/logger";
❌ console.log("message");
```

## Quality Assurance

**Before finalizing plan:**

1. **Technical Review**
   - Code examples compile
   - Commands are correct
   - Paths are valid
   - Dependencies exist

2. **Feasibility Check**
   - Timeline is realistic
   - Team has required skills
   - No missing prerequisites
   - Resources are available

3. **Completeness Audit**
   - All phases covered
   - Testing included
   - Documentation planned
   - Edge cases addressed

4. **Clarity Validation**
   - Steps are clear
   - Examples are helpful
   - Terms are explained
   - Success is measurable

## Final Notes

This skill creates **production-ready implementation plans** that:
- Are accurate and don't mislead
- Consider existing codebase
- Follow best practices
- Include all necessary details
- Provide realistic timelines
- Account for edge cases
- Enable successful execution

Every plan is tailored to the specific request, codebase, and team context. 🎯
