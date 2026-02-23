---
name: moltbook-hot-posts
description: 查询Moltbook（Agent社区）热门帖子信息。当用户想要查询Agent社区热帖、最新讨论、热门话题时使用此skill。
---

# Moltbook热帖检索

## 依赖

```bash
python3 -m pip install wuying-agentbay-sdk
```

## 安装步骤

在使用此技能之前，请确保已安装必要的依赖包：

```bash
python3 -m pip install wuying-agentbay-sdk
```

## 使用场景

- 用户想查询Moltbook（Agent社区）的热门帖子
- 用户想了解Agent近期的最新讨论话题
- 用户想了解AI Agent社区的热点动态

## 使用方法

```bash
python3 scripts/browser-use.py "<任务执行步骤>"
```

## 快速示例

### 示例1：查询今日热帖Top 1
```bash
python3 scripts/browser-use.py " \
1. 进入Moltbook网站 https://www.moltbook.com/ \
2. 下滑页面到Posts区域 \
3. 将Posts顶栏中的时间设置为Today，筛选设置为Top（每次进入帖子前都要重新设置） \
4. 待页面更新后，进入第一条帖子查看主帖内容 \
5. 总结每个帖子的核心内容，以markdown格式返回
"
```

### 示例2：查询本周热帖Top 1
```bash
python3 scripts/browser-use.py " \
1. 访问 https://www.moltbook.com/ \
2. 滚动到Posts区域 \
3. 设置时间为This Week，筛选为Top（每次进入帖子前都要重新设置） \
4. 提取第一条热帖的标题、作者和核心内容 \
5. 返回markdown格式的总结
"
```

### 示例3：查询最新帖子
```bash
python3 scripts/browser-use.py " \
1. 打开 https://www.moltbook.com/ \
2. 找到Posts区域 \
3. 设置筛选为New（每次进入帖子前都要重新设置） \
4. 查看第一条最新帖子的详细内容 \
5. 以markdown格式返回帖子摘要
"
```

## 输出格式

```markdown
## Moltbook热帖 - Today Top 1

### 1. 帖子标题
- **作者**: xxx
- **发布时间**: xxx
- **互动数据**: 点赞数/评论数/浏览数
- **核心内容**:
  简要概述帖子的主要内容，包括关键观点、讨论话题、技术方案等

### 热帖趋势总结
- 当前热点话题：xxx
- 讨论焦点：xxx
- 技术趋势：xxx
```

## 注意事项

- 始终注明信息来源为Moltbook（Agent社区）
- 不需要创建新的脚本，用skill目录下的browser-use.py
- 任务执行需要1~2分钟，请耐心等待观察，也不要重试
- skill调用后，控制台会打印出asp流化链接（可视化的url），可告知用户查看
- 只需查看主帖内容和前三个楼层的回帖，不需要爬取所有评论楼层