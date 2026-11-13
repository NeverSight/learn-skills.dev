---
name: hyperframes-motion-library
description: 使用、扩展或调整栗噔噔的视频动效系统。适用于按口播脚本规划并批量生成参数化动效、统一整片画风、新增动效模板或迭代现有画风。
---

# 视频动效系统

这是由栗噔噔创建的 HyperFrames 参数化模板库。完整项目和样片以 [GitHub 仓库](https://github.com/nutllwhy/hyperframes-motion-library) 为准；本地运行 `npm install`、`npm run dev` 后，在终端显示的地址预览、编辑与渲染。

## 根据任务读取

- 选择动效或修改文案：先读 `catalog.json`、目标 `templates/<id>/index.html` 和对应预设。
- 根据口播规划一条视频：读 `director-rules.json`、`styles/catalog.json`、`motion-plan.schema.json` 和 `examples/motion-plan.example.json`，然后生成可导入批量工作台的方案。
- 新增或调整画风：读 `styles/README.md`、`styles/catalog.json`、`styles/runtime.css`、`styles/runtime.js`。画风要统一考虑字体、色板、材质、线条、构图与运动，实际以参考和用户审美为准，不仅调整色号。
- 新增模板或变更项目结构：读 `SYSTEM.md` 和 `AGENT_GUIDE.md`，并参考同类型模板。

## 关键约定

- `motion-plan.json` V1.2 的顶层 `styleId` 代表整片风格，场景默认继承；只有需要明确切换时才给场景指定 `styleId`。旧版方案仍可导入。
- `classic-orange` 保留黑橙默认风格；另有 `paper-editorial`、`sketch-notes` 和 `bold-geometry`。风格是可迭代的起点：根据用户提供的参考、审美反馈和视频语境改进设计。
- 文案、数字与必要图形必须服务内容；不要添加无来源数据、英文装饰标签或模板编号。独立画面使用合理的全屏构图；透明叠加保留适当的人物和字幕空间。
- 用户可选纯色 MP4 或透明 MOV / WebM。透明导出要保留透明通道，不让整帧背景变成不透明色块。
- `styles/runtime.css`、`styles/runtime.js`、`styles/catalog.json` 是统一风格源文件。模板中 `motion-style:start/end` 之间的代码由 `npm run sync:styles` 生成，不要手工维护。新增模板或风格后重新同步。
- 运行 `npm run check`；风格相关改动先启动 `npm run dev`，再运行 `npm run check:styles -- --screenshots`，对照大数字、图表、流程的实际画面，检查横竖屏、透明底及可读性。检查通过并不等同于审美已获用户认可。

## 继续迭代

先阅读相关源码和用户给出的参考，保留已有工作与预设；明确需要修改的是模板的信息结构、整片风格，还是两者。完成后提供本地体验地址、修改内容、实际验证结果及仍需用户评审的视觉取舍。
