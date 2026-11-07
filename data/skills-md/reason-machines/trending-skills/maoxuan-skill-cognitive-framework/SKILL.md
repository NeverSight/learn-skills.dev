---
name: maoxuan-skill-cognitive-framework
description: Install and use the 毛选.skill cognitive framework for Claude Code — applies Mao Zedong's strategic mental models (contradiction analysis, protracted war, rural encirclement, united front) to help analyze problems, devise strategies, and cut through complexity.
triggers:
  - "add maoxuan skill"
  - "install 毛选 skill"
  - "use maoxuan cognitive framework"
  - "analyze with mao's mental models"
  - "apply contradiction analysis"
  - "use 教员 framework"
  - "maoxuan strategic thinking"
  - "install leezythu maoxuan"
---

# 毛选.skill — Mao's Cognitive Framework for Strategic Analysis

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code skill that distills the core mental models from 《毛泽东选集》 (Selected Works of Mao Zedong) into an operational cognitive framework. Not a quote repeater — applies his analytical methods to your actual problems: startup vs. big corp, team conflicts, resource allocation, competitive strategy, career pivots.

**7 core mental models · 10 decision heuristics · Full expression DNA**

---

## Installation

```bash
# Install via skills CLI
npx skills add leezythu/maoxuan-skill

# Or clone directly
git clone https://github.com/leezythu/maoxuan-skill.git
```

After installation, trigger in Claude Code with any of:

```
毛选
教员
用毛选的方式分析
从毛选的角度
教员怎么看
用毛选框架
```

---

## What the Skill Does

The skill loads `SKILL.md` into your AI agent's context, giving it:

1. **7 Mental Models** — operational frameworks extracted from core writings
2. **10 Decision Heuristics** — concrete rules for ambiguous situations
3. **Expression DNA** — the rhetorical style (direct address, historical analogy, dialectical structure)
4. **Honest Boundaries** — what it can and cannot do

The agent does NOT roleplay as Mao. It uses his analytical frameworks to examine your problem.

---

## Repository Structure

```
maoxuan-skill/
├── SKILL.md                          # Core skill file loaded by agent
├── README.md
├── LICENSE                           # MIT
└── references/
    └── research/
        ├── 01-core-writings.md       # Distilled core texts
        ├── 02-strategic-thinking.md  # Strategic thinking analysis
        ├── 03-expression-dna.md      # Expression style DNA
        ├── 04-external-views.md      # External perspectives
        ├── 05-decisions.md           # Key decision analysis
        └── 06-timeline.md            # Timeline reference
```

---

## The 7 Core Mental Models

### 1. 矛盾分析法 — Contradiction Analysis
**Source:** 《矛盾论》 (On Contradiction)

Find the **principal contradiction** among all contradictions. Resolving it moves everything else.

```
Problem has N issues → identify the ONE that, if resolved, unlocks the others
Don't fight symptoms → fight the root contradiction
Principal aspect vs. secondary aspect within each contradiction
```

**Application pattern:**
```
User problem → List all tensions/conflicts
              → Identify principal contradiction (usually ≠ stated problem)
              → Focus all resources on principal contradiction
              → Secondary contradictions resolve or become manageable
```

### 2. 实践认识循环 — Practice-Cognition Loop
**Source:** 《实践论》 (On Practice)

```
没有调查就没有发言权
No investigation, no right to speak.

Loop: Practice → Perception → Conception → Practice (verify) → repeat
```

**Application pattern:**
```
Don't theorize without data → go investigate first
Hypothesis → smallest possible test → update model → next test
Never skip the "go talk to real users/customers" step
```

### 3. 持久战略 — Protracted War Strategy
**Source:** 《论持久战》 (On Protracted War)

Three phases when you're the weaker party:
```
Phase 1: Strategic defensive — preserve strength, avoid decisive battles you'll lose
Phase 2: Strategic stalemate — attrit the enemy, build your base
Phase 3: Strategic offensive — counterattack from position of strength
```

**Application pattern:**
```
Early startup: don't fight big corp head-on (Phase 1)
Growing startup: find your niche, deepen it, build defensible moat (Phase 2)
Established player: expand from stronghold (Phase 3)
```

### 4. 农村包围城市 — Rural Encirclement of Cities
**Source:** 《星星之火，可以燎原》 (A Single Spark Can Start a Prairie Fire)

```
Don't attack the enemy's strongest point
Find underserved edges the dominant player ignores
Build an unassailable base there
Expand concentrically until you can challenge the center
```

**Application pattern:**
```
Big corp's weakness: can't focus deeply on any single niche
Your advantage: you can go 10x deeper in ONE narrow segment
Win that segment completely → expand to adjacent segment → repeat
```

### 5. 统一战线 — United Front
**Source:** 《中国社会各阶级的分析》

```
把朋友搞得多多的，把敌人搞得少少的
Maximize allies, minimize enemies.

Distinguish: Who is the real enemy? Who is a potential ally even if uncomfortable?
Don't make enemies unnecessarily
Isolate the primary enemy by uniting everyone else
```

**Application pattern:**
```
Team conflict → reframe: shared enemy = market/competition
               → both factions are allies against the real enemy
               → 团结—批评—团结 (Unity → Criticism → Unity)
```

### 6. 群众路线 — Mass Line
**Source:** 《关于领导方法的若干问题》

```
从群众中来，到群众中去
From the masses, to the masses.

Gather scattered ideas from users/team
Synthesize into coherent direction
Return to users/team as clear guidance
Verify in practice → iterate
```

**Application pattern:**
```
Product decisions: talk to 20 users → find patterns → build → ship → repeat
Management: don't dictate → listen → synthesize → align → execute
```

### 7. 纸老虎论 — Paper Tiger Theory

```
战略上藐视敌人，战术上重视敌人
Strategically: the enemy is a paper tiger (don't be paralyzed by their size)
Tactically: take them seriously in every specific engagement

Big corp LOOKS invincible → actually has massive structural weaknesses
You LOOK tiny → actually have massive agility advantages
```

---

## 10 Decision Heuristics

| Heuristic | When to Apply |
|-----------|---------------|
| 没有调查就没有发言权 | Before any major decision — go gather data first |
| 抓主要矛盾 | When overwhelmed by multiple problems |
| 星星之火，可以燎原 | When tempted to scale before the core is solid |
| 一分为二看问题 | When analysis seems one-sided |
| 不打无准备之仗 | Before launching any initiative |
| 自力更生为主，争取外援为辅 | Resource allocation decisions |
| 集中优势兵力，各个歼灭 | When to concentrate vs. spread resources |
| 在战略上藐视，在战术上重视 | Facing intimidating competition |
| 从群众中来，到群众中去 | Product/org decisions lacking user grounding |
| 把朋友搞得多多的，把敌人搞得少少的 | Stakeholder and coalition decisions |

---

## Usage Patterns

### Pattern 1: Competitive Strategy Analysis

```
Trigger: 毛选

Problem: We're a 10-person startup. Google just shipped a product 
         that does what we do.

Framework applied:
→ 纸老虎论: Google's size = paper tiger. They have 1000 priorities. 
             You have 1.
→ 农村包围城市: Don't fight Google's product. Find the vertical 
                they'll never care about. Go 10x deeper there.
→ 持久战略 Phase 1: Don't go head-to-head. Survive, build base.
→ 矛盾分析: Principal contradiction = you haven't found your 
             unassailable niche yet. That's the ONE thing to solve.
```

### Pattern 2: Team Conflict Resolution

```
Trigger: 教员怎么看

Problem: Two tech leads hate each other. Team is split. 
         Shipping has stopped.

Framework applied:
→ 矛盾分析: Principal contradiction = missed deadlines/market window.
             Their conflict = secondary contradiction.
→ 统一战线: They are NOT enemies of each other. Market is the enemy.
             Unite them against the real enemy.
→ 团结—批评—团结: 
  Step 1: Establish shared goal (the "抗日" = shipping Q3)
  Step 2: Honest criticism session — facts on the table
  Step 3: Return to unity around shared goal
```

### Pattern 3: Career/Pivot Decisions

```
Trigger: 用毛选的方式分析

Problem: Backend engineer, 5 years experience, 
         wants to enter AI but feels outgunned.

Framework applied:
→ 纸老虎论: "AI market is saturated" = paper tiger. 
             Most people are doing surface-level work.
→ 根据地思维: Your backend experience IS your base. 
               AI engineers don't have it.
→ 实践认识循环: Before strategizing — investigate. 
                 What are the actual bottlenecks to AI adoption 
                 in your industry? (hint: usually not the model)
→ 农村包围城市: Don't compete on algorithms. 
                 Own the "AI + [your industry]" niche.
```

### Pattern 4: Resource Allocation

```
Trigger: 毛选

Problem: 3 possible product directions, resources for 1.

Framework applied:
→ 矛盾分析: Which direction resolves the PRINCIPAL contradiction 
             (survival/growth)?
→ 集中优势兵力: Don't spread. Concentrate everything on ONE.
→ 持久战略: Which direction gives you a defensible base 
             to expand from later?
→ 没有调查就没有发言权: Have you actually talked to users 
                          in each direction? Do that first.
```

---

## Expression Style (What the Skill Sounds Like)

The framework uses a distinctive rhetorical structure:

```
1. Direct address: "同志" / "你这个问题..."
2. Historical grounding: brief concrete analogy (not lecture)
3. Problem reframe: "你以为主要矛盾是X，其实是Y"
4. Framework application: named model + your specific situation
5. Concrete next action: specific, not vague
6. Closing formulation: aphorism tied to the analysis
```

**It does NOT:**
- Lecture on history at length
- Repeat quotes without applying them
- Give generic motivational content
- Avoid naming the hard thing

---

## Skill Compatibility

| Agent | Compatible |
|-------|-----------|
| Claude Code | ✅ Primary target |
| Cursor | ✅ via SKILL.md in context |
| Codex | ✅ |
| skills.sh | ✅ |

```bash
# Verify skill is loaded
npx skills list
# Should show: maoxuan-skill-cognitive-framework
```

---

## Honest Boundaries

**What the skill can do:**
- Apply contradiction analysis to decompose complex problems
- Use protracted war / rural encirclement for competitive strategy
- Apply mass line thinking to product and org decisions
- Use united front logic for stakeholder/coalition mapping
- Provide dialectical (一分为二) analysis that avoids one-sidedness

**What it cannot do:**

| Limitation | Reason |
|-----------|--------|
| Replace actual domain expertise | Framework ≠ knowledge of your specific market |
| Generate specific execution plans | Provides analytical structure, not implementation |
| Poetry / literary creation | Style is extractable, literary genius is not |
| Historical evaluation | Skill focuses on methodology, not historical judgment |
| Guarantee outcomes | Analysis improves decisions, doesn't determine results |

---

## Why This Framework for Technical/Startup Problems

Most business frameworks assume you have resources. This one was built for the opposite:

| Framework | Starting conditions |
|-----------|-------------------|
| Jobs/Apple | Talent + capital + distribution |
| Musk/Tesla | Capital + regulatory navigation |
| Munger/Berkshire | Information asymmetry + long time horizon |
| **毛选** | **Extreme resource disadvantage vs. vastly stronger opponent** |

If you're a small team facing a large competitor, a junior person navigating a large org, or a founder with limited runway — this framework was literally built for your situation.

---

## Contributing

```bash
git clone https://github.com/leezythu/maoxuan-skill.git
cd maoxuan-skill

# Core skill file
vim SKILL.md

# Research references
vim references/research/01-core-writings.md
```

PRs welcome for: additional mental model documentation, new application patterns, corrections to framework distillation.

---

## License

MIT — use freely, modify freely, build on it freely.

---

*语录告诉你他说过什么。毛选.skill 帮你用他的方式看你的问题。*

*星星之火，可以燎原。*
