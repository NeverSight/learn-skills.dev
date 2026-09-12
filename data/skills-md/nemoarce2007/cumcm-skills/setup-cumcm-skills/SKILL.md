---
name: setup-cumcm-skills
description: 在赛题工作区初始化 CUMCM 目录、contest-state.json 与忽略规则。在第一次使用本技能包、或目录里还没有 contest-state.json 时使用。不要在已初始化且用户只想建模时使用。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: user
  graph-node: R0
disable-model-invocation: true
---

# setup-cumcm-skills

只建工作区，不解题。

## 何时使用

必须使用：当前目录没有 `contest-state.json`；用户说「初始化」「搭目录」。

禁止使用：已经初始化且用户要读题/写论文。不要覆盖已有 `data/raw`。

## 循环

目标：目录与状态文件就位，且原始数据目录可写但为空或仅有用户已放文件。

`max_rounds`: 2

## 步骤

1. 确认 cwd 是赛题仓库。如果 cwd 是本 skills 开源仓库（存在 `skills/contest-run`）→ 停，要求用户换到赛题目录。
2. 创建：`problem/` `data/raw/` `data/processed/` `src/` `scripts/` `configs/` `results/figures/` `results/tables/` `results/logs/` `paper/` `support/`。
3. 若无 `contest-state.json`，按本仓库 `templates/contest-state.json` 的字段写出最小实例：`schema_version=0.1.0`，`status=uninitialized`，`problems=[]`。
4. 确保赛题仓库 `.gitignore` 含 `.env`、身份类文件；提醒用户不要把 `problem/` 推到公开 remote。
5. 问四项（可短答）：年份、题号（A/B/C…）、论文语言（zh/en）、论文引擎（`latex` / `word`）。前三项写入 `contest.*`，引擎写入 `paper.engine`。
6. 若 `paper/` 下还没有稿：在 cwd、`.agents/skills`、`.claude/skills` 里找 `paper-write/assets/`，按引擎复制到 `paper/latex/` 或 `paper/word-outline.md`。找不到就写 `paper/README.md`，让用户从本技能包的 `paper-write/assets/` 拷。不要覆盖已有 `.tex` / `.docx`。

## 验收

- [ ] `contest-state.json` 可 JSON.parse
- [ ] 上列目录存在
- [ ] 未删除用户已有数据文件
- [ ] 当前仓库不是误初始化在 skills 源码仓（除非用户明确要求）

## 输出

写入 `contest.*`（用户已答部分）和 `paper.engine`（若已选）。`status` 仍为 `uninitialized` 直到 grill 锁定题目。

## 下一跳

`grill-problem`（用户确认题号后）。不要自动开始写论文。
