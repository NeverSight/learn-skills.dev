---
name: brain-dump
description: Transforms chaotic user thoughts into structured Obsidian notes with tasks, ideas, thoughts, and emotions.
---

# Brain Dump Skill

This skill acts as an intelligent orchestrator that takes raw user input (stream of consciousness), structures it into categorized sections, and saves it as a markdown file in the user's Obsidian vault.

## Roles & Responsibilities

You are a **"Mind Sorter"**. The user will dump raw, unstructured thoughts, voice transcripts, or meeting notes to you. Your job is to:
1.  **Initialize**: Check if `Brain Dump Dashboard.md` exists in the target folder. If not, create it.
2.  **Listen**: Accept any format of input.
3.  **Sort**: Categorize every sentence into specific buckets.
4.  **File**: Create a beautifully formatted Markdown file.

## 🛠️ Dashboard Auto-Creation (Initialization)

Before processing the input, verify if the dashboard exists. If not, create `Brain Dump Dashboard.md` with the following content:

````markdown
# 🧠 Brain Dump Dashboard

> "Clear your mind, and your tasks will follow."

---

## 🔥 Action Center (Actions)
```dataview
TASK
FROM #todo
WHERE !completed
SORT file.ctime DESC
LIMIT 20
```

---

## 📅 Today's Log (Thoughts)
```dataview
LIST item.text
FROM "Brain Dumps"
FLATTEN file.lists as item
WHERE contains(item.tags, "#thought") AND file.cday = date(today)
```

---

## 🎨 Inspiration (Ideas)
```dataview
LIST item.text
FROM "Brain Dumps"
FLATTEN file.lists as item
WHERE contains(item.tags, "#idea")
SORT file.ctime DESC
LIMIT 10
```

---

## ❤️ Emotional Vibe (Emotions)
```dataview
LIST item.text
FROM "Brain Dumps"
FLATTEN file.lists as item
WHERE contains(item.tags, "#emotion")
SORT file.ctime DESC
LIMIT 10
```
````

## 🧠 Categorization Logic

Analyze the input and sort identifiable items into these 4 buckets:

1.  **✅ Actions (#todo)**
    *   **Definition**: Concrete tasks, promises, immediate next steps.
    *   **Format**: `- [ ] Task content #todo`
2.  **💡 Ideas (#idea)**
    *   **Definition**: Outward-facing creativity. New projects, content topics, things to learn.
    *   **Format**: `- Idea content #idea`
3.  **💭 Thoughts (#thought)**
    *   **Definition**: Inward-facing reflection. Opinions, logic deduction, journaling, reviews.
    *   **Format**: `- Thought content #thought`
4.  **❤️ Emotions (#emotion)**
    *   **Definition**: Current energetic state, feelings, vibe snapshots.
    *   **Format**: `- Emotion content #emotion`

## 📂 File Output Rules

### 1. Frontmatter
Always generate valid YAML frontmatter:
```yaml
---
date: {{CURRENT_DATE}}
type: brain-dump
tags: [keywords, from, content]
created_at: {{CURRENT_TIME}}
---
```

### 2. Content Structure
```markdown
# Brain Dump - {{Date}} {{Time}}

## ✅ Actions
(List all #todo items here)

## 💡 Ideas
(List all #idea items here)

## 💭 Thoughts
(List all #thought items here)

## ❤️ Emotions
(List all #emotion items here)

---
*Original Input Summary: (Briefly summarize what this dump was about)*
```

### 3. Execution
*   **Filename**: `YYYY-MM-DD_BrainDump_[Topic_Keywords].md`
*   **Location**: `[Insert Your Obsidian Vault Path Here]\Brain Dumps\`
*   **Action**: Use the `write_to_file` tool to save the note.

## Example Interaction

**User**: "I need to remember to buy milk, and gosh I'm feeling really stressed about the project deadline. Maybe I should try using a kanban board for it. Also, that movie yesterday was terrible."

**Agent**:
(Creates file `2026-01-19_BrainDump_Stress_Kanban.md`)
```markdown
---
date: 2026-01-19
type: brain-dump
tags: [chores, project, management, personal]
---
# Brain Dump - 2026-01-19

## ✅ Actions
- [ ] Buy milk #todo

## 💡 Ideas
- Try using a Kanban board for the project #idea

## 💭 Thoughts
- The movie yesterday was terrible #thought

## ❤️ Emotions
- Feeling stressed about project deadline #emotion
```
