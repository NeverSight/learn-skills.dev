---
name: re-loader
description: >
  加载器/投放器分析：多层下载、内存加载、模块拼接。
  触发词：加载器、loader、dropper、投放器、内存加载、模块拼接
capabilities: [malware-behavior]
---

# 加载器 / 投放器分析（下载链 / 内存加载 / 模块拼接）

## 何时使用 / 何时不用

- 用：样本是"下载器/投放器"——体积小、动态获取后续载荷、运行时在内存里加载/拼接最终模块
- 用：多层载荷链（下载器 → 解压 → 内存加载 → 最终 RAT/勒索/挖矿）的逐层还原
- 用：反射式加载 / 进程空洞 / 模块拼接类投递技术分析
- 不用：样本本身就是完整载荷（静态可看到全部功能，走 [[re-triage]] / [[re-binary-core]]）
- 不用：只做静态字符串提取（先 [[re-triage]] 初勘，下载器特征不明显时静态先行）
- 注意：动态分析强制前置（[[re-sandbox]]，[[re-analyze/platform-tips]] 最高原则）——下载器必须运行才能观察下载链；网络隔离下分析

## 工具准备

所有工具先验证再使用。本技能是动态分析为主——运行环境与监控工具直接复用下列技能（装法见各技能），本技能额外补两个提取用工具。

### 动态环境（复用，运行强制前置）

- [[re-sandbox]]：VM 快照 + 网络隔离（INetSim 是下载链喂料的关键——模拟 HTTP 接收下载请求并可回放录制响应，坑 1）
- [[re-tracing]]：strace / ltrace / ProcMon / APIMonitor——下载、解压、进程操作的调用级跟踪
- [[re-behavior]]：procmon / sysdig / bpftrace——进程树、注入检测（进程空洞/APC/反射式加载）
- [[re-memdump]]：gcore 默认转储——内存中载荷提取
- 验证: 沙箱快照就绪 + `strace -V` + `gcore --help` 可用

### python3 + pefile —— 内存模块解析/拼接校验（可选但常用）

- python3 装法见 [[re-proto-rev]] 工具准备
- `pip install pefile`
- 验证: `python3 -c "import pefile; print(pefile.__version__)"`

### pe-sieve / hollows_hunter —— Windows 内存进程扫描（可选）

- 来源: GitHub hasherezade/pe-sieve releases 与 hasherezade/hollows_hunter releases，解压即用（Windows）
- 用途: 扫描进程内存，提取反射式加载/进程空洞的 PE 模块（步骤 3 的自动化帮手）
- 验证: `pe-sieve.exe /?` 输出用法

### 载荷脱壳（复用）

- [[re-anti-analysis]]（[[re-packer-id]] / [[re-unpack-simple]] / [[re-unpack-advanced]]）：载荷落地后常加壳，脱壳产物回沙箱复跑验证

## 操作步骤

按顺序执行，每步记录证据（路径 + sha256，见 [[re-triage]]）；每层载荷的"来源"（URL/路径/内存偏移）与 sha256 是报告核心（[[re-ioc]]）。

1. **初始样本识别（下载器 vs 完整载荷）**：
   ```sh
   file loader.bin && sha256sum loader.bin
   ls -la loader.bin                                   # 下载器通常小（几 KB~几百 KB）
   strings -n 6 loader.bin | grep -iE 'http|url|download|temp|\.exe|\.dll' | head -30
   ```
   - 下载器特征：体积小、strings 含 URL/路径、导入表网络与解压 API 多（WinINet/WinHTTP/URLDownloadToFile、CryptAPI、RtlDecompressBuffer）；完整载荷反之（功能全在自身）
   - 哈希先查 VT/社区（[[re-ti]]）确认家族与已有结论，别从零开始
   - 判定为下载器 → 步骤 2；已经是完整载荷 → 转 [[re-binary-core]] 静态或 [[re-malware]] 行为

2. **下载/解压链跟踪**：
   ```sh
   # Linux 沙箱内
   strace -ff -o out -e trace=network,file,process ./loader.bin
   grep -E 'connect|sendto|openat|execve' out.* | head -50
   # Windows 沙箱内: ProcMon 过滤 网络操作/文件写入/进程创建 三个类别
   ```
   - 网络: INetSim 记录样本请求的 URL 与参数（下载目标、User-Agent、分片参数）；断网拿不到后续层 → 把录制响应回放喂料（坑 1）
   - 解压: 观察 RtlDecompressBuffer / 7z / Expand 类调用与临时文件写入路径（%TEMP% 常见）；每层产物 `sha256sum` 存档
   - 链不触发 → 反沙箱延迟/交互检测（坑 3），回 [[re-sandbox]] 环境伪装

3. **内存加载分析（反射式加载 / 进程空洞）**：
   - 反射式加载: VirtualAlloc(RWX) + 手工解析 PE + 手工重定位（无 LoadLibrary/NtMapViewOfSection 调用，全手动）；特征: 大块分配 + 写入 + 执行，无进程创建
   - 进程空洞: NtUnmapViewOfSection（抹掉目标进程镜像）→ NtWriteVirtualMemory（写入恶意镜像）→ SetThreadContext + ResumeThread（从挂起进程切换执行）
   - 观察: [[re-behavior]] 进程树/注入（sysdig `proc.name=loader` 或 ProcMon 进程操作 + 内存写入）；[[re-memdump]] 在窗口期 `gcore -o out <pid>` 提取（时机见坑 2）
   - Windows 自动化: pe-sieve /hollows_hunter 扫描进程提取内存 PE（可选）

4. **模块拼接（多文件合成 / 多段写入）**：
   ```sh
   # 拼接后校验: 内存切片/下载片段重组出的模块
   python3 - <<'EOF'
   import pefile
   pe = pefile.PE('mem_module.bin')      # 解析重组产物
   print(pe.FILE_HEADER.Machine, len(pe.sections), pe.OPTIONAL_HEADER.AddressOfEntryPoint)
   EOF
   ```
   - 多文件合成: 下载日志里的分片参数（range/分块 URL）记录顺序 → 按序拼接；配置与载荷分离存储时先拼配置再拼代码
   - 内存模块落盘: 按转储中的内存布局与节对齐切片重组；pefile 校验失败 → 对齐/偏移修正（RWX 节区映射、重定位表修复）
   - 拼接/修复完成 → 回到步骤 1 初勘（file/hash/熵），继续下一层

5. **提取最终载荷分析**：
   - file/hash/熵（[[re-triage]]）确认最终载荷类型：仍是加载器 → 迭代回步骤 2；是 RAT/勒索/挖矿/间谍 → 转 [[re-malware]]（行为/C2/报告全流程）
   - 加壳 → [[re-anti-analysis]] 脱壳，脱壳产物回沙箱复跑验证（[[re-sandbox]]）再继续
   - 每层 sha256 + 来源（URL/路径/内存偏移）整理进报告（[[re-ioc]] 结构），形成完整投递链

## 跨域联合

- [[re-sandbox]] / [[re-behavior]]：动态环境（强制前置，[[re-analyze/platform-tips]] 最高原则）与注入/进程树检测——本技能由 [[re-malware]] 网关引用，沙箱是工作流第 1 步
- [[re-tracing]]：下载/解压链跟踪（strace / ProcMon），步骤 2
- [[re-memdump]]：内存载荷提取（默认转储优先，[[re-analyze/platform-tips]] 关键经验: 等 OEP 解密后转储），步骤 3
- [[re-anti-analysis]]：载荷加壳处理与反沙箱绕过（[[re-packer-id]] / [[re-unpack-*]]），步骤 5
- [[re-protocol]]：下载协议/C2 交互分析（netcap / proto-rev / crypto-*）
- [[re-ioc]]：每层 hash / URL / 文件路径出 IOC 与报告
- [[re-malware]]：最终载荷行为分析、勒索场景转 [[re-ransomware]]
- [[re-analyze/platform-tips]] 相关分支：默认沙箱、静态优先、直读 vs 转储（OEP 后转储）、Linux/Windows 平台分支（strace vs ProcMon）

## 常见坑与陷阱

- **多层网络下载（断网导致拿不到后续）**：现象——严格断网跑下载器，只见第 1 层行为，后续载荷永远拿不到，链分析中断；原因——载荷全在远程，下载失败使链断在第 1 层；对策——两阶段：先在受控环境（INetSim/fake DNS）识别下载 URL，再把录制字节作为模拟响应回放喂料，逐层获取；每层响应字节与 sha256 存档（步骤 2）
- **内存载荷转储时机**：现象——`gcore` 转储太早（载荷未解密/未映射到可执行状态）或太晚（已执行完毕被清理），提取出的模块残缺/全零；原因——内存载荷只在落地窗口期完整存在；对策——按跟踪日志定位落地点（网络接收 → 写入内存 → 创建线程），在反射入口/线程创建前转储（[[re-analyze/platform-tips]] 关键经验: 等 OEP 解密后 dump）；配合断点暂停进程再转储；多转几次对比
- **反沙箱延迟下载**：现象——样本检测到沙箱特征后 sleep 数十秒~数小时，或等待鼠标/键盘交互才触发下载，短观察窗口只看到"没动静"；原因——反沙箱延迟与交互检测（ATT&CK T1497.003 时间逃逸 / T1497.002 用户活动检测，见 [[re-sandbox]] 时间/交互检测坑）；对策——[[re-sandbox]] 环境伪装（真实时钟、交互模拟、资源充足）+ [[re-behavior]] 拉长观察窗口；必要时 patch 检测点（[[re-anti-analysis]] 域）
- **加密载荷需先解密**：现象——下载到的"载荷"熵 >7.0 全是随机字节，静态分析无从下手；原因——传输/落地时加密（XOR/自定义），loader 运行时才在内存解密；对策——[[re-crypto-id]] / [[re-crypto-keys]] 从 loader 静态还原算法与密钥，或直接 [[re-memdump]] 提取内存中的解密后形态（跳过磁盘形态），而不是对着密文硬分析
- **伪装后缀的自解压加载器**：现象——readelf 报错无法解析；原因——PHDR 被故意填充损坏（干扰解析）；对策——忽略损坏的 PHDR 只看有效 LOAD 段；识别标准模式：入口 → 解压函数 → mmap(RW) → 解压 → mprotect(RX) → 跳转
- **位操作密集代码反编译差**：现象——Hex-Rays 输出不可读；原因——ARM64 位操作密集；对策——切反汇编视图手动分析（位流读取/移位/条件分支场景反编译器不如直接看汇编）
- **自写解压器 bug（carry 语义）**：现象——Python 重写解压器输出错误；原因——refill 路径返回值/进位语义误判；对策——仔细对照汇编核对 carry 语义，用已知明文加断言对比
- **入口偏移不确定**：现象——payload 入口字段含义不明；原因——数据表字段无文档；对策——跟踪 loader 实际跳转目标（`br mmap_base + offset`）确认入口
- **后缀不可信**：现象——按后缀选工具链出错；原因——自解压样本伪装扩展名；对策——`file` 永远是第一步；解析器选容错实现（可处理损坏头）
（来源：reverse-skill field-journal，MIT）
