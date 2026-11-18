---
name: soia-pkm-organize-article-moc
description: 将 Obsidian 文章库按元数据、主题双链、月份和两级 MOC 规范化整理。触发：「整理文章库」「重建 MOC」「收藏归类」
version: 2.1.2
created_at: 2026-07-02 17:57:11
updated_at: 2026-11-18 10:30:00
created_by: claude opus 4.6
updated_by: gemini-4-hydrogen
---

# soia-pkm-organize-article-moc

PKM 闭环 `clip → ★organize → distill → compose → publish` 的**整理与 MOC 同步环节**：补齐元数据、按主题双链与月份归位并增量维护两级 `_MOC/`。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 整理单篇新归档文章（默认闭环） | 补摘要/`topics`/`captured_at`/`author`，按月归位并调 `rebuild_moc.py --article` 增量同步两级 MOC 与地图 | 文章终路径、受影响 MOC 与地图/Base 校验回执 |
| 盘点或全量重建文章库 `_MOC/` | 先 `rebuild_moc.py --full-rebuild --dry-run` 审查未知 topic，确认后同盘原子替换 `_MOC/` | 总篇数、主题分布与未知 topic 报告 |

### 客户如何使用

- 「把刚归档的这篇 X 文章整理归位，并增量同步 MOC。」
- 「先 dry-run 检查一下文章库的 MOC 有没有未知主题或未按月归位的文件。」

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-pkm-vault-skills -a <agent> -s soia-pkm-organize-article-moc`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-pkm-vault@soia`（Codex 用 `codex plugin add soia-pkm-vault@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。配置 `~/.config/soia-skills/soia-pkm-organize-article-moc/config.yml` 或 `$SOIA_PKM_ORGANIZE_ARTICLE_MOC_CONFIG_FILE`（纯本地操作无需联网）。

### 私密信息与中间数据

仅读写目标 vault 文章目录、`_MOC/` 与 `.categories.json`；全量重建先在同盘暂存目录成功后再原子替换，无凭据外泄风险。

### 日志与完成回执

汇报篇数、补全的 `topics`、归位与 MOC 增量/重建详情、`OB知识库地图` 更新与 `.base` 验证及未完成项；整理失败时严禁把「已归档」包装成「已整理」。

## 整理规程与脚本边界

1. **批量 vs 单篇审批边界**：批量移动/改名先读 [references/知识库整理规程.yml](references/知识库整理规程.yml) 只读盘点并确认计划；单篇随 `clip-web`/`clip-wechat-article` 默认自动收口不重复审批，但**单篇严禁调用 `--full-rebuild` 清空重建**（用户说“仅归档”时停在 clip）。
2. **元数据与移动安全**：优先复用 `_MOC/` 已有分类（无人物笔记的 `people` 保留纯文本，不造空占位页，带小数点文件名按完整路径解析）；未知附件只记“附件缺失”不造假链接。按文件名日期从 `<年>/` 移入 `<年>/<月>/` 前须生成逐文件 SHA-256 清单，不用裸 `mv`。
3. **底层脚本**：
   - `python3 scripts/rebuild_moc.py --article <path>`：单篇增量同步受影响的一/二级 MOC（未知 topic 先阻断，优先更新 `_MOC/.categories.json` 后重试）。
   - `python3 scripts/rebuild_moc.py --full-rebuild [--dry-run] [--allow-unknown-topics]`：先 dry-run 报告再原子全量替换（无 `--article`/`--full-rebuild` 直接拒绝运行）。书库侧另配 `soia-pkm-library-book-catalog/scripts/backfill_reading_records.py`。
4. **索引门禁**：凡路径变化或增删文件，按 `soia-pkm-maintain-vault-health/references/index-sync-contract.md` 立即重建全库地图，涉及 `20_资料库/` 再验 `.base`。

## 验证与前向测试

改后运行仓库 `unittest`（`tests/` 覆盖参数、去重、落盘与未知 topic 阻断）与 `audit_skills.py --strict`。
