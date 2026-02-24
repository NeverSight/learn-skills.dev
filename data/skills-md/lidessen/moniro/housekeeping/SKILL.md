---
name: housekeeping
description: Manages project housekeeping including documentation organization, dependency management, directory structure, code cleanup, technical debt tracking, and infrastructure configuration. Use when organizing documentation, cleaning up dependencies, reorganizing folders, removing dead code, addressing tech debt, or maintaining project structure.
---

# Housekeeping

Maintains project infrastructure, organization, and cleanliness - the "home management" that keeps projects healthy as they grow.

## Philosophy

### Why Housekeeping?

Housekeeping exists because **entropy is real**.

Left alone, projects accumulate:
- Dead code that no one removes
- Dependencies that no one audits
- Documentation that no one updates
- Structure that no one questions

```
The Entropy Pattern:
├── Small mess → tolerable
├── Accumulation → friction
├── Friction → slowdown
└── Slowdown → "we need a rewrite"
```

Housekeeping is cheaper than rewrites. Regular small efforts beat occasional heroic cleanups.

### The Two Kinds of Value

| Type | Focus | Housekeeping |
|------|-------|--------------|
| External | Users, features, business | Building the product |
| Internal | Developers, structure, maintainability | Managing the home |

Both are essential:
- Features without housekeeping → unsustainable mess
- Housekeeping without features → no product

**Balance**: 80-90% development, 10-20% housekeeping. Adjust based on project health.

### The Boy Scout Rule

> Leave the campground cleaner than you found it.

Applied to code:
- Touching a file? Fix the obvious issues while you're there.
- Don't make a separate "cleanup ticket" for small things.
- Incremental improvement beats scheduled cleanup sprints.

## Six Areas

Each area has its own WHY. Understand the principle, then apply judgment.

### 1. Documentation

**WHY**: Documentation you can't find is documentation that doesn't exist.

The problem isn't "we need more docs." It's "we can't find what we have" or "what we have is wrong."

Focus on:
- Discoverability (can you find it?)
- Currency (is it still true?)
- Audience (who is this for?)

See [documentation/](documentation/) for strategies.

### 2. Dependencies

**WHY**: Every dependency is a liability.

Each package you add:
- Requires updates forever
- Introduces security risk
- Adds to install time
- Creates potential conflicts

Keep only what provides clear value. Audit regularly.

See [dependency-management.md](dependency-management.md) for patterns.

### 3. Directory Structure

**WHY**: Structure should make discovery easy.

Good structure:
- Files are where you expect them
- New developers can navigate without asking
- Related code is together

Bad structure:
- "Where should this go?" confusion
- 50+ files in one directory
- 5+ levels of nesting

See [directory-structure.md](directory-structure.md) for organization patterns.

### 4. Code Organization

**WHY**: Dead code is worse than no code.

Dead code:
- Gets maintained by mistake
- Confuses readers
- Makes search results noisy

Duplication:
- Drifts over time
- Fixes apply to one copy, not all
- Creates false confidence

See [code-organization.md](code-organization.md) for cleanup techniques.

### 5. Technical Debt

**WHY**: Debt compounds.

Small debt: fine. Accumulated debt: crippling.

Track it, prioritize it, pay it down regularly. Don't let it become invisible.

See [tech-debt.md](tech-debt.md) for tracking approaches.

### 6. Infrastructure

**WHY**: Infrastructure friction affects everyone, every day.

Poor infrastructure:
- Slow builds → slow iteration
- Flaky CI → ignored failures
- Outdated configs → mysterious bugs

Good infrastructure is invisible. You only notice it when it's bad.

See [infrastructure.md](infrastructure.md) for maintenance patterns.

## When to Do Housekeeping

### Regular Cadence

| Frequency | Activity |
|-----------|----------|
| Weekly | Quick checks (warnings, unused imports) |
| Monthly | Dependency updates, doc review |
| Quarterly | Full audit, tech debt sprint |

### Opportunistic

- **When touching code**: Fix obvious issues while you're there
- **When blocked**: Use waiting time for cleanup
- **When confused**: Confusion reveals organizational problems

### Event-Triggered

- **Before major refactors**: Clean house first
- **When onboarding**: New eyes see mess clearly
- **After releases**: Stable period for maintenance

## The Progressive Approach

Don't block development with perfectionism:

```
✅ Incremental improvements
✅ Clean as you go
✅ Fix high-impact issues first

❌ "Cleanup month" that freezes everything
❌ Perfectionism paralysis
❌ Over-organizing small projects
```

**Start small**: Pick one area, make it better. Repeat.

## Reference

Detailed workflows and examples:

- [documentation/](documentation/) - Doc organization strategies
- [dependency-management.md](dependency-management.md) - Dependency patterns
- [directory-structure.md](directory-structure.md) - Structure guidelines
- [code-organization.md](code-organization.md) - Code cleanup techniques
- [tech-debt.md](tech-debt.md) - Debt tracking
- [infrastructure.md](infrastructure.md) - Config maintenance
- [examples/](examples/) - Walkthrough examples

## Common Questions

**How often should I do housekeeping?**
Quick checks weekly, focused work monthly, comprehensive audit quarterly. Don't wait until it's overwhelming.

**Won't this slow down feature development?**
Short-term yes, long-term no. Tech debt slows development more than regular housekeeping. 10-20% of time is a reasonable investment.

**Where do I start with a messy project?**
Pick one area with most pain (usually docs or dependencies). Make that area good. Build momentum.

**How do I convince the team?**
Measure impact (velocity, onboarding time). Show quick wins. Integrate into regular work, don't ask for "cleanup month."

## Understanding, Not Rules

| Tension | Resolution |
|---------|------------|
| Features vs Housekeeping | Both are essential. Balance, don't choose. |
| Perfection vs Progress | Good enough now beats perfect never. |
| Scheduled vs Opportunistic | Mix both. Regular cadence + clean as you go. |
| Individual vs Team | Make it visible. Share the load. |

The goal isn't a perfectly organized codebase. It's a codebase that **stays healthy as it grows**.
