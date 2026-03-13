---
name: feishu-drive
description: 飞书云空间文件管理。上传/下载/移动/搜索文件、创建文件夹。
required_permissions:
  - drive:file:upload
  - drive:file:download
  - drive:drive:readonly
---

# 飞书云空间文件管理

通过 Drive API 管理文件和文件夹。

**Base URL**: `https://open.feishu.cn/open-apis/drive/v1`

---

## 快速启动（必读）

为避免文件进入"私有黑盒"：

1. **创建锚点文件夹**（如 `AI-Workspace`）
2. **授权机器人**：文件夹【协作】设置中添加应用为【管理】权限
3. **获取 Token**：复制文件夹 URL 中的 Token
4. **测试**：调用 `batch_query` 查询该 Token

⚠️ API 创建的文件夹默认只对机器人可见，需手动添加协作者。

---

## 文件夹操作

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 创建文件夹 | `/folders` | POST | `{"name":"文件夹名","folder_token":"root"}` | 创建新文件夹 |
| 获取文件夹元数据 | `/folders/{folder_token}/meta` | GET | - | 查询文件夹详情 |
| 获取元数据（批量） | `/metas/batch_query` | POST | `{"request_list":[{"token":"fldxxx","type":"folder"}]}` | 批量查询文件/文件夹 |
| 获取文件夹内容 | `/folders/{folder_token}/children` | GET | - | 查询文件夹内文件列表 |
| 移动文件夹 | `/folders/{folder_token}/move` | POST | `{"target_token":"fldxxx"}` | 移动文件夹 |
| 复制文件夹 | `/folders/{folder_token}/copy` | POST | `{"target_token":"fldxxx"}` | 复制文件夹 |
| 删除文件夹 | `/folders/{folder_token}` | DELETE | - | 删除空文件夹 |

---

## 文件上传

| API | 端点 | 方法 | 请求体 | 说明 |
|-----|------|------|--------|------|
| 小文件上传 | `/files/upload_all` | POST | `multipart/form-data` | 一次性上传（<20MB） |
| 大文件预上传 | `/files/upload_prepare` | POST | `{"file_name":"big.zip","size":104857600}` | 初始化分片上传 |
| 分片上传 | `/files/upload_part` | POST | `multipart/form-data` | 上传单个分片 |
| 完成分片上传 | `/files/upload_finish` | POST | `{"upload_id":"xxx","block_num":10}` | 完成上传 |

**小文件上传**:
```
POST /files/upload_all
Content-Type: multipart/form-data

file_name=test.txt
parent_type=explorer
parent_node=fldXXX
file=<binary>
```

---

## 文件下载

| API | 端点 | 方法 | 说明 |
|-----|------|------|------|
| 下载文件 | `/files/{file_token}/download` | GET | 返回文件二进制流 |
| 获取文件元数据 | `/files/{file_token}/meta` | GET | 查询文件详情 |
| 获取文件列表 | `/files` | GET | 参数：`folder_token` 父文件夹 |

---

## 文件操作

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 移动文件 | `/files/{file_token}/move` | POST | `{"type":"explorer","folder_token":"fldXXX"}` | 移动文件 |
| 复制文件 | `/files/{file_token}/copy` | POST | `{"type":"explorer","folder_token":"fldXXX","name":"副本.txt"}` | 复制文件 |
| 删除文件 | `/files/{file_token}` | DELETE | - | 删除文件 |
| 创建快捷方式 | `/shortcuts` | POST | `{"target_token":"filexxx","parent_token":"fldxxx"}` | 创建文件快捷方式 |
| 获取文件统计 | `/files/{file_token}/statistics` | GET | - | 查询文件访问统计 |

---

## 搜索

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 搜索文件 | `/files/search` | POST | `{"search_key":"关键词","owner_ids":["ou_xxx"]}` | 全文搜索 |
| 搜索V2 | `/files/search_v2` | POST | 同上 | 新版搜索接口 |

---

## 权限管理

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 添加协作者 | `/permissions/{token}/members` | POST | `{"member_type":"user","member_id":"ou_xxx","perm":"full_access"}` | 添加权限 |
| 移除协作者 | `/permissions/{token}/members/{member_id}` | DELETE | - | 移除权限 |
| 获取协作者 | `/permissions/{token}/members` | GET | - | 查询权限列表 |
| 更新协作者 | `/permissions/{token}/members/{member_id}/patch` | PATCH | `{"perm":"edit"}` | 修改权限 |
| 转让所有者 | `/permissions/{token}/transfer_owner` | POST | `{"member_type":"user","member_id":"ou_xxx"}` | 转移所有权 |
| 获取权限设置 | `/permissions/{token}/public` | GET | - | 查询公开访问设置 |
| 更新权限设置 | `/permissions/{token}/public` | PATCH | `{"external_access":false}` | 修改公开访问 |

**权限类型**: `view`(查看) / `edit`(编辑) / `full_access`(完全访问)

---

## 文件版本管理

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 获取版本列表 | `/files/{file_token}/versions` | GET | - | 查询文件历史版本 |
| 获取版本详情 | `/files/{file_token}/versions/{version_id}` | GET | - | 查询指定版本信息 |
| 删除版本 | `/files/{file_token}/versions/{version_id}` | DELETE | - | 删除历史版本 |

---

## 文件评论

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 获取全文评论 | `/files/{file_token}/comments` | GET | - | 查询文件所有评论 |
| 获取回复列表 | `/files/{file_token}/comments/{comment_id}/replies` | GET | - | 查询评论的回复 |
| 添加全文评论 | `/files/{file_token}/comments` | POST | `{"content":{"text":"评论内容"}}` | 添加评论 |
| 回复评论 | `/files/{file_token}/comments/{comment_id}/replies` | POST | `{"content":{"text":"回复内容"}}` | 回复评论 |
| 解决/重开评论 | `/files/{file_token}/comments/{comment_id}` | PATCH | `{"is_solved":true}` | 标记评论状态 |

---

## 订阅管理

| API | 端点 | 方法 | 请求体示例 | 说明 |
|-----|------|------|-----------|------|
| 订阅文件 | `/files/{file_token}/subscriptions` | POST | `{"subscription_type":"file_edit"}` | 订阅文件变更通知 |
| 获取订阅状态 | `/files/{file_token}/subscriptions/{subscription_id}` | GET | - | 查询订阅状态 |
| 取消订阅 | `/files/{file_token}/subscriptions/{subscription_id}` | DELETE | - | 取消订阅 |

**订阅类型**: `file_edit`(文件编辑) / `file_comment`(评论) / `file_share`(分享)

---

## 最佳实践

1. **创建文件夹后立即添加协作者**（避免不可见）
2. **大文件用分片上传**（>20MB）
3. **权限继承**：父文件夹授权后，子文件夹自动继承
4. **版本管理**：定期清理历史版本节省空间
5. **订阅通知**：关键文件订阅变更通知，及时响应
