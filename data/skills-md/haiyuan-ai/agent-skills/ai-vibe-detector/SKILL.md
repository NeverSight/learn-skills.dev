---
name: ai-vibe-detector
description: >-
  分析文本中的 AI 风格信号、误判风险和自然化改写方向。支持文本或 URL 输入。触发词：AI 味/去 AI 味/改得像人写的/是否像 AI 写的/朱雀检测。Analyze text for AI-style signals, humanize wording, assess detector risk. Not for bypassing detectors.
---

# AI Vibe Detector

分析文本中的 AI 风格信号、AI 润色痕迹、误判风险，并提供自然化改写建议。

## When to Use This Skill

Trigger this skill when the user:
- 要求检查文本是否像 AI 写的
- 问“这篇文章 AI 味重吗”
- 需要去 AI 化或改得更自然
- 想知道某段文字会不会被 AI 检测器误伤
- 提到”朱雀检测””AI 检测风险”等平台或检测场景
- 提供了一个 URL，要求分析该文章的 AI 味

Do not frame the task as:
- 保证通过 AI 检测
- 绕过、欺骗、击败某个检测器
- 证明文本一定是 AI 或一定是人写

## Core Workflow

### 0. Input Handling

如果用户提供的是 URL 而非文本：
1. 使用当前环境中可用的网页抓取能力获取页面内容
2. 如果首次抓取失败（反爬拦截、验证页面、内容为空），检查当前环境中是否有其他可用的抓取工具或技能（如专门的网页内容提取、浏览器自动化等），尝试用替代方式获取
3. 提取正文部分（忽略导航、侧栏、广告等非正文内容）
4. 如果所有抓取方式均失败，提示用户手动粘贴文章内容
5. 将提取的正文作为待分析文本，进入下面的分析流程

### 1. Analysis Steps

1. 获取待分析文本，先区分正文、引用、代码、命令、提示词和模板内容。
2. 判断文本类型：
- 叙述 / 观点文
- 技术说明 / 文档
- 公告 / 营销文
- 学术 / 正式写作
- 混合内容
3. 从四层信号分析文本：
- 高置信结构信号
- 中置信语言信号
- 低置信平台启发式
- 反误判信号
4. 输出结论标签、置信度、误判风险，而不是只给一个总分。
5. 如果用户要求改写，优先做“降低模板感、增加具体性、保留原意”的自然化修改。

## Output Format

Use this output structure by default:

```text
（如有 3+ 段落，先输出分段分析，见下方 Paragraph-Level Analysis）

结论：更像 AI 风格化写作 / 更像 AI 润色痕迹 / 更像人工原生写作 / 证据不足
置信度：低 / 中 / 高
误判风险：低 / 中 / 高

主要依据：
1. ...
2. ...
3. ...

反误判因素：
1. ...
2. ...

如果要改：
- 优先改 🔴 段落（如有分段分析）
- 为什么这些位置最像模板化表达
- 给 1-3 个局部改写示例
```

### Paragraph-Level Analysis

When text has 3+ paragraphs, or when the user requests detailed analysis, add per-paragraph breakdown:

```text
分段分析：
🔴 高 | 第3段：总而言之，人工智能技术的快速发展为各行各业带来了...
       → 触发：模板化开头 + 空泛总结 + 连接词密度高
🟡 中 | 第1段：最近在搞一个 side project，用 Claude 帮我写了...
       → 触发：情绪过稳、段落收束句
🟢 低 | 第2段：上周三凌晨三点，服务器炸了，我翻了半小时日志...
       → 具体细节多，节奏自然
```

Place this before the overall conclusion. Rewrite suggestions should target 🔴 paragraphs first.

If the user explicitly wants a score, use a secondary score only:
- `AI 风格风险：0-10`
- Always pair it with confidence and false-positive risk
- Never present the score as proof of authorship

## Analysis Framework

### 1. High-Confidence Structural Signals

Look for:
- 模板化开头和结尾反复出现
- 段落长度和节奏异常均匀
- “定义 -> 展开 -> 总结”结构过于稳定
- 每段都像完成一个标准小节，没有自然跳跃
- 大量总结句、收束句、过度照顾读者理解

These signals are stronger when they appear together.

### 2. Medium-Confidence Language Signals

Look for:
- 连接词密度偏高
- 空泛抽象名词偏多，具体信息偏少
- 情绪过稳、判断过平滑
- 同义改写很多，但真实信息增量很少
- 明显“像在写一篇合格答案”而不是“像在表达一个具体的人”

### 3. Low-Confidence Platform Heuristics

These can raise detector risk but are not reliable authorship evidence:
- 序号、列表、括号、破折号
- 段末标点高度一致
- 某些连接词或总结词
- 口语化不足或过度工整

Use these only as weak indicators.

### 4. False-Positive Protection

Before calling something “AI 味重”, check whether the style is explained by:
- 技术文档、SOP、教程、FAQ
- 学术 / 公文 / 正式说明文体
- 引用、法规、公告、品牌规范
- 代码、命令、表格、清单
- 用户给模型的 prompt，而不是最终成文
- 人写后被工具轻度润色，而不是纯 AI 生成
- 翻译文本（措辞均匀、缺乏口语痕迹是翻译的正常特征，不等于 AI 生成）

## Decision Labels

Prefer one of these labels:

### 更像人工原生写作
- 有真实选择痕迹
- 有非模板化取舍
- 具体细节和节奏变化自然

### 更像 AI 风格化写作
- 模板感强
- 结构和语气过稳
- 抽象总结多于具体经验

### 更像 AI 润色痕迹
- 原始观点可能是人的
- 但措辞被统一抛光、平滑、标准化
- 常见于“人写初稿 + AI 改顺”场景

### 证据不足
- 文本太短
- 类型本身高度模板化
- 引用/代码/清单占比太高

## Zhuque and Similar Detector Risk

When the user mentions 朱雀或类似检测器:
- Explain that these tools often react to highly regular structure, overused transitions, and polished-but-generic prose
- Treat platform-specific rules as heuristics, not facts
- Do not say “这样改就一定能过”
- Say “可能降低被判为模板化写作的风险”，not “保证通过检测”

For this case, add:
- 平台风险信号
- 误判风险
- 更稳妥的自然化建议

## Rewrite Guidance

If the user asks to humanize the text:
- 如有分段分析结果，优先改写 🔴 高风险段落
- 优先删”空泛总结”和”万能连接词”
- 保留原文观点，不靠随机口语词堆砌
- 增加可验证的细节、具体对象、具体动作
- 允许节奏不完全对称
- 局部加入真实视角，但不要凭空捏造经历

Avoid:
- 强行加“我觉得”“说真的”“绝了”之类口头禅
- 为了“像人”故意制造病句
- 凭空添加个人经历、时间、地点
- 面向某个检测器定向调参式改写

## Resources

Use references selectively:
- `references/official-detector-landscape.md` - Official product positioning and limits of major AI detectors
- `references/research-limitations.md` - Research consensus on detector limits and false positives
- `references/platform-heuristics.md` - Practical but weak platform-specific heuristics
- `references/wikipedia-ai-features.md` - Legacy style-signal checklist
- `references/zhuque-detection.md` - Legacy Zhuque-oriented heuristics, use cautiously

## Output Principles

1. 不把风格信号说成作者身份证明
2. 不承诺通过任何检测器
3. 先讲证据，再讲结论
4. 必须给误判风险提示
5. 自然化改写优先“减模板感”，不是“演人设”
6. 不提供面向特定检测器的定向规避建议
