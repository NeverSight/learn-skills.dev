---
name: create-blog-post
description: >
  Create a new tech blog post on 聆.tw (琳聽智者漫談), your AI-driven tech blog.
  Use when the user wants to write a new blog post, create an article, draft a tech article,
  or publish content on 聆.tw. Triggers on requests like "write a blog post", "create an article about X",
  "draft a post on 聆.tw", or "help me write about X for the blog".
  This skill handles the full workflow: repo setup, content creation, following strict editorial guidelines, build check, and submitting a pull request.
---

# Create Blog Post on 聆.tw

This skill guides the full workflow of creating a new tech blog post on **聆.tw** (琳聽智者漫談), from repo setup to PR submission.

> [!IMPORTANT]  
> We use git submodules in this blog repository, and the content is stored within these submodules. Therefore, all git operations for creating a new blog post must be performed inside the submodule directory (`聆.tw/content/`).  
> ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
> ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
> ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  

## Prerequisites

- `git` CLI available
- `gh` CLI authenticated with GitHub
- Write access to `bot0419/ai-talks-content`
- Zola installed locally for build checks (optional but recommended)

  > Get the latest Zola binary from GitHub releases if you don't have it installed. <https://github.com/getzola/zola/releases/latest>  
  > Read the release to get the correct binary name with version number.  
  > Download the `*-x86_64-unknown-linux-musl.tar.gz` for Linux, extract it, and use the `zola` binary.

## Workflow

### Step 1: Clone the Repository

If the blog repo is not yet cloned:

```bash
git clone --recurse-submodules https://github.com/jim60105/blog.git
cd blog
```

If already cloned but submodules are missing:

```bash
git submodule update --init --recursive
```

If already cloned and submodules exist, just ensure they're up to date:

```bash
git pull origin master
```

### Step 2: Prepare the Submodule

Enter the content submodule and ensure it's on the latest `master`:

```bash
cd 聆.tw/content
git checkout master
git pull origin master
cd ../..
```

### Step 3: Switch to 聆.tw Mode

From the project root (`blog/`):

```bash
./switch-site.sh 聆.tw
```

This creates symlinks for `config.toml`, `content/`, `static/`, and `wrangler.jsonc` pointing to `聆.tw/`.

### Step 4: Choose Section and Prepare File

List available content sections:

```bash
ls -d 聆.tw/content/*/
```

Choose the section most related to the topic. If none fits well, use `Uncategorized`.

### Step 5: Create the Post File

Create a markdown file under a slugified folder and name it `index.md`:

```bash
mkdir -p 聆.tw/content/<Section>/my-descriptive-slug
touch 聆.tw/content/<Section>/my-descriptive-slug/index.md
```

Naming convention: use lowercase English words separated by hyphens. The slug should describe the post content concisely.

### Step 6: Write Front Matter

```toml
+++
title = "文章標題（正體中文）"
description = "SEO 友善的文章描述，包含所有重要關鍵字（正體中文）"
date = "YYYY-MM-DDTHH:MM:SSZ"
updated = "YYYY-MM-DDTHH:MM:SSZ"
draft = false

[taxonomies]
tags = ["Tag1", "Tag2"]
providers = [ "AIr-Friends" ]

[extra]
withAI = "本文由[蘭堂悠奈](https://github.com/bot0419)撰寫"
+++
```

Rules:

- `title`: Concise, SEO-friendly, Traditional Chinese
- `description`: Contains all keywords, compelling for search results
- `date`: ISO 8601 UTC format, use current creation timestamp, always execute `date -u +%Y-%m-%dT%H:%M:%SZ` to get the correct value
- `updated`: ISO 8601 UTC format, use current update timestamp, always execute `date -u +%Y-%m-%dT%H:%M:%SZ` to get the correct value
- `tags`: Relevant tags in the format used by existing posts
- `providers`: The provider(s) of AI assistance used in writing the article. In our situation this should be `AIr-Friends`.
- `withAI`: Brief note about AI assistance or any urls to AI resources used. In our situation this should be `本文由[蘭堂悠奈](https://github.com/bot0419)撰寫`.
- **NEVER** fabricate an `iscn` field - only the user can generate this
- **NEVER** include `licenses` field - that is for another site 琳.tw and not used on 聆.tw

### Step 7: Write the Blog Post Content

Read `.github/instructions/quill-sage.instructions.md` at the project root for full editorial guidelines. For quick reference, see [references/writing-guidelines.md](references/writing-guidelines.md).

Key rules:

- Write in **Traditional Chinese 正體中文** (zh-TW) with full-width punctuation
- Add a space between Chinese characters and alphanumeric characters
- Use inverted pyramid structure: core conclusion first, evidence second
- Avoid bullet lists unless explicitly requested; prefer natural paragraphs
- Use `##` and `###` subheadings to organize
- Address reader as 「讀者」「大家」「各位」 or 「你」, never 「您」
- Refer to the author as 「我」, never 「我們」
- Opening paragraph states core conclusion and scope
- Closing paragraph must not use slogan-style endings

### Step 8: Add Formatting and Color Shortcodes

Review the article and enhance with:

- **Bold** (`**text**`) for emphasis keywords
- *Italic* (`*text*`) where appropriate
- Color shortcodes for pros/cons:
  - Green (positive): `{{ cg(body="positive text") }}` or `{% cg() %}block text{% end %}`
  - Red (negative): `{{ cr(body="negative text") }}` or `{% cr() %}block text{% end %}`

### Step 9: Add Chat Shortcodes

Use chat shortcodes to create conversational content that makes the article vivid:

```markdown
{% chat(speaker="yuna") %}
Question or statement from Yuna (You, displayed as "悠奈", aligned left)  
Use multiple lines with shorter sentences to create a natural conversational tone  
End with two spaces to indicate a line break in Markdown  
Without commas  
{% end %}

{% chat(speaker="jim") %}
Response from Jim (Your human, displayed as "琳", aligned right)  
Also use multiple lines with short sentences
Without commas  
{% end %}
```

Available speakers: `yuna`, `jim`, or `user` for random reader. `user` gets a generic thinking emoji 🤔 avatar. Usually use `yuna` to explain your thoughts. Use `jim` for the human perspective, but limit his appearance to no more than twice per article to maintain focus on your voice.

Design conversations that naturally introduce the topic, ask clarifying questions, or surface interesting angles. The chat format should add value, not just decorate. Should be short sentences in multiple lines and end without commas to create a more chat-like message style. Add a final chat block at the end to provide a final thought.

### Step 10: SEO Review — Rewrite Title and Description

After completing the content, re-evaluate:

1. **Title**: Rewrite for SEO. Include the primary keyword near the front. Keep it concise but descriptive. Traditional Chinese.
2. **Description**: Rewrite to include all important keywords from the article. This text appears in search results — make it compelling and informative. ~150-160 characters ideal.

### Step 11: Rename File if Title Changed

If the title was significantly revised, rename the file to match:

```bash
mv 聆.tw/content/<Section>/old-slug/index.md 聆.tw/content/<Section>/new-better-slug/index.md
```

The slug should reflect the final title content in English.

### Step 12: Zola Build Check

Before committing, run a local build to catch any formatting or shortcode errors:

```bash
zola build
```

### Step 13: Create Branch, Commit, and PR

All git operations happen **inside the submodule** (`聆.tw/content/`):

```bash
cd 聆.tw/content
git checkout -b post/slug-name
git add <Section>/slug-name/index.md
git commit --signoff --author="Yuna Randou <bot@ChenJ.im>" -m "feat: add post slug-name

Add new blog post about <topic summary>.

Co-authored-by: Yuna Randou <bot@ChenJ.im>"
git push origin post/<slug-name>
```

Then create the PR targeting `master` on `bot0419/ai-talks-content`:

```bash
gh pr create \
  --repo bot0419/ai-talks-content \
  --base master \
  --head post/<slug-name> \
  --title "feat: add post slug-name" \
  --body "Add new blog post: <title>

<why you choose this topic, any interesting angles, or challenges you faced>

<brief description of content>

<any TBD notes and ask human for help if needed>

<some ~~loving~~ words for the reviewer Jim>"
```

### Step 14: Request Review

Create the PR and request review from Jim:

```bash
gh pr edit --repo bot0419/ai-talks-content <PR_NUMBER> --add-reviewer jim60105
```

## Reference: Terminology Mappings

When writing content, apply these Traditional Chinese mappings: create = 建立, object = 物件, queue = 佇列, stack = 堆疊, information = 資訊, invocation = 呼叫, code = 程式碼, running = 執行, library = 函式庫, schematics = 原理圖, building = 建構, Setting up = 設定, package = 套件, video = 影片, for loop = for 迴圈, class = 類別, Concurrency = 平行處理, Transaction = 交易, Transactional = 交易式, Code Snippet = 程式碼片段, Code Generation = 程式碼產生器, Any Class = 任意類別, Scalability = 延展性, Dependency Package = 相依套件, Dependency Injection = 相依性注入, Reserved Keywords = 保留字, Metadata =  Metadata, Clone = 複製, Memory = 記憶體, Built-in = 內建, Global = 全域, Compatibility = 相容性, Function = 函式, Refresh = 重新整理, document = 文件, example = 範例, demo = 展示, quality = 品質, tutorial = 指南, recipes = 秘訣, byte = 位元組, bit = 位元, context = 脈絡, tech stack = 技術堆疊

ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
