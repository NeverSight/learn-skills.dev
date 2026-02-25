---
name: scrum-conductor
description: 'Orchestrates AI-enhanced Scrum ceremonies and sprint coordination. Use when running sprint ceremonies, generating automated daily standups, engineering structured tickets, forecasting sprint capacity, or grooming backlogs. Use for fact-based standups, machine-readable tickets, predictive velocity, and backlog deduplication across GitHub Issues, Jira, and Linear.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Scrum Conductor

## Overview

Facilitates AI-enhanced Scrum orchestration with automated ticket management and high-velocity sprint coordination. Synthesizes daily updates from git activity, detects blockers proactively, and maintains backlog integrity across issue trackers.

**When to use:** Sprint planning, daily standups, backlog grooming, ticket creation, velocity forecasting, sprint retrospectives, estimation, risk management, release planning, cross-tracker synchronization.

**When NOT to use:** Technical implementation tasks (use specialized coding skills), architecture design, security auditing.

## Quick Reference

| Pattern              | Approach                                                        | Key Points                                                   |
| -------------------- | --------------------------------------------------------------- | ------------------------------------------------------------ |
| Fact-first standups  | Auto-generate from git logs and PRs                             | Never ask humans for data in commit history                  |
| Ticket engineering   | Machine-readable DoD with acceptance criteria                   | Binary true/false criteria, implementation pointers          |
| Sprint planning      | Capacity calculation with focus factor and velocity             | Budget = avg velocity (last 3 sprints) adjusted for absences |
| Estimation           | Planning Poker with Fibonacci scale, T-shirt sizing for roadmap | Reference stories anchor the scale, re-calibrate quarterly   |
| Capacity forecasting | Historical cycle time and lead time                             | Factor holidays, context debt, and bottlenecks               |
| Backlog grooming     | AI clustering and deduplication                                 | Flag tickets older than 2 sprints for archive                |
| Backlog refinement   | 1-2 sessions per sprint, Definition of Ready checklist          | Stories must meet DoR before entering sprint planning        |
| Blocker detection    | Scan PRs, assignments, and dependencies                         | Flag stale PRs, OOO assignees, breaking deps                 |
| Parking lot          | Move deep-dives out of standups                                 | Standups focus on status and blockers only                   |
| Sprint retrospective | Start/Stop/Continue with action item tracking                   | Track retro action completion rate across sprints            |
| Risk management      | Dependency mapping, risk register (probability x impact)        | Address risk scores 6+ immediately, monitor 3-5              |
| Release planning     | Multi-sprint roadmap with confidence levels                     | Feature flags decouple deployment from release               |
| Escalation tiers     | Tier 1 autonomous, Tier 2 clarification, Tier 3 pairing         | Match response to complexity                                 |
| Priority frameworks  | MoSCoW, value vs effort matrix, WSJF                            | WSJF favors small high-value items                           |

## Conductor Protocol

1. **Ceremony Initialization**: Identify the current sprint phase (Planning, Daily, Review, Retro)
2. **Telemetry Sync**: Pull recent activity from git commits, PRs, and communication channels
3. **Fact Synthesis**: Generate factual summaries before ceremonies begin
4. **Verification**: Confirm all action items are converted into tracked tickets with clear owners and DoD

## Common Mistakes

| Mistake                                                           | Correct Pattern                                                                   |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Asking developers for status updates available in commit logs     | Auto-generate fact summaries from PRs and merges before standups                  |
| Creating tickets without a machine-readable Definition of Done    | Every ticket needs explicit acceptance criteria and technical pointers            |
| Guessing sprint velocity without historical data                  | Use cycle time, holidays, and context debt to forecast capacity                   |
| Letting standups run beyond 15 minutes with deep-dive discussions | Move deep-dives to a parking lot session; standups focus on blockers              |
| Allowing the backlog to grow to 200+ items without pruning        | Auto-flag tickets older than 2 sprints for archive or refactor                    |
| Using AI to replace human conversation                            | Use AI to prepare for the conversation, not substitute it                         |
| Ignoring team sentiment and morale signals                        | High velocity with low morale is a leading indicator of burnout                   |
| No Definition of Done agreed by the team                          | Establish a team-wide DoD checklist applied to every story                        |
| Skipping retrospectives when the sprint "went fine"               | Every sprint has improvement opportunities; consistency builds the habit          |
| Sprint planning without capacity calculation                      | Calculate capacity: members x available days x focus factor                       |
| Stories entering sprint without acceptance criteria               | Enforce Definition of Ready before stories enter a sprint                         |
| Estimating stories individually instead of as a team              | Use Planning Poker so the full team contributes perspective                       |
| Slicing stories horizontally by layer                             | Slice vertically through all layers so each ticket delivers working functionality |
| No dependency mapping between sprint stories                      | Map dependencies explicitly and identify the critical path                        |
| Retro action items with no owner or due date                      | Every action item needs an owner, a due date, and follow-up tracking              |

## Delegation

- **Synthesize daily standup summaries from git activity and PRs**: Use `Task` agent to pull commit logs and generate fact-based updates
- **Cluster and deduplicate backlog tickets across issue trackers**: Use `Explore` agent to scan GitHub Issues, Jira, and Linear for similar or conflicting items
- **Plan sprint capacity and risk assessment using historical velocity**: Use `Plan` agent to model delivery probability and identify at-risk items

## References

- [Automated daily rituals, fact-checking workflows, blocker detection, sprint planning, retrospectives, and refinement](references/daily-rituals.md)
- [Ticket engineering standards, user story templates, estimation techniques, and priority frameworks](references/ticket-engineering.md)
- [Predictive velocity, sprint metrics, risk management, distributed teams, and release planning](references/velocity-risk.md)
- [Multi-agent task handoffs, escalation tiers, AI retrospectives, blocker detection, and human escalation guardrails](references/agile-agents.md)
