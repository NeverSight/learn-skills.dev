---
name: usability-tester
description: 'Conduct usability tests and identify UX issues through systematic observation. Use when testing user flows, validating designs, identifying friction points, running heuristic evaluations, or ensuring users can complete core tasks. Use for test planning, think-aloud protocol, task scenarios, severity rating, accessibility evaluation.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Usability Tester

## Overview

Validates that users can successfully complete core tasks through systematic observation and expert evaluation. Covers moderated and unmoderated testing, heuristic evaluation, accessibility checks, and issue severity scoring. Not a substitute for analytics or A/B testing -- those measure what happens, usability testing reveals why.

**When to use:** Testing user flows, validating designs, identifying friction points, running heuristic evaluations, ensuring users can complete core tasks, planning and executing usability test sessions.

**When NOT to use:** Analytics or A/B test setup, visual design critique without task-based evaluation, automated UI testing (use a testing framework), performance benchmarking.

## Quick Reference

| Method                 | Best For                                | Participants                | When to Use                            |
| ---------------------- | --------------------------------------- | --------------------------- | -------------------------------------- |
| Moderated testing      | Deep insights, complex flows            | 5-8 per persona             | Design and prototyping stage           |
| Unmoderated testing    | Scale, quantitative data                | 20-50+                      | Pre-launch and post-launch             |
| Guerrilla testing      | Quick validation, early concepts        | 5-10 random                 | Early concept stage                    |
| First-click testing    | Navigation, information architecture    | 20-50                       | Any stage, especially IA redesigns     |
| Heuristic evaluation   | Expert review against principles        | 3-5 evaluators              | Before user testing, design audits     |
| Cognitive walkthrough  | Task flow analysis                      | 2-3 evaluators              | Early design, new feature review       |
| Accessibility audit    | Inclusive design validation             | 3-5 users with disabilities | Pre-launch, compliance reviews         |
| Synthetic user testing | Scalable task validation with AI agents | N/A (automated)             | Continuous, regression testing         |
| AI-moderated sessions  | Async moderated testing at scale        | 10-50+                      | When moderator availability is limited |

## Core Metrics

| Metric                 | Target                                      | What It Measures            |
| ---------------------- | ------------------------------------------- | --------------------------- |
| Task success rate      | 80% or higher for core tasks                | Can users complete the task |
| Time on task           | Simple under 30s, medium 1-2m, complex 3-5m | Efficiency                  |
| Error rate             | Fewer than 2 per task                       | Learnability and clarity    |
| Post-task satisfaction | 4.0 or higher on 5-point scale              | Subjective ease             |
| SUS score              | 68+ (industry average), 80+ (excellent)     | Overall usability           |

## Issue Severity

Severity equals Impact (1-3) multiplied by Frequency (1-3). Critical (8-9): fix before release. High (6-7): fix before release. Medium (4-5): next release. Low (1-3): backlog.

## Common Mistakes

| Mistake                                                                 | Correct Pattern                                                                        |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Writing task scenarios with product jargon or step-by-step instructions | Use natural language with realistic context and clear goals to test discoverability    |
| Helping users or explaining the UI during test sessions                 | Observe silently and let users struggle; confusion reveals real issues                 |
| Testing only the happy path with ideal inputs                           | Include error states, edge cases, and recovery scenarios in test plans                 |
| Using fewer than 5 participants per persona                             | Recruit 5-8 users per persona; after 5, diminishing returns per Nielsen research       |
| Collecting findings without severity scoring or follow-up actions       | Score every issue by impact times frequency and assign fix priority                    |
| Skipping heuristic evaluation before user testing                       | Run expert review first to catch obvious issues cheaply before spending on recruitment |
| Ignoring accessibility in test planning                                 | Include participants with disabilities and test with assistive technologies            |
| Running only one round of testing                                       | Test in waves: 5 users, fix issues, test 5 more until success rate meets targets       |

## Delegation

- **Test plan and scenario creation**: Use `Task` agent to draft objectives, research questions, and realistic task scenarios for each persona
- **Heuristic evaluation**: Use `Task` agent to walk through interfaces against Nielsen's 10 heuristics and document violations with severity ratings
- **Metrics analysis and severity scoring**: Use `Task` agent to calculate SUS scores, task success rates, and severity ratings from raw test data
- **Test report generation**: Use `Task` agent to compile findings into structured reports with prioritized recommendations
- **Test infrastructure planning**: Use `Plan` agent to select testing methods, define recruitment criteria, and schedule test waves

> If the `quality-auditor` skill is available, delegate full codebase quality audits and scoring to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s quality-auditor -a claude-code -y`

## References

- [Test Planning](references/test-planning.md) -- objectives, research questions, recruitment, task scenario templates, screening criteria
- [Conducting Tests](references/conducting-tests.md) -- think-aloud protocol, facilitation rules, post-task questions, session structure
- [Testing Methods](references/testing-methods.md) -- unmoderated, guerrilla, first-click, cognitive walkthrough, method selection by lifecycle stage
- [Heuristic Evaluation](references/heuristic-evaluation.md) -- Nielsen's 10 heuristics, evaluation process, severity rating, combining with user testing
- [Metrics and Severity](references/metrics-severity.md) -- success rate, time on task, errors, satisfaction, SUS scoring, severity formula
- [Reporting](references/reporting.md) -- test report template, key insights format, stakeholder presentation, recommended actions
- [Accessibility Testing](references/accessibility-testing.md) -- inclusive recruitment, assistive technology testing, WCAG alignment, accessibility heuristics
- [Remote and Tools](references/remote-and-tools.md) -- remote vs in-person comparison, testing tools, test frequency, checklists
