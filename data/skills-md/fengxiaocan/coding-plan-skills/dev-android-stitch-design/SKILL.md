---
name: dev-android-stitch-design
description: 遵循 Google Stitch 现代设计风格与统一设计系统规范的 Android UI/UX 设计与实现工作流。当用户要求创建 Android 页面、重构 UI、封装公共组件、编写 Compose 界面、优化交互视觉或审查 Android 界面规范时使用。由 /dev-android-stitch-design 命令触发。
---

# Dev Android Stitch Design — Stitch UI/UX Design System Workflow

**核心法则：UI 页面负责“组合组件”，Design System 负责“决定组件长什么样”。业务页面严禁自行发明视觉样式。**

整体设计风格参考 **Google Stitch** 所体现的现代移动端设计思路：**简洁、清晰、高信息层级、适量留白、统一圆角、统一字体体系、统一组件高度、统一颜色体系、克制装饰、高度稳定自适应**。

---

## 激活时行为

收到 `/dev-android-stitch-design` 或用户发起以下请求时触发：
- "创建/实现一个 Android 页面"
- "重构/优化现有界面 UI"
- "封装一套公共 Android UI 组件"
- "审查当前 Compose/XML 页面的样式规范"
- "适配 Android 界面小屏与深色模式"

触发后，AI 必须严格按照以下 **5 阶段工作流** 推进，严禁未经设计系统检查直接生成散乱代码。

---

## 5 阶段工作流程

### 第 1 阶段：资产扫描与设计系统盘点（Scan & Inventory）

在编写或修改任何页面前，AI 必须先扫描项目工程中现有的 Design System 资产：

1. **扫描基础 Token**：
   - 检查 `ui/theme/` 或对应资源目录是否存在：
     - `Color.kt`（语义色彩体系）
     - `Typography.kt`（文字排印层级）
     - `Shape.kt`（圆角分级）
     - `Dimensions.kt`（4dp 栅格间距与组件尺寸）
     - `Theme.kt`（Light / Dark 动态配色与 CompositionLocal）
2. **扫描公共组件库**：
   - 检查 `ui/components/` 是否已封装：
     - `AppButton` / `AppIconButton`
     - `AppCard`
     - `AppListItem`
     - `AppTextField`
     - `AppDialog` / `AppConfirmDialog`
     - `AppTopBar`
     - `AppSwitch` / `AppChip` / `AppDivider`
     - `AppLoading` / `AppEmptyState` / `AppErrorState`
3. **盘点决策**：
   - **已有完整 Design System**：后续阶段必须 100% 复用，严禁新建异构组件。
   - **部分缺失**：优先规划补充基础 Token 或公共组件，严禁在业务页面内直接硬编码临时组件。
   - **全新项目/完全缺失**：向用户提示并建议先初始化基础 Design System 结构，或依据标准 Stitch 规范先行搭建。

---

### 第 2 阶段：复用评估与信息架构规划（Audit & Architecture）

在动手编码前，进行界面层级规划与组件复用评估：

1. **信息层级设计（从上至下）**：
   ```text
   页面标题 (AppTopBar / Large Title)
   ↓
   当前最核心信息 / 状态卡片 (AppCard)
   ↓
   主要操作 (AppPrimaryButton)
   ↓
   次要分组与列表项 (AppSection + AppListItem)
   ↓
   次要操作 / 底部信息
   ```
2. **复用评估（严格阻断重复造轮子）**：
   - 严禁出现 `NewButton`、`CustomCard`、`SettingsItemView` 等业务专用组件。
   - 检查是否能通过现有 `AppButton(style = ...)` 或参数配置实现。
   - 检查重复模式：若页面内相同布局（如“图标 + 标题 + 副标题 + 开关”）出现 ≥ 2 次，必须抽象为通用公共组件（如 `AppSwitchListItem`）。
3. **Section 结构规范**：
   - 结构模式：`Section Title` (12~14sp Medium Secondary) + `AppCard` (Items 分隔线由 1dp Divider 划分)。
   - Section 之间留白：标准间距 `24dp`。
   - 严禁把每一行设置项拆成一个独立孤立卡片（禁止卡片泛滥碎片化）。

---

### 第 3 阶段：规范实现与代码构建（Strict Implementation）

实现 UI 时必须遵循以下硬性规范，逐条核对：

#### 1. 零 Magic Number 原则（强制）
- 严禁直接硬编码无依据数值：
  - ❌ 禁止 `fontSize = 17.sp`, `RoundedCornerShape(13.dp)`, `height(47.dp)`
  - ❌ 禁止 `padding(13.dp)`, `padding(19.dp)`, `padding(21.dp)`
  - ✅ 必须使用 `AppTypography.bodyMedium`, `AppShapes.medium`, `AppDimensions.buttonHeightMedium`

#### 2. 4dp Grid 栅格与间距系统
- 所有间距必须为 4dp 整数倍：
  - `2dp`：极小视觉微调
  - `4dp`：紧凑元素内边距
  - `8dp`：小元素间距
  - `12dp`：关联元素间距
  - `16dp`：标准内容间距、页面默认左右 Padding、标准 Card 内边距
  - `20dp`：中等间距、重点 Card 内边距
  - `24dp`：Section 区块间距、大屏页面边距
  - `32dp`：大区块留白
  - `48dp`：超大区块留白 / 标准触控尺寸

#### 3. 统一圆角体系（最多 4~5 级）
- `Small (8dp)`：Chip、小控件、Badge
- `Medium (12dp)`：输入框 (AppTextField)
- `Large (16dp)`：卡片 (AppCard)
- `XLarge (20dp)`：Dialog (AppDialog)、BottomSheet (20~24dp)
- `Full (50% / CircleShape)`：圆形按钮、Avatar、Icon 背景

#### 4. 文字排印体系（Typography）
- 整个页面常规字体大小不得超过 3~4 种：
  - `TitleLarge`：22sp / Medium 或 SemiBold（页面大标题）
  - `TitleMedium`：18sp / Medium（卡片标题、弹窗标题）
  - `TitleSmall`：16sp / Medium（子模块标题）
  - `BodyLarge`：16sp / Normal（列表主标题、重点正文）
  - `BodyMedium`：14sp / Normal（标准正文、输入框文字）
  - `BodySmall`：12sp / Normal（辅助提示、副标题、时间戳）
  - `LabelLarge`：14sp / Medium（主按钮文案）
  - `LabelMedium`：12sp / Medium（次按钮、Chip 文案）
  - `LabelSmall`：11sp / Medium（Badge、极小标注）
- **字重规则**：仅使用 `Normal`, `Medium`, `SemiBold`；**避免滥用 Bold**（仅用于关键金额/核心数据），严禁用连续加粗来做视觉层级，优先使用字号、颜色和留白。
- **跨页面一致性**：同一级别的信息（如不同页面的设置项标题）必须使用完全相同的 Typography。

#### 5. 按钮统一规范（绝对红线）
- 业务页面禁止直接使用裸 Compose 按钮：
  - 必须使用封装组件：`AppPrimaryButton`, `AppSecondaryButton`, `AppOutlinedButton`, `AppTextButton`, `AppIconButton`。
- **统一高度**：
  - Large Button：`52dp`
  - Medium Button：`44~48dp`
  - Small Button：`36~40dp`
  - 同类型按钮在任何状态、任何内容下高度必须恒定一致！
- **文本禁止换行**（强制设置）：
  ```kotlin
  maxLines = 1, softWrap = false, overflow = TextOverflow.Ellipsis
  ```
  - 严禁按钮因为文字过长自动折成两行（例如从 48dp 变成 72dp）。
- **空间不足处理优先级**：
  1. 第一优先级：缩短按钮文案（推荐 2~6 个汉字，原则不超过 8 个字；如“立即开始进行设备扫描”改为“开始扫描”）。
  2. 第二优先级：扩大按钮宽度（使用 `weight(1f)` 或拉通铺满）。
  3. 第三优先级：适度减少左右 Content Padding（如 `24dp` -> `16dp`）。
  4. 第四优先级：文字截断显示省略号 `TextOverflow.Ellipsis`。
  - **严禁**通过“自动换行”、“无限增加按钮高度”、“极端缩小子号”解决空间不足！
- **横向多按钮**：
  - 必须考虑最小宽度，使用 `weight()` 或响应式布局，禁止裸 `Row` 靠文字随意撑开。
  - 双按钮推荐：对称 `1f : 1f` 或 `取消(自适应/40%) : 保存修改(主要/60%)`。
- **触控区域**：
  - `AppIconButton` 即使视觉 Icon 是 20dp 或 24dp，**Touch Target 必须保留至少 48×48dp**。

#### 6. 语义颜色与深色模式（Dark Mode）
- 严禁裸写 `Color.Red`, `Color.Green`, `Color.White`, `Color.Black`。
- 必须使用语义色彩：
  - `Primary`, `OnPrimary`, `Secondary`, `OnSecondary`
  - `Background`, `Surface`, `SurfaceVariant`
  - `TextPrimary`, `TextSecondary`, `TextTertiary`
  - `Success`, `Warning`, `Error`, `Info`
  - `Divider`, `Outline`, `Disabled`
- 状态颜色全 App 严格一致（如“已连接”状态不得在不同页面使用不同色系）。
- 所有页面与组件必须原生支持 Light / Dark Theme 切换，文字与背景色联动自适应。

#### 7. 常用组件统一
- **AppListItem**：标准高度普通项 `56dp`，带副标题 `64~72dp`。标准三段式结构：`Leading Icon` + `Title & Subtitle` + `Trailing Action (Switch/Chevron/Text)`。
- **AppTextField**：标准高度 `52~56dp`，圆角 12dp，集成 Label, Placeholder, Error, Focus 状态。
- **AppDialog**：圆角 20dp，操作按钮控制在 1~2 个。超过 2 个操作转为 BottomSheet 或独立页面。小屏空间不足时，按钮由横向转为纵向单列排列，**严禁横向挤压换行**。
- **AppDivider**：粗细统一 `1dp`，颜色严格取自 Theme Divider，禁止随手写 `0.5dp` 或不透明度灰色。
- **轻量反馈**：保存成功、复制成功等轻量反馈优先使用 `Snackbar`，禁止滥用弹窗 Dialog 阻塞用户。

---

### 第 4 阶段：极端场景与多端自适应校验（Edge Cases & Responsiveness）

UI 实现后，必须在代码逻辑层面验证以下极端边界情况：

1. **多屏幕尺寸适配**：
   - 适配 `320dp`（小屏手机）、`360dp`（标准紧凑屏）、`411dp`（主流大屏）。
   - 折叠屏 / 平板（`>= 600dp`）：核心内容区必须设置最大宽度约束（`600dp / 720dp / 840dp`），居中对齐，严禁输入框或表单无限制横向拉伸至整屏。
   - 响应式断点（WindowSizeClass）：
     - Compact (< 600dp)：单栏流式布局
     - Medium (600~839dp)：宽内容区或适度双栏
     - Expanded (>= 840dp)：NavigationRail + Master-Detail 双栏/多栏
2. **系统字体缩放测试**：
   - 必须防御 `130%` 和 `150%` 系统超大字体设置。
   - 正文区域支持自然向上撑高，**但 Button, TopBar, Tab, Navigation 高度必须受到约束，按钮文字不得失控换行**。
3. **长文本防御**：
   - 标题必须声明 `maxLines = 1`, `overflow = TextOverflow.Ellipsis`。
   - 列表副标题最多 `maxLines = 2`。
   - 卡片描述最多 `maxLines = 3`。
4. **禁止失控 wrapContent**：
   - 对于 Button, Chip, Tab, TopBar, ListItem，严禁毫无约束地使用 `wrapContentHeight`。

---

### 第 5 阶段：UI 规范审查与交付报告（Review & Delivery）

完成页面或组件编写后，生成结构化交付报告，逐项检查 5 大维度：

```markdown
## 🎨 Android UI 规范审查与交付报告

### 📱 界面与模块
- **模块/页面名称**：`[ScreenName]`
- **对应源文件**：`[FilePath]`

### 🔍 5 大维度审查清单
| 审查维度 | 检查项 | 状态 | 规范对齐说明 |
|---------|-------|------|-------------|
| **1. 视觉一致性** | 零 Magic Number，严格使用 Token | ✅ 通过 | 字体全部来自 AppTypography，间距来自 Dimensions |
| | 圆角层级统一 (8/12/16/20/Full) | ✅ 通过 | 卡片使用 Large(16dp)，输入框 Medium(12dp) |
| | 4dp 栅格体系与留白 | ✅ 通过 | 外边距 16dp，区块间距 24dp |
| **2. 按钮规范** | 公共组件封装 (AppPrimaryButton 等) | ✅ 通过 | 统一封装，高度恒定 48dp |
| | 按钮文字单行不换行 | ✅ 通过 | maxLines=1, softWrap=false, ellipsis |
| | 触控区域 >= 48x48dp | ✅ 通过 | 所有 IconButton 点击区域 >= 48dp |
| **3. 架构与复用** | 复用现有公共组件库 | ✅ 通过 | 无重复造轮子，无异构 CustomButton |
| | Section 与分组卡片规范 | ✅ 通过 | 单卡片容纳多个 Item + 1dp Divider |
| **4. 边界与弹性** | 320dp 小屏与长文本防御 | ✅ 通过 | 标题单行省略，小屏无横向破损 |
| | 字体放大 (130%) 布局稳定性 | ✅ 通过 | 关键控件高度受控，正文自然自适应 |
| **5. 主题与状态** | 语义颜色 & Dark Mode 支持 | ✅ 通过 | 无硬编码颜色，Light/Dark 动态生效 |
| | 状态颜色统一 (Success/Error/Warning) | ✅ 通过 | 严格遵循语义状态色彩规范 |

### 💡 核心设计亮点与复用组件
- [复用组件 1]
- [复用组件 2]

### ⚠️ 注意事项与后续待办（如有）
- [待办项或建议]
```

---

## AI 行为绝对红线（严禁行为）

1. ❌ **严禁写死 Magic Number**（如 `17.sp`, `13.dp`, `47.dp`）。
2. ❌ **严禁为单个业务页面新建异构按钮**（如 `CustomButton`, `SpecialButton`）。
3. ❌ **严禁让按钮文字折行拉伸高度**。
4. ❌ **严禁在按钮空间不足时无限制增高或极端缩小字体**。
5. ❌ **严禁直接写死色彩**（如 `Color.Red`, `Color.White`, `0xFF123456`），必须从 Theme 语义色获取。
6. ❌ **严禁把每个列表项都做成独立 Card** 导致页面严重碎片化。
7. ❌ **严禁触控区域低于 48×48dp**。
8. ❌ **严禁仅按开发者本地大屏手机尺寸设计**，必须验证 320dp/360dp 小屏表现。
9. ❌ **严禁轻量操作滥用 Dialog 弹窗**。
10. ❌ **严禁为所谓的“科技感”乱加发光、高饱和霓虹与复杂花哨装饰**，始终保持 Google Stitch 现代克制留白美感。
