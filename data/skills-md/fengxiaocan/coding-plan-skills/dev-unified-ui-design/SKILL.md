---
name: dev-unified-ui-design
description: 遵循统一跨平台设计系统规范（Web / iOS / Android / Desktop / Flutter / React Native / Compose Multiplatform / Electron / Tauri）的 UI/UX 设计、组件封装与页面规范审查工作流。当用户要求创建跨平台界面、重构 UI、封装公共设计系统组件、消除 Magic Number、优化响应式排版与多端一致性审查时使用。由 /dev-unified-ui-design 命令触发。
---

# Dev Unified UI Design — Cross-Platform Design System Workflow

**核心黄金法则：页面只负责组织内容，设计系统负责决定内容长什么样。业务页面严禁自行发明视觉样式。**

同一种组件，在所有页面和所有平台上，应保持相同的视觉语义、尺寸体系、交互逻辑和信息层级。

---

## 激活条件与触发方式

收到 `/dev-unified-ui-design` 或用户发起以下请求时触发：
- "创建/实现一个跨平台页面（Web/移动端/桌面端/Flutter/React/Compose）"
- "重构现有页面 UI，消除 Magic Number，统一视觉风格"
- "封装一套跨平台通用 Design System 组件库（Button, Card, Dialog, TextField 等）"
- "审查当前界面的设计规范、排版一致性、响应式弹性与深色模式"
- "解决界面在小屏/超大屏/字体放大/长文本下的折行、溢出与遮挡问题"

触发后，AI 必须严格按照以下 **5 阶段工作流** 推进，严禁未经设计系统检查直接编写散乱的业务代码。

---

## 5 阶段工作流程

```text
阶段 1: 资产扫描与盘点 → 检查已有 Design Tokens、Theme 与 Foundation 组件库
阶段 2: 架构规划与复用 → 确立信息层级（Header→Section→Card→Action），阻断重复造轮子
阶段 3: 严格规范实现   → 严格应用 Token、4/8 栅格、按钮防折行、恒定高度、语义色彩
阶段 4: 极端场景与弹性 → 验证断点自适应、320px 窄屏、150% 字体缩放、长文本防御、遮挡检测
阶段 5: 审查清单与交付 → 输出 8 大维度审查表与结构化交付报告
```

---

### 第 1 阶段：资产扫描与设计系统盘点（Scan & Inventory）

在编写或修改任何页面前，AI 必须先扫描目标工程中现有的 Design System 资产：

1. **扫描 Design Tokens & Theme**：
   - 检查是否存在全局 Token 定义（CSS Variables / Tailwind Config / TS Tokens / Kotlin Theme / Dart Theme）：
     - `Colors`（语义色彩：Brand, Surface, Text, Border, State, Overlay）
     - `Typography`（字号、字重、行高分级）
     - `Spacing`（4 / 8 基础网格间距）
     - `Radius`（XS/Sm/Md/Lg/XL/Full 圆角分级）
     - `Size`（按钮高度、输入框高度、图标尺寸）
     - `Elevation / Shadow`（层级阴影）
     - `Breakpoints`（响应式断点）
     - `ZIndex`（层叠上下文层级）
2. **扫描公共基础组件库（Foundation Components）**：
   - 检查是否存在统一封装的基础组件：
     - `Button` / `IconButton`（Primary, Secondary, Outlined, Text, Danger）
     - `TextField` / `TextArea`
     - `Card`
     - `Dialog` / `BottomSheet`
     - `ListItem`
     - `Table`
     - `Tabs` / `Chip`
     - `Navigation` / `Header` / `Sidebar`
     - `Snackbar` / `Toast`
     - `Loading` / `EmptyState` / `ErrorState`
3. **盘点决策**：
   - **已有完整 Design System**：后续阶段必须 100% 复用已有 Token 与组件，严禁新建异构组件。
   - **部分缺失**：优先补充缺失的基础 Token 或公共组件，严禁在业务页面内直接硬编码临时样式。
   - **全新项目/完全缺失**：提示用户并先建立规范的 `design-system/` 目录结构与核心 Tokens。

---

### 第 2 阶段：复用评估与信息架构规划（Audit & Architecture）

在动手编写界面前，进行信息层级规划与组件复用评估：

1. **标准信息层级（从上至下）**：
   ```text
   Page Header (Title + Description + Top Actions)
   ↓
   Core Status / Highlights Card (核心状态卡片 / 仪表盘)
   ↓
   Primary Action (主要核心操作，原则上一个区域仅一个)
   ↓
   Section Groups (Section Title + Grouped Cards / ListItems)
   ↓
   Secondary Content / Footnotes (辅助说明与次要操作)
   ```
2. **复用评估（严格阻断重复造轮子）**：
   - 严禁出现 `CustomButton`、`SpecialCard`、`SettingsItemView`、`BlueButton` 等命名混乱的孤立组件。
   - 组件只能通过 `Variant`（Primary, Secondary, Outline, Danger）和 `Size`（Small, Medium, Large）扩展。
   - 重复规则：相同 UI 模式出现 ≥ 2 次，必须考虑抽象为公共组件；出现 ≥ 3 次，默认必须组件化。
3. **Section 与分组结构规范**：
   - 结构模式：`Section Title` + 聚合容器（如包含多个 ListItem 的单 Card，中间以 1px/1dp Divider 分隔）。
   - Section 之间留白：标准间距 `24~32`。
   - **严禁卡片泛滥**：不要把每一个单行设置项都做成独立孤立 Card，避免页面视觉破碎化。

---

### 第 3 阶段：严格规范实现与 Token 落地（Strict Implementation）

实现 UI 时必须逐条核对并执行以下硬性设计规范：

#### 1. 零 Magic Number 原则（强制）
- ❌ 严禁出现 `13px`, `17px`, `19px`, `27px`, `37px`, `43px` 等随意捏造的数值。
- ✅ 所有间距、字号、圆角、高度必须来自 Design Token（如 `Spacing.md`, `Radius.lg`, `Typography.bodyMedium`）。

#### 2. 4 / 8 基础网格间距体系
- 间距等级：
  - `2` (微调), `4` (xs 紧凑内边距), `8` (sm 小元素间距), `12` (compact 关联元素间距)
  - `16` (md 标准内容间距、页面默认边距、Card 内边距)
  - `20` (comfortable 重点卡片内边距), `24` (lg Section 模块间距、大屏边距)
  - `32` (xl 大区块留白), `48` (3xl 超大留白 / 标准触控最小基准), `64` (section 大留白)
- 页面默认边距：小屏 `16`，中屏 `20~24`，大屏 `24~32`。
- **宽屏内容最大宽度限制**：桌面与超宽屏必须限制内容最大宽度（标准内容 `1200~1440`，设置/阅读/表单页 `640~840`），严禁正文在 4K 屏幕上无限横向拉伸。

#### 3. 统一圆角体系（全项目最多 5 级）
- `Radius XS (4)`：极小标签、Badge
- `Radius Small (8)`：Chip、小控件
- `Radius Medium (12)`：TextField、Button
- `Radius Large (16)`：Card、Modal 面板
- `Radius XLarge (20~24)`：Dialog、BottomSheet
- `Radius Full (9999)`：Avatar、圆形图标按钮、Pill Tag
- 严禁不同页面使用随意的不同圆角。

#### 4. 文字排印体系（Typography）
- 单个页面常规字体等级建议最多使用 **3~5 种**（如 Title, Section Title, Body, Secondary Text, Label）。
- 推荐层级：
  - Display Large (`32~40`), Headline Large (`28~32`), Headline Medium (`24~28`)
  - Title Large (`20~22`), Title Medium (`18`), Title Small (`16`)
  - Body Large (`16`), Body Medium (`14`), Body Small (`12`)
  - Label Large (`14`), Label Medium (`12`), Label Small (`11`)
- **同级文字全项目严格统一**：所有列表项标题用同级 Typography，所有辅助说明用同级 Typography。
- **字重规则**：仅使用 Regular, Medium, SemiBold。**严禁滥用 Bold**（Bold 仅用于关键数据和核心金额），依靠字号、色彩和留白体现层级。
- **行高规则**：正文行高 `字号 × 1.4~1.6`，标题行高 `字号 × 1.2~1.4`。

#### 5. 按钮统一规范（绝对红线）
- 尺寸统一：Large (`48~52`), Medium (`40~44`), Small (`32~36`)。
- **恒定高度**：同尺寸按钮在任何状态、任何内容下高度必须恒定一致，**禁止由文字多少撑高高度**。
- **按钮文本禁止自动换行**（强制设置）：
  - `maxLines = 1` / `white-space: nowrap` / `overflow: hidden; text-overflow: ellipsis`。
  - 严禁按钮因为文字过长折成两行（例如从 40px 变成 72px）。
- **空间不足梯次处理优先级**：
  1. 第一优先级：**缩短文案**（动词+对象，推荐 2~6 个汉字，原则不超过 8 个字；如“立即开始扫描设备”改为“开始扫描”）。
  2. 第二优先级：**扩大可用宽度**（使用 `flex-grow / weight(1f)` 或拉通铺满）。
  3. 第三优先级：**调整排列方向**（横向 Row 转纵向 Column）。
  4. 第四优先级：**适度减少左右 Padding**。
  5. 第五优先级：**文本省略号 Ellipsis**。
  - **严禁**：换行折行、无限增高、极端缩小子号到不可读。
- **触控区域**：IconButton 即使视觉图标是 16~24，**触控区域必须保留至少 40×40，推荐 44×44 或 48×48**。
- **按钮文案原则**：简洁明了（动词 + 对象），说明文字写在按钮外部，禁止把整句说明塞进按钮。
- **主次与危险操作**：一个主要操作区仅保留一个 Primary Action；删除等危险操作必须使用 Danger 语义样式。

#### 6. 语义色彩与深色模式（Dark Mode）
- 严禁裸写 `#333`, `#666`, `Color.Red`, `Color.White`, `纯黑`, `纯白`。
- 必须使用语义色彩 Token：`Primary`, `Surface`, `SurfaceElevated`, `TextPrimary`, `TextSecondary`, `TextTertiary`, `Border`, `Divider`。
- **状态颜色跨端一致**：Success (绿系), Warning (黄/橙系), Error (红系), Info (蓝系)，禁止同一状态在不同端/不同页面使用不同颜色。
- 所有组件原生支持 Light / Dark Theme 切换。

#### 7. 常用核心组件规格
- **Card**：统一 Radius, Padding, Background, Border, Elevation，仅用于内容分组与状态容器。
- **TextField**：标准单行高度 `44~52`，多行必须限制 `min-height` 与 `max-height` 并支持滚动。错误提示统一置于输入框底部。
- **Dialog**：统一背景、圆角 (16~24)、最大宽度 (Small 320~400, Medium 400~560, Large 560~720)。内容过长时：**Header 固定、Content 滚动、Footer 固定**。Footer 按钮宽度不足时自动转为纵向排列，严禁横向挤压换行。
- **ListItem**：标准三段式（Leading + Title/Subtitle + Trailing）。单行 `48~56`，双行 `64~72`，富文本 `72~88`。
- **Table**：统一 Header/Row 高度与边框。窄屏优先隐藏低优先级列、横向滚动或转为 Card List，禁止文字挤压重叠。
- **Tabs & Chip**：单行固定高度，多 Tabs 采用横向滚动或 More 菜单；Chip 保持短文本。
- **Feedback & State**：轻量反馈优先使用 `Snackbar / Toast`，禁止滥用 Dialog 阻断用户。统一 Empty State, Error State, Loading 视图。Loading 过程中禁止引起 **Layout Shift**（组件突然消失/闪现跳动）。
- **Divider**：统一 `1px / 1dp` 语义分割线。
- **Avatar & Badge**：Avatar 必须固定尺寸规格，禁止被原始图片尺寸撑大；Badge 单行小字号。

---

### 第 4 阶段：极端场景与多端自适应校验（Edge Cases & Responsiveness）

UI 实现后，必须在代码逻辑层面验证以下极端边界情况：

1. **响应式断点与布局形态**：
   - 断点分级：Compact (<600), Medium (600~839), Expanded (840~1199), Large (>=1200), Web Extra (>=1440)。
   - Compact：单栏流式、Bottom Navigation、重要按钮可 Full Width。
   - Medium：适度双栏、Navigation Rail。
   - Expanded / Large：Sidebar、Master-Detail、限制最大内容宽度。
   - **禁止固定分辨率假定**：严禁仅按 1920×1080 或 390×844 写死布局。
2. **最小支持尺寸与防重叠**：
   - 保证在最小窗口（如移动端 320px、桌面端 800×600）以及低高度窗口（600/720px）下，不重叠、不遮挡、不破版。
3. **横向布局挤压优先级（Shrink Priority）**：
   - 横向排布（如 Icon + Title + Action）空间不足时：
     - `Fixed Icon` (固定尺寸) → `Flexible Text` (优先压缩并 Ellipsis) → `Fixed Action` (固定按钮/开关)。
     - 严禁 Flexible 容器无约束导致把右侧 Action 挤出屏幕或文字覆盖图标。
4. **遮挡防御（Obscuration Audit）**：
   - **Safe Area**：处理 Notch、Status Bar、Home Bar、窗口控制按钮、折叠屏折痕。
   - **Keyboard 遮挡**：软键盘弹出时，当前焦点输入框必须保持可见（Scroll Into View），操作按钮不被永久遮挡。
   - **BottomBar 留白**：底部有 Fixed/Sticky Action Bar 时，滚动列表末尾必须预留 `BarHeight + SafeArea + Spacing` 底部 Padding。
   - **Dropdown / Tooltip 边界检测**：空间不足时自动向上反转展开或重定位，禁止被父容器 `overflow: hidden` 裁切。
5. **系统字体与浏览器缩放防御**：
   - 防御 `100%`, `125%`, `150%` 字体缩放及浏览器缩放。**严禁通过“禁止字体缩放”逃避适配**。
   - 容器与正文允许垂直自然延伸，但 Button, Header, Tab 必须保持防折行约束。
6. **国际化长文本防御**：
   - 假设英/德/法等语言文本长度可能增加 `30% ~ 100%`，标题 1 行 Ellipsis，避免硬编码文字宽度 `width: 120px`。
7. **交互状态自适应**：
   - 桌面/Web 必须具备明确的 `Focus` 状态环与平滑的 `Hover`（禁止 Hover 改变尺寸导致抖动）。
   - `Pressed` 不得改变整体尺寸（禁止 Border 1px 突变 4px）。
   - Z-Index 统一定义（Base, Sticky, Dropdown, Overlay, Modal, Toast, Tooltip），严禁写死 `999999`。

---

### 第 5 阶段：UI 规范审查与交付报告（Review & Delivery）

完成界面或组件实现后，生成结构化交付报告，逐项检查 8 大审查维度：

```markdown
## 🎨 统一跨平台 UI 设计规范审查与交付报告

### 📱 界面与模块
- **模块/页面名称**：`[Screen/Component Name]`
- **目标平台**：`[Web / iOS / Android / Desktop / Flutter / React / Compose]`
- **源文件路径**：`[FilePath]`

### 🔍 8 大维度审查清单
| 审查维度 | 检查项 | 状态 | 规范对齐说明 |
|---------|-------|------|-------------|
| **1. 视觉一致性** | 零 Magic Number，全部引用 Token | ✅ 通过 | 间距、圆角、字号全部对齐 Design Tokens |
| | 圆角分级统一 (4/8/12/16/20/Full) | ✅ 通过 | Card 16，Button 12，Dialog 20 |
| | 4/8 栅格体系与留白对齐 | ✅ 通过 | 默认 Padding 16，Section 留白 24，最大宽度受控 |
| **2. 按钮规范** | 按钮高度恒定 (52/44/36) | ✅ 通过 | 统一封装，高度不受文字多寡影响 |
| | 按钮文字单行不换行 (nowrap/ellipsis) | ✅ 通过 | maxLines=1，超长按优先级梯次截断 |
| | 触控区域 >= 40x40 (推荐 44~48) | ✅ 通过 | IconButton 点击区域受控 |
| **3. 组件复用** | 阻断私造组件，全量复用组件库 | ✅ 通过 | 无自定义裸写 Button/Card/Dialog |
| | Section 与分组卡片聚合 | ✅ 通过 | 避免单项散装卡片，使用标准 Divider 聚合 |
| **4. 文本与排印** | 页面字体等级 <= 3~5 种 | ✅ 通过 | 仅使用 Title/Body/Label，字重克制（非核心数据不加粗） |
| | 行高与跨端同级文字统一 | ✅ 通过 | 正文 1.5x 行高，跨页面同级字号严格一致 |
| **5. 响应式布局** | 响应式断点与流式适配 (Flex/Grid) | ✅ 通过 | 无写死绝对定位与固定像素宽，遵循 Shrink Priority |
| | 最小窗口/极窄屏 (320px) 稳健性 | ✅ 通过 | 按钮自动转 Column，无文字重叠破版 |
| **6. 边界与遮挡** | Safe Area / Keyboard / Sticky 留白 | ✅ 通过 | 底部内容预留 BottomBar 避让，输入框自适应上浮 |
| | Dropdown / Tooltip 视口溢出检测 | ✅ 通过 | 边缘自动反转定位，无视口裁剪 |
| **7. 弹性与缩放** | 字体放大 150% 布局稳定 | ✅ 通过 | 正文自然向下延伸，导航与操作栏不破损 |
| | 国际化长文案 (30~100% 扩张) 防御 | ✅ 通过 | 标题单行省略，按钮文案精简并防御超长 |
| **8. 主题与状态** | 语义色彩与 Dark Mode 适配 | ✅ 通过 | 无硬编码色值，深浅色切换对比度合规 |
| | 状态色彩统一 (Success/Warning/Error/Info) | ✅ 通过 | 全局语义色一致，Focus/Hover/Disabled 状态齐备 |

### 💡 核心设计亮点与复用组件
- [复用组件/Token 说明 1]
- [响应式自适应亮点 2]

### ⚠️ 注意事项与后续建议（如有）
- [后续待办或跨端平台原生适配说明]
```

---

## AI 行为绝对红线（严禁行为）

1. ❌ **严禁写死 Magic Number**（如 `13px`, `17px`, `19px`, `27px`, `37px`, `43px`）。
2. ❌ **严禁为单个业务页面新建异构组件**（如 `CustomButton`, `SpecialCard`, `NewDialog`）。
3. ❌ **严禁按钮文字自动换行**（必须 `nowrap / maxLines = 1`）。
4. ❌ **严禁按钮高度随文字长度动态变化**。
5. ❌ **严禁通过极端缩小子号解决按钮或布局溢出**。
6. ❌ **严禁直接写死色彩**（如 `#333`, `Color.Red`, `0xFF123456`, 纯白, 纯黑），必须使用语义 Token。
7. ❌ **严禁把每个列表项都做成独立 Card** 导致页面严重碎片化。
8. ❌ **严禁触控区域低于 40×40px**（推荐 44~48px）。
9. ❌ **严禁仅按本地固定大分辨率开发**，必须在代码中保障小屏与自适应。
10. ❌ **严禁轻量操作滥用 Dialog 弹窗**，轻量反馈使用 Snackbar/Toast。
11. ❌ **严禁主要内容使用绝对定位（Absolute Position）**。
12. ❌ **严禁横向排布中文字挤压覆盖图标或操作控件**。
13. ❌ **严禁忽略 Safe Area、键盘遮挡与滚动底部避让**。
14. ❌ **严禁通过“禁止系统字体缩放”逃避排版适配**。
15. ❌ **严禁随手乱写 `z-index: 999999`**，必须遵循统一 Z-Index 体系。
16. ❌ **严禁为了赶进度破坏 Design System**（“先随便做，以后再改”绝对禁止）。

---

## 冲突决策优先级

当遇到设计与空间冲突时，严格按以下优先级裁决：
```text
1. 可用性 (Usability)
   ↓
2. 内容可访问性 (Content Accessibility)
   ↓
3. 响应式稳定性 (Responsive Stability)
   ↓
4. 无障碍规范 (Accessibility / Screen Reader)
   ↓
5. 交互一致性 (Interaction Consistency)
   ↓
6. 视觉一致性 (Visual Consistency)
   ↓
7. 品牌风格 (Brand Style)
   ↓
8. 装饰效果 (Decorative Styling)
```

---

## 最终验收标准（17 项全票通过法则）

一个跨平台 UI 只有同时满足以下 17 项条件才算验收通过：
1. [ ] 视觉与排版统一：字号、行高全部来源于单一 Typography Token
2. [ ] 颜色统一：全部使用语义色彩，状态色语义全端一致
3. [ ] 按钮统一：尺寸分级恒定，文字单行不换行，空间不足按标准梯次处理
4. [ ] 组件统一：无临时私造组件，全部复用 Foundation 组件
5. [ ] 间距统一：严格对齐 4/8 栅格，无异构 Magic Number
6. [ ] 响应式正常：不同分辨率与窗口尺寸下自适应排版
7. [ ] 小屏不破版：320px 窄屏无水平溢出破损
8. [ ] 大屏不失控：超宽屏内容区域设置合理最大宽度
9. [ ] 字体放大不重叠：150% 字体缩放下正文自适应且关键控件不锁死
10. [ ] 按钮高度不失控：不随文字折行，高度始终恒定
11. [ ] 内容不被遮挡：无 Header/Footer/Floating 元素遮挡正文
12. [ ] 弹窗不超出屏幕：超出时 Header/Footer 固定，中间滚动
13. [ ] 导航不遮挡操作：底部栏与滚动列表预留充足 Padding 避让
14. [ ] 键盘不遮挡输入：聚焦输入框自动进入可视区
15. [ ] 下拉与浮层不被裁剪：Dropdown/Tooltip 自适应视口边界
16. [ ] Dark Mode 表现正常：深浅主题切换对比度达标
17. [ ] 跨平台体验一致：在不同系统下保持相同产品的品牌与视觉语义
