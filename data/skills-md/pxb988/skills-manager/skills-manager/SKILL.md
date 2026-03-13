---
name: skills-manager
description: 管理 Claude Code 本地技能的工具。支持列出、查看、创建、删除、编辑、备份、搜索和描述 skills。
tags:
  - skills
  - management
  - cli
  - utilities
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
license: MIT
custom_instructions: |
  # Skills Manager - Claude Code 技能管理器

  ## 核心原则（必须遵守）

  > **中心化存储 + 符号链接分发**：所有技能操作必须以 `~/.agents/skills/` 为中心仓库。
  > 绝不直接在 `~/.claude/skills/` 或任何助手目录中创建/修改/删除技能源文件。
  > 助手目录中只允许存在指向中心仓库的符号链接/Junction。

  ### 操作流程强制约束
  - **创建技能** → 先在 `~/.agents/skills/<name>/` 创建，再映射到各助手
  - **安装技能** → 下载/克隆到 `~/.agents/skills/`，然后创建符号链接到各助手
  - **删除技能** → 先清理所有助手的符号链接/Junction，再删除 `~/.agents/skills/<name>/`，最后更新 `.skill-lock.json`
  - **修改技能** → 只修改 `~/.agents/skills/<name>/` 中的文件，符号链接会自动同步
  - **打包技能** → 完成后必须主动提醒用户是否需要映射到各 AI 助手

  ### Windows 平台注意事项
  - Windows 不支持 `ln -sf`（需管理员权限），必须使用 PowerShell 的 `New-Item -ItemType Junction`
  - Junction 不需要管理员权限，是 Windows 上的最佳选择
  - 脚本会自动检测 OS 并选择正确的链接方式

  ## 触发条件
  当用户需要管理本地 skills 时使用此技能，包括但不限于：
  - 添加技能到 .agents 系统
  - 列出已安装的 skills
  - 查看 skill 的详细信息
  - 创建新的 skill
  - 删除/卸载 skill
  - 编辑现有 skill
  - 备份/恢复 skill
  - 搜索 skills
  - **描述/生成 skill 的功能说明**
  - **打包并安装技能后主动提醒映射**

  ## 添加技能实现细节

  当用户要求添加技能时，按以下步骤执行：

  ### 1. 解析源类型
  ```bash
  if [[ "$source" =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$ ]]; then
    source_type="github"; repo_url="https://github.com/$source"
  elif [[ "$source" =~ ^https?:// ]] || [[ "$source" =~ ^git@ ]]; then
    source_type="git"; repo_url="$source"
  else
    source_type="local"; local_path="$source"
  fi
  ```

  ### 2. 安装到 .agents 中心仓库
  ```bash
  agents_skills_dir="$HOME/.agents/skills"
  skill_dest="$agents_skills_dir/$skill_name"
  mkdir -p "$agents_skills_dir"
  # 复制或克隆到中心仓库
  ```

  ### 3. 更新 .skill-lock.json
  ### 4. 检测 AI 助手并创建符号链接/Junction

  ```bash
  # 检测 OS
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) os_type="windows" ;;
    *)                     os_type="unix" ;;
  esac

  # 为每个助手创建链接
  if [ "$os_type" = "windows" ]; then
    powershell.exe -NoProfile -Command "New-Item -ItemType Junction -Path '<target>' -Target '<source>'"
  else
    ln -sf "$skill_dest" "$agent_skill_dir/$skill_name"
  fi
  ```

  ## 技能目录体系（三级）

  按优先级排序：
  - **中心仓库 (最高优先级)**: `~/.agents/skills/` — 所有技能的唯一数据源
  - **主技能目录**: `~/.claude/skills/` — 通过符号链接/Junction 指向中心仓库
  - **市场技能目录**: `~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/`

  ## 标准 Skill 结构

  ```
  skill-name/
  ├── SKILL.md              # 必需 - 技能定义文件
  ├── README.md            # 可选
  ├── scripts/             # 可选
  └── assets/              # 可选
  ```

  ## 常用操作命令

  ### 列出所有 Skills
  ```bash
  ls -la "$HOME/.agents/skills"    # 中心仓库（推荐）
  ls -la "$HOME/.claude/skills"    # 主技能目录
  ```

  ### 创建新 Skill
  ```bash
  ~/.claude/skills/skills-manager/scripts/create-skill.sh -n <name> -d "<description>"
  ```
  ```powershell
  ~\.claude\skills\skills-manager\scripts\create-skill.ps1 -Name <name> -Description "<description>"
  ```

  ### 添加技能到 .agents 系统

  **Bash 版（Linux/macOS/Windows Git Bash）:**
  ```bash
  ~/.claude/skills/skills-manager/scripts/add-skill.sh [OPTIONS] <source>
  ```

  **PowerShell 版（Windows 原生）:**
  ```powershell
  ~\.claude\skills\skills-manager\scripts\add-skill.ps1 -Source <source> [-Agent <name>] [-Force] [-DryRun]
  ```

  ## 使用方式

  用户可以通过自然语言指令来管理 skills，例如：
  - "添加 skill-name 到 .agents 系统"
  - "从 GitHub 添加 owner/repo"
  - "列出所有已安装的 skills"
  - "创建一个名为 my-new-skill 的 skill"
  - "删除旧的 test-skill"
  - "备份所有 skills"
  - "搜索包含 'pdf' 关键字的 skills"
  - **"描述 my-awesome-skill 这个 skill 是做什么的"**

  ## 注意事项

  1. 技能目录有三个层级（中心仓库 > 主目录 > 市场目录）：
     - 中心仓库: `~/.agents/skills/` — 唯一的数据源
     - 主技能目录: `~/.claude/skills/` — 只存放符号链接/Junction
     - 市场技能目录: `~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/`
  2. 删除 skill 前请确认不再需要，或者已做好备份
  3. 编辑 SKILL.md 时确保 YAML 格式正确
  4. 创建新 skill 时至少需要包含 SKILL.md 文件
  5. 市场技能 (anthropic-agent-skills) 通常是只读的，修改后可能被覆盖
  6. 用户自定义技能应通过 `.agents` 中心仓库管理
  7. **中心仓库是唯一数据源**: 修改技能只需修改 `~/.agents/skills/` 中的文件，所有助手通过链接自动同步

metadata:
  trigger: 用户需要管理本地 Claude Code skills 时
  source: Custom skill for managing local Claude Code skills
  version: 1.1.0
---

# Skills Manager

这是一个用于管理 Claude Code 本地技能的工具。

## 功能

- **添加技能**: 将技能添加到 .agents 系统，自动映射到所有 AI 助手
- **列出技能**: 显示所有已安装的 skills 及其基本信息
- **查看详情**: 查看某个 skill 的完整信息和内容
- **创建技能**: 快速创建新的 skill 模板
- **删除技能**: 安全地卸载不需要的 skills
- **编辑技能**: 修改现有 skill 的配置和内容
- **备份技能**: 导出技能存档
- **搜索技能**: 按名称或描述搜索 skills
- **描述技能**: 分析和解释 skill 的功能、用途和使用场景

使用时直接用自然语言描述你的需求即可，例如：
- "添加 skill-name 到 .agents 系统"
- "列出所有 skills"
- "创建一个新的 skill"
- "描述 my-awesome-skill 这个 skill"
