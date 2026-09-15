---
name: inkos-multi-agent-novel-writing
description: Multi-agent CLI system for autonomous novel writing, auditing, and revision with human review gates
triggers:
  - write novel with AI agents
  - autonomous novel production
  - inkos novel writing
  - multi-agent creative writing
  - AI novel audit and revision
  - automated chapter writing TypeScript
  - inkos CLI novel agent
  - novel writing pipeline with review gates
---

# InkOS Multi-Agent Novel Writing

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

InkOS is a multi-agent CLI system that autonomously writes, audits, and revises novels. Agents handle the full pipeline: Writer → Validator → Auditor → Reviser, with human review gates at configurable checkpoints.

## Installation

```bash
npm install -g @actalk/inkos
# or run directly
npx @actalk/inkos --version
```

**Requirements:** Node.js ≥ 20.0.0

## Quick Start

```bash
# Create a new novel project
inkos book create --title "吞天魔帝" --genre xuanhuan

# Write the next chapter
inkos write next 吞天魔帝

# Audit a specific chapter
inkos audit 吞天魔帝 --chapter 3

# Run the full daemon (continuous production)
inkos daemon start
```

## Project Structure

After `inkos book create`, the project directory contains:

```
story/
  outline.md              # Story outline (architect agent input)
  book_rules.md           # Per-book custom rules and audit dimensions
  chapter_summaries.md    # Auto-generated per-chapter summaries
  subplot_board.md        # Subplot progress tracking (A/B/C lines)
  emotional_arcs.md       # Per-character emotional arc tracking
  character_matrix.md     # Character interaction matrix + info boundaries
  parent_canon.md         # Spinoff only: imported canon constraints
  style_profile.json      # Style fingerprint (if style import used)
  style_guide.md          # LLM-generated qualitative style guide
  chapters/
    ch001.md
    ch002.md
    ...
```

## Core Commands

### Book Management

```bash
inkos book create --title "Title" --genre xuanhuan  # genres: xuanhuan | xianxia | dushi | horror | general
inkos book list
inkos book status 吞天魔帝
```

### Writing Pipeline

```bash
inkos write next 吞天魔帝           # Write next chapter (auto-loads all context)
inkos write chapter 吞天魔帝 5      # Write specific chapter
inkos audit 吞天魔帝 --chapter 3    # Audit chapter (33 dimensions)
inkos revise 吞天魔帝 --chapter 3   # Revise based on audit results
inkos revise 吞天魔帝 --chapter 3 --mode spot-fix   # Point fix only (default)
inkos revise 吞天魔帝 --chapter 3 --mode rewrite    # Full rewrite (use cautiously)
inkos revise 吞天魔帝 --chapter 3 --mode polish     # Polish (no structural changes)
```

### Genre System

```bash
inkos genre list                        # List all built-in genres
inkos genre show xuanhuan               # View full rules for a genre
inkos genre copy xuanhuan               # Copy genre rules to project for customization
inkos genre create wuxia --name 武侠     # Create new genre from scratch
```

### Style Matching

```bash
inkos style analyze reference.txt               # Analyze style fingerprint
inkos style import reference.txt 吞天魔帝        # Import style into book
inkos style import reference.txt 吞天魔帝 --name "某作者"
```

### Spinoff (Prequel/Sequel/IF-branch)

```bash
inkos book create --title "烈焰前传" --genre xuanhuan
inkos import canon 烈焰前传 --from 吞天魔帝       # Import parent canon constraints
inkos write next 烈焰前传                         # Writer auto-reads canon constraints
```

### AIGC Detection

```bash
inkos detect 吞天魔帝 --chapter 3     # Detect AIGC markers in chapter
inkos detect 吞天魔帝 --all           # Detect all chapters
inkos detect --stats                  # View detection history statistics
```

### Daemon (Continuous Production)

```bash
inkos daemon start                    # Start scheduler (default: 15 min/cycle)
inkos daemon stop
inkos daemon status
```

## Configuration

### Global Config (`~/.inkos/config.json`)

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4o",
    "apiKey": "sk-...",
    "temperature": 0.8
  },
  "daemon": {
    "intervalMinutes": 15,
    "dailyChapterLimit": 10,
    "parallelBooks": 2
  },
  "webhook": {
    "url": "https://your-server.com/hooks/inkos",
    "secret": "your-hmac-secret",
    "events": ["chapter-complete", "audit-failed", "pipeline-error"]
  },
  "aigcDetection": {
    "provider": "gptzero",
    "apiKey": "...",
    "endpoint": "https://api.gptzero.me/v2/predict/text"
  }
}
```

### Per-Book Rules (`story/book_rules.md`)

````markdown
# Book Rules: 吞天魔帝

## 禁忌 (Forbidden)
- 主角不得主动求饶
- 不得出现「命运」「天意」等宿命论表述

## 高疲劳词
- 震撼, 惊骇, 恐惧, 颤抖

## additionalAuditDimensions
- 数值系统一致性: 战力数值不得前后矛盾
- 角色成长节奏: 主角突破间隔不少于3章

## 写手特别指令
- 战斗场面优先感官描写，禁止数值报告
````

## Agent Architecture

InkOS runs five specialized agents in sequence:

```
ArchitectAgent  →  outline.md, book_rules.md
     ↓
WriterAgent     →  ch00N.md (reads: outline, summaries, arcs, matrix, style_guide, canon)
     ↓
ValidatorAgent  →  11 deterministic rules, zero LLM cost
     ↓  (error found → trigger spot-fix immediately)
AuditorAgent    →  33 LLM dimensions, temperature=0 for consistency
     ↓
ReviserAgent    →  spot-fix | rewrite | polish | anti-detect
```

### Post-Write Validator Rules (Deterministic, No LLM)

| Rule | Condition |
|------|-----------|
| Forbidden patterns | `不是……而是……` constructs |
| Em-dash ban | `——` character |
| Transition word density | 仿佛/忽然/竟然≤1 per 3000 chars |
| High-fatigue words | Per-book list, ≤1 per chapter |
| Meta-narrative | Screenwriter-style narration |
| Report terminology | Analytical framework terms in prose |
| Author moralizing | 显然/不言而喻 etc. |
| Collective reaction | 「全场震惊」clichés |
| Consecutive 了 | ≥4 consecutive sentences with 了 |
| Paragraph length | ≥2 paragraphs over 300 chars |
| Book-specific bans | `book_rules.md` forbidden list |

### Audit Dimensions (33 total, LLM-evaluated)

Key dimensions include:
- Dims 1–23: Core narrative quality (plot, character, pacing, foreshadowing)
- Dim 24–26: Subplot stagnation, arc flatness, rhythm monotony (all 5 genres)
- Dim 27: Sensitive content
- Dim 28–31: Spinoff-specific (canon conflicts, future info leakage, world rule consistency, foreshadowing isolation)
- Dim 32: Reader expectation management
- Dim 33: Outline deviation detection

## Code Integration Examples

### Programmatic Usage (TypeScript)

```typescript
import { BookManager } from '@actalk/inkos'
import { WriterAgent } from '@actalk/inkos/agents'
import { ValidatorAgent } from '@actalk/inkos/agents'

// Create and configure a book
const manager = new BookManager()
const book = await manager.createBook({
  title: '吞天魔帝',
  genre: 'xuanhuan',
  outlinePath: './my-outline.md'
})

// Run the write pipeline for next chapter
const writer = new WriterAgent({ temperature: 0.8 })
const chapter = await writer.writeNext(book)

// Run deterministic validation (no LLM cost)
const validator = new ValidatorAgent()
const validationResult = await validator.validate(chapter, book)

if (validationResult.hasErrors) {
  // Auto spot-fix triggered
  const reviser = new ReviserAgent({ mode: 'spot-fix' })
  const fixed = await reviser.revise(chapter, validationResult.errors, book)
  console.log('Fixed violations:', validationResult.errors.length)
}
```

### Webhook Handler (Express)

```typescript
import express from 'express'
import crypto from 'crypto'

const app = express()
app.use(express.raw({ type: 'application/json' }))

app.post('/hooks/inkos', (req, res) => {
  const sig = req.headers['x-inkos-signature'] as string
  const expected = crypto
    .createHmac('sha256', process.env.INKOS_WEBHOOK_SECRET!)
    .update(req.body)
    .digest('hex')

  if (sig !== `sha256=${expected}`) {
    return res.status(401).send('Invalid signature')
  }

  const event = JSON.parse(req.body.toString())

  switch (event.type) {
    case 'chapter-complete':
      console.log(`Chapter ${event.chapter} of "${event.book}" complete`)
      // Trigger human review gate
      notifyReviewer(event)
      break
    case 'audit-failed':
      console.log(`Audit failed: ${event.criticalCount} critical issues`)
      break
    case 'pipeline-error':
      console.error(`Pipeline error in "${event.book}":`, event.error)
      break
  }

  res.status(200).json({ received: true })
})
```

### Custom Genre Definition

```typescript
// genres/wuxia.ts
import type { GenreConfig } from '@actalk/inkos/types'

export const wuxia: GenreConfig = {
  id: 'wuxia',
  name: '武侠',
  chapterTypes: ['江湖相遇', '武功切磋', '恩怨纠葛', '门派争斗', '武林大会'],
  forbiddenPatterns: [
    '内力值', '战力', '等级提升',   // No numerical power system
    '系统', '面板', '属性点'
  ],
  fatiguedWords: ['震惊', '无敌', '碾压', '秒杀'],
  languageRules: [
    {
      bad: '内力增加了100点',
      good: '一股暖流沿经脉漫开，指尖的颤抖渐渐平息'
    }
  ],
  auditDimensions: [
    '武功描写感官化',
    '江湖规则内部一致性',
    '恩怨情仇弧线完整性'
  ]
}
```

### Style Import Pipeline

```typescript
import { StyleAnalyzer } from '@actalk/inkos/style'

const analyzer = new StyleAnalyzer()

// Analyze reference text
const profile = await analyzer.analyze('./reference-novel.txt')
console.log(profile)
// {
//   avgSentenceLength: 18.3,
//   ttr: 0.42,           // Type-Token Ratio
//   rhetoricalDensity: 0.15,
//   paragraphLengthDist: { p25: 45, p50: 89, p75: 156 },
//   punctuationStyle: 'sparse'
// }

// Import into book (generates style_profile.json + style_guide.md)
await analyzer.importToBook('./reference-novel.txt', '吞天魔帝', {
  authorName: '某作者'
})
```

## Audit Revision Loop

The v0.4 hardened audit-revision loop prevents revision from introducing more AI markers:

```
AuditorAgent (temp=0)
     ↓ critical issues found
ReviserAgent spot-fix
     ↓
AI marker count comparison
     ↓ markers increased?
  YES → discard revision, keep original
  NO  → accept revision
     ↓
Re-audit (temp=0)
```

**Key settings for audit consistency:**
- Auditor always runs at `temperature: 0` — eliminates 0–6 critical variance on same chapter
- Default revision mode is `spot-fix` (only modify problem sentences)
- `rewrite` mode is available but measured to introduce 6× more AI markers
- `polish` mode is boundary-locked: no paragraph add/delete, no name changes, no new plot

## Spinoff Canon Constraints

When `parent_canon.md` is detected, 4 additional audit dimensions activate automatically:

```markdown
# parent_canon.md (auto-generated by `inkos import canon`)

## 正传世界规则
- 力量体系: 炼体→炼气→炼丹→炼神→炼虚
- 地理: 九州大陆，东海以东无人居住
- 阵营: 正道五宗 vs 魔道三门

## 关键事件时间线
- 第1章: 主角获得吞天诀
- 第45章: 正道五宗盟约成立 [分歧点]

## 角色快照 (分歧点时状态)
- 林天: 炼气期第三层，未知父母身世
- 剑宗宗主: 在世，尚未叛变

## 伏笔状态 (正传专属，番外禁止回收)
- 古剑残片: 未解
- 神秘老人身份: 未解
```

## Troubleshooting

**Validator fires on every chapter**
Check `book_rules.md` fatigue word list — words listed there are enforced ≤1 per chapter. Remove infrequently used terms.

**Audit results wildly inconsistent between runs**
Confirm auditor temperature is locked to 0 in config. If using a proxy LLM API, ensure it respects `temperature: 0`.

**Revision introduces more AI markers than original**
This is expected behavior — InkOS v0.4 automatically detects this and discards the revision. If it happens repeatedly, switch from `rewrite` to `spot-fix` mode explicitly.

**Spinoff audit incorrectly flags events**
Verify `parent_canon.md` has accurate divergence point timestamps. Events before the divergence point are canon-locked; events after are fair game for the spinoff.

**Daemon stops a book after repeated failures**
Check `daemon status` for the suspended book. After fixing the underlying issue (usually outline ambiguity or `book_rules.md` contradiction), run `inkos daemon resume 书名`.

**Style guide not being applied by writer**
Run `inkos style import` again — if `style_guide.md` is missing or empty, the writer skips style injection silently. Check that the reference text is ≥5000 characters for reliable fingerprinting.
