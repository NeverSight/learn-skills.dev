---
name: replicate-macos-app
description: Use in Codex when the user wants to replicate (复刻) or rebuild a closed-source macOS app as a standalone app with full source code, or wants only this skill's toolchain installed and checked. Requires Codex on the Mac where the original app is installed.
---

# macOS 闭源 App 复刻

## 目标

把闭源的原版 App（下文称 **A**）复刻成新 App（下文称 **B**）。B 的界面和 A 一致，A 的正常功能在 B 上都能用；B 有完整源码，能在没有 A 的 Mac 上构建和运行。

- **范围**：A 访问的服务端分两类。服务器由用户配置、或按公开协议和公开 API 提供的服务（数据库、SSH/SFTP、Git、WebDAV、S3、IMAP、用户自备密钥的 API 等），B 实现对应的客户端功能。A 的开发商为 A 运营的私有服务端（账号、云同步、团队协作、在服务端完成的处理，以及试用、购买、激活和更新检查），B 不实现、不调用它的接口，也不显示 A 的许可状态。
- **语言**：B 只支持探索 A 时的系统语言。
- **命名**：B 默认叫 `<A 的名称>-replicate`，A 的名称依次取 `CFBundleDisplayName`、`CFBundleName`、`.app` 文件名，例如 SQLiteFlow 的复刻版叫 SQLiteFlow-replicate。B 的 `.app` 文件名、`CFBundleName` 和 `CFBundleDisplayName` 都用这个名称，并使用自己的 bundle identifier、配置目录和数据目录。
- **来源**：B 的源码依据 A 的行为重新编写，交付时这样向用户说明。A 的代码和资源（反编译结果、包里的 JS 和脚本、图标、图片）只作分析材料，不放进 B。

## 运行环境

本 Skill 只支持 Codex，并且要在 A 所在的 Mac 上运行。当前环境不是 Codex 时，告诉用户后停止。不在 A 所在的 Mac 上时，只写代码和做平台无关的工作，汇报时说明还没有观察 A。

## 分工

本 Skill 负责复刻的范围、阶段顺序、记录和每个阶段的完成标准，分析和构建交给专门的工具。用到某个工具时，先读取它的 Skill，按其中的流程选择具体工具和参数：

| 工作 | 负责的工具 |
| --- | --- |
| 分析 A 的包、代码和内部逻辑 | REA：读取 `reverse-engineer-anything` Skill，使用 REA MCP |
| 在 A 和 B 上截图、点击、输入 | Computer Use |
| 导出 A 和 B 的 AX 树，记录设置和文件的变化 | 本 Skill 的 `ax` 和 `state_diff.py` |
| 构建、运行和调试 B | Build macOS Apps 插件中的 Skills |

REA、Computer Use 和 Build macOS Apps 的安装和连接核对见 [references/setup.md](references/setup.md)。用户只要求准备工具时，按 setup.md 完成后停止。

## 规则

- 付费购买、使用账号、更改系统安全设置、破坏性的系统修改，以及上传或发布 A 的资源、分析材料和 B 的源码，先取得用户授权。
- 探索时使用合成文件和隔离目录。A 的 `.app` 保持只读，包里的样例文件复制到隔离目录再打开；修改 A 的设置前记下原值，测完恢复。
- 写进记录的凭据和个人数据先脱敏。
- A 无法操作（屏幕锁定、缺少权限、A 无响应）时，告诉用户需要做什么，写进 `progress.md` 的「等待用户处理」，同时推进不依赖 A 的工作。连续的 GUI 操作前运行 `caffeinate -di -t 秒数`，防止中途锁屏。

## 记录

`SKILL_DIR` 指本 Skill 所在目录，`PROJECT_DIR` 指复刻项目目录，脚本一律用绝对路径运行。记录放在 `PROJECT_DIR/replica/`：

| 路径 | 内容 |
| --- | --- |
| `spec.md` | A 的规格，每个界面和每个功能一节；实现和对照都以它为准 |
| `progress.md` | 当前阶段、下一步、工具状态、构建和启动命令、等待用户处理的事项 |
| `evidence/` | 截图、AX 导出、REA 结果、状态快照等工具的原始输出 |
| `app.json` | A 的路径、bundle identifier 和版本，供脚本读取 |

每做完一步就更新 `spec.md` 和 `progress.md`。接手已有项目时，先读这两个文件。

## 流程

### 1. 确定目标

1. 用户给出的 App 和项目位置直接使用。不知道目标时，只问 App 名称或路径，并解析到本机唯一的 `.app`。没指定项目位置时，用当前空目录或已有的复刻项目，都没有就在当前目录下新建以 B 的名称命名的子目录。
2. 初始化项目：

   ```bash
   python3 "$SKILL_DIR/scripts/init_project.py" PROJECT_DIR --app-path APP_PATH
   ```

   它创建上表的记录，并编译 AX 工具 `replica/bin/ax`；已有的文件保持不变。不需要 AX 时加 `--skip-ax`。
3. 按 setup.md「连接核对」确认要用的工具能用。
4. 弄清 A 访问哪些服务端，按「目标」判断各属于哪一类：先让 REA 从 A 的代码和字符串中找出域名、协议和认证方式的线索，再按 [references/methods.md](references/methods.md) 中对应的方法核实。A 的核心功能大多依赖 A 的私有服务端时，告诉用户复刻后能保留的范围，由用户决定是否继续。

### 2. 探索 A

把 A 的每个界面和每个功能写进 `spec.md`，内容以 A 实际运行时的表现为准。前两步从包里得到的入口是找功能的线索，每条都要在 A 上找到对应的界面或功能，或写进「不复刻」。

1. **分析包**：每个 A 都交给 REA 分析，原生 App 和 Electron 等跨平台 App 都一样。读取 `reverse-engineer-anything` Skill，让 REA 分析 A 的 `.app`，回答下面的问题，原始输出存到 `evidence/rea/`：
   - A 由哪些部分组成：主程序、嵌套 bundle（扩展、XPC、Helper、登录项）、内嵌框架，以及开源依赖的名称和版本。
   - Info.plist 声明了哪些入口：文档类型、导入和导出的类型、URL scheme、服务、权限说明。
   - 界面里定义了哪些窗口、面板、菜单项及其 action：原生 App 解析编译后的 nib 和 storyboard；Electron App 分析 JS 代码中的窗口、IPC 通道和模块。
2. **读取资源**：REA 不解析的资源用脚本读取：

   ```bash
   python3 "$SKILL_DIR/scripts/bundle_scan.py" PROJECT_DIR
   ```

   它把开发语言的文案、AppleScript 字典、App Intents、帮助文档，以及包里的 SQLite 表结构、Core Data 模型和数据文件写进 `evidence/bundle/`。
3. **界面**：逐个进入 A 的每个界面状态：主窗口、打开文档后、每个设置页、每个对话框和 sheet、每种右键菜单、菜单栏图标的面板。每个状态用 Computer Use 截图，导出 AX 树，在「界面」下写一节。导出 AX 树：

   ```bash
   "$PROJECT_DIR/replica/bin/ax" dump BUNDLE_ID > "$PROJECT_DIR/replica/evidence/ax/<状态>.txt"
   ```

   导出里的 `frame` 是控件相对窗口的位置和尺寸，实现布局时直接使用。`ax perform BUNDLE_ID 路径` 按路径点击元素。
4. **功能**：逐个操作每个入口，把触发方式和 A 的实际结果写在「功能」下。一节是一次可以单独验证的操作；同一操作的菜单项、快捷键和按钮写在同一节；每个影响行为的设置项也单独写一节。菜单和窗口之外，还要检查快捷键、拖放、文件关联、URL scheme、撤销重做、多窗口、首次启动、退出和重启恢复，以及权限被拒绝时的表现。偏好设置和文件的变化用快照比较：

   ```bash
   python3 "$SKILL_DIR/scripts/state_diff.py" snapshot PROJECT_DIR before --path TEST_DIR
   # 在 A 上执行操作
   python3 "$SKILL_DIR/scripts/state_diff.py" snapshot PROJECT_DIR after --path TEST_DIR
   python3 "$SKILL_DIR/scripts/state_diff.py" diff PROJECT_DIR before after
   ```

5. **内部逻辑**：操作看不出来的行为（算法、文件格式、默认值、内部规则、同一操作走了不同的路径），先写下要回答的问题和几种可能的解释，再交给 REA，从相关的界面文案、action、常量或符号追到实现。REA 的结论用 A 上的实验验证后，再写进 `spec.md`。REA 回答不了的问题，按 methods.md 选其他方法。
6. **不复刻**：依赖 A 私有服务端的入口，以及系统提供、B 自动具备的菜单（例如「服务」子菜单），写进「不复刻」并注明原因。

`spec.md` 的写法：

```markdown
## 界面

### 设置 > 通用

- 到达：Synthetic > 设置…，点工具栏「通用」
- 截图：`evidence/screens/settings-general.png`
- AX：`evidence/ax/settings-general.txt`
- 外观：窗口 480×320，不可缩放；两列表单，标签靠右，控件靠左；底部没有按钮，改动立即生效
- 对照：未开始

## 功能

### 导出为 PDF

- 入口：`MenuBar > MenuBarItem[文件] > MenuItem[导出为 PDF…]`，⌥⌘E
- 前置：已打开文档；没有文档时菜单项禁用
- 结果：弹出保存面板，默认文件名为文档名；输出 A4 纵向，页边距 2 cm
- 保留：记住上次导出的目录
- 对照：未开始

## 不复刻

- `MenuBar > MenuBarItem[Synthetic] > MenuItem[登录…]`：依赖 A 的私有服务端（账号）
- `MenuBar > MenuBarItem[Synthetic] > MenuItem[服务] > **`：系统提供的服务子菜单
```

AX 路径从 A 的导出中原样复制，写在反引号里。随文档或数据变化的标签（窗口标题、最近打开的文件）写成 `Role[*]`，匹配同一角色下的任意标签。路径末尾加 ` > **`，表示连同它下面的全部元素。Apple 菜单、分隔线、窗口的关闭/最小化/缩放按钮，以及表格和列表里随数据生成的元素，不需要写。

完成标准：`evidence/rea/` 和 `evidence/bundle/` 中的每个入口都在 `spec.md` 有对应的节或写进了「不复刻」；`python3 "$SKILL_DIR/scripts/spec_check.py" PROJECT_DIR` 没有错误，「界面」每一节都有截图、AX 导出和外观描述，「功能」每一节都写了入口和结果。检查输出中，`uncovered` 列出 A 的 AX 导出里还没写进 `spec.md` 的可操作元素（`--all` 列出全部），`errors` 列出全部问题。AX 确实读不到 A（例如整个界面自绘）时，在 `progress.md` 写明原因，按截图逐个清点控件，检查时加 `--no-ax`。

### 3. 实现 B

构建、运行和调试 B 交给 Build macOS Apps：每项工作开始前，读取插件中与它相关的 Skills（例如 `build-run-debug`、`swiftpm-macos`、`swiftui-patterns`、`appkit-interop`、`window-management`），按其中的流程进行。复刻另有以下要求：

- **技术栈**：原生界面通常用 SwiftUI + AppKit；复杂编辑器等场景有更合适的技术栈时直接采用。
- **界面**：按 `spec.md` 的截图、外观描述和 AX 导出里的 `frame` 实现。图标和图片自己绘制，或使用 SF Symbols 和可合法使用的开源资源。
- **功能**：全部是真实逻辑。按钮连到真实操作，状态变化、文件读写、错误提示、持久化、撤销和重启恢复都实际可用。B 运行时不调用 A，不嵌入 A 的二进制，也不用截图代替界面。
- **依赖**：开源组件按包名和版本从上游获取，来源、版本和许可写进 B 的 README。
- **公开协议的服务**：能在本地搭建的，用容器或本机进程搭一个测试实例，A 和 B 连同一个实例，搭建方法写进 B 的 README；只有第三方实例时，使用用户授权的测试账号。
- **阻塞**：范围内的功能缺少账号、硬件、许可证或 entitlement，或公开协议的服务既不能在本地搭建、也没有可用实例时，把这一节的对照写成 `阻塞：原因`，其中能在本地实现的部分照常实现。构建方式带来的限制换一种构建方式解决，例如 SwiftPM 不生成 App Intents 元数据时改用 Xcode 工程。
- `spec.md` 没写清的地方，回到 A 上确认，再补进 `spec.md`。
- 构建和启动命令写进 `progress.md`。每次测试前确认运行的是刚构建的 B。

### 4. 对照

按 `spec.md` 逐节在 A 和 B 上做同样的操作并比较。两边使用相同的窗口尺寸、外观（浅色或深色）、语言和起始数据。

- **界面**：两边的截图存到 `evidence/compare/`，比较布局、尺寸、间距、字体、颜色、图标和控件状态。B 的 AX 导出可以和 A 的逐行比较控件和 `frame`。App 名称出现的地方（App 菜单、关于窗口、窗口标题）两边各显示自己的名称。
- **功能**：用相同的输入和起始状态，比较结果、输出文件、错误提示、持久化和重启后的状态。给 B 拍状态快照时加 `--app-path B_APP_PATH`。
- 每一节的「对照」写 `一致`、`有差异：具体差异` 或 `阻塞：原因`。有差异就修 B，修完重新对照这一节和受它影响的节。
- 用户试用后指出的差异，写进对应的节，同样修复后重新对照。

完成标准：`python3 "$SKILL_DIR/scripts/spec_check.py" PROJECT_DIR --final` 没有错误，即「界面」和「功能」下每一节的对照都是 `一致` 或 `阻塞：原因`。

### 5. 交付

交付 B 的 `.app`、完整源码、构建和启动命令、B 的 README，并向用户列出：界面和功能的数量与对照结果（取自 `spec_check.py --final` 的输出）、阻塞项及原因、「不复刻」中的功能。有阻塞项时，明确说明这是带阻塞的交付。打包、公证和发布在用户要求时执行。
