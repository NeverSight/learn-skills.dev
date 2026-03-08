---
name: zhongkao-xiaosimen
description: 初中小四门（地理、历史、生物、道德与法治）练习题生成与知识点学习系统。根据人教版教材按年级、章节、知识点生成选择题、判断题、填空题、材料分析题，每题配套知识点卡片。Use when user asks to generate middle school geography, history, biology, or ethics practice questions, or requests knowledge point review for Chinese 中考 subjects.
---

# 初中小四门练习题与知识点系统

为初中生（七年级、八年级）生成地理、历史、生物、道德与法治四科的配套练习题和知识点学习材料。

## 快速开始

用户可通过以下方式触发：

| 触发方式 | 示例 |
|---------|------|
| 指定科目出题 | "出 10 道八年级地理选择题" |
| 指定章节出题 | "生物七年级上册第三单元练习题" |
| 知识点复习 | "总结八年级历史第一单元知识点" |
| 错题强化 | "针对洋务运动出 5 道易错题" |
| 综合测试 | "生成一份八年级上学期地理期中模拟卷" |
| 考前冲刺 | "中考道法必背知识点汇总" |
| 材料分析题 | "出 2 道八年级道法材料分析题" |

## 四科覆盖范围

### 地理（七年级 + 八年级）

| 年级 | 核心内容 | 教材参考 |
|------|---------|---------|
| 七上 | 地球与地图、陆地与海洋、天气与气候、居民与聚落 | [geo-7.md](references/geo-7.md) |
| 七下 | 亚洲、东南亚、印度、俄罗斯、中东、欧洲西部、撒哈拉以南非洲、澳大利亚、美国、巴西 | [geo-7.md](references/geo-7.md) |
| 八上 | 中国疆域与人口、中国自然环境、中国自然资源、中国经济发展 | [geo-8.md](references/geo-8.md) |
| 八下 | 四大地理区域、北方/南方/西北/青藏地区、省级行政区 | [geo-8.md](references/geo-8.md) |

### 历史（七年级 + 八年级）

| 年级 | 核心内容 | 教材参考 |
|------|---------|---------|
| 七上 | 中国古代史（史前—魏晋南北朝） | [hist-7.md](references/hist-7.md) |
| 七下 | 中国古代史（隋唐—明清） | [hist-7.md](references/hist-7.md) |
| 八上 | 中国近代史（鸦片战争—新中国成立前） | [hist-8.md](references/hist-8.md) |
| 八下 | 中国现代史（新中国成立—改革开放至今） | [hist-8.md](references/hist-8.md) |

### 生物（七年级 + 八年级）

| 年级 | 核心内容 | 教材参考 |
|------|---------|---------|
| 七上 | 生物与生物圈、细胞、生物圈中的绿色植物 | [bio-7.md](references/bio-7.md) |
| 七下 | 人体营养、呼吸、循环、排泄、神经调节、生殖发育 | [bio-7.md](references/bio-7.md) |
| 八上 | 动物的主要类群、动物的运动和行为、细菌真菌病毒 | [bio-8.md](references/bio-8.md) |
| 八下 | 生物的遗传和变异、生命的起源和进化、生态系统 | [bio-8.md](references/bio-8.md) |

### 道德与法治（七年级 + 八年级）

| 年级 | 核心内容 | 教材参考 |
|------|---------|---------|
| 七上 | 成长的节拍、友谊的天空、师长情谊、生命的思考 | [ethics-7.md](references/ethics-7.md) |
| 七下 | 青春时光、做情绪情感的主人、在集体中成长、走进法治天地 | [ethics-7.md](references/ethics-7.md) |
| 八上 | 走进社会生活、遵守社会规则、勇担社会责任、维护国家利益 | [ethics-8.md](references/ethics-8.md) |
| 八下 | 坚持宪法至上、理解权利义务、人民当家作主、崇尚法治精神 | [ethics-8.md](references/ethics-8.md) |

## 出题工作流

### Step 1: 确认参数

从用户请求中识别以下参数（未指定则用默认值）：

```yaml
subject: 地理|历史|生物|道法       # 必须
grade: 七年级|八年级               # 默认：八年级
semester: 上册|下册|全册           # 默认：全册
chapter: 具体单元/章节             # 默认：随机
count: 题目数量                   # 默认：10
difficulty: 基础|中等|拔高         # 默认：中等
types: [选择, 判断, 填空, 材料分析] # 默认：选择题
output: markdown|html              # 默认：html
```

### Step 2: 查阅教材知识点

根据科目和章节，读取对应的教材参考文件获取准确知识点：
- 地理：`references/geo-7.md` 或 `references/geo-8.md`
- 历史：`references/hist-7.md` 或 `references/hist-8.md`
- 生物：`references/bio-7.md` 或 `references/bio-8.md`
- 道法：`references/ethics-7.md` 或 `references/ethics-8.md`

**如果教材文件尚未填充内容**，则基于人教版课标知识体系生成题目，并在输出中标注"建议补充教材原文以提高精度"。

### Step 3: 按题型生成

遵循 [question-types.md](references/question-types.md) 中的题型模板生成题目。

**支持题型：**
- `choice`：选择题（4 选 1）
- `truefalse`：判断题（正确/错误）
- `fillblank`：填空题（文本输入）
- `material`：材料分析题（多小问 + 自评）

**题型混合规则：**
- 综合测试卷应包含多种题型
- 材料分析题通常放在试卷后半部分
- 默认情况下，如用户未指定题型，生成选择题 + 判断题混合

### Step 4: 选择输出格式

**默认输出为 HTML 交互页面**。根据 [html-template.md](references/html-template.md) 生成独立 HTML 文件，使用 Write 工具将文件写入项目的 `quiz-output/` 目录。

- 如果用户明确要求 Markdown 格式，则按下方 Markdown 模板输出
- 否则一律生成 HTML 交互练习页面

### HTML 生成关键架构

**数据与代码分离**：题目数据放在 `<script type="application/json" id="quiz-json">` 标签中作为纯 JSON，由 `JSON.parse()` 读取。**禁止**直接在 JavaScript 代码中拼写题目数据对象。

这样做的原因：
- JSON 转义规则简单（只需 `\"` 转义双引号）
- 浏览器内置 JSON 解析器处理，不会因引号问题报语法错误
- 中文内容中的各种引号、括号天然安全

**生成步骤**：
1. 阅读 [html-template.md](references/html-template.md) 中的完整 HTML 模板
2. 将题目数据组织为合法 JSON 填入 `<script id="quiz-json">` 标签
3. **每道题必须包含 `hints` 数组**（3级渐进提示），详见模板中的 hints 字段说明
4. 文本中的专有名词优先用中文引号「」包裹（无需转义）
5. 如果必须使用英文双引号，用 `\"` 转义
6. 使用 Write 工具将完整 HTML 写入文件

### HTML 交互页面功能

生成的 HTML 文件是**完全独立的单文件**，无需任何外部依赖，双击即可在浏览器中打开。

核心功能：
- **逐题作答**：每次显示一道题，选择答案后即时反馈
- **渐进式提示**：每题 3 级提示（方向提示→关键知识→解题思路），用提示会扣分，鼓励先独立思考
- **知识点卡片**：答对显示知识拓展，答错显示详细解析和易错提醒
- **进度追踪**：显示当前进度、正确率、连续答对数
- **成绩面板**：做完所有题后显示总分、薄弱知识点、错题汇总
- **错题回顾**：可重新练习答错的题目
- **计分与激励**：积分系统、连击奖励、成就动画
- **材料分析题**：支持多小问作答，显示参考答案和评分标准，学生自评（完全正确/部分正确/错误）
- **响应式设计**：手机/平板/电脑均可使用
- **中文界面**：全中文 UI，适合初中生使用

详细 HTML 结构和模板参见 [html-template.md](references/html-template.md)，游戏化机制参见 [gamification.md](references/gamification.md)。

### HTML 文件命名规范

```
quiz-output/{subject}-{grade}-{topic}-{timestamp}.html
```

> **⚠️ 文件名禁止包含空格！** 空格会导致 Markdown 链接和 URL 断裂。topic 中的空格必须替换为连字符 `-`。

示例：`quiz-output/geography-8-中国自然环境-20260225.html`

**命名规则**：
- 只允许使用：英文字母、数字、中文、连字符 `-`、句点 `.`
- **禁止**：空格、括号、引号、特殊符号
- topic 过长时适当缩短（控制在 10 个字以内）

### Step 5: 发布到 GitHub Pages（⚠️ 强制步骤，不可跳过）

> **⚠️ 本步骤为强制步骤，不是可选的。** 生成 HTML 文件后必须立即读取 [publish-quiz.md](scripts/publish-quiz.md) 并严格执行完整的发布流程。**禁止**生成 HTML 后直接结束对话而不执行发布。

HTML 文件生成后，**必须自动执行发布流程**（详见 [publish-quiz.md](scripts/publish-quiz.md)）：

1. **读取** [publish-quiz.md](scripts/publish-quiz.md) 获取仓库信息和完整操作步骤
2. 构造 GitHub Pages 在线链接：`https://xingyun-new.github.io/Skills-XiaoSiMen/quiz-output/{filename}`
3. 在项目根目录 `README.md` 的「在线练习」表格末尾追加新条目
4. 执行 `git add` → `git commit` → `git push origin main`
5. 向用户展示可直接访问的在线链接

**此步骤为默认行为**，每次生成 HTML 后自动执行，无需用户额外指示。如果 git 操作失败，向用户说明原因并提供手动操作指引。

## Markdown 输出格式（仅当用户指定 Markdown 时使用）

### 单题格式模板

```markdown
### 第X题（选择题 | 难度：★★☆）

**【题目】** XXXXX

A. XXX
B. XXX
C. XXX
D. XXX

**【答案】** B

**【知识点卡片】**
- 📚 考点：XXX
- 📖 出处：人教版X年级X册 第X单元
- 💡 关键记忆：一句话核心记忆点
- ⚠️ 易错提醒：常见错误及原因
- 🔗 关联知识：与之相关的其他考点
```

### 综合试卷格式

```markdown
# XX学科 X年级X学期 模拟测试卷

**总分：100分 | 时间：60分钟**

## 一、选择题（每题2分，共X分）
[题目...]

## 二、判断题（每题1分，共X分）
[题目...]

## 三、填空题（每空1分，共X分）
[题目...]

## 四、材料分析题（共X分）
[题目...]

---

## 参考答案与知识点解析
[逐题解析 + 知识点卡片]
```

## 教学方法论

本 skill 融合以下教学策略（详见 [teaching-methods.md](references/teaching-methods.md)）：

### 出题原则

| 原则 | 说明 |
|------|------|
| 知识覆盖 | 每组题尽量覆盖不同知识点，避免重复考查同一概念 |
| 梯度设计 | 基础→中等→拔高，先建立信心再提升挑战 |
| 干扰项质量 | 选择题的错误选项必须具有合理迷惑性，源自常见错误 |
| 素养导向 | 减少死记硬背，增加理解运用和材料分析 |
| 真题风格 | 贴近中考真题的命题风格和难度分布 |

### 知识点讲解原则

| 原则 | 说明 |
|------|------|
| 先理解后记忆 | 知识点卡片先解释"为什么"，再给出记忆方法 |
| 口诀助记 | 对适合的知识点提供记忆口诀或谐音联想 |
| 对比辨析 | 易混淆概念放在一起对比，突出区别 |
| 图表优先 | 地理读图题、生物结构图等优先用文字描述图示内容 |
| 错因分析 | 每个易错点说明"为什么会错"和"怎样避免" |

### 自适应学习（参考 Education Tutor 方法论）

**建构式教学**：从学生已有认知出发，逐步搭建新知识
- 先通过1-2道基础题检测已有水平
- 根据答题情况调整后续题目难度
- 错题自动归入薄弱知识点，后续重点强化

**间隔重复**：知识点在不同题目中反复出现
- 第1次：直接考查核心概念
- 第2次：变换情境再次考查
- 第3次：与其他知识点综合考查

**即时反馈**：每题做完立即查看解析
- 答对：强化记忆 + 拓展关联知识
- 答错：分析错因 + 提供正确理解路径 + 补充同类练习

## 特殊题型说明

### 地理读图题
用文字精确描述地图/图表内容，标注关键地理要素（经纬度、图例、比例尺等），引导学生从图中提取信息作答。

### 历史材料分析题
提供原始史料或改编材料，设置"材料反映了什么""结合所学知识分析原因/影响"等设问，考查史料解读和历史思维能力。

### 生物实验探究题
描述实验步骤和现象，考查变量控制、对照实验设计、结果分析等科学探究能力。

### 道法情境分析题
创设贴近初中生生活的情境（校园、家庭、社会），考查法律知识运用和价值判断能力。

## 参考资料

| 文件 | 内容 |
|------|------|
| [publish-quiz.md](scripts/publish-quiz.md) | **GitHub Pages 自动发布流程** |
| [html-template.md](references/html-template.md) | HTML 交互页面完整模板 |
| [gamification.md](references/gamification.md) | 游戏化积分与成就系统 |
| [teaching-methods.md](references/teaching-methods.md) | 完整教学方法论 |
| [question-types.md](references/question-types.md) | 各题型详细模板与示例 |
| [textbook-guide.md](references/textbook-guide.md) | 如何添加电子教材内容 |
| [geo-7.md](references/geo-7.md) / [geo-8.md](references/geo-8.md) | 地理教材知识点 |
| [hist-7.md](references/hist-7.md) / [hist-8.md](references/hist-8.md) | 历史教材知识点 |
| [bio-7.md](references/bio-7.md) / [bio-8.md](references/bio-8.md) | 生物教材知识点 |
| [ethics-7.md](references/ethics-7.md) / [ethics-8.md](references/ethics-8.md) | 道法教材知识点 |
