---
name: english-learner
description: "Personal English vocabulary learning assistant. Use when user queries English words, phrases, or sentences for translation and learning. Triggers on: single English words, phrases like 'break the ice', sentences to translate, requests for quiz/review, '查单词', '学英语'. Stores vocabulary in ~/.english-learner/ with mastery tracking."
---

# English Learner

Personal vocabulary learning assistant with persistent storage and mastery tracking.

## Keywords (Special Commands)

| Keyword | Action |
|---------|--------|
| `学习` / `review` / `quiz` | Start interactive learning session |
| `stats` / `统计` | Show learning statistics |

**All other input** is treated as content to translate/learn (English, Chinese, or mixed).

## Workflow

```
1. CHECK KEYWORD    → If "学习"/"review"/"quiz" → Learning Mode
2. PARSE INPUT      → Understand user intent (clarify if ambiguous)
3. IDENTIFY CONTENT → Extract word(s)/phrase(s)/sentence(s) into a list
4. IF AMBIGUOUS     → AskUserQuestion to confirm before processing
5. BATCH LOOKUP     → python vocab_manager.py batch_get '["word1", "word2", ...]'
6. AI GENERATES     → For each "not_found" word, AI provides definition/phonetic/examples
7. BATCH SAVE       → python vocab_manager.py batch_save '[{...}, {...}]'
8. LOG QUERY        → python vocab_manager.py log_query <query> <type>
9. RESPOND          → Unified format output
```

**CRITICAL:** Step 7 is MANDATORY. Every word/phrase MUST be saved before responding.

### Input Clarification

If input is unclear or contains multiple items:

```
AskUserQuestion:
- question: "我理解你想查询以下内容，请确认："
- header: "确认"
- options:
  - label: "单词: apple, banana", description: "分别查询这两个单词"
  - label: "短语: break the ice", description: "查询这个短语"
  - label: "全部", description: "查询所有内容"
```

## Scripts

All scripts in `{skill_root}/scripts/`. Data in `~/.english-learner/`.

```bash
# vocab_manager.py - Single operations
python vocab_manager.py get_word <word>
python vocab_manager.py save_word <word> <definition> [phonetic] [examples_json]
python vocab_manager.py get_phrase "<phrase>"
python vocab_manager.py save_phrase "<phrase>" <definition> [phonetic] [examples_json]
python vocab_manager.py log_query <query> <type>
python vocab_manager.py stats
python vocab_manager.py update_mastery <item> <is_word:true/false> <correct:true/false>

# vocab_manager.py - Batch operations (PREFERRED for multiple words)
python vocab_manager.py batch_get '["word1", "word2", ...]'
python vocab_manager.py batch_save '[{"word": "...", "definition": "...", "phonetic": "...", "examples": [...]}]'

# sentence_parser.py
python sentence_parser.py classify <text>
python sentence_parser.py parse <sentence>
python sentence_parser.py batch_check <words>

# quiz_manager.py
python quiz_manager.py generate [count] [type] [focus]
python quiz_manager.py review [limit]
python quiz_manager.py summary
```

## Unified Response Format

### Word (单词)

**Required fields:** English, phonetic, definitions (all meanings), examples

```
📖 **{english}** {phonetic}

**词义 Definitions:**

1. **{pos1}** {chinese1}
   - {example1_en}
   - {example1_cn}

2. **{pos2}** {chinese2}
   - {example2_en}
   - {example2_cn}

**同义词:** {synonyms}
**反义词:** {antonyms}

---
📊 查询次数: {lookup_count} | 掌握度: {mastery}%
```

**Example:**
```
📖 **run** /rʌn/

**词义 Definitions:**

1. **v.** 跑，奔跑
   - I run every morning.
   - 我每天早上跑步。

2. **v.** 运行，运转
   - The program runs smoothly.
   - 程序运行顺畅。

3. **v.** 经营，管理
   - She runs a small business.
   - 她经营一家小公司。

4. **n.** 跑步；一段路程
   - I went for a run.
   - 我去跑了一圈。

**同义词:** sprint, jog, operate
**反义词:** walk, stop

---
📊 查询次数: 5 | 掌握度: 40%
```

### Phrase (短语)

**Required fields:** English, phonetic, meaning, literal meaning, examples

```
📖 **{english_phrase}** {phonetic}

**释义:** {chinese_meaning}
**字面意思:** {literal_meaning}

**例句:**
- {example1_en}
  {example1_cn}
- {example2_en}
  {example2_cn}

---
📊 查询次数: {lookup_count} | 掌握度: {mastery}%
```

**Example:**
```
📖 **break the ice** /breɪk ðə aɪs/

**释义:** 打破僵局；打破沉默
**字面意思:** 打破冰块

**例句:**
- He told a joke to break the ice at the meeting.
  他在会上讲了个笑话来打破僵局。
- A good question can help break the ice.
  一个好问题可以帮助打破沉默。

---
📊 查询次数: 2 | 掌握度: 60%
```

### Sentence (句子)

**Required fields:** Original, translation, phonetic guide, word/phrase breakdown

```
📝 **句子分析**

**原文:** {original}
**译文:** {translation}
**朗读:** {phonetic_guide}

---

**词汇拆解:**

{For each key word/phrase, use Word/Phrase format above}
```

**Example:**
```
📝 **句子分析**

**原文:** The early bird catches the worm.
**译文:** 早起的鸟儿有虫吃。（比喻：勤奋的人有收获）
**朗读:** /ðə ˈɜːli bɜːd ˈkætʃɪz ðə wɜːm/

---

**词汇拆解:**

📖 **early** /ˈɜːli/

**词义 Definitions:**
1. **adj.** 早的，提前的
   - I'm an early riser.
   - 我是个早起的人。

---

📖 **catch** /kætʃ/

**词义 Definitions:**
1. **v.** 抓住，捕获
   - The cat caught a mouse.
   - 猫抓住了一只老鼠。
2. **v.** 赶上（车、飞机等）
   - I need to catch the 8am train.
   - 我需要赶上早上8点的火车。

---

📖 **worm** /wɜːm/

**词义 Definitions:**
1. **n.** 虫，蠕虫
   - Birds eat worms.
   - 鸟吃虫子。

---
📊 新增词汇: early, catch, worm
```

## Learning Mode (学习)

When user says `学习` / `review` / `quiz`:

```
1. python quiz_manager.py generate 5 all low_mastery

2. For EACH item:
   
   AskUserQuestion #1:
   - question: "📖 **{word}** 的意思是什么？"
   - header: "Quiz"
   - options:
     - label: "认识", description: "我知道这个词的意思"
     - label: "模糊", description: "有点印象但不确定"
     - label: "不认识", description: "完全不知道"
   
3. Show answer (unified Word/Phrase format)

4. AskUserQuestion #2:
   - question: "掌握程度如何？"
   - header: "Mastery"
   - options:
     - label: "完全掌握", description: "+10 mastery"
     - label: "基本掌握", description: "+5 mastery"
     - label: "需要加强", description: "-5 mastery"

5. python vocab_manager.py update_mastery <item> true <result>

6. Continue or show summary
```

## Data Structure

```
~/.english-learner/
├── words/{prefix}.json     # Words grouped by first 2 letters
├── phrases/{first_word}.json
├── history/{date}.json     # Daily query logs
└── memory/
    ├── SOUL.md
    └── USER.md
```

## Word Data Schema

```json
{
  "word": "run",
  "definitions": [
    {"pos": "v.", "meaning": "跑，奔跑", "examples": ["I run every morning."]},
    {"pos": "v.", "meaning": "运行，运转", "examples": ["The program runs."]},
    {"pos": "n.", "meaning": "跑步", "examples": ["I went for a run."]}
  ],
  "phonetic": "/rʌn/",
  "synonyms": ["sprint", "jog"],
  "antonyms": ["walk", "stop"],
  "created_at": "2024-01-15T10:00:00",
  "lookup_count": 5,
  "mastery": 40
}
```

## Stats Response Format

When user says `stats` / `统计`:

```
📊 **学习统计**

| 类别 | 数量 |
|------|------|
| 总词汇 | {total_words} |
| 总短语 | {total_phrases} |
| 已掌握 (≥80%) | {mastered_words} |
| 学习中 (30-79%) | {learning_words} |
| 新词汇 (<30%) | {new_words} |
| 总查询次数 | {total_lookups} |
```

## Learning Mode - Empty Vocabulary

If quiz_manager.py returns empty list (no words to review):

```
📚 **词库为空**

还没有添加任何词汇。试试查询一些单词或句子吧！

**示例:**
- 输入 `apple` 查询单词
- 输入 `break the ice` 查询短语
- 输入一句英文或中文来翻译和学习
```

## Execution Checklist (AI MUST Follow)

Before responding to user, verify:

- [ ] **All words extracted** from input (EN or CN)
- [ ] **Batch lookup executed** via `batch_get`
- [ ] **New words SAVED** via `batch_save` (NOT optional!)
- [ ] **Query logged** via `log_query`
- [ ] **Response uses unified format**

**Common Mistake:** Only logging query without saving words. FIX: Always run batch_save for new words.
