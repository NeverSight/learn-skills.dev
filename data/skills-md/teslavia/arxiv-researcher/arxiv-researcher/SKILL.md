---
name: arxiv-researcher
description: |
  arXiv 科研与工程实验室（统一 CLI 版）。
  在 Claude Code 中通过自然语言或 `arxiv <subcommand>` 完成论文发现、初始化、精读、复现、工程化与贡献闭环。
  关键词：arXiv、paper、research、reproduce、工程化、复现、开源贡献。
---

# arXiv Researcher (Unified CLI)

## Claude Code 最新使用方式

优先使用以下两种方式：

1. `/arxiv-cli` 统一入口（推荐）
   - 例：`/arxiv-cli 搜索最近 7 天 speculative decoding 且有代码的论文`
2. 自然语言目标驱动
   - 例：“搜索最近 7 天 speculative decoding 且有代码的论文，并给出前三篇建议。”
3. 显式命令驱动
   - 例：“执行 `arxiv daily "speculative decoding" --days 7 --code-only` 并总结结果。”

说明：旧的 `/arxiv-*` 分散指令已迁移到统一入口 `/arxiv-cli`，底层执行命令为 `arxiv <subcommand>`。

## 安装

```bash
git clone https://github.com/teslavia/arxiv-researcher.git
cd arxiv-researcher
./install.sh
```

如果系统 Python 受限（PEP 668），使用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

## 统一命令入口

```bash
arxiv --help
```

主要子命令：

- `arxiv search` / `arxiv fetch` / `arxiv daily`
- `arxiv init` / `arxiv context`
- `arxiv read` / `arxiv brain`
- `arxiv repro` / `arxiv lab` / `arxiv deploy` / `arxiv dataset` / `arxiv fix`
- `arxiv extend` / `arxiv contrib`

## 推荐 SOP

```text
search/daily -> init -> read -> repro -> lab/deploy/dataset -> contrib
```

## 项目结构（重构后）

```text
arxiv-researcher/
├── arxiv_engine/
│   ├── cli.py
│   ├── core/
│   └── pipelines/
├── skills/arxiv-cli/SKILL.md
├── requirements.txt
├── setup.py
└── install.sh
```

## 故障排查

- `arxiv: command not found`：执行 `python3 -m pip install -e .`
- 无当前上下文：先 `arxiv init <id>` 或 `arxiv context <id>`
- 查看参数帮助：`arxiv <subcommand> --help`
