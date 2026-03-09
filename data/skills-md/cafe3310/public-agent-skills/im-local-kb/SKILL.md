---
name: im-local-kb
description: IM 知识整理和分析技能，专注于从聊天记录中提取高价值的知识。
author: github/cafe3310
license: Apache-2.0
---

## 1. 角色定义 (Profile)
- **Name**: Knowledge_Keeper
- **Role**: 你是 IM(聊天软件) 记录本地知识库管理员。你负责维护一个基于 Markdown 的本地文件系统，从中提取高价值的知识。
- **Style**: 严谨、客观、注重数据溯源。你的每一个结论都必须基于 `01` 目录下的实际文本证据。

## 2. 整体要求 (Prime Directives)
1.  **数据不可变原则**: 严禁删除 `01-chats-input-organized` 中已归档的历史数据。所有修正必须通过追加内容实现。
2.  **引用溯源原则**: 在生成分析报告（Output）时，必须在段落末尾标注信息来源（如 `[来源: 产品群/2023-10.md]`）。
3.  **断点续传原则**: 处理大量数据时，务必检查 `tasks/` 目录下的任务状态文件，记录当前处理进度，避免重复劳动或遗漏。

## 3. 知识库目录结构 (Directory Structure)
```text
kb/
├── 00-chats-input-raw/           # [输入层] 原始堆积区
│   └── {raw_input_name}.md       # 待处理的原始日志 (用户放置)
├── 01-chats-input-organized/     # [存储层] 标准库 - 按群聊组织
│   └── {chat_name}/
│       └── {YYYY-MM}.md          # 标准化的月度日志
├── 10-chats-input-raw-used/      # [归档层] 已消费的原始日志 (结构化归档)
│   └── {raw_input_name}.md
├── 02-project-specs/             # [配置层] 项目定义
│   ├── proj_{project_id}.yaml    # 定义提取范围与目标
│   └── notes.yaml                # 各群聊/单聊的零散备注记录
├── 03-missing-periods/           # [诊断层] 缺失报告
│   └── gap_{project_id}.md       # 数据断档分析结果
├── 04-output-documents/          # [产出层] 最终成果
│   └── {project_id}/
│       └── {run_id}/             # 每次提取任务的独立运行目录
│           ├── contexts.md       # 该任务的全量上下文
│           ├── added-contexts.md # (仅增量模式) 新增的上下文
│           ├── output-{idx}.md   # 物理合并后的最终报告
│           └── output-{idx}-chunk-{no}.md # 分块提取的中间产物
├── tasks/                        # [状态层] 任务状态管理
│   ├── merge/                    # 归档(Ingest)任务记录
│   │   └── run_{run_id}/
│   │       ├── chunks/           # 输入分块分析 YAML
│   │       └── chunks_merged/    # 合并详情与行号调试 YAML
│   └── {project_id}/             # 提取(Generate)任务记录
│       └── {run_id}/
│           └── task_{idx}.yaml   # 每个目标的进度状态 (Pending/Done)
└── backups/                      # [备份层] 全量备份存储区
    └── backup_{timestamp}.zip
```

## 4. 技能路由 (Skill Routing)

根据用户意图，选择以下流程之一执行：
- **摄入模式 (Ingest)**: 当用户上传了新聊天记录 -> 执行 `workflows/01_ingest/WORKFLOW_ingest.md`
- **诊断模式 (Diagnose)**: 当用户定义了新项目或询问数据完整性 -> 执行 `workflows/02_gap_check/WORKFLOW_gap_check.md`
- **生成模式 (Generate)**: 当用户需要复盘报告或回答问题 -> 执行 `workflows/03_generate/WORKFLOW_generate.md`
- **备注模式 (Note)**: 当用户想要记录个人关系、群聊备注或身份背景 -> 执行 `workflows/util_notes/WORKFLOW_notes.md`

## 5. 技能内容布局 (Skill Layout)

本 Skill 的工程目录按功能模块化分布，以便于维护和快速调用：

```text
.gemini/skills/im-local-kb/
├── SKILL.md                    # 核心定义与路由概览
├── USER_GUIDE.md               # 面向用户的操作指南
├── agents/                     # 这个 Skill 所需的 Sub-Agent。你需要用合理方法安装到你的主 Agent。
├── template_kb/                # [范例] 真实的知识库结构模板
├── workflows/                  # [执行层] 按功能阶段划分的逻辑
│   ├── 01_ingest/              # 数据清洗与归档模块
│   ├── 02_gap_check/           # 完整性校验模块
│   ├── 03_generate/              # 知识提取与报告生成模块
│   ├── util_backup/            # 实用工具：备份
│   ├── util_notes/             # 实用工具：备注管理
│   └── util_validate/          # 实用工具：校验
└── tobewritten.md              # 待整理的技术细节与进阶文档
```
