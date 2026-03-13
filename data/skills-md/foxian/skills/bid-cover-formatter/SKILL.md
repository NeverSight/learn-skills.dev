---
name: bid-cover-formatter
description: Format tender/bidding document covers from Markdown to HTML-styled Markdown. Use when converting Chinese document covers (招标文件/投标文件/报价文件/商务文件/技术文件/技术协议/采购文件) to formatted output with Chinese fonts (黑体/宋体), pt-based spacing, center alignment, and proper layout for A4 printing.
license: Complete terms in LICENSE.txt
---

# 招投标书封面格式化技能

## 技能目的

将招投标书封面 Markdown 内容转换为符合打印规范的 Markdown 格式（使用 HTML 标签表示样式），便于后续转换为 Word 文档。

## 适用场景

识别以下类型文档为封面：

- 标题包含"招标文件"、"投标文件"、"报价文件"、"商务文件"、"技术文件"、"技术协议"、"采购文件"等关键词
- 内容结构符合封面特征（公司信息、项目信息、招标人/报价人/投标人信息等）

---

## 核心要求

### 1. 封面识别规则

**识别信号**：以下任一条件满足即视为封面

- 标题行包含：报价文件、商务文件、技术文件、技术协议、采购文件
- 内容包含：报价人、投标人等信息
- 结构特征：顶部为公司/项目信息，底部为报价人/日期信息

### 2. 内容解析规则

**输入内容分析**：

- 提取所有非空行
- 按语义分组识别：
  - **公司信息段**：顶部 1-2 行，包含公司名称、项目信息
    - 如果只有1行但包含公司名和项目信息，需要智能分离（识别公司名称和项目描述的边界）
  - **卷册信息段**：中间部分，包含卷册标识（如"第二卷"）、文件类型（如"技术部分"）、"报价文件"等
  - **报价人信息段**：底部 2-3 行
    - 2行：报价人（或采购人） + 日期
    - 3行：采购人 + 采购机构 + 日期

**默认假设**（如果信息缺失）：

- 如果卷册部信息不完整，保留现有内容但调整间距
- 如果缺少"第二卷"信息，不调整格式
- 内容行数可能变化，但尽量保持在一页以内

### 2.1 文本排版规则

**日期格式标准化**：

- 输入：`2025年12月` 或 `2025.12`
- 输出：`2025年12月`（统一使用"年月"格式，不添加空格）

**卷册标识空格规则**：

- 输入：`第二卷技术部分`、`第三卷技术分册`
- 输出：`第二卷 技术部分`、`第三卷 技术分册`（在"卷"字后添加空格）

**项目信息处理规则**：

- 项目名称和项目标的保持在同一行，不进行分段
- 第二行直接使用原始输入内容，包含完整的项目描述

### 3. Markdown 输出格式规范（使用 HTML 标签表示样式）

**字号对照表**（中文字号 → pt）：
| 中文字号 | pt 值 |
|---------|-------|
| 一号 | 26pt |
| 二号 | 22pt |
| 三号 | 16pt |
| 四号 | 14pt |
| 小三号 | 15pt |

**字体规范**：

- 黑体：用于所有封面信息（公司信息、项目信息、卷册信息、报价人信息、日期）

**行高基准**：1 行 ≈ 22pt

---

## 格式模板

### 栟准封面格式（8行）

```markdown
<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 0pt; text-align: center;">{公司名称}</div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; text-align: center;">{项目信息}</div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 11pt; text-align: center;">{文件类型}</div>

<div style="margin-top: 176pt;"></div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 0pt; text-align: center;">{卷册标识} {卷册名称}</div>

<div style="margin-top: 242pt;"></div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 0pt; text-align: center;">报价人：{报价人全称}</div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 11pt; text-align: center;">{日期}</div>
```

### 简化封面格式（内容少于8行）

根据实际内容行数灵活调整：

- 如果缺失卷册信息（第5行），调整中间留白大小
- 如果缺失了日期（第8行），移除对应div
- **核心原则**：保持视觉平衡，内容尽量在一页以内

---

## 处理流程

### Step 1: 识别封面

检查输入内容是否为封面文档：

- 扫描标题行，查找关键词
- 分析内容结构特征
- 确认后继续，否则提示用户

### Step 2: 解析内容

按语义分段提取信息：

- 公司信息段（顶部）
- 卷册信息段（中间）
- 报价人信息段（底部）

### Step 3: 生成 Markdown

根据解析内容应用格式模板：

- 填充占位符
- 调整段前距和留白
- 确保字体、字号规范
- 输出为 Markdown 格式（使用 HTML 标签表示样式）

### Step 4: 输出结果

返回完整的 Markdown 代码

---

## 重要注意事项

1. **输出格式**：输出为 Markdown 文件，但使用 HTML `<div>` 标签包裹文本内容来表示样式
2. **字体名称**：统一使用"黑体"
3. **字号单位**：统一使用 22pt（二号）
4. **间距单位**：统一使用 pt
5. **日期格式**：保持完整格式"YYYY年MM月"（无空格），不缩写为"YYYY.MM"
6. **报价人全称**：保持营业执照全称，不可简写
7. **一页限制**：确保内容布局在 A4 纸一页以内
8. **空行处理**：使用空的 `<div>` 设置 margin-top，不使用 `<br>`
9. **标签格式**：每个 `<div>` 独占一行，标签内部无缩进（保持 Markdown 简洁）
10. **居中对齐**：所有包含文字的 `<div>` 标签必须包含 `text-align: center;` 样式，确保内容居中对齐。

---

## 示例

### 输入（Markdown）

```markdown
国能信控技术股份有限公司
陕西公司店塔电厂MIS系统升级改造项目燃料与检修管理系统、备份等设备

报价文件

第二卷技术部分

报价人：马鞍山市睿峰信息技术有限公司
2025年12月
```

### 输出（Markdown 使用 HTML 标签）

```markdown
<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 0pt; text-align: center;">国能信控技术股份有限公司</div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; text-align: center;">陕西公司店塔电厂MIS系统升级改造项目燃料与检修管理系统、备份等设备</div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 11pt; text-align: center;">报价文件</div>

<div style="margin-top: 176pt;"></div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 0pt; text-align: center;">第二卷 技术部分</div>

<div style="margin-top: 242pt;"></div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 0pt; text-align: center;">报价人：马鞍山市睿峰信息技术有限公司</div>

<div style="font-family: 黑体; font-size: 22pt; font-weight: normal; margin-top: 11pt; text-align: center;">2025年12月</div>
```

---

## 质量检查清单

输出 Markdown 前必须检查：

- [ ] 输出格式为 Markdown（非纯 HTML 文件）
- [ ] 所有字体均为"黑体"
- [ ] 所有字号均为 22pt (二号)
- [ ] 所有间距使用 pt 单位
- [ ] 日期格式为"YYYY年MM月"（无空格）
- [ ] 报价人信息完整，包含"报价人："前缀
- [ ] 页面布局合理，不溢出
- [ ] 留白段使用空 `<div>` 而非 `<br>`
- [ ] HTML 结构合法，标签正确闭合
- [ ] 每个 `<div>` 独占一行
- [ ] 所有包含文字的 `<div>` 都包含 `text-align: center;`
