---
name: remove-model-cliche
description: This skill guides the agent in identifying and replacing AI model-specific cliches and formulaic expressions with more natural, human-like language, grounded in external search for better alternatives.
author: github/cafe3310
license: Apache-2.0
---

# remove-model-cliche Skill

## 描述
此技能旨在帮助 Gemini Agent 识别并移除文本中常见的、由大型语言模型滥用而形成的刻板印象和套路化表达（即「模型味」），使其行文更自然。

## 目标

你负责将 AI 生成的文本进行风格优化，核心任务是消除文本中的模型味儿或 AI 机器感。保持原文的核心信息和大致长度不变。你的工作是风格上的改写，而不是内容上的缩写或摘要。

## 基本建议

以下内容需要作为基础建议执行。

语气与态度：
* 避免不切实际或过度奉承的赞美，保持客观、中立自然的口吻。禁止浮夸表达。
* 仅在极其贴切且必要时才使用比喻，删除大部分无必要性比喻。
* 少用 passive voice。

修辞和用语：
* 避免 model-speak：减少 discourse markers 和 metadiscourse，如「说白了，…」「总之，…」「别…」「真正的…」的使用。
* 合理减少「的」「了」的使用。合理使用和省略代词与被指代对象。
* 尽量少用 parenthetical gloss。整体上减少 glossing。

句式和逻辑：
* 减少英文书面语气：减少多从句连接式叙述。
* 减少学院 essay 风格：避免完美的逻辑推理链条，可以稍微跳跃点，甚至先下结论然后补逻辑。

标点使用：
* 不要生硬使用破折号、引号、冒号。禁用 scare quotes。
* 使用方引号「」而非弯引号。

标题与格式：
* 不要用 two-part title。
* 避免 listicle style。
* 避免滥用 markdown 格式：极度谨慎使用标题和列表，多用流畅的文段表达。

## 工作流

当用户指示进行文风订正以去除「模型味」时，遵循以下迭代流程：

1.  复述上述「基本建议」，告知用户接下来要做出的编辑，等待用户确认编辑。写到新的文件而不是原始文件。
2. 编辑后，询问用户是否要搜索并移除当前互联网上搜到的模型刻板用词。如果是，则做个 web_search，搜索这些刻板用词，给用户看一下文章中包含的这些表达。用户确认后，基于 1 的输出文件，做个替换，换成更自然的形式。写到另一个新的文件而不是原始文件。

仅需要进行一轮搜索，了解当前流行的模型刻板表达即可。不用反复搜索以寻求每个细节的替换建议。
