---
name: repomix-gh
argument-hint: <owner/repo> [output.md] [--force] [--full]
description: GitHub 仓库打包工具（gh + zip download，默认 lean 模式）
---

> GitHub 仓库打包工具，使用 gh + zip download 快速生成 LLM 可学习的单文件文档。

## 快速开始

```bash
# Lean 模式（默认，排除测试和多语言文档）
bash src/repomix-gh.sh affaan-m/everything-claude-code

# Full 模式（包含所有文件）
bash src/repomix-gh.sh affaan-m/everything-claude-code output.md --full
```

## 用法

```bash
bash src/repomix-gh.sh owner/repo [output.md] [--force] [--full]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `owner/repo` | GitHub 仓库（如 `affaan-m/everything-claude-code`） |
| `output.md` | 输出文件名（默认：`{repo}.md`） |
| `--force` | 强制重新下载（跳过缓存） |
| `--full` | Full 模式，包含所有文件（默认为 lean 模式） |

### 示例

```bash
# 基本用法（默认 lean 模式）
bash src/repomix-gh.sh jl-pkgs/StrategicRandomSearch.jl

# 指定输出文件
bash src/repomix-gh.sh Deltares/Wflow.jl Wflow.md

# Full 模式（包含所有文件）
bash src/repomix-gh.sh affaan-m/everything-claude-code ecc.md --full

# 强制更新缓存
bash src/repomix-gh.sh owner/repo output.md --force
```

## 输出示例

```
📦 repomix-gh: affaan-m/everything-claude-code
================================
✓ 使用缓存: ~/.cache/repomix-gh/...zip
🎯 Lean 模式：排除测试和多语言文档（默认）
📝 生成文档: output.md
================================
[repomix 输出...]

📊 文件类型统计 (Top 20):
================================
  .md                      430 个文件
  .js                       34 个文件
  .json                     18 个文件
  ...

================================
✓ 完成！输出文件:
  output.md (1.4M)

📈 总计: 398,690 tokens, 233 个文件
```

**生成的 md 文件头部包含：**
```markdown
<!-- Token 总数: 398,690 -->
<!-- 文件总数: 233 -->
<!-- 生成时间: 2026-02-23 05:41:13 UTC -->
<!-- 仓库: affaan-m/everything-claude-code@main -->
<!-- 模式: --lean -->
```

## 模式对比

| 模式 | 文件大小 | 文件数 | Tokens | 说明 |
|------|---------|-------|--------|------|
| **完整** | 4.9M | 627 | 1.5M | 包含所有内容 |
| **Lean** | 2.1M | 350 | 632K | 排除测试和多语言文档 |

## 工作流程

```
gh api 获取默认分支 → curl 下载 zip → unzip 解压 → repomix 打包
```

**速度对比（everything-claude-code 示例）：**

| 方式 | 时间 | 速度 |
|------|------|------|
| **gh + zip** | 2s | 26 MB/s |
| git clone | ~30s | ~2 MB/s |
| npx --remote | ~60s | ~1 MB/s |

## 缓存机制

```bash
~/.cache/repomix-gh/
├── owner_repo-main.zip     # 缓存 zip
└── owner_repo-main/        # 解压目录
```

- 首次运行：下载并缓存
- 二次运行：直接使用缓存（<1s）
- `--force`: 强制重新下载

## 依赖

- `repomix`: `npm install -g repomix`
- `gh`: https://cli.github.com/

## 经验总结

### ✅ 为什么优先 gh + zip？

1. **快速**: 直接下载 zip，比 git clone 快 10 倍+
2. **轻量**: 不包含 .git 历史，节省空间
3. **可靠**: 失败自动回退到 gh api
4. **灵活**: gh 自动检测默认分支

### ⚠️ 常见问题

**Q: 解压后路径错误？**
A: 使用 `"$TMP"/*/` 匹配解压后的目录

**Q: 下载失败？**
A: 检查网络，或 `gh auth login` 获取更高速率限制

**Q: 仓库太大？**
A: 默认 lean 模式已优化，如需完整内容使用 `--full`

**Q: 重新生成不同参数？**
A: 直接再次运行，使用缓存，无需重新下载

## 参考资料

详见 [Config.md](Config.md)
