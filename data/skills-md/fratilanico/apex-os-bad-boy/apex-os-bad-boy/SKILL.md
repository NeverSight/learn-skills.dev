---
name: apex-os-bad-boy
description: "The ultimate agent productivity system - 45+ skills with intelligent recommendations, risk-based planning levels, and systematic workflows for maximum efficiency."
tier: FULL
tags: [productivity, workflow, planning, debugging, testing, react, nextjs, supabase, browser]
---

# APEX OS Bad Boy

> "Everything you need. Nothing you don't. Mastery at your fingertips."

## Overview

APEX OS Bad Boy is a comprehensive productivity system for AI agents that provides:

- **45+ integrated skills** across all domains
- **Intelligent skill recommendations** (75%+ accuracy)
- **Risk-based planning levels** (SAFE/MID/RISKY)
- **Systematic workflows** for every situation
- **Best-in-class practices** from top engineering teams

This skill teaches agents WHEN and HOW to use the right tools at the right time.

## The Core Philosophy

### 1. The Planning Slider

```
SAFE MODE ──────────────────────────────────▶ RISKY MODE

Full Design    Quick Plan           Just Do It
   ↓               ↓                    ↓
Plan → Code   Plan + Code         Code → Fix
   ↓               ↓                    ↓
Test → Ship   Review → Ship       Ship → Fix
```

| Mode | When to Use | Workflow |
|------|-------------|----------|
| **SAFE** | Production, auth, payments, user data | Design → Plan → TDD → Code → Review → Deploy |
| **MID** | Bug fixes, small features, refactoring | Quick Plan → Code → Review → Ship |
| **RISKY** | POCs, experiments, prototypes | Just Do It → Ship → Fix |

### 2. The 75% Rule

> If a skill has 75%+ probability of helping, invoke it. Always.

### 3. Right Tool, Right Job

> Never use a hammer when you need a scalpel. Know your tools.

---

## The Risk Level Selector

Before ANY task, answer these 3 questions:

**Q1: What's the impact if this breaks?**
- [A] Production / Users affected → SAFE MODE
- [B] Dev environment only → MID MODE
- [C] Easy to revert / POC → RISKY MODE

**Q2: How complex is this?**
- [A] Multi-component / New integration → SAFE MODE
- [B] Single feature / Bug fix → MID MODE
- [C] Simple / Well-understood → RISKY MODE

**Q3: How well do we understand the problem?**
- [A] New territory / Unclear requirements → SAFE MODE
- [B] Known domain, some unknowns → MID MODE
- [C] Clear and straightforward → RISKY MODE

**Scoring:**
- Mostly A → SAFE MODE (80% of tasks)
- Mostly B → MID MODE (15% of tasks)
- Mostly C → RISKY MODE (5% of tasks)

---

## Skill Registry

### META PROCESS (How you work)

| Skill | Tier | When to Use |
|-------|------|-------------|
| brainstorming | CRITICAL | Any new feature/idea |
| writing-plans | CRITICAL | After brainstorming, before code |
| verification-before-completion | CRITICAL | Before claiming done |
| receiving-code-review | HIGH | Before any merge |
| subagent-driven-development | HIGH | Multi-task implementation |
| recursive-agent-coordination | HIGH | Multiple agents working together |
| dispatching-parallel-agents | HIGH | 2+ independent tasks |

### FRONTEND

| Skill | Tier | When to Use |
|-------|------|-------------|
| vercel-react-best-practices | HIGH | React/Next.js code |
| web-design-guidelines | HIGH | UI review |
| shadcn-master | MEDIUM | UI component creation |
| framer-motion-best-practices | MEDIUM | Animations |
| performance-optimization | HIGH | Bundle/speed issues |
| nextjs-master | MEDIUM | Next.js specific |

### BACKEND

| Skill | Tier | When to Use |
|-------|------|-------------|
| supabase-expert | HIGH | Database/auth/RLS |
| docker-best-practices | MEDIUM | Containerization |
| security-best-practices | CRITICAL | Any user data/API |

### QUALITY

| Skill | Tier | When to Use |
|-------|------|-------------|
| tdd-master | HIGH | Test-driven implementation |
| systematic-debugging | HIGH | Bug hunting |

### SPECIALTY

| Skill | Tier | When to Use |
|-------|------|-------------|
| browser-use | HIGH | Simple browser automation |
| agent-browser | MEDIUM | Complex browser interactions |
| c4-documentation | LOW | Architecture docs |
| using-git-worktrees | MEDIUM | Isolated branches |
| finishing-a-development-branch | HIGH | Branch completion |

---

## Task → Skill Decision Matrix

### Universal Decision Tree

```
"I have an idea / want to build something new"
  → brainstorming (MUST)
    → writing-plans → [domain skill]

"I need to implement multiple tasks"
  → subagent-driven-development

"Something is broken / not working"
  → systematic-debugging → [relevant domain skill]

"I'm writing code and want to make sure it's good"
  → receiving-code-review

"I'm about to claim something is done"
  → verification-before-completion (MUST)
```

### Domain-Specific

| Task | Invoke |
|------|--------|
| Build React component | vercel-react-best-practices + shadcn-master |
| Optimize performance | performance-optimization |
| Review UI | web-design-guidelines |
| Set up database | supabase-expert |
| Build API endpoint | security-best-practices + tdd-master |
| Containerize app | docker-best-practices |
| Test website | browser-use |
| Complex browser testing | agent-browser |
| Write tests first | tdd-master |
| Debug tricky bug | systematic-debugging |
| Create new skill | opencode-skill-principles |

---

## Workflows

### SAFE MODE Workflow

```
brainstorming → writing-plans → tdd-master → implementation → 
verification → code review → deploy
```

**Required Skills:**
- ✅ brainstorming (must)
- ✅ writing-plans (must)
- ✅ tdd-master (should)
- ✅ verification-before-completion (must)
- ✅ receiving-code-review (must)

### MID MODE Workflow

```
quick plan → implementation → review → ship
```

**Required Skills:**
- ✅ writing-plans (brief)
- ✅ systematic-debugging (if bugs)
- ✅ verification-before-completion (must)
- ✅ receiving-code-review (quick)

### RISKY MODE Workflow

```
JUST DO IT → Ship Fast → Fix Fast
```

⚠️ ONLY for: POCs, experiments, prototypes

**Required Skills:**
- ✅ verification-before-completion (quick check)
- ✅ systematic-debugging (if breaks)

---

## Anti-Patterns (NEVER DO)

### Process Anti-Patterns
- ✗ Never skip brainstorming for "simple" tasks
- ✗ Never claim done without verification
- ✗ Never skip code review
- ✗ Never use RISKY mode for production code
- ✗ Never skip security review for auth/payment

### Code Anti-Patterns
- ✗ Never commit secrets to git
- ✗ Never use eval() with user input
- ✗ Never skip RLS on Supabase
- ✗ Never write empty catch blocks
- ✗ Never use console.log in production

---

## Skills.sh Integration

### One-Command Setup

Install all Vercel agent skills with a single command:

```bash
npx skills add vercel-labs/agent-skills
```

This installs 5 premium skills (100+ rules total):

| Skill | Description | Rules |
|-------|-------------|-------|
| `react-best-practices` | React/Next.js performance optimization | 40+ rules across 8 categories |
| `web-design-guidelines` | Accessibility, UX, and web best practices | 100+ rules |
| `react-native-guidelines` | React Native/Expo performance & patterns | 16 rules |
| `composition-patterns` | React component composition patterns | Patterns |
| `vercel-deploy-claimable` | One-command Vercel deployment | CLI |

### Auto-Update Workflow

To check for and install updates:

```bash
npx skills add vercel-labs/agent-skills --force
```

**Process:**
1. Run the command to fetch latest version
2. Report what will be updated (new skills, changes)
3. **ASK USER for confirmation before applying**
4. Execute update only after human approval

### Browse More Skills

Visit https://skills.sh to discover additional skills from the community.

### Required Skills Location

```
~/.agents/skills/           # Domain skills (from skills.sh)
~/.config/opencode/skills/  # Meta skills
~/.opencode/skills/         # Coordination skills
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  ALWAYS INVOKE                                          │
│  • brainstorming for new features                        │
│  • verification-before-completion before claiming done   │
│  • security-best-practices for auth/data                │
│  • receiving-code-review before merge                   │
├─────────────────────────────────────────────────────────────┤
│  HIGH PRIORITY                                           │
│  • writing-plans after brainstorming                     │
│  • subagent-driven-development for multi-task           │
│  • tdd-master for test-driven work                      │
│  • vercel-react-best-practices for React/Next.js       │
│  • supabase-expert for database                         │
├─────────────────────────────────────────────────────────────┤
│  AS NEEDED                                               │
│  • browser-use for automation                           │
│  • web-design-guidelines for UI                         │
│  • systematic-debugging for bugs                        │
│  • performance-optimization for speed                   │
├─────────────────────────────────────────────────────────────┤
│  SKILLS.SH (run these commands)                          │
│  npx skills add vercel-labs/agent-skills     # Install  │
│  npx skills add vercel-labs/agent-skills --force  # Update│
└─────────────────────────────────────────────────────────────┘
```

---

*APEX OS Bad Boy v8.0 - "Everything you need. Nothing you don't."*
