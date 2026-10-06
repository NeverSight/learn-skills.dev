---
name: traffic-analysis
description: CTF 流量分析与网络取证（pcap / network forensics）：pcap 分诊、DNS/ICMP/TCP 隐信道与隧道重组（covert channel / tunneling）、USB HID 键鼠抓包还原、WPA/TLS 解密、文件与凭据提取。触发：流量/pcap/抓包/Wireshark/tshark/网络取证/流量包/隐蔽信道/隧道。不做二进制逆向——那是 ghidra-static 系；提取出的文件需逆向时回 re-triage。动手前必须先用 skill 工具加载本 skill 全文并遵守其流程；一切观察/结论用 ledger.py 落账。
whenToUse: 拿到 pcap/pcapng 要分析时；DNS 隧道、ICMP/时序/TCP flag 隐信道、USB HID 键盘鼠标抓包、802.11 eapol/WPA 解密、TLS keylog 解密、--export-objects 文件提取、明文凭据收割
---

# Traffic Analysis（场景 6：流量里找信号）

前置：拿到 pcap/pcapng（题目附件，或别的主线提取出的文件）／后继：提取出的二进制 → `~/.dsh/skills/re-triage` 重新分诊；文本/flag 类结论直接交付

> **内容看不懂时，信号在元数据里**：包长、TTL、IPID、时延、TCP flags 的 per-packet 分布画直方图，值落在可打印 ASCII 区间的分布就是信号（TokyoWesterns 2018 方法论，细节 references/tunnels.md §通用检测）。同一路径失败 2 次换工具，单方向 ≤15 分钟（铁律 6，全文见 ghidra-core §1）。

## 路径约定

```bash
TA="$HOME/.dsh/skills/traffic-analysis/scripts"   # 本 skill 脚本（全零依赖，Python 3 stdlib）
# Windows:
TS="$HOME/Desktop/src/tools/wireshark/tshark.exe" # tshark 4.6.8（7z 免安装解包；未加 PATH，用全路径）
EC="$HOME/Desktop/src/tools/wireshark/editcap.exe" # editcap（pcapng→pcap 转换）
# WSL/Linux（apt 安装，PATH 直达）:
# TS="$(command -v tshark)"; EC="$(command -v editcap)"
```

本 skill 不依赖 tshark——`pcap_triage.py` / `conflict_oracle.py` / `decode_engine.py` 自研解析器保底（全 stdlib）；tshark/editcap/scapy/aircrack-ng/hashcat 是否可用以 `python "$SK/doctor.py"` 的 toolchain 节为准（SK 路径见 ghidra-core），缺失按 hint 装或绕。ghidra-core 的 unreferenced_data.py / ledger.py 仅为路由引用，非本 skill 脚本的运行依赖。

## 流程

### 1. 打不开先修

`xxd cap.pcap | head -1` 对 magic bytes（d4c3b2a1/a1b2c3d4=pcap，0a0d0d0a=pcapng）→ 修头/pcapfix/格式转换，配方见 `references/pcap-triage.md` §修复。

### 2. 开局三连（每条 30 秒内）

```bash
python "$TA/pcap_triage.py" cap.pcap      # 零依赖：包数/时间跨度/协议分布/包长直方图/top 会话 + 路由 hint
"$TS" -r cap.pcap -q -z io,phs            # 有 tshark 时交叉验证：协议分层统计
"$TS" -r cap.pcap -q -z conv,ip           # 会话/端点
```

- `pcap_triage.py` **exit 2 = 某协议占比 >60%**，直接跟它打印的路由 hint 走；报告末尾的**每流字段一致性矩阵**打出 ⚠ 重复键冲突时，走 `conflict_oracle.py`（见 §2.5 异常即约束）
- **大 pcap（百万包级）**：信号载体往往藏在包数最少的协议/会话里，按包数倒序找（EHAX 2026 经验）
- pcapng 会被 pcap_triage 拒收：`"$EC" -F pcap in.pcapng out.pcap` 转换后再来

### 2.5 解码阶梯：轴必须交叉，且先算预算

```
明文候选 = OP(字段₁..字段₃) × 顺序(下标/seq/TS/外部置换表) × 打包(半字节 hi|lo, 位序) × 后变换
- OP 至少覆盖 1~3 元 XOR / ADD / SUB → scripts/decode_engine.py 强制全交叉
- 顺序源包含"附件二进制里零引用的置换表"（ghidra-core scripts/unreferenced_data.py）
- 硬门 1（预算）：先算候选总数；算得出却仍剪轴 ⇒ 必须写明理由（铁律 13）
- 硬门 2（覆盖）：任一轴恒为 identity/常量 ⇒ 记为未覆盖，禁止计入"试过"
- 硬门 3（oracle）：无校验手段（hash 常量/重复项一致性/格式校验位）不许全交叉开跑
- 尺寸对齐：载体位数与目标长度严丝合缝 = 信道判对的强证据（非禁令——尺寸巧合可作诱饵）
```

**异常即约束**：

```
同一逻辑键（同 seq / 同下标 / 重传）上字段取值冲突
  ⇒ 该字段大概率不是明文；明文可能是 ≥2 字段的复合函数（xor/add/sub）
  ⇒ 正确函数必须让重复项一致 → 免费过滤器：scripts/conflict_oracle.py
  ⇒ 注意真实抓包重传载荷可合法不同——冲突是假设生成器，不是排除器
  ⇒ 未解决前用 ghidra-core ledger.py anomaly --consequence 落账，禁止当噪声枚举
```

**表先看跨度**：附件有二进制时，32 字节零引用表 → 先查 +0x40/+0x80 是否构成 64/128 项置换，相邻表可能是同一置换的两半或倒序（ghidra-core unreferenced_data.py）。

### 3. 路由表（按分诊发现选路）

| 分诊发现 | 去哪 |
|---|---|
| DNS 占比高 / 查询名 >40 字节 / TXT 记录异常 | `references/tunnels.md` §DNS + `scripts/dnscat2_reassemble.py` |
| ICMP 异常（payload 非标准/长度可疑/时延双峰） | `references/tunnels.md` §ICMP + `scripts/timing_decode.py` |
| TCP flag 组合混乱（FIN+SYN 同现）、同端口包数 %4==0 | `references/tunnels.md` §TCP flags |
| 包内容雷同、间隔只有两档 | `references/tunnels.md` §时序 + `timing_decode.py --mode interval` |
| USB linktype（189/220/288） | `references/usb-hid.md` + `hid_keyboard.py` / `mouse_render.py` |
| 802.11/radiotap、eapol 四次握手 | `references/wifi-tls.md` §WPA |
| TLS 密文 + 附件有 keylog/私钥/coredump | `references/wifi-tls.md` §TLS |
| HTTP/SMB/FTP 明文传文件 | `references/pcap-triage.md` §文件提取 |
| FTP/Telnet/HTTP Basic/NTLM 认证流量 | `references/pcap-triage.md` §凭据 |
| 协议分布全正常、内容全噪声 | 元数据直方图：`timing_decode.py --mode len` / `--mode byte --offset N`（TTL=IP+8，TOS=IP+1；**IPID 是 16 位大端，`--offset` 只读 1 字节 → 高字节 IP+4 恒为 0、低字节 IP+5**），方法论 `references/tunnels.md` §通用检测 |
| 附件 = pcap + 二进制 | 先用 ghidra-core `unreferenced_data.py` 提取零引用材料清单（置换/替换/密钥表），再解 pcap |
| 字段取值在重传/重复键上冲突 | 复合算子分支：`conflict_oracle.py`（不是噪声分支）→ **照抄其末尾 decode_engine 处方**执行；要点：确定函数=抵消项不是无信息；真复合不一定消除冲突（冲突由重生字段携带时真组合继承冲突，走处方的铺轴+oracle 过滤） |

### 4. 证据落账（强制）

每个观察/结论走 ghidra-core `scripts/ledger.py`（`observe`/`conclude`，key 用 pcap 文件名），机制见 ghidra-core `references/evidence-ledger.md`。**提取出的文件先正向验证**（魔数/file 命令/能打开）才算证据；自建解码脚本在支撑结论前用已知答案自检（铁律 10 ②）。

### 5. 时间盒与换路

同一路径失败 2 次 → 换工具（如 hid 手工解析不行就回 tshark 换字段导）；单方向 ≤15 分钟无产出 → 回 §3 路由表选下一行；彻底卡住 `ledger.py stuck` 留痕并问用户。

## 脚本速查

| 脚本 | 一句话 |
|---|---|
| `scripts/pcap_triage.py` | 开局分诊（零依赖）；某协议占比 >60% exit 2 并给路由 hint；报告末尾附 top TCP 流字段一致性矩阵，重复键冲突打 ⚠ |
| `scripts/conflict_oracle.py` | 重复逻辑键上字段冲突报告 + 消除冲突的 1~3 元 xor/add/sub 组合排名（假设生成器，非排除器）；自动剔同键无载荷握手包、退化组合（含逐包唯一宽字段）单列、重生字段冲突诊断、末尾输出可照抄的 decode_engine 处方 |
| `scripts/decode_engine.py` | 字段×算子×顺序×打包多轴全交叉解码；无 --oracle（sha256/前缀/可打印）exit 2 拒绝开跑，超 --max-candidates 同样 exit 2；自动剔除与数据包同键的无载荷包（--keep-empty 关闭） |
| `scripts/hid_keyboard.py` | usbhid.data hex 行 → 还原文本（内置完整 HID 键码表+Shift 映射，--lines 跟踪方向键分行） |
| `scripts/mouse_render.py` | HID 鼠标/数位板位移 → 累加轨迹 → PGM 图（纯 stdlib；输出是 `<out>_mode<N>.pgm` 不是 `<out>.pgm`；`--png` 需 PIL——**venv 里没有 PIL、PATH 上的 python 3.10 才有**，缺了自动降级只出 PGM） |
| `scripts/dnscat2_reassemble.py` | DNS 查询名列表 → 去 9 字节头/去重传 → 重组 payload（缺省只自动猜 **2 级**隧道域名；3 级以上必须显式 `--domain`，否则静默猜错成 `example.com`） |
| `scripts/timing_decode.py` | 时序分档/包长/单字节字段 → bit/字节 → ASCII 渲染 |

## References

| 文件 | 何时读 |
|---|---|
| `references/pcap-triage.md` | pcap 修头/pcapfix、`--export-objects` 文件提取、流重组、明文凭据与 NTLMv2、strings 碰运气 |
| `references/tunnels.md` | DNS（dnscat2/尾部字节/TXT/oracle）、ICMP、TCP flags、时序隐信道配方 + 通用元数据直方图方法论 + pcap+二进制复合题载体判定 tells |
| `references/usb-hid.md` | USB 键盘 8 字节报告、鼠标/数位板画图还原、LED Morse、蓝牙 RFCOMM 重组 |
| `references/wifi-tls.md` | WPA eapol 破解+airdecap 二次分析、TLS 解密三途径、SMB3.1.1 会话密钥推导 |
