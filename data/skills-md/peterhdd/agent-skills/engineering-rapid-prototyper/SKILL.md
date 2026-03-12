---
name: engineering-rapid-prototyper
description: "Build functional prototypes and MVPs at maximum speed to validate ideas through working software. Use when you need proof-of-concept development, rapid iteration on user feedback, no-code or low-code solutions, backend-as-a-service integration, A/B testing scaffolding, quick feature validation, or modular architectures designed for fast experimentation and learning."
metadata:
  version: "1.0.0"
---

# Rapid Prototyping Guide

## Overview
This guide covers fast proof-of-concept development and MVP creation. Use it when building prototypes to validate hypotheses, setting up A/B testing, or choosing rapid development stacks that prioritize speed-to-deploy over production hardening.

## Stack Selection Guide

### How to choose tools
- When authentication is needed, use Clerk or NextAuth for instant setup — never build custom auth for a prototype. If the prototype does not need user accounts to test the hypothesis, skip auth entirely.
- When a database is needed, use Prisma + Supabase for instant hosting, schema management, and row-level security. If the prototype only needs to store <100 records for testing, use a JSON file or localStorage — do not set up a database.
- When deployment is needed, use Vercel for instant hosting and preview URLs on every PR. First deploy must happen within 2 hours of project start.
- When no-code/low-code can cover the requirement, use it — speed to validation matters more than custom code.
- When building, implement core functionality first, polish and edge cases later. If you are writing error handling before the happy path works end-to-end, stop.

### Decision Rules for Scope
- Maximum 5 database tables. If the schema needs >5 tables, you are overbuilding — cut scope or simplify the data model.
- Maximum 3-5 features. If the feature list exceeds 5, rank by hypothesis impact and cut the bottom ones. A prototype tests one hypothesis well, not five hypotheses poorly.
- Maximum 8 pages/routes. If more are needed, combine views or cut features.
- Zero custom UI components — use shadcn/ui, Radix, or similar. If a component does not exist in the library, simplify the design to fit what exists.
- No custom backend logic beyond CRUD + one business rule. If the prototype requires complex backend processing (queues, scheduled jobs, multi-step workflows), mock it with a simple endpoint that returns realistic fake data.
- No optimization. No caching, no CDN config, no database indexes, no lazy loading, no code splitting. These are production concerns. The prototype must be fast enough to demo — nothing more.

### Kill Criteria
- If setup (project init → first deploy) takes >3 hours, the stack is too complex. Switch to a simpler approach.
- If after 2 days the core hypothesis cannot be tested in the prototype, redesign the prototype — not the hypothesis.
- If a single feature takes >1 day to implement, the feature is too complex for a prototype. Simplify or fake it with static data.
- If you are writing tests, you have left prototype mode. Prototypes are disposable. Tests are for code you intend to keep.

### Recommended Stack
- **Framework**: Next.js 14+ (App Router)
- **UI**: shadcn/ui + react-hook-form + Zod validation
- **State**: Zustand (only if client state is needed — prefer server components + server actions)
- **Database**: Prisma + Supabase (only if persistence is needed to test the hypothesis)
- **Auth**: Clerk or NextAuth (only if user identity is part of the hypothesis)
- **Animation**: Framer Motion (only for demos — skip if internal testing only)
- **Deploy**: Vercel

See [Stack Setup](references/stack-setup.md) for the full package.json and shadcn/ui install commands.

## Workflow

### Hour 0-2: Hypothesis and Setup
- Write the hypothesis in one sentence: "We believe [user] will [action] because [reason], measured by [metric]." If you cannot write this sentence, you are not ready to build.
- Scaffold project with `scripts/scaffold.sh` or `npx create-next-app`. Install shadcn/ui. Deploy empty shell to Vercel. This must be done in <2 hours.
- If auth is needed, configure Clerk (15 min). If database is needed, create Supabase project and run `prisma db push` (20 min). If neither is needed for the hypothesis, skip both.

### Hour 2-8: Core Flow (Day 1)
- Build the single most important user flow end-to-end: entry point → core action → visible result. No side features, no settings, no edge cases.
- Use server components + server actions for data fetching. Only add client components when interactivity requires it.
- Hardcode anything that is not part of the hypothesis. Use seed data, placeholder images, and realistic fake content. If a feature needs an external API that is not set up, return mock data from a server action.
- Deploy to Vercel at end of day 1. The prototype must be clickable by a real user on day 1.

### Hour 8-20: Supporting Features (Day 2-3)
- Add 2-4 supporting features, one at a time. Deploy after each feature. If a feature breaks the deploy, revert it immediately — do not debug for >30 minutes.
- Add a feedback mechanism: either a simple form (shadcn/ui textarea + server action that writes to Supabase) or a Hotjar/PostHog snippet (3 lines of code).
- If A/B testing is needed, use Vercel Edge Config or a simple cookie-based split — not a full experimentation platform.

### Hour 20-24: Test and Decide (Day 3-4)
- Share with 5-10 target users. Observe or collect feedback for 24-48 hours.
- Measure against the hypothesis metric defined in hour 0. If the metric is positive, plan production build. If negative, decide: pivot the hypothesis or kill the prototype.
- Never iterate on a prototype for >1 week. After 1 week, either commit to production-quality rebuild or archive it.

See [Code Examples](references/code-examples.md) for a feedback form component and A/B testing hook.

## Validation Feedback Loop
The prototype exists to answer a question. Use this protocol to ensure it actually does:
- **Before building**: Write the hypothesis, the metric, and the threshold for success/failure. Example: "If >30% of test users complete the checkout flow without help, the UX hypothesis is validated."
- **During building**: After each feature, deploy and check if the feature is testable by a real user. If it is not clickable end-to-end, it is not done.
- **Day 1 checkpoint**: Share the deployed prototype with 1 person (yourself or a teammate). Can they complete the core flow without explanation? If not, the flow is broken — fix before adding features.
- **Day 2-3 checkpoint**: Share with 5-10 target users. Observe or collect feedback. If users are confused by the same step, that is the blocker — fix that one step, do not add more features.
- **Decision point** (day 3-5): Measure the hypothesis metric. Three outcomes:
  - **Metric met**: Hypothesis validated. Document the learnings, archive the prototype, begin production planning with the production skills.
  - **Metric close but not met**: One iteration allowed. Identify the single biggest friction point, fix it, re-test with 5 more users. If still not met, kill it.
  - **Metric far from target**: Hypothesis rejected. Document why. Decide: pivot (new hypothesis, new prototype) or kill (move to a different idea entirely).

## Self-Verification Protocol
Prototypes do not need test suites, but they need basic verification:
- The app deploys successfully to Vercel (or equivalent) from the main branch. If deploy is broken, nothing else matters.
- The core flow works end-to-end: a new user can complete the primary action without hitting an error screen or dead end.
- The feedback mechanism works: submit test feedback and verify it is captured (check Supabase table, Hotjar recording, or PostHog event).
- The A/B split (if any) is working: verify both variants render by toggling the split cookie/flag.
- No placeholder text ("Lorem ipsum", "TODO", "test") is visible to test users — it undermines credibility and skews feedback.
- The prototype loads in <3 seconds on a mobile connection (throttle in DevTools to "Fast 3G" and verify). Slow prototypes get abandoned before the hypothesis is tested.

## Scripts

- `scripts/scaffold.sh` -- Create a Next.js + TypeScript + Tailwind project structure with minimal boilerplate files (no npm install). Run with `--help` for options.

## Anti-Patterns (Stop Immediately If You Catch Yourself Doing These)
- Writing unit tests or integration tests for prototype code.
- Setting up CI/CD pipelines, linting rules, or pre-commit hooks.
- Creating a design system, custom theme, or component library.
- Building an admin panel, settings page, or user profile page (unless it is the hypothesis).
- Adding error boundaries, retry logic, loading skeletons, or empty states.
- Refactoring code for "cleanliness" — prototype code is disposable.
- Debating technology choices for >15 minutes — pick the default stack and move on.
- Building features "while we are at it" that are not in the 3-5 feature list.

## Transition to Production
When the hypothesis is validated and the decision is to build for real:
- Do NOT refactor the prototype into production code. Start fresh with the production skill (engineering-frontend-developer, engineering-backend-architect, etc.).
- Extract from the prototype: validated user flows, data model shape, API contract, and UI screenshots. These are the spec for the production build.
- Archive the prototype repo. It served its purpose.

## References

- [Stack Setup](references/stack-setup.md) -- Package.json and shadcn/ui install commands.
- [Code Examples](references/code-examples.md) -- Feedback form component and A/B testing hook.
- [Full Stack Integration](references/full-stack-integration.md) -- Prisma schema, Supabase + Clerk auth, server actions, tRPC, file uploads, and email with Resend.
- [UI Patterns](references/ui-patterns.md) -- Data tables, command palette, form wizard, dashboard layout, toasts, and loading skeletons with shadcn/ui.
