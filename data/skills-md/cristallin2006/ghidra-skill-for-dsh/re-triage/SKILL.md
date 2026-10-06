---
name: re-triage
description: 未知二进制的第一步（file triage / sample identification）：判文件类型（PE/ELF/Mach-O/固件/APK）、语言（C/C++/Go/Rust/.NET/Python）、壳（packer detection）、威胁面，决定后续路线（静态深挖/动态/换工具）。触发：新样本、未知 exe/elf/bin/固件、"看看这个文件"、疑似加壳、恶意样本分诊（malware triage）。只做判断和路线决策，不做深挖——要深挖去 ghidra-static。动手前必须先用 skill 工具加载本 skill 全文并遵守其流程；一切观察/结论用 ledger.py 落账。
whenToUse: 收到未知二进制需要判断"这是什么、壳/语言/威胁面、接下来怎么打"时；新样本、疑似加壳、恶意软件初筛、CTF 题目开题
---

# RE Triage（场景 1：这是什么？）

前置：无（本 skill 是逆向工作流入口）／后继：检出壳 → `~/.dsh/skills/re-unpack`；判型完成要深挖 → `~/.dsh/skills/ghidra-static`；目的是找漏洞 → `~/.dsh/skills/vuln-audit`；具体命令 → `~/.dsh/skills/ghidra-core`；**输入是 pcap/抓包文件 → 不归本 skill，直接去 `~/.dsh/skills/traffic-analysis`**

> **铁律 4（Triage 硬门）**：未记录 imports（DLL/SYS 还要 exports）+ 语言/壳判定之前，MUST NOT 进入深挖或动态分析。导入表只有 kernel32/ntdll 且极少 → 高度怀疑 `LoadLibrary`+`GetProcAddress` 动态加载，禁止宣称"无网络/无文件能力"。（全文见 ghidra-core §1）
>
> **证据台账**：开工即落账——每次区域观察走 ghidra-core `scripts/ledger.py observe`（首次入账自动建账）；新会话接手旧样本先 `ledger.py status` + 读 `<ws>/out/<样本名>.ledger.md` 再动手。机制见 ghidra-core `references/evidence-ledger.md`。

## 路径约定

```bash
SK="$HOME/.dsh/skills/ghidra-core/scripts"     # 唯一代码家
# Windows:
RPC="$HOME/Desktop/src/ghidra-bridge/ghidra-rpc-venv/Scripts"  # ghidra-rpc CLI
# WSL/Linux:
# RPC="$HOME/ghidra-rpc-venv/bin"
```

> 路由表提到的外部工具（checksec/GoReSym/rustfilt 替代/dnSpyEx 等）是否已装：`python "$SK/doctor.py"` 的 toolchain 节为准；未装的按其 hint 装或走对应 skill 的失败阶梯。

## 流程（5~15 分钟，强制起点）

1. **ensure + triage 一把出**（daemon 没起就起、样本没 load 就 load，含全量分析）：

```bash
python "$SK/rpc_driver.py" ensure /path/to/sample
python "$SK/rpc_driver.py" "@$HOME/.dsh/ghidra-workspace/out/sample.triage.json" triage /path/to/sample
```

产出：元数据（language/compiler/image_base/内存块）、按库分组的 imports/exports/entry points、可疑 API 命中（反调试/注入/加密/网络/持久化/动态加载六组）、干净 IAT 警告、字符串快赢（flag|pass|correct…）、语言启发（Go/Rust/.NET/Python，**`python_ext`=Cython/CPython 扩展模块信号——exports 有 `PyInit_*` / imports 引 `Py_Initialize` / 字符串含 `__Pyx_`，命中 → ctf-patterns §12 元数据优先路线**）与 **`packer` 壳判定块**（节名 / 文件内 `UPX!` magic / 结构特征三信号交叉，verdict ∈ upx / packed-unknown / none）。`lang_hints.upx` 只是兼容字段——判壳以 `packer` 块为准，且 **verdict=none 不排除壳**（节名可改、magic 可抹）；反过来 **verdict=packed-unknown 也不等于有壳**——出现 `.CRT`/`.tls` 节（MinGW-w64 标准布局）或未初始化可写块全是 `.bss` 标准族（ELF 正常布局，Cython 扩展 `.so` 常因此误报）时，对应结构信号会被降级到 `false_positive_hints`，见到该字段先怀疑误报，不要直接去脱壳。有疑点按 advice 人工复核。参数细节见 ghidra-core §5 能力清单。

2. **手工补充**（详情 `references/triage.md`）：`file` / `checksec` / DIE 查壳；`strings -el` 补宽字符；PE 查 TLS 回调目录（先于 main 执行）。
3. **下判据 → 选路线**（见下「语言/平台路由」与「路线决策」）。

## 任务地图（一个完整逆向任务的全貌）

本 skill 是入口，不是全部。端到端长这样，每段的知识在对应 skill 里：

```
① 分诊判型（本 skill）→ ② 选路线（下表）→ ③ 深挖/审计 → ④ 交付
```

- ③ 读懂逻辑/提取算法 → `ghidra-static`（Recon→Analysis→标注/patch，命令见 ghidra-core）
- ③ 找漏洞 → `vuln-audit`（按 checklist 逐项排查，命中项回 ghidra-static 深挖确认）
- ③ 静态卡住/要验证猜想/想先跑起来看 → `re-dynamic`（直接运行、函数级 Oracle、Frida/gdb/angr 入口）
- 检出壳 → `re-unpack`（脱壳+验证）→ 脱壳产物回 ① 重新分诊
- **输入是 pcap/pcapng 抓包 → `traffic-analysis`（流量分诊/隧道/隐信道/USB HID/WiFi/TLS）；它提取出的二进制回本 skill 重新分诊**
- **输入是 APK → 先拆组成：纯 DEX（无 lib/）→ `android-re`；含 so 且逻辑在 native → 按 ABI 选 so 走 ghidra-static**
- ④ 交付纪律（证据带地址+复现命令、产物 SHA256、禁止无证据否定结论）在 `ghidra-static` §交付
- 任何阶段的命令细节 → `ghidra-core`；静态 15 分钟无关键路径 / 同一路径失败 2 次 → 转动态或换工具（铁律 6，全文见 ghidra-core §1）

## 路线决策（判完型之后去哪）

| 判定 | 下一步 |
|---|---|
| 普通 native 二进制，要读懂/提取逻辑 | → **ghidra-static**（静态深挖） |
| 目的是找漏洞/攻击面 | → **vuln-audit**（按清单排查） |
| 有壳（UPX 节名/高熵/导入表异常干净） | → **re-unpack**（检出壳 = 唯一的下一步；脱壳产物回本表重新分诊）。**检出壳后 MUST NOT 对 packed 字节做任何内容分析（肉眼或脚本）——那是噪声** |
| .NET（mscoree/_CorExeMain） | **离开 Ghidra**：dnSpyEx + de4dot（例外：NativeAOT/IL2CPP 是 native，留下） |
| PyInstaller/Pyarmor | 先解包（pyinstxtractor / Pyarmor-Static-Unpack）再分析 pyc |
| 静态 15 分钟无关键路径 | → **re-dynamic**（跑起来看/函数级 Oracle/动态插桩入口） |
| 同一路径失败 2 次 | 换工具，禁止空转 |

## 流程分级（别对单点题跑完整流程）

分诊后先判任务量级，再决定流程深度：

- **轻量路径**（命中任一信号）：文件 < 4KB、只有一个校验函数、strings 快赢直接命中 flag 形态、期望值与比较逻辑一屏可见 → 直接给结论 + 最小证据（一条 `observe` + 一条 `conclude` + 验证命令），**不强制**完整台账覆盖、不强制 `decompile-all` 全量分析。实测对照：单点洞察题两臂都能秒解，跑完整流程贵 6–7 倍且零增益
- **完整流程**：多阶段（加密载荷/VM/壳/协议）、需要交付报告/证据链、环境弱（无 oracle 可跑）——skill 的价值集中在这里
- 轻量路径中一旦发现多阶段特征，立即升级完整流程，禁止带病轻量

## 语言/平台路由（识别到就换打法，别硬上通用流程）

| 识别特征（triage 自动报） | 走向 |
|---|---|
| `go.buildid` / `runtime.gopanic` / 巨大静态二进制 | 先跑 GoReSym 恢复符号（stripped 也行）→ 只看 `main.*` 包函数；Go string 是 {ptr,len} 非 NUL 结尾，Ghidra 默认字符串分析会漏，装 golang-loader 插件或靠 xref。**深挖细节 → ghidra-static `references/go-binary.md`**（pclntab 版本指纹、garble/GoResolver、buildinfo 挖模块路径） |
| `panicked at` / `_ZN` mangling / `.rustc` section | `strings \| grep panicked` 先挖源码路径行号；`rustfilt` demangle；泛型单态化 → 从字符串 xref 入手而非逐个函数。**深挖细节 → ghidra-static `references/rust-binary.md`**（panic 路径=源码地图、crate 依赖还原） |
| `mscoree.dll` / `_CorExeMain` | **离开 Ghidra**：dnSpyEx + de4dot，全流程见 `references/dotnet-il.md`；例外：NativeAOT / IL2CPP 是 native，留在 Ghidra |
| PyInstaller / Pyarmor 特征 | 先解包（pyinstxtractor）再分析 pyc——**版本判定与反编译器选择矩阵见 `references/pyc-bytecode.md`**（≤3.8 uncompyle6/decompyle3，≥3.9 pycdc）；PyArmor 加密 code object → 转 re-dynamic |
| UPX 节名 / `packer.verdict=upx`（magic 命中） | → re-unpack（原生 `upx -d` 或修头后解，验证清单见 re-unpack） |
| 自定义壳 / 熵高 | → re-unpack 失败阶梯（仿真/动态 dump；本 skill 只负责判"有壳"） |
| APK | **先拆开看组成**：含 `lib/` 且逻辑在 so → 按 ABI 选 so（优先 x86_64）走 ghidra-static；**纯 DEX（无 lib/）→ `~/.dsh/skills/android-re`**（多 dex 启发式：真逻辑常在极小 dex；签名/debuggable 判定、flag 形态全扫见 android-re `references/apk-triage.md`）。JNI 找不到符号 → 查 `JNI_OnLoad` 的 `RegisterNatives` 方法表 |
| WASM / Mach-O / 内核 .ko | 见 `references/triage.md` §平台速查 |
| pyc（裸字节码文件） | `references/pyc-bytecode.md`（magic→版本、反编译器矩阵、dis 兜底） |
| 固件 / binwalk 类镜像 | `references/firmware.md`（判型/提取/架构识别/Ghidra 基址反推） |
| OLLVM 混淆（bcf/fla/sub） | `references/ollvm-deobf.md`（工具选型决策表、手工 deflat、angr 化简）；识别原则仍在 `references/anti-analysis.md` §4 |
| PE DOS stub 异常大 | 查 DOS stub 藏代码（`int 16h`），Windows 题常见 |

## 分诊判据细则

- **干净 IAT 警告**（`clean_iat_warning: true`）：导入只来自 kernel32/ntdll 且 < 15 个 → 动态加载嫌疑，**禁止**据此宣称"无网络/无文件能力"；去 `strings` 找 DLL/API 名字符串、`search-decompiled "LoadLibrary"` 查证据
- **可疑 API 六组**：命中不等于恶意（where.exe 也命中 GetTickCount），看**组合**：injection 组 ≥2 个 + network 组 ≥1 个才是攻击面信号；单组单命中降级为备注
- **字符串快赢为空**：可能是宽字符（`strings -el`）、资源段字符串或自定义加密——triage 只扫已定义 ASCII 字符串
- 细节与平台速查：`references/triage.md`；命中反调试/反混淆：`references/anti-analysis.md`（识别清单、Check→Bypass 对照、OLLVM 分层）

## References

| 文件 | 何时读 |
|---|---|
| `references/triage.md` | 分诊细节：语言识别特征、壳检测、高危 API 组合、平台速查、flag 形态 regex 集（全家权威源） |
| `references/anti-analysis.md` | 命中反调试/反混淆/自校验时的识别与绕过对照表 |
| `references/dotnet-il.md` | 判出 .NET 后：de4dot 脱混淆、dnSpyEx 反编译/IL patch、混淆器对抗决策 |
| `references/pyc-bytecode.md` | pyc/PyInstaller 样本：magic→版本判定、反编译器选择矩阵、PyArmor 识别 |
| `references/firmware.md` | 固件镜像：binwalk/熵判型、文件系统提取、ARM/MIPS 基址反推导入 Ghidra |
| `references/ollvm-deobf.md` | OLLVM 混淆的工具级执行：选型决策表、手工 deflat、claripy 化简 |
