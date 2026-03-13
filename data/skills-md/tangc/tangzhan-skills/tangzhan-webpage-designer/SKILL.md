---
name: tangzhan-webpage-designer
description: 将任何文本转换为独立的、具有特定设计风格的网页。内置 30+ 种精选设计风格，具备智能风格匹配和有说服力的推荐逻辑。充当您的智能设计顾问。
---

# 文本转网页转换器 (Text to Webpage Converter)

## 简介

此技能将用户提供的文本内容转换为单文件、响应式的 HTML 网页。它利用了一个包含 30 种独特设计风格的库（源自 designprompts.dev）。该技能旨在充当一名“设计顾问”：它会分析用户的文本，推荐最合适的风格，或者接受用户指定的风格请求。

## 核心逻辑

1.  **分析内容 (Analyze Content)**：确定用户文本的语气、受众和目的。
2.  **选择风格 (Select Style)**：
    *   **用户指定**：如果用户要求特定风格（例如“赛博朋克”），则在 [风格矩阵] 中进行匹配。
    *   **智能推荐**：如果未指定，则根据内容分析结果，从 [风格矩阵] 中选择最契合的风格。
    *   **决胜机制**：如果多种风格都适合或内容较为中性，则基于视觉多样性或“顾问精选”进行选择（并提供有说服力的理由）。
3.  **加载提示词 (Load Prompt)**：从 `references/` 目录读取相应的设计系统文件（例如 `references/cyberpunk.md`）。
4.  **生成网页 (Generate)**：将读取到的风格提示词与用户内容结合，生成 HTML 代码。

## 风格矩阵 (Style Matrix)

使用此矩阵来确定选择哪种风格。

| ID | 风格名称 (Style Name) | 视觉氛围 (Visual Vibe) | 适用场景 (Best For) | 关键词 (Keywords) | 参考文件 (Reference File) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 01 | **Monochrome** | 严谨、社论感、高对比度 | 时尚、建筑、奢侈品博客 | 黑白, 衬线体, 锐利 | `references/monochrome.md` |
| 02 | **Bauhaus** | 几何感、构成主义、大胆 | 海报、艺术作品集、创意机构 | 三原色, 形状, 不对称 | `references/baohaus.md` |
| 03 | **Modern Dark** | 电影感、氛围感、发光 | 开发者工具、SaaS、高科技 | 暗黑模式, 渐变, 聚光灯 | `references/modernDark.md` |
| 04 | **Newsprint** | 权威、密集、经典 | 新闻、博客、长文阅读 | 网格, 衬线体, 米白, 边框 | `references/newsprint.md` |
| 05 | **SaaS** | 干净、值得信赖、现代 | 初创公司、产品落地页 | 蓝色点缀, Inter字体, 留白 | `references/saas.md` |
| 06 | **Luxury** | 优雅、宽敞、高级 | 珠宝、高端服务、酒店 | 金色, 衬线体, 极简, 慢动作 | `references/luxury.md` |
| 07 | **Terminal** | 复古未来、黑客、原始 | 开发博客、CLI工具、加密货币 | 等宽字体, 绿/黑, 光标 | `references/terminal.md` |
| 08 | **Swiss Minimalist** | 客观、网格化、理性 | 企业报告、建筑、瑞士设计 | Helvetica, 红色点缀, 严谨网格 | `references/swissMinimalist.md` |
| 09 | **Kinetic** | 动态、移动、喧闹 | 活动推广、作品集、潮流 | 跑马灯, 大字, 动效 | `references/kinetic.md` |
| 10 | **Flat Design** | 2D、多彩、简单 | 插画作品集、趣味应用 | 纯色, 无阴影, 矢量感 | `references/flatDesign.md` |
| 11 | **Art Deco** | 装饰性、几何、金色 | 请柬、历史、地下酒吧 | 金线, 对称, 1920年代 | `references/artDeco.md` |
| 12 | **Material Design** | 触感、熟悉、谷歌风 | 安卓应用、仪表盘 | 阴影, 涟漪, 纸张层级 | `references/materialDesign.md` |
| 13 | **Neo Brutalism** | 原始、未打磨、大胆 | Z世代品牌、艺术、前卫博客 | 高对比, 默认字体, 粗边框 | `references/neoBrutalism.md` |
| 14 | **Bold Typography** | 喧闹、文字为主、图形化 | 宣言、声明、海报 | 巨型文本, 负空间 | `references/boldTypography.md` |
| 15 | **Academia** | 传统、温暖、学术 | 大学、研究、文学 | 米色, 衬线体, 红/金, 纸张 | `references/academia.md` |
| 16 | **Cyberpunk** | 反乌托邦、霓虹、故障 | 游戏、科幻、夜生活 | 霓虹粉/蓝, 故障风, 暗黑 | `references/cyberpunk.md` |
| 17 | **Web3** | 数字化、金融、深邃 | 加密货币、NFT、金融科技 | 橙/蓝, 暗黑, 数据可视化 | `references/web3.md` |
| 18 | **Playful Geometric** | 有趣、活力、形状 | 儿童、创意机构、初创公司 | 孟菲斯风格, 亮色 | `references/playfulGeometric.md` |
| 19 | **Minimal Dark** | 光滑、柔和、磨砂 | 个人网站、笔记、情绪板 | 深灰, 琥珀微光, 毛玻璃 | `references/minimalDark.md` |
| 20 | **Claymorphism** | 柔软、3D、玩具感 | 亲和力应用、教育 | 3D, 阴影, 马卡龙色, 圆润 | `references/claymorphism.md` |
| 21 | **Professional** | 经典、干净、衬线体 | 律所、简历、咨询 | 象牙白, 衬线体, 平衡 | `references/professional.md` |
| 22 | **Botanical** | 有机、自然、柔和 | 健康、食品、自然 | 大地色, 圆润, 绿色 | `references/botanical.md` |
| 23 | **Vaporwave** | 怀旧、超现实、粉色 | 音乐、复古博客、艺术 | 80年代, 粉/青, 网格, 雕像 | `references/vaporwave.md` |
| 24 | **Enterprise** | 可靠、企业感、蓝色 | B2B、大型组织、内网 | 靛蓝, 等轴测, 干净 | `references/enterprise.md` |
| 25 | **Sketch** | 手绘、随性、粗糙 | 笔记、DIY、个人博客 | 涂鸦, 铅笔, 纸张 | `references/sketch.md` |
| 26 | **Industrial** | 技术、原始、工程感 | 硬件、工具、规格说明 | 橙色, 灰色, 等宽字体, 线条 | `references/industrial.md` |
| 27 | **Neumorphism** | 柔软、物理感、凸起 | 智能家居、控制面板、播放器 | 柔和阴影, 单色 | `references/neumorphism.md` |
| 28 | **Organic** | 流动、自然、侘寂 | 陶瓷、健康、生活方式 | 斑点形状, 纹理, 土色 | `references/organic.md` |
| 29 | **Maximalism** | 混乱、繁忙、表现力 | 独立杂志、艺术、时尚 | 撞色, 密集, 图案 | `references/maximalism.md` |
| 30 | **Retro** | 怀旧、低保真、像素 | 旧科技、游戏、档案馆 | Windows 95, 像素, 米色 | `references/retro.md` |

## 执行指令 (Execution Instructions)

1.  **选择 (Selection)**：首先，告诉用户你选择了哪种风格，以及*为什么*。
    *   *示例*：“考虑到您内容的专业技术性质，我选择了 **'Terminal' (终端)** 风格，以为其赋予一种复古未来的黑客氛围。”
2.  **工具使用 (Tool Use)**：使用 `read` 工具读取上述矩阵中对应的 **参考文件 (Reference File)** 内容。
3.  **生成 (Generate)**：
    *   将 **用户文本** 和 **参考文件内容** 传递给你的编码模型。
    *   给编码模型的指令：“你是一名专家级前端工程师。请使用参考内容中定义的设计系统，将用户的文本转换为一个单文件 HTML 网页。确保严格遵守参考文件中定义的颜色、字体和布局规则。”
