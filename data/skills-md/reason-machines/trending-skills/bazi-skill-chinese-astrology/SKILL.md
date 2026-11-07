---
name: bazi-skill-chinese-astrology
description: Claude Code skill for 四柱八字 (BaZi) Chinese astrology chart reading and destiny analysis using nine classical texts
triggers:
  - "算八字"
  - "看八字"
  - "批八字"
  - "排八字"
  - "四柱命盘分析"
  - "帮我算命"
  - "bazi chart reading"
  - "chinese astrology analysis"
---

# BaZi Skill — 四柱八字命理分析

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code skill for interactive BaZi (Four Pillars of Destiny) chart calculation and analysis, referencing nine classical Chinese astrology texts. Guides users through birth information collection, produces a complete 四柱 chart, and delivers professional destiny analysis.

## What This Skill Does

- **Interactive information collection** — step-by-step prompts for name, birth date (solar/lunar), birth hour (时辰), gender, and birthplace
- **Chart calculation** — derives Year/Month/Day/Hour pillars (年柱/月柱/日柱/时柱), calculates 大运 (major cycles) and 流年 (annual cycles)
- **Comprehensive analysis** — day master strength (日主强弱), ten gods (十神), five elements balance (五行), pattern determination (格局), career, relationships, health guidance
- **Classical text references** — cross-references nine canonical texts including 《穷通宝典》, 《滴天髓》, 《子平真诠》, and more

## Installation

```bash
# Install to current git project (run from repo root)
mkdir -p .claude/skills
git clone https://github.com/jinchenma94/bazi-skill .claude/skills/bazi

# Install globally (available in all projects)
git clone https://github.com/jinchenma94/bazi-skill ~/.claude/skills/bazi
```

After installation, Claude Code automatically discovers the skill from `.claude/skills/bazi/SKILL.md` or `~/.claude/skills/bazi/SKILL.md`.

## Project Structure

```
bazi-skill/
├── SKILL.md                  # Skill entry point (this file)
├── references/
│   ├── wuxing-tables.md      # Five elements, heavenly stems, earthly branches, ten gods
│   ├── shichen-table.md      # Time period conversion table, daily time calculation
│   ├── dayun-rules.md        # Major cycle forward/reverse rules, starting age calculation
│   └── classical-texts.md    # Core rules from nine classical texts
├── LICENSE
└── README.md
```

## Triggering the Skill

Type any of these in Claude Code to activate:

```
算八字    看八字    批八字    排八字
四柱      命盘      算命      排盘      bazi
```

## Step-by-Step Workflow

When triggered, follow this exact sequence:

### Step 1: Collect Birth Information

Ask the user for these fields **one at a time** (do not ask all at once):

```
1. 姓名 (Name) — optional, for personalization
2. 性别 (Gender) — 男/女, affects 大运 direction
3. 出生日期 (Birth date) — ask whether 阳历 (solar) or 农历 (lunar)
4. 出生时辰 (Birth hour) — see shichen-table.md for conversion
5. 出生地点 (Birthplace) — province/city for timezone adjustment
```

### Step 2: Convert to Four Pillars

Reference `references/wuxing-tables.md` for all lookup tables.

**Year Pillar (年柱):**
```
Year stem index  = (year - 4) mod 10  → maps to 天干
Year branch index = (year - 4) mod 12  → maps to 地支
```

**Month Pillar (月柱):**
```
Month branch is fixed by solar term (节气), not calendar month.
Month stem is derived from year stem using the 五虎遁年起月法 table.
```

**Day Pillar (日柱):**
```
Use pre-calculated 万年历 (perpetual calendar) lookup.
Day stem/branch cycle repeats every 60 days (六十甲子).
```

**Hour Pillar (时柱):**
```
Convert clock time → 时辰 (see shichen-table.md)
Hour stem derived from day stem using 五鼠遁日起时法 table.
```

### Step 3: Identify Day Master (日主)

The Day Pillar's Heavenly Stem is the Day Master — the central reference point for all analysis.

```
Example: 日柱 = 甲子
Day Master = 甲 (Wood, Yang)
```

### Step 4: Calculate 大运 (Major Cycles)

Reference `references/dayun-rules.md`:

```
Male + Yang year stem  → Forward (顺排)
Male + Yin year stem   → Reverse (逆排)
Female + Yang year stem → Reverse (逆排)
Female + Yin year stem  → Forward (顺排)

Starting age = days to next/previous 节气 ÷ 3 (round to nearest integer)
Each 大运 lasts 10 years.
```

### Step 5: Determine Ten Gods (十神)

Cross-reference Day Master against each pillar stem using the 十神 table in `references/wuxing-tables.md`:

| Relationship | Same element, same polarity | Same element, opposite polarity |
|---|---|---|
| Self | 比肩 | 劫财 |
| Element I produce | 食神 | 伤官 |
| Element that produces me | 正印 | 偏印 |
| Element I control | 正财 | 偏财 |
| Element that controls me | 正官 | 七杀 |

### Step 6: Assess Five Elements Balance (五行平衡)

```
Count Wood/Fire/Earth/Metal/Water across all 8 characters (stems + branches).
Note hidden stems (藏干) in branches — include these in element count.
Identify excess and deficiency.
```

### Step 7: Determine Pattern (格局)

Reference `references/classical-texts.md` — 《子平真诠》 and 《三命通会》 sections:

```
普通格局 (Common patterns): 正官格, 七杀格, 正印格, 偏印格,
                            食神格, 伤官格, 正财格, 偏财格
特殊格局 (Special patterns): 从格, 化格, 专旺格, etc.

Month branch hidden stem often determines the primary pattern.
```

### Step 8: Full Analysis Output

Structure your analysis report as follows:

```markdown
## 八字命盘 | BaZi Chart

**姓名**: [Name]  **性别**: [Gender]  **出生**: [Date Time]

| 柱  | 天干 | 地支 |
|-----|------|------|
| 年柱 | X   | X   |
| 月柱 | X   | X   |
| 日柱 | X   | X   |
| 时柱 | X   | X   |

**日主**: X（X行，X）

---

## 大运排列

起运年龄: X岁（约 XXXX 年起）

| 序 | 大运 | 年份 | 十神 |
|----|------|------|------|
| 1  | XX  | XXXX–XXXX | XX |
...

---

## 命理分析

### 日主强弱
[Assessment of day master strength based on seasonal support, roots, and helpers]

### 五行分析
[Element count and balance assessment]

### 格局判定
[Pattern name and explanation, citing classical text]

### 十神解读
[Key ten god relationships and their implications]

### 大运流年
[Current and upcoming major/annual cycle analysis]

### 综合建议
**事业**: [Career guidance]
**感情**: [Relationship guidance]  
**健康**: [Health guidance]
**择吉**: [Auspicious timing suggestions]

---
*参考典籍: 《穷通宝典》《三命通会》《滴天髓》《渊海子平》《千里命稿》*
*免责声明: 仅供传统文化学习与娱乐参考，不构成任何决策依据。*
```

## Key Reference Tables

### 天干 Heavenly Stems
```
甲(Wood+) 乙(Wood-) 丙(Fire+) 丁(Fire-) 戊(Earth+)
己(Earth-) 庚(Metal+) 辛(Metal-) 壬(Water+) 癸(Water-)
```

### 地支 Earthly Branches
```
子(Water+/Rat)  丑(Earth-/Ox)   寅(Wood+/Tiger) 卯(Wood-/Rabbit)
辰(Earth+/Dragon) 巳(Fire-/Snake) 午(Fire+/Horse) 未(Earth-/Goat)
申(Metal+/Monkey) 酉(Metal-/Rooster) 戌(Earth+/Dog) 亥(Water-/Pig)
```

### 五虎遁年起月法 (Month Stem from Year Stem)
```
Year stem 甲/己 → January stem starts at 丙
Year stem 乙/庚 → January stem starts at 戊
Year stem 丙/辛 → January stem starts at 庚
Year stem 丁/壬 → January stem starts at 壬
Year stem 戊/癸 → January stem starts at 甲
```

### 五鼠遁日起时法 (Hour Stem from Day Stem)
```
Day stem 甲/己 → 子时 stem = 甲
Day stem 乙/庚 → 子时 stem = 丙
Day stem 丙/辛 → 子时 stem = 戊
Day stem 丁/壬 → 子时 stem = 庚
Day stem 戊/癸 → 子时 stem = 壬
```

## Classical Texts Quick Reference

| 典籍 | Primary Use |
|------|-------------|
| 《穷通宝典》| Day master seasonal adjustment (调候) |
| 《三命通会》| Pattern and spirit star (格局神煞) analysis |
| 《滴天髓》 | Five element strength and flow (五行旺衰) |
| 《渊海子平》| Ten gods and six relations (十神六亲) |
| 《千里命稿》| Case study verification (命例实证) |
| 《协纪辨方书》| Auspicious date selection (择日神煞) |
| 《果老星宗》| Star and fate combined reading (星命合参) |
| 《子平真诠》| Use god and pattern (用神格局) |
| 《神峰通考》| Correcting common errors (命理辨误) |

Full excerpts and rules are in `references/classical-texts.md`.

## Common Patterns & Troubleshooting

### Lunar to Solar Date Conversion
- Always confirm whether user provides 阳历 (Gregorian) or 农历 (lunar)
- Use 万年历 lookup for lunar→solar conversion before calculating pillars
- Intercalary months (闰月) require special handling

### Solar Term (节气) Boundaries
- Month pillar changes at 节 (first solar term of month), NOT at month start
- Critical for people born near the 1st–8th of a month
- When uncertain, inform user their month pillar may differ by one month

### Timezone Adjustment
- Standard Chinese charts use Beijing time (UTC+8)
- Users born outside China: convert local birth time to Beijing time
- Some practitioners use true solar time (真太阳时) — note if applying this

### Day Master Strength Assessment Checklist
```
✓ Is the birth season supportive? (得令)
✓ Does the day branch support the day master? (得地)  
✓ Do other stems help the day master? (得助)
Strong (身强) if 2+ conditions met; Weak (身弱) if 0–1 conditions met.
```

### Missing Information Handling
- If user cannot provide exact birth time: analyze without hour pillar, note limitation
- If only year/month known: provide partial analysis with appropriate caveats
- Never fabricate birth data — always ask for clarification

## Example Interaction

```
User: 帮我算八字

Claude: 好的，我来为您排八字！请问您的性别是？

User: 女

Claude: 好的。请问您的出生日期是阳历还是农历？

User: 阳历，1990年3月15日

Claude: 明白了。请问您出生的时辰或具体时间？

User: 早上8点半

Claude: 早上8点半是辰时（07:00–09:00）。请问出生地点？

User: 上海

Claude: [Proceeds to calculate pillars, 大运, and full analysis]
```

## Disclaimer

本 Skill 仅供传统文化学习与娱乐参考，分析结果不构成任何医疗、法律、财务或人生重大决策依据。命理学属于传统文化范畴，请理性看待。
