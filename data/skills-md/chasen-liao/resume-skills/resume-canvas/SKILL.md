---
name: resume-canvas
description: 指导与驱动 resume-canvas (本地 HTML 简历可视化微调编辑器) 的运行、编辑协议验证、文本与排版微调以及保存后的事实重验闭环。当用户需要预览视觉简历、进行文字小修小补、排版微调（字号/间距/颜色/页边距）、启动本地编辑器或排查编辑协议时使用。
---

# 简历 Canvas 微调器 (resume-canvas)

专职负责已生成的独立视觉 HTML 简历的本地可视化微调、编辑协议检验与保存重验闭环。

## 定位与协作入口

- **角色定位**：AI 生成视觉简历后的“最后小修小补”工具。提供所见即所得的本地 Web 界面，供用户快速修正错别字、微调字号、字重、颜色、对齐、行高、段后距与页边距。
- **职责边界**：
  - **允许**：编辑已有字段的纯文本，调整受限排版样式。
  - **禁止**：不用于经历采访与生成、无中生有编造事实、JD 匹配分析、结构重排、插入任意 HTML 或图片编辑。
  - **模式限制**：仅适用于 6 套内置视觉模板（`modern-minimal`、`classic-business`、`creative-bold`、`japanese-minimal`、`minimal-blue-business`、`tech-dark`）。**ATS-safe 模式不使用 Canvas**（单栏纯文本结构无需也未接入编辑协议）。
- **上游来源**：
  - `resume-builder`：生成母版视觉 HTML 且完成初始 PDF 渲染验证后，若用户需要微调排版或文字，路由至本技能。
  - `jd-tailorer`：生成岗位定制版视觉 HTML 且完成初始 PDF 渲染验证后，若用户需要微调，路由至本技能。
  - `resume-workflow`：完整编排工作流在交付阶段按需调用本技能。

---

## 核心工作流

首次执行校验或保存后重验前，读取 [渲染环境与命令路径](../resume-builder/references/runtime-setup.md)。Canvas CLI 可独立启动，保存后的 PDF/截图重验则需要完整运行时；使用实际脚本和私有产物的绝对路径。

### 第一步：验收编辑协议契约

在启动 Canvas 或交付视觉 HTML 之前，必须确保目标 HTML 符合编辑字段协议：

1. **协议根标记**：
   `<html>` 根节点必须声明：
   - `data-resume-editor-template="<模板标识>"`（如 `modern-minimal` 等）
   - `data-resume-editor-version="1"`
   - `data-resume-layout="full-page"`
2. **字段独立性要求**：
   - 字段总数必须大于 0；
   - 必须使用唯一、小写、语义化的 `data-resume-editor-id`（例如 `profile-name`、`experience-1-title`、`experience-1-bullet-1`、`skill-1` 等）；
   - **可独立编辑原则**：`data-resume-editor-id` 只能标在具体的叶子文本元素上；
   - **禁止把编辑 ID 放在容器上**：禁止把 ID 放在 `<html>`、`<body>`、`<main>`、`.page`、`.resume`、`header`、`footer`、`section`、`ul`、`ol`、`figure` 或包含多个板块/复合内容的容器上，严禁使用整页兜底 ID。带链接的复合联系方式需将文本拆分为独立字段。
3. **执行静态校验（门禁命令）**：
   ```bash
   npx -p @chasen-liao/resume-skills@latest resume-skills validate "<最终_visual.html路径>"
   ```
   - 重复执行直到输出“校验通过”；
   - 若出现错误（缺少协议版本、缺少模板名、存在容器 ID、重复 ID 等），必须对照报错节点在 HTML 中修复，严禁在校验未通过时启动 Canvas。

---

### 第二步：启动本地编辑器

校验通过后，调用 CLI 启动本地服务：

```bash
npx -p @chasen-liao/resume-skills@latest resume-skills editor "<最终_visual.html路径>" --manifest "<交付目录/自定义文件名.resume-manifest.json>"
```

#### CLI 参数与运行模式说明

- `--manifest <path>`：显式关联验证清单文件。当用户在 Canvas 中保存时，该 manifest 会被自动置为失效，保障产物真实性。
- `--json`：NDJSON 流式输出机器可读事件（`server_started`、`error`、`update_available`、`validation_passed`）。适合 Agent 后台集成或自动化流水线，脚本逐行 `JSON.parse`。
- `--no-open`：禁止自动拉起系统默认浏览器。适合无 GUI 环境、远程 SSH 容器或开发者自行手动打开网页。
- `--port <number>`：显式指定服务端口（严格模式，若端口被占用直接报错；未指定时默认从 8848 尝试顺延至 8853，仍被占用则使用随机端口）。

#### 环境降级与异常处理

若当前执行环境缺少 Node.js（`< 20`）或无法执行 `npx` 命令：
- **必须明确报告未启动**：严禁向用户虚假声称“已在后台打开编辑器”；
- **提供完整命令**：向用户输出包含其实际 HTML 路径的完整命令，提示用户在其本机终端中手动执行启动：
  ```bash
  npx -p @chasen-liao/resume-skills@latest resume-skills editor "<实际生成的_visual.html绝对路径>"
  ```

---

### 第三步：交互协同与 Live Preview

1. **界面交互指引**：
   - **中间画布**：单选选中字段可直接打字编辑（纯文本），双击同样可编辑；支持 `Tab`/方向键切换字段焦点，`Ctrl/Cmd+Enter` 确认，`Esc` 撤销。
   - **右侧面板**：选中具体字段后可调整字号、字重、颜色、行高、段后间距；可调整页面边距与全局主题色。
   - **左侧状态**：实时显示 A4 页面垂直溢出与高度占用指示。
2. **Live Preview 热重载**：
   - 编辑器通过 SSE 与本地服务保持长连接；
   - 当 Agent 在后台根据用户反馈修改并重新保存该 HTML 时，前端画布会自动触发热重载刷新最新内容，用户无需手动刷新页面。

---

### 第四步：保存与重验闭环（强制关键防线）

当用户在编辑器中完成修改并点击“**保存修改**”后：

1. **状态变化**：
   - 编辑器将修改原子写回源 HTML，并自动将关联的 `*.resume-manifest.json` 状态置为失效（`invalidated`）；
   - 旧的 PDF 不再匹配当前最新的 HTML 内容。
2. **必须回到 Agent 工作流执行重验闭环**：
   - **事实核验**：检查 HTML 中的修改内容是否涉及关键经历、时间、职位、数据或技能。若发现未经确认的新事实，必须向用户核实，不可直接交付；
   - **重新渲染与验证 PDF**：
     必须重新执行渲染与验证脚本，生成有效的新 PDF 与 manifest：
     ```bash
     powershell -NoProfile -ExecutionPolicy Bypass -File skills/resume-builder/scripts/render_resume.ps1 -HTML "<最终_visual.html路径>" -OutputPdf "<交付目录/自定义文件名.pdf>"
     ```
   - **整页截图视觉复核**：AI 必须打开重新渲染生成的整页截图，按 [整页截图视觉复核](../resume-builder/SKILL.md#整页截图视觉复核视觉模式强制执行) 检查底部留白、上下平衡、板块间空隙和双栏各栏分布。明显底部空缺或留白失衡时，即使自动校验通过也不得交付；在 Canvas 支持的排版项内调整后重新渲染、校验并查看新截图。若需要结构重排，回到 `resume-builder` 或 `jd-tailorer` 处理，不扩展 Canvas 的编辑边界。
   - 确认 PDF 页数恰好为 1 页，有效利用率 ≥ 98%，manifest 为有效状态，且 AI 已实际看图确认留白均匀后，微调闭环才算完成。无法查看截图时必须说明视觉复核未完成。

---

## 协作出口与下游路由

- **微调完成并重新验证后**：交付最终的视觉 HTML、PDF 及 manifest。
- **区分母版与定制版后续流转**：
  - **若微调的是母版简历**：微调并重验通过后作为最新母版；后续若需针对新目标岗位投递，以母版事实为基准**路由至 `jd-tailorer`**。
  - **若微调的是岗位定制版简历**：仅作为当前特定公司/岗位的独立交付物（保存在 `tailored/<公司名>-<岗位>/` 目录下），**严禁将已定制版直接作为新母版去派生其他岗位**；投递其他岗位必须回到唯一母版事实。
  - **版本归档**：无论母版还是定制版，微调定稿并重验通过后，更新对应版本的 `version-notes.md` 并建议用户在本地私有 Git 仓库完成语义化提交，不自动执行 Git 提交。
