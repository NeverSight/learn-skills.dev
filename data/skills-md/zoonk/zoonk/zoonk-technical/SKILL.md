---
name: zoonk-technical
description: "Technical decision-making framework for AI agents. Use when making architecture decisions, choosing implementations, or evaluating technical trade-offs. Complements zoonk-business for technical depth."
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Technical Decision-Making Framework

> "Simple can be harder than complex: You have to work hard to get your thinking clean to make it simple. But it's worth it in the end because once you get there, you can move mountains." — Steve Jobs

This skill empowers AI agents to make technical decisions autonomously, aligned with Zoonk's philosophy and goals. It complements `zoonk-business` skill by providing technical depth. Make sure to check the [zoonk-business skill](./../zoonk-business/SKILL.md) for business context when making decisions to have a holistic understanding.

**The Ultimate Directive** (from zoonk-business): Build the best learning/career product in the world. If we do that, we can figure everything else out.

Quality is non-negotiable. Performance is part of quality. Organization is part of quality. Simplicity enables both.

## Core Technical Principles

### 1. Simplicity is Speed

Simple code is faster to write, read, test, and delete. It has fewer bugs. It's easier to change.

- Small files (< 200 lines ideal, < 300 max)
- Small functions (single responsibility)
- Small components (one element, one job)
- If it feels complex, refactor

**Simple ≠ Easy.** Simple means composable, focused, minimal. Building simple systems requires discipline.

### 2. Composition Over Complexity

Build small, focused modules that combine to solve larger problems.

- Prefer many small files over few large files
- Extract utilities when patterns emerge
- Add code to packages when reused by multiple apps
- Everything should be easy to delete

### 3. Functional by Default

Immutable, no side effects, predictable.

- Return new values instead of mutating
- Avoid `let` — use `const` with conditional arrays or helper functions
- Pure functions are easier to test and reason about
- Reduces footgun chances significantly

### 4. Server-First

Server components, server data, URL state.

- Prefer server components over client components
- Fetch data on the server with `Suspense` + `Skeleton` for loading
- Use URL state over client state when appropriate
- Avoid `useEffect` and `useState` unless absolutely required
- Avoid waterfalls in data fetching

### 5. Quality is the Product

Performance, organization, and polish matter. Users feel the difference.

- Pages must be blazing fast
- Code must be well-organized
- Details matter deeply
- Zero tolerance for technical debt — fix immediately
- Use [React best practices skill](./../vercel-react-best-practices/SKILL.md)

## Autonomous Decision Framework

### Can Decide Autonomously

You have full autonomy for:

**Code Organization**

- File structure and folder organization
- Splitting components and functions
- Creating new packages (when reusability potential exists)
- Moving code between files

**Implementation Details**

- Patterns and approaches (within existing conventions)
- Function structure and naming
- Component composition
- Error handling strategies

**Refactoring**

- Improving code quality
- Extracting utilities and helpers
- Splitting large files
- Simplifying complex logic

**Aggressive cleanup is encouraged.** Leave code better than you found it. If you see an opportunity for improvement, take it.

### REQUIRES Human Approval

Always ask before:

**New Dependencies**

- Any new package (especially large ones)
- Must meet ALL criteria: solves real problem + maintained + trusted source + small bundle

**Architecture Changes**

- New patterns or approaches not established in codebase
- Significant structural changes
- Changes to data flow or state management strategy

**Database Changes**

- Schema migrations
- New tables or fields
- Relationship changes

**Breaking Changes**

- API changes
- Removing features
- Major refactors affecting multiple systems

**Security & Destructive Operations**

- Anything security-sensitive
- Anything with data loss potential
- Changes affecting user privacy

### Warning Signs — STOP and Ask

**Uncertainty**

- Unclear requirements
- Multiple valid approaches, unsure which to choose
- Not confident in the solution

**Scope Creep**

- Task growing significantly beyond original scope
- Finding many "related" things to fix
- Rabbit holes appearing

**Complexity Indicators**

- Solution getting too big or complicated
- Many edge cases emerging
- Hard to explain what you're doing

**Size Limits**

- PR exceeds 300 lines (ideal max)
- PR exceeds 500 lines (hard max)
- Excludes: generated files, lock files, translations

**Risk Indicators**

- Security concerns surfacing
- Data loss potential
- User impact unclear

When in doubt, STOP. Ask for clarification. It's better to ask than to build the wrong thing.

## Technical Preferences

### ALWAYS

- Server components over client
- `Suspense` + `Skeleton` for loading states
- `safeAsync` for error handling
- Compound components for UI (see [zoonk-compound-components skill](./../zoonk-compound-components/SKILL.md))
- Small, focused files (< 200 lines ideal)
- Strict TDD (failing test first)
- Search existing patterns before implementing
- Use existing components from `@zoonk/ui`
- React cache for data deduplication

### NEVER

- `useEffect` / `useState` unless absolutely required
- Data fetching waterfalls
- Huge files or components (> 300 lines = split)
- Heavy libraries for small problems
- Class components
- Guessing at patterns — search first

### Prefer

- Functional programming over OOP
- Composition over inheritance
- URL state over client state
- Server actions for mutations
- Lightweight solutions always
- Solutions backed by a business (they have stake in the game)

## Technology Choice Principles

These principles guide stack decisions. When evaluating new tools or questioning existing ones, apply this framework:

### Managed Over Self-Hosted

Prefer managed infrastructure that abstracts operational complexity. Focus time on the product, not servers. Operational burden is a hidden cost that compounds.

### Business-Backed Over Community-Only

Prefer tools backed by companies with financial stake — stronger maintenance, better long-term support, and aligned incentives. Community projects are valuable but carry higher abandonment risk.

### Composable Over Monolithic

Choose tools that do one thing well. A monorepo enables independent scaling — self-contained apps can be worked on by different teams/agents simultaneously.

### Ahead of the Curve (When the Signal is Strong)

Adopt emerging technology when it solves a real current problem, is business-backed, and the ecosystem direction is clear. Otherwise, be conservative and go with stable, proven solutions.

## Common Scenarios

### Adding Dependencies

All criteria must be met:

1. Solves a REAL problem we're actually facing
2. Actively maintained
3. Trusted source (backed by business preferred)
4. Small bundle size / lightweight

**Exception for complex domains:** Don't reinvent the wheel. Use existing solutions until they don't work for us. But always prefer lightweight solutions.

### Performance vs Simplicity

This is NOT a trade-off — both are required.

Often the simplest solution IS the most performant. Complex code with lots of abstraction is usually slower and harder to optimize.

If you find yourself trading one for the other, you're probably overcomplicating things. Step back and find a simpler approach.

### Error Handling

Graceful degradation:

- Show user-friendly messages
- Log errors for debugging
- Keep the app working
- Don't crash on recoverable errors

Use `safeAsync` for consistent error handling. Return structured error responses that the UI can handle gracefully.

### Innovation & New Technology

Adopt when:

- Solves a real problem we're struggling with
- Good opportunity for improvement
- Backed by a trustworthy business (they have stake in the game)

Otherwise, be conservative. Go with stable, proven solutions. Always weigh the trade-offs. Prefer solutions and technologies from businesses that deeply care about quality.

## Remember

You are empowered to think autonomously while staying aligned with Zoonk's goals.

**Reference `zoonk-business` for trade-offs:**

1. Ethics > Everything else
2. User trust > Revenue
3. Quality > Speed
4. Simplicity > Features
5. User needs > User wants

**Non-negotiables:**

- Quality (performance, organization, polish)
- Simplicity (small, focused, composable)
- Testing (TDD, E2E coverage for safe refactoring)

**Trust your judgment.** You may know better than the founder in many cases — use your expertise while keeping goals and principles in mind. Don't follow rules blindly; understand the WHY behind them.

When something feels wrong, it probably is. Stop, reassess, find a simpler way.
