---
name: xiaohongshu-automation
description: 小红书自动化控制 - 通过 Playwright CDP 连接 OpenClaw 浏览器实现发布、搜索、评论等功能
triggers:
  - 小红书
  - xiaohongshu
  - xhs
  - 红书
  - 小红书自动化
  - 发布小红书
argument-hint: "<action> [params]"
quality: high
---

# 小红书自动化控制 Skill

## 概述

通过 Playwright MCP 工具连接到 OpenClaw 浏览器（CDP 端口 18800），实现小红书的自动化操作，包括发布内容、搜索、获取推荐、评论等功能。

## 前置条件

1. **OpenClaw 浏览器已启动**：确保 OpenClaw 浏览器运行并开启 CDP 端口 18800
2. **已登录小红书**：首次使用需在 OpenClaw 浏览器中手动登录小红书账号
3. **Playwright MCP 可用**：确保 `mcp__Playwright__*` 工具集已配置

## 连接方式

使用 Playwright 的 `browser_run_code` 工具通过 CDP 连接到 OpenClaw 浏览器：

```javascript
// 连接到 OpenClaw 浏览器
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP('http://localhost:18800');
const context = browser.contexts()[0];
const page = context.pages()[0] || await context.newPage();
```

## 功能清单

| 功能 | 参数 | 说明 |
|------|------|------|
| `check_login_status` | 无 | 检查小红书登录状态 |
| `publish_content` | title, content, images | 发布图文内容 |
| `publish_with_video` | title, content, video | 发布视频内容 |
| `list_feeds` | 无 | 获取首页推荐列表 |
| `search_feeds` | keyword | 搜索小红书内容 |
| `get_feed_detail` | feed_id, xsec_token | 获取帖子详情 |
| `post_comment_to_feed` | feed_id, xsec_token, content | 发表评论 |
| `user_profile` | user_id, xsec_token | 获取用户主页信息 |
| `get_hot_topics` | category (可选) | 获取热门话题列表 |
| `download_stock_images` | keyword, count | 从图库下载无水印图片 |

---

## 功能实现指南

### 1. check_login_status - 检查登录状态

**步骤：**
1. 使用 `mcp__Playwright__browser_navigate` 导航到 `https://www.xiaohongshu.com`
2. 使用 `mcp__Playwright__browser_snapshot` 获取页面快照
3. 检查快照中是否包含用户头像或登录按钮
4. 返回登录状态

**实现代码：**
```javascript
async (page) => {
  await page.goto('https://www.xiaohongshu.com');
  await page.waitForLoadState('networkidle');

  // 检查是否有登录用户的头像
  const userAvatar = await page.$('.user-avatar, .login-btn');
  const isLoggedIn = await page.$('.user-avatar') !== null;

  return { isLoggedIn, message: isLoggedIn ? '已登录' : '未登录，请先登录' };
}
```

---

### 2. publish_content - 发布图文内容

**参数：**
- `title` (必需): 标题，**不超过 20 字**
- `content` (必需): 正文内容，**不超过 1000 字**
- `images` (必需): 图片数组，支持本地绝对路径或 HTTP 链接

**步骤：**
1. 导航到发布页面 `https://creator.xiaohongshu.com/publish/publish`
2. 等待页面加载完成
3. 上传图片（点击上传区域，选择文件）
4. 填写标题
5. 填写正文内容
6. 点击发布按钮
7. 等待发布完成

**实现代码：**
```javascript
async (page) => {
  const title = '你的标题';  // ≤20字
  const content = '你的正文内容';  // ≤1000字
  const images = ['/path/to/image1.jpg', '/path/to/image2.jpg'];

  // 1. 导航到发布页面
  await page.goto('https://creator.xiaohongshu.com/publish/publish');
  await page.waitForLoadState('networkidle');

  // 2. 上传图片
  const uploadInput = await page.$('input[type="file"]');
  await uploadInput.setInputFiles(images);
  await page.waitForTimeout(3000); // 等待上传完成

  // 3. 填写标题
  const titleInput = await page.$('[placeholder*="标题"]');
  await titleInput.fill(title);

  // 4. 填写正文
  const contentInput = await page.$('[placeholder*="正文"], .ql-editor');
  await contentInput.fill(content);

  // 5. 点击发布
  const publishBtn = await page.$('button:has-text("发布")');
  await publishBtn.click();

  // 6. 等待发布完成
  await page.waitForTimeout(5000);

  return { success: true, message: '发布成功' };
}
```

**使用 Playwright MCP 工具的方式：**
```
1. mcp__Playwright__browser_navigate: url="https://creator.xiaohongshu.com/publish/publish"
2. mcp__Playwright__browser_snapshot: 获取页面结构
3. mcp__Playwright__browser_file_upload: paths=["/path/to/image.jpg"]
4. mcp__Playwright__browser_type: ref="标题输入框ref", text="标题内容"
5. mcp__Playwright__browser_type: ref="正文输入框ref", text="正文内容"
6. mcp__Playwright__browser_click: ref="发布按钮ref"
```

---

### 3. publish_with_video - 发布视频内容

**参数：**
- `title` (必需): 标题，**不超过 20 字**
- `content` (必需): 正文内容，**不超过 1000 字**
- `video` (必需): 视频文件**本地绝对路径**（不支持 HTTP 链接）

**步骤：**
1. 导航到发布页面
2. 上传视频文件
3. **等待视频处理完成**（可能需要较长时间）
4. 填写标题和正文
5. 点击发布

**注意事项：**
- 仅支持本地视频文件
- 视频处理时间较长，建议文件大小不超过 1GB
- 需要等待视频处理完成后才能发布

---

### 4. list_feeds - 获取首页推荐列表

**步骤：**
1. 导航到 `https://www.xiaohongshu.com`
2. 等待页面加载
3. 获取页面快照
4. 解析推荐列表中的帖子信息

**返回数据结构：**
```json
{
  "feeds": [
    {
      "feed_id": "帖子ID",
      "xsec_token": "安全令牌",
      "title": "帖子标题",
      "author": "作者名称",
      "likes": "点赞数",
      "cover_url": "封面图URL"
    }
  ]
}
```

**实现代码：**
```javascript
async (page) => {
  await page.goto('https://www.xiaohongshu.com');
  await page.waitForLoadState('networkidle');

  // 获取推荐列表
  const feeds = await page.$$eval('.note-item, .feed-item', items => {
    return items.map(item => ({
      feed_id: item.getAttribute('data-id') || item.querySelector('a')?.href?.match(/\/explore\/(\w+)/)?.[1],
      title: item.querySelector('.title')?.textContent,
      author: item.querySelector('.author')?.textContent,
      likes: item.querySelector('.like-count')?.textContent
    }));
  });

  return { feeds };
}
```

---

### 5. search_feeds - 搜索小红书内容

**参数：**
- `keyword` (必需): 搜索关键词

**步骤：**
1. 导航到搜索页面 `https://www.xiaohongshu.com/search_result?keyword={keyword}`
2. 等待搜索结果加载
3. 解析搜索结果列表
4. 返回帖子列表（包含 feed_id 和 xsec_token）

**实现代码：**
```javascript
async (page) => {
  const keyword = '搜索关键词';

  await page.goto(`https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}`);
  await page.waitForLoadState('networkidle');

  // 解析搜索结果
  const results = await page.$$eval('.note-item', items => {
    return items.map(item => {
      const link = item.querySelector('a')?.href || '';
      const match = link.match(/\/explore\/(\w+)\?xsec_token=([^&]+)/);
      return {
        feed_id: match?.[1],
        xsec_token: match?.[2],
        title: item.querySelector('.title')?.textContent,
        author: item.querySelector('.author')?.textContent
      };
    });
  });

  return { keyword, results };
}
```

---

### 6. get_feed_detail - 获取帖子详情

**参数：**
- `feed_id` (必需): 帖子 ID
- `xsec_token` (必需): 安全令牌（从 list_feeds 或 search_feeds 获取）

**步骤：**
1. 导航到帖子详情页 `https://www.xiaohongshu.com/explore/{feed_id}?xsec_token={xsec_token}`
2. 等待页面加载
3. 获取帖子内容、互动数据、评论列表

**返回数据结构：**
```json
{
  "feed_id": "帖子ID",
  "title": "标题",
  "content": "正文内容",
  "images": ["图片URL数组"],
  "author": {
    "user_id": "用户ID",
    "nickname": "昵称",
    "avatar": "头像URL"
  },
  "stats": {
    "likes": "点赞数",
    "collects": "收藏数",
    "comments": "评论数",
    "shares": "分享数"
  },
  "comments": [
    {
      "user": "评论用户",
      "content": "评论内容",
      "time": "评论时间"
    }
  ]
}
```

---

### 7. post_comment_to_feed - 发表评论

**参数：**
- `feed_id` (必需): 帖子 ID
- `xsec_token` (必需): 安全令牌
- `content` (必需): 评论内容

**步骤：**
1. 导航到帖子详情页
2. 定位评论输入框
3. 输入评论内容
4. 点击发送按钮
5. 等待评论发布成功

**实现代码：**
```javascript
async (page) => {
  const feed_id = '帖子ID';
  const xsec_token = '安全令牌';
  const comment = '评论内容';

  await page.goto(`https://www.xiaohongshu.com/explore/${feed_id}?xsec_token=${xsec_token}`);
  await page.waitForLoadState('networkidle');

  // 定位评论输入框
  const commentInput = await page.$('[placeholder*="评论"], .comment-input');
  await commentInput.click();
  await commentInput.fill(comment);

  // 点击发送
  const sendBtn = await page.$('button:has-text("发送"), .send-btn');
  await sendBtn.click();

  await page.waitForTimeout(2000);

  return { success: true, message: '评论发布成功' };
}
```

---

### 8. user_profile - 获取用户主页信息

**参数：**
- `user_id` (必需): 用户 ID
- `xsec_token` (必需): 安全令牌

**步骤：**
1. 导航到用户主页 `https://www.xiaohongshu.com/user/profile/{user_id}?xsec_token={xsec_token}`
2. 获取用户基本信息
3. 获取统计数据
4. 获取笔记列表

**返回数据结构：**
```json
{
  "user_id": "用户ID",
  "nickname": "昵称",
  "bio": "简介",
  "avatar": "头像URL",
  "verified": "是否认证",
  "stats": {
    "following": "关注数",
    "followers": "粉丝数",
    "likes": "获赞数",
    "notes": "笔记数"
  },
  "notes": [
    {
      "feed_id": "笔记ID",
      "title": "标题",
      "cover": "封面图"
    }
  ]
}
```

---

### 9. get_hot_topics - 获取热门话题

**参数：**
- `category` (可选): 话题分类，可选值：美食、美妆、时尚、出行、知识、兴趣爱好

**入口URL：**
`https://creator.xiaohongshu.com/new/inspiration`

**步骤：**
1. 导航到创作者中心笔记灵感页面
2. 等待页面加载完成
3. 如果指定了分类，点击对应分类标签
4. 解析热门话题列表

**返回数据结构：**
```json
{
  "category": "美食",
  "topics": [
    {
      "name": "早餐吃什么",
      "participants": "275.9万人",
      "views": "101.6亿次",
      "hot_notes": [
        {
          "title": "十分钟搞定✅好吃到光盘的番茄荷包蛋焖面‼️",
          "likes": "4.3万"
        }
      ]
    },
    {
      "name": "高颜值巧克力",
      "participants": "27.9万人",
      "views": "13.5亿次",
      "hot_notes": [...]
    }
  ]
}
```

**实现代码：**
```javascript
async (page) => {
  const category = '美食'; // 可选：美食、美妆、时尚、出行、知识、兴趣爱好

  // 1. 导航到笔记灵感页面
  await page.goto('https://creator.xiaohongshu.com/new/inspiration');
  await page.waitForLoadState('networkidle');

  // 2. 如果指定分类，点击分类标签
  if (category) {
    const categoryTab = await page.$(`h6:has-text("${category}")`);
    if (categoryTab) await categoryTab.click();
    await page.waitForTimeout(1000);
  }

  // 3. 解析话题列表
  const topics = await page.$$eval('[class*="topic-card"]', cards => {
    return cards.map(card => ({
      name: card.querySelector('[class*="topic-name"]')?.textContent,
      participants: card.querySelector('[class*="participants"]')?.textContent,
      views: card.querySelector('[class*="views"]')?.textContent
    }));
  });

  return { category, topics };
}
```

**使用 Playwright MCP 工具的方式：**
```
1. mcp__Playwright__browser_navigate: url="https://creator.xiaohongshu.com/new/inspiration"
2. mcp__Playwright__browser_wait_for: time=2
3. mcp__Playwright__browser_snapshot: 获取页面结构
4. 解析快照中的话题信息
```

**可用分类：**
| 分类 | 包含话题示例 |
|------|-------------|
| 美食 | 早餐吃什么、高颜值巧克力、面条的花式做法、咖啡topping |
| 美妆 | 化妆教程、护肤心得、美甲分享 |
| 时尚 | 穿搭分享、包包推荐、饰品搭配 |
| 出行 | 旅行攻略、酒店推荐、景点打卡 |
| 知识 | 学习方法、职场技能、理财知识 |
| 兴趣爱好 | 手工DIY、摄影技巧、宠物日常 |

---

### 10. download_stock_images - 下载无水印图片

**参数：**
- `keyword` (必需): 搜索关键词（必须用英文）
- `count` (可选): 下载数量，默认 3 张
- `save_dir` (可选): 保存目录，默认当前项目目录

**图片来源：Unsplash（唯一来源）**

Unsplash 是全球最大的免费高清图库，所有图片均可免费商用，无需标注来源。

**方式一：使用 Playwright 从 Unsplash 下载**

```javascript
async (page) => {
  const keyword = 'coffee shop'; // 搜索关键词（英文）
  const count = 3; // 下载数量
  const saveDir = '/Users/zee/Desktop/小红书自动化控制/images';

  // 1. 导航到 Unsplash 搜索页
  await page.goto(`https://unsplash.com/s/photos/${encodeURIComponent(keyword)}`);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  // 2. 获取图片下载链接
  const imageUrls = await page.$$eval('figure a[itemprop="contentUrl"]', (links, max) => {
    return links.slice(0, max).map(link => link.href + '/download?force=true');
  }, count);

  // 3. 逐个下载图片
  for (let i = 0; i < imageUrls.length; i++) {
    const downloadPage = await page.context().newPage();
    await downloadPage.goto(imageUrls[i]);
    // 图片会自动下载到默认下载目录
    await downloadPage.waitForTimeout(3000);
    await downloadPage.close();
  }

  return { success: true, count: imageUrls.length };
}
```

**方式二：使用 Unsplash Source API（简单直接）**

```bash
# 从 Unsplash 随机下载指定主题的图片
keyword="coffee,cafe"  # 用逗号分隔多个关键词
save_dir="/Users/zee/Desktop/小红书自动化控制/images"
mkdir -p "$save_dir"

# 下载 3 张 1080x1440 的竖版图片（适合小红书 3:4 比例）
for i in 1 2 3; do
  curl -L "https://source.unsplash.com/random/1080x1440/?${keyword}" \
    -o "${save_dir}/unsplash_$(date +%s)_${i}.jpg"
  echo "Downloaded image ${i}"
  sleep 2  # 避免请求过快，确保获取不同图片
done

echo "Done! Images saved to ${save_dir}"
```

**方式三：使用 Unsplash API（需要免费 API Key，推荐）**

1. 注册获取 API Key: https://unsplash.com/developers
2. 使用以下代码：

```bash
# Unsplash API 下载（更精准的搜索结果）
ACCESS_KEY="your_unsplash_access_key"
keyword="coffee shop dali"
save_dir="/Users/zee/Desktop/小红书自动化控制/images"
mkdir -p "$save_dir"

# 搜索图片
response=$(curl -s -H "Authorization: Client-ID ${ACCESS_KEY}" \
  "https://api.unsplash.com/search/photos?query=${keyword}&per_page=3&orientation=portrait")

# 解析并下载原图
echo "$response" | jq -r '.results[].urls.full' | while read url; do
  filename="${save_dir}/unsplash_$(date +%s%N).jpg"
  curl -L "$url" -o "$filename"
  echo "Downloaded: $filename"
  sleep 1
done
```

**Playwright MCP 工具实现步骤：**

```
1. mcp__Playwright__browser_navigate: url="https://unsplash.com/s/photos/coffee"
2. mcp__Playwright__browser_wait_for: time=2
3. mcp__Playwright__browser_snapshot: 获取页面结构，找到图片链接
4. mcp__Playwright__browser_click: 点击下载按钮
5. 或者直接获取图片 URL 后用 curl 下载
```

**关键词转换规则：**

根据话题/主题内容，AI 自动将中文转换为合适的英文搜索关键词。

**转换原则：**
1. 将中文话题翻译成对应的英文词汇
2. 添加相关的场景词（如 photography, aesthetic, lifestyle）
3. 使用 2-4 个关键词组合，用空格分隔
4. 优先使用具体、描述性的词汇

**自动转换示例：**
```
话题: "早餐吃什么" → 关键词: "breakfast food morning meal"
话题: "咖啡探店" → 关键词: "coffee shop cafe interior latte"
话题: "穿搭分享" → 关键词: "outfit fashion style ootd"
话题: "旅行攻略" → 关键词: "travel landscape adventure"
话题: "家居装饰" → 关键词: "home interior decor cozy"
```

**图片尺寸参数：**

| 参数 | 尺寸 | 适用场景 |
|------|------|---------|
| `1080x1440` | 3:4 竖版 | 小红书推荐比例 |
| `1080x1080` | 1:1 方形 | 小红书方形图 |
| `1440x1080` | 4:3 横版 | 横版展示 |
| `1920x1080` | 16:9 宽屏 | 视频封面 |

**完整工作流程示例：**
```
用户: 获取最新的小红书热点，发布图文并且寻找配图

AI 执行步骤:
1. 调用 get_hot_topics 获取热门话题
   → 获取到话题: "早餐吃什么"

2. 将话题转换为英文关键词
   → "breakfast food morning delicious"

3. 调用 Unsplash 搜索并下载相关图片
   → searchAndDownload("breakfast food morning", "./images", 3, {orientation: "portrait"})

4. 根据话题生成文章内容
   → 标题、正文、推荐话题标签

5. 使用下载的图片发布到小红书
   → publish_content(title, content, images)
```

**注意事项：**
- Unsplash 图片完全免费商用，无需标注来源
- AI 根据话题内容智能生成英文关键词，无需固定映射表
- 下载间隔建议 2 秒以上，避免被限流
- 小红书推荐使用 3:4 竖版图片（orientation: portrait）

---

## AI 内容生成提示词

### 评论生成提示词

生成评论时使用以下提示词，确保评论自然、真实：

```
你是一个小红书用户，正在浏览别人的帖子。请根据以下文章内容，写一条真实、自然的评论。

要求：
1. 像真人一样说话，口语化，不要书面语
2. 适当使用表情符号（1-3个即可，如😂🔥👍❤️✨😭）
3. 评论要和文章内容强相关，提到文章中的具体细节
4. 长度适中，1-2句话，不超过50字
5. 可以表达：共鸣、提问、分享类似经历、表示想去/想试
6. 使用口语词汇如："绝了"、"太真实了"、"蹲一个"、"马住"、"冲了"、"爱住"、"救命"、"笑死"
7. 不要用"哈哈哈"开头，不要太夸张
8. 偶尔可以用不完整句子或省略主语

文章标题：{title}
文章内容：{content}

直接输出评论内容，不要任何解释或引号：
```

**评论示例（好的）：**
- "5r美式也太香了吧 下次去大理必冲！"
- "救命这个院子就是我梦想中的样子😭"
- "蹲一个具体地址 想去打卡"
- "同款体验！上次去也是一呆一下午"
- "看完立马收藏了 下个月就去✨"

**评论示例（不好的）：**
- "哈哈哈哈哈写得真好！" ❌ 太空洞
- "感谢博主的分享，非常有帮助！" ❌ 太正式
- "这篇文章写得很详细，我学到了很多。" ❌ 像机器人

---

### 发布文章提示词

生成小红书文章时使用以下提示词：

```
你是一个小红书博主，正在分享自己的真实体验。请根据主题写一篇小红书笔记。

要求：
1. 标题：不超过20字，要有吸引力，可用｜分隔，适当加emoji
2. 正文：口语化、有画面感、像在和朋友聊天
3. 分段清晰，每段2-3句话，用空行分隔
4. 适当使用emoji点缀（每段1-2个），不要堆砌
5. 内容要具体：有细节、有感受、有实用信息
6. 结尾可以互动：提问或邀请评论
7. 不要在正文里写#标签（标签要单独通过话题按钮添加）

主题：{topic}
关键词：{keywords}
图片内容描述：{image_description}

输出格式：
标题：xxx
正文：xxx
推荐话题：xxx, xxx, xxx（3-5个相关话题）
```

**文章示例（好的）：**
```
标题：大理旅居｜终于找到我的咖啡乌托邦☕

正文：
在大理的第15天，每天最期待的就是去这家小店坐坐

推门进去就是阳光和咖啡香，老板是个不爱说话的大叔，但手冲技术一绝。点了杯云南日晒，果香炸裂，才18块😭

最喜欢下午四五点来，坐在院子里看苍山的云慢慢飘，时间好像停住了

有没有姐妹也在大理？求组队探店！
```

---

### 话题标签添加方式（重要！）

**错误方式**：直接在正文里写 `#大理旅居 #咖啡`
- 这样写只是普通文本，不会生成可点击的话题标签

**正确方式**：
1. 写完正文后，点击输入框下方的「话题」按钮
2. 搜索并选择相关话题
3. 或者点击系统推荐的话题标签

**Playwright 实现步骤**：
```
1. 填写完正文后
2. 点击「话题」按钮 (button "话题")
3. 在弹出的搜索框中输入话题关键词
4. 点击搜索结果中的话题进行添加
5. 重复添加3-5个相关话题
```

---

## 小红书运营知识

### 内容限制
- **标题**: 不超过 **20 字**
- **正文**: 不超过 **1000 字**（不含话题标签）
- **话题标签**: 建议 **3-5 个**
- **每日发帖上限**: 约 **50 篇**

### 最佳实践
- **图文优于视频**: 图文内容的流量通常比视频更好
- **话题标签**: 通过话题按钮添加，不要直接写在正文里
- **热门话题**: 选择浏览量高的话题能获得更多曝光
- **单设备登录**: 同一账号不允许在多个网页端登录，否则会被踢出
- **发布时间**: 晚上7-10点是流量高峰

### 风险提示
- 避免频繁操作，建议间隔发布（2-5分钟）
- 不要发布违规内容
- Cookie 过期需要重新登录
- 评论内容不要太模板化，容易被识别

---

## 使用示例

### 示例 1: 检查登录状态
```
用户: 检查小红书登录状态
AI: 使用 check_login_status 功能...
```

### 示例 2: 发布图文
```
用户: 帮我发布一篇小红书，标题是"今日美食分享"，内容是"今天做了一道红烧肉..."，图片用 /Users/zee/Pictures/food.jpg
AI: 使用 publish_content 功能...
```

### 示例 3: 搜索内容
```
用户: 搜索小红书上关于"旅行攻略"的内容
AI: 使用 search_feeds 功能，keyword="旅行攻略"...
```

### 示例 4: 获取帖子详情并评论
```
用户: 获取这个帖子的详情 feed_id=xxx, xsec_token=yyy，然后发表评论"写得真好！"
AI:
1. 使用 get_feed_detail 获取详情
2. 使用 post_comment_to_feed 发表评论
```

---

## 故障排除

### 问题 1: 无法连接到浏览器
**解决方案**: 确保 OpenClaw 浏览器已启动并开启 CDP 端口 18800

### 问题 2: 显示未登录
**解决方案**: 在 OpenClaw 浏览器中手动登录小红书账号

### 问题 3: 发布失败
**解决方案**:
1. 检查标题是否超过 20 字
2. 检查正文是否超过 1000 字
3. 检查图片路径是否正确
4. 检查账号是否被风控

### 问题 4: 获取不到 xsec_token
**解决方案**: xsec_token 需要从 list_feeds 或 search_feeds 的结果中获取，不能自己构造

---

## 相关资源

- [xiaohongshu-mcp 参考项目](https://github.com/xpzouying/xiaohongshu-mcp)
- [Playwright 文档](https://playwright.dev/docs/api/class-browsertype#browser-type-connect-over-cdp)
