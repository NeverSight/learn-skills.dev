---
name: ohos-dev-distributed-mmi-ram-rom-measurement
description: Use when measuring RAM/ROM impact of OpenHarmony multimodal input (MMI) subsystem changes on DAYU200 (RK3568). Covers ROM measurement via readelf section analysis and file size comparison, RAM measurement via /proc/PID/smaps, smaps_rollup, hidumper --mem, and baseline/current .so swap methodology. Includes code-level theoretical analysis for heap-allocated data structures.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: ram-rom-measurement
  version: 0.2.0
  status: draft
  tags:
    - multimodalinput
    - ram
    - rom
    - performance
    - binary-size
  related-skills:
    - ohos-dev-distributed-mmi-device-test-harness
---

# MMI RAM/ROM 影响度量

衡量 multimodalinput 子系统代码变更前后的 ROM（二进制体积）和 RAM（运行时内存）占用变化。

**前置 skill**: 编译部署、设备连接等基础设施见 `ohos-dev-distributed-mmi-device-test-harness`。

## When to Use

- 提交 PR 前需要量化代码变更对二进制体积的影响
- 需要证明重构/新特性不引入内存膨胀
- 评审要求提供 RAM/ROM 数据

## Safety and Comparability Gates

Replacing system `.so` files, remounting `/` read-write, and rebooting a device are destructive test
operations. Do them only after explicit user approval, keep `.bak` copies of every replaced library,
and restore the device to the requested final state before ending the workflow.

A RAM/ROM conclusion is only comparable when these conditions are recorded:

- baseline and current image/build or `.so` provenance
- exact libraries replaced
- whether the same functional path was executed before both captures
- whether process-level numbers are idle-vs-idle, exercised-vs-exercised, or mixed

If baseline is idle but current is post-exercise, do not present process-level PSS delta as feature
RAM cost. Use it only as context and rely on library PSS plus code-level theoretical analysis.

## 度量三支柱

本 skill 要求从三个互相佐证的维度度量 RAM 影响：

| 维度 | 方法 | 反映什么 | 局限 |
|------|------|---------|------|
| **ROM 段级** | `readelf -S` | 静态映射内存（.text/.rodata/.bss） | 不反映堆分配 |
| **RAM 实测** | smaps + hidumper 真机采集 | 进程实际物理内存 | 受采集条件/编译差异影响 |
| **RAM 理论** | git diff 分析新增容器 + 结构体估算 | 堆分配和运行时数据结构 | 人工估算，依赖正确的结构体大小分析 |

三个维度**必须同时完成**，互相交叉验证。仅做段级估算会遗漏堆分配；仅做实测会受噪声影响；仅做理论分析无法确认实际表现。

## 度量目标库和进程范围

先根据代码变更确定影响面，不要默认只看服务端进程。至少检查改动是否触达以下库：

| 库 | 角色 | RAM 分析范围 |
|----|------|-------------|
| `libmmi-server.z.so` | 服务端主逻辑 | `multimodalinput` 进程 |
| `libmmi-server-common.z.so` | 服务端公共 | `multimodalinput` 进程 |
| `libmmi-util.z.so` | 工具库 | 所有加载该库的目标进程 |
| `libmmi-client.z.so` | 客户端 API/代理 | 触发该 API 的客户端进程，不能用服务端进程 PSS 代表 |

规则：

- ROM 分析应覆盖所有受影响的 libmmi `.so`，包括 `libmmi-client.z.so`。
- RAM 分析必须按实际加载进程归属。`libmmi-client.z.so` 通常不在 `multimodalinput`
  服务端进程中加载；如果客户端 API、proxy、NAPI 或测试二进制路径受影响，需要选择一个会加载
  `libmmi-client.z.so` 的客户端进程执行功能路径并采集该进程的 smaps/hidumper 数据。
- 如果改动只影响服务端内部路径，可以说明 client so 未加载到服务端进程，但仍要用代码 diff、符号
  或段级数据确认 `libmmi-client.z.so` 是否真的无变化或不参与本次 RAM 结论。
- 最终报告要列出“库 → 进程 → 是否执行功能路径 → 是否纳入 RAM 结论”的映射，避免把服务端 PSS
  误当成全量 MMI RAM 成本。

## ROM 度量方法

### 1. 文件级对比（快速）

```bash
BUILD_OUT="code/out/rk3568/multimodalinput/input"
ls -la $BUILD_OUT/libmmi-*.z.so
```

### 2. 段级对比（精确，推荐）

使用 `readelf -S` 分析关键段：

```bash
readelf -S libmmi-server.z.so | grep -E '\.text|\.rodata|\.data|\.bss'
```

| 段 | 含义 | 影响 |
|----|------|------|
| `.text` | 可执行代码 | 直接影响 ROM；映射为 shared clean 影响 RAM PSS |
| `.rodata` | 只读数据（字符串常量等） | 影响 ROM 和 shared clean PSS |
| `.data` | 已初始化全局变量 | 影响 ROM 和 private dirty |
| `.bss` | 零初始化全局变量 | 不影响 ROM；影响 anonymous RAM |
| `.data.rel.ro` | 重定位后只读 | 影响 ROM |

### 3. 基线获取策略

**方案 A：设备 .bak 文件**（推荐）

部署修改版 .so 前，先备份原始 .so：

```bash
$HDC shell "cp /system/lib/libmmi-server.z.so /data/local/tmp/libmmi-server.z.so.bak"
# 部署新 .so...
# 之后拉取基线
$HDC file recv /data/local/tmp/libmmi-server.z.so.bak ./libmmi-server.z.so.bak
```

**方案 B：CI 基线构建**

从 CI 每日构建镜像中提取同版本 .so 作为基线。

## RAM 度量方法

### 1. 找到进程 PID

```bash
$HDC shell "pidof multimodalinput"
```

**注意 PID 稳定性**：multimodalinput 是系统服务，可能被 watchdog 重启导致 PID 变化。在多条 hdc 命令之间 PID 可能不同。**解决方案**：使用命令替换在单次 hdc shell 调用中完成 PID 查找和数据采集：

```bash
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps_rollup"
```

### 2. smaps_rollup（进程级汇总）

```bash
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps_rollup"
```

关键字段：
- **Pss**: 按共享比例分摊后的实际物理内存（最能反映真实占用）
- **Rss**: 驻留物理内存（包含共享页全量）
- **Size**: 虚拟地址空间大小

### 3. smaps per-library PSS（重要）

```bash
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps" > smaps.txt
```

解析脚本和注意事项见 `references/smaps-pss-attribution.md`。关键要求是每个 mapping header 都要重置当前库名，避免把 anonymous PSS 错归到上一个 `.so`。

### 4. hidumper --mem（系统级）

```bash
$HDC shell "hidumper --mem \$(pidof multimodalinput)"
```

输出包含：native heap、.so mmap PSS、total PSS 等分类。

**注意**：hidumper 输出可能很长，通过 hdc shell 可能被截断。可重定向到文件后拉取：

```bash
$HDC shell "hidumper --mem \$(pidof multimodalinput) > /data/local/tmp/hidumper_mem.txt"
$HDC file recv /data/local/tmp/hidumper_mem.txt ./hidumper_mem.txt
```

### 5. RAM 增量归因（必须）

每一个 RAM 增长结论都必须回答“增长来自哪里”。不能只报告 total PSS 或
`multimodalinput` 进程 PSS 差值。至少把增长拆成以下来源并给出证据：

| 来源 | 证据 | 处理要求 |
|------|------|----------|
| 新增/变化的 `.so` 映射 | baseline/current smaps 中的 mapped `.so` 列表和 PSS | 列出每个 `.so` 的基线 PSS、当前 PSS、差值、是否新增加载 |
| libmmi 代码段变化 | `readelf -S` + smaps per-library PSS | 单独列出 libmmi 各库 PSS 增量和对应 section 差异 |
| native heap 增长 | `hidumper --mem` native heap + 代码 diff | 对应到新增容器、对象、缓存、RS 资源或生命周期状态 |
| anonymous/file PSS 增长 | smaps_rollup `Pss_Anon`/`Pss_File` 或 smaps 分类 | 说明是否来自堆、匿名映射、文件映射、测试框架或系统状态 |
| 测试环境/框架噪声 | 新增加载的测试二进制依赖、input-test 框架等 `.so` | 与目标特性分开，不得直接归因给代码变更 |
| 未归因残差 | total delta - 已解释 delta | 单独列出；残差过大时结论只能标记为“不完整归因” |

推荐从 smaps 中按完整路径聚合所有 `.so` PSS，而不是只匹配 `libmmi`；参考脚本见 `references/smaps-pss-attribution.md`。

对 baseline/current 两份结果做 outer join，生成“新增/变化的已加载 `.so`”表：

| 进程 | `.so` 路径 | 基线 PSS(kB) | 当前 PSS(kB) | 差值(kB) | 是否新增加载 | 归因 |
|------|-----------|--------------|--------------|----------|--------------|------|
| multimodalinput | /system/lib/libmmi-server.z.so | X | Y | +/-Z | no | libmmi server 代码段变化 |
| multimodalinput | /system/lib/libxxx.z.so | 0 | Y | +Y | yes | 功能路径触发 / 测试框架 / 环境噪声 |

如果内存增长主要来自加载了新的 `.so`，报告必须列出这些 `.so` 的名称、路径、
PSS 增量和触发原因；不能只写“.so mmap PSS 增长”。如果无法证明某个新加载库由目标
特性触发，应归入“环境/测试框架差异”或“未归因”，不要归入目标特性成本。

### 6. 基线 RAM 获取

**精确方法**：临时恢复 .bak .so → 重启 → 采集 → 恢复修改版 .so

```bash
# 1. 备份当前修改版
$HDC shell "mount -o rw,remount /"    # RK3568 根文件系统在 /，不是 /system
$HDC shell "cp /system/lib/libmmi-server.z.so /data/local/tmp/libmmi-server.z.so.new"
# 对 libmmi-server-common.z.so, libmmi-util.z.so 同样操作

# 2. 恢复基线
$HDC shell "cp /data/local/tmp/libmmi-server.z.so.bak /system/lib/libmmi-server.z.so"
# 对每个库同样恢复 .bak
$HDC shell "reboot"
# 等待重启 (~60s)...

# 3. 采集基线 RAM
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps_rollup"
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps" > smaps_baseline.txt
$HDC shell "hidumper --mem \$(pidof multimodalinput) > /data/local/tmp/hidumper_baseline.txt"

# 4. 恢复修改版
$HDC shell "mount -o rw,remount /"
$HDC shell "cp /data/local/tmp/libmmi-server.z.so.new /system/lib/libmmi-server.z.so"
# 对每个库同样恢复 .new
$HDC shell "reboot"
```

> **RK3568 mount 注意**：根文件系统挂载在 `/`，不是 `/system`。`mount -o rw,remount /system` 会报 "not in /proc/mounts" 错误。正确命令是 `mount -o rw,remount /`。

**估算方法**（不需要重启）：

基于段级分析推算 RAM 变化：
- `.text` + `.rodata` 差值 → 影响 shared clean PSS
- `.bss` 差值 → 影响 anonymous 内存
- `.data` 差值 → 影响 private dirty

当段差值很小（< 1%）且 `.bss` 无变化时，可以直接用估算方法而无需重启。

### 7. 采集前必须执行功能路径

**关键约束**：仅部署 .so 并重启是不够的。如果变更引入了懒分配（lazy allocation）的数据结构，必须在采集前执行完整的功能路径，确保所有运行时状态被实际分配：

```
部署 .so → 重启 → 等待系统稳定 (30s) → 执行功能路径 → 等待稳定 (5s) → 采集
```

功能路径按变更内容定义，不要固定成某一个特性用例。通用模板：

1. 初始化变更依赖的系统状态（如 display、window、device、session、permission）。
2. 调用新增或修改的 public API、IPC、server handler、callback 或事件路径。
3. 触发懒分配和缓存路径（如首次事件、重复事件、边界设备、窗口、显示组）。
4. 覆盖清理路径（解绑、销毁、断连、窗口删除、服务重启前后状态）。
5. 记录实际执行的步骤，并说明哪些受影响库和进程被该路径覆盖。

例如 display group 绑定可以用 `UpdateDisplayInfo`、`UpdateWindowInfo`、
`BindDeviceToDisplayGroupByDisplay` 和事件注入触发；其他特性必须替换成自己的最小完备功能路径。

不执行功能路径的 RAM 采集会**低估**实际内存占用，因为懒分配的容器仍为空。

## 代码理论分析方法（第三支柱）

段级估算只能反映静态映射内存，无法反映堆分配（new/malloc）。对于引入新数据结构的特性变更，**必须**分析代码 diff 中的新增容器和对象。

详细估算规则见 `references/theoretical-ram-estimation.md`。主流程只要求输出：

- 新增容器、对象、缓存和 RS 资源清单。
- 每类对象的典型场景和上界场景估算。
- 分配时机、清理路径和泄漏风险。
- 理论估算与实测 libmmi PSS/native heap/Pss_Anon 的交叉验证结论。

## 输出报告模板

```markdown
## ROM 影响

### 文件级对比

| 库 | 基线(bytes) | 当前(bytes) | 差值 | 比例 |
|----|------------|------------|------|------|
| libmmi-server.z.so | X | Y | +/-Z | +/-N% |
| ... | | | | |
| **合计** | | | | |

### libmmi-server.z.so 段级分析

| 段 | 基线 | 当前 | 差值 |
|----|------|------|------|
| .text | X | Y | +/-Z |
| .rodata | | | |
| .data | | | |
| .bss | | | |

### 影响范围映射

| 库 | 受影响代码路径 | 目标进程 | 是否采集 RAM | 说明 |
|----|--------------|----------|--------------|------|
| libmmi-server.z.so | server handler / event path | multimodalinput | yes/no | |
| libmmi-client.z.so | client API / proxy / NAPI | <client-process-or-test-binary> | yes/no | |

## RAM 影响

### RAM 增长原因归因

#### 进程级增量拆解

| 指标/类别 | 基线(kB) | 当前(kB) | 差值(kB) | 证据来源 | 归因 |
|-----------|----------|----------|----------|----------|------|
| total PSS | X | Y | +/-Z | smaps_rollup / hidumper | 汇总，仅作入口 |
| .so mmap PSS | X | Y | +/-Z | hidumper + smaps `.so` 聚合 | 见“已加载 .so 增量”表 |
| native heap | X | Y | +/-Z | hidumper | 见“heap/anonymous 增量”表 |
| Pss_Anon | X | Y | +/-Z | smaps_rollup | heap/anonymous/运行时状态 |
| Pss_File | X | Y | +/-Z | smaps_rollup | 文件映射或加载库变化 |

#### 已加载 .so 增量

| 进程 | `.so` 路径 | 基线 PSS(kB) | 当前 PSS(kB) | 差值(kB) | 是否新增加载 | 触发路径/归因 |
|------|-----------|--------------|--------------|----------|--------------|---------------|
| multimodalinput | /system/lib/libmmi-server.z.so | X | Y | +/-Z | no | 目标 libmmi 代码变化 |
| <process> | /system/lib/libxxx.z.so | 0 | Y | +Y | yes | 功能路径触发 / 测试框架 / 环境噪声 |

#### libmmi PSS 增量

| 库 | 基线 PSS (kB) | 当前 PSS (kB) | 差值 | section 证据 | 归因 |
|----|-------------|---------------|------|--------------|------|
| libmmi-server.z.so | X | Y | +/-Z | .text/.rodata/.data/.bss 差异 | server 代码路径 |
| libmmi-client.z.so | X | Y | +/-Z | .text/.rodata/.data/.bss 差异 | client API/proxy 路径 |

#### heap/anonymous 增量

| 增长项 | 估算增量 | 实测对应指标 | 代码证据 | 分配/释放路径 | 结论 |
|--------|----------|--------------|----------|---------------|------|
| 新增 map/vector/cache | X KB | native heap / Pss_Anon | 文件:行号或 diff 摘要 | 创建/清理函数 | 目标特性成本 |
| 测试框架对象 | X KB | native heap / Pss_Anon | 测试入口或依赖 | 测试进程生命周期 | 环境差异 |

#### 未归因残差

| total PSS 差值 | 已解释 .so 差值 | 已解释 heap/anon 差值 | 未归因残差 | 处理 |
|----------------|----------------|----------------------|------------|------|
| +X kB | +Y kB | +Z kB | +N kB | N 过大时标记结论不完整，并继续补采 smaps/hidumper/功能路径证据 |

### 实测对比（libmmi 库 PSS）

| 库 | 基线 PSS (kB) | 修改版 PSS (kB) | 差值 | 归因 |
|----|-------------|---------------|------|------|
| libmmi-server.z.so | X | Y | +/-Z | section/code path evidence |
| ... | | | |

### 理论分析

| 场景 | 当前实现 | 后续/完整实现（如适用） |
|------|---------|------------------------|
| 不使用路径 | ~X B | ~X B |
| 典型功能路径 | ~X KB | ~X KB |
| 极端上界 | ~X KB/MB | ~X KB/MB |

### 实测 vs 理论对照

[说明两者是否一致，差异原因]

## 结论

ROM: +/-X bytes (+/-N%)
RAM: 服务端进程 PSS +/-X kB；客户端进程 PSS +/-Y kB（如适用）；理论典型场景 ~Z KB
```

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 用 `ls -l` 文件大小评估 RAM | 文件大小包含 ELF 头、符号表等不映射到内存的部分 | 用 readelf 段级分析 |
| 忽略 .bss 段 | .bss 不占 ROM 但影响 anonymous RAM | 单独检查 .bss |
| 拿 RSS 做进程间对比 | RSS 包含共享页全量，被多次计算 | 用 PSS |
| 对比不同版本系统的 RAM 数据 | 系统库版本差异导致噪声 | 确保只替换目标 .so，系统基线一致 |
| `libmmi-client.z.so` 只看服务端进程 | client so 不在服务端进程加载，RAM 结论缺失 | 选择加载 client so 的客户端进程或测试二进制单独采集 |
| 重启后不执行功能路径就采集 | 懒分配的数据结构未实际分配，RAM 被低估 | 采集前必须执行完整功能路径触发所有状态分配 |
| 只做段级估算不做理论分析 | 段级估算不反映堆分配（new/malloc），遗漏运行时数据结构 | 结合 diff 中的新增容器做理论内存估算 |
| 只做理论分析不做实测 | 理论估算可能遗漏/高估，无法确认实际表现 | 三支柱（段级 + 实测 + 理论）交叉验证 |
| 只报 total PSS 或 .so mmap PSS 增长 | 无法判断增长来自哪个库、堆对象还是测试环境 | 必须列出进程级分类、每个已加载 `.so` 的 PSS 增量、heap/anonymous 增量和未归因残差 |
| `.so mmap PSS` 增长但不列新增 `.so` | 无法判断是否由目标特性加载库导致 | 对 baseline/current 的完整 `.so` 列表做 outer join，列出新增加载和 PSS 变化 |
| 把测试框架额外加载的 `.so` 归因给目标特性 | 夸大特性 RAM 成本 | 未证明由目标功能触发的 `.so` 归入环境/测试框架差异或未归因 |
| smaps 解析器不重置 current_lib | anonymous mapping 的 PSS 被错误归入上一个 libmmi 库，严重高估 | 每个 mapping header 行必须重置 current_lib |
| PID 在多条 hdc 命令间变化 | 读取了不同进程的 smaps | 使用 `$(pidof multimodalinput)` 在单次 shell 调用内完成 |
| `mount -o rw,remount /system` | RK3568 根文件系统在 /，报 "not in /proc/mounts" | 使用 `mount -o rw,remount /` |
| 忽略 Parcelable/RefBase 继承 | 低估含 RefCounter 堆分配的对象大小 | 分析完整继承链，包含 vtable 和 RefCounter |
| 忽略 RS SurfaceNode/BufferQueue | 遗漏最大的单项内存开销（每 group 50-200 KB） | 分析 RS 资源创建路径，区分 nullptr vs 实际创建 |
| 理论分析只看 sizeof 不看堆分配 | 遗漏 std::string 长字符串、vector 元素、map 节点的堆分配 | 分析每个字段的实际内存布局 |
