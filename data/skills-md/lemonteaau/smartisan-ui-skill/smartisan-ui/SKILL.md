---
name: smartisan-ui
description: 用 Smartisan OS（锤子科技 / 坚果手机）的 UI 风格做前端界面：轻拟物、细腻纵向渐变、极细描边、柔和投影与内凹阴影、灰阶为主 + 低饱和蓝强调 + 锤子红品牌色。当用户提到 Smartisan、锤子、锤子风格、坚果 OS、Smartisan OS、老罗/罗永浩那种拟物风、"像锤子手机一样的 UI"，或要求把网页/组件/App 原型做成这种风格时使用。适用于网页（HTML/CSS/Tailwind/任意前端框架）和 Flutter。内含完整的 Figma《Smartisan OS UI Kit (Unofficial)》（17 页、全部组件和变体）提取出的 token、组件规格、可直接引用的 CSS、Tailwind preset、图标和参考截图，并经 Smartisan R2 真机校对。
---

# Smartisan OS UI 风格

来源：
- Figma 社区文件 [Smartisan OS UI Kit (Unofficial)](https://www.figma.com/community/file/1419385240874679870)，作者 Paix Chan，CC BY 4.0，基于 Smartisan R2 上的 Smartisan OS 8。所有数值都从 Figma 节点里读出，17 页、每个组件和每个变体都覆盖到了。
- 在一台真机 Smartisan R2（Smartisan OS 8.5.3）上用 adb 校对：屏幕 dp 宽度、字体、真实页面底纹、App Bar 阴影、列表图标颜色等，文档里标 **[R2]**。

## 文件

| 文件 | 用途 |
|---|---|
| `assets/smartisan.css` | 全部 token（CSS 变量）+ 全部组件类 `.s-*`。**做网页时优先直接引用这一份** |
| `assets/smartisan.js` | 可选的交互小工具：滑块进度自动同步、对话框开关（`data-s-open` / `data-s-close`、点遮罩和 Esc 关闭）、`Smartisan.toast()` |
| `assets/flutter/*.dart` | **Flutter 版**：token（`smartisan_theme.dart`）、23 个矢量图标（`smartisan_icons.dart`）、全部组件（`smartisan_widgets.dart`），只依赖 Flutter SDK。用法见 `references/flutter.md` |
| `assets/demo.html` | 整套 Kit 的 1:1 复刻：17 页，每个变体都有，外加一块"Real device"展示板。拿不准 HTML 结构时照抄这里 |
| `assets/icons-sprite.svg` | 29 个图标的 `<symbol>`：单色 `si-*`（`currentColor`）+ 彩色 `si-c-*`。内联到 `<body>` 开头后用 `<svg class="s-icon"><use href="#si-back"/></svg>` |
| `assets/icons/*.svg` | 29 个原始图标（保留原渐变） |
| `assets/icons/variants/*.svg` | Figma 里各组件实际用到的上色版本（白色 App Bar 图标、Chip 五色、列表按下/禁用态、底部导航选中/未选中） |
| `assets/kit-renders/*.svg` | 旋钮按钮、开关、滑块的原始矢量渲染，用于像素级核对 |
| `assets/brand/*.svg` | Kit 封面和页头用的 T 标、字标、UNOFFICIAL 徽标（商标归属见 README，只用于展示页，不要用在产品里） |
| `assets/tokens.json` | W3C DTCG 格式的 token，保留 Figma 变量名 |
| `assets/tailwind.preset.js` | Tailwind preset（`bg-s-grey-100`、`rounded-s-lg`、`shadow-s-card`……） |
| `references/tokens.md` | 颜色 / 渐变 / 字体 / 圆角 / 描边 / 阴影 / 尺寸全表，含 [R2] 实测值 |
| `references/components.md` | 每个组件的 HTML 结构、尺寸、所有状态的取值 |
| `references/flutter.md` | Flutter 接入步骤、CSS→Flutter 组件对照、常见错误 |
| `references/inventory.md` | Figma 节点清单：节点 ID → 组件 / 变体 → CSS 类 → 截图 → 素材 |
| `references/screenshots/NN-*.png` | 17 个 Figma 页面的截图，作为视觉对照 |

## 工作流程

**先判断技术栈**：
- **Flutter 项目** → 读 `references/flutter.md`，把 `assets/flutter/*.dart` 复制到 `lib/smartisan/`，然后用 `S*` 组件写页面。不要直接用 Material 控件，也不要从 CSS 自己翻译。
- **React / Vue / 原生 iOS / Android 等其它栈** → 按 `references/components.md` 和 `assets/tokens.json` 实现，外观以 `references/screenshots/` 为准。
- **网页（HTML / CSS / 任意前端框架）** → 走下面的步骤。

1. **先看 `assets/demo.html`** 里对应组件的写法；需要精确数值时查 `references/components.md` 和 `tokens.md`；不确定长什么样时，直接看 `references/screenshots/` 里那一页的截图（可以用 Read 读图）。
2. **把 `assets/smartisan.css` 复制进项目**（或移植到项目现有的样式体系：Tailwind 项目用 `tailwind.preset.js`，CSS-in-JS 项目读 `tokens.json`）。不要凭感觉重新调色。
3. 根元素加 `class="s-page"`；想要真机那种竖条纹底，再加 `s-page--textured`。
4. 把 `icons-sprite.svg` 内联到 `<body>` 开头。注意它的隐藏方式是 `position:absolute; width:0; height:0`，**不能改成 `display:none`**，否则彩色图标里的渐变不会渲染。
5. 交互部分可以引入 `assets/smartisan.js`：
   - 对话框和 Toast 用 `hidden` 属性控制显示和隐藏；
   - `<button data-s-open="dlg">` 打开对话框，对话框里的 `data-s-close` 关闭它；
   - `Smartisan.toast('已保存')` 弹出提示，它会自动放进 `.s-toast-host`；
   - 滑块的进度条填充（`--p`）会自动更新。

   App Bar 里要放文字按钮时，用 `.s-btn.s-btn--sm`（主操作，如"完成"）或 `.s-btn--outline`；只放纯文字用 `.s-appbar__text`。列表行里要放占满剩余宽度的控件（如音量滑块），给控件加 `.s-list-item__control`。
6. 用户要 React / Vue 组件时，按 `.s-*` 的结构和 `components.md` 的状态表来封装：pressed、disabled、selected 都要做齐。`.is-pressed` 可以用来静态展示按下态。
7. 做完后按下方「自检清单」逐条检查；有浏览器的话截图和 `references/screenshots/` 对比。

## 美学要点（为什么看起来像锤子）

1. **轻拟物，不是扁平**。可点的东西都有"实体感"：主按钮是上浅下深的蓝色渐变，加 0.8px 深蓝描边和向下 4px 的短投影；圆形按钮是凹槽底座里嵌一颗白色旋钮；开关、滑块轨道、滚轮选择器、Tab 选中态、左滑操作托盘都是**内凹**的（inset shadow）。
2. **渐变极其克制**。几乎所有渐变都只是同色系 2–5% 的明度差（`#5b87eb→#5883eb`、`#fff→#fcfcfc`），用来制造光照感；图标也带一层几乎看不出的 `#8c8c8c→#989898` 渐变。不要做成炫彩渐变。
3. **极细描边**。普遍是 0.4 / 0.5 / 0.8px，颜色只比背景深一点（`#e2e2e2`、`#eee`）。[R2] 在 2.5x 屏上 0.8dp 正好是 2 个物理像素。
4. **灰阶文字体系**。正文 `#333`；标题栏和按钮文字 `#636363`；副标题 `#7f7f7f` / `#9d9d9d`；禁用 `#bababa`。标题也用灰色加粗，**不用纯黑**。
5. **强调色少而低饱和**：蓝 `#5b87eb` 用于主按钮、选中、进度，对话框主操作用 `#5e80d0`；锤子红 `#cd3f3a` 用于品牌 App Bar（如 App Store），红色圆形图标（红勾、删除）用 `#e5645a`；暖黄 `#fcf6e6` 配棕字 `#ad8a67` 用于 Toast。
6. **居中对称**。App Bar、对话框、底部弹窗的标题都绝对居中，左边返回、右边操作。
7. **卡片式分组列表**：白底，圆角 10，0.8px `#e2e2e2`，极淡的大范围投影 `0 10px 16px rgba(0,0,0,.04)`；行高 60，行间 0.8px `#f2f2f2`；分组标题在卡片外上方（14px 600 `#7f7f7f`），说明文字在卡片下方居中。[R2] 真机设置页一致，卡片左右边距 12dp。
8. **按下态是换色或下沉，不是涟漪**。主按钮按下变纯色 `#4772e6`；白按钮按下 `#f8f8f8`；旋钮按下变 `#ebebeb→#f2f2f2`；对话框按钮按下 `#dfdfdf`；列表行按下整行变蓝 `#5985eb`、文字变白。不要用 Material ripple，也不要 hover 放大。
9. **禁用**：主按钮整体 `opacity: .3`；列表和文字用 `#bababa`，图标用 `#c6c6c6→#c8c8c8`。
10. **页面层次**：页面底 `#f5f5f5`（[R2] 真机是 `#f0f0f0` 加 3.6px 宽、`#eeeeee` 的竖条纹）；内容块白色；底部弹窗正文区更深（`#efefef`），和白色按钮形成层次；App Bar 下方 [R2] 有一道约 8px 的渐隐阴影（`.s-appbar--shadow`）。
11. **字体**：[R2] 系统字体是 **Smartisan Compact**（拉丁字符）+ **Noto Sans CJK SC**（中文）；Figma Kit 用 Inter 替代。字体栈已经按这个顺序写好。

## 核心 token 速查

```
页面底        #f5f5f5（[R2] #f0f0f0 + 竖条纹）  分隔线 #f2f2f2   描边 #e2e2e2 / #eeeeee
正文          #333333   标题/按钮字 #636363   副标题 #7f7f7f / #9d9d9d   禁用 #bababa
主蓝渐变      #5b87eb→#5883eb  描边 #3f68e2   按下 #4772e6 / 描边 #2f54d7   文字按钮 #5079d9
对话框主操作  #5e80d0   对话框按钮底 #f7f7f7（按下 #dfdfdf）   遮罩 rgba(0,0,0,.6)
锤子红        App Bar #cd3f3a→#c83530 底边 #b7241f；红色图标 #e5645a→#e55f55 描边 #da463e
图标灰        #8c8c8c→#989898（纯色 #929292）；禁用 #c6c6c6→#c8c8c8；> 箭头 #b2b2b2
圆角          3 分段 / 4 小按钮 / 6 菜单·Tab·Toast·输入框 / 8 弹窗按钮 / 10 大按钮·卡片 / 12 对话框 / 20 底部弹窗顶 / 100 胶囊
字体          18 粗(对话框标题) 16 粗(栏标题/按钮) 16 常规(列表标题) 14 粗(小按钮/对话框操作) 14 半粗(分组标题) 12 常规(副标题) 12 半粗(Chip) 8(底部导航)
尺寸          App Bar 48 · 列表行 60 · 大按钮 60 · 弹窗按钮 48 · 对话框操作 54 · 底部导航 54 · 菜单项 42 · Chip 30 · 开关 52×24 · 单选 22
设计宽度      432dp（[R2] 1080px ÷ 2.5）；大按钮 408、弹窗按钮 392、对话框 368
```

## 组件清单（Figma 页 → CSS 类）

- **App Bar**：`.s-appbar`，红色版 `--red`，真机阴影 `--shadow`
- **Button**：
  - 大按钮 `.s-btn`，小按钮 `--sm`，白色弹窗按钮 `--sheet`，描边按钮 `--outline`，文字按钮 `--text`
  - 图标按钮 `.s-btn-icon`
  - 圆形旋钮按钮 `.s-round-btn`，小号 `--sm`
  - 分段按钮 `.s-segmented`
- **Bottom Navigation**：`.s-bottom-nav`
- **Bottom Sheet**：`.s-sheet`、`.s-sheet__header`
- **Chip**：`.s-chip`
  - 颜色：默认白 / `--yellow` / `--blue` / `--red` / `--grey`
  - 样式：默认纯文字 / `--all` / `--leading` / `--trailing`
- **Date Time Picker**：`.s-picker`
- **Dialog**：
  - `.s-overlay` + `.s-dialog`
  - 标题 `__header`，正文 `__body`（`--flush` / `--field`），按钮组 `__actions`（1–3 个按钮，主操作加 `data-primary`）
  - Simple Dialog `.s-dialog--simple`，输入框 `.s-textfield`
- **Radio**：`.s-radio`、`.s-radio-item`
- **Divider**：`.s-divider`，竖线 `--v`，短竖线 `--short`
- **List**：
  - 分组 `.s-list-group`，卡片 `.s-list`，行 `.s-list-item`，尾部 Detail `__detail`
  - List Tile 2 `--simple`，List Tile 3 `--plain`
  - 左滑操作行 `.s-swipe`
- **Popup Menu**：`.s-menu`
- **Search**：`.s-search`、`.s-search-field`、结果行 `.s-result`、整体 `.s-search-with-result`
- **Slide Bar**：`.s-slider`（`<input type="range">`，用 `--p` 设进度），配 `.s-slider-row` 或 `.s-slider-card`
- **Switch**：`.s-switch`
- **Tab Bar**：`.s-tabs`
- **Toast**：`.s-toast`
- **文档外框**（用于做设计规范 / 展示页）：`.s-kit-canvas`、`.s-kit-board`、`.s-kit-header`、`.s-kit-set`、`.s-kit-label`、`.s-kit-cover`

## Figma 原稿里的坑（已在 skill 里纠正）

- Segmented Button 单项的变体名是反的：`Selected=False` 才是蓝块。
- `icon-down` 的 `direction=up` 和 `direction=down` 两个变体也是反的，文件已按实际形状命名为 `chevron-up` / `chevron-down`。
- 播放三角的外接框故意向右偏约 3.8px，这样三角形的视觉重心才落在圆心（光学居中）。sprite 里的 `si-play` 已经带了这个偏移，**不要再额外加 margin**。旋钮按钮里图标的尺寸按 CSS 写的来：大号 28px，小号 10px。
- 搜索框单独使用时描边是 `#e9e9e9`，放进搜索栏后是 `#e2e2e2`。
- 每页的展示板底色是 `#f5f5f5`，只有 Tab Bar 页是白色。

## 不要做

- 不要用大圆角卡片、大面积彩色渐变、毛玻璃（那是 iOS / 现代 Web 的风格，不是锤子）。
- 不要用高饱和色、纯黑文字、粗边框、重投影。投影透明度基本 ≤ 0.1，只有圆形旋钮到 0.21。
- 不要用 Material 的 ripple、FAB、浮动标签输入框、底部 Snackbar。
- 开关不要做成 iOS 那种绿色胶囊。锤子的开关是白色凹槽里一颗白色拨钮，另一侧露出一个小圆点作指示：开时拨钮在右、左侧露蓝点；关时拨钮在左、右侧露灰点。
- 主色不要泛滥，一屏通常只有一个蓝色主按钮或一个选中态。

## 自检清单

- [ ] 页面底是 `#f5f5f5`（或真机条纹），内容块白色，没有纯黑文字
- [ ] 描边都 ≤ 0.8px，颜色是 `#e2e2e2` / `#eee` / `#f2f2f2` 这一档
- [ ] 主按钮、开关、滑块、Tab 选中、旋钮都有渐变或内凹，不是纯平色块
- [ ] 所有可点元素都有按下态（换色 / 下沉），禁用态正确
- [ ] 标题居中；列表行高 60；对话框宽 368、按钮高 54、主操作在最右
- [ ] 图标是灰色细线风格（2px 圆头），尺寸是 16 / 20 / 24
- [ ] 和 `references/screenshots/` 里对应页面对比过

## 适配说明

- 原稿是 432dp 宽的手机界面。做移动端页面时，内容区 `max-width: 432px` 居中最接近原貌；做桌面网页时组件尺寸保持不变，用灰底加白色卡片分组来铺开，不要把按钮、行高等比例放大。
- 0.4px 描边在 1x 屏上会显示成 1px，这是正常的。
- Kit 没有定义暗色模式，[R2] 上的系统也没有暗色。用户要暗色时要说明这是推导出来的，并保持同样的"低对比渐变 + 细描边 + 内凹"逻辑。
- 滚轮选择器、左滑行这两类组件，CSS 只负责外观，交互（滚动吸附、拖拽）要另外写。
