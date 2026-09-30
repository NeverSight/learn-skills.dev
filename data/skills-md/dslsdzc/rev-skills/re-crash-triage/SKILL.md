---
name: re-crash-triage
description: >
  崩溃/漏洞样本分析：确定性复现、ASAN/UBSAN 报告解读、输入最小化
  (afl-tmin/cmin)、gdb 回溯定位、rr 录制重放、PoC 产出。
  触发词：崩溃、crash、ASAN、UAF、堆溢出、越界、段错误、segfault、
  core dump、PoC、漏洞分析、崩溃分析。
capabilities: [debugging]
---

# 崩溃分析与漏洞定位（crash triage）

## 何时使用 / 何时不用

- 用：fuzz 产出崩溃输入；程序段错误/abort；需要判断崩溃是否真实漏洞（可达性）并产出最小 PoC；多线程/非确定性崩溃需复现
- 不用：还没崩溃、要主动找 bug（→ [[re-fuzzing]]）；崩溃已定位、需要深挖函数逻辑（→ [[re-binary-core]] 底座）
- 不用：只需要看符号栈（直接 [[re-gdb]] 亦可，但本技能含完整"复现→最小化→定位→PoC"流程）

## 工具准备

所有工具先验证再使用。复现崩溃是动态执行，默认沙箱内跑（[[re-analyze/platform-tips]] 最高原则，见 [[re-sandbox]]）。

### ASAN / UBSAN —— 内存与未定义行为检测（clang/gcc 内置）

- clang: `sudo apt install clang` / `sudo dnf install clang` / `sudo pacman -S clang` / macOS Xcode 自带
- gcc: Debian/Ubuntu `sudo apt install gcc`（ASAN 内置在 gcc，无独立包）；Fedora `sudo dnf install gcc`；Arch `sudo pacman -S gcc`
- 编译: `gcc -fsanitize=address,undefined -g -fno-omit-frame-pointer -o target_asan target.c`（clang 参数相同）
- 验证: 写一个数组越界小程序编译运行，确认输出含 `AddressSanitizer` 字样

### gdb —— 回溯与 core 分析

- Debian/Ubuntu: `sudo apt install gdb`
- Fedora/RHEL: `sudo dnf install gdb`
- Arch: `sudo pacman -S gdb`
- macOS: `brew install gdb`（需 codesign 授权）；Xcode 自带 lldb 亦可（见 [[re-lldb]]）
- Windows: WSL 内 Linux 版；Windows 本机用 WinDbg（[[re-windbg]]）
- 验证: `gdb --version`

### rr —— 录制/重放（非确定性崩溃）

- Debian/Ubuntu: `sudo apt install rr`（universe 仓库）
- Fedora/RHEL: `sudo dnf install rr`
- Arch: `paru -S rr`（AUR 包；官方仓库无 rr）
- macOS: 无支持（rr 仅支持 Linux，官方原话 "Apple hardware is fine, Apple software is not"）；Apple Silicon 用户用 Asahi Linux 或 Linux 虚拟机（需 PMU 透传）
- Windows: WSL2 内 Linux 版
- 源码编译:
  ```sh
  git clone https://github.com/rr-debugger/rr && mkdir rr/obj && cd rr/obj
  cmake -DCMAKE_BUILD_TYPE=Release ../rr && make -j$(nproc) && sudo make install
  ```
- 前置: Linux 内核 3.11+（建议 4.7+）；`perf_event_paranoid` > 1 时超慢，先放开：
  ```sh
  sudo sysctl kernel.perf_event_paranoid=1
  ```
- 虚拟机内需 PMU 透传（VMware/KVM 可，VirtualBox 不可）
- 验证: `rr --version`

### afl-tmin / afl-cmin —— 输入最小化与去重（随 AFL++ 安装）

- 安装见 [[re-fuzzing]] 的 AFL++ 一节（`afl-tmin` / `afl-cmin` 随包安装）
- 验证: `afl-tmin -h`

## 操作步骤

按顺序执行；崩溃输入与 PoC 先 sha256 存证（[[re-triage]] 方法）。

1. **确定性复现**：
   ```sh
   sha256sum crash_input > crash_input.sha256
   ./target < crash_input          # stdin 输入
   ./target crash_input            # 文件输入
   ./target -f crash_input         # 按目标实际参数形态
   ```
   - 连续跑 3 次都崩 = 确定性崩溃，继续第 2 步；时崩时不崩 = 非确定性（多线程/未初始化/ASLR），跳到第 4 步用 rr
   - core dump 开启（崩溃后留 core 供分析）: `ulimit -c unlimited`；`cat /proc/sys/kernel/core_pattern` 若指向 systemd-coredump/apport 则 core 会被系统收走（见坑 4）
2. **ASAN 报告解读**（目标须为 `-fsanitize=address -g -fno-omit-frame-pointer` 构建，见工具准备）：
   - `heap-buffer-overflow` / `stack-buffer-overflow` / `global-buffer-overflow`：越界读写——报告含越界方向（`READ of size N` / `WRITE of size N`）与越界偏移
   - `heap-use-after-free`：UAF——看 `freed by` 与 `allocated by` 两段栈，找释放点与再使用点
   - `attempting double-free`：重复释放
   - `SEGV`：空指针/野指针访问，细节需 gdb 补（第 4 步）
   - 关键：`#0` 帧是崩溃点，**别只看行号**——结合数据流向判断是哪个输入字节导致
3. **输入最小化**：
   ```sh
   afl-tmin -i crash_input -o crash.min -- ./target @@
   # 多个崩溃输入先按路径去重：
   afl-cmin -i crashes_dir -o minimized -- ./target @@
   ```
   - afl-tmin 产出保持崩溃的最短输入；可再手工删头/尾字节验证（二分查找最小边界）
   - 最小化后输入即 PoC 底稿；崩溃类型保持 = 同一 bug 的判定依据
4. **gdb 回溯定位**：
   ```sh
   gdb -q ./target
   (gdb) set disable-randomization on     # 关 ASLR 便于地址对照
   (gdb) run crash.min
   (gdb) bt                                # 完整回溯
   (gdb) info registers                    # 崩溃点寄存器
   (gdb) x/16i $pc                         # 崩溃点反汇编
   ```
   - core 文件分析：`gdb -q ./target /path/to/core`
   - `bt` 全是 `??`（无符号）：记模块基址 + 偏移，进 [[re-ghidra]] / [[re-ida]] 反编译补帧（见坑 5）
   - 非确定性崩溃 → rr 录制重放：
     ```sh
     rr record ./target crash_input
     rr replay                            # 打开 gdb 会话
     (rr) continue                         # 跑回崩溃点
     (rr) bt
     (rr) reverse-continue                 # 崩溃前反向执行找根因
     ```
5. **PoC / 报告**：
   - PoC：`crash.min` + sha256 + 复现命令（环境：ASAN 构建参数、运行参数、输入通道）
   - 报告要点：崩溃类型（ASAN 类别）、崩溃点函数/行/偏移、数据流向（哪个输入字节 → 越界下标）、根因（长度校验缺失 / 索引未验证 / 释放后使用）、**可达性**（见坑 3：崩溃路径真实可触达、输入可控）、影响评估（越界读→信息泄露、越界写→RCE、纯崩溃→DoS）、修复建议
   - 产出：PoC hash 与崩溃特征可进 [[re-ioc]]

## 跨域联合

- [[re-vuln]]：本网关工作流第 3 步固定调用本技能（崩溃分析是漏洞挖掘链路的核心环节）
- [[re-fuzzing]]：其崩溃产出（`out/crashes/`）交本技能分析（本技能也反向使用其 afl-tmin/cmin 工具链）
- [[re-binary-core]]：定位后补符号/读函数逻辑走底座（[[re-ghidra]] / [[re-ida]] / [[re-radare2]]）；[[re-triage]] 提供存证方法
- [[re-memdump]]：进程已死 / 已有 core 文件需更多上下文时转储分析（崩溃 core → memdump）
- [[re-sandbox]] / [[re-analyze/platform-tips]]：复现是动态执行，默认沙箱内跑

## 常见坑与陷阱

- **非确定性崩溃（多线程）**：现象——同一输入 10 次里崩 3 次，gdb 重跑复现不了；原因——线程竞态 / 未初始化内存 / ASLR 地址差异；对策——rr 录制（`rr record ./target input`）在崩溃点自动停止，`rr replay` + `reverse-continue` 反向定位根因；先 `set disable-randomization on` 排除 ASLR 因素
- **ASAN 与优化差异**：现象——ASAN（-O0/-O1）崩溃但 release（-O2）不崩，或反过来 release 才崩；原因——优化改变内存布局/时序，掩盖或暴露未定义行为；对策——两种构建都试；补 `-fsanitize=undefined` 抓 UB；影响与可达性判断以真实 release 行为为准（ASAN 报出的是潜在漏洞，需确认）
- **崩溃≠漏洞（可达性）**：现象——ASAN 报越界但在死代码/不可达分支，或崩溃由 harness 引入；原因——fuzzer 触发的输入未必对应真实攻击面；对策——gdb 回溯 + 反编译确认崩溃路径可触达、输入可控；区分 harness bug 与目标 bug（[[re-vuln]] 工作流第 4 步兜底确认）
- **core 被系统收走**：现象——`ulimit -c unlimited` 后崩溃仍无 core 文件；原因——`core_pattern` 指向 systemd-coredump（管道方式）/apport 拦截；对策——`cat /proc/sys/kernel/core_pattern` 确认；临时 `sudo sysctl kernel.core_pattern=core`（core 落到工作目录）；或 `gdb --args ./target crash.min` 直接跑、不依赖 core
- **符号缺失**：现象——`bt` 全 `??`、地址对不上；原因——strip / 静态链接 / 二进制与 core 版本不一致；对策——core 与二进制必须同版本（对比 sha256）；记录崩溃模块基址与偏移，在 [[re-ghidra]] / [[re-ida]] 按偏移定位函数，换算回 gdb 地址
