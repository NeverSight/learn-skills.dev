---
name: wfdata-search
description: "用于从万方数据检索文献"
reference:
  - reference/api-catalog.md
---
# 万方数据搜索技能

本技能提供万方数据平台的文献检索能力，支持：

- 文献关键词检索
- 文献详情获取
- 基于语义的向量检索

完整 API 说明请参考：

👉 `reference/api-catalog.md`

该文档包含：

- API 接口地址
- 请求参数
- 返回结构
- 文献类型说明

---

## 工具脚本

- `scripts/wf_data_query.py` - 文献关键词检索
- `scripts/wf_data_get_doc.py` - 获取文献详情
- `scripts/wf_data_vector_search.py` - 向量语义检索

---

# 认证信息

所有接口需要以下请求头：

| Header | 说明 |
|------|------|
| X-Ca-AppKey | 应用 Key |
| Authorization | APPCODE 认证码 |
| Content-Type | application/json |

---

# 工具说明

## 1. 文献检索 (使用wf_data_query)

搜索万方数据库中的文献资源。

该工具适用于：

- 文献检索
- 按关键词搜索论文
- 按文献类型筛选

### 参数

| 参数 | 类型 | 必填 | 说明 |
|----|----|----|----|
| query | string | 是 | 检索关键词 |
| collections | string[] | 否 | 文献类型 |
| rows | int | 否 | 返回条数 |
| start | int | 否 | 起始位置 |


### 可用 collections

| collection               | 说明   |
| ------------------------ | ---- |
| OpenPeriodical           | 期刊论文 |
| OpenPeriodicalChi        | 中文期刊 |
| OpenPeriodicalEng        | 英文期刊 |
| OpenThesis               | 学位论文 |
| OpenConference           | 会议论文 |
| OpenPatent               | 专利   |
| OpenClaw                 | 法规   |
| OpenCstad                | 成果   |
| OpenStandard             | 标准   |
| OpenMagazine             | 刊名   |
| OpenMeeting              | 会议名录 |
| OpenNstr                 | 科技报告 |
| OpenVideo                | 视频   |
| OpenFZLocalChronicle     | 方志   |
| OpenFZLocalChronicleItem | 方志条目 |

更多字段和高级参数请参考：

👉 `reference/api-catalog.md`

---

# 2. 获取文献详情 (wf_data_get_doc)

根据文献 ID 获取文献详细信息。

### 参数

| 参数         | 类型     | 必填 | 说明    |
| ---------- | ------ | -- | ----- |
| collection | string | 是  | 文献资源库 |
| doc_id     | string | 是  | 文献 ID |


---

# 3. 向量语义搜索 (wf_data_vector_search)

通过自然语言进行语义搜索，系统会匹配语义相似的论文片段。

适用于：

* 自然语言搜索
* 研究问题检索
* 语义相关文献发现

### 参数

| 参数          | 类型       | 必填 | 说明     |
| ----------- | -------- | -- | ------ |
| query_text  | string   | 是  | 自然语言查询 |
| collections | string[] | 否  | 全文资源库  |



### 可用全文 collections

| collection                 | 说明     |
| -------------------------- | ------ |
| OpenPeriodicalFulltext     | 期刊全文   |
| OpenThesisFulltext         | 学位论文全文 |
| OpenConferenceFulltext     | 会议论文全文 |
| OpenPatentFulltext         | 专利全文   |
| OpenClawFulltext           | 法规全文   |
| OpenStandardFulltext       | 标准全文   |
| OpenLocalchronicleFulltext | 方志全文   |

---

# 推荐调用流程

对于科研问题，建议 Agent 使用以下流程：

```
用户问题
   ↓
wf_data_vector_search（语义检索）
   ↓
获取文献ID
   ↓
wf_data_get_doc（获取文献详情）
   ↓
整理研究结果
```

对于精准关键词搜索：

```
用户关键词
   ↓
wf_data_query
   ↓
获取文献ID
   ↓
wf_data_get_doc
```

---

# 返回结果

所有接口返回 JSON 数据。

典型结构：

```json
{
  "documents": [],
  "num_found": 120
}
```

---

# 注意事项

1. 请确保配置正确的 API 认证信息
2. 向量搜索适合语义问题检索
3. 关键词检索适合精确查找
4. 建议 rows 不超过 50