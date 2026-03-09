---
name: evolve
version: 4.5.0
description: 自我進化 Agent - 已遷移至原子化架構
redirect: ./skills/SKILL.md
---

# ⚠️ This file has moved

The Self-Evolving Agent skill has been reorganized into an atomic architecture.

## New Location

**👉 [skills/SKILL.md](./skills/SKILL.md)**

## Quick Links

| Module | Description | Path |
|--------|-------------|------|
| Getting Started | 入門與環境設定 | [→](./skills/00-getting-started/) |
| Core | 核心流程（PSB + PDCA） | [→](./skills/01-core/) |
| Checkpoints | 強制檢查點（護欄） | [→](./skills/02-checkpoints/) |
| Memory | 記憶系統操作 | [→](./skills/03-memory/) |
| Emergence | 涌現機制 | [→](./skills/04-emergence/) |
| Integration | 外部工具整合 | [→](./skills/05-integration/) |
| Scaling | 大規模專案優化 | [→](./skills/06-scaling/) |
| Evolution | 自我進化機制 | [→](./skills/99-evolution/) |

## Why the Change?

- **Easier to maintain**: Small modules > monolithic file
- **Easier to contribute**: Community content in `community/` directories
- **Easier to learn**: Read modules progressively
- **Easier to extend**: Add new modules without touching existing content

## Migration

If you were using the old SKILL.md, simply update your imports:

```
Old: SKILL.md (2000+ lines)
New: skills/SKILL.md (entry point) + skills/*/_base/*.md (modules)
```
