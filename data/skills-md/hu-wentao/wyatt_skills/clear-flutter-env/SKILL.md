---
name: clear-flutter-env
description: 用于在 macOS 上清除 Flutter 环境变量 (FLUTTER_STORAGE_BASE_URL 和 PUB_HOSTED_URL)。适用于需要重置环境或解决 Flutter 代理问题的场景。
---

# 清除 Flutter 环境变量 (macOS)

## 概述

此技能允许用户在 macOS 平台上快速清除 `FLUTTER_STORAGE_BASE_URL` 和 `PUB_HOSTED_URL` 两个环境变量。这在切换 Flutter 镜像源或重置开发环境时非常有用。

## 核心任务

### 清除环境变量

用户可以直接请求清除 Flutter 相关的环境变量。该操作将执行以下命令：

```bash
unset FLUTTER_STORAGE_BASE_URL
unset PUB_HOSTED_URL
```

## 资源

### scripts/

- `clear_flutter_env.sh`: 执行 `unset` 命令的 Shell 脚本。

### 如何使用

1. **直接执行**: 告知用户执行以下命令：
   ```bash
   unset FLUTTER_STORAGE_BASE_URL
   unset PUB_HOSTED_URL
   ```
2. **运行脚本**: 如果需要，可以运行提供的脚本：
   `./scripts/clear_flutter_env.sh`
