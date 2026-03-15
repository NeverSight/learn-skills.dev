---
name: dingtalk-contact
description: 钉钉通讯录与联系人查询。当用户提到"钉钉通讯录"、"查找员工"、"搜索用户"、"查用户信息"、"获取用户详情"、"用户手机号"、"员工姓名"、"员工工号"、"查部门"、"搜索部门"、"部门成员"、"部门列表"、"部门详情"、"子部门"、"父部门"、"部门路径"、"员工总数"、"通讯录搜索"、"userId 转 unionId"、"unionId 转 userId"、"dingtalk contact"、"dingtalk directory"、"find user"、"get user info"、"department members"时使用此技能。支持：按关键词搜索用户/部门、获取用户完整信息（姓名/手机/工号/部门/职位/unionId）、获取部门成员列表、获取部门树结构、查询用户所在部门路径、员工总人数统计等全部通讯录操作。
---

# 钉钉通讯录技能
负责钉钉通讯录的所有查询操作。本文件为**策略指南**，仅包含决策逻辑和工作流程。完整 API 请求格式见文末「references/api.md 查阅索引」。

## 工作流程（每次执行前）
1. **读取/写入配置** → 通过 `scripts/dt_helper.sh` 管理，配置跨会话保留，无需重复询问
2. **仅收集缺失配置** → 若缺少某项，**一次性询问用户**所有缺失的值，用 `bash scripts/dt_helper.sh --set KEY=VALUE` 写入
3. **获取 Token** → 直接调用 `dt_helper.sh` 即可，token 如何获取/缓存无需关注
4. **执行操作** → 凡是包含变量替换、管道或多行逻辑的命令，写入 `/tmp/<task>.sh` 再 `bash /tmp/<task>.sh` 执行。不要把多行命令直接粘到终端里（终端工具会截断），也不要用 `<<'EOF'` 语法（heredoc 在工具中同样会被截断导致变量丢失）

> 凭证禁止在输出中完整打印，确认时仅显示前 4 位 + `****`

### 所需配置
| 配置键 | 必填 | 说明 | 如何获取 |
|---|---|---|---|
| `DINGTALK_APP_KEY` | ✅ | 应用 AppKey | 钉钉开放平台 → 应用管理 → 凭证信息 |
| `DINGTALK_APP_SECRET` | ✅ | 应用 AppSecret | 同上 |
| `DINGTALK_MY_USER_ID` | ❌ | **当前操作用户**的 userId（即运行此技能的人自己），仅在需要以自身为起点查询时才需要 | 管理后台 → 通讯录 → 成员管理 → 点击姓名查看 |

### 身份标识说明
| 标识 | 说明 |
|---|---|
| `userId`（= `staffId`） | 企业内部员工 ID，可通过通过管理后台 -> 通讯录 -> 成员管理 -> 点击姓名查看 |
| `unionId` | 跨企业/跨应用唯一标识，可通过`bash scripts/dt_helper.sh --to-unionid <userid>` 获取 |

### 执行脚本模板
```bash
#!/bin/bash
set -e
HELPER="<THE_SKILL_MD_PATH>/scripts/dt_helper.sh"
NEW_TOKEN=$(bash "$HELPER" --token)       # api.dingtalk.com 接口用
OLD_TOKEN=$(bash "$HELPER" --old-token)   # oapi.dingtalk.com 接口用
# USER_ID=$(bash "$HELPER" --get DINGTALK_MY_USER_ID)  # 以当前操作用户为起点时启用

# 在此追加具体 API 调用，例如按姓名搜索用户并获取详情：
KEYWORD="张三"
SEARCH=$(curl -s -X POST https://api.dingtalk.com/v1.0/contact/users/search \
  -H "x-acs-dingtalk-access-token: $NEW_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"queryWord\":\"$KEYWORD\",\"offset\":0,\"size\":20}")
echo "搜索结果: $SEARCH"

TARGET_UID=$(echo "$SEARCH" | grep -o '"list":\["[^"]*"' | grep -o '"[^"]*"$' | tr -d '"')
DETAIL=$(curl -s -X POST "https://oapi.dingtalk.com/topapi/v2/user/get?access_token=${OLD_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"userid\":\"$TARGET_UID\",\"language\":\"zh_CN\"}")
echo "用户详情: $DETAIL"
```

> **Token 失效处理**：dt_helper 仅按时间缓存，无法感知 token 被提前吊销。若 API 返回 `errcode 40001`/`40014`（token 无效/过期），用 `--nocache` 跳过缓存强制重新获取：
> ```bash
> OLD_TOKEN=$(bash "$HELPER" --old-token --nocache)  # 强制重新获取旧版 token
> NEW_TOKEN=$(bash "$HELPER" --token --nocache)       # 强制重新获取新版 token
> ```

## references/api.md 查阅索引
确定好要做什么之后，用以下命令从 `references/api.md` 中提取对应章节的完整 API 细节（请求格式、参数说明、返回值示例）：
```bash
grep -A 30 "^## 1. 按关键词搜索用户" references/api.md
grep -A 50 "^## 2. 获取用户完整详情" references/api.md
grep -A 20 "^## 3. unionId → userId 转换" references/api.md
grep -A 18 "^## 4. 企业员工总人数" references/api.md
grep -A 25 "^## 5. 按关键词搜索部门" references/api.md
grep -A 25 "^## 6. 获取子部门列表" references/api.md
grep -A 20 "^## 7. 获取子部门 ID 列表" references/api.md
grep -A 25 "^## 8. 获取部门详情" references/api.md
grep -A 40 "^## 9. 获取部门成员完整列表" references/api.md
grep -A 18 "^## 10. 获取部门成员 userId 列表" references/api.md
grep -A 20 "^## 11. 获取用户所在部门路径" references/api.md
grep -A 12 "^## 错误码" references/api.md
grep -A 6 "^## 所需应用权限" references/api.md
```
