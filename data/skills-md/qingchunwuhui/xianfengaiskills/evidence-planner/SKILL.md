---
name: evidence-planner
description: |
  生成技术实战、排错或开发任务的“证据分镜表”(Evidence Shot List)，指导精准留证。
  适用于用户准备开始复杂任务（如Debug、环境搭建）需要规划截图时，或用户提及 /shotlist, /plan, 分镜表, 截图清单 时触发。
---

# Evidence Planner (实战分镜规划师)

## 1. 核心目标 (Core Goal)
解决实战中“不知道该截什么图”以及“事后忘记截图”的痛点。
通过预判任务类型，在行动开始前生成一份包含“Must-Have”和“Nice-to-Have”的关键证据 Checkbox 清单。用户在实战过程中只需对照清单“填空”，从而在保持心流的同时完成高质量留证。

## 2. 触发时机 (Triggers)
- 用户输入关键词：`/shotlist`, `/plan`, `分镜表`, `截图清单`。
- 用户准备开始一个复杂的 Debug、功能开发或环境搭建任务时。

## 3. 输入规范 (Input Specification)
为了生成最精准的分镜表，请提供以下四要素：
1. **任务类型 (Action)**: 如排查、部署、优化、重构。
2. **技术栈 (Tech Stack)**: 如 React, Docker, Kubernetes, Webpack。
3. **环境/上下文 (Context)**: 如 "内网生产环境", "iOS Safari浏览器", "VSCode Remote插件"。
4. **具体症状/目标 (Specifics)**: 如 "内存泄漏", "白屏", "API 502错误"。

> **✅ 黄金Prompt公式**: `Action + Stack + Context + Specifics`
> **例子**: "我要排查(Action) Linux服务器上(Context) Docker容器(Stack) 频繁OOM重启的问题(Specifics)"

## 4. 执行流程 (Workflow)

### Step 1: 任务嗅探 (Task Sniffing)
分析用户的任务描述，确定任务场景（Bug排查、环境配置、代码重构、性能优化等）。

### Step 2: 生成分镜表 (Generation)
基于场景生成结构化清单。
> 💡 **模板资源**: 详细的通用模板和各场景示例（Debug、部署、前后端联调）请查阅 [templates.md](references/templates.md)。

**核心原则**:
1.  **Must-Have (核心证据)**: 缺失将导致无法复盘的证据（如报错堆栈、关键配置）。
2.  **Nice-to-Have (辅助证据)**: 丰富上下文的证据（如资源占用、依赖树）。

### Step 3: 根据内容输出 (Action)
1.  **检查上下文**: 
    *   查看 `Active Document` 是否为相关的实战记录/复盘笔记文件。
    *   确认用户是否指定了保存路径（默认知识库路径：`e:\OBData\ObsidianDatas\0收集箱日清\`）。

2.  **执行动作 (Execute)**:
    *   **Scenario A: 插入活跃文档 (Insert)**
        *   若有活跃实战文档，使用代码编辑工具将分镜表插入到文档的开头或“准备阶段”章节。
    *   **Scenario B: 新建知识库文档 (Create)** 
        *   若无活跃文档或用户明确要求保存，则在知识库中创建新文件。
        *   **命名规范**: `{YYYY-MM-DD}-实战分镜-{TaskSkeleton}.md` (例如: `2024-03-21-实战分镜-Ubuntu服务器配置Clash.md`)
        *   **保存位置**: 用户指定的目录 或 `e:\OBData\ObsidianDatas\0收集箱日清\`。
        *   **工具**: 使用 `write_to_file` 工具写入完整的 Markdown 内容。
    *   **Scenario C: 仅输出预览 (Preview)**
        *   若用户明确仅需查看，直接在聊天窗口输出 Markdown 内容。

## 5. 最佳实践 (Best Practices)
- **宁缺毋滥**: Must-Have 最好控制在 3-5 项，避免给用户造成心理负担。
- **指令具体**: 避免说“截图代码”，要说“截图 `main.js` 中第 15-20 行的异常捕获逻辑”。
- **标记建议**: 建议用户使用截图工具（如 Snipaste/ShareX）的高亮功能（红框/箭头）标注重点。
