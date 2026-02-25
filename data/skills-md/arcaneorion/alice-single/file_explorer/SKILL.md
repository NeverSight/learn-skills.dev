---
name: file_explorer
description: 高效的项目文件浏览器。当需要列出整个项目结构、模糊搜索文件或安全地读取（支持大文件分块）本地代码库内容时使用。
---

# 文件浏览器技能 (File Explorer)

此技能专为 Alice 探索复杂项目而设计，提供比原生 `ls/cat` 更安全、更高效的手段。

## 核心功能

- **项目树生成 (`--tree`)**: 快速展示项目目录结构，支持忽略忽略文件。
- **模糊搜索 (`--search`)**: 像 `fzf` 一样根据文件名快速定位。
- **安全读取 (`--read`)**: 自动检测文件大小。如果文件过大，提供分块读取建议，防止上下文溢出。

## 使用方法

在终端运行：

```bash
# 查看项目树状结构 (深度默认为 2)
python skills/file_explorer/explorer.py --tree --depth 3

# 模糊搜索包含 "config" 的文件
python skills/file_explorer/explorer.py --search "config"

# 安全读取文件内容
python skills/file_explorer/explorer.py --read "agent.py"
```

## 注意事项

Alice 已被权限锁定。此技能仅能访问项目根目录下的文件。严禁尝试访问路径外的内容。
对于 10KB 以上的文件，请优先使用 `--read` 以获取安全分段。
