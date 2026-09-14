---
name: lanhu-design
description: 蓝湖设计稿与 Axure 原型分析。通过 lanhu MCP Server 直接读取蓝湖项目的原型页面、设计图、切图资源。

  触发场景：
  - 需要从蓝湖获取 Axure 原型页面进行需求分析
  - 需要查看蓝湖 UI 设计图和设计参数
  - 需要提取蓝湖设计稿中的切图资源
  - 需要通过蓝湖团队留言板协作
  - 收到蓝湖邀请链接需要解析

  触发词：蓝湖、lanhu、设计稿、原型图、蓝湖链接、设计图、切图
---

# 蓝湖设计稿分析

## 前置条件

lanhu MCP Server 已注册在Trae CN/User/mcp.json中。首次使用需配置蓝湖 Cookie：

1. 浏览器登录蓝湖 → F12 开发者工具 → Network → 复制请求头中的 Cookie
2. 填入 `.claude/settings.json` 的 `lanhu.env.LANHU_COOKIE`

## MCP 工具清单

| 工具 | 用途 | 输入 |
|------|------|------|
| `lanhu_resolve_invite_link` | 解析蓝湖邀请链接 | 邀请链接 URL |
| `lanhu_get_pages` | 获取原型文档页面列表+截图 | 含 docId 的蓝湖 URL |
| `lanhu_get_ai_analyze_page_result` | AI 分析原型页面（开发/测试/探索视角） | 含 docId 的 URL + 页面名 + 模式 |
| `lanhu_get_designs` | 获取 UI 设计图列表 | 不含 docId 的蓝湖 URL |
| `lanhu_get_ai_analyze_design_result` | AI 分析设计图（含尺寸/颜色/CSS） | 不含 docId 的 URL + 设计图名 |
| `lanhu_get_design_slices` | 提取设计稿切图资源 | 不含 docId 的 URL + 设计图名 |
| `lanhu_say` | 发送团队留言 | URL + 内容 |
| `lanhu_say_list` | 查询留言列表 | URL 或 'all' |
| `lanhu_say_detail` | 查看留言详情 | 消息 ID |
| `lanhu_say_edit` | 编辑留言 | URL + 消息 ID + 新内容 |
| `lanhu_say_delete` | 删除留言 | URL + 消息 ID |
| `lanhu_get_members` | 获取项目成员 | URL |

## URL 类型区分（重要）

| URL 类型 | 特征 | 用于 |
|---------|------|------|
| **原型文档 URL** | 含 `docId` 参数 | `lanhu_get_pages`、`lanhu_get_ai_analyze_page_result` |
| **设计项目 URL** | 不含 `docId` | `lanhu_get_designs`、`lanhu_get_design_slices` |
| **邀请链接** | `lanhuapp.com/link/#/invite?sid=xxx` | 先用 `lanhu_resolve_invite_link` 解析 |

## 典型工作流

### 1. 需求分析（与 analyze-requirements 联动）

```
收到蓝湖链接
  │
  ├─ 邀请链接？ → lanhu_resolve_invite_link → 获取真实 URL
  │
  ├─ 含 docId？（原型文档）
  │   ├─ lanhu_get_pages → 获取页面列表和截图
  │   └─ lanhu_get_ai_analyze_page_result(mode="development") → 获取字段/逻辑/流程
  │
  └─ 不含 docId？（设计项目）
      ├─ lanhu_get_designs → 获取设计图列表
      └─ lanhu_get_ai_analyze_design_result → 获取尺寸/颜色/CSS
```

### 2. 前端开发（获取设计参数）

```
lanhu_get_designs → 查看设计图列表
  → lanhu_get_ai_analyze_design_result → 获取精确设计参数（尺寸/间距/颜色/字体）+ HTML+CSS 代码
  → lanhu_get_design_slices → 提取切图/图标资源
```

### 3. 分析模式选择

`lanhu_get_ai_analyze_page_result` 支持 3 种模式：

| 模式 | 关注点 | 适用场景 |
|------|--------|---------|
| `development` | 字段规则、业务逻辑、全局流程图 | 后端/前端开发 |
| `testing` | 测试场景、用例、边界值、校验规则 | 测试编写 |
| `exploration` | 核心功能概览、模块依赖、评审要点 | 需求评审 |

## 与其他技能联动

| 场景 | 先用 lanhu-design | 再用 |
|------|-------------------|------|
| 需求分析 | 获取原型截图和页面结构 | `analyze-requirements` 输出开发任务清单 |
| 前端开发 | 获取设计参数和切图 | `ui-pc` 实现页面 |
| 接口开发 | 从原型推导接口字段 | `api-development` / `crud-development` |

## 注意

- 蓝湖 Cookie 有效期有限，过期需重新获取
- 原型文档和设计项目使用不同的 URL 格式，工具不能混用
- 大型原型建议分页面分析，避免单次请求过大
- 与 `analyze-requirements` 的区别：本技能负责**从蓝湖获取数据**，`analyze-requirements` 负责**分析数据输出任务**
