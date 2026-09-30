---
name: re-harmonyos
description: >
  鸿蒙（HarmonyOS）应用逆向：hap/hsp/har 包结构、ArkTS 字节码（.abc、ArkCompiler）分析。
  触发词：鸿蒙、HarmonyOS、hap、ArkTS、abc 字节码、方舟编译器
capabilities: [bytecode-parser]
---

# 鸿蒙应用逆向（HarmonyOS / hap / ArkTS）

## 何时使用 / 何时不用

- 用：拿到 hap（应用发布包）/ hsp（共享包）/ har（静态库归档），需要看模块配置、资源、ArkTS 业务逻辑
- 用：需要还原 .abc 字节码（ArkCompiler 产物）中的业务逻辑——字符串定位、反汇编、混淆还原
- 用：鸿蒙应用含 native 库（libs/ 下 .so），需要静态/动态联动分析
- 不用：普通 Android APK（走 [[re-apk]]；dex/smali 体系与本技能不同）
- 不用：纯 Web/前端应用（非鸿蒙容器，脚本/Web 路径走 [[re-script-deob]] 或 [[re-browser-ext]]）
- 注意：**动态执行默认沙箱（[[re-analyze/platform-tips]] 最高原则）**——静态解包/反汇编免沙箱；模拟器/真机运行观察必须进 [[re-sandbox]]

## 工具准备

参考 [[re-analyze/platform-tips]]——静态分析（解包、字符串、反汇编）免沙箱；动态步骤按最高原则进沙箱。

### hap 解包（zip 容器，通用思路）

- hap = zip 容器，与 APK 同源（同属 zip/jar 家族）——任何通用 zip 解包工具都能解（unzip / 7-Zip / python3 zipfile 模块），不绑死单一实现
- 流程与 [[re-apk]] 同源：先列清单（`unzip -l`）→ 再解包 → 验证完整性（CRC/文件数对照）
- 专业解包工具（集成 module.json 解析与资源提取）可作备选，注意按发行版本选择对应版本
- 验证: 解包后目录结构完整（对照步骤 1 的清单）

### python3（字符串提取与脚本）

- Linux: `apt install python3` / `dnf install python3` / `pacman -S python`；macOS: 自带；Windows: 官方安装器
- zipfile 为标准库：`python3 -m zipfile -l app.hap` 列清单、`python3 -m zipfile -e app.hap out/` 解包
- 验证: `python3 --version`

### 字符串/资源提取工具

- `strings`（binutils 自带）与 `grep`：捞 .abc 与资源中的 URL、密钥、提示语
- 资源文件（布局、图片、rawfile）先用 `file` 判断类型再提取

### ArkCompiler 反汇编器（针对 abc 的替代，泛化描述）

- [[re-java]] 的 jadx 类思路复用：Android 用 jadx 解 dex，鸿蒙侧对应的是 ArkCompiler 反汇编工具——官方工具链（随 SDK 发行）与开源实现均可，选能输出指令级汇编（指令助记符 + 操作数/常量引用）的实现即可，多个实现可交叉验证
- 版本匹配：先识别编译版本再选工具（见坑 2）

## 操作步骤

按顺序执行；每步产物（解包目录、反汇编输出 + sha256）存档（见 [[re-triage]]）。

1. **包结构识别与解包**：
   ```sh
   file app.hap
   unzip -l app.hap | head -30
   unzip -o app.hap -d out/
   ```
   - hap ≈ APK 变体：`module.json`（模块配置，等价 manifest：入口/权限/组件声明）、`resources/`（资源，等价 res/）、`ets/`（ArkTS 编译产物所在，.abc 字节码）、`libs/`（native .so）、`assets/`（rawfile 等原始资源）
   - hsp / har 同为 zip 容器，结构类似（hsp 含 .abc，har 为静态库归档），解包流程一致
   - zip 容器解包流程与 APK 同源（[[re-apk]]）：列清单 → 解包 → 校验；发现嵌套容器则递归解（见坑 4）

2. **字节码识别（.abc）**：
   ```sh
   find out/ -name "*.abc" | head
   xxd out/ets/modules.abc | head -10    # 看文件头
   ```
   - `.abc` 是 ArkCompiler（方舟编译器）字节码文件，业务逻辑主体；文件头含固定魔数与版本字段，其后为段结构（字符串段/字面量段/指令段等，具体布局随编译版本演进）
   - 旧版本布局有差异（模块文件命名/位置不同）——以解包清单为准；`file` 识别不出时用 `xxd`/python3 读头部，先识别编译版本再定工具（见坑 2）

3. **业务逻辑还原（字符串 + 反汇编）**：
   ```sh
   strings -n 8 out/ets/*.abc | grep -iE 'https?://|key|secret|token|sign' | head
   grep -rnE 'https?://|key|secret' out/resources/ | head    # 资源内字符串也是线索
   ```
   - 字符串定位：.abc 内字符串以常量形式存储，strings/grep 可捞 URL、密钥、提示语——从敏感串反查引用点，沿调用链还原逻辑（思路同 [[re-java]] 的字符串定位）
   - ArkCompiler 反汇编：输出指令级汇编后，先找入口与敏感串引用点，再看常量加载与调用关系还原流程
   - JS/TS 业务资源提取：hap 内可能含明文 JS/TS 片段（assets/、rawfile、未编译资源）——提取后按 [[re-script-deob]] 方法处理（美化、去混淆、解码）
   - 混淆后函数名变短名时，字符串与行为兜底（见坑 3）

4. **与 Android 异同**：
   - 无 dex/smali 层：业务逻辑在 .abc（ArkCompiler 字节码），不是 dex——smali 补丁、baksmali 等思路不直接适用，对应物是 ArkCompiler 反汇编
   - 资源与 manifest 结构类似：module.json ≈ AndroidManifest（入口/权限/组件）、resources/ ≈ res/——[[re-apk]] 的资源分析思路（资源转储、字符串资源定位）部分复用，工具换鸿蒙侧对应物
   - 工具链复用与差异：zip 解包、字符串提取、`file` 识别、native so 分析（[[re-format-elf]] + [[re-ghidra]]）全复用；dex 相关工具（jadx/apktool）不适用，由 ArkCompiler 反汇编器替代；动态 hook 思路（[[re-frida]]）在鸿蒙模拟器/真机仍可用，挂载方式随环境差异调整

5. **动态侧（沙箱）**：
   - 模拟器/真机运行时观察，编排走 [[re-mobile]]：安装 hap（官方部署工具）→ 启动观察 → 抓包/日志 → hook 运行时取明文，与静态反汇编互证
   - 一律在 [[re-sandbox]]（模拟器快照 / 受控设备 + 网络隔离）内执行，遵循 [[re-analyze/platform-tips]] 默认沙箱原则

## 跨域联合

- [[re-apk]]：zip 容器解包流程同源、manifest/资源分析思路复用
- [[re-hybrid-app]]：hap 内嵌 WebView/混合框架（JS bundle）时，按框架类型分流处理
- [[re-java]]：jadx 类反编译器思路复用（abc 侧对应 ArkCompiler 反汇编工具）
- [[re-mobile]]：动态侧编排（模拟器/真机 + hook + 抓包），本技能挂靠该网关域
- [[re-script-deob]]：提取出的明文 JS/TS 业务资源去混淆
- 底座：native so → [[re-binary-core]]（[[re-format-elf]] / [[re-ghidra]]）；初勘 → [[re-triage]]；动态沙箱 → [[re-sandbox]]；沙箱原则 → [[re-analyze/platform-tips]]

## 常见坑与陷阱

- **Android 工具直接开 hap 漏 ets 目录**：现象——jadx/apktool 打开 hap 报错、或只见资源与配置不见业务代码；原因——dex 系工具不认识 .abc，ets/ 目录被跳过；对策——按步骤 1 先做完整 zip 解包与清单核对，业务代码用 ArkCompiler 反汇编器，不要依赖 dex 工具
- **abc 反汇编器版本敏感**：现象——反汇编报错、输出错位或指令对不上；原因——ArkCompiler 持续演进，不同编译版本的字节码布局/指令集有差异，工具按版本匹配；对策——先识别编译版本（文件头版本字段 + module.json/构建信息），再选对应版本工具，必要时多实现交叉验证
- **混淆后短名用字符串兜底**：现象——反汇编里函数/变量全是短名，逻辑读不通；原因——构建期混淆/压缩抹掉语义；对策——字符串表与资源兜底：grep URL/提示语/密钥串 → 定位引用点 → 沿调用链恢复语义，配合动态行为对照
- **hap 双容器解包不完整**：现象——解包后缺资源/缺模块、运行时资源错乱；原因——部分版本构建在 zip 内再嵌套资源容器（内部 zip/资源索引），单层解包只拿到外层；对策——解包后检查嵌套容器并递归解到模块/资源文件为止，用 CRC/文件数对照验证完整性
- **业务逻辑在 native so 里**：现象——.abc 里找不到核心算法/加密；原因——敏感逻辑下沉 libs/ 下的 .so（JNI/NDK 风格）；对策——so 走 [[re-format-elf]] + [[re-ghidra]]（[[re-binary-core]]），结合 .abc 侧调用点还原整体流程
