---
name: design-system-review
description: 基于 docs/design/DESIGN.md 审查 AI 生成或修改的前端页面是否视觉跑偏。Use when 用户要求检查页面是否符合设计规范、发现未登记色值、字号漂移、圆角漂移、组件不一致、响应式或页面破版风险，并生成 review-report.md；P0/P1 问题需要终端非 0 退出形成阻断感。
---

# 设计系统审查

## 核心定位

检查项目页面是否偏离 `docs/design/DESIGN.md`，并输出：

- `docs/design/review-report.md`
- `work/design-review/`

审查结果不要只停留在对话里，必须落文件。

## 默认脚本

```bash
node .agents/skills/design-system-review/scripts/scan-token-drift.mjs --root . --design docs/design/DESIGN.md
```

审查 PC/Web 页面时：

```bash
node .agents/skills/design-system-review/scripts/scan-token-drift.mjs --root . --platform pc
```

审查移动端/H5/小程序页面时：

```bash
node .agents/skills/design-system-review/scripts/scan-token-drift.mjs --root . --platform mobile
```

当 `--platform pc` 存在时，脚本会读取 `docs/design/DESIGN.md` 和可选 `docs/design/DESIGN_PC.md`。当 `--platform mobile` 存在时，脚本会读取 `docs/design/DESIGN.md` 和可选 `docs/design/DESIGN_MOBILE.md`。

脚本行为：

- P0：`exit 2`
- P1：`exit 1`
- P2/P3：`exit 0`，但打印 warning

## 审查项

v0.1 先检查四类高价值问题：

1. 未登记色值。
2. 圆角漂移。
3. 字号漂移。
4. 组件样式不一致。

分级规则见 `references/review-severity.md`。

## 文件与 Git 规则

首次创建 `work/` 时必须创建 `work/.gitignore`：

```gitignore
*
!.gitignore
```

`work/design-review/` 存临时截图、扫描中间结果和调试文件，默认不入库。

## 输出规则

对话中只输出：

- 报告文件路径。
- P0/P1 数量和简短摘要。
- 是否需要修改页面或更新 `DESIGN.draft.md`。

不要在对话中展开完整扫描清单。详细内容写入 `docs/design/review-report.md`。
