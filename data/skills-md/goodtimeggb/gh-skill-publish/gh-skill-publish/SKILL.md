---
name: gh-skill-publish
displayName: GitHub 发布开源 Skill 流程
version: 1.0.3
description: 把 WorkBuddy 自建 skill 发布到 GitHub 公开仓库并上架 SkillHub 的标准流程。当用户想把本地开发的 skill 推送到 GitHub 开源、添加 LICENSE、打版本 tag 与 GitHub Release、或通过 SkillHub 绑定 GitHub 让他人在 WorkBuddy 客户端搜到并安装时使用。覆盖本地 git 初始化、gh 创建公开仓库、LICENSE、annotated tag + Release、SkillHub 导入与后续增量同步。
agent_created: true
---

# GitHub 发布 Skill 标准流程

## Overview

本 skill 沉淀「把 WorkBuddy 自建 skill 推到 GitHub 公开仓库 + 开源规范化 + 上架 SkillHub」的可复用流程。核心目标：让其他人能在 WorkBuddy 客户端的技能市场搜到并一键安装该 skill。

SkillHub 是 WorkBuddy 内置技能市场（代码层叫 BuiltinMarket）。要让用户在 WorkBuddy 里搜到，**必须上架 SkillHub**；通过「绑定 GitHub 账号 → 选仓库导入」是最省事的方式，无需反复传 zip。

## 适用场景

- 用户完成一个 skill 开发，想对外发布或开源
- 用户要把 skill 推送到 GitHub 公开仓库
- 用户要为 skill 补 LICENSE、打版本 tag、建 Release
- 用户想通过 SkillHub 让他人在 WorkBuddy 搜到并安装

## 前置检查

执行流程前先确认：

- `gh` CLI 已登录，且目标 GitHub 账号对仓库有写权限：`gh auth status`
- skill 目录含规范文件：
  - `SKILL.md`：frontmatter 含 `name` / `description` / `version` / `agent_created: true`
  - `manifest.yaml`：`name` / `slug` / `version` / `description` / `author` / `category` / `tags` / `triggers` / `license` / `icon` / `permissions`
  - `README.md`、`icon.png`（512×512）
- 仓库根是 skill 根（`SKILL.md` / `manifest.yaml` 在仓库根），便于 SkillHub 直接读取

## 流程步骤

1. **本地 git 初始化与排除**：在 skill 目录 `git init -b main`，写 `.gitignore` 排除 `output/`、`.git`、`__pycache__`、`.workbuddy` 等本地产物，保持仓库即 skill 本体。
2. **创建公开仓库并推送**：用 `gh repo create <owner>/<name> --public --source . --remote origin --push` 一次性创建并推送。
3. **添加 LICENSE**：写 MIT（或选其他）`LICENSE` 文件，署名与 `manifest.author` 一致，提交并推送。
4. **打 tag + GitHub Release**：`git commit` 到 `main` 后，用 `gh release create vX.Y.Z --title "vX.Y.Z" --notes "..."` 自动创建 annotated tag 并发布 Release。
5. **SkillHub 绑定 GitHub 导入上架**：登录 SkillHub → 绑定 GitHub → 选仓库导入（自动读取 `manifest.yaml` / `SKILL.md` / `icon.png`）→ 提交审核（1–3 工作日）→ 上架。
6. **后续增量更新**：之后 skill 有改动，本地 `git commit` + `git push`，SkillHub 重新同步即可，无需重传 zip。

完整命令模板与逐字段说明见 `references/publish-checklist.md`。

## 关键陷阱（必读）

- `gh repo create` **不支持** `--yes`，用 `--source . --remote origin --push` 替代。
- GitHub API 读取偶发 `EOF`（reading/view/list），但 `gh release create` 返回正式 URL 且退出码 0 即成功，勿因读取报错误判失败；用 `git ls-remote --tags` 验证 tag 即可。
- `init_skill.py` 在 Git Bash 下对 `/c/...` 路径有 MSYS 转换 bug，会误建 `C:\c\...` 双层前缀目录。改用 Windows 原生路径（如 `C:/Users/...`）执行，或在 Bash 创建后手动移动到 `C:\Users\Administrator\.workbuddy\skills\`，并清理误建的 `C:\c` 垃圾树。
- `.gitignore` 必须排除 `output/` 等本地产物，避免仓库变成「skill 本体 + 产物」冗余，且打包 zip 时也要排除 `output/`（防递归膨胀）。
- 图像生成（如 skill 封面图）并行多图时输出文件名时间戳相同会互相覆盖，必须**串行生成 + 立即重命名**。

## Resources

- `references/publish-checklist.md`：完整命令模板、manifest 字段清单、SkillHub 表单填写指引、踩坑对照表。
