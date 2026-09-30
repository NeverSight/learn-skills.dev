---
name: re-electron
description: >
  Electron 桌面应用逆向：asar 解包、主/渲染进程 JS、V8 字节码（.jsc）边界、CDP 动态调试、反调试对抗。
  触发词：Electron、asar、桌面应用逆向、.jsc、V8 快照、CDP、ELECTRON_RUN_AS_NODE、devtools 检测。
capabilities: [electron-analysis]
---

# Electron 桌面应用逆向（asar / CDP / .jsc）

## 何时使用 / 何时不用

- 用：Electron 打包桌面应用——`resources/app.asar` 结构、主/渲染进程 JS 逻辑还原、原生 `.node` 模块、密钥/通信逻辑提取
- 用：V8 字节码 `.jsc` 文件（bytenode 类工具编译产物）的识别与边界判断
- 用：动态调试——主进程 `--inspect`、渲染进程 `--remote-debugging-port`（CDP）、`ELECTRON_RUN_AS_NODE` 以 Node 模式复用运行时
- 用：反调试对抗——devtools / inspect 检测识别与绕过（联动 [[re-evasion]]）
- 不用：纯浏览器扩展（走 [[re-browser-ext]]）
- 不用：脱离 Electron 场景的混淆 JS/脚本（走 [[re-script-deob]] / [[re-deobfuscate]]）
- 不用：`.jsc` 出现在 Cocos 游戏资源场景（那是 Cocos 引擎字节码，走 [[re-game]]；本技能只管 Electron 的 V8 字节码）
- 不用：仅需通用二进制初勘（[[re-binary-core]] 通用底座；本技能只补 Electron 打包层语义）
- 注意：**动态执行默认沙箱（[[re-analyze/platform-tips]] 最高原则）**——跑应用、连 CDP、加载 `.jsc` 均按动态处理，静态解包可免沙箱

## 工具准备

所有工具先验证再使用。静态解包可免沙箱；运行应用 / 动态调试默认沙箱 + 网络隔离（[[re-analyze/platform-tips]] 最高原则）。Electron 应用多为跨平台打包，工具链以 npm 生态为主、跨 OS 一致。

### Node.js + npm —— 工具底座（asar / CDP 客户端 / bytenode / fuses）

- Linux: 发行版包 `apt install nodejs npm`（Debian/Ubuntu 仓库版本偏旧，V8 版本锁场景用 NodeSource 或 nvm 装新版）；macOS: `brew install node`；Windows: 官方安装器或 `choco install nodejs`；跨平台: nvm（`nvm install <version>`）按需切换 Node 版本
- 验证: `node --version && npm --version`
- nvm: 官方安装脚本（GitHub nvm-sh/nvm）；Windows 用 nvm-windows 或官方安装器

### @electron/asar —— asar 归档解包（现维护的官方包）

- `npm install -g @electron/asar` 或免安装 `npx @electron/asar ...`（npx 首次自动下载；旧包名 `asar` 已弃用但 CLI 兼容仍可用）
- 验证: `npx @electron/asar --help`（应列出 `pack / list / extract-file / extract` 子命令）
- 用法: `npx @electron/asar extract app.asar out/`（整包解出）、`npx @electron/asar list app.asar`（列目录）、`npx @electron/asar extract-file app.asar path/to/file`（单文件）
- 免工具直读：asar 头部内嵌 JSON 目录（`{"files":{...}}`，每文件含 `size`/`offset`/`integrity`），JSON 字符串自偏移 16 起（前 12 字节为 pickle 嵌套大小字段，offset 12 为头字符串长度，均 uint32 LE）——`strings app.asar | grep '"files"'` 或小脚本 `JSON.parse` 定位，无需任何工具

### strings / grep —— 文本线索

- Linux: binutils 自带（`apt install binutils` 等）；macOS: 自带（或 `brew install binutils`）；Windows: WSL 内或 Sysinternals strings
- 验证: `strings --version`

### chrome-remote-interface —— CDP 客户端（动态调试主力）

- 项目内 `npm install chrome-remote-interface`（官方 npm 包，Chrome DevTools Protocol 客户端）
- 验证: `node -e "require('chrome-remote-interface')"` 不报错即装好；实际连通见操作步骤 6
- 备选: 纯 curl + Node 内置 ws，无需装包（`curl http://127.0.0.1:<port>/json/list` 拿 `webSocketDebuggerUrl` 后连 WebSocket 发 JSON-RPC）

### bytenode —— .jsc 编译/加载理解工具（验证与对照用）

- `npm install -g bytenode` 或项目内安装
- 验证: `npx bytenode --help`（`-c` 编译、`-e/--electron` 编译为 Electron 用、`-ep/--electron-path` 指定 Electron 可执行文件）
- 用途：用目标版本 Node/Electron 重编译对照样本 `.jsc` 的魔数与可加载性；本身不是反编译工具（见坑 1）
- Electron 42+ 主进程场景（`electronMain`）无 CLI 对应参数，须用 API 调用形态：`require('bytenode').compileFile({ electronMain: true, filename: 'main.js' })`（与坑 1 的 `electronMain` 模式呼应）

### @electron/fuses —— 运行能力开关检查/翻转

- `npm install -g @electron/fuses`（官方包）
- 验证: `npx @electron/fuses read --app <应用可执行文件或 .app 路径>`——输出各 fuse 状态（RunAsNode / EnableNodeCliInspectArguments / EnableEmbeddedAsarIntegrityValidation / OnlyLoadAppFromAsar 等）
- 翻转: `npx @electron/fuses write --app <路径> RunAsNode=off EnableNodeCliInspectArguments=off`（写前先 read 评估；翻转改动二进制、破坏签名，macOS 需重新签名）
- 免工具查看：strings 搜 fuse 哨兵串 `dL7pKGdnNz796PbbjQWNKmHXBZaB9tsX`，其后为 fuse 版本、长度与 wire 字节（`0x30`(0)=禁用、`0x31`(1)=启用、`0x72`(r)=移除）

### 通用反编译器 —— 原生 .node 模块

- Ghidra（官方 release 包，需 JDK；部分发行版仓库有 `apt install ghidra` / `pacman -S ghidra`；macOS `brew install --cask ghidra`；Windows 官方 zip；验证 `analyzeHeadless -help`）
- IDA：商业版；Freeware 版架构支持范围以官方页面为准
- `.node` 本质是 ELF/Mach-O/PE 动态库，导入反编译器前先用 `file`/`readelf -h` 确认架构（联动 [[re-format-elf]] / [[re-format-macho]] / [[re-format-pe]]）

### （可选）xvfb-run —— Linux 无显示环境跑 GUI 应用

- Linux: `apt install xvfb` / `dnf install xvfb` / `pacman -S xvfb`
- 验证: `xvfb-run -a node --version`；无显示服务器时 `xvfb-run -a electron .` 运行目标
- macOS/Windows 有原生显示，无需

## 操作步骤

按顺序执行，每步结果存档；动态执行默认沙箱。

1. **识别 Electron 与版本**：
   ```sh
   ls resources/                    # 打包应用应有 app.asar（+ app.asar.unpacked/）
   strings <可执行文件> | grep -i -E 'electron|chrome' | head
   ```
   - 判定信号：`resources/app.asar` 结构、进程列表中多进程（主进程 + GPU/渲染子进程）、二进制内 Electron/Chromium 版本串
   - 版本确认：打包应用 `--version` 常无输出——可靠途径是动态阶段用 CDP 执行 `process.versions`（electron/chrome/v8/node/modules 全字段）；静态只能靠二进制 strings 版本串辅助
   - Electron → Chromium/Node 对应关系查官方 electron-timelines 发布表（只列 Chromium/Node，无 V8 列）；V8 版本只能运行时 `process.versions.v8` 获取

2. **asar 解包**：
   ```sh
   npx @electron/asar list app.asar                       # 先看目录结构
   npx @electron/asar extract app.asar out/               # 整包解出
   npx @electron/asar extract-file app.asar package.json  # 单文件快速取
   ```
   - 免工具：JSON 目录自偏移 16 起，`strings app.asar | grep '"files"'` 或脚本按 size/offset 拼接即可还原全部文件
   - `app.asar.unpacked/` 目录是未打进归档的原生模块，原样在磁盘上，直接分析
   - 改包前先 `npx @electron/fuses read --app <可执行文件>` 看 `EnableEmbeddedAsarIntegrityValidation` / `OnlyLoadAppFromAsar`——完整性校验开启时替换 app.asar 会导致启动失败（见坑 2）

3. **主进程入口与逻辑**：
   - 解包后读 `out/package.json` 的 `main` 字段 → 主进程入口 JS（默认 `main.js`）
   - 主进程是 Node 环境：require 链、`app`/`BrowserWindow`/`ipcMain` 调用即业务骨架；IPC handler（`ipcMain.handle/on`）是主/渲染通信枢纽，先列全
   - 主进程逻辑可被 `ELECTRON_RUN_AS_NODE=1 <可执行文件> script.js` 以纯 Node 方式复用（同一 V8/Node ABI，见坑 3 的边界）——不依赖 electron API 的部分可离线跑通观察行为
   - 主进程打包为 `.jsc` 的场景：`ELECTRON_RUN_AS_NODE` 下 `require('bytenode')` 加载 .jsc（版本必须匹配，见坑 1）

4. **渲染进程 JS 还原**：
   - 渲染代码一般打包在 `out/` 某子目录（webpack/browserify/rollup bundle，常混淆、压缩成一行）
   - 还原顺序：确定入口 HTML（BrowserWindow 的 loadFile/loadURL 参数）→ 找 `<script>` 引用的 bundle → 美化（js-beautify 类）→ 字符串定位（strings/`xxd`）→ 混淆层走 [[re-script-deob]] / [[re-deobfuscate]]
   - 渲染进程密钥/逻辑提取以字符串引用（硬编码密钥、API 域名、特征常量）为锚点展开
   - `.jsc` 文件出现时跳到坑 1 的边界处理（不可当 JS 文本解析）

5. **原生模块 `.node`**：
   - 定位：`app.asar.unpacked/**/*.node`（以及解包后 require 路径指向的 .node）
   - 识别：`file xxx.node`（ELF/Mach-O/PE + 架构）、`readelf -h`（Linux）；`.node` 即动态库，走 [[re-format-elf]] / [[re-format-macho]] / [[re-format-pe]] 前置 → [[re-ghidra]] / [[re-ida]] / [[re-radare2]] 反编译，C++ 语义走 [[re-cpp-abi]]
   - NODE_MODULE_VERSION（`process.versions.modules`）与 Electron 版本一一对应，用错版本加载 .node 会报 ABI 错误——可借此确认目标 Electron 版本
   - 导出函数即 N-API/V8 接口层，从导出表 + JS 侧调用点交叉定位业务函数（联动 [[re-imports]]）

6. **动态 CDP 调试**：
   ```sh
   # 主进程（Node/V8 Inspector，默认端口 9229）
   <可执行文件> --inspect=9229
   <可执行文件> --inspect-brk=9229        # 启动即暂停，等调试器
   # 渲染进程（Chromium CDP，默认端口 9222）
   <可执行文件> --remote-debugging-port=9222
   ```
   - 启动前先 `npx @electron/fuses read --app <可执行文件>`：`EnableNodeCliInspectArguments` 为 Disabled 时 `--inspect`/`--inspect-brk` 被忽略（SIGUSR1 也不再开 inspector）——此时只能走渲染进程 CDP 或 [[re-frida]] 注入
   - 渲染进程连接流程：
     ```sh
     curl -s http://127.0.0.1:9222/json/list    # 列 targets（title/url/webSocketDebuggerUrl）
     ```
     用 chrome-remote-interface 连 `webSocketDebuggerUrl`，`Runtime.evaluate` 执行任意 JS、`Console.enable` 收日志、`Page.captureScreenshot` 截图；主进程同法连 `--inspect` 端口
   - 端口以 `/json/list` 实际响应为准，别猜固定端口（应用可能占用/修改）；窗口未创建时 target 不会出现，先在 UI 触发再枚举
   - 单实例锁（`app.requestSingleInstanceLock()` 常见）导致二次启动直接退出——用 `--user-data-dir=<新目录>` 或先结束现有实例
   - 浏览器页面里连 CDP 的 WebSocket 受 Origin 检查（Chrome 111+）：加 `--remote-allow-origins=*`；Node 客户端无 Origin 头不受影响
   - 运行时信息取证：`Runtime.evaluate` 执行 `process.versions`（版本）、`process.env`（环境变量）、`require.cache`（已加载模块）——比静态字符串可靠
   - Linux 无显示环境用 `xvfb-run -a` 包一层再启动

7. **反调试对抗与数据提取**：
   - devtools/inspect 检测常见形态：查 `process.argv`/`process.execArgv` 里的 inspect 参数、DevTools 打开检测（窗口尺寸 `outerWidth - innerWidth`、console 计时）、`debugger` 语句、`process.versions` 异常校验
   - 定位检测点 → patch 跳过（改 bundle 后重新 pack asar，注意坑 2 完整性）或运行时 hook（[[re-frida]]）、CDP 层 `Debugger.enable` 前先绕过
   - 注入面判断：`contextIsolation`（Electron 12 起默认 true）、`sandbox`（Electron 20 起默认 true）、`nodeIntegration`（默认 false）决定 preload/渲染进程能 require 什么、CDP `Runtime.evaluate` 要选对执行上下文（主 world vs 隔离 world 的 contextId）
   - 数据提取联动：运行时内存/密钥 [[re-memdump]]、硬编码密钥 [[re-crypto-keys]]、加密数据还原 [[re-crypto-decrypt]]、系统调用/文件行为 [[re-tracing]]
   - 行为观察：`ELECTRON_ENABLE_LOGGING=1` 或 `--enable-logging` 打开 Chromium 日志，失败诊断先行

## 跨域联合

- [[re-managed]]：托管代码网关路径（re-managed → 本技能），Electron 的 JS 层归其编排
- [[re-script-deob]] / [[re-deobfuscate]]：渲染进程混淆 JS 还原
- [[re-evasion]]：devtools/inspect 检测对抗方法论（本技能出目标特征，绕过策略联动）
- [[re-format-elf]] / [[re-format-macho]] / [[re-format-pe]]：原生 `.node` 模块格式解析前置
- [[re-cpp-abi]]：原生模块 C++ 语义（RTTI/虚表/STL）恢复
- [[re-imports]]：.node 导出表与库指纹、Electron 版本确认辅助
- [[re-ghidra]] / [[re-ida]] / [[re-radare2]]：原生模块反编译
- [[re-frida]]：fuse 禁 inspect 场景的动态注入替代通道
- [[re-memdump]] / [[re-crypto-keys]] / [[re-crypto-decrypt]]：运行时密钥与加密数据提取
- [[re-tracing]]：动态行为观察（文件/网络/系统调用）
- [[re-variant]]：多版本对比（补丁定位、逻辑差异）
- [[re-game]]：Cocos 场景 `.jsc`（JS 引擎字节码）与 Electron `.jsc`（V8 字节码）的区分
- [[re-sandbox]]：一切动态执行强制前置（[[re-analyze/platform-tips]] 默认沙箱原则）
- 配套：[[re-patching]]（改 bundle 字节补丁）、[[re-triage]]（初勘前置）

## 常见坑与陷阱

- **`.jsc` 是 V8 字节码快照，不是 JS 文本**：现象——解出 `.jsc` 文件后 grep/美化/解析全无效，内容是不可读二进制；原因——bytenode 类工具把 JS 编译成 V8 字节码并移除源码（`Function.prototype.toString()` 被替换为桩代码，这是识别特征之一）；边界——V8 字节码格式未文档化、随 V8 版本变化，目前无公开反编译工具；`node --print-bytecode`（官方 Node 构建可用）只能打印「运行中」编译出的字节码助记符，不是源码还原；对策——先确认样本 `.jsc` 的编译环境（魔数/加载器提示、`process.versions.v8` 对照），能加载就跑行为分析（strace/网络/内存），需要源码语义就找未编译的 .js 副本或 bundle map；版本锁——`.jsc` 必须由同 V8 版本、同平台/架构的 Node 或 Electron 编译才能加载，跨版本加载直接崩；Electron 42+（V8 ≥ 14.8）主进程加载的 `.jsc` 需用真实 Electron 主进程编译（bytenode `electronMain` 模式），`ELECTRON_RUN_AS_NODE` 方式编译的会在加载时崩溃（read-only snapshot 校验不匹配）——不确定的边界如实报告，不臆断源码内容
- **asar 内路径混淆与完整性校验**：现象——解出的文件路径与 require 逻辑对不上，或改完 app.asar 应用启动即退出；原因——asar 支持任意文件名（含 `..`/编码变体），且 `EnableEmbeddedAsarIntegrityValidation` fuse 开启时 asar 内容被校验、`OnlyLoadAppFromAsar` 开启时拒绝非 asar 加载；对策——按 JSON 目录的 size/offset 而非路径语义还原；改包前先 `@electron/fuses read`，校验开启时改用运行时 hook（frida）或动态分析，不硬改归档
- **`ELECTRON_RUN_AS_NODE` 行为差异**：现象——设了环境变量应用没按预期当 Node 跑，或主进程 `.jsc` 加载崩溃；原因——该模式下 Electron 只提供 Node 运行时（无 `electron` API、`require('electron')` 行为异常），且 `RunAsNode` fuse 为 Disabled 时该环境变量被完全忽略（连带 `process.fork()` 失效）；对策——先 read fuses 确认 RunAsNode 状态；该模式只用于复跑不依赖 electron API 的逻辑，GUI/窗口代码必须走正常启动
- **contextIsolation / sandbox 决定注入面**：现象——preload 脚本里 require 报错、CDP evaluate 拿不到页面变量；原因——Electron 12 起 contextIsolation 默认 true（渲染进程与 preload 上下文隔离）、Electron 20 起 sandbox 默认 true（preload 无完整 Node 能力）、nodeIntegration 默认 false；对策——CDP `Runtime.evaluate` 先枚举执行上下文（`Runtime.enable` 后看 contextId），区分主 world 与隔离 world 再求值；注入/读取面按这三个开关的实际配置设计
- **fuses 改变运行能力（调试入口可能整体关闭）**：现象——`--inspect`、`--inspect-brk`、`ELECTRON_RUN_AS_NODE` 全部无效，应用像没收到参数；原因——`EnableNodeCliInspectArguments` / `RunAsNode` fuse 被翻转关闭；对策——`@electron/fuses read` 先确认；fuse 写入会改二进制并破坏签名（macOS 需重新签名，未签名时用 resetAdHocDarwinSignature 选项），这是改打包产物的最后手段，优先换 frida / 渲染进程 CDP 通道
- **单实例锁与 CDP 端口不确定**：现象——带参数二次启动直接退出、/json/list 连不上；原因——`requestSingleInstanceLock()` 让第二个实例立即退出，CDP 端口可能被应用占用或改掉；对策——用独立 `--user-data-dir` 绕过单实例锁；端口以 `/json/list` 实际响应为准；窗口未创建时 target 未暴露，先触发 UI 再枚举
