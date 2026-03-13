---
name: browser-use
description: 用 Browser-Use 做复杂网页自动化（多步骤登录、填表、发帖、数据抓取）。当内置 browser tool（snapshot→act）搞不定时用这个——它是专门的浏览器AI agent，一个task丢进去自主完成全流程。触发词：browser-use、浏览器自动化、自动登录、自动填表、自动发帖、网页操控、复杂网页操作。
---

# Browser-Use 浏览器自动化

## 何时用 Browser-Use vs 内置 browser tool

| 场景 | 内置 tool | Browser-Use |
|------|:-:|:-:|
| 截图/看页面/点一个按钮 | ✅ 免费快 | ❌ 杀鸡用牛刀 |
| 5步以上流程（登录→导航→填表→提交） | ❌ 容易断 | ✅ |
| 需要反检测（真Chrome） | ❌ | ✅ |
| 批量重复操作 | ❌ | ✅ |

**代价**：Browser-Use 每步调一次外部 LLM（花钱+慢），简单操作用内置 tool。

## 执行流程

### 1. 检查环境
```bash
test -d ~/browser-use-env && echo "已安装" || echo "需要安装"
```

### 2. 首次安装（仅一次）
```bash
python3 -m venv ~/browser-use-env
source ~/browser-use-env/bin/activate
pip install browser-use playwright langchain-openai
playwright install chromium
```

### 3. 决定模式
- **简单场景 / 不怕被检测**：用内置 Chromium（模式A），直接跑
- **需要反检测 / 用户已有登录态**：连真 Chrome（模式B），需用户配合

模式B前置步骤——提示用户：
> 请先完全退出 Chrome（Mac: Cmd+Q），然后告诉我"关了"

用户确认后执行：
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
# Windows: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
# Linux: google-chrome --remote-debugging-port=9222 &
```
验证：`curl -s http://127.0.0.1:9222/json/version`

### 4. 写脚本并运行
脚本写到用户 workspace 下，然后：
```bash
source ~/browser-use-env/bin/activate
python3 脚本路径.py
```

### 5. 反馈结果
运行完把结果发给用户，失败则按故障决策树处理。

## 脚本模板

```python
import asyncio
from browser_use import Agent, ChatOpenAI, Browser

async def main():
    # LLM — 任何 OpenAI 兼容 API 均可
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key="<YOUR_API_KEY>",
        base_url="https://api.openai.com/v1",  # 或其他兼容端点
    )

    # 模式A: 内置 Chromium
    browser = Browser(headless=False, user_data_dir="~/.browser-use/任务名-profile")
    # 模式B: 连真 Chrome
    # browser = Browser(cdp_url="http://127.0.0.1:9222")

    agent = Agent(
        task="详细的任务描述（见下方写法指南）",
        llm=llm,
        browser=browser,
        use_vision=True,
        max_steps=25,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Task 写法指南（关键！）

### ✅ 好的写法：具体分步
```python
task = """
1. 打开 https://www.reddit.com/login
2. 输入用户名: x_user
3. 输入密码: x_pass
4. 点击登录按钮
5. 如果遇到 CAPTCHA，等待30秒让用户手动完成
6. 登录成功后，导航到 https://www.reddit.com/r/xxx/submit
7. 在标题框输入: xxx
8. 在正文框输入: xxx
9. 点击发布按钮
"""
```

### ❌ 坏的写法：模糊笼统
```python
task = "去Reddit发个帖子"
```

### 进阶技巧
- **键盘导航兜底**：task里加 "如果按钮点不了，用 Tab+Enter 键盘导航"
- **错误恢复**：加 "如果页面加载失败，刷新重试"
- **敏感数据**：用占位符 + `sensitive_data` 参数，密码不暴露给LLM

## 敏感数据处理

```python
agent = Agent(
    task="登录网站，用户名 x_user，密码 x_pass",
    sensitive_data={"x_user": "真实用户名", "x_pass": "真实密码"},
    use_vision=False,  # 关闭截图防止LLM看到密码
    llm=llm, browser=browser,
)
```

## 关键参数速查

| 参数 | 说明 | 推荐 |
|------|------|------|
| `use_vision` | AI看截图 | 一般True，有密码时False |
| `max_steps` | 最大步数 | 20-30 |
| `max_failures` | 最大重试 | 3（默认） |
| `flash_mode` | 快速模式（跳过思考） | 简单任务True |
| `extend_system_message` | 追加系统提示 | 加特定指令 |
| `allowed_domains` | 限制访问域名 | 安全场景用 |
| `fallback_llm` | 备用LLM | 主LLM不稳时设 |

## 故障决策树

```
被网站检测为自动化？
  └→ 换模式B连真Chrome

CAPTCHA人机验证？
  └→ 提示用户手动完成，task里写等待时间

LLM调用超时？
  └→ 设 fallback_llm 或换更快的模型

操作了但没效果（如帖子没发出）？
  └→ 1. 检查是否被平台反垃圾拦截（新账号常见）
     2. task里加更具体的确认步骤

网站UI变化导致找不到元素？
  └→ Browser-Use能自适应，但可在task里加备选路径
```

## LLM兼容性

| LLM | 兼容 | 备注 |
|-----|:---:|------|
| GPT-4o / 4o-mini | ✅ | 最佳，推荐 |
| Claude | ✅ | 好用 |
| Gemini | ❌ | 结构化输出不兼容 |
