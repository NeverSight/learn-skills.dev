---
name: prepare-release
description: 发布前准备。重置版本号、更新 CHANGELOG 和 README、校验一致性。
---

## 执行流程

### 步骤 1: 版本重置

#### 1.1 获取远程版本

```bash
git fetch origin main
```

#### 1.2 检查哪些插件有修改

```bash
git diff --name-only origin/main -- plugins/
```

根据输出判断哪些插件目录有变更，只有变更的插件才需要更新版本。

#### 1.3 读取生产版本号

获取 origin/main 的 marketplace 版本和有修改的插件版本：

```bash
# marketplace 版本
git show origin/main:.claude-plugin/marketplace.json | jq -r '.metadata.version'

# 指定插件版本
git show origin/main:.claude-plugin/marketplace.json | jq -r '.plugins[] | select(.name=="<plugin>") | .version'
```

#### 1.4 计算新版本号

将获取的生产版本的 patch 版本 +1。

示例：
- 生产 marketplace: `0.1.10` → 重置为 `0.1.11`
- 生产 sync: `0.1.10` → 重置为 `0.1.11`

#### 1.5 更新版本文件

**只更新有修改的插件**：

1. `.claude-plugin/marketplace.json`
   - `metadata.version`（总是更新）
   - 有修改的插件的 `version`

2. `plugins/<name>/.claude-plugin/plugin.json`
   - 只更新有修改的插件

**未修改的插件保持原版本不变。**

**重要**：仅在 `.claude-plugin/marketplace.json` 中注册的插件才参与版本重置。本地开发中但未注册的插件（如 ralph 等）需先从 marketplace.json 删除其条目，或直接忽略。

### 步骤 2: 更新 CHANGELOG.md

在文件顶部（`# Changelog` 标题之后）插入新版本条目。

#### 格式

```markdown
## {marketplace_version}

### {Plugin Name} ({plugin_version})

- Added ...
- Changed ...
- Fixed ...

### Marketplace

- Bumped version from {old_marketplace_version} to {new_marketplace_version}
- Updated {plugin} plugin to version {plugin_version}
```

#### 规则

- 每个有版本变更的插件一个子章节：`### {Plugin Name} ({plugin_version})`
  - Plugin Name 使用首字母大写 + " Plugin" 后缀，如 `Sync Plugin`、`Git Plugin`
- 使用 `git log origin/main..HEAD -- plugins/{name}/` 获取该插件的变更摘要
- **必须使用英文**编写条目（Added/Changed/Fixed/Cleaned up/Updated 等前缀）
- 末尾加 `### Marketplace` 段落，列出 bumped version 和 updated plugins

### 步骤 3: 更新插件 README 版本历史

对每个有版本变更的插件：

1. 读取其 `plugins/{name}/README.md`
2. 检查是否存在 `## 版本历史` 段落
3. 如果存在，在该段落顶部（紧接 `## 版本历史` 之后）插入新条目

#### 格式

```markdown
- **v{version}** - {中文摘要，分号分隔}
```

示例：
```markdown
- **v0.1.12** - 新增 XXX 命令；修复 YYY 问题；更新 ZZZ 配置
```

**仅处理有 `## 版本历史` 段落的 README**，没有该段落的跳过。

### 步骤 4: 更新根目录 README.md

更新 `## 插件列表` 表格中有版本变更的插件版本号。

表格格式参考：

```markdown
| 插件      | 版本    | 描述                                                                |
| ------- | ----- | ----------------------------------------------------------------- |
| sync    | 0.1.12 | 开发环境配置同步插件（...） |
```

仅更新有版本变更的行，其他行保持不变。

### 步骤 5: 校验

逐一确认以下位置的版本号一致性：

1. `.claude-plugin/marketplace.json` 中的 `metadata.version`
2. `.claude-plugin/marketplace.json` 中各插件的 `version`
3. `plugins/<name>/.claude-plugin/plugin.json` 中的 `version`
4. `CHANGELOG.md` 顶部条目的版本号
5. 根目录 `README.md` 插件列表表格中的版本号
6. 各插件 `README.md` 版本历史顶部条目的版本号（如有）

输出校验结果表格供用户确认：

```
| 位置                          | 插件   | 版本    | 状态 |
| ----------------------------- | ------ | ------ | ---- |
| marketplace.json (metadata)   | -      | 0.1.16 | ✅   |
| marketplace.json (plugin)     | sync   | 0.1.12 | ✅   |
| plugin.json                   | sync   | 0.1.12 | ✅   |
| CHANGELOG.md                  | sync   | 0.1.12 | ✅   |
| README.md (root)              | sync   | 0.1.12 | ✅   |
| README.md (plugin)            | sync   | 0.1.12 | ✅   |
```
