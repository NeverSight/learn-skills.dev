---
name: fagi-update
description: |
  FAGI 更新器。用户说「更新 FAGI」「升级 FAGI」「把 FAGI 更新到最新版」「检查 FAGI 更新」或输入 /fagi-update 时使用。只同步 edccyf-web/FAGI-XHS 仓库，不更新用户安装的其他 Skill，不修改用户的个人规则库和存档。
  Update FAGI when the user asks to update, upgrade, or check updates for FAGI.
---

# fagi-update：更新 FAGI

用户已经明确要求更新 FAGI。直接执行更新，不再做第二次文字确认；宿主若要求 Shell 权限，由用户在宿主的权限窗口中决定。

## 更新范围

- 只从目标仓库 `edccyf-web/FAGI-XHS`（https://github.com/edccyf-web/FAGI-XHS）更新。
- 保留用户在各 skill 的 `data/` 目录中的个人规则库、审查历史、踩坑案例、词库文件。
- 保留用户项目的 `.workbuddy/skills/` 符号链接配置。
- 不更新用户安装的其他 Skill。
- 不创建后台任务、定时任务或 Agent Hook。

## 受保护的个人数据（更新时不覆盖）

以下路径是用户的个人资产，更新时必须保留，不覆盖、不删除：

| skill 目录 | 受保护路径 | 内容 |
|---|---|---|
| `fagi-publish-precheck/` | `data/profile.md` | 用户账号画像 |
| `fagi-publish-precheck/` | `data/my-rules.md` | 个人黑名单/白名单/语义规则 |
| `fagi-publish-precheck/` | `data/expressions.md` | 安全表达库（实测改写对） |
| `fagi-publish-precheck/` | `data/wordlists/` | 个人大词表 |
| `fagi-publish-precheck/` | `data/history/` | 审查历史报告 |
| `fagi-publish-precheck/` | `data/cases/` | 被罚案例存档 |
| `fagi-xhs-dual-account-strategist/` | `data/` | 行业映射等用户配置 |
| 所有 skill | `data/` 目录下除 `README.md` 和 `templates/` 外的所有文件 | 用户运行时产生的数据 |

## 执行步骤

1. **识别 FAGI 安装位置**：全局更新时，Codex 使用 `~/.codex/skills/`，WorkBuddy 使用 `~/.workbuddy/skills/`；若用户明确要求更新某个 FAGI 项目，按该项目 `SOURCE_OF_TRUTH.md` 定位 `skills/` 真源。只处理 `fagi` 主入口和 `fagi-*` 子 skill。遇到指向项目真源的符号链接时，在真源更新内容，保留链接本身。

2. **记录保护范围**：记录各安装位置的个人 `data/` 和符号链接。第4步脚本执行前会将现有个人数据及待覆盖文件备份到安装目录外的恢复目录，默认只读计划不产生备份。

3. **从 GitHub 拉取最新版本**：

   ```bash
   git clone --depth 1 https://github.com/edccyf-web/FAGI-XHS.git /tmp/fagi_update_<timestamp>/
   ```

   本仓库的唯一真源为 `skills/fagi/`，直接使用该目录。不要从原始快照或旧压缩包更新。

4. **更新并去重**：使用本 skill 的 `scripts/sync_skills.py`，从已拉取的发布包更新；不使用当前安装的旧脚本。`--source` 指向仓库的 `skills/fagi/`，每个 `--root` 是一个宿主的安装目录：

   ```bash
   python3 <仓库>/skills/fagi/fagi-update/scripts/sync_skills.py --source <仓库>/skills/fagi --root ~/.codex/skills --root ~/.workbuddy/skills
   # 确认计划无 blocked 后，对同一命令加 --apply 执行已授权更新。
   ```

   - 只传入实际存在且用户要求更新的宿主目录；不创建没有使用的其他宿主安装。
   - 默认只输出计划；用户已要求更新时，计划无冲突即可直接用 `--apply`，无需再问一次。
   - 按发布包主入口 `package.json` 的 `fagi.agents` 确定同步白名单，主入口自身单独计入；保留独立子 skill 安装，不嵌套复制。完整同步 `agents/`、`tests/` 等资源。
   - **去重单位是同一宿主安装目录**：按 `SKILL.md` 的 frontmatter name 确认同一 skill，检查根目录旧版别名和 `fagi/` 内的嵌套副本。不按目录名相似或功能相似删除，不把 Codex 与 WorkBuddy 各自安装的一套当作重复。
   - 只将已确认同名且不高于远端发布版本的旧版副本，或内容完全一致的同版副本，从活动加载目录移到安装目录外的 `fagi-skill-backups/<时间戳>/duplicates/`。这是移除活动副本，可恢复；不永久销毁。
   - 同版内容不同、版本未知且内容不一致、存在更高本地版本、链接引用或个人数据冲突时，输出 issues/blocked，不自动覆盖降级、不删除、不合并冲突数据。先完成无冲突的诊断并向用户报告具体差异。
   - 不覆盖现有 `data/`；旧副本仅有的数据可补入，已有同名数据相同则复用，不同则阻止操作。原有链接保持原样，通过链接更新真源，指向旧副本的链接不擅自改写。
   - 执行前在安装目录外备份个人数据和将覆盖的文件；安装内容与数据校验通过后才将重复副本移出，保留可恢复备份。

5. **验证安装与去重**：按发布清单检查 skill 身份和全部非 data 文件哈希，核对个人数据与原有链接保持不变。再次运行只读计划，应无待更新文件和无未处理重复项；有 blocked 或遗留项则如实说明，不能声称全部完成。无重复时报告“发现0个重复项”，不为凑结果删其他 skill。

6. **清理下载临时目录**：成功后可清理本轮拉取和解压的临时副本；安装目录外的恢复备份保留并告知路径，不能与下载缓存一起删除。

## 回复格式

成功：

> FAGI 已更新完成。当前对话如果还没有读取到新能力，新建一次对话后即可使用。
>
> 更新了以下 skill：
> - fagi（主入口）
> - fagi-xhs-competitor-analyzer（对标分析师）
> - fagi-xhs-keyword-planner（关键词研究员）
> - fagi-xhs-dual-account-strategist（双账号策略师）
> - fagi-xhs-title-optimizer（标题优化师）
> - fagi-xhs-note-writer（笔记作家）
> - fagi-xhs-compliance-check（合规检测官）
> - fagi-publish-precheck（发布前审查官）
> - fagi-xhs-data-review（数据复盘师）
> - fagi-update（更新器）
>
> 你的个人规则库（data/ 目录）已保留，无需重新配置。另说明移出活动目录的重复项数量、保留版本、冲突项（如有）和恢复备份位置。

失败：

> FAGI 没有更新完成：{简短原因}。处理完 {权限或网络问题} 后，再说一次「更新 FAGI」。

## 边界

- 用户只问版本、更新内容或是否需要更新时，先回答问题，不执行命令。
- 用户明确要求检查更新且希望实际同步时，按本 Skill 更新。
- 不更新非 FAGI 的其他 Skill（如 dbskill、khazix-skills 等）。
- 不修改用户的 `.workbuddy/skills/` 符号链接配置。
- 不修改用户项目的 `AGENTS.md`、`README.md`、`SOURCE_OF_TRUTH.md` 等项目级文件。
- 如果 GitHub 仓库结构变化导致 skill 目录名调整，更新前先告知用户变化，获得确认后再执行。
