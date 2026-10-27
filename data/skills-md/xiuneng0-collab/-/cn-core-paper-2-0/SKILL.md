---
name: cn-core-paper-2-0
description: Write, restructure, refine, or pre-submit check Chinese core-journal papers, and guide Chinese-core publication experience plus graduate research growth. Use when the user wants help drafting or polishing a Chinese core paper, adapting to target journal style, organizing literature/evidence/figures/tables/formulas, creating or reviewing T1/T2/T3 Chinese-core engineering figures, reproducing high-quality paper diagrams and CNN module-style pipeline figures, reducing template-like writing, preparing submission, discussing successful Chinese-core publication experience, choosing a research direction, or judging whether supervisor communication, research-group support, senior-student mentoring, collaboration, equipment, consumables, testing schedules, and academic-integrity boundaries can support publication and graduation.
---

# 中文核心论文

直接把这项技能当成“中文核心论文写作、投稿经验与研究生成长总控模板”使用。

默认目标：

1. 先辨方向与支持系统，再进入写作。
2. 先建立文献坐标和证据链，再动语言。
3. 先保住数据口径，再改结构和表达。
4. 先让文章像正式期刊论文，再追求润色感。

## 最易上手用法

当用户只说“帮我改成中文核心风格”“按中文核心重写”“做投稿前精修”时，默认按下面顺序工作：

1. 先读 [references/07_最简使用指南.md](references/07_最简使用指南.md)。
2. 再读 [references/01_中文核心论文通用指令.md](references/01_中文核心论文通用指令.md)。
3. 需要重搭结构时读 [references/02_中文核心论文章节模板.md](references/02_中文核心论文章节模板.md)。
4. 需要总检时读 [references/03_中文核心论文投稿前检查清单.md](references/03_中文核心论文投稿前检查清单.md)。
5. 需要 Word、图表、公式规范时再按需读 `05` 和 `06`。
6. 需要顶级中文核心期刊绘图审美、T1/T2/T3 图件分层、工科图复现或 image2/深度研究配合画图时，读 [references/09_T1级工科绘图审美与复现规范.md](references/09_T1级工科绘图审美与复现规范.md)。
7. 需要给 GPT 制定修图建议、要求其继续优化现有图并生成仿真/重绘代码时，再读 [references/10_GPT修图与仿真代码协作模板.md](references/10_GPT修图与仿真代码协作模板.md)。

当用户问“中文核心成功投稿经验”“怎么发中文核心”“目标期刊怎么适配”“如何减少模板化表达”“科研工作流怎么搭”“文献综述工作流怎么生成”时，先读 [references/08_中文核心成功投稿经验.md](references/08_中文核心成功投稿经验.md)。

当用户问“科研迷茫”“研究方向怎么定”“导师或课题组怎么样”“实验条件会不会影响毕业/发文”“研究生科研怎么推进”时，也先读 [references/08_中文核心成功投稿经验.md](references/08_中文核心成功投稿经验.md)。

不要一上来把全部参考文件都塞进上下文。优先按任务读最少的文件。

## 绘图能力强化：CNN 模块结构图优先规范

当用户明确要求“复现那些图”“卷积神经网络结构图”“论文里的模块流水线图”“按深度研究建议继续改图”时，默认把 CNN 图当作本技能的高频重点样式，优先执行以下规则：

1. 先复现结构，不先发明风格。把输入图像、卷积块、池化块、全连接层、输出层、阶段箭头、图例、图题和重复次数全部锁定，再谈美化。
2. 采用白底、低饱和、论文插图气质，避免海报风、强渐变、重阴影、炫光和夸张 3D。
3. 用模块化分组框组织版面：每个 stage 用虚线圆角边界包住，顶部放模块名，底部放重复次数或阶段说明。
4. 以左到右流水线呈现“特征提取 -> 特征表示 -> 分类预测”，箭头方向清楚，图例放在底部统一解释。
5. 颜色只服务分组，不服务装饰。模块色相少而稳，黑白打印后仍需可读。
6. 内部文字保持短句，中文核心期刊风格优先于 PPT 风格，标题、图题和图例保持双语或与原图一致。
7. 优先 vector-first：系统图、拓扑图、模块结构图优先 SVG/PDF；PNG 仅作导出预览。
8. 如果用户给了参考截图，先把截图拆成版式、模块、箭头、图例、字体和层级，再开始重绘。

CNN 类图件默认交付为：

- 结构说明
- 可编辑矢量源
- 导出文件（SVG/PDF/PNG）
- assumptions
- 可直接复用的提示词

## 默认工作流

### 1. 先锁住不该改的东西

优先确认或从上下文提取：

1. 题目
2. 主线
3. 绝对不能改的数据口径
4. 目标期刊或目标风格

如果用户没有完整说出，也应先从当前稿件中推断，再在修改时保持一致。

### 2. 先判断用户要哪一类帮助

通常分为 8 类：

1. 从零搭稿
2. 章节重构
3. 中文核心风格精修
4. 图表公式与 Word 规范化
5. 投稿前总检查
6. 让大模型继续协作写稿
7. 中文核心投稿经验、科研工作流、期刊适配与研究生成长判断
8. T1/T2/T3 中文核心工科图件设计、复现与审美升级
9. GPT 修图建议、image2 边界控制、仿真/重绘代码协作交付

对应读取：

1. 从零搭稿：读 `02` + `07`
2. 重构精修：读 `01` + `02` + `03`
3. 图表公式：读 `06`
4. Word 排版：读 `05`
5. 提示词协作：读 `04`
6. 投稿经验、科研工作流、期刊适配与研究方向支持系统：读 `08`
7. 工科图件设计、复现、审美升级：读 `06` + `09`
8. GPT 修图和仿真代码协作：读 `06` + `09` + `10`

## 硬性写作原则

处理中文核心工程论文时，默认遵守以下规则：

1. 不把论文写成项目汇报。
2. 不把论文写成版本流水账。
3. 不夸大创新性，不写“首次提出”“显著优于”之类高风险表述，除非用户提供明确证据并要求保留。
4. 不把配置推导、理论计算、归档核算写成外部仪器实测。
5. 结论里尽量保留关键参数，而不是空泛收尾。
6. 摘要、结论、图题、表题、术语、单位必须前后一致。

## 语言风格默认值

默认采用“中文核心工程期刊”表达，而不是：

1. PPT 讲稿风
2. AI 综述风
3. 项目申报书风
4. 口号式宣传风

优先使用：

1. `结果表明`
2. `由此可见`
3. `该结果说明`
4. `在该配置下`
5. `该设计主要用于`
6. `与参数分析一致`

尽量删除：

1. `具有重要意义`
2. `显著提升`
3. `充分证明`
4. `广阔应用前景`
5. `提供了一种新思路`
6. `效果良好`

## 输出时的默认组织方式

除非用户只要求局部润色，否则优先按下面方式输出结果：

1. 先给修改后的正文或改稿成品。
2. 再简要说明改了哪些关键点。
3. 明确哪些数据口径被保留不动。
4. 如果仍有风险，指出具体残留项，例如功耗未实测、采样率仅为核算一致性等。

不要只给泛泛建议而不落地修改。

## 参考文件说明

### 必读入口

- [references/07_最简使用指南.md](references/07_最简使用指南.md)
作用：最快理解这套模板该怎么用。

### 总控规则

- [references/01_中文核心论文通用指令.md](references/01_中文核心论文通用指令.md)
作用：统一主线、语言、边界和期刊化风格。

### 结构模板

- [references/02_中文核心论文章节模板.md](references/02_中文核心论文章节模板.md)
作用：搭文章骨架，避免写成流水账。

### 总检查

- [references/03_中文核心论文投稿前检查清单.md](references/03_中文核心论文投稿前检查清单.md)
作用：投稿前逐项排雷。

### 提示词协作

- [references/04_大模型写作提示词模板.md](references/04_大模型写作提示词模板.md)
作用：当需要让其他模型继续协作写稿、改稿时使用。

### Word 规范

- [references/05_中文核心论文Word排版模板说明.md](references/05_中文核心论文Word排版模板说明.md)
作用：Word 终稿排版、版式和对象化细节。

### 图表公式

- [references/06_中文核心图表公式细则.md](references/06_中文核心图表公式细则.md)
作用：三线表、图题表题、公式对象、单位和图表口径统一。

### T1 级工科绘图审美

- [references/09_T1级工科绘图审美与复现规范.md](references/09_T1级工科绘图审美与复现规范.md)
作用：把图件按 T1/T2/T3 中文核心目标分层，指导系统图、拓扑图、机构图、传感器原理图、标定曲线、显式 MPC 分区图、谱相干图、工艺流程图等高水平工科图的重绘、审美升级和可复现交付。

### GPT 修图与仿真代码协作

- [references/10_GPT修图与仿真代码协作模板.md](references/10_GPT修图与仿真代码协作模板.md)
作用：把“给 GPT 修图建议”升级为可执行任务书，要求同时交付结构保真建议、仿真/重绘代码、数据文件、SVG/PDF/PNG 和 assumptions，尤其适合把 deep research、image2 与中文核心 T1 工科图件工作流结合。

### 投稿经验

- [references/08_中文核心成功投稿经验.md](references/08_中文核心成功投稿经验.md)
作用：把中文核心投稿理解为研究方向、科研支持系统、工作流生成、文献定位、证据组织、期刊适配和反复修订的综合训练。

## 一句话默认策略

先辨方向与支持系统，再建文献和证据链，后修语言，最后做图表公式和投稿前总检。
