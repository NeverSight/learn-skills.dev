---
name: cicpa-company-query
description: >
  Use when querying company business registration info (工商信息) from CICPA system (中注协行业知识库).
  Triggers on 工商信息, 企业查询, 法人, 注册资本, 注册地址, 地址核查, 查公司, 企业详情, 子公司,
  关联方识别的子公司发现, 单个公司查询.
  Full export (--browser-export) triggers on 全量, 完整维度, 所有维度, 60+维度, 60多个维度,
  53个Excel, 全部工商信息, 完整企业画像, 尽调, 尽职调查.
  Also triggers on 批量查企业, 注协查询, cicpa query, audit working papers needing company background.
slug: nigo-cicpa-company-query
displayName: 中注协企业工商查询
version: 1.0.0
summary: 从中注协行业知识库查询企业工商注册信息（法人、注册资本、注册地址等），支持单个查询和全量60+维度导出。
license: MIT
---

# 注协系统工商信息查询

> ## ⛔ 绝对禁止使用 MCP 工具
>
> `sw-audit-toolbox_cicpa_query` 的 export/subsidiary 模式有已知的 **Playwright sync/async 冲突 bug**，
> 在当前环境调用必定崩溃。
>
> **必须且只能使用 CLI 脚本**。所有命令见下方 Quick Reference。
>
> 如果你在工具列表中看到了 MCP 工具，**忽略它们**，按照下方 CLI 命令执行。

## Overview

通过中注协行业知识库（zsk-cmis.cicpa.org.cn）查询企业工商信息。四种模式：
- **轻量搜索**：单企业关键词搜索，返回基础信息 + org_id
- **企业详情**：单企业完整详情（工商信息 + 股东 + 主要人员 + 股权结构）
- **基础查询**：批量查询 22 个字段，输出单 Excel
- **完整导出**：61 个维度、53 个 Excel 文件打包 ZIP（纯 API）

无需配置文件，通过 AI 控制浏览器登录获取 cookies，24 小时内复用。

### ⚠️ Cookie 文件位置（重要）

Cookie 文件保存在**当前工作目录**（`Path.cwd()`）下的 `.cicpa_cookies.json`，不是用户主目录。

**AI 执行命令时必须确保工作目录正确**：
- 如果在项目目录下执行，cookie 就在项目目录下
- `related-party-identification` 等其他 skill 调用时，也在同一工作目录找 cookie
- **不要**在 `~`（主目录）下运行 cookie 相关命令，否则会保存到 `~/.cicpa_cookies.json`，其他项目找不到

## Mode Selection ⚠️ 关键决策

| 用户说的 | 模式 | 命令 |
|----------|------|------|
| "查一下XX公司"、"XX的工商信息" | 轻量搜索 | `search_company("XX")` |
| "XX公司详情"、"XX股东、高管" | **企业详情** | `--detail "XX"` |
| "全量工商信息"、"完整维度"、"60多个维度" | **完整导出** | `--browser-export` |
| "查一下地址"、"注册资本多少" | 基础查询 | `-n "企业名"` |
| "批量查企业工商信息" | 基础查询 + `--all-fields` | `-n ... --all-fields` |
| "发现XX的子公司" | 子公司发现 | `--discover-subsidiaries "XX"` |
| **不确定** | **问用户** | |

### 输出对比

| | 轻量搜索 | 企业详情 | 基础查询 | 完整导出 |
|---|---------|---------|---------|---------|
| 耗时 | <1 秒 | 2~3 秒 | 5~10 秒 | 30 秒~3 分钟 |
| 字段 | 基础 20+ | 工商+股东+人员+股权 | 10~22 个 | **61 维度** |
| 输出 | 返回 dict | 终端+JSON | 单 Excel | ZIP (53 个 Excel) |
| API | home_search (轻量) | 4 个详情 API | batch upload | batch export |

**⚠️ 禁止：先用基础查询再补完整导出。** 用户要"全量"就一步到位 `--browser-export`。

## Quick Reference

```bash
SCRIPT=~/.claude/skills/cicpa-company-query/scripts/cicpa_query.py

# ===== 轻量搜索（Python 函数，非 CLI）=====
# 返回 [{name, org_id, legal_person, address, ...}]
# from cicpa_query import search_company
# results = search_company("华为技术有限公司")

# ===== 企业详情（--detail）=====
# 按名称搜索（自动获取 org_id）
python3 $SCRIPT --detail "华为技术有限公司"

# 按 org_id 直接查询
python3 $SCRIPT --detail "T003573795" -o output.json

# ===== 子公司发现（--discover-subsidiaries）=====
# 发现持股 >= 50% 的子公司
python3 $SCRIPT --discover-subsidiaries "天津卓朗科技发展有限公司"

# 自定义阈值
python3 $SCRIPT --discover-subsidiaries "天津卓朗科技发展有限公司" --subsidiary-threshold 30

# ===== 基础查询 =====
python3 $SCRIPT -n "华为技术有限公司"

# 基础查询（全部 22 个字段）
python3 $SCRIPT -n "企业名" --all-fields

# 从文件读取企业名单
python3 $SCRIPT -f companies.xlsx

# ===== 完整导出（53 个 Excel → ZIP）=====
python3 $SCRIPT -n "企业A" "企业B" --browser-export

# ===== Cookies 管理 =====
# ⚠️ Cookie 文件在当前工作目录下：./cicpa_cookies.json
# 确保用 workdir 参数指定正确目录，不要在 ~ 下运行
python3 $SCRIPT --check-cookies
python3 $SCRIPT --save-cookies '{"XSRF-TOKEN":"xxx","cicpa_token":"xxx",...}'
python3 $SCRIPT --login
```

### 输出选项

| 参数 | 说明 |
|------|------|
| `--detail ID_OR_NAME` | **单企业详情**（org_id 或名称） |
| `--discover-subsidiaries NAME` | **发现子公司**（默认持股>=50%） |
| `--subsidiary-threshold N` | 子公司持股阈值（配合上一参数，默认 50） |
| `-o PATH` | 指定输出路径 |
| `--all-fields` | 导出全部 22 个字段（默认 10 个） |
| `--by-dimension` | 按维度分类导出多个 Excel → ZIP |
| `--browser-export` | **完整导出**（61 维度，53 个 Excel → ZIP） |
| `--save-cookies JSON` | 保存 AI 抓取的 cookies（JSON 字符串） |
| `--login` | 终端手动浏览器登录 |

### Python API（供其他 skill 调用）

```python
import sys
sys.path.insert(0, '<cicpa-scripts-dir>')
from cicpa_query import search_company, discover_subsidiaries, get_company_detail
```

**三个函数的区别（AI 选择依据）：**

| | `search_company` | `discover_subsidiaries` | `get_company_detail` |
|---|---|---|---|
| API 调用 | 1 次（home_search） | 2 次（search + equity） | 4 次（basic+holders+persons+equity） |
| 输入 | 关键词 | 企业名称 + 阈值 | org_id 或名称 |
| 返回 | `[{name, org_id, ...}]` | `[{name, ratio, org_id}]` | `{basic_info, shareholders, ...}` |
| 耗时 | <1 秒 | 1~2 秒 | 2~3 秒 |
| **何时用** | 只需 org_id 或确认企业存在 | 查"这家公司投资/控股了谁" | 查"这家公司的完整信息" |

```python
# ① 只需 org_id 或基础信息 → search_company
#    场景：确认企业名称、拿 org_id 给其他函数用
results = search_company("华为技术有限公司")
# → [{"name": "华为技术有限公司", "org_id": "T003573795", "legal_person": "任正非", ...}]

# ② 查子公司/对外投资 → discover_subsidiaries
#    场景：关联方预查、合并下载名单
subs = discover_subsidiaries("审计目标", threshold=50)
# → [{"name": "子公司A", "ratio": 100.0, "org_id": "Txxx"}, ...]

# ③ 查一家公司的完整信息 → get_company_detail
#    场景：审计中了解交易对手、函证地址核查、单公司尽调
detail = get_company_detail("T003573795", "天津卓朗科技发展有限公司")
# → {
#     "basic_info": {name, address, capital, legal_person, ...},
#     "shareholders": {list: [{holder_name, held_ratio, ...}]},
#     "main_persons": {tab_list, ...},
#     "equity": {holders: {...}, invests: {...}}
#   }
```

### 完整导出包含的维度（5 大类 53 个文件）

| 维度 | 文件数 | 内容示例 |
|------|--------|---------|
| 基本信息 | 14 | 工商信息、股东、变更记录、分支机构、主要人员 |
| 经营情况 | 18 | 招投标、商标、专利、客户、供应商、税务信息 |
| 企业发展 | 7 | 对外投资、融资历史、核心团队、债券信息 |
| 经营风险 | 13 | 行政处罚、欠税、经营异常、股权出质、注销 |
| 司法风险 | 9 | 裁判文书、立案、开庭公告、被执行人、失信 |

## When to Use

**AI 决策指南：用户要什么 → 用哪个**

| 用户说/需要 | 用什么 | 为什么 |
|------------|--------|--------|
| "查一下这家公司"、"确认企业名称" | `search_company()` | <1 秒，只拿基础信息 |
| "这家公司投资了谁"、"查子公司" | `--discover-subsidiaries` | equity API 拿对外投资 |
| "这家公司详情"、"查股东高管" | `--detail` | 4 个 API 拿完整信息 |
| "批量查企业"、"查几个字段" | `-n` + `--all-fields` | batch 查询，输出 Excel |
| "全量"、"完整维度"、"60多个维度" | `--browser-export` | 61 维度 53 个 Excel |

**特殊场景：被其他 skill 调用**
- `related-party-identification` 预查子公司 → 调用 `discover_subsidiaries()`
- `related-party-identification` 需要拿 org_id → 调用 `search_company()`
- 函证地址核查只需地址/电话 → `search_company()` 已足够，不需要 `--detail`

## When NOT to Use

- 只需要天眼查/企查查的单个企业信息（用网页直接查更快）
- 需要 A 股上市公司财报数据（用 a-stock-financial skill）
- 需要法律法规查询（用 china-law-search skill）

## 前置条件

1. **依赖**：`pip install requests openpyxl`（浏览器登录还需 `playwright`）
2. **无需配置文件**

## Cookie 自动检查与获取流程

**AI 在任何需要调用注协 API 的操作前，必须先检查 cookie。全自动化，不要问用户。**

### ⚠️ 浏览器工具选择（强制）

| 工具 | 是否可用 | 说明 |
|------|---------|------|
| **`playwright-mcp_*`** (Playwright MCP) | ✅ **必须用这个** | 打开可见浏览器窗口，用户能看到并操作 |
| `agent-browser` | ❌ **禁止使用** | 无头模式，用户看不到浏览器窗口，无法手动登录 |
| 脚本内 `--login` | ❌ **禁止使用** | 检测到非交互式终端会失败 |

**原因**：登录需要用户手动操作（拖滑块验证），必须打开用户可见的浏览器窗口。只有 `playwright-mcp_*` 系列工具能做到这一点。

### 自动流程

```
① 检查本地 cookie（每次执行查询前自动做）
   bash: python3 $SCRIPT --check-cookies
   （⚠️ 用 workdir 指定项目目录）

② ✅ 有效 → 直接执行查询命令，无需任何登录操作

③ ❌ 无效/不存在 → AI 自动启动浏览器登录：
   告诉用户："Cookie 已过期/不存在，正在打开浏览器，请手动登录"
   
   步骤 1：打开登录页
     调用 playwright-mcp_browser_navigate → https://cmis.cicpa.org.cn/#/login
     → 告诉用户："请在浏览器中登录（选用户类型、输入密码、拖滑块）"

   步骤 2：用户说"已登录"后，点击「行业执业知识库」
     调用 playwright-mcp_browser_snapshot → 找到"行业执业知识库"菜单项
     调用 playwright-mcp_browser_click → 点击该菜单项
     调用 playwright-mcp_browser_wait_for → 等待新标签页加载

   步骤 3：导航到企业数据库并抓取 cookies
     调用 playwright-mcp_browser_tabs → 切换到新打开的 zsk 标签页
     调用 playwright-mcp_browser_navigate → https://zsk-cmis.cicpa.org.cn/companylibrarynew/
     调用 playwright-mcp_browser_run_code_unsafe → 执行以下代码获取并转换 cookie：
       ```javascript
       const cookies = await page.context().cookies();
       const cookieDict = cookies.reduce((acc, c) => { acc[c.name] = c.value; return acc; }, {});
       JSON.stringify(cookieDict);
       ```
     ⚠️ **Cookie 格式转换（必须）**: page.context().cookies() 返回 `[{name, value, ...}]` 数组，
     上面的 JS 代码已经转换为 `{name: value}` 字典格式

   步骤 4：保存并验证
     bash（⚠️ workdir 必须是项目目录）:
       python3 $SCRIPT --save-cookies '<步骤3返回的JSON>'
       python3 $SCRIPT --check-cookies → 确认 ✅ 有效

④ 如果 Playwright MCP 工具不可用 → 退化为手动方式：
   提示用户手动登录后粘贴 cookie，或在交互终端运行 python3 cicpa_query.py --login
```

**Playwright MCP 工具映射：**

| 步骤 | 工具 | 说明 |
|------|------|------|
| 打开页面 | `playwright-mcp_browser_navigate` | 导航到 URL |
| 查看页面 | `playwright-mcp_browser_snapshot` | 获取页面快照（无障碍树） |
| 点击元素 | `playwright-mcp_browser_click` | 点击按钮/链接 |
| 切换标签 | `playwright-mcp_browser_tabs` | list/new/close/select |
| 等待加载 | `playwright-mcp_browser_wait_for` | 等待文本/元素/URL 变化 |
| 获取 cookies | `playwright-mcp_browser_run_code_unsafe` | 执行 `page.context().cookies()` |
| 截图调试 | `playwright-mcp_browser_take_screenshot` | 查看当前页面状态 |

### 备用方式：手动从浏览器 F12 抓取 cookies

仅在 Playwright MCP 不可用时使用：

```
1. 打开浏览器访问 https://cmis.cicpa.org.cn，手动登录
2. 登录成功后访问 https://zsk-cmis.cicpa.org.cn/companylibrarynew/
3. F12 → Network → 刷新 → 找「companylibrarynew」请求 → 复制 Cookie 请求头
4. 粘贴给 AI
```

用户粘贴后，AI 解析 `key1=value1; key2=value2` 为 `{key1: value1, key2: value2}` 格式，然后保存：
```bash
python3 $SCRIPT --save-cookies '{解析后的JSON}'
python3 $SCRIPT --check-cookies
```

> **为什么不用 `document.cookie`？** `document.cookie` 无法获取 HttpOnly 的 cookie（如 `__snaker__id`、`gdxidpyhxdE`），只能拿到部分 cookie。

### ⚠️ 关键：必须走完整 SSO 流程

| 场景 | 获得的 cookies | 能否查询 |
|------|---------------|---------|
| 只登录 cmis，不进知识库 | 4 个（不完整） | ❌ 报"未登陆用户" |
| 登录 cmis → **点击知识库** → 跳转 zsk | **9 个**（完整） | ✅ 正常 |

**必须的 9 个 cookies**：`XSRF-TOKEN`、`yuqing_whole_jsessionid`、`cicpa_token`、`cicpa_ticket`、`companyVerifyCode`、`userid`、`u_name`、`__snaker__id`、`gdxidpyhxdE`

如果 `--check-cookies` 显示少于 9 个，说明 SSO 流程不完整，需要重新登录。

### Cookie 文件格式说明

`.cicpa_cookies.json` 必须是以下格式的 JSON（保存到当前工作目录）：

```json
{
  "cookies": {
    "XSRF-TOKEN": "xxx",
    "yuqing_whole_jsessionid": "xxx",
    "cicpa_token": "xxx",
    "cicpa_ticket": "xxx",
    "companyVerifyCode": "xxx",
    "userid": "xxx",
    "u_name": "xxx",
    "__snaker__id": "xxx",
    "gdxidpyhxdE": "xxx"
  },
  "session_token": "xxx",  // 可选，从 localStorage 获取
  "saved_at": 1719123456.789  // ⚠️ 必须字段，Unix 时间戳，用于检查 24 小时有效期
}
```

**关键点**：
- `cookies` 字段必须是 `{name: value}` 格式，不是 `[{name, value}]` 数组
- `saved_at` 字段是必需的，用于检查 cookie 是否超过 24 小时过期
- 通过 Playwright 的 `page.context().cookies()` 获取时需要转换格式

### MCP 模式的已知限制

如果通过 MCP 工具（如 `cicpa_query` MCP）调用 `export` 或 `subsidiary` 模式：
- **Cookie 失效时会触发浏览器登录**：在无头模式下打开浏览器会导致崩溃
- **建议优先使用 CLI 模式**：通过 `--login` 参数在交互式终端中登录，或使用 `--save-cookies` 手动保存

### 注意点

```bash
python3 $SCRIPT --check-cookies
# → 显示 cookie 数量、名称、剩余有效期
# → ✅ 有效 或 ❌ 需要重新登录
```

| 注意点 | 说明 |
|--------|------|
| **企业名称必须精确** | 用工商注册全称（如"深圳市腾讯计算机系统有限公司"），简称无法匹配 |
| **Cookies 24h 过期** | 过期后需重新登录 |
| **最多 10,000 家** | 单次批量查询上限 |
| **导出耗时** | 10 家约 45 秒，100+ 家可能 2-3 分钟 |
| **自动验证** | 完整导出后自动对比输入 vs 输出公司名称，报告匹配情况 |

## Common Mistakes

| 问题 | 原因 | 解决 |
|------|------|------|
| **用户要"全量"却只给了基础查询** | 没看 Mode Selection，用了默认模式 | 用户说"全量/完整/所有维度"→ 必须用 `--browser-export` |
| **先用基础查询再补完整导出** | 分两步浪费时间 | 用户要全量就一步到位，不要多此一举 |
| **Cookie 保存到了主目录** | 在 `~` 下执行命令，cookie 保存到 `~/.cicpa_cookies.json` | **所有命令必须在项目工作目录下执行**（bash 用 `workdir` 参数） |
| **其他 skill 找不到 cookie** | 工作目录不一致，cookie 在另一个目录 | 确保 `--save-cookies`、`--check-cookies`、扫描脚本都在同一 `workdir` 下运行 |
| 查询报"未登陆用户" | 只有 4 个不完整 cookie | 重新登录，确保点了「行业执业知识库」，拿到 9 个 cookie |
| 上传后匹配 0 家 | 企业名称非注册全称 | 用精确的工商注册名 |
| Cookies 无效 | 超过 24 小时 | 重新登录获取 cookies |
| 导出轮询超时 | 数据量大或系统繁忙 | 等待后手动去下载中心下载 |
| XSRF 报错 | cookies 中缺少 XSRF-TOKEN | 重新登录 |

## 目录结构

```
~/.claude/skills/cicpa-company-query/
  SKILL.md                    # 本文档
  scripts/
    cicpa_query.py            # 主脚本
```


---

> 作者：nigo
> 微信公众号：逆行的狗
