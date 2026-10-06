---
name: re-dynamic
description: 让二进制跑起来观察行为（dynamic analysis）：直接运行（ELF 走 WSL、PE 走本机）、函数级 Oracle（单函数调用+观察输入输出）、Frida 插桩、gdb/qiling 入口指引。触发：静态看不懂/需要验证函数行为/拿到 check 函数要试输入/想"先跑起来看看"。不做静态分析——那是 ghidra-static。动手前必须先用 skill 工具加载本 skill 全文并遵守其流程；一切观察/结论用 ledger.py 落账。
whenToUse: 静态分析卡住要运行时事实时；验证 check 函数/算法猜想（喂输入看返回）；样本行为观察（先跑起来看）；需要 Frida/gdb/qiling 动态手段的入口指引
---

# RE Dynamic（场景 4：跑起来看）

前置：静态卡住或要验证猜想 → 从 `~/.dsh/skills/ghidra-static` 来；判型不明先 `~/.dsh/skills/re-triage`／后继：拿到运行时事实后回 ghidra-static 标注进台账

> **先跑起来看**：对可执行样本，静态深挖前先花 2 分钟跑一遍观察 I/O——运行行为常常直接告诉你程序结构（菜单、校验提示、魔数），省掉半小时静态。（铁律全文见 ghidra-core §1）

## 路径约定

```bash
ORACLE="$HOME/.dsh/skills/re-dynamic/scripts/oracle.py"
# 后端：qiling（Windows 走 WSL Ubuntu /root/re-pwn-venv；WSL/Linux 下同一 venv 原生可用，
# rootfs /root/qiling-rootfs，均已装）
# re-tools venv：Windows ~/Desktop/src/re-tools-venv/Scripts/python.exe；Linux ~/re-tools-venv/bin/python
# win_gui_drive.py 为 Windows-only；frida_time_hook.py 双平台
# 跨架构（WSL 已装）：qemu-riscv64 / qemu-aarch64（qemu-user 直接跑 foreign-arch ELF）、
#   gdb-multiarch（target remote :1234 配 qemu -g）；binutils 手读只核对单点，整份反编译走 Ghidra
```

## 1. 直接运行（第一选择，最便宜）

```bash
wsl -d Ubuntu -- /mnt/c/.../sample          # ELF（含加壳判断后的产物）
./sample.exe                                 # PE 本机直接跑
qemu-riscv64 /path/to/chall                  # foreign-arch ELF（readelf -h 确认 e_machine 后）
qemu-riscv64 -g 1234 /path/to/chall &        # 配 gdb-multiarch：target remote :1234
```

**跨架构铁则**：foreign-arch ELF（riscv64/aarch64/mips…）**先 import 进 Ghidra 用对应 processor 反编译**，objdump 只用于核对单点——"参数角色靠调用约定手读 asm 推断"是错模型的典型来源（DEFCON26 复盘 R1）。跨架构题常带 host/协议层多方件，记账用 `ledger.py conclude --locus proto:/channel:` 前缀（非地址型，铁律 7）。

来源不明/疑似恶意的样本先评估再跑（快照 VM 更佳）；程序等输入就给输入，看输出猜结构。**观察到的每一个行为事实都用 ghidra-core `scripts/ledger.py observe` 回写台账**（机制见 ghidra-core references/evidence-ledger.md）。

⚠️ **LD_PRELOAD 对静态链接样本完全失效**（encode 复盘 RETRO§3.2）：静态链接 ELF 没有动态符号解析，hook  libc 函数、伪造时间源、拦截 OpenSSL 全部不生效。先 `file` 确认链接方式；静态链接样本的替代通道：① 直接 patch 二进制（ghidra-core `patch_bytes`）；② oracle.py/qiling 的 syscall hook；③ Frida spawn 注入（不依赖动态链接）。不要在静态链接样本上调试"为什么 LD_PRELOAD 没反应"超过一轮。

## 2. 函数级 Oracle（oracle.py）

给定二进制 + 函数地址（Ghidra listing 里的地址）+ 参数，真实调用该函数并返回 JSON（retval/stdout/regs/stop_reason）。CTF check 函数验证的标准动作：喂候选输入，看返回 0/1。

```bash
python "$ORACLE" <binary> 0x101064 1 0x20              # 整参（SysV 前 6 / Win64 前 4）
python "$ORACLE" <binary> 0x1020a0 str:flag{guess}     # 字符串参数（自动写内存传指针）
python "$ORACLE" <binary> 0x1020a0 str:test @out.json  # @out 落盘约定
```

**能力与边界（v2，实测）**：

| 场景 | 状态 |
|---|---|
| 静态链接 ELF，任意函数（含 libc 调用） | ✅ 加 `--init-until <main 的 Ghidra 地址>` 先跑 CRT 初始化 |
| 动态链接 ELF，**leaf 函数**（不调 libc：XOR/比较/数学） | ✅ 直接调（PIE/非 PIE 地址自动换算） |
| 动态链接 ELF，调 libc 的函数 | ⚠️ `--init-until` 供使用，但 glibc 版本与 rootfs 不符时初始化可能崩（UC_ERR_FETCH_UNMAPPED）→ 升 Frida/gdb |
| **i386 ELF（32 位）** | ✅ v2 已支持（参数按 cdecl 压栈；rootfs x86_linux） |
| PE（qiling windows rootfs） | 实验性：leaf 函数可调；复杂 PE 可能撞 API stub 缺失 → 升 Frida |
| 浮点参数 / 结构体参数 | 未支持（整型+字符串） |

**中间态取证（`--break` + `--dump`，v2 新增）**：在指定 PC 停下 dump 内存表达式，不用手写 gdb 脚本抓流水线中间态（base64 产物、XOR 中间值、比较前的密文缓冲区）：

```bash
python "$ORACLE" ./encode 0x804887c --init-until 0x804887c \
    --break 0x8048a10 --dump ebp-0x8c:28 --dump 0x804a020:32 --dump eax
```

dump 表达式：`reg+/-0xoff:len`（寄存器相对）、`0x地址:len`（Ghidra 地址，自动换算运行时）、裸 `reg`（只读寄存器值）。`--max-hits N` 控制断点命中几次后停录（默认 1）。断在函数入口时 prologue 尚未执行——`ebp` 还是调用者的，栈参数用 `esp+4:8`（32 位）/寄存器（64 位）读。

已知行为：libc stdout 全缓冲——oracle 的 `stdout` 可能为空但 retval 正确，需要输出证据时在函数里找 write/puts 直接调用或看 retval。

## 3. 升级阶梯（oracle 不够用时）

① **Frida**（re-tools-venv 已装）：真实进程 hook——反仿真/复杂 API/要看中间状态时用；`frida`/`frida-trace` 入口见 ghidra-static references/ctf-patterns.md §6
② **gdb + pwndbg**（WSL 已装）：断点单步、内存断点；`wsl -d Ubuntu -- gdb /mnt/c/.../sample`
③ **angr**（re-tools-venv 已装）：符号执行求输入——"什么输入能让 check 返回 1"的直接求法，路径爆炸时慎用

## 3.5 四个高价值套路（五题复盘 + chal 复盘实战）

**① 外部随机/时间源是输入，不是逻辑**：校验依赖 `time()`/随机数/环境时，先判它是"输入"还是"逻辑"。是输入 → **合法地构造/覆写它**，把概率型 oracle 变成确定性 oracle——且不需要 patch 任何字节，天然满足铁律 10 的验证独立性（复盘实例：snake.exe 的 4 个关键格子由 `time.time()` 播种，命中概率 1/40320；枚举 FILETIME 后 frida hook `GetSystemTimeAsFileTime` 覆写返回值，未修改的二进制自己打印 flag）。覆写模板：`scripts/frida_time_hook.py`（Windows `GetSystemTimeAsFileTime` / Linux `time`/`gettimeofday` / Java `System.currentTimeMillis`）。

**② Windows GUI 消息驱动（模态对话框程序的 oracle）**：用 pywin32 驱动 GUI 程序批量试输入。实测两条铁律：
- **打开窗口用 `PostMessageA`**：模态对话框（`DialogBoxParam`）里 `SendMessageA` 会死锁
- **高频连点回 `SendMessageA`**：`PostMessage` 队列约 10000 条后静默丢弃（实测发 19999 次只到 12205 次）

组合记忆：**打开用 Post、连点用 Send**。驱动脚本：`scripts/win_gui_drive.py`。

**③ 打桩 oracle 家族（单因子隔离）**：任一因子（函数返回值/随机源/配置字）是否参与计算存疑时，不要继续读码——把它打桩成常量看输出变不变。工具：ghidra-core `scripts/oracle_family.py`，binary + `--stub 0xaddr=0xval`（同地址多个值 = 一个家族）批量产 patched 副本（x86-64 函数头写 `mov eax,imm32;ret`）逐个运行出差分表：**输出变 ⇒ 该因子参与计算；任意常量下都不变 ⇒ 无关通道，立即停止在它上面读码**。这是推翻"参数角色读反"类错模型的决定性实验（DEFCON26 复盘 R1：`FUN_13d74` 角色被读反，错模型持有数小时；打桩实验几分钟即证伪）。落账按 `--source runtime-oracle`；注意这是 patch 态运行，只回答"参不参与"，验证数据模型仍须未修改进程 + 独立来源（§4①）。

**④ 机器真值路线（gdb 帧槽位取数，chal 复盘 E6）——四前置条件全满足才走**：

1. 本机可运行的 **native** 样本（CPython 扩展/so/未壳 PE）；
2. 语义落在**栈槽**上（函数参数/局部变量，而非寄存器即时值）；
3. 上游有**宿主语言层遮住真值**（Cython 包装、FFI 边界、回调入 native）；
4. 「反编译文本 → 模型」**连续两轮对不上**（扰动实验先做过，铁律 14）。

满足 → **不要把它当最后手段**：断在 Python API 包装函数（`PyLong_FromLong` 等），dump 调用者栈帧按槽位取真值。**自写解码器先用已知值自检**（解一个 `int(1)` 就知道布局判没判对——CPython ≥3.12 是 `lv_tag`（`ndigits<<3|sign`），pre-3.12 是 `ob_size`；布局判别与 `const_scan --binary` 同源；chal 复盘 E5：第一版按 `ob_size` 解 3.12 全部解成 `None`，空结果本身就是强异常信号）。**反例（不要走这条路）**：Go/Rust 大二进制（先 pclntab/GoReSym、`rustfilt` demangle）、加壳样本（先 re-unpack 脱壳）、.NET/Java/DEX（反编译层更高效）、内核/固件/跨架构（remote stub 或 qemu-user，见跨架构铁则）。


## 4. 验证可信度（铁律 10 细则，encode 复盘 E2/E3）

**① patch 态禁区**：被 patch 过的运行态（`write-bytes`/`assemble`/调试器改字节/改寄存器/跳过长度门）
只能用于**探索控制流**，禁止用于**验证数据模型**。验证数据模型必须同时满足：

- 进程未修改，或修改点与测量点**无数据依赖**（patch 了长度门再去读缓冲区 = 溢出直接污染测量对象，同源）
- 至少一个**独立来源**交叉印证：静态常量（read_views）/ 第二输入 / 已知明文

被迫在 patch 后测量的结论，落账必须 `ledger.py conclude --independent no`（render 标 ⚠UNVERIFIED），
交付时显式声明「自我一致，未独立验证」。**模型与 trace 同源于「我的理解」，二者一致不构成证据。**

**② harness 自检门**：任何自建投喂/读数 harness（subprocess 管道、gdb 批处理、输入文件重定向），
在用于**支撑结论**之前必须用已知答案的输入自检——例如喂 10 字节，断言程序实际收到 10 字节、
NUL 在 +10。自检失败或同输入多次运行结果不同 → **该 harness 全部输出作废**，不得作为证据，
并在台账 `--harness <路径:版本>` 标注。已知坑：`subprocess`+文件重定向竞态（fd 未同步就 fork）、
`gdb < input.txt`（gdb 与 inferior 抢同一 fd，输入多/少 1 字节）。

**③ 偶发命中不是发现**：「随机 N 个输入里 K 个命中」必须复跑 ≥100 次确认可复现，
否则按 harness 不可信处理（回 ②）。幽灵命中率（12/2000 但复跑 0/300）是工具 bug 的签名，不是程序的。

**④ 矛盾读数的第一动作**：`strlen` 忽大忽小、同一缓冲两次读出不同值 → 先交叉验证工具
（独立 harness / strace / oracle.py --dump），禁止为矛盾编造机制（「IFUNC 怪癖」之类）。

**⑤ 独立 oracle 引擎排序（挑"独立引擎"时先看这条）**：验证用的第二引擎必须与主分析脚手架**零共享**才算独立。PE 样本的独立性排序：**Wine（真实 x86 执行 + 独立 Win32 实现）> 真机运行 > 第二套自写实现（纯 Python 按反汇编重写模型）≫ 另一个 Unicorn harness**。**Qiling 不是独立引擎——它底层就是 Unicorn**，你的自写 Unicorn harness 的 ABI 理解错了，Qiling 会跟着错（happyVm 复盘：`IO_STATUS_BLOCK` 布局、`HeapReAlloc` 参数序写错时所有"证据"会一起错）。自建 harness 必须当被测对象对待：正负对照 + 已知答案自检 + 独立引擎复验，一个都不省；验证与求解并行（答案出来之前就把 Wine/真机准备好）。ELF 样本同理：WSL 原生运行 > 第二实现 ≫ 另一个 Unicorn。

## 防死循环

oracle 搭不起来（缺 stub/反仿真/地址算不对）→ 按阶梯升，**每级 ≤15 分钟**；禁止反复重试同一层（铁律 6/7，全文见 ghidra-core §1；卡点写台账）。

## References

| 文件 | 何时读 |
|---|---|
| `references/js-antidebug.md` | CTF web/misc 遇到混淆 JS / 浏览器反调试时（混淆分类、反调试四件套中和模板、Node vm 沙箱脱 eval 链） |
| `references/js-env-rebuild.md` | JS 肯跑之后的下一步：补环境最小 stub、webpack 抠模块、Node 本地复现并对照浏览器输出 |
