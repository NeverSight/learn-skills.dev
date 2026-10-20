---
name: ctf
description: CTF (Capture The Flag) 竞赛全方位解题助手。覆盖 Web 渗透、Pwn 二进制利用、Reverse 逆向、Crypto 密码学、Misc 杂项取证、Blockchain 智能合约、Cloud 云安全等七大方向。当用户参与 CTF 比赛、做 CTF 题目、询问漏洞利用技巧、需要 payload、需要绕过技巧、分析二进制、破解密码学题目、做取证分析、审计智能合约、容器逃逸等场景时，必须使用本 skill。即使用户没有明确说"CTF"，只要涉及漏洞利用、payload 构造、绕过防护、逆向分析、密码学攻击等典型 CTF 技术点，都应触发本 skill。
---

# CTF 解题全能助手

本 skill 是一个分层的 CTF 知识库，覆盖主流 CTF 比赛的所有方向。每个方向下又按漏洞类型/技术点拆分为独立文件，便于按需查阅。

## 工作流程

接到用户题目后，按以下步骤推进：

### 1. 识别题目类型

先从题目描述、附件、URL、源码片段中判断属于哪个方向：

| 信号 | 大概率方向 |
|------|------------|
| HTTP 接口、Web 框架源码、URL、Cookie、参数 | **Web** |
| ELF/PE 二进制、`pwn`/`nc` 提示、glibc、栈/堆 | **Pwn** |
| 给可执行文件让你找 flag、加壳、混淆 | **Reverse** |
| `.py` 加密脚本、`n e c p`、密文、签名 | **Crypto** |
| 图片、流量包 pcap、磁盘镜像、内存 dump | **Misc** |
| Solidity/Vyper 合约、`etherscan`、ABI | **Blockchain** |
| Dockerfile、k8s yaml、云服务配置 | **Cloud** |

### 2. 路由到对应方向的 README

确定方向后，**必须先读对应方向的 `README.md`**，它包含该方向的子路由表、通用方法论、工具清单。不要直接跳到具体漏洞文件，因为 README 会告诉你"先做什么、再做什么"。

```
references/web/README.md          ← Web 方向总览
references/pwn/README.md          ← Pwn 方向总览
references/reverse/README.md      ← Reverse 方向总览
references/crypto/README.md       ← Crypto 方向总览
references/misc/README.md         ← Misc 方向总览
references/blockchain/README.md  ← Blockchain 方向总览
references/cloud/README.md        ← Cloud 方向总览
```

### 3. 在 README 中精确定位漏洞文件

每个 README 都有一张"症状 → 文件"映射表。根据题目具体特征（例如"参数会拼进 SQL"、"模板渲染了用户输入"）定位到具体文件，再读取该文件获取完整攻击链、payload 模板、绕过技巧、最新 CVE 参考。

### 4. 实战解题

读取具体漏洞文件后：

1. **复现**：按文件里的"攻击链"小节一步步操作
2. **绕过**：如果遇到 WAF/过滤/防护，查"绕过技巧"小节
3. **最新技术**：每个文件末尾都有"2024-2026 新技术点"小节，覆盖最新 bypass、CVE、利用链
4. **工具**：需要脚本辅助时，查 `scripts/` 目录或文件里的"工具"小节

### 5. 输出格式

给用户解题时，按这个结构输出：

```
## 题目分析
[判断的题目类型 + 关键信号]

## 漏洞类型
[具体漏洞名 + 对应文件路径]

## 攻击思路
[1. xxx  2. xxx  3. xxx]

## Payload / 利用代码
[可直接使用的 payload，标注变量替换处]

## 绕过技巧（如有）
[WAF/过滤的绕过方法]

## 最新技术点（如有）
[2024-2026 新出现的技巧/CVE]
```

## 通用解题原则

- **先信息收集，再动手**：Web 先看 robots.txt、源码、响应头；Pwn 先 `checksec`、`file`；Reverse 先查壳、看字符串；Crypto 先看加密算法和参数规模。
- **小步快跑**：每一步都验证，不要一次性构造复杂 payload。
- **保留中间产物**：所有 payload、shellcode、解密结果都保存到工作目录，方便回溯。
- **关注版本**：很多利用链高度依赖版本（glibc 2.31 vs 2.34、PHP 7 vs 8、OpenSSL 1.x vs 3.x），先确认版本再选利用方式。
- **合法合规**：本 skill 仅用于 CTF 比赛和授权渗透测试。不要用于未授权的真实攻击。

## 工具脚本

`scripts/` 目录下有辅助脚本，可在解题时直接调用：

- `generate_payloads.py` — 生成各类 payload（SQLi/XSS/命令注入/反序列化等）
- `encoding_toolkit.py` — 编码解码工具箱（Base64/Base32/Hex/URL/Unicode/ROT/JWT 等）
- `crypto_helper.py` — 密码学攻击辅助（RSA 因子分解、AES padding oracle、LCR 等等）

调用方式：`python <ctf-skill-root>/scripts/<script>.py`

## 文件结构总览

```
ctf/
├── SKILL.md                          ← 你现在在读的文件
├── references/
│   ├── web/                          ← Web 渗透
│   │   ├── README.md                 ← Web 子路由
│   │   ├── sqli.md                    ← SQL 注入（含 NoSQL、二次、盲注）
│   │   ├── xss.md                     ← XSS（含 DOM、CSP bypass）
│   │   ├── ssti.md                    ← 模板注入（Jinja2/Twig/Freemarker 等）
│   │   ├── ssrf.md                    ← SSRF（含 cloud metadata、gopher）
│   │   ├── xxe.md                     ← XXE
│   │   ├── csrf.md                    ← CSRF（含 SameSite bypass）
│   │   ├── file-upload.md             ← 文件上传
│   │   ├── file-inclusion.md          ← 文件包含（LFI/RFI/日志投毒）
│   │   ├── deserialization.md         ← 反序列化（PHP/Java/Python/.NET）
│   │   ├── command-injection.md       ← 命令注入（含无字母数字、Windows）
│   │   ├── prototype-pollution.md    ← 原型链污染（Node.js）
│   │   ├── jwt-attacks.md             ← JWT 攻击
│   │   ├── request-smuggling.md       ← HTTP 请求走私
│   │   ├── graphql-attacks.md         ← GraphQL 攻击
│   │   ├── race-conditions.md         ← 竞态条件
│   │   └── logic-vulnerabilities.md  ← 逻辑漏洞
│   ├── pwn/                          ← 二进制利用
│   │   ├── README.md
│   │   ├── stack-overflow.md          ← 栈溢出（含 ROP/ret2libc/canary bypass）
│   │   ├── format-string.md          ← 格式化字符串
│   │   ├── heap-basics.md            ← 堆基础（chunk 结构、bins）
│   │   ├── uaf.md                     ← Use After Free
│   │   ├── tcache-attacks.md          ← Tcache 攻击（glibc 2.26+）
│   │   ├── fastbin-attacks.md        ← Fastbin 攻击
│   │   ├── unsorted-bin-attacks.md   ← Unsorted Bin 攻击
│   │   ├── house-of-series.md        ← House of 系列（含 House of Apple 2/3）
│   │   ├── io-file-attacks.md        ← IO_FILE 利用（glibc 2.34+ 主流）
│   │   ├── modern-protections.md     ← 现代防护绕过（ASLR/PIE/NX/Canary/RELRO/FORTIFY）
│   │   ├── botcake.md               ← Botcake/perthread_struct/largebin/off-by-one
│   │   └── kernel-pwn.md             ← Linux 内核利用
│   ├── reverse/                      ← 逆向工程
│   │   ├── README.md
│   │   ├── static-analysis.md        ← 静态分析（IDA/Ghidra/Binary Ninja）
│   │   ├── dynamic-analysis.md       ← 动态分析（gdb/x64dbg/frida）
│   │   ├── anti-debugging.md         ← 反调试与反反调试
│   │   ├── common-algorithms.md      ← 常见算法识别（TEA/RC4/AES/SM4 等）
│   │   ├── obfuscation.md            ← 反混淆（OLLVM/控制流平坦化/VMP）
│   │   ├── android-reverse.md        ← Android 逆向
│   │   └── wasm-reverse.md           ← WASM 逆向
│   ├── crypto/                       ← 密码学
│   │   ├── README.md
│   │   ├── rsa-attacks.md            ← RSA 攻击全集
│   │   ├── aes-attacks.md            ← AES 攻击（CBC/ECB/CTR/GCM）
│   │   ├── ecc-attacks.md            ← 椭圆曲线攻击
│   │   ├── hash-attacks.md           ← 哈希攻击（长度扩展/碰撞/彩虹表）
│   │   ├── lattice-attacks.md        ← 格攻击（LLL/Coppersmith）
│   │   ├── padding-oracle.md         ← Padding Oracle
│   │   ├── lcg-attacks.md            ← LCG 攻击
│   │   └── modern-symmetric.md      ← 现代对称密码（ChaCha20/SM4）
│   ├── misc/                         ← 杂项
│   │   ├── README.md
│   │   ├── forensics.md              ← 数字取证（内存/磁盘/日志）
│   │   ├── steganography.md          ← 隐写术
│   │   ├── traffic-analysis.md       ← 流量分析
│   │   ├── osint.md                  ← OSINT
│   │   └── encoding.md               ← 编码与解码
│   ├── blockchain/                   ← 区块链安全
│   │   ├── README.md
│   │   ├── reentrancy.md             ← 重入攻击
│   │   ├── integer-overflow.md       ← 整数溢出
│   │   ├── access-control.md         ← 访问控制
│   │   ├── proxy-attacks.md          ← EIP-1967/UUPS 代理攻击
│   │   └── defi-attacks.md           ← DeFi 攻击（闪电贷/MEV/价格操纵）
│   └── cloud/                        ← 云安全
│       ├── README.md
│       ├── container-escape.md       ← 容器逃逸
│       ├── seccomp-bypass.md         ← seccomp 绕过
│       ├── k8s-attacks.md            ← Kubernetes 攻击
│       └── cloud-services.md         ← 云服务攻击（AWS/GCP/Azure metadata）
└── scripts/
    ├── generate_payloads.py
    ├── encoding_toolkit.py
    └── crypto_helper.py
```

## 重要提示

- **不要一次性读完所有文件**。先读 SKILL.md（本文件）→ 读对应方向的 README → 读具体漏洞文件。这样能节省上下文。
- **每个漏洞文件都是自包含的**，包含：原理、利用步骤、payload 模板、绕过技巧、最新技术点、工具推荐、参考链接。
- **遇到不确定的题目**，可以同时读 2-3 个候选文件做对比。
- **最新技术点**：每个文件末尾的"2024-2026 新技术点"小节是本 skill 的核心价值之一，覆盖了最新 bypass、CVE、利用链、新工具。
