---
name: cuimao-translator
description: Claude Code skill for translating English PDF books into fluent, natural Chinese using a multi-mode, multi-style translation pipeline.
triggers:
  - translate this PDF to Chinese
  - 翻译这个PDF
  - 英译中
  - 帮我汉化这本书
  - translate PDF book to Chinese
  - 精翻这个文档
  - quick translate English PDF
  - 一键翻译PDF
---

# 萃猫翻译 · Cuimao Translator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code skill that translates English PDF books into idiomatic, natural-sounding Chinese. Designed for book-length texts, it avoids "translation smell" through mode selection, style presets, and automated Europeanized-Chinese detection.

---

## Installation

```bash
git clone https://github.com/Cuimao777/cuimao-translator.git ~/.claude/skills/cuimao-translator
```

Restart Claude Code. The skill auto-activates when you say phrases like "翻译这个PDF" or "translate this PDF".

---

## File Structure

```
cuimao-translator/
├── SKILL.md                      # Main skill file (auto-loaded by Claude Code)
├── README.md
└── references/
    ├── glossary-en-zh.md         # 100+ English-Chinese term pairs
    ├── translation-guide.md      # Sentence patterns, diagnostics, register guides
    └── refined-workflow.md       # 5-step refined translation pipeline
```

---

## Three Translation Modes

| Mode | Trigger Words | Pipeline | Best For |
|------|--------------|----------|----------|
| ⚡ Quick | `快翻` `速译` `quick` | Read → Translate | Skimming, short snippets |
| 📖 Normal | `翻译` (default) | Analyze → Translate | Most books, articles |
| 💎 Refined | `精翻` `精细翻译` `出版级` | Analyze → Draft → Review → Revise → Polish | Publication-quality output |

You can upgrade after Normal completes: reply `继续润色` or `refine` to enter the Refined pipeline.

---

## Five Style Presets

| Style Key | Use Case | Characteristics |
|-----------|----------|-----------------|
| `storytelling` | Novels, biography, narrative non-fiction | Natural transitions, Chinese rhythm |
| `academic` | Textbooks, research papers | Formal register, precise terminology |
| `literal` | Manuals, legal docs, contracts | Close to source structure, minimal rewrite |
| `elegant` | Literary fiction, poetry, essays | Four-character idioms, musicality |
| `conversational` | Self-help, memoirs, dialogue-heavy | Relaxed, reader-friendly tone |

If not specified, the skill auto-detects from content. `storytelling` is the safe default for most books.

---

## How to Use

### Basic Usage

Just say it naturally in Claude Code chat:

```
翻译这个 PDF
```

```
translate this PDF book to Chinese
```

```
帮我把这本书汉化，用 storytelling 风格
```

### Specify Mode + Style

```
精翻这个PDF，academic 风格
```

```
快翻这几页，conversational 风格
```

```
出版级翻译，elegant 风格
```

### Upgrade After Normal Translation

```
继续润色
```

```
refine
```

---

## Translation Philosophy: 信 → 达 → 雅

### 信 (Faithful)
- Every English sentence has a corresponding Chinese sentence
- Facts, numbers, logic, proper nouns are preserved exactly
- No summarizing, skipping, or embellishment

### 达 (Fluent)
- Output reads as if written by a native Chinese author
- Topic-comment sentence structure (Chinese-native order)
- Split long sentences into 7–15 character natural chunks
- Active voice preferred; complement clauses over adverbial chains

### 雅 (Culturally Adapted)
- English idioms/slang → find Chinese equivalent expressions
- Untranslatable wordplay → translate meaning + add note
- Unknown cultural references → brief translator's note

---

## Europeanized Chinese Auto-Detection (六重检测)

After every translation, the skill self-checks for six common "translation smell" patterns:

| # | Problem | Bad Example | Fix |
|---|---------|-------------|-----|
| 1 | 被字句泛滥 | 他被表扬了 | 他受到了表扬 |
| 2 | 连接词堆砌 | 因为…所以…虽然…但是… | Remove redundant connectors |
| 3 | 定语过长 | 那个在昨天下午三点去买东西的人 | Split into multiple short sentences |
| 4 | 之一滥用 | 最重要的问题之一 | 极其重要的问题 |
| 5 | 的的的 | ≥3 `的` in one sentence | Restructure the sentence |
| 6 | 名词化过度 | 政策的实施 | 实施政策 |

---

## Real Example

**English Input:**

```
The old man had taught the boy to fish and the boy loved him.
He was an old man who fished alone in a skiff in the Gulf Stream
and he had gone eighty-four days now without taking a fish.
```

**Chinese Output (storytelling style):**

```
老头儿教过那孩子打鱼，孩子也爱他。
他是个独自在湾流里的一只小船上打鱼的老头儿，
如今已经接连八十四天一条鱼也没打着了。
```

---

## Working with the References

### Glossary (`references/glossary-en-zh.md`)

Contains 100+ curated English→Chinese term mappings. The skill applies these automatically for consistency across an entire book. When translating a new domain-specific text, you can extend it:

```markdown
<!-- Add domain terms at the bottom of glossary-en-zh.md -->
| machine learning | 机器学习 |
| gradient descent | 梯度下降 |
| overfitting | 过拟合 |
| hyperparameter | 超参数 |
```

### Translation Guide (`references/translation-guide.md`)

Covers:
- Sentence transformation patterns (passive → active, noun phrase → verb phrase)
- Register-specific vocabulary lists
- How to handle culturally-specific content per genre

### Refined Workflow (`references/refined-workflow.md`)

Documents the 5-step Refined pipeline in detail:
1. **Analyze** — genre, register, key terms, author voice
2. **Draft** — first-pass translation
3. **Review** — check against 六重检测
4. **Revise** — fix flagged issues
5. **Polish** — rhythm, flow, final read-aloud check

---

## Practical Patterns

### Translate a Specific Chapter

```
翻译第三章，storytelling 风格
```

```
translate chapter 5 only, academic style
```

### Batch Translation with Consistency

For multi-chapter books, mention the book title so the skill maintains term consistency:

```
这是《Thinking, Fast and Slow》的第二章，请继续保持之前的翻译风格和术语
```

### Custom Glossary Injection

Paste a term list before the content:

```
请使用以下术语表翻译：
- neural network → 神经网络
- token → 词元
- prompt → 提示词

[paste content here]
```

### Output Format Control

```
翻译后按段落对照输出（英文段落 + 中文段落交替）
```

```
只输出中文译文，不要对照
```

---

## Trigger Reference

| Trigger | Effect |
|---------|--------|
| `翻译` / `translate` | Normal mode, auto-detect style |
| `汉化` / `英译中` | Normal mode |
| `速译` / `快翻` / `quick` | Quick mode |
| `精翻` / `精细翻译` / `出版级` | Refined mode |
| `继续润色` / `refine` | Upgrade current translation to Refined |
| `storytelling` / `叙事` | Force storytelling style |
| `academic` / `学术` | Force academic style |
| `literal` / `逐句` | Force literal style |
| `elegant` / `文学` | Force elegant style |
| `conversational` / `口语` | Force conversational style |

---

## Troubleshooting

**Skill not activating after install:**
- Restart Claude Code completely
- Verify file is at `~/.claude/skills/cuimao-translator/SKILL.md`
- Check file permissions: `chmod -R 644 ~/.claude/skills/cuimao-translator/`

**Translation sounds too formal / too casual:**
- Explicitly specify a style preset: `用 conversational 风格重译`
- For mixed-register texts, specify per section

**Terminology inconsistent across chapters:**
- Start each session by referencing the book title
- Add domain terms to `references/glossary-en-zh.md` before translating

**Output contains Europeanized Chinese patterns:**
- Run: `检查译文中的翻译腔，按六重检测标准修正`
- For Refined mode, this check runs automatically

**PDF content not parsing correctly:**
- Extract text from PDF first, then paste into chat
- For scanned PDFs, run OCR before translation

---

## License

MIT — see [LICENSE](https://github.com/Cuimao777/cuimao-translator/blob/main/LICENSE)
