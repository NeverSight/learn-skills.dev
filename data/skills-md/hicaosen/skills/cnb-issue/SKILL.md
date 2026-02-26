---
name: cnb-issue
description: |
  操作 CNB (cnb.cool) 平台上的 Issue。当用户需要创建、查询、更新 CNB 上的 Issue，
  或需要管理 Issue 的标签、处理人、评论时，使用此 skill。
  触发词: cnb issue、cnb 问题单、腾讯代码平台 issue、cnb.cool issue、cnb工单
---

# CNB Issue 操作 Skill

操作 CNB 平台 (https://cnb.cool) 上的 Issue。本 skill 提供了封装好的 `cnb-client.js` 工具脚本。

## 前提条件

1. **安装依赖**

   在 skill 的 `scripts` 目录下执行：
   ```bash
   cd <skill-base-directory>/scripts
   npm install
   ```

   其中 `<skill-base-directory>` 是本 skill 的安装目录（触发 skill 时会显示 Base directory 信息）。

2. **获取 API Token**
   - 登录 https://cnb.cool
   - 进入个人设置 -> 访问令牌
   - 创建包含 `repo-issue:r` 或 `repo-issue:rw` 权限的令牌

3. **设置环境变量**
   ```bash
   export CNB_TOKEN="your-token-here"
   ```

## 重要提示

- **执行前必须检查 CNB_TOKEN 环境变量是否存在**，如果没有设置，立即停止并告知用户需要设置
- **如果执行命令遇到任何错误**，立即停止，不要继续尝试其他操作，向用户报告错误信息

## 使用 cnb-client.js 工具

本 skill 包含 `scripts/cnb-client.js` 命令行工具。脚本位于 `<skill-base-directory>/scripts/cnb-client.js`。

### 查询 Issue

```bash
# 列出仓库的所有 Issue
node <skill-base-directory>/scripts/cnb-client.js list owner/repo

# 带过滤条件查询
node <skill-base-directory>/scripts/cnb-client.js list owner/repo '{"state":"open","labels":"bug"}'

# 获取单个 Issue 详情
node <skill-base-directory>/scripts/cnb-client.js get owner/repo 123
```

### 创建 Issue

```bash
# 创建简单 Issue
node <skill-base-directory>/scripts/cnb-client.js create owner/repo '{"title":"Bug: 登录页面无法加载","body":"详细描述问题..."}'

# 创建带标签和处理人的 Issue
node <skill-base-directory>/scripts/cnb-client.js create owner/repo '{
  "title": "[Bug] 支付页面超时",
  "body": "## 问题描述\n支付页面在高峰期出现超时情况",
  "labels": ["bug", "priority-high"],
  "assignees": ["username"]
}'
```

### 更新 Issue

```bash
# 更新标题和内容
node <skill-base-directory>/scripts/cnb-client.js update owner/repo 123 '{"title":"新标题","body":"新内容"}'

# 关闭 Issue
node <skill-base-directory>/scripts/cnb-client.js update owner/repo 123 '{"state":"closed"}'

# 重新打开 Issue
node <skill-base-directory>/scripts/cnb-client.js update owner/repo 123 '{"state":"open"}'
```

### 管理标签

```bash
# 添加标签
node <skill-base-directory>/scripts/cnb-client.js add-labels owner/repo 123 '["bug","urgent"]'

# 设置标签（替换现有标签）
node <skill-base-directory>/scripts/cnb-client.js set-labels owner/repo 123 '["enhancement"]'

# 移除单个标签
node <skill-base-directory>/scripts/cnb-client.js remove-label owner/repo 123 wontfix
```

### 管理处理人

```bash
# 添加处理人
node <skill-base-directory>/scripts/cnb-client.js add-assignees owner/repo 123 '["user1","user2"]'

# 移除处理人
node <skill-base-directory>/scripts/cnb-client.js remove-assignees owner/repo 123 '["user1"]'
```

### 管理评论

```bash
# 添加评论
node <skill-base-directory>/scripts/cnb-client.js add-comment owner/repo 123 "这是评论内容"

# 查看评论列表
node <skill-base-directory>/scripts/cnb-client.js list-comments owner/repo 123
```

## 完整示例：创建 Bug 报告流程

```bash
# 1. 创建 Issue
ISSUE=$(node <skill-base-directory>/scripts/cnb-client.js create myorg/myproject/myrepo '{
  "title": "[Bug] 支付页面超时",
  "body": "## 问题描述\n支付页面在高峰期出现超时情况\n\n## 影响范围\n- 移动端用户\n- 高峰期 (18:00-21:00)\n\n## 期望行为\n支付应在 5 秒内完成",
  "labels": ["bug", "priority-critical", "payment"],
  "assignees": ["backend-team"]
}')

echo "Issue 创建成功: $ISSUE"

# 2. 添加初始评论
node <skill-base-directory>/scripts/cnb-client.js add-comment myorg/myproject/myrepo 123 "已分配给后端团队处理，预计 24 小时内修复。"
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `list <repo> [query]` | 列出 Issues |
| `get <repo> <number>` | 获取 Issue 详情 |
| `create <repo> <json>` | 创建 Issue |
| `update <repo> <number> <json>` | 更新 Issue |
| `add-labels <repo> <number> <labels>` | 添加标签 |
| `set-labels <repo> <number> <labels>` | 设置标签 |
| `remove-label <repo> <number> <name>` | 移除标签 |
| `add-assignees <repo> <number> <users>` | 添加处理人 |
| `remove-assignees <repo> <number> <users>` | 移除处理人 |
| `add-comment <repo> <number> <body>` | 添加评论 |
| `list-comments <repo> <number>` | 列出评论 |

## API 权限说明

| 权限 | 说明 |
|------|------|
| `repo-issue:r` | 读取 Issue |
| `repo-issue:rw` | 读写 Issue |
| `repo-notes:r` | 读取评论 |
| `repo-notes:rw` | 读写评论 |

## 仓库路径格式

CNB 支持两种仓库路径格式：
- 个人仓库: `username/repo`
- 组织仓库: `org/project/repo`

## 在 Node.js 中使用

如果需要在 Node.js 脚本中使用，可以导入 `cnb-client.js` 的函数：

```javascript
// 使用 skill base directory 下的脚本
const {
  listIssues,
  getIssue,
  createIssue,
  updateIssue,
  addLabels,
  addAssignees,
  createComment,
  getComments
} = require('<skill-base-directory>/scripts/cnb-client');

// 或者在 async 函数中使用
async function main() {
  // 列出 Issues
  const issues = await listIssues('owner/repo', { state: 'open' });

  // 创建 Issue
  const issue = await createIssue('owner/repo', {
    title: 'Bug report',
    body: 'Description...',
    labels: ['bug']
  });

  // 添加评论
  await createComment('owner/repo', issue.number, 'Thanks for reporting!');
}
```
