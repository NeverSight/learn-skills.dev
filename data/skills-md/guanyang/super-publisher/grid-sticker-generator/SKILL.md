---
name: grid-sticker-generator
description: A universal 4x4 grid sticker generator. uses strict visual guidelines (No Text, Transparent BG) and supports loading theme templates from resources.
---

# Universal Grid Sticker Generator

这是一个通用的 Q 版表情包网格生成器。它定义了一套严格的**视觉设计规范**和**提示词构建框架**，用于生成高质量、易于切割的 4x4 表情包网格图。

## 🎨 核心视觉规范 (Visual Design Standards)

无论生成什么主题，以下规范 **必须严格执行**：

1.  **Format (格式)**:
    *   **网格布局**: **16-grid sticker sheet**, 4 rows by 4 columns (4x4 布局)。
    *   **间距**: 彼此之间保持均匀、宽敞的间距，互不粘连 (Even spacing, no overlap)。
    *   **画幅**: 1:1 正方形。

2.  **Style Constraints (风格约束)**:
    *   **背景**: **Transparent Background** (Output image with transparent background).
    *   **边缘**: **No outline**, **No white border**, **Clean edges** (无描边、无白边、边缘清晰).
    *   **风格**: **Vector style**, **Flat color**, **Organic shapes** (矢量、扁平、有机形状).

3.  **Content Restrictions (内容禁忌)**:
    *   **NO TEXT**: **严禁**出现汉字、英文、数字。
    *   **NO BUBBLES**: **严禁**出现对话气泡。
    *   **纯视觉表达**: 所有的情绪和梗必须通过肢体语言、表情和漫符 (如 💢, 💦, ❤️) 来表达。

## 📂 模板系统 (Template System)

本 Skill 支持加载不同的主题模板。模板位于 `resources/` 目录下。

### 默认模板：打工人 (Office Worker)
*   **Template File**: `resources/office_worker_template.md`
*   **Description**: 包含“摸鱼”、“加班”、“画饼”等32个经典职场梗的随机库。

## 🛠️ 执行流程 (Execution Workflow)

1.  **确定主题与角色**:
    *   分析用户输入，确定角色形象（如：熊猫程序员、美少女战士产品经理）。
    *   确定使用的模板（默认为 Office Worker，或用户自定义其他主题）。

2.  **构建 Prompt**:
    *   **Header**: Load Role & Style from SKILL guidelines.
    *   **Subject**: "Cute Q-version character, [User Role Description]".
    *   **Action List**: 
        *   如果使用模板：从模板的库中抽取 (16 - N) 个动作补充到列表中。
        *   如果无模板：根据主题生成 16 个多样化的通用情绪动作（喜怒哀乐、日常行为）。
    *   **Negative Prompts**: `text, words, letters, chinese characters, speech bubble, watermark, signature`.

3.  **生成图像**:
    *   调用绘图工具 (`Nano-Banana Pro` / `generate_image`) 输出图像。

## 使用示例

**使用内置打工人模板:**
> "生成一个 '秃顶的猫咪程序员' 表情包。"
> (系统自动加载 office_worker_template.md 的梗库进行补全)

**自定义主题 (不使用模板):**
> "生成一套 '快乐的小狗' 表情包，包含跑、跳、睡觉、吃骨头等动作。"
> (系统基于通用 4x4 规范，自由发挥小狗的日常动作)
