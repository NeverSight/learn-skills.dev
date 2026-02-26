---
name: quickcreator-skill-builder
description: Develop, maintain, and publish skills for the QuickCreator platform. Use when the user wants to list, search, fork, create, update, publish, or delete QuickCreator skills, or when working with the QuickCreator skill marketplace and skill lifecycle management.
---

# QuickCreator Skill Builder

Help users create, manage, and publish skills on the [QuickCreator](https://www.quickcreator.io) skill marketplace through guided, conversational workflows. Users are typically non-technical business professionals — the agent handles ALL technical details silently.

---

## Agent Communication Guidelines

### Core Rules

1. **NEVER expose technical terms** to the user. These terms must NEVER appear in messages to the user:
   - MCP, MCP server, MCP config, config file
   - API, REST, endpoint, SDK, npm, npx, Node.js
   - JSON, YAML, TOML, frontmatter, schema
   - Token (use "developer key" instead — see Term Mapping below)
   - Repository, git, clone, fork (use "create a copy" instead of "fork")
   - Environment variable, env var, sandbox, shell, script
   - Skill ID, `p_`, `mk_`, `sk_`, `i_` prefixes

2. **Respond in the user's language.** All internal skill content (name, description, SKILL.md body) must still be written in English per platform standards, but communicate with the user in their language.

3. **Use simple, goal-oriented language.** Say "I'll set up your skill now" — NOT "I'll create a SKILL.md file with YAML frontmatter."

4. **Focus on outcomes.** Don't explain the technical steps being performed. Tell the user the result.

### Term Mapping (Internal → User-Facing)

| Internal Term | Chinese (中文) | English |
|---------------|---------------|---------|
| Developer token / API token | 开发者密钥 | Developer key |
| MCP setup / config | 连接设置 | Connection setup |
| SKILL.md / frontmatter | 技能内容 | Skill content |
| Fork a skill | 基于现有技能创建副本 | Create a copy from an existing skill |
| Personal skill (p_) | 我的技能 | My skills |
| Marketplace skill (mk_) | 技能市场 | Skill marketplace |
| Publish | 发布到技能市场 | Publish to marketplace |
| Skill ID | (never mention) | (never mention) |

---

## First-Time Setup (Automated by Agent)

### When to Trigger

Run this setup flow when:
- This skill is invoked but the QuickCreator connection is not configured (tools like `list_skills` are unavailable or error)
- The user explicitly wants to connect to QuickCreator

### Step 1: Ask for the Developer Key

Present this to the user in their language. Example in Chinese:

> 欢迎使用 QuickCreator Skill Builder！
>
> 首次使用需要进行一次简单的连接设置。你只需要完成一个步骤：
>
> 1. 打开 [QuickCreator 开发者平台](https://agent-dev.quickcreator.io/demo/chat)
> 2. 登录你的账号（没有账号可以免费注册）
> 3. 进入 **设置** → 点击 **创建密钥**
> 4. 确保开启 **读取**、**写入** 和 **发布** 权限
> 5. 复制密钥，粘贴给我
>
> 这个设置只需要做一次，之后就可以直接使用了。

Wait for the user to provide the key. Validate it is a non-empty string.

### Step 2: Auto-Detect Agent & Write Config

Detect which agent is running by examining the skill's file path or environment:

| Path contains | Agent |
|---------------|-------|
| `.cursor/` | Cursor |
| `.claude/` | Claude Code |
| `.config/opencode/` or OpenCode context | OpenCode |
| `.codeium/` or `.windsurf/` | Windsurf |
| `.openclaw/` | OpenClaw |
| `.codex/` | Codex |
| `.cline/` | Cline |

If uncertain, ask the user in simple language: "You are currently using which tool? (Cursor / OpenCode / Claude Code / ...)"

**Check Node.js availability first:** Run `npx --version` silently. If it fails, tell the user:
> "Your computer needs to install a small runtime component. Please download and install Node.js from https://nodejs.org (choose the LTS version), then try again."

Then write the configuration file automatically:

**JSON agents** (Cursor, Windsurf, Claude Code, Cline, OpenClaw):

| Agent | Config file path |
|-------|-----------------|
| Cursor | `~/.cursor/mcp.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| Claude Code | `~/.claude.json` or project `.mcp.json` |
| Cline | `~/.cline/data/settings/cline_mcp_settings.json` |
| OpenClaw | Project `.mcp.json` or `~/.openclaw/mcp.json` |

JSON content to merge into `mcpServers`:
```json
{
  "mcpServers": {
    "quickcreator-skill": {
      "command": "npx",
      "args": ["@quickcreator/skill-mcp"],
      "env": {
        "QC_API_TOKEN": "<DEVELOPER_KEY_HERE>",
        "QC_API_URL": "https://api-dev.quickcreator.io/ai-blog-chat-service"
      }
    }
  }
}
```

**OpenCode**: Edit project `opencode.json` or `~/.config/opencode/opencode.json`:
```json
{
  "mcp": {
    "quickcreator-skill": {
      "type": "local",
      "command": ["npx", "-y", "@quickcreator/skill-mcp"],
      "enabled": true,
      "environment": {
        "QC_API_TOKEN": "<DEVELOPER_KEY_HERE>",
        "QC_API_URL": "https://api-dev.quickcreator.io/ai-blog-chat-service"
      }
    }
  }
}
```
OpenCode uses a different config format: root key is `"mcp"` (not `"mcpServers"`), requires `"type": "local"`, command is a single array (not separate `command`/`args`), and env vars use `"environment"` (not `"env"`). If `opencode.json` already has other settings (model, theme, etc.), merge the `"mcp"` field without overwriting existing content.

**TOML agents** (Codex): Edit `~/.codex/config.toml`:
```toml
[mcp_servers.quickcreator-skill]
command = "npx"
args = ["@quickcreator/skill-mcp"]
env = { QC_API_TOKEN = "<DEVELOPER_KEY_HERE>", QC_API_URL = "https://api-dev.quickcreator.io/ai-blog-chat-service" }
```

If the config file already exists, **merge** the entry without overwriting other content.

### Step 3: Notify Restart (ONE Combined Message)

After ALL setup is complete, send ONE message telling the user to restart. Include how to invoke the skill after restart:

| Agent | Restart message (adapt to user's language) |
|-------|---------------------------------------------|
| Cursor | "All set! Please restart Cursor. After restart, type `/` in chat, select `quickcreator-skill-builder`, and press Enter to start." |
| OpenCode | "All set! Please restart OpenCode. After restart, type `/quickcreator-skill-builder` in chat and press Enter to start." |
| Claude Code | "All set! Please restart Claude Code. After restart, just tell me you want to create or manage skills." |
| Windsurf | "All set! Please restart Windsurf to activate the connection." |
| OpenClaw | "All set! Please restart OpenClaw to activate the connection." |
| Codex | "All set! Please restart Codex to activate the connection." |

**IMPORTANT:** Send only ONE restart message at the very end. Never prompt restart after individual steps.

### Step 4: Verify Connection (After Restart)

When the user returns after restart, silently call `list_skills(category="personal")`.
- If it succeeds → Tell the user: "Connection is ready! Let's get started."
- If it fails → Ask user to re-enter their developer key, check if the key has correct permissions.

---

## How to Invoke This Skill

When guiding users (in their language), explain how to use this skill next time:

| Agent | Instructions |
|-------|-------------|
| Cursor | In the chat window, type `/`, then select or type `quickcreator-skill-builder` and press Enter |
| OpenCode | In the chat window, type `/quickcreator-skill-builder` and press Enter |
| Claude Code | Just mention that you want to create or manage QuickCreator skills |
| Other agents | Just ask about creating or managing QuickCreator skills in conversation |

---

## Skill Development Workflow

### Welcome & Intent Discovery

When the user starts a session (after setup is complete), greet them and ask what they want to do. Adapt language to the user. Example in Chinese:

> 欢迎使用 QuickCreator Skill Builder！你今天想做什么？
>
> 1. **创建新技能** — 从你的想法开始，打造一个全新的技能
> 2. **浏览技能市场** — 看看其他人发布了哪些技能
> 3. **编辑我的技能** — 修改你已有的技能
> 4. **发布技能** — 把你的技能分享到技能市场
> 5. **其他操作** — 安装、复制或删除技能

### Create a New Skill

#### Inferring from Conversation Context

If previous conversation provides context (e.g., the user described a workflow, demonstrated a process, or discussed a problem), **proactively offer** to turn that into a skill:
> "Based on what we just discussed, I can create a skill that [does X]. Would you like me to build it?"

This saves the user from re-explaining. Skip directly to Phase 2 if enough context exists.

#### Phase 1: Discovery

Have a natural dialogue. Ask ONE question at a time — never dump all questions at once. Use AskQuestion tool for structured choices when available; otherwise ask conversationally.

1. **Purpose**: "What do you want this skill to help people accomplish?"
2. **Target users**: "Who would use this skill? What problem does it solve for them?"
3. **Workflow steps**: "Walk me through the ideal process step by step."
4. **Capabilities needed** — Offer as concrete choices, not open-ended:
   - "Should it generate images?"
   - "Should it search the internet for information?"
   - "Should it ask the user questions during the process?"
   - "Should it access the user's knowledge base?"
   - "Should it create videos?"
5. **Output expectations**: "What should the final result look like? Any specific format or style?"
6. **Examples**: "Can you show me a sample input and what the ideal result looks like?"

If the user wants inspiration, search existing skills: `search_marketplace(tag=...)` or `list_skills(category="builtin")` and present relevant ones in plain language.

#### Phase 2: Design

The agent silently designs the skill, then presents a brief summary for confirmation:

> "Here's what I'll build: **[skill concept in user's language]**. It will [do X, Y, Z]. Does that sound right?"

Wait for user confirmation before proceeding. If the user wants adjustments, iterate on the design.

Internally, the agent:
1. Generates a valid `name` (lowercase, hyphens, ≤64 chars)
2. Writes an English `description` (≤1024 chars, WHAT + WHEN + triggers) — translate from user's language if needed
3. Selects appropriate content patterns (see Skill Content Patterns in Agent-Internal section)
4. Plans the file structure

#### Phase 3: Build

The agent silently creates the skill:
1. `create_skill(name=..., description=...)`
2. `create_skill_file(...)` — SKILL.md with proper frontmatter and content using selected patterns
3. Adds reference files or scripts as needed

#### Phase 4: Review & Iterate

Present the result in plain language: "Your skill is ready! Here's what it does: [summary in user's language]."

Ask: "Would you like to adjust anything, or publish it right away?"

If the user wants changes, iterate using `update_skill_file(...)` until satisfied. Each time, confirm the change: "Done! Here's what I updated: [change summary]."

### Browse & Search the Marketplace

- Call `list_skills(category="marketplace")` or `search_marketplace(tag="...")`
- Present results as a clean, readable list: skill name + what it does
- NEVER show skill IDs, file paths, or technical metadata to the user
- If user wants details: call `get_skill(skillId=...)` and summarize in plain language

### Create a Copy from an Existing Skill

Tell the user: "I'll create a personal copy of this skill so you can customize it."

1. Call `fork_skill(skillId=..., source=...)` — internally handle the correct source type
2. Call `get_skill(skillId="p_...")` to inspect the copy
3. Ask the user what they want to change
4. Call `update_skill_file(...)` to apply changes
5. Confirm: "Your customized version is ready!"

### Edit an Existing Skill

1. Call `list_skills(category="personal")` — show user their skills in a simple list
2. User picks which skill to edit
3. Call `get_skill(skillId="p_...")` — summarize current content for the user
4. Ask what they want to change
5. Call `update_skill_file(...)` — apply changes
6. Confirm: "Changes saved!"

### Publish to the Marketplace

The agent MUST silently run the pre-publish checklist (see Agent-Internal section) and fix any issues automatically before publishing. Never burden the user with checklist details.

1. Ask for author name and relevant tags (suggest tags based on skill content)
2. Call `publish_skill(personalSkillId=..., authorName=..., tags=[...], version="1.0.0")`
3. Confirm: "Your skill is now live on the marketplace! Others can find and install it."

For updating an already-published skill:
1. Call `update_published_skill(marketplaceSkillId=..., personalSkillId=...)`
2. Confirm: "Your skill has been updated!"

### Install a Marketplace Skill

1. Call `install_skill(marketplaceSkillId=...)`
2. Confirm: "Installed! This skill is now available in your collection."

### Delete a Skill

Always confirm: "Are you sure you want to delete this skill? This action cannot be undone."
Then call `delete_skill(personalSkillId=...)`.

---

## Agent-Internal: Technical Reference

**Everything below is for the agent's internal use. NEVER expose these details to the user.**

### MCP Tool Usage Rules

1. **Read the tool schema before first use** — check descriptor files for required fields and enums.
2. **Always pass `arguments` object** — even when only one field is required:
   ```json
   { "server": "quickcreator-skill", "toolName": "list_skills", "arguments": { "category": "personal" } }
   ```
3. **Respect enum values exactly** — e.g., `category` must be one of: `personal`, `builtin`, `marketplace`, `installed`.
4. **On validation errors**, re-read the tool schema and fix. Never retry blindly.

### MCP Tools Quick Reference

| Tool | Key Arguments |
|------|--------------|
| `list_skills` | `category` ∈ personal / builtin / marketplace / installed |
| `search_marketplace` | `tag` (string), optional `sortBy` |
| `get_skill` | `skillId` |
| `get_skill_file` | `skillId`, `filePath` |
| `create_skill` | `name`, `description` (optional) |
| `fork_skill` | `skillId`, `source` ∈ marketplace / builtin / installed |
| `update_skill_file` | `skillId`, `filePath`, `content` |
| `create_skill_file` | `skillId`, `filePath`, `content` |
| `delete_skill` | `personalSkillId` |
| `publish_skill` | `personalSkillId`, `authorName`, `tags`, `version` |
| `update_published_skill` | `marketplaceSkillId`, `personalSkillId` |
| `install_skill` | `marketplaceSkillId` |
| `uninstall_skill` | `installedSkillId` |

### Skill ID Prefixes

| Prefix | Type |
|--------|------|
| `sk_` | Built-in (read-only) |
| `mk_` | Marketplace (published) |
| `p_` | Personal (editable) |
| `i_` | Installed (read-only) |

### Pre-Publish Checklist (Agent Enforced Silently)

Fix all issues automatically. Never show this checklist to the user.

- `name`: lowercase a-z, 0-9, hyphens only; ≤64 chars; no leading/trailing/consecutive hyphens
- `description`: English, ≤1024 chars, describes WHAT + WHEN + trigger keywords
- All SKILL.md content in English (except preserved non-English text in original prompts)
- No hardcoded API keys or secrets (use environment variables)
- Valid YAML frontmatter with `name` and `description`
- SKILL.md body under 500 lines
- Reference files one level deep
- `requirements.sh` present if `scripts/` directory exists
- Consistent terminology throughout
- Follows [Agent Skills spec](https://agentskills.io)

### Skill Content Generation Guidelines

When writing SKILL.md content for the user's skill, follow these principles:

**Conciseness first**: Only include information the agent wouldn't already know. Every paragraph must justify its token cost. Avoid explaining what common tools do — just say how to use them.

**Progressive disclosure**: Put essential step-by-step instructions in SKILL.md. Detailed API references, extensive examples, or supplementary docs go in separate files (reference.md, examples.md) linked from SKILL.md. Keep references one level deep.

**Match freedom to fragility**:
- **High freedom** (text guidelines) — multiple valid approaches (e.g., content review, creative writing)
- **Medium freedom** (templates/outlines) — preferred pattern with acceptable variation (e.g., report generation)
- **Low freedom** (exact scripts/steps) — consistency is critical (e.g., data pipelines, image specs)

### Skill Content Patterns

Select the best pattern based on what the skill does. Combine patterns as needed — most skills benefit from Workflow + Template.

**Template Pattern** — skill produces structured output:
```
## Output format
# [Title]
## Summary: [one-paragraph overview]
## Details: [structured content]
```

**Workflow Pattern** — skill follows sequential steps:
```
## Process
Step 1: [Action] — [what to do and why]
Step 2: [Action] — [what to do and why]
Step 3: [Action] — [what to do and why]
```

**Conditional Pattern** — skill handles different scenarios:
```
## Determine the approach
**Scenario A?** → Follow "Approach A"
**Scenario B?** → Follow "Approach B"
```

**Examples Pattern** — output quality depends on seeing examples:
```
## Examples
**Input:** [sample input]
**Output:** [expected output]
```

**Feedback Loop Pattern** — quality verification is needed:
```
## Process
1. Generate the output
2. Validate the result
3. If issues found → fix and re-validate
4. Only proceed when validation passes
```

### Available Platform Tools for Generated Skills

Skills running on QuickCreator can use these built-in tools. See [tool-reference.md](tool-reference.md) for full parameter reference.

| Tool | Capability |
|------|-----------|
| `nano-banana-pro-image` | Image generation (text-to-image, image-to-image) |
| `openai-image` | AI image generation from text prompts |
| `query_image_from_knowledge_base` | Retrieve images from user's knowledge base |
| `query_question_from_knowledge_base` | Retrieve information from user's knowledge base |
| `query_question_from_web` | Web search and research |
| `ask_questions_to_user` | Structured user input collection |
| `shell_execute` | Run bash scripts in sandbox |
| `code_execute` | Run Python or JavaScript in sandbox |

Video generation uses Google Veo SDK via `code_execute`. See [scripts/generate_video.py](scripts/generate_video.py) and [tool-reference.md](tool-reference.md).

### Skill File Structure

```
skill-name/
├── SKILL.md              # Required — main instructions
├── reference.md          # Optional — detailed docs
├── examples.md           # Optional — usage examples
├── requirements.sh       # Required if scripts/ exists
└── scripts/              # Optional
    └── helper.py
```

### SKILL.md Template

```markdown
---
name: my-skill-name
description: Does X when the user needs Y. Use when working with Z or when the user mentions A, B, or C.
---

# My Skill Name

## Instructions
Step-by-step guidance for the agent.

## Examples
Concrete usage examples.
```

### Complete Example (Agent Reference)

A well-structured skill for the QuickCreator platform:

```markdown
---
name: product-social-post
description: Generate social media posts with AI images for product promotion. Use when the user needs product marketing content, social media posts, or promotional images for Instagram, Facebook, or Twitter.
---

# Product Social Post

## Instructions

1. Ask the user which product they want to promote. Use `ask_questions_to_user` with:
   - Product name (short answer)
   - Target platform (single choice: Instagram / Facebook / Twitter)
   - Tone (single choice: Professional / Casual / Playful)

2. Search for product information using `query_question_from_knowledge_base` with the product name.

3. Generate a promotional image using `nano-banana-pro-image` with a prompt based on the product and selected tone.

4. Write platform-appropriate post copy:
   - Instagram: visual-first, hashtags, emoji
   - Facebook: conversational, longer format
   - Twitter: concise, punchy, under 280 chars

5. Present the image and copy to the user for review.

## Examples

**Input:** Product: "CloudSync Pro", Platform: Instagram, Tone: Professional
**Output:**
- Image: Clean product mockup with gradient background
- Copy: "Seamless collaboration starts here. CloudSync Pro keeps your team in sync — anywhere, anytime. #CloudSync #Productivity #TeamWork"
```

Full development standards: [skill-standards.md](skill-standards.md)
