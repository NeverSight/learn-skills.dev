---
name: clear-cache
description: 清理本地插件缓存，用于调试或重新加载插件。
---

## 执行命令

```bash
rm -rf $HOME/.claude/plugins/cache/taptap-plugins
```

## 说明

此命令会删除本地的插件缓存目录，用于：
- 调试插件时强制重新加载
- 解决缓存导致的问题
- 测试插件的全新安装流程
