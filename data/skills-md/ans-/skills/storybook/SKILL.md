---
name: storybook
description: Generate personalized illustrated storybooks with custom artwork. Supports 5-10 pages (default 6), age-appropriate text length (3-18 years), and multiple art styles (watercolor, cartoon, pixel-art, claymation, comic, coloring-book). Use when creating picture books, children's storybooks, illustrated stories, or any request involving generating a story with images for children.
---

# Storybook Skill

Generate personalized illustrated storybooks with cover, story pages, and custom artwork.

## Workflow

Creating a storybook involves these steps:

1. Gather requirements (theme, age, pages, style)
2. Generate story structure (title, cover, pages)
3. Create illustrations with generate_image tool
4. Output complete storybook

## Step 1: Gather Requirements

Confirm these parameters before generating:

| Parameter  | Options                                                          | Default         |
| ---------- | ---------------------------------------------------------------- | --------------- |
| Theme      | User-provided story topic                                        | Required        |
| Target Age | 3-18 years                                                       | 6 years         |
| Page Count | 5-10 pages                                                       | 6 pages         |
| Art Style  | watercolor, cartoon, pixel-art, claymation, comic, coloring-book | cartoon         |
| Language   | Any supported language                                           | User's language |

## Step 2: Generate Story Structure

### Text Length Guidelines (by age)

| Age Range   | Characters per Page |
| ----------- | ------------------- |
| 0-3 years   | 10-20               |
| 4-6 years   | 20-40               |
| 7-9 years   | 40-70               |
| 10-18 years | 70-100              |

### Story Structure

1. **Cover Page**: Title + subtitle + cover illustration
2. **Opening** (1-2 pages): Introduce characters and setting
3. **Development** (2-4 pages): Build the story, introduce conflict
4. **Climax** (1-2 pages): Peak of the story
5. **Resolution** (1-2 page): Conclusion with positive message

> [!NOTE]
> **Idiom (成语) Storybooks**: The last 1-2 pages should explain:
>
> - The moral/lesson of the idiom story (寓意)
> - The meaning of the idiom (含义)
> - Usage examples in daily life (用法, optional)

For detailed page templates by count (4/6/10 pages), see [references/story-templates.md](references/story-templates.md).

## Step 3: Create Illustrations

Maintain consistency across all illustrations:

- **Characters**: Same appearance throughout (hair, clothing, features)
- **Art style**: Match user's chosen style exactly
- **Color palette**: Child-friendly, cohesive
- **Composition**: Clear focal point, simple backgrounds

For detailed prompt templates, art style reference table, cover rules, and examples, see [references/illustration-guide.md](references/illustration-guide.md).

## Step 4: Output

Create all files in the specified output directory. For detailed `story.json` schema, `story.md` format, tags reference, and JSON formatting rules, see [references/output-format.md](references/output-format.md).

```
[story-name]/
├── story.json      # Story metadata and content
├── story.md        # Human-readable story document
├── cover.png/jpg   # Cover illustration
├── page_1.png/jpg  # Page illustrations
└── ...
```

## Example Usage

**User**: Create a storybook about a brave little mouse for my 5-year-old

**Response structure**:

1. Confirm: 6 pages, age 5 (20-40 chars/page), cartoon style
2. Generate story with cover + 5 story pages
3. Create illustrations for each page
4. Output complete storybook
