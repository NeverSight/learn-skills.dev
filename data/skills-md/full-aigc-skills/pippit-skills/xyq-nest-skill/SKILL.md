---
name: xyq-nest-skill
description: 通过小云雀的 AI 能力进行综合创作，支持生成和编辑图片/视频。覆盖场景包括：生成（文生图、文生视频、图生视频、做动画、画一个xxx、来段xxx）、编辑修改（把xxx换成yyy、去掉xxx、加上xxx、改成xxx、调整xxx、局部修改、改镜头）、风格转换（风格迁移、转绘、换风格）、视频续写延长、复刻视频/TVC/宣传片、短剧/短漫剧生成、音乐MV生成、产品广告/展示片制作、分镜/故事板设计、教育视频/短视频制作。当用户提到小云雀、xyq、上传参考图/视频、查看生成进度时也应触发。关键判断：只要用户的请求涉及 AI 视频的创作、生成、编辑、修改，无论措辞如何（如"画只猫"、"做个海报"、"做个视频"、"这个视频帮我改一下"、"帮我复刻这段视频"、"用这首歌做个MV"、"一句话生成短剧"），都必须触发此技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "requires":
          {
            "bins": ["python3"],
            "env": ["XYQ_ACCESS_KEY"]
          },
        "primaryEnv": "XYQ_ACCESS_KEY"
      }
  }
---

# 小云雀会话（生视频）

通过 小云雀的API 创建会话、发送消息（生图、生视频、编辑视频等）、上传图片/视频文件，并查询会话消息进展。

小云雀是一个 AI 综合创作平台，同时为人类创作者和 Agent 设计。Agent 通过 Skill 入口理解任务、调用模型并自动编排工作流。

**平台核心能力：**
- **生成**：文生图、文生视频、图生视频、视频续写
- **编辑**：局部修改、元素替换、镜头调整、风格迁移
- **复杂创作**：一句话生成完整短剧（剧本→分镜→成片）、复刻已有视频风格做 TVC/宣传片、用音乐生成 MV、产品展示片制作

用户的所有创作和编辑需求都通过发送自然语言消息来完成，Agent 会自主编排工作流。复杂任务（短剧、MV）耗时较长，需耐心轮询。

## 功能

1. **创建会话 / 发消息** - 创建新会话或向已有会话发送一条消息（如「创作一个视频」）
2. **查询会话进展** - 根据 `thread_id` 、 `run_id`、`after_seq` 增量拉取该会话的消息列表，用于轮询创作过程的消息和最终产物结果
3. **上传文件** - 支持上传`单张图片`或`单个视频文件`到小云雀资产库，得到文件对应的 `asset_id`（编辑已有视频/图片时需要先上传）
4. **下载结果** - 将会话中生成的图片/视频批量下载到本地，支持指定输出目录和文件名前缀。


## 前置要求

```bash
export XYQ_ACCESS_KEY="your-access-key"
```

可选：`XYQ_OPENAPI_BASE` 或 `XYQ_BASE_URL`，默认 `https://xyq.jianying.com`。

无需安装额外依赖，仅使用 Python 标准库。

## 使用方法

### 1. 创建会话 / 发送消息

```bash
# 创建新会话并发送「生一个动漫视频」
python3 {baseDir}/scripts/submit_run.py --message "生一个动漫视频"

# 向已有会话发送消息
python3 {baseDir}/scripts/submit_run.py --message "再生成一个故事视频" --thread-id THREAD_ID
```

### 2. 查询会话进展

```bash
# 查询会话消息列表
python3 {baseDir}/scripts/get_thread.py --thread-id THREAD_ID --run-id RUN_ID --after-seq SEQUENCE
```

> `run_id` 由 `submit_run` 返回，用于指定查询某次具体运行的结果。

### 3. 上传文件

- 当用户提供了参考的文件地址时，先进行文件上传，仅支持图片、视频。
- 单次指令执行仅支持单个文件，多个文件可并行调用，单个文件大小必须在200MB以下。

```bash
# 上传图片
python3 {baseDir}/scripts/upload_file.py /path/to/image.png

# 上传视频
python3 {baseDir}/scripts/upload_file.py /path/to/video.mp4
```

### 4. 下载结果

任务完成后，可以将会话中的所有产物批量下载到本地。

```bash
# 指定 URL 列表，指定输出目录，指定文件名前缀（如 artifact_01.png, artifact_02.png ...）进行下载
python3 {baseDir}/scripts/download_results.py --urls URL1 URL2 URL3 --output-dir ./xyq_output --prefix "artifact"
```

## 典型工作流

理解这些工作流，才能正确组合上面的脚本完成用户需求。

### 场景 1：用户要求生成图片或视频（最常见）

```
1. submit_run.py --message "用户的描述"  →  拿到 thread_id、run_id 和 web_thread_link
2. **立即**将 `web_thread_link` 展示给用户（如"任务已提交，可在此查看：{web_thread_link}"）
3. 每隔 `10` 秒钟调用 get_thread.py --thread-id THREAD_ID --run-id RUN_ID --after-seq SEQUENCE 进行轮询
4. 检查 messages：
  - 当任务还在创作中：
    - 将过程创作信息展示给用户，继续轮询
  - 当任务完成（run 结束）：
    - 如果涉及意图确认/流程中断（如"请回答以下问题"）：
      → 向用户展示问题，等待用户回复
      → 使用 `thread_id` 重新提交任务（保持同一会话，产生新的 run_id）
      → 回到步骤 2 继续轮询（可能多轮，直到不再意图确认）
    - 如果 content 中包含产物 URL：
      → 信息展示 → 下载产物 → 结果展示
5. 自动下载：download_results.py --urls URL1 URL2 URL3 --output-dir 输出目录 --prefix 有意义的前缀
6. 向用户展示：过程中的创作信息，以及下载后的本地文件列表
```

### 场景 2：用户提供图片/视频要求编辑修改（如"参考这个视频做一个新的"）

```
1. upload_file.py /path/to/video.mp4  →  拿到 asset_id
2. submit_run.py --message "参考这个视频做一个新的" --asset-ids asset_id  →  拿到 thread_id、run_id、web_thread_link
3. 后续同场景 1 的步骤 2-6
```

用户给了文件路径 + 编辑指令 = 先上传文件，再把编辑指令和 所有asset_id 一起发送。

### 场景 3：用户提供参考图/视频要求生成新内容

```
1. upload_file.py /path/to/ref1.png  →  拿到 asset_id1
2. upload_file.py /path/to/ref2.mp4  →  拿到 asset_id2
3. 直到所有文件上传完成，拿到所有 asset_id
4. submit_run.py --message "根据参考图、视频生成xxx" --asset-ids asset_id1 asset_id2, ...  →  拿到 thread_id、run_id、web_thread_link
5. 后续同场景 1 的步骤 2-6
```

### 场景 4：在已有会话中追加新需求

```
1. submit_run.py --message "新的描述" --thread-id THREAD_ID  →  拿到 thread_id、run_id、web_thread_link
2. 后续同场景 1 的步骤 2-6
```

### 轮询策略

- **间隔**：每 10 秒查询一次
- **增量拉取**：首次用 --after-seq 0，后续根据messages消息列表长度，计算新的 seq 值
- **完成判断**：当创作任务完成且messages的content中包含产物结果 URL（图片/视频地址）
- **超时**：连续轮询 `48 小时`仍无结果，告知用户"生成时间较长，可稍后查看"，不再继续轮询
- **错误重试**：单次查询失败可重试 1 次，连续 3 次失败则停止并告知用户

## 输出格式

**submit_run** 返回：
```json
{
  "thread_id": "90f05e0c-...",
  "run_id": "abc123-...",
  "web_thread_link": "https://xyq.jianying.com/..."
}
```

**get_thread** 返回：
```json
{
  "messages": [
    {"id": "1", "role": "user", "content": "生一个动漫视频"},
    {"id": "2", "role": "assistant", "content": [
      {
        "type": "{type}",
        "subtype": "{sub_type}",
        "data": {...}
      }
    ]},
    {"id": "3", "role": "assistant", "content": [
      {
        "type": "{type}",
        "subtype": "{sub_type}",
        "data": {..., "url": "{url}"....}
      }
    ]}
  ]
}
```

**upload_file** 返回：
```json
{
  "asset_id": "{asset_id}"
}
```

**download_results** 返回：
```json
{
  "output_dir": "./xyq_output",
  "downloaded": ["./xyq_output/01.png", "..."],
  "total": 10
}
```

## 向用户展示内容

- 任务提交后：立即将 `web_thread_link` 展示给用户，方便用户直接打开浏览器查看任务页面
- 任务在创作中：
  - 展示过程中的创作信息等，继续轮询
- 任务完成（run 结束）：
  - 若涉及意图确认/流程中断（如"请回答以下问题"）→ 展示问题 → 等待用户回复 → 使用同一 `thread_id` 重新提交任务 → 继续轮询（可能多轮）
  - 若 content 中包含产物 URL：
  - 结果地址：来自 `get_thread` 返回的 `messages` 中，任务创作完成会包含产物 URL，将产物链接、下载的本地文件等信息告知用户。

## 核心原则：用户侧不做创作，只做传话

你（用户侧 Agent）的职责是**搬运工**，不是创作者。后端有专门的 Agent 负责理解需求、拆解分镜、编排工作流、选模型、写 prompt。你要做的只有三件事：

1. **上传**：如果用户给了本地文件 → `upload_file.py` 拿到 asset_id
2. **提交任务**：把用户的原始描述 + asset_id 原封不动发给 `submit_run.py`
3. **传话**：根据 `get_thread.py` 返回的消息列表，展示过程中的意图询问、创作信息等
4. **取件**：`get_thread.py` 轮询结果 → 检查结果 → 下载产物 → 结果展示给用户

**绝对不要做的事：**
- 不要替用户扩写、润色、翻译 prompt（用户说"帮我推演分镜"，就直接传"帮我推演分镜"，不要自己先写个分镜表再逐条发）
- 不要自行编排镜头描述、剧情推演、风格分析
- 不要在消息中添加自己编的 prompt（如"超写实风格，电影级光影，8K分辨率"之类的描述词）

后端 Agent 对模型能力、参数配置、prompt 工程远比用户侧更专业。用户侧越俎代庖只会降低生成质量，换个弱模型更是灾难。

**正确示例：**
```
用户说：「根据多张参考图，做个科普故事视频」
用户给了参考图：/path/to/ref1.png, /path/to/ref2.png, /path/to/ref3.png

→ upload_file.py /path/to/ref1.png →  拿到 asset_id1
→ upload_file.py /path/to/ref2.png →  拿到 asset_id2
→ upload_file.py /path/to/ref3.png →  拿到 asset_id3
→ submit_run.py --message "根据参考图、视频生成xxx" --asset-ids asset_id1 asset_id2, asset_id3  →  拿到 web_thread_link，立即展示给用户
→ 轮询 ─┬─ 意图确认 → 用户确认 → 使用 thread_id 重新提交 → 继续轮询
        └─ 无意图确认 → 信息展示 → 下载产物 → 结果展示
```

**错误示例：**
```
❌ 用户侧自己先写了个九宫格分镜表（对峙、交锋、危机...）
❌ 然后把自己编的描述发给后端
❌ 或者拆成9次 submit_run 分别发送
```

## 注意事项

- 鉴权方式为请求头 `Authorization: Bearer <XYQ_ACCESS_KEY>`
- 创建会话时 `message` 是用户的指令要求，不能为空
- 查询会话时可用 --after-seq 做增量拉取，便于轮询新消息（含 assistant 回复与生图/生视频结果）
- 上传文件仅支持图片（image/*）和视频（video/*）类型，其他类型会被拒绝，文件大小须在 200MB 以下
- 生成过程中将过程中的创作信息展示给用户；任务完成后给出**产物结果（图片/视频）URL链接**和下载的**本地文件列表**。
