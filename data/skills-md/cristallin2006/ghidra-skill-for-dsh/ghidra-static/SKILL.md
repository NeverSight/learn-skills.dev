---
name: ghidra-static
description: 对已建立基本认知的二进制做静态深挖（static analysis / reverse engineering）：反编译（decompile）、xref 追数据流、语义标注、patch 二进制、导出交付。触发：反编译某函数、提取算法/flag 逻辑、打补丁、批量导出伪码、CTF 逆向题主体攻坚。前提是已知样本类型——未知样本先走 re-triage。动手前必须先用 skill 工具加载本 skill 全文并遵守其流程；一切观察/结论用 ledger.py 落账。
whenToUse: 已知样本类型后的静态分析：反编译指定函数、追数据流/调用链、还原算法或校验逻辑、语义化标注、patch 二进制、导出 patched 文件、CTF 逆向题主体攻坚
---

# Ghidra Static（场景 2：深挖它）

前置：未知样本先分诊 → `~/.dsh/skills/re-triage`／后继：交付（报告+产物）；具体命令 → `~/.dsh/skills/ghidra-core`

> **铁律 5（确认即标注）**：搞清一个函数立即改成语义名 + 写 plate comment（地址/作用/依据）。结论必须带地址和可复现命令。（全文见 ghidra-core §1）
>
> **证据台账**：本 skill 全程经 ghidra-core `scripts/ledger.py` 落账——`query` 先查后析、`observe` 观察入账（同区第二次回访被脚本强制要求 `--delta`，答不出 = 断路器）、`conclude` 权威结论写入即锁定、`stuck` 卡点必记。机制见 ghidra-core `references/evidence-ledger.md`。
>
> **铁律 8（读数纪律）**：关键常量用 ghidra-core `scripts/read_views.py` 三视图取唯一权威读数并 `conclude` 锁定；反编译器的 hex/字符串渲染只是视图（会吞前导 0），引用前先 `--expect-hex` 对照；观测矛盾先怀疑读数，不怀疑程序；求逆前先正向跑通流水线。（全文见 ghidra-core §1）
>
> **铁律 9/10（缓冲区归属 + 验证独立性）**：imm-store 拼栈上常量必须按 disp 区间归属变量并 `--expect-len` 核对声明长度；求逆前 MUST 过 ghidra-core `scripts/crypto_sanity.py check`，求逆后 MUST 过 `check-result`，exit 2 = 读数可疑禁止求逆。`conclude` 强制 `--source`/`--independent`——patch 态/自写 harness/单一来源的结论标 ⚠UNVERIFIED，禁止原样交付；宣布「不可满足」前必须先正向复现已知输出。（全文见 ghidra-core §1，patch 态细则见 re-dynamic §4）

## 路径约定

```bash
SK="$HOME/.dsh/skills/ghidra-core/scripts"     # 唯一代码家
# Windows:
RPC="$HOME/Desktop/src/ghidra-bridge/ghidra-rpc-venv/Scripts"  # ghidra-rpc CLI
# WSL/Linux: RPC="$HOME/ghidra-rpc-venv/bin"
```

所有命令形如 `python "$SK/rpc_driver.py" <命令> <binary> [参数]`，参数细节一律见 **ghidra-core §5 能力清单**，本文件不重复。

## Recon（静态锚点）

- `strings <bin> "flag|correct"`：字符串过滤；`imports`/`exports`/`metadata`；`memory-map`
- `functions <bin> --limit N --offset M [--address-min/--address-max]`：分页列函数
- 从可疑字符串/API 的 `xrefs-to` 反查调用者 → 锁定 `main` / check 函数

## Analysis

- `decompile <bin> <函数|0x地址>`：函数伪码；多个目标就连发（daemon 热，~0.2s/条）
- `decompile-all <bin> [--limit N]`：真·全量批量导出
- `search-decompiled <bin> <regex>`：**跨函数正则搜伪码**（找常量/模式首选，比逐个 decompile 快得多）
- `xrefs-to`/`xrefs-from` 追数据流；`basic-blocks` 拿 CFG；`disassemble` 看汇编；`pcode [--high]` 看 P-code
- `find-bytes <bin> "48 8d ?? ??"`：字节模式搜索
- 命中具体模式 → 查 `references/ctf-patterns.md`（已知明文 XOR、.rodata 期望值、比较函数即 oracle、自定义 VM 五步法、魔数表…）
- 反编译结果看不懂 → 换视角（dogbolt.org 多反编译器对比）或直接看 `disassemble` 汇编
- **字段序、结构体偏移、常量比对这类问题，一律看汇编不要看伪码**：反编译器的栈槽命名（`local_XXXX`/`uStack_XXXX`）会给出**错误**的字段序
- 自定义解密 stub 不想脱壳 → `emulate-function`（P-code 仿真，支持寄存器/内存预置）

## Annotate / Patch / 交付

- 写操作即刻生效+自动存盘：`rename-function` / `batch-rename`、`set-comment`（eol/pre/post/plate/repeatable）/ `batch-set-comment`、`set-signature`
- patch：`assemble <bin> 0x401050 "NOP"`（写字节+重建指令一步到位；助记符建议大写）或 `write-bytes`（自动清冲突指令，结果报 `instructions_cleared`）
- 导出 patched 二进制：`export-binary`（Original File 格式，返回 md5 与原文件对比）
- 二进制比对：`version-track`（找变化函数）→ `function-diff`（看具体差异）→ `match-function`（找对应函数）
- **交付纪律**：报告含 范围 / 证据（地址+复现命令）/ 结论 / 产物路径+SHA256。未经证据支撑的否定结论（"无网络能力"）禁止出现。
- **flag 类交付清单（CTF 题按此模板逐项打勾，缺项不许交付）**：
  1. flag 本体 + **验证方式声明**（runtime-oracle / 往返复算 / 仅静态推断——最后一档标 ⚠UNVERIFIED）
  2. **正例**：正确输入被接受（命令+输出）
  3. **负例 ≥1**：近似错值被拒绝（排除"凡输入皆通过"，铁律 11 oracle 成对）
  4. **唯一性**：解空间可枚举时给穷举结论或剩余歧义清单
  5. **产物**：脚本路径 + 中间产物（按 `<sample>.stageN.*` 命名）+ SHA256
  6. **验证引擎声明**：用了几个独立引擎？只有一个 Unicorn 系（含 Qiling）⇒ 独立性不成立（re-dynamic §4⑤）
- **交付前硬门（判真/假 check、"诱饵"判定后必过）**：任何"该分支是假/诱饵/作者逻辑坏了"的结论，交付前必须能指向一次判定性实验（钉值/读状态量/拟合表达式）的记录（ledger anomaly 或 observe），否则按铁律 10④ 不许交付

## 时间盒与退路

- 静态深挖 ~15 分钟无关键路径 → 转动态 → **`re-dynamic`**（直接运行 / 函数级 Oracle / Frida、gdb、angr 入口；工具可用性以 `python "$SK/doctor.py"` 的 toolchain 节为准）
- 同一路径失败 2 次 → 换工具，禁止空转
- daemon 整体挂掉 → ghidra-core §4 的 legacy driver.py 后路

## References

| 文件 | 何时读 |
|---|---|
| `references/ctf-patterns.md` | CTF 模式库与 flag 狩猎启发式（XOR/期望值/oracle/自定义 VM/魔数/S-box 指纹/随机源分类/侧信道/动态工具选型/Cython 扩展元数据） |
| `references/go-binary.md` | triage 报 `lang_hints.go=true` 或发现 Go 指纹（pclntab/buildinfo/garble）时 |
| `references/rust-binary.md` | triage 报 `lang_hints.rust=true` 或发现 Rust 特征串时 |
| `references/cpp-binary.md` | C++ 样本：vtable/RTTI 恢复、this 指针类型化、STL 噪声过滤、MFC 消息映射 |
| `references/classic-crypto.md` | 认出算法后的求逆执行：换表 base64/RC4/TEA 手撕、流水线求逆纪律（识别归 ghidra-core crypto-ident.md） |
| `references/decompiler-pitfalls.md` | 要引用伪码下结论前：L0-L3 信任模型、反编译器失败模式表、五阶段流水线、质量门 6 条（decomp_lint.py 体检先行） |
| （已迁移） | 漏洞定位完成、要写 exp 时 → 转 **`pwn-exploit`** 场景 skill（`pwn-exploit/references/basic-chain.md`：checksec 打法树/ROP/libc 泄露/pwntools 骨架，WSL 工具链） |
