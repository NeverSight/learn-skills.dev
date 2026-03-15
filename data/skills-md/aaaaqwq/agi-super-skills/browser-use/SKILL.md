---
name: browser-use
description: AI驱动的智能浏览器自动化工具。使用LLM理解页面并自动执行任务，比传统Playwright更智能、更省token。适用于复杂交互、动态页面、需要智能决策的浏览器操作。Chrome浏览器优先。
allowed-tools: Bash, Exec, Read, Write
---

# browser-use 智能浏览器自动化

## 概述

browser-use 是一个 AI 驱动的浏览器自动化工具，它使用 LLM 来：
- 理解网页内容
- 智能决策下一步操作
- 自动完成任务

与 Playwright 的区别：
| 特性 | Playwright | browser-use |
|------|-----------|-------------|
| 控制方式 | 预编程脚本 | AI智能决策 |
| 适应性 | 页面变化需重写 | 自动适应 |
| Token消耗 | 较低但需调试 | 智能精简 |
| 复杂交互 | 需精确选择器 | 自然语言描述 |
| 维护成本 | 高 | 低 |

## 安装状态

✅ 已安装：
- browser-use 0.11.11
- browser-use-sdk 2.0.15

## 快速开始

### 基本用法

```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="打开 polymarket.com，查看 Fed 利率市场",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### 使用自定义 LLM（推荐配置）

**⚠️ 重要**：xingsuancode API 是 **Anthropic 格式**，不是 OpenAI 格式！必须使用 `ChatAnthropic`。

```python
from browser_use.llm.anthropic.chat import ChatAnthropic

# xingsuancode API（Anthropic 兼容）✅ 推荐
llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    base_url="https://cn.xingsuancode.com",  # 注意：不加 /v1
    api_key="your-api-key",  # 或从 pass show api/xingsuancode 获取
)

agent = Agent(
    task="你的任务",
    llm=llm,
)
```

```python
# ❌ 错误用法：不要用 ChatOpenAI + xingsuancode
# from browser_use.llm.openai.chat import ChatOpenAI  # 这个不行！xingsuancode 不支持 OpenAI 格式
```

```python
# 如果使用 OpenAI 兼容 API（如 aixn），用 ChatOpenAI：
from browser_use.llm.openai.chat import ChatOpenAI
llm = ChatOpenAI(
    model="gpt-4o",
    base_url="https://ai.9w7.cn/v1",
    api_key="your-api-key",
)
```

### 使用 Chrome 浏览器

```python
from browser_use import Agent, BrowserProfile, BrowserSession

# 配置使用 Chrome
profile = BrowserProfile(
    executable_path="/usr/bin/google-chrome-stable",
    headless=True,
    disable_security=True,
)
session = BrowserSession(browser_profile=profile)

agent = Agent(
    task="任务描述",
    llm=llm,
    browser_session=session,
)
```

### 保存/加载登录态

```python
# 保存登录态
await browser_context.save_storage_state(path="polymarket_auth.json")

# 加载登录态
context = BrowserContextConfig(
    storage_state="polymarket_auth.json"
)
```

## 常用配置

### 最小化 Token 消耗

```python
agent = Agent(
    task="任务",
    llm=llm,
    use_vision=False,  # 禁用视觉，减少token
    max_actions_per_step=3,  # 限制每步操作数
    message_compaction=True,  # 消息压缩
)
```

### 调试模式

```python
agent = Agent(
    task="任务",
    llm=llm,
    headless=False,  # 显示浏览器
    slow_mo=1000,  # 慢放，每步延迟1秒
    save_conversation_path="debug_log/",  # 保存日志
)
```

### 提取结构化数据

```python
from pydantic import BaseModel

class MarketData(BaseModel):
    question: str
    yes_price: float
    no_price: float

agent = Agent(
    task="获取 Polymarket Fed 利率市场数据",
    llm=llm,
    output_model_schema=MarketData,
)
result = await agent.run()
# result 将是 MarketData 类型
```

## Polymarket 集成

### 查看市场

```python
agent = Agent(
    task="""
    1. 打开 https://polymarket.com/event/fed-decision-in-march-885
    2. 提取以下信息：
       - 市场问题
       - Yes 价格
       - No 价格
       - 交易量
    3. 返回 JSON 格式数据
    """,
    llm=llm,
)
```

### 执行交易

```python
agent = Agent(
    task="""
    1. 打开 Polymarket
    2. 连接钱包（如果需要）
    3. 导航到 Fed 利率市场
    4. 买入 $0.60 的 No（价格 ≥ 0.85）
    5. 确认交易
    """,
    llm=llm,
    sensitive_data={
        "wallet_address": "0x...",
    }
)
```

## 最佳实践

### 1. 任务描述要清晰

```python
# 好 ✅
task="打开 polymarket.com，找到 Fed 利率市场，提取 Yes/No 价格"

# 差 ❌
task="帮我看看那个市场"
```

### 2. 使用结构化输出

```python
from pydantic import BaseModel

class TradingResult(BaseModel):
    success: bool
    market: str
    action: str  # "buy_yes", "buy_no"
    amount: float
    price: float
    tx_hash: str | None

agent = Agent(
    task="执行交易...",
    output_model_schema=TradingResult,
)
```

### 3. 错误处理

```python
try:
    result = await agent.run()
except Exception as e:
    print(f"任务失败: {e}")
    # 可以使用 browser tool 作为后备
```

### 4. 复用登录态

```python
# 第一次登录后保存
# 后续直接加载，避免重复登录

browser_context = BrowserContextConfig(
    storage_state="~/.playwright-data/polymarket/auth.json"
)
```

## Token 消耗优化

### 对比（相同任务）

| 工具 | 平均 Token | 原因 |
|------|-----------|------|
| browser tool | ~5000-10000 | 每次快照全页面 |
| Playwright | ~1000-2000 | 需多次调试 |
| browser-use | ~2000-4000 | AI精简决策 |

### 优化技巧

1. **禁用视觉**：`use_vision=False`
2. **限制历史**：`max_history_items=10`
3. **压缩消息**：`message_compaction=True`
4. **减少步骤**：`max_actions_per_step=3`
5. **使用 Flash 模式**：`flash_mode=True`（快速模式）

## 完整示例

```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os

class MarketInfo(BaseModel):
    question: str
    yes_price: float
    no_price: float
    volume: str

async def check_polymarket():
    # 使用本地 LLM API
    llm = ChatOpenAI(
        model="claude-3-5-sonnet-20241022",
        base_url="https://cn.xingsuancode.com",
        api_key=os.environ.get("XSC_API_KEY"),
    )
    
    agent = Agent(
        task="""
        访问 Polymarket Fed 利率市场：
        https://polymarket.com/event/fed-decision-in-march-885
        
        提取并返回：
        - 市场问题
        - Yes 价格（0-1）
        - No 价格（0-1）
        - 24h 交易量
        """,
        llm=llm,
        output_model_schema=MarketInfo,
        use_vision=False,
        max_actions_per_step=5,
    )
    
    result = await agent.run()
    return result

if __name__ == "__main__":
    asyncio.run(check_polymarket())
```

## 资源

- 官方文档: https://docs.browser-use.com
- GitHub: https://github.com/browser-use/browser-use
- 示例: `~/clawd/skills/browser-use/examples/`

## 快速命令

```bash
# 安装（已完成）
pip install browser-use

# 运行脚本
python3 script.py

# 测试
python3 -c "from browser_use import Agent; print('✅ OK')"
```

---

**记住**: browser-use 让浏览器操作更智能，省去调试选择器的痛苦！🚀
