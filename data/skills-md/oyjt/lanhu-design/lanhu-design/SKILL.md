---
name: lanhu-design
description: "Use for Lanhu (蓝湖) UI design handoffs and lanhuapp.com design project links: list design screens, inspect screenshots and HTML/CSS specs, extract design tokens, download slices/assets, or implement UI. Trigger when the request explicitly mentions 蓝湖, Lanhu, lanhuapp.com, or the bundled Lanhu scripts. Do not use for standalone Figma/Sketch files, generic UI implementation, PRD/Axure docId links, or image editing unrelated to Lanhu."
license: MIT; see LICENSE.txt
compatibility: Requires Node.js 18+, network access to lanhuapp.com, and a valid LANHU_COOKIE environment variable.
metadata:
  author: oyjt
  version: 1.4.2
---

# Lanhu Design

## 概览

优先通过 `lanhu` CLI 读取 UI 设计稿、分析设计规格、获取切图信息，并把切图落到当前项目的资源目录。未安装 CLI 时继续使用内置脚本，Skill 仍可独立运行。

## 执行入口选择

开始工作前先探测 `lanhu` 命令：

```bash
command -v lanhu
```

- 命令存在：先运行 `lanhu auth status --json`，后续优先使用 `lanhu designs`、`lanhu image`、`lanhu specs`、`lanhu slices`、`lanhu download` 或 `lanhu export`，并为 Agent 调用加 `--json`。
- 命令不存在：检查 `LANHU_COOKIE`，继续使用下方 `scripts/*.mjs` 兼容入口。
- 不要在 Agent 工作流中自行全局安装 CLI；是否安装由用户或宿主环境决定。
- 业务命令不得自动扫描浏览器。需要授权时提示用户显式运行 `lanhu auth`；受限浏览器场景使用 `lanhu auth import`。

需要详细工具契约、返回结构和还原规则时，读取 `references/lanhu-design-tools.md`。
需要设计还原实现规则（CSS 值保真、DOM 结构映射、切图命名策略、目录选择、倍率指引）时，读取 `references/design-implementation-rules.md`。

## 前置条件

内置兼容脚本依赖 `LANHU_COOKIE` 环境变量。CLI 用户可以改用 `lanhu auth` 管理用户级凭据。蓝湖没有面向本 CLI 的公开 OAuth，Cookie 缺失或过期时会返回稳定认证错误。

获取 Cookie 的步骤：

1. 在浏览器打开 `https://lanhuapp.com` 并登录。
2. 按 F12（macOS 为 Cmd+Option+I）打开开发者工具，切换到 Network 标签页。
3. 刷新页面，在请求列表中点击任意 `lanhuapp.com` 请求。
4. 在 Request Headers 中找到 `Cookie` 字段，复制完整值（通常 200–500 字符）。
5. 将该值设置为环境变量 `LANHU_COOKIE`。

注意事项：

- Cookie 会过期（通常数天到数周），出现认证错误时需重新获取。
- Cookie 是敏感凭据，不要提交到版本控制或输出给用户。
- 所有脚本需要 Node.js >= 18（使用原生 fetch）。

## 脚本列表

| 脚本 | 用途 |
|------|------|
| `scripts/get_designs.mjs` | 列出蓝湖项目的设计图 |
| `scripts/get_design_specs.mjs` | **获取设计规格 HTML+CSS（主路径：DDS Schema；降级：Sketch JSON）** |
| `scripts/download_design_images.mjs` | 下载设计图原图到本地目录（视觉校验用） |
| `scripts/get_design_slices.mjs` | 获取单个设计图的切图/素材元数据 |
| `scripts/download_slices.mjs` | 从切图 JSON 批量下载切图文件 |
| `scripts/lanhu-client.mjs` | 共享 HTTP 客户端模块（被上述脚本引用，不直接运行） |
| `scripts/design-converter.mjs` | 纯转换模块（被 get_design_specs.mjs 引用，不直接运行） |

## 工作流

0. 确认 `LANHU_COOKIE` 环境变量已设置。如果首次运行脚本返回认证错误，提示用户检查 Cookie 是否已配置且未过期，参考上方「前置条件」重新获取。不要在认证失败后继续调用其他脚本。
1. 先判断用户给的是蓝湖 UI 设计项目链接，而不是需求文档链接。UI 设计项目通常是 `https://lanhuapp.com/web/#/item/project/stage?tid=xxx&pid=xxx`，必须有 `pid`，`tid` 可选；不要把带 `docId` 的 PRD 链接当设计稿处理。
2. 运行 `node scripts/get_designs.mjs <url>` 获取设计图列表。后续分析和切图都以这个列表里的 `index`、`name`、`id` 为准。
3. 如果设计图很多，先让用户指定范围；如果用户已经明确说"全部"，再用 `all`。不要默认一次分析大量设计图。
4. **【还原 UI 的强制前置步骤】查看或实现 UI 前，必须先下载并用 Read 工具查看设计图原图**：运行 `node scripts/download_design_images.mjs <url> --designs <names> --output <dir>` 下载原图，`--designs` 支持序号（逗号分隔）、精确名称或 `all`，下载后用 Read 工具实际查看。不要跳过看图直接基于 HTML 规格还原——原图是布局、层级、视觉效果的最终核对依据，`source="sketch"` 降级时更是布局结构的主力参考。
4.5. **获取设计规格 HTML+CSS**：运行 `node scripts/get_design_specs.mjs <url> --design <name_or_index>` 获取规格。返回的 `source` 字段决定数据权威性，必须先判断：
   - `source="dds"`：从 DDS Schema 生成的高精度 flex 布局 HTML+CSS，`html` 字段是颜色、字号、间距、渐变、圆角、布局等所有参数的权威来源，直接复用、不得主观修改；原图用于核对布局是否错位。
   - `source="sketch"`：降级路径，`html` 仅为绝对定位的元素清单，**不可当作布局权威**。此时以原图视觉为布局主力参考，以 `design_tokens` / `sketch_annotations` 的原始数值为精确数值来源。
   - `source="sketch"` 时，HTML 元素带 `data-css`，返回还包含 `design_scale` 和 `layer_css_annotations`，用于逐图层核对路径、文本、切图和 CSS 标注。
   - `image_url_mapping` 列出需要下载的图片资源映射表。若返回 `dds_error`，说明已降级到 sketch，应更依赖原图。
   - 返回的 `source_guidance` 字段是针对当前 `source` 的数据权威性指引，直接按它执行。
   - 加 `--output <dir> --download-images` 可在保存 HTML 的同时自动把引用图片下载到 `<dir>/assets/slices/`，使保存的 HTML 可直接在浏览器渲染核对。
5. 下载切图、图标、图片素材时，运行 `node scripts/get_design_slices.mjs <url> --design <name>` 获取切图 JSON。单次只传一个设计图名称或序号。
6. 下载前确认平台和倍率偏好。用户不指定时推荐 Web 2x，但仍要明确说明选择；常用键包括 `1x`、`2x`、`3x`、`ios_1x`、`ios_2x`、`ios_3x`、`android_mdpi`、`android_hdpi`、`android_xhdpi`、`android_xxhdpi`、`android_xxxhdpi`。除 `2x` 可回退到 `download_url` 外，其它倍率必须由切图 JSON 的 `scale_urls` 提供，不要复制同一文件伪造成多倍率资源。
7. 将步骤 5 的切图 JSON 输出保存为文件，然后运行 `node scripts/download_slices.mjs <json_file> --output <dir> --scale <scale>` 批量下载。识别当前项目资源目录和命名风格，执行后核对文件数量和失败列表。

## 设计还原规则

完整规则见 `references/design-implementation-rules.md`。以下是必须遵守的核心要求。

### 数据来源优先级（按 `get_design_specs.mjs` 返回的 `source` 分级）

还原前必须先看 `source` 字段，不同来源的权威性完全不同：

**`source="dds"`（高保真，HTML 权威）：**

1. **`html` 字段**：颜色、尺寸、间距、字体、圆角、渐变、定位、布局结构的权威来源。直接复制精确的 CSS 属性值，不得修改。
2. **`design_tokens` 字段**：补充 HTML 中可能被合并的高风险视觉信息（复合渐变、非均匀圆角、阴影、opacity<100）。
3. **设计图原图**：用于核对布局是否错位、元素是否齐全，不覆盖 HTML 数值。
4. **切图元数据（`get_design_slices.mjs`）**：补充 `fills`、`borders`、`opacity`、`rotation`、`text_style`、`shadows`、`border_radius`。

**`source="sketch"`（降级，原图为布局主力）：**

1. **设计图原图**：布局结构、层级关系、视觉效果的主力参考。`html` 是扁平的绝对定位元素清单，**不能当作布局权威**，仅用于核对元素是否齐全。
2. **`design_tokens` / `sketch_annotations` 字段**：颜色、字号、间距、圆角、阴影等精确数值的权威来源。
3. **`html` 字段**：仅作元素清单和绝对定位参考，布局意图需结合原图重建。
4. **切图元数据**：同上，补充视觉细节。

### 禁止修改 CSS 值

- 不要转换色值格式（`rgba()` ↔ hex 保持原样）。
- 不要四舍五入或简化数值（如 `0.30000001192092896` 保持原样）。
- 不要把 `linear-gradient` 简化成纯色。
- 不要调整 `font-family` 顺序或删除 fallback 字体。
- 不要把 margin/padding 取整为"干净"的数字。
- 不要用 SVG、CSS shape、emoji 或占位图替换切图。
- 不要省略任何可见的设计元素。
- 不要在最终代码中保留蓝湖远程 CDN URL。

### DOM 结构映射

HTML 的 class 名称表达布局意图，需转译为目标框架组件，同时保持 CSS 值不变：

- `flex-row` → 水平排列（React: `display:flex`，Flutter: `Row()`，SwiftUI: `HStack`）
- `flex-col` → 垂直排列（React: `flex-direction:column`，Flutter: `Column()`，SwiftUI: `VStack`）
- `justify-between` → 两端对齐（`space-between` / `MainAxisAlignment.spaceBetween`）
- `relative` / `absolute` → 定位层叠（Flutter: `Stack` + `Positioned`，SwiftUI: `ZStack`）

详细映射表见 `references/design-implementation-rules.md`。

### 框架检测与代码生成

实现 UI 前先检测项目类型（读取 `package.json`、`pubspec.yaml`、`build.gradle`、`Podfile` 等），生成匹配框架的代码（React JSX、Vue SFC、Flutter Widget、SwiftUI View、Android Compose 等）。CSS 属性需按平台做单位映射（px→dp/pt），但不能改变数值精度。未检测到框架时默认生成纯 HTML。各框架的 CSS 属性映射表和资源引用方式见 `references/design-implementation-rules.md`。

若项目根目录存在 `DESIGN.md`（或同等职责的设计系统文档），解析规格与落盘代码前必须先读取并遵守其令牌、排版、组件与命名约定；图层级具体数值仍以规格数据为准，冲突时以规格数值保证当前屏还原度并向用户说明取舍。详见 `references/design-implementation-rules.md`。

### 生成后保真审计

代码生成后必须逐属性对照设计规格 HTML+CSS 执行保真检查，覆盖 10 项：尺寸约束、裁剪、色值、渐变、绝对定位、字体、间距、图片资源、元素完整性、无远程 URL。对每个差异标注是平台适配还是错误，错误必须修正后交付。完整清单见 `references/design-implementation-rules.md`。

## 切图下载

从 `get_design_slices.mjs` 保存返回结果为 JSON 后，可运行：

```bash
node scripts/download_slices.mjs slices.json --output ./src/assets/images/slices/home --scale 2x
```

常用参数：

- `--scale 2x`：下载 Web 2x，文件名后缀默认 `@2x`。
- `--scale ios-all`：下载 iOS `1x/@2x/@3x`。
- `--scale android-all`：下载 Android 全套并放入 `mipmap-*` 子目录。
- `--name-map names.json`：提供 `{slice_id_or_name_or_layer_path: "semantic_name"}`，覆盖自动文件名。
- `--referer https://lanhuapp.com/`：需要带 Referer 时使用。

脚本只负责稳定下载和基础去重。语义化命名应优先结合当前项目已有命名规范处理。
全套倍率依赖 `scale_urls` 中的真实多倍率地址；缺失时脚本会报错而不是复制 `download_url`。
Photoshop 稿（设计 JSON 根节点 `type=ps`）的切图登记在 `assets[]`，脚本会自动按图层 id 提取 `png_xxxhd`/`svg` 地址并推导多倍率（PS 稿图层像素尺寸为 @2x 基准）。

### 切图下载前置步骤

下载切图前，按以下顺序准备：

1. **识别项目类型**：检查 `package.json`、`pubspec.yaml`、`*.xcodeproj`、`build.gradle` 等标志文件，判断 React/Vue/Flutter/iOS/Android。
2. **确定输出目录**：用户指定 > 项目已有资源目录 > 通用默认路径。详细规则见 `references/design-implementation-rules.md`。
3. **确认倍率**：用户不指定时推荐 Web 2x，但必须明确告知选择。
4. **准备命名映射**：根据切图的 `layer_path`、`parent_name` 生成语义化英文文件名（`icon_`、`bg_`、`btn_` 等前缀），沿用项目已有命名风格。命名策略详见 `references/design-implementation-rules.md`。

## 完成检查

交付前确认：

- 已先运行 `get_designs.mjs` 并基于列表匹配目标设计图。
- 还原 UI 前已下载并用 Read 工具实际查看过设计图原图。
- UI 实现已按 `source` 分级核对：`dds` 以 HTML+CSS 为权威，`sketch` 以原图布局 + `design_tokens` 数值为主，没有用设计截图主观改 DDS 的精确值。
- 已执行生成后保真审计（10 项清单），所有错误已修正，仅保留合理的平台适配差异。
- 生成代码匹配检测到的项目框架，遵循项目已有约定（命名、目录、样式方案）。
- 所有远程图片/切图已下载为本地资源，代码中没有蓝湖 CDN URL。
- 图片资源使用目标框架约定的引用方式（如 React `import`、Flutter `AssetImage`）。
- 切图下载数量、失败数量、输出目录已向用户说明。
- 中间产物已按 `references/design-implementation-rules.md` 的「临时文件清理规则」处理：先列出候选路径并检查引用，取得用户明确确认后再删除；仅保留被代码引用的切图文件。用户未确认时保留文件并报告路径。
- 工作流中未出现认证错误。如果出现过，已引导用户刷新 Cookie 并重试。

## 交付输出

最终回复简要列出：处理的设计图和 `source`、新增或修改的代码/资源路径、切图下载成功与失败数量、执行的验证及结果、仍需用户处理的认证或平台适配事项。不要输出 Cookie、带认证参数的完整请求头或不必要的远程资源 URL。
