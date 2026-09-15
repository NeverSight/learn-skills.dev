---
name: taiwan-md-knowledge-base
description: AI-native open knowledge base about Taiwan built with Astro v5, featuring bilingual content (zh-TW/en), D3.js knowledge graph, and structured Markdown SSOT architecture.
triggers:
  - "add content to taiwan.md"
  - "contribute to taiwan knowledge base"
  - "add a new article about Taiwan"
  - "set up taiwan-md locally"
  - "add bilingual article to taiwan.md"
  - "create knowledge graph node for taiwan"
  - "translate taiwan article to English"
  - "add new category to taiwan.md"
---

# Taiwan.md Knowledge Base

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Taiwan.md is an open-source, AI-native knowledge base about Taiwan built with Astro v5. It uses a Single Source of Truth (SSOT) architecture where all content lives in the `knowledge/` directory as Markdown files, and the website is a build-time projection. Features include bilingual support (Traditional Chinese as default + English), an interactive D3.js knowledge graph, and 96+ curated articles across 12 categories.

---

## Installation & Setup

### Prerequisites
- Node.js 18+
- npm or pnpm

### Clone and Install

```bash
git clone https://github.com/frank890417/taiwan-md.git
cd taiwan-md
npm install
```

### Development Server

```bash
npm run dev
# Site available at http://localhost:4321
```

### Build & Preview

```bash
npm run build
npm run preview
```

### Sync Knowledge to Content

```bash
bash scripts/sync.sh
# Copies knowledge/ → src/content/ for Astro build
```

---

## Project Architecture

```
taiwan-md/
├── knowledge/               ← SSOT: ALL content lives here
│   ├── History/             ← Chinese articles + _Hub.md
│   ├── Geography/
│   ├── Culture/
│   ├── Food/
│   ├── Art/
│   ├── Music/
│   ├── Technology/
│   ├── Nature/
│   ├── People/
│   ├── Society/
│   ├── Economy/
│   ├── Lifestyle/
│   ├── About/               ← Meta content
│   └── en/                  ← English translations (mirrors zh-TW)
│       ├── History/
│       ├── Geography/
│       └── ...
├── scripts/
│   └── sync.sh              ← Syncs knowledge/ → src/content/
├── src/
│   ├── pages/               ← Astro pages
│   ├── layouts/             ← Shared layouts
│   └── content/             ← Build-time projection (DO NOT EDIT)
├── public/
│   └── images/wiki/         ← Cached Wikimedia Commons images
└── docs/                    ← Architecture & roadmap docs
```

**Critical rule:** Never edit files in `src/content/` directly. Always edit `knowledge/` and run `scripts/sync.sh`.

---

## Content Structure

### The 12 Categories

| Slug | Chinese | English |
|------|---------|---------|
| `history` | 歷史 | History |
| `geography` | 地理 | Geography |
| `culture` | 文化 | Culture |
| `food` | 美食 | Food |
| `art` | 藝術 | Art |
| `music` | 音樂 | Music |
| `technology` | 科技 | Technology |
| `nature` | 自然 | Nature |
| `people` | 人物 | People |
| `society` | 社會 | Society |
| `economy` | 經濟 | Economy |
| `lifestyle` | 生活 | Lifestyle |

### Article File Naming

```
knowledge/
├── Food/
│   ├── _Hub.md              ← Category hub page (literary overview)
│   ├── bubble-tea.md        ← Individual article (zh-TW)
│   └── beef-noodle.md
└── en/
    └── Food/
        ├── _Hub.md          ← English hub page
        ├── bubble-tea.md    ← English translation
        └── beef-noodle.md
```

---

## Writing Articles

### Chinese Article Template (`knowledge/[Category]/article-slug.md`)

```markdown
---
title: 珍珠奶茶
description: 台灣最具代表性的飲料文化，從夜市攤車到全球連鎖，珍珠奶茶如何征服世界。
category: food
date: 2024-01-15
tags: [飲食文化, 台灣之光, 夜市]
image: /images/wiki/bubble-tea-abc123.jpg
imageCaption: 台灣珍珠奶茶 | Wikimedia Commons | CC BY-SA 4.0
sources:
  - title: 珍珠奶茶的起源考證
    url: https://example.com/boba-origin
  - title: 台灣飲料市場報告
    url: https://example.com/beverage-report
---

## 30 秒認識

珍珠奶茶（波霸奶茶）誕生於 1980 年代台灣，現已成為全球年產值超過 30 億美元的飲料產業。

## 深度閱讀

### 起源爭議

台南翰林茶館與台中春水堂都聲稱是珍珠奶茶的發明者...

### 全球擴張

2010 年代，珍珠奶茶席捲歐美亞各大城市...

## 為什麼重要

珍珠奶茶不只是一杯飲料，它是台灣軟實力的最佳代言人——在沒有邦交的地方，台灣味道先到了。

## 參考資料

- [珍珠奶茶的起源考證](https://example.com/boba-origin)
- [台灣飲料市場報告](https://example.com/beverage-report)
```

### English Article Template (`knowledge/en/[Category]/article-slug.md`)

```markdown
---
title: Bubble Tea
description: Taiwan's most iconic beverage culture — how boba conquered the world from night market stalls to global chains.
category: food
date: 2024-01-15
tags: [food culture, taiwan pride, night market]
image: /images/wiki/bubble-tea-abc123.jpg
imageCaption: Taiwanese Bubble Tea | Wikimedia Commons | CC BY-SA 4.0
sources:
  - title: Origins of Bubble Tea
    url: https://example.com/boba-origin
  - title: Taiwan Beverage Market Report
    url: https://example.com/beverage-report
---

## 30-Second Overview

Bubble tea (boba) was born in 1980s Taiwan and has grown into a global industry worth over $3 billion annually.

## Deep Dive

### The Origin Debate

Both Hanlin Tea Room in Tainan and Chun Shui Tang in Taichung claim to have invented bubble tea...

### Global Expansion

In the 2010s, bubble tea swept across cities in Europe, America, and Asia...

## Why This Matters

Bubble tea isn't just a drink — it's Taiwan's finest soft power ambassador. Where there's no diplomatic recognition, Taiwanese flavor arrived first.

## References

- [Origins of Bubble Tea](https://example.com/boba-origin)
- [Taiwan Beverage Market Report](https://example.com/beverage-report)
```

### Hub Page Template (`knowledge/[Category]/_Hub.md`)

```markdown
---
title: 美食
titleEn: Food
description: 台灣的飲食文化是移民歷史、地理環境與創意精神的完美結晶。
category: food
---

## 關於這個分類

台灣是一個以食物說故事的地方...

## 精選文章

這個分類收錄了台灣飲食文化最具代表性的面向...
```

---

## Frontmatter Reference

### Required Fields

```yaml
---
title: "文章標題"           # Display title
description: "一句話說明"   # Meta description (150 chars max)
category: food             # Must match one of 12 category slugs
date: 2024-01-15           # ISO date format
---
```

### Optional Fields

```yaml
---
tags: [tag1, tag2]         # Array of tags for knowledge graph
image: /images/wiki/...    # Must be from Wikimedia Commons cache
imageCaption: "..."        # Attribution: Title | Source | License
sources:                   # REQUIRED: clickable URLs, no plain-text refs
  - title: "Source Name"
    url: https://...
---
```

---

## Adding Images (Wikimedia Commons Policy)

All images must be from Wikimedia Commons with verified CC licenses. Cache them locally:

```bash
# Download and cache a Wikimedia image
# Images are stored with MD5-hashed filenames
curl -o public/images/wiki/$(echo "filename.jpg" | md5sum | cut -d' ' -f1).jpg \
  "https://commons.wikimedia.org/wiki/Special:FilePath/Taiwan_landscape.jpg"
```

Image attribution format in frontmatter:
```yaml
imageCaption: "Description | Wikimedia Commons | CC BY-SA 4.0"
```

---

## Knowledge Graph Integration

Articles automatically appear in the D3.js knowledge graph at `/graph`. Nodes are created from articles; edges are created from shared tags and cross-references.

### Linking Articles

Reference other articles within content using relative paths:

```markdown
台灣的[半導體產業](/technology/tsmc)是台積電...

See also: [Bubble Tea](/food/bubble-tea) for more on Taiwan's soft power.
```

### Tagging for Graph Connections

Use consistent tags to create knowledge graph bridges:

```markdown
# Both articles tagged [democratic transition] will be connected
tags: [democratic transition, civil society, 1990s]
```

---

## Sync Workflow

After editing any file in `knowledge/`, always sync before building:

```bash
# 1. Edit content
vim knowledge/Food/new-article.md
vim knowledge/en/Food/new-article.md

# 2. Sync to src/content/
bash scripts/sync.sh

# 3. Verify build
npm run build

# 4. Preview
npm run preview
```

---

## Three-Layer Depth Pattern

Every article should follow this structure for AI-readability and varied reading levels:

```markdown
## 30 秒認識 / 30-Second Overview
[2-3 sentences, the essential fact]

## 深度閱讀 / Deep Dive
### Subsection 1
[Detailed exploration with data]

### Subsection 2
[Historical context or comparison]

## 為什麼重要 / Why This Matters
[Curatorial perspective — answer "why should the world care?"]

## 參考資料 / References
[Clickable URLs only — no plain-text citations]
```

---

## Contributing via PR

### Full PR Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/taiwan-md.git
cd taiwan-md

# 2. Create branch
git checkout -b add/food/scallion-pancake

# 3. Add zh-TW article
cat > knowledge/Food/scallion-pancake.md << 'EOF'
---
title: 蔥抓餅
description: ...
category: food
date: 2024-01-20
sources:
  - title: Source
    url: https://...
---
Content here...
EOF

# 4. Add English translation
mkdir -p knowledge/en/Food
cat > knowledge/en/Food/scallion-pancake.md << 'EOF'
---
title: Scallion Pancake
...
EOF

# 5. Sync and test
bash scripts/sync.sh
npm run build

# 6. Commit and PR
git add knowledge/
git commit -m "feat(food): add scallion pancake article (zh+en)"
git push origin add/food/scallion-pancake
```

### Commit Message Convention

```
feat(category): add [article name] article (zh+en)
fix(category): correct [article name] factual error
i18n(category): add English translation for [article name]
feat(graph): add knowledge graph connections for [topic]
```

---

## AI-Native Features

### llms.txt

The site exposes `/llms.txt` for AI consumption. When writing content, use structured headers that AI can parse:

```markdown
# Title

**Key fact:** One-sentence essential truth.

## Context
...

## Significance
...
```

### Meta AI Summary Tag

Pages include `<meta ai-summary>` — write descriptions that work as standalone AI context:

```yaml
description: "台積電（TSMC）生產全球90%最先進晶片，是台灣的「矽盾」——台灣的地緣政治生存策略。"
```

---

## Astro Page Patterns

### Category Page (`src/pages/[category].astro`)

```astro
---
import { getCollection } from 'astro:content';

const category = 'food';
const articles = await getCollection('knowledge', ({ data }) =>
  data.category === category
);
---

<ul>
  {articles.map(article => (
    <li>
      <a href={`/${category}/${article.slug}`}>{article.data.title}</a>
      <p>{article.data.description}</p>
    </li>
  ))}
</ul>
```

### Bilingual Route Pattern

```
/food/bubble-tea        ← zh-TW (default)
/en/food/bubble-tea     ← English
```

---

## Content Quality Checklist

Before submitting a PR, verify:

- [ ] Both `knowledge/[Category]/article.md` (zh-TW) and `knowledge/en/[Category]/article.md` (en) exist
- [ ] All `sources` entries have clickable `url` fields (no plain-text-only references)
- [ ] Article follows three-layer depth: 30-sec → deep dive → why it matters
- [ ] Images sourced from Wikimedia Commons with proper `imageCaption` attribution
- [ ] `category` slug matches one of the 12 valid categories exactly
- [ ] `bash scripts/sync.sh && npm run build` completes without errors
- [ ] Factual claims are verified against cited sources

---

## Troubleshooting

### Build fails after adding article

```bash
# Check frontmatter syntax
cat knowledge/Food/my-article.md | head -20

# Common issue: missing required fields
# Ensure title, description, category, date are all present

# Re-sync and rebuild
bash scripts/sync.sh
npm run build 2>&1 | grep ERROR
```

### Article not appearing in knowledge graph

```bash
# Ensure tags array is populated
# Check category slug matches exactly (case-sensitive)
# Verify sync was run after editing
bash scripts/sync.sh
```

### English article not showing at /en/...

```bash
# Verify file exists at correct path
ls knowledge/en/Food/my-article.md

# Check category field matches zh-TW article exactly
grep "category:" knowledge/Food/my-article.md
grep "category:" knowledge/en/Food/my-article.md
```

### Images not loading

```bash
# Images must be cached locally in public/images/wiki/
ls public/images/wiki/

# Verify frontmatter path starts with /images/wiki/
grep "image:" knowledge/Food/my-article.md
# Should be: image: /images/wiki/filename-hash.jpg
```

### Sync script permission error

```bash
chmod +x scripts/sync.sh
bash scripts/sync.sh
```

---

## Resources

- **Live site:** https://taiwan.md
- **Knowledge graph:** https://taiwan.md/graph
- **Contribute guide:** https://taiwan.md/contribute
- **llms.txt:** https://taiwan.md/llms.txt
- **License:** CC BY-SA 4.0 (content) + MIT (code)
- **Contact:** cheyu.wu@monoame.com
