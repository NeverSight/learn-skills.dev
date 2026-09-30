---
name: re-wasm
description: WASM 逆向：格式解析、wasm2wat、浏览器侧。触发词：WASM、wasm、WebAssembly、wat
capabilities: [web-assembly]
---

# WebAssembly 逆向（WABT / wasmtime / Chrome DevTools）

## 何时使用 / 何时不用

- 用：.wasm 模块还原逻辑（网页前端加密/校验、浏览器插件、游戏、恶意网页/供应链 JS 加载的 wasm 载荷）
- 用：`WebAssembly.instantiate` / `WebAssembly.Module` / `.wasm` fetch 出现的样本——wasm 与 JS 胶水一体分析
- 不用：非 wasm（native 走 [[re-binary-core]]、.NET 走 [[re-dotnet]]、Java 走 [[re-java]]、纯 JS/脚本走 [[re-script-deob]]）
- 不用：wasm 模块本身可读性尚可、只需读逻辑——直接 `wasm2wat` 读 WAT 即可，无需完整流程
- 注意：动态运行默认沙箱（[[re-analyze/platform-tips]] 最高原则）；wasm 模块相对隔离，但宿主 JS 胶水会调 DOM/网络等敏感 API——JS 侧先还原（[[re-script-deob]]）

## 工具准备

参考 [[re-analyze/platform-tips]]——wasm 解析/反编译为静态步骤，免沙箱；动态运行（wasmtime/wasm3/浏览器加载）按最高原则进沙箱（至少断网）。

### WABT（wasm2wat / wasm-decompile / wasm-objdump，解析与反编译主力）

- Debian/Ubuntu: `apt install wabt`；Fedora: `dnf install wabt`；Arch: `pacman -S wabt`
- macOS: `brew install wabt`；Windows: `choco install wabt` 或 GitHub `WebAssembly/wabt` release 的 bin 目录
- 验证: `wasm2wat --version && wasm-decompile --version && wasm-objdump --version`

### wasmtime（WASI CLI 运行时，--invoke 直调导出函数）

- 官方安装器（全平台，装到 `~/.wasmtime/bin`）: `curl https://wasmtime.dev/install.sh -sSf | bash`
- Debian/Ubuntu: 无官方包——用官方安装脚本/二进制（install.wasmtime.dev）或源码构建；Fedora: 官方仓库无 CLI 包——用官方安装脚本或第三方仓库（GetPageSpeed/COPR）；Arch: `pacman -S wasmtime`；macOS: `brew install wasmtime`；Windows: `winget install BytecodeAlliance.Wasmtime`
- 验证: `wasmtime --version`

### wasm3（轻量解释器，无 WASI 依赖也可跑，嵌入式/快速验证场景）

- Arch: 官方仓库无 wasm3——AUR（如 wasm3 包）或源码构建；macOS: `brew install wasm3`
- Debian/Ubuntu/Fedora 无官方包 → GitHub `wasm3/wasm3` release 下载对应平台单文件二进制，或源码构建: `git clone --depth 1 https://github.com/wasm3/wasm3 && cmake -B build -S wasm3 && cmake --build build`
- 验证: `wasm3 --version`

### Chrome DevTools（浏览器侧动态分析）

- Chrome/Chromium: Debian/Ubuntu `apt install chromium`（Chrome 用官方 deb）；Fedora `dnf install chromium`；Arch `pacman -S chromium`；macOS `brew install --cask google-chrome`；Windows 官方安装器
- 验证: 启动浏览器 `F12` 打开 DevTools → Sources 面板能展开 .wasm 文件
- 本地起服务供浏览器加载: `python3 -m http.server 8000`

### binaryen（wasm-opt 优化/混淆还原，wasm-dis 反汇编）

- Debian/Ubuntu: `apt install binaryen`；Fedora: `dnf install binaryen`；Arch: `pacman -S binaryen`
- macOS: `brew install binaryen`；Windows: `choco install binaryen` 或 GitHub `WebAssembly/binaryen` release
- 验证: `wasm-opt --version`

## 操作步骤

按顺序执行，每步记录证据（路径 + sha256，见 [[re-triage]]）。

1. **识别 wasm 模块**：
   ```sh
   file sample.wasm                          # "WebAssembly (wasm) binary module version 0x1 (MVP)"
   xxd sample.wasm | head -1                 # 魔数 00 61 73 6D（\0asm）+ 版本 01 00 00 00
   ```
   - 魔数 `\0asm`（`00 61 73 6D`）+ 版本 `01 00 00 00` = 标准 wasm；不符 → 不是 wasm（可能加密/混淆/损坏，见坑 3）
   - 常以内嵌形态出现，先还原成 .wasm 文件：`atob(...)` 的 base64 串、JS 里 `Uint8Array([0,97,115,109,...])` 数组字面量
   - 从 JS 侧确认：`WebAssembly.instantiate` / `WebAssembly.Module` / `.wasm` fetch 出现即 wasm 载荷（JS 胶水走 [[re-script-deob]]）

2. **section 解析（wasm-objdump / wasm2wat）**：
   ```sh
   wasm-objdump -x sample.wasm        # 全部 section：Type/Import/Function/Table/Memory/Global/Export/Code/Data
   wasm-objdump -h sample.wasm        # 只列 section 摘要
   wasm2wat sample.wasm -o sample.wat # 二进制 → WAT 文本（有扩展指令时加 --enable-all）
   wasm-objdump -d sample.wasm        # 反汇编全部函数体（WAT 风格指令）
   ```
   - 各 section 的逆向意义：Type（函数签名，辅助还原类型）、Import（**宿主 JS/WASI 注入的函数——调用边界**）、Export（**JS 可调的对外函数名**）、Data（**字符串常量区**）、Code（指令体）
   - 先读 Import + Export 建立调用面，再进 Code

3. **反编译（wasm-decompile）**：
   ```sh
   wasm-decompile sample.wasm -o sample.c    # 类 C 伪码（可读性优先）
   ```
   - 与 WAT 对照：wasm-decompile 可读性好但丢部分类型/边界信息；关键函数以 `wasm2wat` 产出的 WAT 为准精读
   - 入口定位：`(export "checkPassword" ...)` → JS 侧 `instance.exports.checkPassword`；import 的函数 → 到 JS 胶水找实现（坑 2）
   - 字符串：`wasm-objdump -s sample.wasm` dump 全部 section 原始内容（hex dump，含 Data 段；Data section 亦可从 `-x` 输出读）；WAT 里找 `(data (i32.const 偏移) "字符串")`，把代码里 `i32.const 偏移` 映射回字符串（坑 1）
   - 函数多/疑似混淆时先用 wasm-decompile 粗读，挑出目标函数再精读

4. **浏览器侧（DevTools Sources / JS 调用面）**：
   - 打开样本页面（本地起服务），DevTools → Sources → 左侧展开 `.wasm` 文件：Chrome 自动给出反编译伪代码视图，可下断点、单步，Scope 面板看 wasm 局部变量，Call Stack 同时显示 JS↔wasm 帧
   - 调用面：JS 侧 `WebAssembly.instantiate(bytes, importObject)` 的 `importObject` 定义了 wasm 的 import 实现；`instance.exports.xxx(...)` 是 wasm 对外函数——在 JS 调用点下断点，单步进入 wasm 帧观察入参/返回值
   - 无头环境：Chrome headless + DevTools Protocol（`--headless --remote-debugging-port=9222`），或 Node `WebAssembly.instantiate` 等价复现调用
   - 动态改值：DevTools 在 wasm 伪代码视图里修改参数重放调用，黑盒对比输出

5. **动态（wasmtime + 插桩/黑盒差分）**：
   ```sh
   wasmtime run sample.wasm                                   # WASI 程序（需 _start 导出）
   wasmtime run --invoke checkPassword sample.wasm '"test"'   # 直调导出函数（参数按 JSON 解析）
   wasmtime run --dir . --env FLAG=xxx sample.wasm            # 显式授权 WASI 文件/环境能力
   wasm3 sample.wasm checkPassword test                       # 无 WASI 模块用 wasm3（参数原样）
   ```
   - 插桩：`wasm-objdump -d` 静态指令 + `--invoke` 黑盒差分——同一导出函数喂不同输入，观察输出变化定位分支/校验逻辑
   - WASI 系统调用：`strace -f wasmtime run sample.wasm`（坑 5，走 [[re-tracing]]）
   - 需要 BigInt 参数或进 JS 侧跟踪时，写 node 胶水：
     ```js
     const { instance } = await WebAssembly.instantiate(bytes, imports);
     console.log(instance.exports.f(1n, 2n));   // i64 必须 BigInt（坑 4）
     ```
   - 一切动态执行默认沙箱（[[re-analyze/platform-tips]] 最高原则）

## 跨域联合

- [[re-managed]]：网关工作流步骤①（识别运行时）②（反编译）固定调用本技能；wasm 宿主程序（JS/Node）属托管代码域
- [[re-script-deob]]：JS 胶水代码（instantiate/import 对象/fetch wasm/atob 内嵌）先去混淆还原——imports 的实现基本都在 JS 侧，两技能必须联用
- [[re-tracing]]：WASI 程序动态侧——`strace -f wasmtime run` 观察系统调用边界
- [[re-emulation]]：可选——无合适运行时的 WASI 模块模拟执行（wasm 常经 Emscripten 编译，模拟前先按 WASI 映射理解宿主依赖）
- [[re-firmware]]：嵌入式/路由器 web 界面中的 wasm 模块
- 底座 [[re-binary-core]]：初勘（[[re-triage]]）；wasm 与 native 混合样本
- [[re-malware]]：恶意网页/供应链 JS 加载 wasm 载荷的完整链路
- [[re-deobfuscate]]：wasm 混淆（wasm-obfuscator 等）属混淆对抗，深层还原思路一致

## 常见坑与陷阱

- **字符串在 data 段不在代码里**：现象——wasm2wat/反编译只见 `i32.const 偏移` 数字，grep 不到任何明文；原因——wasm 没有字符串类型，字符串常量存 Data 段、代码用内存地址引用；对策——`wasm-objdump -s sample.wasm` dump 全部 section 原始内容（hex dump，Data 段在其中；也可从 `-x` 输出读 Data section）（WAT 里看 `(data (i32.const 偏移) "…")`），把偏移映射回引用处
- **imports 是 JS 边界不是库调用**：现象——wasm 文件里找不到关键校验/解密逻辑；原因——wasm 的 import 由宿主 JS 注入（`WebAssembly.instantiate(bytes, { env: {...} })`），敏感逻辑在 JS 侧；对策——`wasm-objdump -x` 列出 Import section → 到 JS 胶水代码找对应实现（[[re-script-deob]]）——wasm 只证明"调用了什么"，不证明"它做了什么"
- **wasm 混淆（wasm-obfuscator 等）先反混淆再分析**：现象——wasm2wat 输出大段控制流扁平化、死代码、`select` 噪音，字符串被切碎/加密，函数名全抹；原因——混淆器做控制流平坦化 + 字符串加密 + 名称抹除；对策——binaryen 逐遍优化还原平坦化：`wasm-opt --flatten --simplify-locals --vacuum --dce -O3` 多轮迭代；字符串加密需定位解密逻辑（思路同 [[re-deobfuscate]]，注意解密函数可能是 import——回到坑 2）
- **BigInt 调用约定**：现象——JS 调 wasm 导出函数报 `TypeError: Cannot convert a BigInt value to a number`，或 i64 参数静默截断；原因——i64 参数/返回值在 JS↔wasm 边界只能走 BigInt（Number 仅 2^53 精度）；对策——JS 侧 `instance.exports.f(1n, 2n)` 传 BigInt；wasmtime `--invoke` 参数按 JSON 解析不支持 BigInt——需要时写 node 胶水；复刻算法用 Python int / JS BigInt，别用 Number
- **WASI 系统调用边界**：现象——wasmtime 跑 WASI 程序报 `unknown import: wasi_snapshot_preview1.…`，或浏览器与运行时行为不一致；原因——WASI 程序通过 import `wasi_snapshot_preview1` 拿文件/时钟/随机数/网络能力，运行时未授权该能力即失败；浏览器里宿主 import 是 JS 而非 WASI，同一模块两端行为可以不同；对策——`wasm-objdump -x` 看 Import 段确认用到的 WASI 函数 → `wasmtime run --dir . --env K=v` 显式授权 → `strace -f wasmtime run` 观察实际系统调用（[[re-tracing]]）；结论标注运行环境（browser vs wasi）
