---
name: wecom-automation
description: 企业微信个人账号直连自动化。基于 Wechaty 框架实现企业微信消息接收、自动同意好友、知识库问答、人工介入提醒。适用于企业微信个人机器人和自动化助手场景。
allowed-tools: Bash, Read, Write, Edit, Exec, mcporter__*
---

# 企业微信个人账号直连自动化

基于 Wechaty 框架连接企业微信个人账号，实现完整的 AI 助手功能。适用于企业微信机器人、自动化客服、个人助手等场景。

## 核心功能

### 1. 自动同意好友添加
- 监听好友请求事件
- 自动通过好友验证
- 发送个性化欢迎消息
- 标注用户信息和来源

### 2. 智能问答（基于知识库）
- 向量知识库存储企业知识
- 语义搜索匹配问题
- LLM 生成专业回复
- 支持多轮对话上下文

### 3. 人工介入提醒
- 置信度阈值自动判断
- 通过 Telegram/飞书通知人工
- 记录未解决问题用于优化
- 平滑转接到人工客服

### 4. 消息类型支持
- 文本消息（问答、对话）
- 图片消息（OCR、识别）
- 文件消息（DOCX、PDF 等）
- 语音消息（转文字、语音交互）
- 链接消息（预览、摘要）
- 名片消息（保存、处理）

## 技术架构

```
┌──────────────┐
│  企业微信     │
│  个人账号     │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│   Wechaty        │
│   (PadLocal)     │
└──────┬───────────┘
       │
       ▼
┌────────────────────┐
│  OpenClaw Gateway  │
│  (消息分发、处理）   │
└──────┬─────────────┘
       │
       ├──────────────┬──────────────┐
       │              │              │
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ 向量知识库 │   │  LLM API  │   │ 通知服务  │
│(PG+pgvec)│   │ (Kimi/GPT)│   │(Telegram)│
└──────────┘   └──────────┘   └──────────┘
```

## 快速开始

### 方案选择

企业微信个人账号直连有两种方案：

#### 方案 A：Wechaty + PadLocal（推荐，适合个人）
**优点**：
- 配置简单，快速上手
- 稳定性高，官方维护
- 支持所有消息类型
- 适合个人使用

**缺点**：
- PadLocal 需要付费（约 50 元/月）
- 单账号限制

**适用场景**：个人助手、小规模客服

#### 方案 B：企业微信内部应用 API（适合企业）
**优点**：
- 官方 API，免费使用
- 稳定性最高
- 支持大规模部署

**缺点**：
- 需要企业认证
- 配置相对复杂
- 功能受限于 API

**适用场景**：企业客服、大规模应用

**本技能使用方案 A（Wechaty + PadLocal）**

### 第一步：申请 PadLocal Token

1. 访问 https://github.com/wechaty/wechaty
2. 选择 "PadLocal" 协议
3. 注册账号并获取 Token
4. 保存 Token 到 pass：

```bash
pass insert api/wechaty-padlocal
```

### 第二步：安装依赖

```bash
# 1. 安装 Node.js 依赖
cd ~/clawd/skills/wecom-automation
npm install

# 2. 安装 Python 依赖
pip3 install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
```

### 第三步：配置环境变量

编辑 `~/clawd/skills/wecom-automation/.env`：

```env
# Wechaty 配置
WECHATY_PUPPET=padlocal
WECHATY_TOKEN=$(pass show api/wechaty-padlocal)
WECHATY_LOG_LEVEL=info

# 企业微信账号配置
WECOM_NAME="企业微信机器人"
WECOM_QR_CODE_PATH=/tmp/wecom_qrcode.png

# 知识库配置
KB_DB_URL=postgresql://postgres@localhost/wecom_kb
KB_SIMILARITY_THRESHOLD=0.7
KB_TOP_K=3

# LLM 配置
LLM_PROVIDER=kimi
LLM_API_KEY=$(pass show api/kimi)
LLM_API_BASE=https://api.moonshot.cn/v1
LLM_MODEL=moonshot-v1-8k

# 人工介入通知
NOTIFICATION_CHANNEL=telegram:YOUR_TELEGRAM_ID
NOTIFICATION_ENABLED=true

# OpenClaw Gateway 配置
GATEWAY_URL=http://localhost:8080
GATEWAY_TOKEN=$(pass show api/openclaw-gateway)
```

### 第四步：初始化数据库

```bash
# 创建数据库
sudo -u postgres createdb wecom_kb

# 初始化表结构
psql wecom_kb < ~/clawd/skills/wecom-automation/schema.sql

# 导入示例知识库
python3 ~/clawd/skills/wecom-automation/scripts/import_kb.py \
  --input ~/clawd/skills/wecom-automation/knowledge/sample.md \
  --category "常见问题" \
  --key "$(pass show api/kimi)"
```

### 第五步：启动机器人

```bash
# 方式 1：直接运行
cd ~/clawd/skills/wecom-automation
npm start

# 方式 2：通过 PM2（推荐）
pm2 start ~/clawd/skills/wecom-automation/ecosystem.config.js

# 查看日志
pm2 logs wecom-bot
```

### 第六步：扫码登录

启动机器人后会显示二维码：

```
██████████████████████████████████
██                              ██
██  1. 打开企业微信 → 扫一扫    ██
██  2. 扫描下方二维码登录      ██
██                              ██
██████████████████████████████████

[二维码图片]
```

使用企业微信扫码登录后，机器人即可正常工作。

## 使用方法

### 场景 1：新好友自动欢迎

```javascript
// workflows/on_friend_add.js
const { Contact } = require('wechaty')

bot.on('friendship', async friendship => {
  if (friendship.type() === Friendship.Type.Receive) {
    const contact = friendship.contact()

    // 自动通过好友请求
    await friendship.accept()

    // 发送欢迎消息
    await contact.say(`👋 欢迎来到${contact.name()}！

我是智能助手小a，可以帮您：
• 解答常见问题
• 处理售后请求
• 查询订单状态

如有复杂问题，我会转接人工客服为您服务。`)

    // 添加到数据库
    await saveUser(contact)
  }
})
```

### 场景 2：知识库问答

```javascript
// workflows/answer_question.js
const { Message } = require('wechaty')

bot.on('message', async msg => {
  if (msg.type() === Message.Type.Text) {
    const text = msg.text()
    const from = msg.from()

    // 搜索知识库
    const results = await searchKnowledge(text)

    // 生成答案
    const answer = await generateAnswer(text, results)

    // 判断是否需要人工介入
    if (answer.confidence < 0.7) {
      await escalateToHuman(from, text, answer)
    } else {
      await msg.say(answer.text)
    }
  }
})
```

### 场景 3：文件处理（DOCX/PDF）

```javascript
// workflows/handle_file.js
const { Message } = require('wechaty')

bot.on('message', async msg => {
  if (msg.type() === Message.Type.Attachment) {
    const file = await msg.toFileBox()

    // 下载文件
    const filePath = `/tmp/${file.name}`
    await file.toFile(filePath)

    // 处理文件（提取内容、分析等）
    const content = await extractFileContent(filePath)

    // 发送回复
    await msg.say(`✅ 已收到文件：${file.name}\n\n正在处理...`)

    // 处理后回复
    await processAndReply(msg, content)
  }
})
```

### 场景 4：人工介入提醒

```javascript
// workflows/escalate.js
async function escalateToHuman(contact, question, answer) {
  // 1. 发送用户消息
  await contact.say('⏳ 已为您转接人工客服，请稍候...')

  // 2. 通过 Telegram 通知人工客服
  const notification = `🚨 需要人工介入

用户：${contact.name()}
问题：${question}
时间：${new Date().toLocaleString()}

请及时处理。`

  await sendTelegramNotification(notification)

  // 3. 记录未解决问题
  await saveUnknownQuestion(contact, question)
}
```

## 目录结构

```
~/clawd/skills/wecom-automation/
├── SKILL.md                    # 本文件
├── package.json                # Node.js 依赖
├── requirements.txt            # Python 依赖
├── ecosystem.config.js         # PM2 配置
├── .env.example                # 环境变量模板
├── schema.sql                  # 数据库表结构
├── bot.js                      # Wechaty 机器人主文件
├── config/
│   ├── knowledge.js            # 知识库配置
│   └── escalation.js           # 人工介入规则
├── workflows/
│   ├── on_friend_add.js        # 好友添加处理
│   ├── answer_question.js      # 问答处理
│   ├── handle_file.js          # 文件处理
│   └── escalate.js             # 人工介入
├── lib/
│   ├── knowledge.js            # 知识库操作
│   ├── llm.js                  # LLM 调用
│   ├── notification.js         # 通知服务
│   └── database.js             # 数据库操作
└── knowledge/
    └── sample.md               # 示例知识文档
```

## API 参考文档

### 企业微信 API 文档
- [企业微信 API 总览](https://developer.work.weixin.qq.com/document/path/90665)
- [消息发送](https://developer.work.weixin.qq.com/document/path/90236)
- [成员管理](https://developer.work.weixin.qq.com/document/path/90198)

### Wechaty 文档
- [Wechaty 官方文档](https://wechaty.js.org)
- [PadLocal 协议](https://github.com/wechaty/puppet-service)
- [消息类型](https://wechaty.js.org/docs/api/message)

### Kimi API 文档
- [Kimi API 总览](https://platform.moonshot.cn/docs)
- [Embedding API](https://platform.moonshot.cn/docs/api/embedding)
- [Chat API](https://platform.moonshot.cn/docs/api/chat)

## 高级功能

### 1. 多轮对话记忆

```javascript
// 使用 Redis 存储会话上下文
const redis = require('redis')
const client = redis.createClient()

async function getConversationHistory(userId) {
  const history = await client.get(`conv:${userId}`)
  return history ? JSON.parse(history) : []
}

async function appendMessage(userId, role, content) {
  const history = await getConversationHistory(userId)
  history.push({ role, content, timestamp: Date.now() })
  await client.set(`conv:${userId}`, JSON.stringify(history))
}
```

### 2. 文件处理

```javascript
// 提取 DOCX 内容
const docx = require('docx')

async function extractDocx(filePath) {
  const doc = await docx.Document.read(filePath)
  const text = doc.paragraphs.map(p => p.text).join('\n')
  return text
}

// 提取 PDF 内容
const pdf = require('pdf-parse')

async function extractPdf(filePath) {
  const data = await fs.readFile(filePath)
  const result = await pdf(data)
  return result.text
}
```

### 3. 语音转文字

```python
# 使用 Whisper API
import openai

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio
        )
    return transcript["text"]
```

### 4. 图片 OCR

```python
# 使用 Kimi Vision
import openai

def ocr_image(image_path):
    with open(image_path, "rb") as image:
        result = openai.chat.completions.create(
            model="gemini-2.5-pro",
            messages=[{
                "role": "user",
                "content": "识别图片中的文字"
            }],
            image=image
        )
    return result.choices[0].message.content
```

## 监控与维护

### 日志查看

```bash
# PM2 日志
pm2 logs wecom-bot

# 错误日志
pm2 logs wecom-bot --err

# 实时日志
pm2 logs wecom-bot --lines 100
```

### 性能监控

```javascript
// 添加自定义指标
const prometheus = require('prom-client')

const messageCounter = new prometheus.Counter({
  name: 'wecom_messages_total',
  help: 'Total messages received',
  labelNames: ['type']
})

const answerLatency = new prometheus.Histogram({
  name: 'wecom_answer_latency_seconds',
  help: 'Answer generation latency',
  buckets: [0.1, 0.5, 1, 2, 5, 10]
})
```

### 人工介入统计

```sql
-- 查看未解决问题分布
SELECT
    COUNT(*) as count,
    SUBSTRING(question, 1, 30) as question_preview
FROM unknown_questions
GROUP BY question_preview
ORDER BY count DESC
LIMIT 10;

-- 查看每日介入次数
SELECT
    DATE(created_at) as date,
    COUNT(*) as escalations
FROM escalation_log
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT 7;
```

## 故障排查

### 问题 1：无法扫码登录

```bash
# 检查 Wechaty 日志
pm2 logs wecom-bot --lines 50

# 重启机器人
pm2 restart wecom-bot

# 清理缓存
rm -rf /tmp/wechaty*
pm2 restart wecom-bot
```

### 问题 2：消息不回复

```bash
# 检查知识库连接
psql wecom_kb -c "SELECT COUNT(*) FROM knowledge_chunks;"

# 测试 LLM API
curl -X POST https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer $KIMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"moonshot-v1-8k","messages":[{"role":"user","content":"测试"}]}'

# 检查环境变量
cat ~/clawd/skills/wecom-automation/.env | grep -E "^(LLM|KB|NOTIFICATION)"
```

### 问题 3：文件无法接收

```bash
# 检查临时目录权限
ls -la /tmp/

# 创建日志目录
mkdir -p ~/clawd/skills/wecom-automation/logs
chmod 755 ~/clawd/skills/wecom-automation/logs

# 检查磁盘空间
df -h
```

## 安全最佳实践

1. **密钥管理**
   - 所有密钥使用 `pass` 存储
   - 环境变量引用，不硬编码
   - 定期轮换 Token

2. **数据隐私**
   - 客户信息加密存储
   - 定期清理敏感日志
   - 遵守数据保护法规

3. **访问控制**
   - API 接口鉴权
   - IP 白名单限制
   - 请求频率限制

4. **审计日志**
   - 记录所有人工介入
   - 定期审查访问日志
   - 异常行为告警

## 扩展功能

### 1. 主动营销

```javascript
// 定期推送优惠信息
const schedule = require('node-schedule')

schedule.scheduleJob('0 10 * * 1-5', async () => {
  const users = await getActiveUsers(7)
  for (const user of users) {
    await user.say('🎉 今日特惠：...')
  }
})
```

### 2. 群组管理

```javascript
// 自动邀请用户加入群组
bot.on('friendship', async friendship => {
  const contact = friendship.contact()
  const room = await bot.Room.find({ topic: '客户群' })

  if (room) {
    await room.add(contact)
    await contact.say('已邀请您加入客户群')
  }
})
```

### 3. 数据统计

```javascript
// 每日生成报表
async function generateDailyReport() {
  const stats = {
    newUsers: await countNewUsers(),
    questions: await countQuestions(),
    escalations: await countEscalations()
  }

  await sendReportToAdmin(stats)
}
```

## 相关技能

- **wecom-cs-automation**: 企业微信客服 API 方式
- **feishu-automation**: 飞书平台自动化
- **notion-automation**: Notion 知识库集成
- **telegram-automation**: Telegram 通知集成

## 成本对比

| 方案 | 月成本 | 适用场景 |
|------|--------|---------|
| **Wechaty + PadLocal** | ~50元 | 个人、小团队 |
| **企业微信内部应用** | 免费 | 企业、大规模 |
| **企业微信客服 API** | 按量 | 企业客服 |

## 参考资源

- [Wechaty GitHub](https://github.com/wechaty/wechaty)
- [PadLocal 官网](https://github.com/wechaty/puppet-service)
- [企业微信开发者中心](https://developer.work.weixin.qq.com/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
