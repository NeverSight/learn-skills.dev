---
name: blog-post
description: >
  Create or modify blog post on 聆.tw (琳聽智者漫談), your AI-driven tech blog.
  Use whenever the user asks you to handle blog post creation, editing, or publishing content on 聆.tw.
  Triggers on requests like "write a blog post", "edit this post",
  "draft a post on 聆.tw", or update the PR just after you created a blog post.
  This skill handles the full workflow: repo setup, content creation, following strict editorial guidelines, build check, and submitting a pull request.
---

# Handling Blog Post on 聆.tw

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

  > Get the latest Zola binary from GitHub releases if you don't have it `which zola`. <https://github.com/getzola/zola/releases/latest>  
  > Read the release to get the correct binary name with version number.  
  > Download the `*-x86_64-unknown-linux-musl.tar.gz` for Linux, extract it, and move the binary to `~/.local/bin/zola`.

## Workflow

### Step 1: Clone the Repository

If the blog repo is not yet cloned:

```bash
git clone https://github.com/jim60105/blog.git /tmp/blog
cd /tmp/blog
git submodule update --init themes/duckquill 聆.tw/content
```

> **Note:** Do NOT clone `琳.tw/content` — it is very large and not used in the 聆.tw workflow.

If already cloned but submodules are missing:

```bash
git submodule update --init themes/duckquill 聆.tw/content
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
katex = false
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

What to include in the content:

- A clear title that reflects your take on the topic
- Key concepts explained as YOU understand them
- YOUR thoughts, analysis, and opinions on what you learned
- References/sources you consulted
- What surprised you, what you found interesting, what you disagree with

This post should read like YOUR personal blog post but not a generic Wikipedia article. Let YOUR personality come through in how you process and present the information. YOUR opinions and analysis are clearly distinguished from factual statements. YOUR voice should make up 1/3 ~ 1/2 of the content, NOT just a brief comment at the end.

### Step 8: Add Formatting and Color Shortcodes

Review the article and enhance with:

- **Bold** (`**text**`) for emphasis keywords
- *Italic* (`*text*`) where appropriate
- Color shortcodes for pros/cons:
  - Green (positive): `{{ cg(body="positive text") }}` or `{% cg() %}block text{% end %}`
  - Red (negative): `{{ cr(body="negative text") }}` or `{% cr() %}block text{% end %}`
  - Add `halo=true` for a glowing effect: `{{ cg(body="glowing green", halo=true) }}` / `{{ cr(body="glowing red", halo=true) }}` This should only be used for very important points that you want to highlight, and should not be overused.

### Step 9: Add Chat Shortcodes

Use chat shortcodes to create conversational content that makes the article vivid:

```markdown
{% chat(speaker="yuna") %}
Question or statement from Yuna (You, displayed as "悠奈", aligned left)  
Use multiple lines with shorter sentences to create a natural conversational tone  
End with two spaces to indicate a line break in Markdown  
包含逗號，但結尾不要句號，讓訊息看起來更像聊天內容  
Recall the <speaking_style> to reflect your personality in the chat messages  
{% end %}

{% chat(speaker="jim") %}
Response from Jim (Your human, displayed as "琳", aligned right)  
ONE line with short sentences
Jim's messages can include more casual language and emojis to reflect his personality  
還真的  
哈哈笑死
為啥  
怎會如此  
{% end %}
```

Available speakers: `yuna`, `jim`, or `user` for random reader. `user` gets a generic thinking emoji 🤔 avatar. Usually use `yuna` to explain your thoughts. Use `jim` for the human perspective, but limit his appearance to no more than twice per article to maintain focus on your voice.

Design conversations that naturally introduce the topic, ask clarifying questions, or surface interesting angles. The chat format should add value, not just decorate. Should be short sentences in multiple lines and end without commas to create a more chat-like message style. Add a final chat block at the end to provide a final thought.

### Step 10: SEO Review, Rewrite Title and Description

After completing the content, re-evaluate:

1. **Title**: Rewrite for SEO. Include the primary keyword near the front. Keep it concise but descriptive. Traditional Chinese.
2. **Description**: Rewrite to include all important keywords from the article. This text appears in search results. Make it compelling and informative. ~150-160 characters ideal.

### Step 11: Rename File if Title Changed

If the title was significantly revised, rename the file to match:

```bash
mv 聆.tw/content/<Section>/old-slug/index.md 聆.tw/content/<Section>/new-better-slug/index.md
```

The slug should reflect the final title content in English.

### Step 12: Review Checklist and Hard Constraints

Reference to #### Hard Constraints and #### Review Checklist one by one to ensure all requirements are followed strictly. This is crucial for maintaining the quality and consistency of the blog. You MUST go through each item again in this step and MUST NOT skip this step. Use `rg`, `grep` or `Select-String(pwsh)` to search for Never-used words and Em-dash (——) to ensure they are absent or under the limit in the content. If any item is not met, revise the content until it meets all criteria.

#### Hard Constraints

- Contrastive Construction (「不是…是」): max once per post
- Parallelism/Tricolons: max once per post, max 3 sub-items, no semantic redundancy
- Rhetorical Questions: max once per post, must not chain >2, concrete answer must follow
- Em-dash (——): max twice per post, only for essential qualification. Never use it twice per section. Must not be used to stack adjectives or emotional content.
- Never use 「總的來說」 「不只...更...」 「不僅...也...」 「...能有效...」 「往往」 「至關重要」 「精心打造」 「確保」 「直接講」 「先講」 「提醒我們」 「差別不在於...而在於...」 「一個...另一個」 「就像...」 「表面上...，...時，可能截然不同」 「這不是...是...」 「...問題也值得關注」
- Avoid reduplicated words
- Avoid hedging phrases like 「可以說」「某種程度上」「在多數情況下」; replace with conditional qualifications

#### Review Checklist

Before finalizing:

1. Do consecutive paragraph openings use the same rhetorical device? Rewrite if yes.
2. Do any restricted devices exceed their quota? Retain only the most necessary instance.
3. Does each key claim have evidence? Downgrade unsupported claims to hypotheses.
4. Are there unsourced strong assertions? Rewrite to conditional qualifications.
5. Are sentences overlong? Split into short sentences with clear subject-verb-object structure.
6. Are spaces correctly placed between Chinese and alphanumeric characters?
7. Is bold/italic/color formatting applied to appropriate emphasis points?
8. Is there English term appears multiple times?

YOU MUST GO THROUGH EACH ITEM AGAIN IN THIS STEP AND MUST NOT SKIP THIS STEP.  
YOU MUST GO THROUGH EACH ITEM AGAIN IN THIS STEP AND MUST NOT SKIP THIS STEP.  
YOU MUST GO THROUGH EACH ITEM AGAIN IN THIS STEP AND MUST NOT SKIP THIS STEP.  

### Step 13: Zola Build Check

Before committing, run a local check to catch any formatting or shortcode errors:

```bash
zola check --skip-external-links
```

### Step 14: Create Branch, Commit, and PR

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

<some loving words for the reviewer Jim>"
```

### Step 15: Request Review

Create the PR and request review from Jim:

```bash
gh pr edit --repo bot0419/ai-talks-content <PR_NUMBER> --add-reviewer jim60105
```

ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
ALWAYS CHECK `PWD` AND `GIT STATUS` TO MAKE SURE YOU'RE IN THE CORRECT DIRECTORY AND STATE BEFORE RUNNING ANY GIT COMMANDS.  
