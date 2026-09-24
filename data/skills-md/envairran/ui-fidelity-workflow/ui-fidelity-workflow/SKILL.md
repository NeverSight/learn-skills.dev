---
name: ui-fidelity-workflow
description: Translate visual UI feedback into testable constraints, reproduce Figma or screenshot designs in an existing product, and diagnose persistent layout or motion defects without accumulating CSS patches. Use for high-fidelity implementation, scoped visual refinement, ambiguous UI feedback, or repeated unsuccessful UI fixes.
---

# UI Fidelity Workflow

将用户的视觉判断变成可验证的实现。还原包含外观、交互、动画过程、实际内容和既有功能。不要用另一套设计替换用户已确认的设计。

本 skill 是行为指导，不会训练模型权重，也不能保证任意截图的像素级复现。适用于不同产品与技术栈；浏览器例子在原生应用中应换成对应布局和动画工具。

## 确定任务与授权

- **只检查/给方案**：读证据、复现、提出最小方案，不修改产品代码或部署。
- **按稿还原/执行修改**：在已授权范围实现并验证，明确的需求不反复询问。
- **探索风格**：仅对指定范围探索，先做足够小的可评审样本，不自动重做整个产品。
- **部署**：按用户已有授权和项目流程进行；实现授权不自动包含发布、删除或重启。

先用一两句话说明理解、范围和关键验收点。简单改字无需完整审计。缺信息时，先做不依赖答案的检查。

## 将感觉转成验收约束

对复杂需求写下六项；简单任务可压成一句话：

1. 哪个页面、元素，从哪个状态触发。
2. 现在看到什么，证据来自截图、视频、运行页面还是代码。
3. 目标位置、尺寸、关系、路径或交互结果。
4. 哪些内容要保持，以及数据和后端边界。
5. 验证的设备、视口、滚动位置和内容。
6. 本轮是诊断、修改，还是也允许上线。

对影响方案的歧义，用直观语言问 1–3 个问题。例如：“收起时，下边缘要一直往上走，还是允许先停住再往上走？”不要让用户选 CSS 属性。可逆的小参数可以说明假设后继续；不同交互、产品含义或扩大范围则等待关键答案。

区分终点和全过程：结束时卡片变小，不代表过程中没有下坠。将要求写成可观察的关系，如 `正文可见底边 <= 按钮顶边 - 已确认间距`。动态测量见 [motion-and-layout.md](references/motion-and-layout.md)。

## 证据与实现

1. 确认当前运行版本、目标状态与设计来源。新近明确需求优先于旧文档；稿、截图、现网冲突时指出具体差异，不自行拼接。
2. 定位目标组件、直接父布局、实际生效样式与事件入口。只读本轮必要文件；有证据指向上层再扩大范围。
3. 先修结构、尺寸关系、字体和内容密度，再修材质和动效。缺字体、资源或目标设备时说明限制。
4. 在现有组件与状态管理中修改；减少同一职责的重复控制。不要默认追加 wrapper、样式补丁包、`!important` 或新依赖。
5. 验证本轮约束和直接相邻的已有行为。编译通过只说明编译通过；未经观察的效果写“待验证”。

## 按需读取参考

| 情况 | 读取 |
|---|---|
| Figma、截图还原、token/组件对应 | [figma-and-fidelity.md](references/figma-and-fidelity.md) |
| 审美反馈模糊、设计判断/风格探索 | [taste-and-clarification.md](references/taste-and-clarification.md) |
| 裁切、滚动、收起、玻璃渐隐、返回手势 | [motion-and-layout.md](references/motion-and-layout.md) |
| 反复修不好、CSS 冲突、怀疑旧包 | [debugging-and-cleanup.md](references/debugging-and-cleanup.md) |
| 视觉验收、交付、发布检查 | [verification.md](references/verification.md) |
| 经验来源和情境检验 | [cases-and-evaluation.md](references/cases-and-evaluation.md) |

不要默认读取所有参考。Figma、浏览器、视频工具都是可选能力；调用前遵守环境工具说明及适用技能，不虚构工具名或访问权限。

## 交付

说明实际改动、原因、验证结果和未验证项。诊断分清“已观察”“已证实根因”“候选原因”。让用户能从对照图、逐帧记录或复现步骤判断效果；避免未经定义的“还原度 99%”。

回滚是版本管理需求，不能靠旧构建永久包裹新构建来实现。清理只删除已确认失效且获授权的内容；保留必要变体、运行构建与指定回滚版本。
