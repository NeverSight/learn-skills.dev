---
name: re-nim
type: atomic
description: >
  Nim 编译产物逆向：运行时识别、NimString 结构、异常与 GC 路径。
  触发词：Nim逆向、nim、NimString、NimMain、nim 产物。
capabilities: [lang-runtime-analysis]
---

# Nim 逆向

## 何时使用 / 何时不用

- 用：Nim 产物（`NimMain` / GC 符号、NimString 结构特征），需要还原字符串逻辑、异常路径、GC/所有权关系
- 用：Nim/C 混合产物中区分 Nim 侧代码（按符号来源分组后 Nim 侧进本技能路径）
- 不用：纯 C/C++ 产物（走 [[re-cpp-abi]] / [[re-binary-core]] 通用路径）
- 不用：只需函数逻辑（直接反编译技能）

## 工具准备

### readelf / llvm-nm（符号与节分析）

- 安装与验证见 [[re-cpp-abi]] 工具准备
- Nim 产物以 ELF 为主（Linux 默认 C 后端）；macOS 用 llvm-nm

### Ghidra / IDA（反编译底座）

- 安装与验证见 [[re-ghidra]] / [[re-ida]]；Nim 符号（NimMain/NimStringV2 等）导入后直接可读

### nim 编译器（可选，对照编译）

- Linux: `apt install nim` / `dnf install nim` / `pacman -S nim`；macOS: `brew install nim`；Windows: choosenim/官方安装器
- 验证: `nim -v`；用途: 同版本编译对照产物，验证字符串布局/GC 符号形态（版本差异见 [[layout]]）

### xxd + Python struct（字节级核对）

- 系统自带（`xxd`）；Python 3 自带 `struct`
- 用途: 符号/布局输出异常时按偏移直接解析 NimString 与对象结构（示例见 [[examples]]）

## 操作步骤

按顺序执行，每步产物存档（路径 + sha256，见 [[re-triage]]）。

1. **产物识别**：
   ```sh
   readelf -s sample | grep -iE 'NimMain|nimGC|NimString' | head   # ELF；Mach-O 用 llvm-nm
   readelf -s sample | grep -iE 'nimIncRef|nimDecRef|rawNewString|eqStrings' | head
   ```
   - Nim 特征：`NimMain`（入口链）、GC 符号（refc 的 `nimGC_*` / orc 的 `nimIncRefCyclic` 等）、`NimStringV2`/`NimStringDesc` 结构类型
   - 注意：release 构建下 GC 符号常被内联/消除（见坑 1），靠 `NimMain` 与字符串函数兜底
   - 入口链：C `main` → `NimMain` → `NimMainInner` → `NimMainModule`（模块初始化）→ 业务 main
   - 模块初始化顺序按依赖拓扑（import 关系）：`NimMainModule` 内的初始化段先跑被依赖模块——在初始化段断点/下钻时按调用序对照 import 链

2. **字符串与序列结构（先判 GC 模式）**：
   - **orc/arc**（2.x 默认 orc）：`NimStringV2 = {len: int, p: ptr NimStrPayload}`；`NimStrPayload = {cap: int, data: 内联字符数组}`——字符串是"len + 堆上 payload 指针"，cap 高位带字面量标记位（见 [[layout]]）
   - **refc**（旧默认）：`NimStringDesc = {len, reserved, data[]}`——字符内联在结构体里
   - 定位：`rawNewString`（1.x 与 2.x 均为此 importc 名）分配调用点 → 结构布局 → 字符串操作函数（`eqStrings` 等）
   - 分析：字符串比较点是关键逻辑（校验/协议/命令分发）——`eqStrings` 调用点即字符串相等判断
   - 序列（seq）与 string 同构：v2 布局同为 `len + payload 指针`（payload 带 cap），refc 同为 `len/reserved + 内联`——按同一判别表处理
   - 内存视图（v2 布局，64 位）：
     ```
     栈/对象内:  len(int64) | p(ptr) ───────────────┐
     堆上 payload:  cap(int64, bit62=字面量标记) | data[cap+1] ←┘
     ```
     字符串本体只有 16 字节句柄，内容在独立堆块——分析对象结构时按句柄跳转，别在对象里找字符数据

3. **内存中定位字符串（动态/转储场景）**：
   ```python
   # 在内存转储中按 v2 布局找字符串：cap 是 8 字节对齐的容量值，data 后跟可打印 ASCII
   # 候选: 8 字节对齐的 cap + len 匹配的 data → 反推 NimStringV2 起点
   ```
   字符串内容在堆上 payload 里，栈上只有 len+指针；先按 `cap` 前缀特征定位 payload，再往回找引用它的 NimStringV2（[[examples]] 有完整示例）。

4. **异常与 raises 路径**：
   - Nim 2.2.x（Linux x86-64 默认）异常走 goto 式异常表，**无 setjmp 符号**；raise 路径经 `raiseExceptionEx`/`raiseExceptionAux`
   - 老默认（`--exceptions:setjmp`，Nim 2.0 及以前）用 setjmp/longjmp：`nimSetjmp` 符号可见
   - 定位：`raiseExceptionEx` 调用点 → 异常对象分配与消息 → catch 分支（异常表驱动）
   - 分析：异常路径揭示输入校验与失败处理，比正常路径更早暴露边界条件

5. **GC 与引用计数（按 GC 模式分叉）**：
   - refc：引用计数 + 周期收集——`nimGC_*`/`nimGCunref`/`nimIncRef`/`nimDecRef` 调用点
   - orc/arc：ARC 语义——`nimIncRefCyclic`/`nimDecRefIsLastCyclicDyn` 等；显式 inc/dec 少，释放由编译期插入
   - 分析：GC 调用点帮助识别对象生命周期与所有权（配合字符串结构）；release 下内联后改用分配/释放边界推断

6. **C 混合编译边界**：
   - `{.compile:}` / `{.importc:}` 混合时 Nim 与 C 符号并存：Nim 侧符号带模块前缀（`hello__u8` 形态）与运行时（NimMain/NimString），C 侧符号无
   - 边界处是逻辑入口：Nim 业务逻辑在 NimMain 调用链内侧，C 库调用经导入表

7. **stripped 产物兜底**：
   ```sh
   strings -n 6 sample | grep -E '@m.*\.nim\.c' | head      # C 生成缓存文件名（含模块名，release 也嵌入）
   strings -n 6 sample | grep -iE 'fatal\.nim|Exception' | head
   ```
   - `NimMain` 等被 strip 后按特征串（`@m<模块>.nim.c`、std 运行时源文件名）与运行时行为识别（[[re-triage]] 初勘兜底）；业务源码名不嵌入二进制，别指望它

## 跨域联合

- [[re-binary-core]] 网关：本技能归属（选择树「Nim 产物」分支）
- [[re-analyze/analysis-contract]]：符号表按数据契约传递
- [[re-cpp-abi]]：C 混合侧与无 RTTI 判别参考
- [[re-triage]]：初勘兜底（strip 产物按特征串识别）

## 常见坑与陷阱

- **GC 版本差异（refc/orc）**：现象——找不到引用计数调用；原因——orc 无显式 inc/dec（ARC 语义）且 release 下 GC 符号内联；对策——先按 Nim 版本与 GC 模式确认再分析，debug/refc 构建符号更全
- **NimString 布局随 GC/版本变化**：现象——按 `len/reserved/data` 手写解析器读 2.x 产物全错；原因——2.x orc 默认是 `NimStringV2{len, p}`（payload 带 cap），`len/reserved/data` 内联是 refc 的 NimStringDesc（1.x 默认）；对策——先确认产物 GC 模式（见 [[layout]] 判别表）再选布局：debug 构建看 GC 符号（refc 有 `nimGCunref`，orc 有 `nimIncRefCyclic`），release 构建看分配函数命名与 cap 字段是否出现
- **导出符号被 strip**：现象——无 NimMain/NimString 符号；原因——strip 处理；对策——按特征字符串/运行时行为识别（步骤 6 兜底）
- **C 混合编译**：现象——Nim/C 符号混杂；原因——`{.compile:}` 混合；对策——按符号来源分组，Nim 侧进本技能路径
- **字符串比较点误判**：现象——关键校验被当普通比较；原因——eqStrings 包装；对策——追踪 Nim 字符串函数调用点定位比较逻辑
- **异常实现代际误判**：现象——按老思路找 nimSetjmp 找不到；原因——2.2+ Linux amd64 默认 goto 式异常（无 setjmp）；对策——无 nimSetjmp 时沿 `raiseExceptionEx` 与异常表定位 catch，别当"无异常处理"
- **release 内联导致符号稀疏**：现象——debug 能看到的 nimGC_*/eqStrings 在 release 里消失；原因——-d:release 内联；对策——release 产物按行为特征（分配/释放边界、字符串函数调用模式）分析，符号表只是线索不是依据
- **字符串内容在堆上，栈上只有句柄**：现象——在栈上按内容搜索字符串找不到；原因——v2 布局的字符数据在独立 payload 堆块里，栈上只有 `len + p` 两个字段；对策——动态/转储场景先按 cap 前缀特征定位 payload 块，再回找引用它的句柄（[[examples]] 内存定位示例）
- **32 位产物结构尺寸减半**：现象——64 位布局表套 32 位产物偏移全错；原因——NI 在 32 位平台是 4 字节（NimStringV2 为 8 字节而非 16，NimStrPayload cap 为 4 字节）；对策——解析前先确认产物位数，按 4/8 字节 NI 选结构尺寸
- **非 PIE 老构建入口即固定地址**：现象——`readelf -h` 的 e_entry 是绝对地址（如 0x401xxx），在内存里直接对得上；原因——非 PIE 构建（老默认）；对策——入口链定位用符号（NimMain 三连）不依赖 PIE 与否，但换算地址时按 e_type 区分
