---
name: Auto-Redbook
description: 小红书笔记素材创作技能。当用户需要创建小红书笔记素材时使用这个技能。技能包含：根据用户的需求和提供的资料，撰写小红书笔记内容（标题+正文），生成图片卡片（封面+正文卡片，支持多种样式主题），支持批量创作多篇笔记。
---

# 小红书笔记创作技能

这个技能用于创建专业的小红书笔记素材，包括内容撰写、图片卡片生成（支持7种样式主题）和智能分页渲染。支持批量创作多篇笔记，自动循环使用不同样式。

## 使用场景

- 用户需要创建小红书笔记时
- 用户提供资料需要转化为小红书风格内容时
- 用户需要生成精美的图片卡片用于发布时
- 用户需要多种风格样式选择时
- 用户需要批量创作多篇笔记时

## 工作流程

### 第一步：确定笔记数量

**重要变更**：笔记数量不再固定为1篇，而是根据任务目录中的需求动态确定。

- 如果用户明确要求创作多篇笔记（如"创作3篇笔记"），则按用户要求的数量创作
- 如果用户提供了多个主题或素材，则根据主题/素材数量创作对应数量的笔记
- 每篇笔记将保存在独立的文件夹中，便于管理和发布

**文件夹组织结构**：
```
任务目录/
├── note_1/
│   ├── note_1.md
│   ├── cover.png
│   ├── card_1.png
│   └── card_2.png
├── note_2/
│   ├── note_2.md
│   ├── cover.png
│   └── card_1.png
└── note_3/
    ├── note_3.md
    ├── cover.png
    ├── card_1.png
    └── card_2.png
```

### 第二步：撰写小红书笔记内容

根据用户需求和提供的资料，创作符合小红书风格的内容：

#### 标题要求
- 不超过 20 字
- 吸引眼球，制造好奇心
- 可使用数字、疑问句、感叹号增强吸引力
- 示例：「5个让效率翻倍的神器推荐！」「震惊！原来这样做才对」

#### 正文要求
- 使用良好的排版，段落清晰
- 点缀少量 Emoji 增加可读性（每段 1-2 个即可）
- 使用简短的句子和段落
- 结尾给出 SEO 友好的 Tags 标签（5-10 个相关标签）

**多篇笔记创作要求**：
- 每篇笔记应有独立的主题和内容
- 笔记之间内容不重复，各有侧重点
- 保持风格统一但内容差异化

### 第三步：生成 Markdown 文档

**注意：这里生成的 Markdown 文档是用于渲染卡片的，必须专门生成，禁止直接使用上一步的笔记正文内容。**

**多篇笔记时的文件命名**：
- 第1篇：`note_1/note_1.md`
- 第2篇：`note_2/note_2.md`
- 第3篇：`note_3/note_3.md`
- 以此类推...

Markdown 文件，文件应包含：

1. YAML 头部元数据（封面信息）：
```yaml
---
emoji: "🚀"           # 封面装饰 Emoji
title: "大标题"        # 封面大标题（不超过15字）
subtitle: "副标题文案"  # 封面副标题（不超过15字）
---
```

2. 用于渲染卡片的 Markdown 文本内容：
   - 使用 `---` 分割线将正文分隔为多个卡片段落
   - 每个分段的文字控制在 200 字左右
   - 脚本会自动检测内容高度并智能分页

完整示例：
```markdown
---
emoji: "💡"
title: "5个效率神器让工作效率翻倍"
subtitle: "对着抄作业就好了，一起变高效"
---

# 神器一：Notion 📝

> 全能型笔记工具，支持数据库、看板、日历等多种视图...

## 特色功能

- 特色一
- 特色二

---

# 神器二：Raycast ⚡

可使用代码块来增加渲染后图片的视觉丰富度

## 推荐原因

- 原因一
- 原因二
- ……

---

# 神器三：Arc 🌈

全新理念的浏览器，侧边栏标签管理...

...

#效率工具 #生产力 #Mac软件
```

### 第四步：渲染图片卡片

将 Markdown 文档渲染为图片卡片。**推荐使用 V2 版本脚本**，支持智能分页和多种样式。

#### 样式循环使用机制（新增 🆕）

**重要变更**：当创作多篇笔记时，图片样式将自动循环使用，确保视觉多样性。

样式循环顺序：
1. purple（紫韵）
2. xiaohongshu（小红书红）
3. mint（清新薄荷）
4. sunset（日落橙）
5. ocean（深海蓝）
6. elegant（优雅白）
7. dark（暗黑模式）

**循环规则**：
- 第1篇笔记使用 `purple` 样式
- 第2篇笔记使用 `xiaohongshu` 样式
- 第3篇笔记使用 `mint` 样式
- ...
- 第7篇笔记使用 `dark` 样式
- 第8篇笔记回到 `purple` 样式（循环开始）
- 以此类推

**渲染命令示例**：
```bash
# 第1篇笔记（purple样式）
python scripts/render_xhs_v2.py note_1/note_1.md -o note_1 --style purple

# 第2篇笔记（xiaohongshu样式）
python scripts/render_xhs_v2.py note_2/note_2.md -o note_2 --style xiaohongshu

# 第3篇笔记（mint样式）
python scripts/render_xhs_v2.py note_3/note_3.md -o note_3 --style mint

# 第8篇笔记（回到purple样式）
python scripts/render_xhs_v2.py note_8/note_8.md -o note_8 --style purple
```

#### V2 渲染脚本（推荐）

V2 版本新增特性：
- ✅ **智能分页**：自动检测内容高度，超出时自动拆分到多张卡片
- ✅ **多种样式**：支持 7 种预设样式主题
- ✅ **字数预估**：基于字数预分配内容，减少渲染次数
- ✅ **样式循环**：多篇笔记自动循环使用不同样式

**Python 版本：**

```bash
# 基本用法
python scripts/render_xhs_v2.py <markdown_file>

# 指定输出目录
python scripts/render_xhs_v2.py <markdown_file> -o <output_directory>

# 指定样式主题
python scripts/render_xhs_v2.py <markdown_file> --style xiaohongshu

# 查看所有可用样式
python scripts/render_xhs_v2.py --list-styles
```

**Node.js 版本：**

```bash
# 基本用法
node scripts/render_xhs_v2.js <markdown_file>

# 指定输出目录和样式
node scripts/render_xhs_v2.js <markdown_file> -o ./output --style mint

# 查看所有可用样式
node scripts/render_xhs_v2.js --list-styles
```

#### 可用样式主题

| 样式键 | 名称 | 描述 |
|--------|------|------|
| `purple` | 紫韵 | 默认样式，紫蓝色渐变 |
| `xiaohongshu` | 小红书红 | 小红书品牌色系 |
| `mint` | 清新薄荷 | 绿色/自然调 |
| `sunset` | 日落橙 | 粉色/日落渐变 |
| `ocean` | 深海蓝 | 蓝绿色海洋调 |
| `elegant` | 优雅白 | 简约灰白调 |
| `dark` | 暗黑模式 | 深色背景，高对比度 |

#### 旧版渲染脚本（保留）

如需使用旧版（不支持自动分页）：

```bash
# Python 版本
python scripts/render_xhs.py <markdown_file> [--output-dir <output_directory>]

# Node.js 版本
node scripts/render_xhs.js <markdown_file> [--output-dir <output_directory>]
```

**旧版已知问题**：单张卡片内容过多时可能出现文字溢出，需手动用 `---` 分隔。

### 第五步：发布小红书笔记（可选）

#### 5.1 首次使用：扫码登录

**推荐方式**：使用扫码登录脚本，自动保存 Cookie，无需手动配置。

**Python 版本：**
```bash
python scripts/login_xhs.py
```

**Node.js 版本：**
```bash
node scripts/login_xhs.js
```

**登录流程**：
1. 运行登录脚本，自动弹出小红书登录页面
2. 使用小红书 APP 扫描二维码登录
3. 登录成功后，Cookie 自动保存到 `.env` 文件
4. 下次发布时自动使用保存的 Cookie

**功能特点**：
- ✅ 自动检测现有 Cookie 是否有效
- ✅ Cookie 失效时提示重新登录
- ✅ 支持重新登录覆盖旧 Cookie
- ✅ 记录 Cookie 更新时间

#### 5.2 发布笔记

登录完成后，使用发布脚本将生成的图片发布到小红书：

**单篇笔记发布**：
```bash
python scripts/publish_xhs.py --title "笔记标题" --desc "笔记描述" --images cover.png card_1.png card_2.png
```

**多篇笔记批量发布（新增 🆕）**：

**重要变更**：支持批量发布多篇笔记，每篇笔记发布后自动等待10分钟再发布下一篇，避免被平台限流。

```bash
# 发布第1篇笔记
python scripts/publish_xhs.py --title "笔记1标题" --desc "笔记1描述" --images note_1/cover.png note_1/card_1.png note_1/card_2.png

# 等待10分钟（600秒）
# 系统会自动等待，或手动执行：python -c "import time; time.sleep(600)"

# 发布第2篇笔记
python scripts/publish_xhs.py --title "笔记2标题" --desc "笔记2描述" --images note_2/cover.png note_2/card_1.png

# 等待10分钟

# 发布第3篇笔记
python scripts/publish_xhs.py --title "笔记3标题" --desc "笔记3描述" --images note_3/cover.png note_3/card_1.png note_3/card_2.png

# 以此类推...
```

**发布间隔说明**：
- 每篇笔记发布完成后，必须等待 **10分钟（600秒）** 再发布下一篇
- 这是为了避免频繁发布被小红书平台识别为异常行为
- 建议在发布脚本之间添加 `time.sleep(600)` 或使用定时任务

**Node.js 版本（如果有）：**
```bash
node scripts/publish_xhs.js --title "笔记标题" --desc "笔记描述" --images cover.png card_1.png card_2.png
```

**发布参数说明**：
- `--title` / `-t`: 笔记标题（不超过20字）
- `--desc` / `-d`: 笔记描述/正文内容
- `--images` / `-i`: 图片文件路径（可以多个，建议封面放第一张）
- `--private`: 设为私密笔记（可选）
- `--post-time`: 定时发布时间（可选，格式：2024-01-01 12:00:00）
- `--dry-run`: 仅验证，不实际发布（可选）

**示例**：
```bash
# 基本发布
python scripts/publish_xhs.py --title "春节学车3280元" --desc "德安驾校春节特惠" --images cover.png card_1.png card_2.png

# 私密笔记
python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png --private

# 定时发布
python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png --post-time "2024-02-01 10:00:00"

# 验证模式（不实际发布）
python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png --dry-run
```

#### 5.3 手动配置 Cookie（备选方案）

如果扫码登录遇到问题，也可以手动配置 Cookie：

1. 在项目根目录创建 `.env` 文件
2. 添加以下内容：
```
XHS_COOKIE=your_cookie_string_here
```

3. Cookie 获取方式：
   - 在浏览器中登录小红书（https://creator.xiaohongshu.com）
   - 打开开发者工具（F12）
   - 在 Network 标签中查看请求头的 Cookie
   - 复制完整的 Cookie 字符串

## 图片规格说明

### 封面卡片
- 尺寸比例：3:4（小红书推荐比例）
- 基准尺寸：1080×1440px
- 包含：Emoji 装饰、大标题、副标题
- 样式：渐变背景 + 圆角内容区（根据所选主题变化）

### 正文卡片
- 尺寸比例：3:4
- 基准尺寸：1080×1440px
- 支持：标题、段落、列表、引用、代码块、图片
- 样式：白色卡片 + 渐变背景边框（根据所选主题变化）
- V2 版本：自动分页，单张卡片内容不会溢出

## 技能资源

### 脚本文件
- `scripts/render_xhs.py` - Python V1 渲染脚本（旧版）
- `scripts/render_xhs.js` - Node.js V1 渲染脚本（旧版）
- `scripts/render_xhs_v2.py` - Python V2 渲染脚本（推荐 ✅）
- `scripts/render_xhs_v2.js` - Node.js V2 渲染脚本（推荐 ✅）
- `scripts/login_xhs.py` - Python 扫码登录脚本（新增 🆕）
- `scripts/login_xhs.js` - Node.js 扫码登录脚本（新增 🆕）
- `scripts/publish_xhs.py` - 小红书发布脚本

### 资源文件
- `assets/cover.html` - 封面 HTML 模板（旧版）
- `assets/card.html` - 正文卡片 HTML 模板（旧版）
- `assets/styles.css` - 共用样式表（旧版）
- `assets/example.md` - 示例 Markdown 文件

## 注意事项

1. **V2 版本推荐**：V2 版本支持智能分页，可自动处理内容溢出问题
2. **样式选择**：根据内容风格选择合适的样式主题
3. **样式循环**：多篇笔记时，样式会按照 purple → xiaohongshu → mint → sunset → ocean → elegant → dark 的顺序循环使用
4. **Markdown 位置**：Markdown 文件应保存在工作目录，渲染后的图片也保存在工作目录
5. **文件夹组织**：多篇笔记时，每篇笔记保存在独立的 `note_N` 文件夹中（N为笔记序号）
6. **内容长度**：建议每个 `---` 分隔的内容块控制在 200 字以内
7. **发布间隔**：批量发布时，每篇笔记之间必须间隔 **10分钟（600秒）**，避免被平台限流
8. **扫码登录**：首次发布前需要运行 `login_xhs.py` 或 `login_xhs.js` 进行扫码登录
9. **Cookie 有效期**：Cookie 有过期限制，失效后登录脚本会自动提示重新登录
10. **发布依赖**：发布功能依赖 xhs 库（Python）或相应的 npm 包（Node.js）
   - Python: `pip install xhs python-dotenv`
   - Node.js: `npm install dotenv`

## 批量发布 GUI 工具（V6.6 新增 🆕）

为了解决批量发布任务运行时间长、终端超时的问题，新增了图形界面（GUI）工具。

### GUI 工具特点

- ✅ 图形界面，操作简单直观
- ✅ 实时显示发布进度和日志
- ✅ 支持暂停、继续、停止操作
- ✅ 自动倒计时显示
- ✅ 不会因运行时间长而超时
- ✅ 自动保存发布记录

### 使用方法

#### 工具1：批量发布工具

**启动文件**：`start_publish.bat`

**使用步骤**：
1. 双击运行 `start_publish.bat`
2. 等待窗口打开（红色标题栏）
3. 点击"开始发布"按钮
4. 观察发布进度和日志
5. 等待完成提示

**界面功能**：
- 📊 实时进度显示（X/10 篇已完成）
- 📝 详细日志输出
- ⏸️ 暂停/继续按钮
- ⏹️ 停止按钮
- ⏱️ 自动倒计时

#### 工具2：进度查看器

**启动文件**：`view_progress.bat`

**使用步骤**：
1. 双击运行 `view_progress.bat`
2. 查看已发布笔记列表
3. 双击笔记打开链接
4. 自动刷新（每5秒）

**界面功能**：
- 📊 进度统计（已发布 X / 10 篇）
- 📋 笔记列表表格
- 🔗 双击打开笔记链接
- 🔄 自动刷新
- 🌐 快速打开创作者中心

### GUI 工具文件说明

| 文件名 | 类型 | 用途 |
|--------|------|------|
| `start_publish.bat` | 批处理 | 启动批量发布工具 |
| `view_progress.bat` | 批处理 | 启动进度查看器 |
| `test_environment.bat` | 批处理 | 测试环境和依赖 |
| `publish_gui.py` | Python | 批量发布 GUI 主程序 |
| `progress_viewer_gui.py` | Python | 进度查看器 GUI 主程序 |

### 修改发布参数

如需修改起始笔记或间隔时间，编辑 `start_publish.bat`：

```batch
@echo off
cd /d "D:\20260127XHS\Auto-Redbook-Skills-main"
C:\Python314\python.exe scripts\publish_gui.py ^
    --notes-dir "D:\jieyue_work\drivingschool_notes" ^
    --start-from 1 ^
    --wait-minutes 10
pause
```

**参数说明**：
- `--notes-dir`: 笔记目录路径
- `--start-from`: 从第几篇开始发布（默认：1）
- `--wait-minutes`: 每篇笔记之间的等待时间（默认：10分钟）

### 环境测试

在首次使用前，建议运行环境测试：

```batch
双击运行: test_environment.bat
```

测试内容：
- ✅ 检查 Python 是否安装
- ✅ 检查脚本语法是否正确
- ✅ 检查依赖是否安装
- ✅ 自动安装缺失的依赖

## 批量创作流程示例

假设用户要求创作 3 篇关于"效率工具"的小红书笔记：

### 步骤1：确定笔记数量和主题
- 笔记1：Notion 使用技巧
- 笔记2：Mac 效率工具推荐
- 笔记3：时间管理方法

### 步骤2：创建文件夹结构
```
工作目录/
├── note_1/
├── note_2/
└── note_3/
```

### 步骤3：撰写并生成 Markdown
- `note_1/note_1.md` - Notion 使用技巧
- `note_2/note_2.md` - Mac 效率工具推荐
- `note_3/note_3.md` - 时间管理方法

### 步骤4：渲染图片（自动循环样式）
```bash
# 笔记1 使用 purple 样式
python scripts/render_xhs_v2.py note_1/note_1.md -o note_1 --style purple

# 笔记2 使用 xiaohongshu 样式
python scripts/render_xhs_v2.py note_2/note_2.md -o note_2 --style xiaohongshu

# 笔记3 使用 mint 样式
python scripts/render_xhs_v2.py note_3/note_3.md -o note_3 --style mint
```

### 步骤5：批量发布（使用 GUI 工具）

**方法1：使用 GUI 工具（推荐）**
```
1. 双击运行 start_publish.bat
2. 点击"开始发布"按钮
3. 等待自动完成（约30分钟，3篇笔记 × 10分钟间隔）
```

**方法2：使用命令行**
```bash
# 发布笔记1
python scripts/publish_xhs.py --title "Notion使用技巧" --desc "..." --images note_1/cover.png note_1/card_*.png

# 等待10分钟
python -c "import time; time.sleep(600)"

# 发布笔记2
python scripts/publish_xhs.py --title "Mac效率工具推荐" --desc "..." --images note_2/cover.png note_2/card_*.png

# 等待10分钟
python -c "import time; time.sleep(600)"

# 发布笔记3
python scripts/publish_xhs.py --title "时间管理方法" --desc "..." --images note_3/cover.png note_3/card_*.png
```

## 版本历史

### V6.6 (2026-01-27)
**新增功能**：
- ✅ 批量发布 GUI 工具（`publish_gui.py`）
- ✅ 进度查看器 GUI 工具（`progress_viewer_gui.py`）
- ✅ 批处理启动器（`start_publish.bat`, `view_progress.bat`）
- ✅ 环境测试工具（`test_environment.bat`）
- ✅ 自动保存发布记录（`publish_records.json`）

**问题修复**：
- ✅ 修复批处理文件编码问题
- ✅ 修复 Python 代码中文引号语法错误
- ✅ 修复批量发布任务超时问题
- ✅ 修复批处理文件闪退问题

**改进**：
- ✅ 图形界面操作更直观
- ✅ 实时显示发布进度
- ✅ 支持暂停/继续/停止操作
- ✅ 自动倒计时显示
- ✅ 不会因运行时间长而超时

### V6.5 (2026-01-27)
**新增功能**：
- ✅ 支持批量创作多篇笔记
- ✅ 动态读取笔记数量
- ✅ 图片样式自动循环使用
- ✅ 每篇笔记独立文件夹保存
- ✅ 发布间隔机制（10分钟/篇）

**改进**：
- ✅ 优化文件夹组织结构
- ✅ 添加批量创作流程示例
- ✅ 完善发布间隔说明

---

**技能版本**: V6.6
**最后更新**: 2026-01-27
**维护者**: StepFun AI Team

## 智能分页说明

V2 版本的智能分页机制：

1. **预估阶段**：基于字数、元素类型预估内容高度
2. **预渲染阶段**：使用 Playwright 预渲染并测量实际高度
3. **拆分阶段**：如果内容超出，按段落/行智能拆分内容
4. **固定输出**：每张卡片固定为 1080×1440px，确保一致性

这种机制确保无论内容多长，都不会出现文字溢出问题。
