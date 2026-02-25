---
name: social-media-automation
description: 自媒体运营自动化技能，支持小红书、抖音、微信公众号、视频号等平台的内容生成、图片生成、数据管理和自动化发布。包含 Tavily API 搜索、内容生成、图片生成、HAP 数据管理和自动化发布等完整流程。新增每日热点内容推荐功能。图片生成支持并行生成、自动下载、自动跳过已存在图片等优化功能。强制要求从 HAP "账号人设" 表读取账号人设配置，禁止使用本地文件。
version: 1.7.0
---

# 自媒体运营自动化技能

## 触发条件

当用户提到以下内容时自动触发：
- "生成小红书笔记"
- "发布到小红书"
- "生成自媒体内容"
- "发布到抖音/公众号/视频号"
- "自媒体运营"
- "社交媒体内容生成"
- "批量生成内容"
- "每日热点推荐"
- "热点内容推荐"
- "根据热点生成内容"

## MCP 配置说明

### 重要原则

**本 Skill 是通用的，不包含任何硬编码的 MCP 配置或密钥信息。**

### MCP 使用流程

1. **用户提供 MCP 配置**
   - 用户会提供 HAP 应用的 MCP 配置信息
   - MCP 配置格式：`{"hap-mcp-{应用名称}": {"url": "https://api.mingdao.com/mcp?HAP-Appkey=...&HAP-Sign=..."}}`
   - 或用户明确指定使用哪个 MCP

2. **确认当前连接的 MCP**
   - 执行操作前，必须先调用 `mcp_hap-mcp-_get_app_info()` 确认当前连接的 HAP 应用
   - 如果用户提供了 MCP 配置，需要确认是否匹配

3. **从 HAP 动态读取配置**
   - 所有 API 密钥和配置都存储在 HAP "API服务配置" 表中
   - 使用时动态从表中读取，不在代码中硬编码
   - 通过 `get_app_worksheets_list()` 动态获取工作表列表
   - **优先通过别名（alias）匹配工作表，如果别名不存在则使用名称（name）匹配**
   - **绝对不要使用硬编码的工作表 ID**

4. **工作表动态识别（重要）**
   - **不假设工作表 ID 是固定的，必须通过别名或名称匹配**
   - 通过 `get_app_worksheets_list()` 获取工作表列表
   - **优先通过 `alias` 字段匹配，如果不存在则使用 `name` 字段匹配**
   - 通过 `get_worksheet_structure()` 获取工作表结构
   - 通过字段名称或别名匹配所需字段

### MCP 确认流程

```
用户请求
    ↓
1. 识别用户提供的 MCP 配置或指定的 MCP
    ↓
2. 调用 get_app_info() 确认当前连接的 MCP 应用
    ↓
3. 对比：当前连接 vs 用户指定的 MCP
    ↓
4. 如果不匹配 → 与用户确认
    ↓
5. 确认后执行操作
```

## 核心能力

### 1. 内容生成流程

#### 完整工作流

```
用户输入主题
    ↓
Step 1: 从 HAP "API服务配置" 表动态读取搜索 API 配置（Tavily/Serper）
    ↓
Step 2: 调用搜索 API 获取主题相关资料（Tavily API）
    ↓
Step 3: **【强制要求】从 HAP "账号人设" 表读取账号人设配置（必须在生成内容之前执行）**
    - **禁止使用本地文件**：绝对不允许使用 `AGENTS.md` 或其他本地文件作为账号人设来源
    - **必须调用 HAP MCP**：必须通过 MCP 调用 `get_record_list()` 从 HAP "账号人设" 表读取
    - **读取流程**：
      1. 确认当前连接的 HAP MCP 应用（通过 `get_app_info()`）
      2. 动态获取"账号人设"表的 ID（通过别名 `account_persona` 或名称 `账号人设` 匹配）
      3. 根据 `platform_type` 查询对应平台的账号人设（如：小红书）
      4. **读取所有必需字段**：
         - 账号定位（positioning）
         - 目标受众（target_audience）
         - 内容方向（content_direction）
         - 内容风格（content_style）**【必须严格遵循】**
         - 内容原则（content_principles）**【必须严格遵守】**
         - 图片生成提示词（image_generation_prompt）
    - **验证要求**：如果未找到账号人设配置，必须抛出异常，不允许继续生成内容
    ↓
Step 4: 根据搜索结果和账号人设撰写内容
    - **严格遵循账号人设**：必须严格按照从 HAP 读取的 `content_style` 和 `content_principles` 生成内容
    - **禁止使用本地人设**：不允许参考或使用本地 `AGENTS.md` 文件中的内容
    - **结合搜索资料**：将搜索到的资料与从 HAP 读取的账号人设结合，生成符合账号定位的内容
    - **确保符合人设**：确保内容符合目标受众、内容方向和账号定位
    ↓
Step 5: 生成封面标题（5-10个备选）
    - 根据账号人设的内容风格生成标题
    - 符合账号定位和目标受众
    ↓
Step 6: 选择话题标签（从 HAP 话题库）
    - 根据内容主题和账号人设的内容方向选择
    ↓
Step 7: 生成配图建议
    - 结合账号人设的图片生成提示词风格
    - 根据内容主题生成配图建议
    ↓
Step 8: 保存到本地文件（预览，按笔记目录结构组织）
    ↓
Step 9: 与用户确认内容、标题、图片
    ↓
Step 10: 用户确认后，从 HAP "账号人设" 表读取图片生成提示词（图片风格）
    ↓
Step 11: 从 HAP "API服务配置" 表动态读取图片生成功能配置
    ↓
Step 12: 结合图片风格提示词和配图建议，生成完整提示词
    ↓
Step 13: 提取密钥，生成图片（可选，使用配置的 API 服务）
    ↓
Step 14: 与用户确认是否直接发布至小红书
    ↓
Step 15: 与用户确认是否同步到 HAP，确认后才上传
    - **小红书笔记**：只上传图片 URL（封面图和其他配图），不上传 Markdown 文档
    - **其他平台**：根据平台需求上传图片和文档
    - **关联选题（如果适用）**：
      - 如果内容是基于选题库中的选题创作的，在创建内容记录时关联对应的选题（`related_topic` 字段）
      - 如果内容不是基于选题创作的，不关联选题
    ↓
Step 16: 发布到目标平台（使用 Playwright MCP，如用户确认）
```

#### 每日热点内容推荐工作流

```
用户请求热点内容推荐
    ↓
Step 1: 从 HAP "热点平台关注表" 读取用户关注的平台（is_followed = 1）
    - 按优先级（priority）排序
    - 获取平台代码（platform_code）
    ↓
Step 2: 从 HAP "API服务配置" 表读取热点新闻 API 配置
    - 功能名称：热点新闻API
    - 服务类型：热点新闻
    - Endpoint URL: https://orz.ai/api/v1/dailynews
    ↓
Step 3: 调用热点新闻 API 获取各平台热点
    - 对每个关注的平台调用：GET https://orz.ai/api/v1/dailynews/?platform={platform_code}
    - 获取热点标题、URL、评分、描述等信息
    - 合并所有平台的热点数据
    ↓
Step 4: 从 HAP "账号人设" 表读取账号人设配置
    - 账号定位（positioning）
    - 目标受众（target_audience）
    - 内容方向（content_direction）
    - 内容风格（content_style）
    - 内容原则（content_principles）
    ↓
Step 5: 基于热点和账号人设分析选题
    - 筛选与账号定位和内容方向相关的热点
    - 分析每个热点的选题价值（热度、相关性、可创作性）
    - 生成 5-10 个选题建议，每个选题包含：
      - 选题标题
      - 来源平台
      - 选题角度（如何结合账号人设）
      - 预期内容方向
      - 推荐理由
      - 相关度评分（1-10分）
    - **按相关度评分排序，标注最推荐的选题**
    ↓
Step 6: 以 Markdown 表格形式展示选题建议，供用户选择
    - **必须使用 Markdown 表格格式展示**，更加直观
    - **表格结构**：
      - 最推荐选题表格（AI 相关或评分 10/10 的选题）
      - 其他推荐选题表格（评分 6-9/10 的选题）
    - **表格列**：序号、选题标题、来源平台、选题角度、推荐理由、相关度评分
    - **明确标注最推荐的选题**（如：⭐ 最推荐选题）
    - 展示所有选题建议
    - 用户选择一个或多个选题
    ↓
Step 6.5: 询问用户是否将选题加入选题库
    - **询问用户**：是否将推荐的选题加入 HAP "选题库" 表
    - **询问方式**：在展示选题建议后，询问"是否将这些选题加入选题库？"
    - 如果用户确认，将用户选择的选题保存到 HAP "选题库" 表：
      - `topic_title`: 选题标题
      - `source_platform`: 来源平台（关联热点平台关注表，使用平台记录的 rowid）
      - `topic_angle`: 选题角度
      - `recommendation_reason`: 推荐理由
      - `relevance_score`: 相关度评分
      - `source_url`: 原文链接
      - `content_preview`: 内容预览
      - `topic_status`: 选题状态（默认：待创作）
    - 如果用户不加入，跳过此步骤
    - **批量保存**：如果用户选择了多个选题，使用 `batch_create_records` 批量保存
    ↓
Step 7: 用户选择选题后，深度搜索相关资料
    - 从 HAP "API服务配置" 表读取搜索 API 配置（Tavily）
    - 基于选题标题和角度，调用搜索 API 获取深度资料
    - 结合热点新闻中的原始信息
    ↓
Step 8: 基于热点信息和搜索资料生成内容
    - 结合热点信息（原始标题、描述、URL）
    - 结合搜索到的深度资料
    - 严格遵循账号人设中的内容风格和内容原则
    - 生成符合账号定位的内容
    ↓
Step 9: 后续流程与标准内容生成流程相同
    - 生成封面标题（5-10个备选）
    - 选择话题标签（从 HAP 话题库）
    - 生成配图建议
    - 保存到本地文件（预览）
    - 与用户确认内容、标题、图片
    - 生成图片（用户确认后）
    - 同步到 HAP（用户确认后）：
      - **如果内容是基于选题库中的选题创作的**：
        - 在创建内容记录时，关联对应的选题（`related_topic` 字段）
        - 更新选题状态为"创作中"或"已创作"
        - 选题库中的 `related_content` 字段会自动关联已创作的内容（双向关联）
      - **如果内容不是基于选题创作的**：
        - 不关联选题，`related_topic` 字段留空
    - 发布到目标平台（用户确认后）
```

**热点新闻 API 使用说明：**

**API 地址：** `https://orz.ai/api/v1/dailynews`

**请求方式：** `GET`

**参数：**
- `platform`: 平台代码（必需），支持的平台代码见"热点平台关注表"说明

**请求示例：**
```
GET https://orz.ai/api/v1/dailynews/?platform=baidu
GET https://orz.ai/api/v1/dailynews/?platform=weibo
GET https://orz.ai/api/v1/dailynews/?platform=zhihu
```

**响应格式：**
```json
{
  "status": "200",
  "data": [
    {
      "title": "热点标题",
      "url": "热点链接",
      "score": "热度评分",
      "desc": "热点描述"
    }
  ],
  "msg": "success"
}
```

**配置说明：**
- 在 HAP "API服务配置" 表中添加一条记录：
  - **功能名称**：热点新闻API（标题字段）
  - **服务提供商**：orz.ai
  - **服务类型**：热点新闻（从下拉列表选择）
  - **Endpoint URL**：https://orz.ai/api/v1/dailynews（**必需填写**）
  - **用途说明**：用于获取各平台的热点新闻数据，支持每日热点内容推荐
  - **配置状态**：启用

**热点平台关注表配置：**
- 用户需要在 HAP "热点平台关注表" 中添加关注的平台
- 设置 `is_followed = 1`（勾选）表示关注此平台
- 设置 `priority`（优先级，1-10）控制获取顺序
- `platform_code` 必须与热点新闻 API 支持的平台代码一致

**选题建议展示格式（重要）：**
- **必须使用 Markdown 表格格式展示选题建议**，更加直观
- **表格结构示例**：
  ```markdown
  ## ⭐ 最推荐选题（AI 相关，强烈推荐）
  
  | 序号 | 选题标题 | 来源平台 | 选题角度 | 推荐理由 |
  |------|---------|---------|---------|---------|
  | 1 | 选题标题1 | 平台1 | AI 技术科普 | 符合账号定位... |
  
  ## 📌 其他推荐选题
  
  | 序号 | 选题标题 | 来源平台 | 选题角度 | 推荐理由 | 相关度 |
  |------|---------|---------|---------|---------|--------|
  | 1 | 选题标题2 | 平台2 | 技术趋势解读 | 符合内容方向... | 8/10 |
  ```
- **必须明确标注最推荐的选题**（如：⭐ 最推荐选题、相关度评分 10/10）
- **按相关度评分排序**，最推荐的选题放在最前面
- **每个选题包含**：标题、来源平台、选题角度、推荐理由、相关度评分
- **不要在对话中生成文件**，直接在对话中以 Markdown 表格形式展示

### 2. 平台支持

#### 小红书

**内容格式：**
- 标题：10字以内，疑问式/数字式/痛点式/反差式
- 正文：300-400字，故事化开头，结构清晰
- 话题标签：5-8个，从 HAP 话题库选取
- 图片：封面图 + 2-3张配图

**发布流程：**
1. 导航到 `https://creator.xiaohongshu.com/publish/publish?type=image_text`
2. 上传图片（使用 `setInputFiles`）
3. 填写标题
4. 填写正文（包含话题标签）
5. 点击发布

**HAP 工作表：**
- 工作表名：`内容管理`（通用表，支持多平台）
- 字段：
  - `platform_type`: 平台类型（SingleSelect: 小红书/抖音/微信公众号/视频号/其他）
  - `content_title`: 内容标题（标题字段）
  - `cover_title`: 封面标题
  - `content`: 正文内容
  - `tags`: 话题标签（空格分隔）
  - `cover_image`: 封面图（附件）
  - `other_images`: 其他配图（附件）
  - `markdown_doc`: Markdown 文档（附件）
  - `publish_status`: 发布状态（草稿/待发布/已发布/已取消）
  - `publish_time`: 发布时间
  - `note_url`: 内容链接（发布后更新，不同平台可能叫法不同）
  - `views`: 浏览量
  - `likes`: 点赞数
  - `collections`: 收藏数
  - `comments`: 评论数

#### 抖音

**内容格式：**
- 视频时长：15-60秒
- 文案：不超过50字
- 话题标签：3-5个

**发布流程：**
1. 导航到 `https://creator.douyin.com/`
2. 上传视频
3. 填写文案
4. 添加话题
5. 点击发布

#### 微信公众号

**内容格式：**
- 标题：不超过64字
- 正文：2000-5000字（HTML格式）
- 摘要：文章摘要
- 封面：封面图片

**发布流程：**
1. 导航到 `https://mp.weixin.qq.com/`
2. 点击"写新文章"
3. 填写标题、正文、摘要
4. 设置封面图
5. 点击发布

#### 视频号

**内容格式：**
- 视频时长：30秒-30分钟
- 文案：不超过1000字
- 话题：3-5个

**发布流程：**
1. 登录视频号管理后台
2. 点击"发布视频"
3. 上传视频
4. 填写文案和话题
5. 点击发布

### 3. 搜索资料（Tavily API）

#### 使用 Tavily API 搜索相关资料

**API 服务配置管理：**

搜索 API 配置统一存储在 HAP "API服务配置" 表中，按功能分类，每个功能一条记录包含所有配置字段。

**重要：配置是动态获取的，不硬编码**

**配置读取流程：**
1. **确认 MCP 连接**：先确认当前连接的 HAP 应用 MCP（通过 `get_app_info()`）
2. **查询配置**：从 HAP "API服务配置" 表查询搜索 API 配置
3. **匹配配置**：根据 `function_name`（功能名称，如"Tavily 搜索API"）或 `service_type`（服务类型：搜索API）匹配配置
4. **验证状态**：验证 `config_status`（配置状态）为"启用"
5. **读取配置**：读取该功能的所有配置字段（API Key、Base URL 等）

**Tavily API 配置示例：**
```python
# Step 1: 确认当前连接的 MCP 应用
current_app = mcp_hap-mcp-_get_app_info()
current_app_name = current_app['data']['name']

# Step 2: 动态获取工作表列表，通过别名匹配找到"API服务配置"表
# 重要：优先使用别名（alias）匹配，不要使用硬编码的 ID
worksheets = mcp_hap-mcp-_get_app_worksheets_list()
api_config_worksheet_id = None
for ws in worksheets:
    # 优先通过别名匹配，如果别名不存在则使用名称匹配
    if ws.get('alias') == 'api_service_config' or ws.get('name') == 'API服务配置':
        api_config_worksheet_id = ws['id']
        break

if not api_config_worksheet_id:
    raise Exception(f"在应用「{current_app_name}」中未找到「API服务配置」表（别名：api_service_config）")

# Step 3: 查询 Tavily 搜索 API 配置
configs = mcp_hap-mcp-_get_record_list(
    worksheet_id=api_config_worksheet_id,
    filter={
        "type": "group",
        "logic": "AND",
        "children": [
            {
                "type": "condition",
                "field": "function_name",
                "operator": "contains",
                "value": ["Tavily"]
            },
            {
                "type": "condition",
                "field": "config_status",
                "operator": "eq",
                "value": ["启用"]
            }
        ]
    }
)

# Step 4: 提取配置并调用 API
if configs and len(configs) > 0:
    config = configs[0]
    api_key = config.get('api_key')  # Tavily API Key（必需）
    endpoint_url = config.get('endpoint_url')  # Endpoint URL（必需）
    
    # 验证必需字段
    if not api_key:
        raise Exception("Tavily API Key 未配置，请在 HAP 'API服务配置' 表中填写 api_key 字段")
    if not endpoint_url:
        raise Exception("Endpoint URL 未配置，请在 HAP 'API服务配置' 表中填写 endpoint_url 字段")
    
    # 调用 Tavily API 搜索
    import requests
    response = requests.post(
        f"{endpoint_url}/search",
        headers={"Content-Type": "application/json"},
        json={
            "api_key": api_key,
            "query": topic,  # 用户输入的主题
            "search_depth": "basic",
            "max_results": 5,
            "topic": "general",
            "include_answer": False,
            "include_raw_content": False,
            "include_images": False
        }
    )
    
    search_results = response.json().get('results', [])
    # 使用搜索结果生成内容
```

**Tavily API 配置字段说明（必需字段）：**
- `function_name`: 功能名称（Text，标题字段，如："Tavily 搜索API"）
- `provider`: 服务提供商（Text，如："Tavily"）
- `service_type`: 服务类型（SingleSelect: 搜索API/图片生成/内容生成/数据分析/其他）
- `api_key`: **API Key（Text，必需）** - Tavily API Key，如：tvly-dev-xxx...
  - **何时填写**：搜索 API（Tavily、Serper 等）必须填写此字段
- `endpoint_url`: **Endpoint URL（Text，必需）** - API 基础地址，如：https://api.tavily.com
  - **何时填写**：所有 API 服务都需要填写此字段，用于指定 API 的访问地址
- `config_status`: 配置状态（SingleSelect: 启用/禁用）
- `purpose`: 用途说明（Text，如："用于搜索主题相关资料"）

**搜索流程：**
1. **读取配置**：从 HAP "API服务配置" 表读取 Tavily 搜索 API 配置
2. **调用 API**：使用配置中的 API Key 调用 Tavily API 搜索主题相关资料
3. **处理结果**：提取搜索结果中的关键信息（标题、内容、URL 等）
4. **读取账号人设**（重要：必须在生成内容之前）：从 HAP "账号人设" 表读取账号定位、内容风格、内容原则等
5. **生成内容**：将搜索结果与账号人设结合，严格遵循账号人设中的内容风格和内容原则，生成高质量内容

**搜索参数说明：**
- `query`: 搜索主题（用户输入）
- `search_depth`: 搜索深度（basic/advanced，推荐 basic）
- `max_results`: 最大结果数（推荐 5）
- `topic`: 主题类型（general/tech/business 等）
- `include_answer`: 是否包含答案摘要（False）
- `include_raw_content`: 是否包含原始内容（False）
- `include_images`: 是否包含图片（False）

**功能配置示例（HAP 表中）：**
- **功能名称**：Tavily 搜索API（标题字段）
- **服务提供商**：Tavily
- **服务类型**：搜索API（从下拉列表选择）
- **用途说明**：用于搜索主题相关资料，获取最新信息
- **API Key**：tvly-dev-xxx...（**必需填写**，Tavily API Key）
- **Endpoint URL**：https://api.tavily.com（**必需填写**，API 基础地址）
- **配置状态**：启用（从下拉列表选择）

**热点新闻 API 配置示例（HAP 表中）：**
- **功能名称**：热点新闻API（标题字段）
- **服务提供商**：orz.ai
- **服务类型**：热点新闻（从下拉列表选择）
- **用途说明**：用于获取各平台的热点新闻数据，支持每日热点内容推荐
- **Endpoint URL**：https://orz.ai/api/v1/dailynews（**必需填写**，API 基础地址）
- **配置状态**：启用（从下拉列表选择）

**重要提示：**
- `api_key` 和 `endpoint_url` 是搜索 API 的必需字段，必须填写
- `api_key` 用于 API 认证
- `endpoint_url` 用于指定 API 的访问地址，格式如：`https://api.tavily.com`
- **热点新闻 API 不需要 `api_key`**，只需要填写 `endpoint_url`

### 4. 内容生成规范

#### 账号人设配置（重要：必须先读取）

**必须从 HAP "账号人设" 表读取账号人设配置：**

**重要原则：生成内容之前，必须先从 HAP "账号人设" 表读取账号人设配置，严格遵循账号定位和内容规则。**

**强制要求：**
- **禁止使用本地文件**：绝对不允许使用 `AGENTS.md` 或其他本地文件作为账号人设来源
- **必须从 HAP 读取**：必须通过 HAP MCP 调用 `get_record_list()` 从 HAP "账号人设" 表读取
- **必须在生成内容之前执行**：如果未读取到账号人设配置，必须抛出异常，不允许继续生成内容
- **必须严格遵循**：生成内容时必须严格按照从 HAP 读取的 `content_style` 和 `content_principles` 执行

**读取流程：**
1. 确认当前连接的 MCP 应用
2. 动态获取"账号人设"表的 ID（通过别名匹配）
3. 根据 `platform_name` 或 `platform_type` 查询对应平台的账号人设
4. **读取所有必需字段**：
   - 账号定位（positioning）：了解账号的核心定位
   - 目标受众（target_audience）：了解内容面向的受众群体
   - 内容方向（content_direction）：了解内容的主要方向
   - 内容风格（content_style）：了解内容应该采用的风格（必须严格遵循）
   - 内容原则（content_principles）：了解内容创作的原则和注意事项（必须严格遵守）
   - 图片生成提示词（image_generation_prompt）：了解图片风格要求
5. **应用到内容生成**：在生成内容时，严格遵循账号人设中的内容风格和内容原则

**账号人设表字段：**
- `platform_name`: 平台名称（Text，标题字段）
- `platform_type`: 平台类型（SingleSelect: 小红书/抖音/微信公众号/视频号）
- `positioning`: **账号定位（Text，必需）** - 账号的核心定位，用于指导内容方向
- `target_audience`: **目标受众（Text，必需）** - 内容面向的受众群体，用于调整内容风格和深度
- `content_direction`: **内容方向（Text，必需）** - 内容的主要方向，用于确定内容主题和范围
- `content_style`: **内容风格（Text，必需）** - 内容应该采用的风格，必须严格遵循
  - **示例**：专业但不高冷，用通俗易懂的语言解释复杂概念。简单直白，避免专业术语堆砌，必要时用类比和例子说明。
- `content_principles`: **内容原则（Text，必需）** - 内容创作的原则和注意事项，必须严格遵守
  - **示例**：✅ 用简单语言解释复杂技术，让非技术人员也能理解；❌ 避免过度使用专业术语
- `image_generation_prompt`: **图片生成提示词（Text）** - 用于生成图片的风格提示词
  - **用途**：用于生成图片的风格提示词，可以设置图片的整体风格、色彩、构图等
  - **使用方式**：生成图片时，将此提示词与具体图片内容描述结合
  - **示例**：中文手写信息海报风格插画，纵向构图，奶油系浅色底，可爱治愈、轻松幽默的科普视觉语言

**使用示例（必须严格按照此流程执行）：**
```python
# Step 1: 确认当前连接的 HAP MCP 应用
current_app = mcp_hap-mcp-_get_app_info()
current_app_name = current_app['data']['name']
print(f"当前连接的 HAP 应用：{current_app_name}")

# Step 2: 通过别名匹配找到"账号人设"表（不要使用硬编码 ID）
worksheets = mcp_hap-mcp-_get_app_worksheets_list()
persona_worksheet_id = None
for ws in worksheets:
    # 优先通过别名匹配，如果别名不存在则使用名称匹配
    if ws.get('alias') == 'account_persona' or ws.get('name') == '账号人设':
        persona_worksheet_id = ws['id']
        break

if not persona_worksheet_id:
    raise Exception(f"在应用「{current_app_name}」中未找到「账号人设」表（别名：account_persona）。请确保 HAP 应用中存在此表。")

# Step 3: 查询小红书账号人设（重要：必须在生成内容之前读取）
personas = mcp_hap-mcp-_get_record_list(
    worksheet_id=persona_worksheet_id,  # 使用通过别名匹配获取的 ID
    filter={
        "type": "group",
        "logic": "AND",
        "children": [
            {
                "type": "condition",
                "field": "platform_type",
                "operator": "eq",
                "value": ["小红书"]
            }
        ]
    }
)

# Step 4: 验证是否读取到账号人设（强制要求）
if not personas or len(personas) == 0:
    raise Exception(f"在应用「{current_app_name}」的「账号人设」表中未找到小红书账号人设配置。请先在 HAP 中添加账号人设记录。")

persona = personas[0]

# Step 5: 读取所有账号人设字段（必需）
positioning = persona.get('positioning')  # 账号定位
target_audience = persona.get('target_audience')  # 目标受众
content_direction = persona.get('content_direction')  # 内容方向
content_style = persona.get('content_style')  # 内容风格（必须严格遵循）
content_principles = persona.get('content_principles')  # 内容原则（必须严格遵守）
image_prompt_base = persona.get('image_generation_prompt', '')  # 图片风格基础提示词

# Step 6: 验证必需字段是否存在
if not content_style:
    raise Exception(f"账号人设配置中缺少「内容风格」（content_style）字段，无法生成内容。")
if not content_principles:
    raise Exception(f"账号人设配置中缺少「内容原则」（content_principles）字段，无法生成内容。")

# Step 7: 打印账号人设信息（用于确认）
print(f"\n✅ 已从 HAP 读取账号人设配置：")
print(f"  - 账号定位：{positioning}")
print(f"  - 目标受众：{target_audience}")
print(f"  - 内容方向：{content_direction}")
print(f"  - 内容风格：{content_style[:100]}...")
print(f"  - 内容原则：{content_principles[:100]}...")

# Step 8: 根据账号人设和搜索结果生成内容
# **必须严格遵循从 HAP 读取的 content_style 和 content_principles**
# **禁止使用本地 AGENTS.md 文件或其他本地文件**

# 生成内容示例：
# 1. 根据 content_style 确定写作风格（如：通俗易懂、专业但不高冷等）
# 2. 根据 content_principles 确定内容原则（如：用简单语言解释复杂技术、避免专业术语堆砌等）
# 3. 根据 positioning 确定内容定位（如：IT公司产品经理视角）
# 4. 根据 target_audience 调整内容深度和表达方式
# 5. 根据 content_direction 确定内容主题和范围
# 6. 结合搜索结果中的资料，生成符合账号人设的内容

# 生成标题时，也要遵循从 HAP 读取的 content_style 和 positioning
# 生成配图建议时，要结合从 HAP 读取的 image_prompt_base

# 生成图片时，将从 HAP 读取的 image_prompt_base 与具体内容结合
```

#### 内容撰写要求（重要：必须遵循账号人设）

**内容生成流程：**
1. **先读取账号人设**：从 HAP "账号人设" 表读取账号定位、内容风格、内容原则等（必须在生成内容之前）
2. **结合搜索资料**：将搜索到的资料与账号人设结合
3. **严格遵循账号人设**：
   - 必须按照 `content_style`（内容风格）来撰写
   - 必须遵守 `content_principles`（内容原则）
   - 确保内容符合 `positioning`（账号定位）
   - 确保内容适合 `target_audience`（目标受众）
   - 确保内容符合 `content_direction`（内容方向）

**小红书笔记（300-400字）通用要求：**
1. **开场吸引**：故事化开头，带情感色彩（兴奋/好奇/思考），用产品经理的视角
2. **技术科普**：用简单语言解释复杂概念，避免专业术语堆砌
3. **产品视角**：分析技术对行业和用户的影响
4. **总结升华**：行动建议/思考启发

**内容生成流程（参考 wechat-article-writer skill）：**
- Step 1: 搜索资料（Tavily API）
- Step 2: 撰写文章（必须先读取账号人设）
- Step 3: 生成标题（5-10个备选，参考小红书爆款标题风格）
- Step 4: 排版优化 + 配图建议

**微信公众号文章（2000-5000字）通用要求：**
1. **标题**：吸引眼球，不超过64字
2. **摘要**：文章核心观点
3. **正文**：HTML格式，结构清晰
   - 引言
   - 主体内容（分章节）
   - 总结
4. **配图**：封面图 + 正文配图

**注意**：以上是通用要求，实际撰写时必须严格遵循账号人设中的 `content_style` 和 `content_principles`。

#### 封面标题生成（必须遵循账号人设，参考小红书爆款标题风格）

生成 5-10 个备选标题，参考小红书爆款标题特点：

**标题类型：**
- **疑问式**：引发好奇（"agentic 是什么？AI 终于能自己干活了"）
- **数字式**：具体数字更有说服力（"3分钟搞懂 agentic AI！"）
- **痛点式**：直击读者痛处（"还在手动操作？agentic AI 让你一次指令全搞定"）
- **反差式**：制造冲突（"AI 不再'等指令'！agentic 让 AI 主动工作"）
- **揭秘式**：制造悬念（"揭秘 agentic：AI 从'问答机'到'智能助手'的进化"）
- **结果式**：先展示价值（"AI 也能自主决策了！agentic 到底是什么？"）
- **对比式**：清晰展示差异（"传统 AI vs agentic AI：从被动响应到主动执行"）
- **趋势式**：强调时代感（"agentic 是什么？AI 的'数字员工'时代来了"）
- **身份标签式**：符合账号人设（"产品经理视角：agentic AI 如何改变我们的工作方式"）

**重要**：
- 标题风格必须符合账号人设中的 `content_style`（内容风格）
- 标题要符合账号人设中的 `positioning`（账号定位）和 `target_audience`（目标受众）
- 参考小红书爆款标题的特点：吸引眼球、引发好奇、强调价值、降低学习门槛
- 推荐首选标题，并说明理由

#### 话题标签选择（必须符合账号人设）

从 HAP 话题库表中选取：

**选择策略：**
1. 优先使用高热度标签（提升曝光）
2. 根据主题匹配话题类型
3. 搭配精准标签吸引目标用户
4. **确保标签符合账号人设中的 `content_direction`（内容方向）和 `target_audience`（目标受众）**

**查询方法：**
```python
# Step 1: 通过别名匹配找到"话题库"表（不要使用硬编码 ID）
worksheets = mcp_hap-mcp-_get_app_worksheets_list()
topics_worksheet_id = None
for ws in worksheets:
    # 优先通过别名匹配，如果别名不存在则使用名称匹配
    if ws.get('alias') == 'topic_library' or ws.get('name') == '话题库':
        topics_worksheet_id = ws['id']
        break

if not topics_worksheet_id:
    raise Exception(f"在应用「{current_app_name}」中未找到「话题库」表（别名：topic_library）")

# Step 2: 查询高热度话题
mcp_hap-mcp-_get_record_list(
    worksheet_id=topics_worksheet_id,  # 使用通过别名匹配获取的 ID
    filter={
        "type": "group",
        "logic": "AND",
        "children": [
            {
                "type": "condition",
                "field": "heat_level",
                "operator": "eq",
                "value": ["高热度"]
            }
        ]
    }
)

# 查询特定平台的内容（通过别名匹配获取工作表ID）
# Step 1: 通过别名匹配找到"内容管理"表（不要使用硬编码 ID）
worksheets = mcp_hap-mcp-_get_app_worksheets_list()
content_worksheet_id = None
for ws in worksheets:
    # 优先通过别名匹配，如果别名不存在则使用名称匹配
    if ws.get('alias') == 'content_management' or ws.get('name') == '内容管理':
        content_worksheet_id = ws['id']
        break

if not content_worksheet_id:
    raise Exception(f"在应用「{current_app_name}」中未找到「内容管理」表（别名：content_management）")

# Step 2: 查询小红书内容
mcp_hap-mcp-_get_record_list(
    worksheet_id=content_worksheet_id,
    filter={
        "type": "group",
        "logic": "AND",
        "children": [
            {
                "type": "condition",
                "field": "platform_type",
                "operator": "eq",
                "value": ["小红书"]
            }
        ]
    }
)
```

### 4. 图片生成

#### 支持多个图片生成 API 配置

**API 服务配置管理：**

所有 API 服务配置统一存储在 HAP "API服务配置" 表中，按功能分类，每个功能一条记录包含所有配置字段。

**重要：配置是动态获取的，不硬编码**

**多配置选择机制：**
- **支持多个图片生成 API 配置**：可以在 HAP "API服务配置" 表中配置多个图片生成 API（如 TUZI API、火山引擎即梦 API 等）
- **"是否默认"字段控制**：通过 `is_default`（是否默认）字段控制使用哪个配置
  - 如果存在标记为"默认"的配置，优先使用该配置
  - 如果没有默认配置，使用第一个启用的配置
- **配置状态控制**：只有 `config_status`（配置状态）为"启用"的配置才会被使用

**配置读取流程：**
1. **确认 MCP 连接**：先确认当前连接的 HAP 应用 MCP（通过 `get_app_info()`）
2. **查询配置**：从 HAP "API服务配置" 表查询所有图片生成类型的配置（`service_type = 图片生成` 且 `config_status = 启用`）
3. **选择配置**：
   - 优先选择 `is_default = 1`（是默认）的配置
   - 如果没有默认配置，使用第一个启用的配置
4. **读取配置**：读取该配置的所有配置字段（API Key、Endpoint URL、Access Key ID 等）

**配置选择示例：**
```python
# Step 1: 确认当前连接的 MCP 应用
current_app = mcp_hap-mcp-_get_app_info()
current_app_name = current_app['data']['name']

# Step 2: 通过别名匹配找到"API服务配置"表
worksheets = mcp_hap-mcp-_get_app_worksheets_list()
api_config_worksheet_id = None
for ws in worksheets:
    if ws.get('alias') == 'api_service_config' or ws.get('name') == 'API服务配置' or ws.get('name') == '密钥管理':
        api_config_worksheet_id = ws['id']
        break

if not api_config_worksheet_id:
    raise Exception(f"在应用「{current_app_name}」中未找到「API服务配置」表（别名：api_service_config）")

# Step 3: 查询所有图片生成 API 配置（启用状态）
configs = mcp_hap-mcp-_get_record_list(
    worksheet_id=api_config_worksheet_id,
    filter={
        "type": "group",
        "logic": "AND",
        "children": [
            {
                "type": "condition",
                "field": "service_type",
                "operator": "eq",
                "value": ["图片生成"]
            },
            {
                "type": "condition",
                "field": "config_status",
                "operator": "eq",
                "value": ["启用"]
            }
        ]
    }
)

# Step 4: 选择配置（优先使用默认配置）
if configs and len(configs) > 0:
    # 优先选择标记为"默认"的配置
    default_config = None
    for config in configs:
        if config.get('is_default') == 1:
            default_config = config
            break
    
    # 如果没有默认配置，使用第一个启用的配置
    if not default_config:
        default_config = configs[0]
    
    config = default_config
    
    # 根据服务提供商读取对应的配置字段
    provider = config.get('provider', '').upper()
    
    if 'TUZI' in provider:
        # TUZI API (OpenAI 兼容接口)
        api_key = config.get('api_key')  # 必需
        endpoint_url = config.get('endpoint_url', 'https://api.tu-zi.com/v1')  # 必需
        # 使用 OpenAI SDK 调用
    elif '火山引擎' in provider or '即梦' in config.get('function_name', ''):
        # 火山引擎即梦 API
        access_key_id = config.get('access_key_id')  # 必需
        secret_access_key = config.get('secret_access_key')  # 必需
        region = config.get('region', 'cn-beijing')
        service = config.get('service', 'cv')
        api_version = config.get('api_version', 'jimeng_t2i_v31')
        sdk_name = config.get('sdk_name', 'volcenginesdkcv20240606')
        # 使用火山引擎 SDK 调用
```

**生成流程：**
1. **确认 MCP**：确认当前连接的 HAP 应用 MCP（通过用户提供或指定）
2. **读取账号人设**：从 HAP "账号人设" 表读取对应平台的账号人设配置
3. **获取图片风格**：从账号人设中提取 `image_generation_prompt`（图片生成提示词）
4. **动态读取配置**：从 HAP "API服务配置" 表查询所有图片生成类型的配置
5. **选择配置**：
   - 优先选择 `is_default = 1`（是默认）的配置
   - 如果没有默认配置，使用第一个启用的配置
6. **提取密钥**：根据服务提供商提取对应的密钥字段
   - TUZI API：`api_key`、`endpoint_url`
   - 火山引擎即梦：`access_key_id`、`secret_access_key`、`region`、`service` 等
7. **生成提示词**：将账号人设中的图片风格提示词与具体配图建议结合，生成完整的图片生成提示词
   - 格式：`{image_generation_prompt}，{具体配图内容描述}`
   - 示例：`手绘风格插画，清新活泼的卡通插画风格，{具体图片内容}`
8. **调用 API 生成图片**：
   - **TUZI API**：使用 OpenAI SDK，支持多个模型（gemini-3-pro-image-preview、dall-e-3、dall-e-2）
     - **必须使用 `response_format="url"` 参数**：确保 API 返回 URL 格式而非 base64
     - **请求参数**：`model`、`prompt`、`n=1`、`response_format="url"`、`size="{width}x{height}"`
   - **火山引擎即梦**：使用火山引擎 SDK
   - **并行生成**：使用线程池并行生成多张图片（最多3个并发），大幅提升生成速度
   - **自动跳过已存在**：检查本地文件是否存在，如果已存在则跳过生成，节省时间和成本
9. **处理 API 响应**：
   - **优先处理 URL**：如果 API 返回 HTTP/HTTPS URL，直接使用
   - **处理 base64 数据**：如果 API 返回 base64 数据（data URI 或 base64 字符串），自动解码并保存为图片文件
   - **错误处理**：如果 API 返回无效数据，记录错误并继续生成其他图片
10. **保存图片**：
    - **保存图片 URL**：保存图片 URL 到 `配图/image_urls.json`（只保存 URL，不保存 base64）
    - **自动下载图片**：从 URL 自动下载图片文件到 `配图/{图片名称}.png`，方便本地查看和展示
    - **图片文件命名**：封面图.png、对比图.png、流程图.png、应用场景图.png 等
    - **下载失败处理**：如果下载失败，保留 URL 并记录警告，不影响后续流程
11. **上传到 HAP**：
    - **小红书笔记**：只上传图片 URL（封面图和其他配图）到 HAP 附件字段，不上传 Markdown 文档
    - **其他平台**：根据平台需求上传图片和文档
    - **上传时使用 URL**：上传到 HAP 时使用图片 URL，不需要 base64 数据

**图片格式要求（小红书）：**
- **尺寸**：768x1024（小红书 3:4 格式，竖屏）
- **风格**：手绘风格插画（清新活泼的卡通插画风格）
- **内容要求**：图片内容必须与正文内容强相关，表达核心含义（流程、介绍、对比等）

**图片类型（必须遵循账号人设）：**
- **封面图**：结合账号人设的图片风格提示词 + 具体内容描述 + **封面标题文字**
  - 封面图必须包含封面标题文字，使用粗体装饰性字体，带笔画和渐变效果
  - 标题文字要醒目，占据封面重要位置，符合小红书封面图设计规范
- **对比图**：结合账号人设的图片风格提示词 + 对比内容描述（与内容强相关）
- **流程图**：结合账号人设的图片风格提示词 + 流程内容描述（与内容强相关）
- **应用场景图**：结合账号人设的图片风格提示词 + 场景内容描述（与内容强相关）

**手绘风格插画特点（参考）：**
- **整体风格**：清新活泼的卡通插画风格，充满正能量和活力
- **线条**：粗黑描边，手绘质感，流畅自然
- **色彩**：明亮饱和的色彩 - 橙色、黄色、蓝色、绿色、红色等温暖色调，和谐配色
- **渲染**：平面风格为主，搭配简单的渐变和高光，增加立体感
- **字体**：粗体装饰性字体，带笔画和渐变效果
- **氛围**：积极向上、充满活力、科技感、温馨可爱
- **设计哲学**：简洁明快、视觉冲击力强、适合数字媒体传播

**重要**：
- 配图建议必须结合账号人设中的 `image_generation_prompt`（图片生成提示词）来生成
- 图片内容必须与正文内容强相关，表达核心含义（流程、介绍、对比等）
- 封面图必须包含封面标题文字
- 图片格式必须符合平台要求（小红书：768x1024，3:4格式）

**图片提示词生成规则：**
1. 从 HAP "账号人设" 表读取 `image_generation_prompt`（图片风格基础提示词）
2. 将风格提示词与具体图片内容描述结合
3. **格式**：`{image_generation_prompt}，{具体图片内容描述，与内容强相关}`
4. **封面图特殊要求**：封面图必须包含封面标题文字
   - 格式：`{image_generation_prompt}，封面图内容: {具体内容描述}，标题文字: "{封面标题}"，使用粗体装饰性字体，带笔画和渐变效果`
5. **示例（封面图）**：
   - 账号人设中的风格：`创建一个手绘风格的插画作品,具有以下特点: 整体风格: 清新活泼的卡通插画风格,充满正能量和活力...`
   - 具体图片内容：`展示"agentic 是什么"的核心概念,中心是一个可爱的大脑图标,大脑周围有多个小机器人或执行箭头,表示自主规划和执行能力`
   - 封面标题：`3分钟搞懂 agentic AI！`
   - 最终提示词：`{image_generation_prompt}，封面图内容: 展示"agentic 是什么"的核心概念,中心是一个可爱的大脑图标,大脑周围有多个小机器人或执行箭头,表示自主规划和执行能力。上方有粗体装饰性标题文字"3分钟搞懂 agentic AI！",使用粗体装饰性字体,带笔画和渐变效果,增强视觉冲击力。标题文字要醒目,占据封面重要位置,符合小红书封面图设计规范。`
6. **示例（对比图）**：
   - 账号人设中的风格：`创建一个手绘风格的插画作品...`
   - 具体图片内容：`左右分屏对比,左侧展示传统AI - 一个简单的问答机形象,只能被动回答问题,用问号表示。右侧展示agentic AI - 一个智能助手形象,正在自主规划任务、执行操作,用执行箭头和任务卡片表示。中间用粗箭头连接,表示从"被动响应"到"主动执行"的转变。整体清晰易懂,色彩对比鲜明。`
   - 最终提示词：`{image_generation_prompt}，{具体图片内容描述}`

### 5. HAP 数据管理

#### 工作表结构

**内容管理表（通用表，支持多平台）：**
- `platform_type`: 平台类型（SingleSelect: 小红书/抖音/微信公众号/视频号/其他）
- `content_title`: 内容标题（Text，标题字段）
- `cover_title`: 封面标题（Text）
- `content`: 正文内容（Text）
- `tags`: 话题标签（Text）
- `cover_image`: 封面图（Attachment）
- `other_images`: 其他配图（Attachment）
- `markdown_doc`: Markdown 文档（Attachment，**小红书笔记不使用此字段**）
- `related_topic`: 关联选题（Relation，关联选题库表，单选，**双向关联**）
- `publish_status`: 发布状态（SingleSelect: 草稿/待发布/已发布/已取消）
- `publish_time`: 发布时间（DateTime）
- `note_url`: 内容链接（Text，不同平台可能叫法不同）
- `views`: 浏览量（Number）
- `likes`: 点赞数（Number）
- `collections`: 收藏数（Number）
- `comments`: 评论数（Number）

**重要说明：**
- **小红书笔记不同步 Markdown 文档**：同步小红书笔记到 HAP 时，只上传图片（封面图和其他配图），不上传 Markdown 文档
- `markdown_doc` 字段仅用于其他平台（如微信公众号），小红书笔记不使用此字段
- **双向关联选题库**：
  - 如果内容是基于选题库中的选题创作的，需要在内容记录中关联对应的选题
  - 如果内容不是基于选题创作的，可以不关联
  - 选题库中的 `related_content` 字段会自动关联已创作的内容

**设计说明：**
- 使用统一的"内容管理"表管理所有平台的内容
- 通过 `platform_type` 字段区分不同平台
- 不同平台共享通用字段，特殊需求可通过备注或扩展字段处理

**话题标签库表：**
- `topic_name`: 话题名称（Text）
- `topic_type`: 话题类型（SingleSelect）
- `heat_level`: 热度等级（SingleSelect: 高热度/中热度/低热度）
- `description`: 说明（Text）
- `last_updated`: 最后更新（DateTime）

**选题库表：**
- `topic_title`: 选题标题（Text，标题字段）
- `source_platform`: 来源平台（Relation，关联热点平台关注表，单选）
- `topic_angle`: 选题角度（Text，如何结合账号人设）
- `recommendation_reason`: 推荐理由（Text）
- `relevance_score`: 相关度评分（Number，1-10分）
- `source_url`: 原文链接（Text）
- `content_preview`: 内容预览（Text，多行文本）
- `topic_status`: 选题状态（SingleSelect: 待创作/创作中/已创作/已取消）
- `related_content`: 关联内容（Relation，关联内容管理表，多选，**双向关联**）
- `notes`: 备注（Text，多行文本）

**设计说明：**
- 选题库用于存储推荐的选题，方便后续管理和创作
- 关联热点平台关注表，可以追溯选题来源
- **双向关联内容管理表**：
  - 选题库中的 `related_content` 字段可以关联多个已创作的内容
  - 内容管理表中的 `related_topic` 字段可以关联对应的选题
  - 如果内容是基于选题创作的，需要在创建内容时关联选题
  - 如果内容不是基于选题创作的，可以不关联
- 选题状态用于跟踪选题的创作进度

**账号人设表：**
- `platform_name`: 平台名称（Text，标题字段）
- `platform_type`: 平台类型（SingleSelect: 小红书/抖音/微信公众号/视频号）
- `positioning`: 账号定位（Text）
- `target_audience`: 目标受众（Text）
- `content_direction`: 内容方向（Text）
- `content_style`: 内容风格（Text）
- `content_principles`: 内容原则（Text）
- `image_generation_prompt`: 图片生成提示词（Text）
  - **用途**：用于生成图片的风格提示词，可以设置图片的整体风格、色彩、构图等
  - **使用方式**：生成图片时，将此提示词与具体图片内容描述结合
  - **示例**：简洁科技风格，蓝紫色渐变背景，现代扁平设计，高质量，专业感

**热点平台关注表：**
- `platform_name`: 平台名称（Text，标题字段，如："百度热搜"、"微博热搜"）
- `platform_code`: 平台代码（Text，如："baidu"、"weibo"，对应热点新闻 API 的平台代码）
- `platform_type`: 平台类型（SingleSelect: 综合新闻/科技/社交媒体/财经/技术社区/其他）
- `is_followed`: 是否关注（Checkbox）- 用户是否关注此平台的热点
- `priority`: 优先级（Number，1-10，数字越大优先级越高）
- `description`: 平台说明（Text，描述平台特点和内容类型）
- `last_fetch_time`: 最后获取时间（DateTime，记录最后一次获取该平台热点的时间）

**支持的平台代码（对应热点新闻 API）：**
- `baidu`: 百度热搜（社会热点、娱乐、事件）
- `sspai`: 少数派（科技、数码、生活方式）
- `weibo`: 微博热搜（社交媒体热点、娱乐、事件）
- `zhihu`: 知乎热榜（问答、深度内容、社会热点）
- `tskr`: 36氪（科技创业、商业资讯）
- `ftpojie`: 吾爱破解（技术、软件、安全）
- `bilibili`: 哔哩哔哩（视频、动漫、游戏、生活）
- `douban`: 豆瓣（书影音、文化、讨论）
- `hupu`: 虎扑（体育、游戏、数码）
- `tieba`: 百度贴吧（兴趣社区、话题讨论）
- `juejin`: 掘金（编程、技术文章）
- `douyin`: 抖音（短视频热点、娱乐）
- `vtex`: V2EX（技术、编程、创意）
- `jinritoutiao`: 今日头条（新闻、热点事件）
- `stackoverflow`: Stack Overflow（编程问答、技术讨论）
- `github`: GitHub Trending（开源项目、编程语言）
- `hackernews`: Hacker News（科技新闻、创业、编程）
- `sina_finance`: 新浪财经（财经新闻、股市资讯）
- `eastmoney`: 东方财富（财经资讯、投资理财）
- `xueqiu`: 雪球（股票投资、财经社区）
- `cls`: 财联社（财经快讯、市场动态）
- `tenxunwang`: 腾讯网（综合新闻、娱乐、科技）

**API服务配置表：**
- `function_name`: 功能名称（Text，标题字段，如："Tavily 搜索API"、"TUZI 图片生成"、"即梦图片生成"、"热点新闻API"）
- `provider`: 服务提供商（Text，如："Tavily"、"TUZI"、"火山引擎"、"orz.ai"）
- `service_type`: 服务类型（SingleSelect: 搜索API/图片生成/内容生成/数据分析/热点新闻/其他）
- `purpose`: 用途说明（Text，如："用于搜索主题相关资料"、"用于生成图片"、"用于获取热点新闻"）
- `is_default`: **是否默认（Checkbox）** - 用于控制使用哪个图片生成 API 配置
  - **用途**：当存在多个图片生成 API 配置时，优先使用标记为"默认"的配置
  - **使用方式**：勾选表示默认使用此配置，不勾选表示非默认配置
  - **选择逻辑**：优先选择 `is_default = 1`（是默认）的配置，如果没有默认配置则使用第一个启用的配置
- `endpoint_url`: **Endpoint URL（Text，必需）** - API 基础地址
  - **热点新闻 API**：`https://orz.ai/api/v1/dailynews`

**密钥字段（用户可填写）：**
- `api_key`: **API Key（Text，必需）** - 用于 API 认证
  - **何时填写**：
    - **搜索 API**（Tavily、Serper 等）：**必须填写**
    - OpenAI、Anthropic、Midjourney 等使用 API Key 认证的服务：**必须填写**
- `endpoint_url`: **Endpoint URL（Text，必需）** - API 基础地址
  - **何时填写**：**所有 API 服务都必须填写**，用于指定 API 的访问地址
  - **格式示例**：
    - Tavily: `https://api.tavily.com`
    - OpenAI: `https://api.openai.com/v1`
    - 自定义代理: `https://proxy.example.com`
- `access_key_id`: Access Key ID（Text）
  - **何时填写**：火山引擎、阿里云、腾讯云等使用 Access Key 认证的服务需要填写
- `secret_access_key`: Secret Access Key（Text）
  - **何时填写**：与 Access Key ID 配对使用，火山引擎、阿里云、腾讯云等需要填写
- `api_secret`: API Secret（Text）
  - **何时填写**：与 API Key 配对使用，部分服务需要填写
- `token`: Token（Text）
  - **何时填写**：GitHub、GitLab、JWT Token 认证的服务需要填写
- `app_id`: App ID（Text）
  - **何时填写**：微信、企业微信、钉钉等使用 App ID 认证的服务需要填写
- `app_secret`: App Secret（Text）
  - **何时填写**：与 App ID 配对使用，微信、企业微信、钉钉等需要填写

**配置字段：**
- `endpoint_url`: **Endpoint URL（Text，必需）** - API 基础地址
  - **何时填写**：**所有 API 服务都必须填写**
  - **格式示例**：
    - Tavily 搜索 API: `https://api.tavily.com`
    - OpenAI API: `https://api.openai.com/v1`
    - 火山引擎即梦: `https://ark.cn-beijing.volces.com/api/v3`
    - 自定义代理: `https://proxy.example.com`
- `region`: Region（Text）
  - **何时填写**：AWS、阿里云、腾讯云、火山引擎等需要指定区域的服务需要填写（如：cn-beijing、us-east-1）
- `service`: Service（Text）
  - **何时填写**：火山引擎等需要指定服务名称的需要填写（如：cv、ocr）
- `api_version`: API版本（Text）
  - **何时填写**：需要指定 API 版本的服务需要填写（如：jimeng_t2i_v31、v1、v2）
- `sdk_name`: SDK名称（Text）
  - **何时填写**：使用 Python SDK 时需要填写 SDK 包名（如：volcenginesdkcv20240606、openai）
- `extra_config`: 其他配置（Text）
  - **何时填写**：需要额外配置参数时填写，JSON 格式（如：{"timeout": 30, "max_retries": 3}）
- `config_status`: 配置状态（SingleSelect: 启用/禁用）
- `notes`: 备注（Text）

**使用说明：**
- **所有 API 服务都必须填写 `endpoint_url`**（API 基础地址）
- 根据不同的 API 服务类型，填写对应的密钥字段：
  - **Tavily 搜索API**：**必须填写** `api_key` 和 `endpoint_url`
  - **火山引擎即梦**：使用 `access_key_id`、`secret_access_key` 和 `endpoint_url`
  - **OpenAI/Anthropic**：**必须填写** `api_key` 和 `endpoint_url`
  - **微信/企业微信**：使用 `app_id`、`app_secret` 和 `endpoint_url`
- 所有密钥字段均为可见，用户可以直接在 HAP 中填写和编辑
- `endpoint_url` 格式：完整的 API 基础地址，如 `https://api.tavily.com` 或 `https://api.openai.com/v1`

**功能配置示例：**

1. **Tavily 搜索API**：用于搜索主题相关资料
   - 服务提供商：Tavily
   - 服务类型：搜索API（从下拉列表选择）
   - **API Key**：tvly-dev-xxx...（**必需填写**，Tavily API Key）
   - **Endpoint URL**：https://api.tavily.com（**必需填写**，API 基础地址）
   - 用途说明：在生成内容前搜索最新资料，提升内容质量
   - 配置状态：启用（从下拉列表选择）

2. **TUZI 图片生成**：用于生成图片（OpenAI 兼容接口）
   - 服务提供商：TUZI
   - 服务类型：图片生成（从下拉列表选择）
   - **API Key**：sk-xxx...（**必需填写**，TUZI API Key）
   - **Endpoint URL**：https://api.tu-zi.com/v1（**必需填写**，API 基础地址）
   - **是否默认**：是（复选框，勾选表示默认使用此配置）
   - 配置状态：启用（从下拉列表选择）
   - 备注：使用 OpenAI 兼容接口，支持多个模型（gemini-3-pro-image-preview、dall-e-3、dall-e-2）

3. **即梦图片生成**：用于生成图片（文生图3.1）
   - 服务提供商：火山引擎
   - 服务类型：图片生成（从下拉列表选择）
   - **Endpoint URL**：https://ark.cn-beijing.volces.com/api/v3（可选，API 基础地址）
   - Access Key ID：用于 API 认证（用户填写）
   - Secret Access Key：用于 API 签名（用户填写）
   - Region：cn-beijing（用户填写）
   - Service：cv（用户填写）
   - API版本：jimeng_t2i_v31（用户填写）
   - SDK名称：volcenginesdkcv20240606（用户填写）
   - **是否默认**：否（复选框，不勾选表示非默认配置）
   - 配置状态：启用（从下拉列表选择）

**重要：**
- 所有配置信息都由用户在 HAP "API服务配置" 表中填写
- Skill 只负责从表中读取，不包含任何默认值或硬编码配置
- 用户需要根据实际使用的 API 服务填写对应的配置字段

#### 数据同步流程

```
1. 搜索资料（Tavily API）→ 获取最新信息
2. 生成内容 → 保存到本地文件（预览，按笔记目录结构：`内容/{平台}/{笔记标题}/{笔记标题}.md`）
3. 与用户确认内容、标题、图片
4. 用户确认后生成图片 → 保存到笔记目录的配图文件夹（`内容/{平台}/{笔记标题}/配图/`）
5. 与用户确认是否发布和同步
6. 用户确认后同步到 HAP：
   - **小红书笔记**：只上传图片 URL（封面图和其他配图），不上传 Markdown 文档
   - **其他平台**：根据平台需求上传图片和文档
7. 用户确认后发布 → 使用 Playwright 发布到目标平台
8. 发布成功 → 更新发布状态和笔记链接

目录结构说明：
- `内容/`：根目录
- `内容/{平台}/`：平台目录（小红书/抖音/微信公众号/视频号）
- `内容/{平台}/{笔记标题}/`：笔记目录，使用封面标题作为目录名
- `内容/{平台}/{笔记标题}/{笔记标题}.md`：Markdown 文档（仅本地保存，小红书不同步到 HAP）
- `内容/{平台}/{笔记标题}/配图/`：配图文件夹

重要说明：
- **小红书笔记的 Markdown 文档不同步到 HAP**，只同步图片 URL
- Markdown 文档仅保存在本地，用于预览和编辑
- 图片生成后：
  1. 保存图片 URL 到 `配图/image_urls.json`
  2. **下载图片到本地**：保存图片文件到 `配图/{图片名称}.png`（如：封面图.png、对比图.png），方便本地查看和展示
  3. 通过 MCP 上传 URL 到 HAP（上传时使用 URL，不需要 base64）
```

### 6. 自动化发布

#### 使用 Playwright MCP

**发布前准备：**
1. 确认用户已登录目标平台
2. 检查内容完整性（标题、正文、图片、标签）
3. 验证 HAP 数据已同步

**发布流程（小红书示例）：**
```javascript
// 1. 导航到发布页面
await page.goto('https://creator.xiaohongshu.com/publish/publish?type=image_text');

// 2. 上传图片
const fileInput = await page.locator('input[type="file"]').first();
await fileInput.setInputFiles(imageFiles);

// 3. 填写标题
await page.getByRole('textbox', { name: '填写标题会有更多赞哦～' }).fill(title);

// 4. 填写正文（包含话题标签）
await page.getByRole('textbox').nth(1).fill(content + '\n\n' + tags);

// 5. 点击发布
await page.getByRole('button', { name: '发布' }).click();

// 6. 等待发布成功，获取笔记链接
// 7. 更新 HAP 记录：发布状态、发布时间、笔记链接
```

**发布后处理：**
1. 获取发布成功的内容链接
2. 更新 HAP "内容管理" 表记录：
   - `platform_type`: 目标平台（小红书/抖音/微信公众号/视频号）
   - `publish_status`: 已发布
   - `publish_time`: 当前时间
   - `note_url`: 内容链接

## 使用示例

### 示例 1: 生成并发布小红书笔记

```
用户：帮我生成一篇关于 "Skills 科普介绍" 的小红书笔记并发布

执行流程：
1. **确认 MCP**：确认当前连接的 HAP 应用 MCP（通过用户提供或指定）
2. **读取搜索配置**：从 HAP "API服务配置" 表读取 Tavily 搜索 API 配置
3. **搜索资料**：调用 Tavily API 搜索主题相关资料（获取最新 5 条结果）
4. **【强制要求】读取账号人设**（必须在生成内容之前执行）：从 HAP "账号人设" 表读取账号人设配置
   - **禁止使用本地文件**：绝对不允许使用 `AGENTS.md` 或其他本地文件
   - **必须调用 HAP MCP**：必须通过 MCP 调用 `get_record_list()` 从 HAP "账号人设" 表读取
   - **读取所有必需字段**：
     - **账号定位**（positioning）：了解账号的核心定位
     - **目标受众**（target_audience）：了解内容面向的受众群体
     - **内容方向**（content_direction）：了解内容的主要方向
     - **内容风格**（content_style）：了解内容应该采用的风格（必须严格遵循）
     - **内容原则**（content_principles）：了解内容创作的原则和注意事项（必须严格遵守）
     - **图片生成提示词**（image_generation_prompt）：了解图片风格要求
   - **验证要求**：如果未找到账号人设配置，必须抛出异常，不允许继续生成内容
5. **撰写内容**：根据搜索结果和从 HAP 读取的账号人设撰写内容
   - **严格遵循账号人设**：必须严格按照从 HAP 读取的 `content_style` 和 `content_principles` 来撰写
   - **禁止使用本地人设**：不允许参考或使用本地 `AGENTS.md` 文件中的内容
   - **结合搜索资料**：将搜索到的资料与从 HAP 读取的账号人设结合，生成符合定位的内容
   - **符合目标受众**：确保内容适合目标受众阅读
6. **生成封面标题**：根据账号人设的内容风格生成 5-10 个封面标题
   - 标题风格必须符合账号人设的内容风格
   - 标题要符合账号定位和目标受众
7. **选择话题标签**：从 HAP 话题库选择 5-8 个话题标签（动态查询）
   - 根据内容主题和账号人设的内容方向选择
8. **生成配图建议**：结合账号人设的图片生成提示词风格，生成配图建议
9. **保存预览**：保存到本地文件（按笔记目录结构：`内容/小红书/{笔记标题}/{笔记标题}.md`）
10. **与用户确认**：与用户确认内容、标题、图片
11. **生成图片**（用户确认后）：从 HAP "账号人设" 表读取图片生成提示词，从 HAP "API服务配置" 表读取图片生成配置，生成图片
12. **与用户确认发布**：与用户确认是否直接发布至小红书
13. **与用户确认同步**：与用户确认是否同步到 HAP，确认后才上传
14. **同步 HAP**（用户确认后）：同步到 HAP "内容管理" 表（platform_type = 小红书）
    - **只上传图片**：上传封面图和其他配图的 URL 到 HAP
    - **不上传 Markdown 文档**：小红书笔记的 Markdown 文档不同步到 HAP
15. **发布内容**（用户确认后）：使用 Playwright 发布到小红书
16. **更新状态**：更新 HAP 发布状态和内容链接
```

### 示例 2: 批量生成内容

```
用户：帮我生成一周的小红书笔记（7篇），主题如下：
1. Claude Code 新功能
2. AI 工具推荐
3. 大模型应用场景
...

执行流程：
1. **确认 MCP**：确认当前连接的 HAP 应用 MCP
2. **批量生成**：对每个主题重复上述流程
3. **动态读取配置**：每次生成图片时从 HAP "API服务配置" 表动态读取配置
4. **批量保存**：批量生成并保存到 HAP "内容管理" 表（platform_type = 小红书）
```

### 示例 3: 多平台发布

```
用户：将这篇笔记发布到小红书和微信公众号

执行流程：
1. **确认 MCP**：确认当前连接的 HAP 应用 MCP
2. **读取内容**：从 HAP "内容管理" 表读取内容（platform_type = 小红书）
3. **动态获取工作表**：动态获取"内容管理"表的 ID 和字段结构
4. **适配格式**：适配不同平台的格式要求：
   - 小红书：300-400字，5-8个话题标签
   - 微信公众号：2000-5000字，HTML格式
5. **发布内容**：分别发布到两个平台
6. **更新 HAP**：在 HAP "内容管理" 表中创建新记录（platform_type = 微信公众号），或更新现有记录的发布状态
```

## 技术实现

### 依赖工具

1. **Tavily API**（配置存储在 HAP）: 搜索相关资料，获取最新信息
2. **wechat-article-writer skill**: 内容生成
3. **HAP MCP**（用户提供）: 数据管理，用于存储内容、配置、话题库等
4. **Playwright MCP**: 自动化发布到各平台
5. **第三方 API**（配置存储在 HAP）: 图片生成、内容生成等 API 服务

### MCP 配置要求

**用户需要提供：**
- HAP 应用的 MCP 配置（包含 Appkey 和 Sign）
- 或明确指定使用哪个已配置的 MCP

**Skill 会自动：**
- 识别当前连接的 MCP 应用
- 动态获取工作表列表和结构
- 从"API服务配置"表读取密钥和配置
- 根据平台类型筛选内容记录

### 文件结构

```
social-media-operation/
├── AGENTS.md                    # 账号人设配置（可选，本地参考文件）
├── 笔记生成工作流.md            # 工作流说明
├── 内容/                        # 内容根目录
│   └── 小红书/                  # 平台分类（小红书/抖音/微信公众号/视频号）
│       └── {笔记标题}/          # 每个笔记一个目录，使用封面标题作为目录名
│           ├── {笔记标题}.md    # Markdown 文档（使用笔记标题命名）
│           └── 配图/            # 配图目录
│               ├── 封面图.png
│               ├── 架构图.png
│               └── 应用场景图.png
├── 话题库/                      # 话题标签库（可选，本地参考文件）
│   └── {类型}.md
└── README.md                    # 项目说明

目录结构说明：
- 内容/：根目录，包含所有平台的内容
- 小红书/：平台目录，展示该平台的所有笔记标题（目录名）
- {笔记标题}/：笔记目录，使用封面标题作为目录名，更清晰直观
- {笔记标题}.md：Markdown 文档，使用笔记标题命名
- 配图/：配图文件夹，包含该笔记的所有配图

示例：
内容/
  └── 小红书/
      └── MCP 是什么？/           # 笔记标题作为目录名
          ├── MCP科普介绍.md      # Markdown 文档
          └── 配图/
              ├── 封面图.png
              ├── 架构图.png
              └── 应用场景图.png

注意：
- 账号人设和话题库数据统一存储在 HAP 中
- 本地文件仅作为参考，实际使用时从 HAP 表读取
- 内容按笔记目录结构组织，每个笔记包含 md 文档和配图
- 目录名使用笔记标题，更清晰直观
```

### HAP 应用配置

**重要：应用名称和 MCP 配置由用户提供，不硬编码**

**通用工作表结构（用户需要在 HAP 中创建）：**
1. **内容管理**（通用表，通过 platform_type 字段区分平台：小红书/抖音/微信公众号/视频号等）
2. **话题标签库**（存储各平台的话题标签）
3. **账号人设**（存储不同平台的账号人设配置）
4. **API服务配置**（按功能分类，每个功能一条记录包含所有配置字段，包括密钥）
5. **热点平台关注表**（存储用户关注的热点平台，用于每日热点内容推荐）
6. **选题库**（存储推荐的选题，关联热点平台关注表和内容管理表）
7. **社交媒体数据**（可选，存储运营数据）

**工作表创建：**
- 用户需要在 HAP 应用中创建上述工作表
- **创建工作表时，建议设置别名（alias），便于后续查询**
- 或用户提供已存在的应用 MCP，Skill 会自动识别工作表结构
- Skill 会通过 `get_app_worksheets_list()` 动态获取工作表列表
- **查询时优先通过别名（alias）匹配，如果别名不存在则使用名称（name）匹配**
- **绝对不使用硬编码的工作表 ID**

## 注意事项

### MCP 和配置管理

1. **MCP 配置由用户提供**：
   - Skill 不包含任何硬编码的 MCP 配置
   - 用户需要提供 HAP 应用的 MCP 配置信息
   - 或明确指定使用哪个已配置的 MCP

2. **MCP 应用确认**：
   - 执行 HAP 操作前，必须先调用 `get_app_info()` 确认当前连接的 MCP 应用
   - 如果用户提供了 MCP 配置，需要对比确认是否匹配
   - 不匹配时需要与用户确认

  3. **动态读取配置**：
     - 所有 API 密钥和配置都存储在 HAP "API服务配置" 表中
     - 使用时必须从表中动态读取，**绝对不要在代码中硬编码**
     - 通过 `get_record_list()` 查询配置，根据功能名称或服务类型匹配

  4. **工作表动态识别（重要）**：
     - 通过 `get_app_worksheets_list()` 动态获取工作表列表
     - **优先通过别名（alias）匹配工作表，如果别名不存在则使用名称（name）匹配**
     - **绝对不要使用硬编码的工作表 ID**
     - **所有查询操作都必须先通过别名或名称匹配获取工作表 ID，然后再使用该 ID 进行查询**

### 内容生成

**账号人设读取检查清单（必须严格执行）：**
1. ✅ **确认 MCP 连接**：执行任何操作前，必须先调用 `get_app_info()` 确认当前连接的 HAP MCP 应用
2. ✅ **动态获取工作表**：通过 `get_app_worksheets_list()` 动态获取工作表列表，通过别名 `account_persona` 或名称 `账号人设` 匹配
3. ✅ **查询账号人设**：使用 `get_record_list()` 根据 `platform_type` 查询对应平台的账号人设记录
4. ✅ **验证必需字段**：检查是否读取到 `content_style` 和 `content_principles` 字段，如果缺失则抛出异常
5. ✅ **禁止使用本地文件**：绝对不允许使用 `AGENTS.md` 或其他本地文件作为账号人设来源
6. ✅ **严格遵循人设**：生成内容时必须严格按照从 HAP 读取的 `content_style` 和 `content_principles` 执行

**其他注意事项：**
5. **内容预览**：生成内容后先保存到本地文件，用户确认后再同步到 HAP
6. **图片生成**：图片生成可能失败（SSL 错误），需要重试或手动制作
7. **发布登录**：发布前需要用户先登录目标平台
8. **字数控制**：不同平台的字数要求不同，需要适配
9. **话题标签**：必须从 HAP 话题库中选取，不要自己编造
10. **账号人设**：**必须从 HAP "账号人设" 表中读取，禁止使用本地文件**，包括图片生成提示词
11. **图片风格**：生成图片时，将从 HAP 读取的账号人设中的 `image_generation_prompt` 与具体配图建议结合

## 最佳实践

### 通用性设计

1. **MCP 配置**：
   - 永远不硬编码 MCP 配置
   - 始终从用户提供的 MCP 或指定的 MCP 读取配置
   - 执行操作前先确认当前连接的 MCP 应用

2. **配置管理**：
   - 所有密钥和配置存储在 HAP "API服务配置" 表中
   - 使用时动态读取，不假设任何默认值
   - 用户需要在 HAP 中填写所有必要的配置信息

3. **工作表识别（重要）**：
   - 动态获取工作表列表
   - **优先通过别名（alias）匹配工作表，如果别名不存在则使用名称（name）匹配**
   - **绝对不要使用硬编码的工作表 ID**
   - **所有查询操作都必须先通过别名或名称匹配获取工作表 ID，然后再使用该 ID 进行查询**
   - 动态获取字段结构，通过名称或别名匹配字段 ID

### 内容运营

4. **内容质量**：确保内容有价值，符合账号定位
5. **更新频率**：保持稳定的更新频率（建议每周3-5篇）
6. **数据追踪**：定期查看 HAP 中的数据，分析爆款规律
7. **互动管理**：及时回复评论，积极与用户互动
8. **多平台适配**：根据不同平台特点调整内容格式和风格
