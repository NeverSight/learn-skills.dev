---
name: dingtalk-docs
description: 管理钉钉云文档中的文档、文件夹和内容。当用户想要创建文档、搜索文档、读取或写入文档内容、创建文件夹整理文档时使用。也适用于用户提到云文档、在线文档、钉钉文档、钉文档等关键词的场景。不要在用户需要操作多维表、管理日程、发消息或处理审批流时触发。
version: 0.3.4
metadata:
  openclaw:
    requires:
      bins:
        - mcporter
      env:
        - DINGTALK_MCP_DOCS_URL
    primaryEnv: DINGTALK_MCP_DOCS_URL
    homepage: https://github.com/aliramw/dingtalk-docs
---

# 钉钉云文档 Skill

## Overview

用户可能要求你创建、搜索、读取或编辑钉钉云文档。操作之间存在严格依赖关系：必须先获取 ID 才能执行后续操作。

## 严格禁止

1. **禁止编造 ID** -- dentryUuid 必须从返回值中提取，编造 ID 会操作到错误文档或报错
2. **创建前必须先获取根目录 ID** -- 必须先调 get_my_docs_root_dentry_uuid 拿到 rootDentryUuid
3. **禁止混淆两个创建方法** -- create_doc_under_node 只能创建文档，create_dentry_under_node 支持文件夹/表格/PPT 等多种类型
4. **写入前必须确认 updateType** -- 0=覆盖（清空后写入），1=续写（追加到末尾），搞反会丢数据，不确定时必须先问用户
5. **禁止只传 ID 读内容** -- 必须拼成完整 URL `https://alidocs.dingtalk.com/i/nodes/{dentryUuid}`
6. **禁止在用户说"表格"时默认创建文档** -- 可能要在线表格(accessType="1")或多维表(accessType="7")，不确定必须先问
7. **禁止传错参数类型** -- accessType 必须是字符串，updateType 必须是数字，类型传错会导致静默失败

## 可用方法列表

| 方法 | 用途 | 必填参数 | 可用性 |
|------|------|---------|--------|
| `get_my_docs_root_dentry_uuid` | 获取"我的文档"根目录 ID | 无 | 稳定可用 |
| `list_accessible_documents` | 搜索有权限的文档 | 无 (keyword 选填) | 稳定可用 |
| `create_doc_under_node` | 创建在线文档 | name, parentDentryUuid | 稳定可用 |
| `create_dentry_under_node` | 创建节点 (文档/表格/文件夹等) | name, accessType, parentDentryUuid | 稳定可用 |
| `write_content_to_document` | 写入文档内容 (覆盖或续写) | content, updateType, targetDentryUuid | 稳定可用 |
| `get_document_content_by_url` | 通过 URL 获取文档 Markdown 内容 | docUrl | **灰度中，部分实例不可见** |

## 灰度发布说明（重要）

根据 GitHub issue #1 下维护者的明确回复：`get_document_content_by_url` **目前在灰度中，全量还需要一点时间**。

因此你必须按下面规则处理：

1. **如果 MCP 客户端里只看到 5 个工具，不要先判断为配置错误**
2. **如果缺少 `get_document_content_by_url`，不要先判断为权限缺失**
3. 通过钉钉 MCP 广场拿到的 URL，当前很可能因为**服务端未放量**而看不到该方法
4. 在该方法未放开前，Skill 应把“读文档内容”视为**条件可用能力**，不是所有环境都保证存在
5. 向用户说明时要直接说清：**这是官方灰度状态，不是本地接入姿势问题**

## 意图判断

用户说"创建文档/新建文档/写个文档/帮我建个文档":
- 创建文档 → 先 get_my_docs_root_dentry_uuid，再 create_doc_under_node
- 创建到指定文件夹 → 用文件夹的 dentryUuid 作为 parentDentryUuid

用户说"建文件夹/新建目录/整理一下文档":
- 创建文件夹 → create_dentry_under_node(accessType="13")

用户说"创建表格/建个PPT/做个脑图":
- 非文档类型 → create_dentry_under_node，accessType: 表格="1"，PPT="2"，脑图="6"，多维表="7"
- 用户说"表格"但不确定类型 → 先问是在线表格还是多维表

关键区分: 在线表格(accessType="1") vs 多维表(accessType="7") vs 文档(用 create_doc_under_node)

用户说"搜索/找文档/查一下/有没有某个文档":
- 搜索 → list_accessible_documents(keyword=关键词)

用户说"读文档/看看内容/打开文档/这个文档写了什么":
- **先确认当前 MCP 服务是否真的暴露了 `get_document_content_by_url`**
- 有 URL 且该方法可用 → 直接 get_document_content_by_url
- 有文档名且该方法可用 → 先 list_accessible_documents 搜索，拿到 dentryUuid，拼 URL 再读
- 如果当前实例缺少 `get_document_content_by_url` → 明确告诉用户：**该读取能力目前仍在官方灰度中，你的实例暂未放开**，不要把原因归咎于用户配置

用户说"写入/更新内容/编辑文档/往文档里加点东西":
- 全新内容或替换 → write_content_to_document(updateType=0) 覆盖
- 追加内容 → write_content_to_document(updateType=1) 续写
- 不确定 → 问用户是覆盖还是追加

## 核心工作流

创建文档并写入:
1. get_my_docs_root_dentry_uuid() → 提取 rootDentryUuid
2. create_doc_under_node(name, parentDentryUuid=rootDentryUuid) → 提取 dentryUuid
3. (HARD-GATE: 必须确认 updateType) write_content_to_document(content, updateType=0, targetDentryUuid=dentryUuid) → 提取写入结果
4. get_document_content_by_url(docUrl="https://alidocs.dingtalk.com/i/nodes/{dentryUuid}") → 验证

搜索并读取（仅当 `get_document_content_by_url` 已放量可用时）:
1. list_accessible_documents(keyword="关键词") → 提取 docs[].dentryUuid
2. get_document_content_by_url(docUrl="https://alidocs.dingtalk.com/i/nodes/{dentryUuid}")

如果当前实例没有 `get_document_content_by_url`：
- 停在搜索结果这一步
- 明确提示用户该能力仍处于官方灰度阶段
- 不要伪造“读取成功”或编造替代读接口

创建文件夹并整理:
1. get_my_docs_root_dentry_uuid() → 提取 rootDentryUuid
2. create_dentry_under_node(name, accessType="13", parentDentryUuid=rootDentryUuid) → 提取 dentryUuid
3. create_doc_under_node(name, parentDentryUuid=文件夹dentryUuid)

## 上下文传递规则

| 操作 | 从返回中提取 | 用于 |
|------|-------------|------|
| get_my_docs_root_dentry_uuid | rootDentryUuid | create_doc_under_node / create_dentry_under_node 的 parentDentryUuid |
| create_doc_under_node | dentryUuid | write_content_to_document 的 targetDentryUuid，拼 URL 读内容 |
| create_dentry_under_node | dentryUuid | 作为子节点的 parentDentryUuid |
| list_accessible_documents | docs[].dentryUuid | 拼成 `https://alidocs.dingtalk.com/i/nodes/{dentryUuid}` 用于读取 |

## CRITICAL: 参数格式

```jsonc
// [正确] docUrl 必须是完整 URL
{"docUrl": "https://alidocs.dingtalk.com/i/nodes/DnRL6jAJ..."}
// [错误] 只传 ID → 报错
{"docUrl": "DnRL6jAJ..."}

// [正确] accessType 是字符串
{"name": "报表", "accessType": "1", "parentDentryUuid": "xxx"}
// [错误] accessType 传数字 → 静默失败
{"name": "报表", "accessType": 1, "parentDentryUuid": "xxx"}

// [正确] updateType 是数字
{"content": "...", "updateType": 0, "targetDentryUuid": "xxx"}
// [错误] updateType 传字符串 → 静默失败
{"content": "...", "updateType": "0", "targetDentryUuid": "xxx"}
```

## 本地文件脚本说明

`scripts/` 目录中的辅助脚本会处理本地文件输入 / 输出：

- `import_docs.py` 会读取工作区内的 `.md` / `.txt` / `.markdown` 文件并导入到钉钉文档
- `export_docs.py` 会将钉钉文档内容导出为工作区内的本地 Markdown 文件
- `create_doc.py` 会调用 `mcporter` 创建文档并写入内容

这些脚本都受以下规则约束：

- 仅允许访问工作区内路径
- 使用 `resolve_safe_path()` 防止目录遍历
- 限制文件大小和扩展名
- 仅通过 `mcporter` 调用 MCP 服务，不直接发起网络请求

## 错误处理

1. 遇到错误: 展示错误信息给用户，不要自行猜测解决方案
2. "Invalid credentials": 提示用户重新配置凭证
3. "Permission denied": 提示用户确认对该文档有操作权限
4. "Document not found": 用 list_accessible_documents 重新搜索确认文档是否存在
5. 如果方法列表里根本没有 `get_document_content_by_url`：按**官方灰度未放量**处理，不要误报为本地配置错误
6. 错误码 52600007: 可能是企业账号限制或父节点 ID 无效，确认 parentDentryUuid 来源

## 详细参考 (按需读取)

- [references/api-reference.md](./references/api-reference.md) -- 完整参数 Schema + 返回值 + 节点类型枚举
- [references/error-codes.md](./references/error-codes.md) -- 错误码说明 + 调试流程
