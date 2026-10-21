---
name: china-law-search
description: 中国国家法律法规数据库（flk.npc.gov.cn）查询工具。支持法规搜索、详情查看、状态检查、按日期筛选新发布法规、批量状态核查。触发词：法律法规、法规查询、法规检索、法规状态、法规废止、法规修订、新发布法规、flk、国家法律法规数据库、china law、law search、规章查询、部门规章、地方规章、国家规章库、规章检索、gov.cn规章。
slug: nigo-china-law-search
displayName: 国家法律法规查询
version: 1.0.0
summary: 中国国家法律法规数据库（flk.npc.gov.cn）查询工具，支持法规搜索、详情查看、状态检查、按日期筛选新发布法规、批量状态核查。
license: MIT
---

# 中国法律法规统一查询

统一查询入口，自动先查国家法律法规数据库（flk.npc.gov.cn），查不到再 fallback 到国家规章库（gov.cn）。

覆盖范围：
- 国家法律法规数据库：宪法、法律、行政法规、地方法规、司法解释、监察法规
- 国家规章库：部门规章、地方政府规章

## When to Use

- 查询某条法律法规/规章是否仍然有效
- 搜索某个关键词相关的法律法规或规章
- 查找某个日期之后新发布的法律法规
- 批量检查一批法规的当前状态（自动两库联查）
- 从Excel读取法规清单，批量检查有效性并输出Excel结果
- 查询新发布法规并直接输出Excel
- 批量下载法规全文（docx）
- 下载法规全文（docx/pdf）

## 使用方式

### Python API（AI Agent 推荐用法）

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/china-law-search/scripts"))
import law_search

# ── 搜索 ──
result = law_search.unified_search("安全生产法")
result = law_search.unified_search("危险化学品 安全管理", content_search=True)

# ── 批量检查 ──
results = law_search.unified_batch_check(["法规名称1", "法规名称2"])

# ── 从Excel批量检查并输出Excel（一步到位，支持断点续查）──
law_search.batch_check_to_excel(
    input_excel="法律法规清单.xlsx",
    output_excel="法规有效性查询结果.xlsx",
    col="B",              # 法规名称所在列
    start_row=2,           # 数据起始行（跳过表头）
    progress_file="check_progress.json",  # 断点续查进度文件
)

# ── 查询新发布法规并输出Excel ──
law_search.new_since_to_excel("2026-01-01", "2026年新发布法规.xlsx")

# ── 批量下载法规全文（推荐工作流：查询→转格式→下载→重试）──
import json

# Step 1: 批量查询
results = law_search.unified_batch_check(["法规名称1", "法规名称2"])

# Step 2: 转成 batch_download_from_check 需要的格式
check_progress = {}
for r in results:
    name = r.get("name", "")
    check_progress[name] = {
        "status": r.get("status", ""),
        "url": r.get("url", ""),
        "source": "国家规章库" if r.get("source") == "gov.cn" else "国家法律法规数据库",
    }

# Step 3: 批量下载（支持断点续下）
law_search.batch_download_from_check(
    check_progress=check_progress,
    output_dir="./下载",
    delay=0.5,
    dl_progress_file="download_progress.json",
)

# Step 4: 如有超时，直接重跑（自动跳过已下载的）
law_search.batch_download_from_check(
    check_progress=check_progress,
    output_dir="./下载",
    delay=0.5,
    dl_progress_file="download_progress.json",
)

# ── 单独调用某个库 ──
from lib import flk_api, gov_api

flk_api.search("安全生产法", exact=True)
flk_api.search("危险化学品", content_search=True)
flk_api.search_all_pages("消防安全", content_search=True)

gov_api.search("商品房屋租赁管理办法")
gov_api.search("消防安全", content_search=True)

# 下载
flk_api.download_file("bbbs_id", output_dir="./downloads")
gov_api.download_as_docx("商品房屋租赁管理办法", output_dir="./downloads")
```

### CLI

```bash
LAW=~/.claude/skills/china-law-search/scripts/law_search.py

# ── 搜索 ──
python3 $LAW search "安全生产法"
python3 $LAW search "安全生产法" --exact
python3 $LAW search "危险化学品 安全管理" --content
python3 $LAW search "消防安全" --content --all-pages

# ── 批量检查 ──
python3 $LAW batch-check laws.txt
python3 $LAW batch-check laws.txt --json

# ── 从Excel批量检查并输出Excel ──
python3 $LAW check-excel 法律法规清单.xlsx -o 查询结果.xlsx --col B --progress progress.json

# ── 查询新发布法规并输出Excel ──
python3 $LAW new-since-excel 2026-01-01 -o 2026年新发布法规.xlsx

# ── 查找新发布法规（文本输出）──
python3 $LAW new-since 2025-03-09
python3 $LAW new-since 2025-03-09 --all-types --all-pages --json

# ── 下载 ──
python3 $LAW download <bbbs_id> --output ./downloads
python3 $LAW batch-download check_result.json --output ./downloads

# ── 从检查进度批量下载 ──
python3 $LAW download-from-check progress.json -o ./下载 --dl-progress dl_progress.json
```

## 文件结构

```
china-law-search/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── law_search.py           # 统一入口（推荐使用）
│   └── flk_api.py              # flk.npc.gov.cn 独立客户端（向后兼容）
└── lib/
    ├── __init__.py
    ├── flk_api.py              # 国家法律法规数据库 API
    ├── gov_api.py              # 国家规章库 API
    ├── refresh_gov_key.js      # playwright-cli 刷新 athenaappkey 脚本
    └── .athena_key_cache.json  # athenaappkey 缓存（自动生成）
```

## 核心函数一览

| 函数 | 用途 | 输入 | 输出 |
|---|---|---|---|
| `unified_search()` | 统一搜索（两库） | 关键词 | dict |
| `unified_batch_check()` | 批量检查状态 | 名称列表 | list |
| `batch_check_to_excel()` | Excel→批量检查→Excel | 输入Excel路径 | 输出Excel |
| `new_since_to_excel()` | 新发布法规→Excel | 日期 | Excel文件 |
| `unified_new_since()` | 新发布法规查询 | 日期 | dict |
| `batch_download_from_check()` | 批量下载全文 | 检查进度dict | 下载进度dict |

## 输出字段说明

所有查询结果统一包含以下字段：

| 字段 | 说明 |
|---|---|
| title | 法规名称 |
| type / flxz | 法规类别（法律/行政法规/部门规章/地方政府规章等） |
| date / gbrq | 公布日期 |
| status / sxx_text | 状态（有效/已修改/已废止/尚未生效） |
| org / zdjgName | 制定机关 |
| source | 数据来源：`国家法律法规数据库` 或 `国家规章库` |
| url | 原文链接（可点击） |

## 文件下载

### 国家法律法规数据库（flk）
- 直接下载官方 docx/pdf 文件，通过签名 URL 从 OSS 获取
- flk 有 JS 反爬保护，`download_file()` 内部通过 playwright-cli 获取签名URL绕过

### 国家规章库（gov.cn）
- 规章库没有直接的文件下载接口
- 通过抓取详情页 HTML，用 pandoc 转 docx（保留原始格式）
- 依赖：需要安装 `pandoc`（`brew install pandoc`）和 `python-docx`（`pip install python-docx`）

### 批量下载
- `batch_download_from_check()` 从检查进度数据批量下载
- 自动区分 flk 和规章库，使用不同下载方式
- 支持断点续下（通过 dl_progress_file 参数）

## athenaappkey 管理

国家规章库 API 需要动态认证 key，约 1 小时过期。

### 自动刷新
`gov_api.py` 检测到 key 过期或无效时，会自动通过 playwright-cli 拦截浏览器请求获取新 key，并验证有效性后再缓存。流程：
1. 用 `playwright-cli open` 打开规章库页面
2. 用 `playwright-cli --raw run-code` 拦截 `athena/forward` 请求，提取 `athenaappkey` header
3. 发一个测试请求验证 key 有效性（`resultCode.code == 200`）
4. 验证通过后保存到缓存，关闭浏览器

如果自动刷新失败（playwright-cli 不可用或网络问题），可按下方"athenaappkey 刷新标准流程"手动获取。

## 文件命名规则

下载文件命名: `法规类型_法规名称_公布日期_状态.ext`
例如: `法律_中华人民共和国安全生产法_2021-06-10_有效.docx`

## 已知问题与经验

### flk 下载超时与重试
- flk.npc.gov.cn 的下载 API 有 JS 反爬保护，直接 HTTP 请求会返回 HTML 而非 JSON
- 解决方案：`flk_api.download_file()` 内部通过 playwright-cli 获取签名下载URL
- 如果 playwright-cli 不可用，下载会失败
- 批量下载时可能出现间歇性超时（`The read operation timed out`），这是 flk 的反爬触发了
- `batch_download_from_check()` 支持断点续下，超时的条目重跑即可自动跳过已完成的
- **建议批量下载 delay 保持 0.5-1 秒**，如有超时直接重跑即可

### 规章库 API 返回格式变化（2026-04 发现）
- 规章库搜索 API 的返回结构可能有两种格式：
  - 旧格式：`result.data` 是 dict，包含 `pager` 和 `list`
  - 新格式：`result.data` 是 list（直接是结果列表），`result.totalCount` 和 `result.pageSize` 在上层
- `gov_api.py` 的 `search()` 和 `search_with_content()` 已兼容两种格式
- 当 athenaappkey 无效时，API 不会返回 HTTP 错误，而是返回 `data: []` + `resultCode` 包含错误信息（如 `athena_01503 解密失败`）
- **如果规章库返回 0 条结果但实际应该有数据，先检查 athenaappkey 是否有效**

### 规章库 athenaappkey 过期
- 规章库 API 的 athenaappkey 约1小时过期
- `gov_api.py` 已改进为自动刷新 + 验证：key 过期或无效时自动通过 playwright-cli 拦截请求获取新 key，并验证有效性
- 自动刷新依赖 playwright-cli（`@playwright/cli`），未安装时会自动通过 `npm install -g @playwright/cli` 安装
- 如果自动刷新失败（如 playwright-cli 不可用），可按"athenaappkey 刷新标准流程"手动获取

### athenaappkey 刷新标准流程（3步）

**Step 1：打开规章库页面**
```bash
playwright-cli open https://www.gov.cn/zhengce/xxgk/gjgzk/index.htm
```

**Step 2：拦截请求获取 key**
```bash
playwright-cli --raw run-code "async page => {
  const keys = [];
  await page.route(url => url.href.includes('athena/forward'), async route => {
    const key = route.request().headers()['athenaappkey'] || '';
    if (key) keys.push(key);
    await route.continue();
  });
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  await page.unroute(url => url.href.includes('athena/forward'));
  return keys.join(',');
}"
```
输出是逗号分隔的多个 key（都一样），取第一个即可。

**Step 3：保存到缓存文件**
```python
import json, time, os
key = '这里粘贴Step2输出的第一个key'
cache_path = os.path.expanduser('~/.claude/skills/china-law-search/lib/.athena_key_cache.json')
with open(cache_path, 'w') as f:
    json.dump({'key': key, 'ts': time.time()}, f)
```

**Step 4：关闭浏览器**
```bash
playwright-cli close
```

刷新后缓存有效期约1小时，足够完成大部分批量操作。

### 部分法规两库都查不到
- 通知、意见、指引等规范性文件两库都不收录
- 中央企业相关的内部管理办法通常不在公开法规库中（如"中央企业合规管理办法"在规章库可查，但"中央企业全面风险管理指引"查不到）
- 具体查不到的类型：国资委发布的"指引"、"意见"、"通知"、"工作规则"、"工作规定"
- 这类文件标记为"未找到"，需从国资委官网或其他渠道获取

### 批量操作建议
- 大批量查询（>100条）建议使用 `batch_check_to_excel()` 并指定 `progress_file`
- 进度文件支持断点续查，中断后重新运行会跳过已完成的
- 下载同理，使用 `dl_progress_file` 支持断点续下
- **查询和下载建议间隔 0.5-1 秒**，如有超时直接重跑（断点续下）
- 批量下载如有超时，重跑即可（自动跳过已完成的）

### unified_batch_check 返回格式
- 返回 list，每个元素是 dict，包含 `name`, `found`, `title`, `status`, `bbbs`, `url`, `flxz`, `source` 等字段
- `found=True` 时有完整信息，`found=False` 时只有 `name` 和 `status`
- 要传给 `batch_download_from_check()`，需要转成 `{法规名: {status, url, source, ...}}` 格式的 dict
- **注意**：`unified_batch_check` 返回的 `status` 字段对规章库结果是 `"有效（规章库）"`，`source` 是 `"gov.cn"`

### flk_api.search 返回格式
- 返回 dict（不是 list），结构为 `{"total": N, "rows": [...]}`
- 每个 row 包含 `bbbs`（ID）、`title`、`gbrq`、`sxx`（时效性编码）、`flxz`（法规分类）等
- **注意**：`gbrq` 字段可能是 `None`（不是空字符串），比较时需要处理 `None` 值
- 搜索结果可能包含不相关的法规（如搜"宪法"会返回"厦门市…关于…宪法…的决定"），`batch_check()` 内部已有精确匹配逻辑，**不要自己写匹配逻辑，直接用 `unified_batch_check`**

## Key Rules

- 批量检查时自动两库联查：先查 flk，查不到的再查规章库
- flk API 无需认证，稳定可靠
- 规章库 API 需要动态 athenaappkey，过期后会自动通过 playwright-cli 刷新并验证，通常无需手动干预。如自动刷新失败，按"athenaappkey 刷新标准流程"手动获取
- **查询和下载间隔建议 0.5-1 秒**
- 国家规章库只收录现行有效规章，已废止的不在库中
- 部分规范性文件（通知、意见、指引等）两库都不收录，需人工确认
- `--content` 按正文内容搜索，两个库都支持
- `--all-pages` 自动翻页获取全部结果，适用于结果较多的场景
- 全文搜索建议用短关键词（2-4个词），长句可能无结果
- 规章库下载通过抓取详情页 HTML 用 pandoc 转 docx，需要安装 pandoc
- Excel 输出使用 openpyxl，需要安装（`pip install openpyxl`）
- **不要自己写法规匹配逻辑**，直接用 `unified_batch_check()`，它内部已处理好精确匹配、多版本选择、None 值等边界情况
- **不要自己写下载逻辑**，用 `batch_download_from_check()` 组合 `unified_batch_check()` 的结果，它自动区分 flk/规章库并支持断点续下
- 批量下载如有超时，重跑即可（自动跳过已完成的，断点续下）

## 自我进化规则

当使用本 skill 完成任务后，如果发现以下情况，应自动更新 skill 代码和文档：

1. **新的 API 变化**：如果 flk 或规章库的 API 接口发生变化（返回格式、URL、认证方式等），更新对应的 `lib/flk_api.py` 或 `lib/gov_api.py`
2. **新的使用模式**：如果用户的使用方式产生了新的有用函数或工作流，将其集成到 `scripts/law_search.py` 并更新 SKILL.md
3. **Bug 修复**：如果在使用中发现并修复了 bug，确保修复被持久化到 skill 文件中
4. **经验积累**：如果遇到新的已知问题或解决方案，更新 SKILL.md 的"已知问题与经验"部分
5. **依赖变化**：如果发现新的依赖需求或依赖版本问题，更新文档

更新时遵循以下原则：
- 保持向后兼容，不破坏已有的 API
- 新增函数同时提供 Python API 和 CLI 接口
- 所有批量操作都支持断点续做（通过进度文件）
- 更新 SKILL.md 的函数一览表和使用示例


---

> 作者：nigo
> 微信公众号：逆行的狗
