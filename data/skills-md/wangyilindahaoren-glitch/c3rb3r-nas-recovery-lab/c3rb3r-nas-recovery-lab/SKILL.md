---
name: c3rb3r-nas-recovery-lab
author: wangyilin
version: 1.1.0
created: 2026-11-03
description: 恢复被 C3RB3R / Cerber 系勒索软件（文件后缀 .L0CK3D、勒索信 read-me3.txt）加密的群晖（Synology DSM）、ext4（QNAP 老卷、手工装的 Linux 等）或 Btrfs NAS 上的数据，无需密钥：利用 Btrfs 写时复制留下的旧 extent 逐字节还原原文件，并用 Btrfs 校验和逐块证实；并对已被整体重写、旧 extent 释放的文件，按 C3RB3R 加密模式（尾部 588 字节标记）切出未被加密的明文部分，以及从损坏的 xlsx/docx/zip 中抢救成员、重建 PDF；实在救不回来的，走雕刻（file carving）在块设备上捞回已释放的旧 extent。只要用户提到 NAS / 群晖 / 黑群晖 被勒索、.L0CK3D、read-me3.txt、C3RB3R、Cerber、"文件被加密想恢复"、"没有备份没有快照怎么救"、"文件打不开但想看里面内容"、"文件被删了想找回"、"磁盘里还有残留文件"、"文件雕复"，即使没提 Btrfs 或 extent，也应使用本 skill。覆盖 CoW / NoCOW 判定、子卷快照代数（lastsnap）效应、extent 树精确重组、大文件跨 extent 推测、文件雕刻、统计、导出、验证和报告。也覆盖「雕刻索引按容器 id 反查」这条高收益打法（容器头的 id = Synology Drive 仓库目录名，按 id 列出该文档在盘上的所有历史版本再按 orig_len 筛，实测把 74 个 .osheet 里救回 65 个），以及群晖回收站/@sharesnap 快照里捞勒索前明文原件的做法。Use for ransomware recovery of .L0CK3D files on Synology/Btrfs/ext4 volumes without the key. 也覆盖"文件在 Synology Drive 同步目录下"这一最省时的情形（Drive 的 Git 仓库里留着勒索前明文，可分钟级重建表格数据，见 references/synology-drive.md）。
---

# C3RB3R 勒索后的 NAS 无密钥恢复（Btrfs 主线 + ext4 路线）

> **扩展维护者**：wangyilin ｜ **上游**：[crt106/c3rb3r-btrfs-recovery](https://github.com/crt106/c3rb3r-btrfs-recovery)（MIT，版权声明见 `LICENSE`）
> **版本**：v1.1.0 ｜ **首发日期**：2026-11-03 ｜ **v1.1.0 新增：ext4 恢复路线**（`references/ext4.md`）
> **维护约定**：每轮开工必须先落 `PROGRESS.md`（见 [§0.7 进度记录](#07-进度记录每轮必做)），
> 每轮收尾必须回写本 skill（见 [§14 收尾回写 skill](#14-收尾回写-skill每轮必做这是本-skill-的自我迭代机制)）。

## 这个 skill 解决什么

C3RB3R 用 ChaCha8 加密文件的一部分，追加 588 字节标记后改名为 `*.L0CK3D`。没有密钥就解不开，但有**两条**恢复路线：

**路线 A（旧 extent）**：勒索程序原地改写文件。Btrfs 写时复制会在盘上留下旧数据块，只要旧 extent 仍被文件中未加密的那部分引用，就能逐字节还原。

**路线 B（明文提取）**：勒索程序改写时把整个文件写成了新的 extent。对这类文件，旧 extent 已被释放回收（A 路线失效），但**新 extent 里未被加密的那部分字节仍是原始明文**——只是搬到了新位置。按加密模式切出明文区间即可取出，通常能拿回 59%~88% 的内容；对 xlsx/docx/zip 还能进一步抢救内部成员（工作表 XML 等），对 PDF 能重建出可打开的文件。

两条路线互补：**A 优先，A 失败后走 B**。两条都不行时还有两条兜底——**路线 C** 从备份目录、备份 zip、其它副本里找原件；**路线 D** 直接在块设备上雕刻已释放的旧 extent（见 `references/carving.md`）。

**卷是 ext4 时不一样**：ext4 没有写时复制，路线 A 原理上不成立（勒索程序原地改写即物理覆盖）。改走**路线 E**：明文区 / 找副本 / **jbd2 日志里的旧数据块** / 已删除 inode / 雕刻 —— 完整路线见 `references/ext4.md`。

参考成果（第一个案例）：homes、photo 等 CoW 共享找回 35,445 个文件（229.9GB，经 SHA 核对与解码验证）；NoCOW 共享中 2024 年 6 月快照前写入的部分又找回约 1 万个可精确还原的文件。精确恢复的部分在开启校验和的共享上抽检约 20 万个 4K 块，全部与 Btrfs 校验和一致。

先读 `references/principles.md` 了解原理。遇到环境或设备问题查 `references/compatibility.md`，遇到结果异常查 `references/pitfalls.md`，**动手前必读 `references/plain-extract.md`（明文提取路线）**，表格类文件（`.osheet`）还要读 `references/osheet.md`；**要重建 `.osheet` 原件就读 `references/osheet-rebuild-exact.md`（2026-11-03 实测可做到逐字节精确）**；**目标是被整文件加密、路线 A 判 `no_candidate` 时，读 `references/carve-osheet.md`（数据区强签名雕刻）**；**卷是 ext4 就直接读 `references/ext4.md`（路线 A 不适用，走路线 E）**。

---

## 开工第一步：先介绍自己，再索取参数（**AI 必读，第一次跟用户说话就照这个做**）

用户第一次把这个 skill 交给你时，**第一句话不是开干，是自我介绍 + 索取参数**。

**为什么**：用户此刻最想知道两件事——「这东西到底能不能救我的文件」和「我要给你什么你才能动」。
上来就 `preflight` 会让人一头雾水；上来就报一串术语更糟。
把"能做什么 / 不能做什么 / 需要什么 / 拿到后会怎样"讲清楚，用户才敢把 SSH 密码交给你。

### ① 先讲这个工具能做什么、不能做什么

用**大白话**，不要一上来就说 extent、代数、NoCOW。

**能做的**：

- 把被勒索程序改写过的文件，从磁盘的**旧数据块**里**逐字节还原**（不是解密，**不需要密钥**）
- 把只被加密了一部分的文件，**切出没被加密的那部分明文**——表格能抢救出工作表内容，PDF 能抢救出页面
- 帮你在**备份目录、回收站、快照、别人的目录**里找同一份文件的原件
- 实在不行的，**直接在磁盘的原始数据区扫描**，把还能认出来的文件切出来
- 还原 WPS 的 `.osheet` 表格（国内企业常见格式），并转成通用的 `.xlsx`
- **卷是 ext4 时**：把 **jbd2 文件系统日志**导出来，从日志里找回**被覆盖前的原始字节**（`references/ext4.md`）

**不能做的**（**一定要主动说，不然用户会以为你无所不能**）：

- **不能解密。** 被勒索程序完整加密的文件，没有密钥就是解不开
- 不能凭空造出**已经彻底消失**的数据
- **Btrfs** 卷走主线（群晖 / OMV / Unraid）；**ext4** 卷有另一条路线（`references/ext4.md`）；**ZFS 不适用**
- **ext4 上别承诺"能还原旧版本"**：它没有写时复制，旧内容是**物理覆盖**掉的，
  只能靠日志 / 副本 / 雕刻碰运气 —— 话说在前面，别等到最后才告诉用户

**预期效果**（给个参照，别承诺过头）：

| 文件类型 | 大概能救回多少 |
|---|---|
| 大图片 / 视频（>1MB），共享开了写时复制或有快照 | **大部分能精确还原**（第一个案例 35,445 个文件 / 229.9 GB，校验和逐块证实） |
| 表格、文档、PDF | 多数要靠"找副本"和"抢救明文"，**恢复件要验证能不能打开** |
| 数据库、被整体加密的小文件 | 只能靠磁盘扫描碰运气，**成功率不确定** |
| **ext4 卷**（`0x25` / `0x26` 模式） | **明文区直接拿**（`0x25` 约 88%、`0x26` 尾部全部）；**jbd2 日志命中时能拼回完整原件** |
| **ext4 卷**（`0x24` 整文件加密） | 没有明文区，**只能靠日志 / 副本 / 雕刻**，命中率不确定 |

### ② 明确列出"请你提供 4 项信息"

| # | 要什么 | 例子 | 为什么需要 |
|---|---|---|---|
| 1 | **NAS 的内网地址 + SSH 端口** | `<NAS_IP>`，端口 `22` 或 `4080` | 我要 SSH 上去读块设备 |
| 2 | **SSH 账号 + 密码** | 账号一般是 `admin` | DSM 上读块设备需要 root（用 `sudo` 提权） |
| 3 | **要恢复的目录（绝对路径）** | `/volume1/homes/xxx/某个文件夹` | 决定范围。**我只读盘点，不会乱动别的** |
| 4 | **恢复结果放在哪（本地路径）** | `D:\c3r_recover` 或 `/work` | **不能写回 NAS**，另存一份更安全，也避免二次覆盖 |

> 第 3 项如果用户只说"某个用户的目录"，追问到**绝对路径**为止——
> 后面所有脚本都靠它定位，写错会读到别人的目录。
> 可以先跑一遍只读盘点（列出该目录下的 `.L0CK3D` 数量和分布）给用户确认范围。

### ③ 讲清楚"我拿到信息后会做什么"（让用户有预期）

1. 先落一份 `PROGRESS.md` 记录进度（跨会话、跨天接着干，见 §0.7）
2. **只读**自检：卷是不是 Btrfs、**加密进程还在不在**、卷还剩多少空闲
3. 盘点目标目录里的 `.L0CK3D`，读出每个文件的**原始长度**
4. 按文件状态分流，四条路线里选合适的
5. 导出 → 校验（SHA-256、解码完整性、已知原件对照）
6. **验证通过的才放回原路径**（只新增、不覆盖、不动密文）
7. 出报告：哪些**精确还原**、哪些是**部分明文**、哪些**救不回来**

### ④ 三个必须遵守的沟通纪律

| 纪律 | 原因 |
|---|---|
| **密码别让用户直接贴在对话里** | 会进对话历史和日志。**优先**：让用户自己在终端 SSH 上去跑，我把命令一条条给他；**次选**：设环境变量 `NAS_PASS=...`，我用 `SSH_ASKPASS` 取，**不写进任何文件**（见 `scripts/upload.sh`）。用户坚持要给就收，但要说明只用于本次连接 |
| **不要问这些**：G 值、走哪条路线、密钥、要不要付费 | G 值我自己算、路线我自己判断、**没有密钥**（这是无密钥恢复）。问这些等于把活推回给用户 |
| **信息不全不要瞎猜**：IP、端口、目录路径必须用户给 | 猜错 IP 会连到别人的机器；猜错路径会读写错目录。宁可多问一句 |

### ⑤ 可直接照抄的开场白模板

> 用户已经给了背景信息的话，把方括号里的内容替换掉即可；
> 不知道的项就问，**别填"未知"糊弄过去**。

```
我这边加载了 C3RB3R 无密钥恢复工具箱。先说清楚它能做什么、不能做什么，
再请你补几个信息，我就能开工。

【它能做什么】
· 把被勒索程序改写过的文件，从磁盘的旧数据块里逐字节还原
  —— 不是解密，不需要密钥
· 把只被加密了一部分的文件切出没被加密的明文
  —— 表格能抢救出工作表内容，PDF 能抢救出页面
· 在备份目录、回收站、快照、别人的目录里找同一份文件的原件
· 实在不行的，直接在磁盘原始数据区扫描，把还能认出来的文件切出来
· 还原 WPS 的 .osheet 表格，并转成通用的 .xlsx

【它不能做什么】
· 不能解密 —— 被完整加密的文件，没有密钥就是解不开
· 不能造出已经彻底消失的数据
· **Btrfs** 卷走主线（群晖 / OMV / Unraid）；**ext4** 卷走 `references/ext4.md` 里的 ext4 路线；**ZFS 不适用**

【预期效果】
· 大图片、视频（>1MB），共享开了写时复制或有快照 → 大部分能精确还原
  （实测案例：35,445 个文件 / 229.9 GB，逐块校验和证实）
· 表格、文档、PDF → 多数靠"找副本"和"抢救明文"，恢复件要验证能不能打开
· 数据库、被整体加密的小文件 → 只能靠磁盘扫描碰运气，成功率不确定

【请提供 4 项信息】
1. NAS 的内网地址 + SSH 端口        例：<NAS_IP>，端口 22 或 4080
2. SSH 账号 + 密码                  账号一般是 admin
3. 要恢复的目录（绝对路径）          例：/volume1/homes/xxx/某个文件夹
4. 恢复结果放在哪（本地路径）        例：D:\c3r_recover

关于密码：它会留在对话记录里。两种更稳的做法——
  a) 你在自己终端 SSH 上去跑，我一步一步给命令（推荐）
  b) 设个环境变量 NAS_PASS=xxx，我用 SSH_ASKPASS 取，不写进任何文件

【拿到信息后我会做】
1. 建一份 PROGRESS.md 记进度（跨会话也能接着干）
2. 只读自检：卷是不是 Btrfs、加密进程还在不在、卷还剩多少空闲
3. 盘点该目录里的 .L0CK3D，读出每个文件的原始长度
4. 按文件状态分流，四条路线里选合适的
5. 导出 → 校验（SHA-256、完整性解码、已知原件对照）
6. 验证通过的才放回原路径（只新增、不覆盖、不动密文）
7. 出报告：哪些精确还原、哪些是部分明文、哪些救不回来

全程只读。恢复期间我不会删任何一个 .L0CK3D 文件——
旧数据块靠密文"拽着"才没被回收，删掉就等于销毁原件。
需要清理时我会先给你清单，你确认了才动。
```

### ⑥ 一个必须抢在所有事情前面的动作

**如果发现加密进程还在跑**（`ls -l /proc/*/exe 2>/dev/null | grep deleted` 有可疑项），
**先 `kill -STOP` 冻结它**（不要 kill、不要重启 NAS）。
这是唯一能把文件**全部解开**的窗口，优先级高于本 skill 的所有流程。
详见下一节。

---

## 第 0 步：先判断还有没有"拿密钥"的窗口（只有几小时）

**加密进程可能还在跑。** 如果攻击就发生在几小时内，用 `ls -l /proc/*/exe 2>/dev/null | grep deleted`、`ps` 查有没有可疑进程，例如公开案例里的 `/usr/bin/libgld -n 308`。如果有，**先 `kill -STOP` 冻结它，不要 kill，也不要重启**，然后按公开救援项目从进程内存里取会话主密钥：

- https://github.com/soimy/c3rb3r-rescue
- https://github.com/Benjamin-zlt/c3rb3r-baremetal-rescue

这是唯一能把文件全部解开的路线，比本 skill 的收益大得多。

进程已经退出（重启过，或事发已十几小时）时，内存路线基本无望。第一个案例对 16.7GB RAM、zram、磁盘 swap 做了逐字节 AES 密钥扫描，又拿内存中 194 个 ChaCha 状态对 77.8 万个文件试解，结果都是 0。此时直接进入下面的 Btrfs 路线，不要在内存上反复投入。详见 `references/c3rb3r-format.md`。

## 安全红线（关系到恢复能否成功）

1. **恢复过程中**不删除、不移动到别的卷、不覆盖任何 `.L0CK3D` 文件，不清空回收站。旧 extent 靠密文文件"拽着"才没被释放，删掉密文就等于销毁原件。
   **恢复完成、用户验收确认后**才可以按第 13 步清理密文和多余副本——但**只能清理"已成功恢复的那批文件"的密文**，绝不碰其它尚未恢复的文件的密文。
2. **不做 defrag、balance、`btrfs check --repair`、rescue，不运行来源不明的"解密器"。** defrag 会重写 extent。
   **ext4 上再禁三条**：不跑 `e2fsck`（不带 `-n` 的会清掉释放的块，把还没捞的旧数据彻底销毁）、
   不用 `debugfs -w`、不 resize2fs / tune2fs（详见 `references/ext4.md`）。
3. 恢复期间尽量减少卷上的写入：暂停 NVR 录像、下载、Photos 索引、同步任务。NAS 重启或 DSM 升级本身不会破坏被引用的旧 extent，但会丢掉内存现场，并带来大量写入。等导出完成后再做。
4. 恢复结果写到 **NAS 以外**的盘，绝不回写原目录。
5. 所有 NAS 端操作只读。用本 skill 的 `scripts/c3r_btrfs.py`，它只做查询、读文件和读块设备，临时文件只放在 `/tmp`，用完删除。
6. 汇报要诚实："精确恢复 + 校验和证实"、"推测后解码通过"、"部分明文"、"失败"必须分开写，候选不等于恢复成功。

## 工具

| 文件 | 在哪运行 | 作用 |
|---|---|---|
| `scripts/c3r_btrfs.py` | NAS（root，Python 3.6+ 标准库） | `preflight`（环境自检）、`env`、`gens`、`survey`、`extract`（可用 `--variant prev\|next\|both` 只导一种候选）、`patch`（只导出推测段另一侧候选的数据）、`csum`、`plan` |
| `scripts/mkjob.py` | 本地 | 把上面的脚本连同路径列表打包成一个 stdin 作业，避免命令行过长，也避免在数据卷上落文件 |
| `scripts/c3r_local.py` | 本地（Python 3.8+；可选 Pillow、pillow-heif、ffmpeg） | `extract`（解包 tar 流）、`validate`（SHA、解码、已知原件对照、挑选最佳候选）、`apply-patch` / `revert-patch`（打补丁换候选并可回退）、`report`（统计） |
| `scripts/plain_extract.py` | NAS（root，Python 3.6+ 标准库） | **路线 B**：按加密模式切出明文部分，直接写回 NAS 目录 |
| `scripts/salvage_zip.py` | NAS（root，Python 3.6+ 标准库） | 从损坏的 xlsx/docx/zip 里逐个抢救成员（用中央目录定位 + CRC 校验） |
| `scripts/probe_modes.py` | NAS（root，Python 3.6+ 标准库） | **诊断**：用结构签名反推每种 mode 的真实加密区间 |
| `scripts/carve_scan.py` | NAS（root，Python 3.6+ 标准库） | **路线 D**：定位 Btrfs / **ext4** 卷在块设备上的字节范围（读分区表 + 用超块魔数自验证），生成 foremost 配置与现成命令。`--fs btrfs\|ext4\|auto` |
| `scripts/ext4_probe.py` | NAS（root，Python 3.6+ 标准库） | **ext4 专用**：读 ext4 超块（块大小 / inode 数 / 特性位 / 日志 inode），用 debugfs 列**已删除 inode**，`--dump-journal` 把 **jbd2 日志导出成镜像**。ext4 上最值钱的一步，越早做越好 |
| `scripts/jrn_match.py` | NAS 或本地（Python 3.6+ 标准库） | **ext4 专用**：用密文的**明文区当指纹**在 jbd2 日志里定位旧内容，按「文件偏移 → 日志偏移」映射把**被覆盖的原始字节**取回来拼成候选原件，并做结构校验 |
| `scripts/carve_match.py` | 本地（Python 3.8+） | **路线 D**：把雕刻产物对应回 `.L0CK3D` 原件（在密文明文区上逐字节比对） |
| `scripts/carve_osheet_sig.py` | NAS（root，Python 3.6+ 标准库） | **路线 D 精确版**：在 DATA 区按 `.osheet` 的强签名顺序扫描（签名来源三选一：`--sig-file` 模板 / `--uid` / `--sig-hex`），捞回被整文件加密后已释放的旧原件 |
| `scripts/carve_osheet_identify.py` | NAS（root，Python 3.6+ 标准库） | **认领**：从雕刻日志的命中地址按尾部标记定容器长度 + 严格解析，判定是不是目标文件（`--len` 给勒索标记里的 orig_len，可给多个） |
| `scripts/carve_osheet_near.py` | NAS（root，Python 3.6+ 标准库） | **细看**：对指定逻辑地址逐个打印容器长度、工作表名、分片首行（用来比较同一文件的多个历史版本） |
| `scripts/osheet_parse.py` | 本地或 NAS（Python 3.6+ 标准库） | 解析 WPS OSheet（`.osheet`）容器：头部、条目链、分片 JSON、单元格（宽松版，只能用来列条目） |
| `scripts/osheet_strict.py` | 本地或 NAS（Python 3.6+ 标准库） | **严格**解析 `.osheet`：头部 TLV、条目链、尾部段全部按文法校验，任何不自洽即报错 —— 交付前必须用它复核 |
| `scripts/osheet_fix.py` | NAS（root，Python 3.6+ 标准库） | **OSheet 修复**：密文明文区 + 路线 A 候选 = 修复件，抽 cells 导 CSV，按状态放回原位 |
| `scripts/osheet_rebuild.py` | 本地或 NAS（Python 3.6+ 标准库） | **容器重建**：只重写 X/len 字段、其余字节照抄，头部用正常文件作模板；先用正常文件往返验证。⚠️ 已知会多追加一段尾段、并把附件数据区吞进末条目，**交付件请改用 `osheet_repair.py`** |
| `scripts/osheet_check.py` | 本地或 NAS（Python 3.6+ 标准库） | **按已确认文法做"能不能打开"级校验**：条目链首尾相接、len 字段 == 实际载荷长、0x05 条目的 0x00 前缀与结束字节、附件数据区在链外、尾部段长度。交付前用它复核 |
| `scripts/osheet_repair.py` | 本地或 NAS（Python 3.6+ 标准库） | **容器修复器**：只重写头部与条目链的 X/len，其余字节逐字节保留；修 schema 长度字段、id/ver 写反、附件条目吞数据区、末尾多出的尾段。`--selftest <正常件>` 先做逐字节往返验证 |
| `scripts/osheet_compress.py` | 本地或 NAS（Python 3.6+ 标准库） | **不压缩 → 压缩形式改写**：0x02 条目压成 zlib、名字加 `@C_` 前缀。WPS 可能只认压缩形式（实测能打开的原件全是压缩形式），两种形式各出一份 |
| `scripts/osheet_extract_attach.py` | NAS 或本地（Python 3.6+ 标准库） | **抠出 .osheet 里的附件图片**：附件条目载荷是元数据 JSON，真正的图片在条目链之外的数据区，按图片头尾标记切分、按元数据 size 对号入座，输出成普通图片文件 |
| `scripts/check_payload.py` | NAS 或本地（Python 3.6+ 标准库） | **查条目载荷**：逐条打印分片 JSON 是否合法、行列数、工作表名、有没有真业务数据 |
| `scripts/cleanup_home.py` | NAS（root，Python 3.6+ 标准库） | **收尾清理**：每个文档只留一份恢复件并用原名，删掉重复件和中间产物目录；`.L0CK3D` 一律不动。`--dry` 先看清单 |
| `scripts/osheet_to_xlsx.py` | 本地（Python 3.8+，需 openpyxl） | **合并还原成 xlsx**：把整个 OSheet 容器还原成一个多工作表的 Excel 文件（每个工作表一个标签页，名字/顺序/样式/合并单元格/日期/公式全还原），用户双击就能打开 |
| `scripts/verify_osheet_xlsx.py` | 本地（Python 3.8+，需 openpyxl） | **回读校验**：抽样比对生成的 xlsx 与源 OSheet 容器每一格（日期比序列号、超长整数比文本） |
| `scripts/restore_inplace.py` | NAS（root，Python 3.6+ 标准库） | **放回原位**：把验证通过的原件写回原路径（只新增、不覆盖密文），出台账 |
| `scripts/pdf_rebuild.py` | NAS（root，Python 3.6+ 标准库） | **路线 B 的 PDF 重建**：解 ObjStm、定位或合成 Catalog 与页树、补 `/Parent`、重生成 xref |
| `scripts/pdf_validate.py` | NAS 或本地（Python 3.6+ 标准库） | **PDF 严格校验**：Catalog、xref 偏移、页面内容流是否在位（判断"能不能打开"） |
| `scripts/fix_nas_acl.py` | NAS（root，Python 3.6+ 标准库） | **群晖收尾**：把 root 建的文件/目录改成用户属主并补 Synology ACL（否则 admin 在 File Station 里读不到） |
| `scripts/gitls.py` | 本地或 NAS（纯标准库） | **Synology Drive 取证**：读 Drive office 目录里的 Git 仓库（列出 / 取 blob / 搜内容），无 git 命令也能用 |
| `scripts/gitgrep.py` | 本地或 NAS（纯标准库） | 在 Drive 的所有 Git 对象里找含关键字的 blob（勒索前的 metatext.json 里带文件名，用来定位文档） |
| `scripts/rebuild_from_drive.py` | 本地（Python 3.6+ 标准库） | **Drive 重建**（旧版）：用 Drive 的 Git 明文 + 模板法重建 `.osheet` 容器（分钟级拿到大部分表格数据，**可能缺工作表**） |
| `scripts/rebuild_exact.py` | 本地（Python 3.8+ 标准库） | **Drive 字节级重建**（2026-10-31 新增）：摸清容器格式后**逐字节**重建 `.osheet`，实测 7 个已知原件 **6 个 SHA-256 与原件完全相同**。先 `--selftest` 自检再重建。详见 `references/synology-drive.md` 第 9 节 |
| `scripts/compare_drive.py` | 本地（Python 3.8+） | 校验 Drive 的 `version/text/` 与雕刻原件**逐格**一致（用已知原件证明 Drive 数据可不可信） |
| `scripts/verify_vs_cipher.py` | 本地（Python 3.8+） | **独立对证**：把重建件与密文**未加密区**逐字节比对（mode 0x26 只加密开头 1 MiB），并算出每个条目里多少字节被证实 |
| `scripts/match_drive_all.py` | 本地（Python 3.8+） | **批量匹配**：用「重建长度 == orig_len」把 Drive 仓库对到密文上，带已知对自检 + uid 一致性过滤（长度会撞车，见 `references/batch-osheet-recovery.md`） |
| `scripts/final_pipeline2.py` | 本地（Python 3.8+） | **批量恢复总流水线**：建映射 → Drive 重建 → 与雕刻原件交叉验证 → 与密文明文区对证 → 组装最终集。配套 `export_map.py` / `plan_batch.py` / `rebuild_batch.py` |
| `scripts/carve_id_dump.py` | NAS（root，Python 3.6+ 标准库） | **雕刻索引按 `id` 反查**：从索引里每个命中地址的容器头提取 `id`（= Drive 仓库名），一次读 512 字节即可，成本极低。本轮最有效的一招 |
| `scripts/carve_probe.py` | NAS（root，Python 3.6+ 标准库） | 按 `id` 把盘上该文档的**所有历史版本**读出来，打印真实长度/严格解析/工作表/首行；`--expect` 命中即存盘 |
| `scripts/carve_len_dump.py` | NAS（root，Python 3.6+ 标准库） | **全量**算出雕刻索引里每个容器的真实长度（可后台 nice 19 跑） |
| `scripts/claim_by_len.py` | NAS（root，Python 3.6+ 标准库） | 按长度表**批量认领**并存盘（配合 `carve_len_dump.py` 的结果） |
| `scripts/drv_survey.py` / `drv_survey2.py` | NAS（root，Python 3.6+ 标准库） | 盘点全部 Drive 仓库：commit 历史、每 commit 的条目、**两种形态**（不压缩 / WPS 压缩）的容器长度 |
| `scripts/drv_grep.py` | NAS（root，Python 3.6+ 标准库） | 在全部 Drive git 对象里按关键词搜 blob —— 绕开长度匹配定位"这个文档是哪个仓库" |
| `scripts/build_wps.py` | 本地或 NAS（Python 3.8+ 标准库） | 按 **WPS 原生压缩形态**重建 `.osheet`（schema=3、id 35 字节、ver 41 字节、条目 `@C_`+zlib） |
| `scripts/scan.sh` / `scripts/status.sh` | NAS（root） | 雕刻扫描监督器（**2~4 路并发 + `nice -n 19`**，限并发避免拖垮 NAS）与状态采集（**用 awk 一次遍历求和，不要 cat 大文件**） |
| `scripts/tidy_delivery.py` | NAS 或本地 | **收尾清理**：把恢复目录整理成"每个文档一份 .osheet + 一份 .xlsx"，删掉密文/中间产物/重名副本。**默认预览，`--apply` 才真删，`--drop-cipher` 才删密文** |
| `scripts/recover_one.py` | NAS（root） | **按需恢复单个文件**：复用已有扫描日志直接认领，**不重新扫盘**。原始长度自动从密文尾部 588 字节读 |
| `scripts/read_footers.py` | NAS（root） | **读标记**：一次性读出目录下所有 `.L0CK3D` 的 `mode / pct / enc / orig_len / session marker`（orig_len = `footer[580:588]` u64 LE，是长度认领的基准） |
| `scripts/carve_gen.py` | NAS（root） | **路线 D 通用版**：按文件魔数（zip/png/jpeg/pdf/ole）在 DATA chunk 上扫描，**边扫边匹配目标长度**。命中即算文件长度并查表，日志只有 KB 级。详见 `references/carve-generic.md`。`--dev` / `--range START:END` 支持**非 Btrfs 卷**（ext4 等） |
| `scripts/carve_claim.py` | NAS（root） | **路线 D 通用认领**：按长度认领候选 → 结构校验（zip 能开 / PDF 有 xref / 图片头尾完整）→ 落盘。2026-10-31 实测：2.65TB 单路扫出 455 个唯一候选，按长度精确命中 **151/463** 个目标（xlsx 66 / pdf 34 / docx 32 / zip 19） |
| `scripts/verify_origins.py` | NAS（root） | **路线 C 逐字节证实**：把候选原件与密文的**未加密区**逐字节比对。0x25/0x26 可证实；0x24 只能标"同名同大小" |
| `scripts/xlsx_from_members.py` | 本地（Python 3.8+） | 把抢救回来的 xlsx 内部成员（`xl/worksheets/sheetN.xml` + `sharedStrings.xml` + `workbook.xml`）**还原成 xlsx + csv** |
| `scripts/validate_installed.py` | NAS（root） | **交付前闸门**：逐个校验已装回的原件"双击能不能打开"（zip 成员全可读 + `testzip()` 无错 / PDF 有 Catalog+页面 / PNG 有 IEND / JPEG 有 FFD9 / OLE2 头），并出统计 |
| `scripts/deep_validate.py` | NAS（root） | **深度闸门**（比上一个严格一档）：xlsx/docx 把每个 XML 成员都用 ElementTree 解析一遍并统计工作表数/非空单元格数；PDF 逐页核对 `/Contents` 在不在，统计"**有内容流的页数**"（=0 的就是打开一片空白的空壳）。交付前跑这个 |
| `scripts/pdf_rebuild_plain.py` | NAS 或本地 | 对**已经是明文**的 PDF（尤其雕刻出来的原件）重建 xref / 页树：中间被覆盖几百字节时，文件头尾和对象都完好，只有 `startxref` 对不上，重建后就能打开 |
| `scripts/pdf_xref_repair.py` | NAS 或本地 | **PDF 就地修复（优先于重建）**：原始字节一个不动，只在文件末尾追加新的 `xref/trailer/startxref`（合法的 PDF 增量更新）。2026-11-01 实测 17 个"重建后小一半"的 PDF 靠这个零损失救活 |
| `scripts/plain_index.py` | NAS 或本地 | **全盘明文索引**：一次 `find` 抓全卷 (size, path)，按 (basename, size) 找别的目录/快照/别人 home 里的原件，按 basename 找同名不同版本。⚠️ **不要加 `-xdev`**（Btrfs 子卷 st_dev 不同，会被整片跳过） |
| `scripts/carve_install.py` | NAS（root） | **路线 C+D 统一收尾**：按 **(长度, 文件名)** 分组 → 候选择优（先逐字节证实，再按结构质量）→ 同名同长度多路径时一一分配 → 出装回计划 → 装回（只新增、不覆盖、不动密文） |
| `scripts/ole2_size.py` | NAS（root） | **OLE2(.xls/.doc) 长度反推**（旧版，⚠️ **长度公式少算 512 字节，别用**）：从文件头 + FAT 算出分配长度。正确算法见 `ole2_lib.py` 的 `alloc_len()` |
| `scripts/ole2_lib.py` | NAS（root） | **OLE2 容器解析库**（只读块设备）：FAT / 迷你FAT / 目录项 / 取流（WordDocument、Workbook）+ BIFF 工作表名 + 共享字符串表 + `doc_cjk()` 抽正文 + `text_hits()`/`context()` 关键词定位。**OLE2 没有结尾签名，只能靠它按正文认领** |
| `scripts/ole2_identify.py` | NAS（root） | **OLE2 按正文认领**：两阶段（`screen` 只读头+FAT 算长度筛候选 → `identify` 读流抽正文按关键词判定）。2026-11-02 实测 12 个 .xls/.doc 目标里 **4 个 .doc 正文 100% 认准** |
| `scripts/ole2_install.py` | NAS（root） | **按正文确认过的 OLE2 装回**：三道闸（长度 == orig_len / 正文含关键词 / 写回 SHA 一致）+ 属主 ACL + 只新增不动密文 |
| `scripts/carve_gen_hits.py` | NAS（root） | **路线 D 扫描器 v2**：把**所有**签名命中偏移都记下来（pdf 开头 / `%%EOF` 结尾…），事后离线做集合配对。解决 `carve_gen.py` 的 pending 队列只有 16 槽、PDF 一多就**溢出漏认**的问题（实测：1/7 盘区上新规则命中 97 个目标长度，老规则 0 个）。子命令 `scan` / `match`。2026-11-02 加 `--skip-file <全局chunk号列表>`（断点续扫，换并发数不重扫）和**行缓冲**（原来 1MB 缓冲，进程被 kill 时缓冲区里的命中全丢）。2026-11-03 加 `--dev` / `--range START:END`：**非 Btrfs 卷（ext4 等没有 DATA chunk 概念的）按字节范围整段扫**，日志镜像这类普通文件也能直接喂给它 |
| `scripts/matched_to_carvelog.py` | 本地或 NAS | 把 `carve_gen_hits.py match` 的离线配对结果转成 `carve_claim.py` 认识的候选日志，好复用那条成熟的认领/装回流水线 |
| `scripts/osheet_rebuild_from_drive.py` | 本地 / NAS | **字节级精确重建 `.osheet`**：用 Drive 的 Git 明文重建成与 WPS 原件**逐字节相同**的容器。`--selftest` 校准（必须 SHA-256 相同才继续）、`--survey` 按 `orig_len` 认领哪一版才是原件、`--exclude` 去掉 Drive 侧多出来的 `text/attachment`。2026-11-03 实测：重建件与盘上真实件 SHA-256 相同。详见 `references/osheet-rebuild-exact.md` |
| `scripts/osheet_fix_crlf.py` | 本地 | 修 xlsx 里被 openpyxl 弄丢的**裸 CR**（openpyxl 写 CRLF、XML 解析器又把字面 CRLF 归一化成 LF）。**只修真正失真的那几格**，无脑全转义会把 1 处不符变成 544 处 |
| `scripts/drive_repo_probe.py` | NAS（root） | 解析一个 `.osheet` 的头部（id/ver）与条目，并和指定 Drive 仓库逐条比对（找出"哪几个 blob 变体不同"） |
| `scripts/drive_grep_all.py` | NAS（root） | 在**全部** Drive 仓库的 git 对象里搜关键字（定位文档用）。`gitgrep.py` 只能给单个 git 根目录，这个能一次扫完 200+ 个仓库 |
| `scripts/carve_worker.py` | NAS（root） | 按 DATA chunk 精确划分的多路并行 `.osheet` 签名扫描器（比 `carve_osheet_sig.py` 直接按 chunk 切，支持断点续扫） |
| `scripts/claim_fast.py` | NAS（root） | 快速认领：在「命中地址 + 目标长度」处查容器尾段标记，直接算容器真实长度 |
| `scripts/verify_carved.py` | NAS 或本地 | 雕刻件证实：把雕刻出的原件与密文的**未加密区**逐字节比对，判 `proven` / `name_size_only` |
| `scripts/office_index.py` / `scripts/office_report.py` | NAS（root） | 汇总 Synology Drive office 目录下每个 WPS 文档的可恢复信息（uid / id / 重建长度 / 工作表名 / 分片大小） |
| `scripts/drv_survey2.py` | NAS（root） | 对全部 Drive 仓库的每个 commit，**两种形态**（不压缩 / WPS 压缩）的容器长度一次算全 |
| `scripts/export_map.py` | 本地 | 导出「`.osheet` 密文 → Drive 仓库」映射表，供批量重建用 |
| `scripts/plan_batch.py` | 本地 | 规划一批 `.osheet` 的恢复来源，并做交叉验证（雕刻原件 vs Drive 重建），雕刻优先 |
| `scripts/rebuild_batch.py` | 本地 | 批量 Drive 重建 + 与雕刻原件交叉验证 |
| `scripts/restore_ops.py` | NAS（root） | 把精确恢复的表格放回 NAS 原目录，并补齐属主与 Synology ACL（只新增、不覆盖） |
| `scripts/upload.sh` | 本地（bash） | 把本地文件推到 NAS（DSM 的 SSH 没开 SFTP 子系统，走 `sudo cat >` 管道）。密码从环境变量 `NAS_PASS` 读 |
| `scripts/progress.py` | 本地或 NAS（Python 3.6+ 标准库） | **进度记录**：开工建 `PROGRESS.md`、切阶段、记关键数字、读回当前进度、收尾结项。详见 `references/progress-log.md` |

运行方式和传输细节（Linux、macOS、Windows，sudo 密码，吞吐优化）见 `references/transport.md`。下文用 `RUN <参数>` 表示：

```
python mkjob.py [--list 列表.txt] -- <参数> | 加上 sudo 密码行 | ssh 用户@NAS "sudo -S -p '' sh -s" > 输出文件
```

## 工作流程

### 0. 先分流（30 秒，决定走哪条路）

**别一上来就动手扫盘。先按目标文件的状态选路线：**

```
RUN plan <目标文件> --g G   →  看 status
```

| status / 情况 | 走哪条路 |
|---|---|
| **文件系统是 ext4（不是 Btrfs）** | **路线 A 原理上不成立**（ext4 没有写时复制，勒索程序原地改写即物理覆盖）→ **别跑 `plan`/`gens`/`survey`**，直接读 **`references/ext4.md`**，走 **B → C → jbd2 日志 → 已删 inode → 雕刻** |
| **文件在 Synology Drive 同步目录下** | **先走 Drive 重建**（分钟级拿到大部分表格数据，**可能缺工作表**）→ 读 `references/synology-drive.md`。**别一上来就雕刻。** |
| `exact` / `needs_inference` | **路线 A**：`RUN extract`，本 skill 的主战场 |
| `no_candidate` + mode=`0x24` + 卷空闲 **< 5%** | 旧数据块大概率已被复用，雕刻白干 → 回头走**路线 C**（找备份副本） |
| `no_candidate` + mode=`0x24` + 卷空闲充足 | **路线 D 精确版：数据区强签名雕刻** → 读 `references/carve-osheet.md`（含决策树、校准步骤、禁行清单） |
| `no_candidate` + mode=`0x25`/`0x26` | 先看 `plan` 里是否还有旧 extent 仍被引用；有就仍走路线 A |

⚠️ **被整文件加密的小文件（本 skill 最常见的"救不回"场景）不要再用元数据区反查旧叶子块**——
叶内 item 布局试了三版没钉死。直接扫数据区，快且稳。

⚠️ **ext4 用户不要在 Btrfs 流程上耗时间**：`preflight` 报 `filesystem FAIL`
（"ext4 没有写时复制，本方法不适用"）就是分流信号，直接跳到 `references/ext4.md`。

### 0.5 最优执行顺序（2026-10-31 实战定型，照做能省几小时）

**核心认知：不同路线的耗时差两个数量级，但拿到的东西不一样。分工做，别串行做。**

| 阶段 | 做什么 | 耗时 | 拿到什么 | 什么时候做 |
|---|---|---|---|---|
| ① | **Drive 重建**（`references/synology-drive.md`） | **分钟级** | 表格数据（**可能缺工作表**），容器是手工拼的 | **第一步，立刻做** |
| ② | 用 ① 的结果转 xlsx 并**全量逐格校验** | 分钟级 | 用户当天就能用的 Excel | 紧接 ① |
| ③ | **雕刻**（`references/carve-osheet.md`） | **小时级** | 字节级精确原件 + 图片附件 | 挂后台跑 |
| ③.5 | **扫回收站 / 快照**（`find /volume1 -path '*#recycle*'`、`/volume1/@sharesnap/`） | **分钟级** | 勒索前的**明文原件**（常被忽略的路线 C 金矿） | 随时，做 ① 的同时 |
| ④ | 认领、替换 ① 的件、回收中间产物 | 分钟级 | 最终交付 | ③ 出结果后 |
| ⑤ | **雕刻索引按 `id` 反查**（`scripts/carve_id_dump.py` + `carve_probe.py`） | 分钟级 | 剩下那些"长度对不上"的文档的**精确原件** | ④ 之后补漏 |

**为什么这么排**：① 是分钟级就能让用户拿到可用文件，③ 要几小时只为了两样东西——
**精确原件**（原件是 WPS 原生格式，重建件不是，WPS 可能打不开）和**图片附件**
（两边都没有二进制，只有雕刻有机会挖到）。**先满足用户，再追求完美。**

**⑤ 是 2026-10-31 第三批补上的**：`①~③` 全做完还剩十几个对不上时，别再按长度盲猜——
把雕刻索引里每个容器的 `id`（= Drive 仓库目录名）提出来，按 id 列出该文档在盘上的
**所有历史版本**再按长度筛。实测把 16 个未救回里的 7 个直接变成字节级精确原件。
**但 ⑤ 依赖 ③ 的扫描日志** —— 扫描白跑就没有索引，所以 ③ 还是要跑。

**③ 期间的纪律**（本轮血泪教训）：

- 雕刻是全盘顺序读，**会吃满磁盘带宽**。NAS 是用户的生产设备，不是专用恢复机。
  实测 20 路并发把 RAID1 阵列读到 341 MB/s，NAS 只剩 ~30 MB/s，File Station 全线卡顿。
- **并发不是越多越好**：机械盘阵列上并发过高会磁头互踩。实测单路 258 MB/s、
  4 路聚合 906 MB/s、20 路反而掉到 341 MB/s。**用 2~4 路**。
- DSM 上**没有 `ionice`**，只能用 `nice -n 19` 降 CPU 优先级；IO 优先级只能靠限并发让出来。
- **定位磁盘读大户要用 `/proc/<pid>/io` 的 `read_bytes` 差值**（真实磁盘读），
  不要信 `ps` 的 `%CPU`——D 状态进程的 %CPU 很低但能吃满 IO。
  本轮实测：`syncd` / `fileindexd` / `synoindexd` / `synoindexscand` 读盘全是 **0**，
  **系统索引不是瓶颈**，别去动索引服务。
- 每 60 秒采集一次状态时**不要 `cat` 大文件全文**（state 文件几个 GB 时等于每分钟
  把几个 GB 读一遍，CPU 直接打满）。用 `awk '{last[$1]=$2} END{...}'` 一次遍历求和。

### 0.6 「用户指定某个目录」时的执行序（2026-10-31 某用户 home 实战定型）

用户往往会直接点名一个目录（"恢复 homes/某某 目录里被勒索的文件"）。这时**别从
preflight + gens + survey 那套通用流程从头走**，按下面这个顺序更快、更省事：

```
① 盘点（5 分钟，只读）
   RUN env /volume1          # 卷/NOCOW/lastsnap
   find <目录> -name '*.L0CK3D' | wc -l          # 密文数
   → 密文里绝大部分文件**根本没被加密**（同目录下往往有几千个明文原件）
② 读标记拿 orig_len（1 分钟）
   python3 scripts/read_footers.py <目录>        # → footers.json
   → mode 分布 + orig_len；**size == orig_len+588 全部成立就说明标记自洽**
③ 路线 C：先在"明文池"里找原件（快、零风险）
   明文池 = 同目录下的明文文件 + Backup/ + #recycle/ + @sharesnap 快照
   匹配键 = (文件名, orig_len)   ← 比"大小差 588"更直接
   → 命中后用 scripts/verify_origins.py **逐字节证实**
      （0x25/0x26 用密文未加密区比对；0x24 只能标"同名同大小"）
   → 装回：只新增、不覆盖、不动密文，属主/ACL 跟同目录密文一致
③.5 **全盘明文索引（几分钟，零风险，收益极高 —— 别跳过）**
   find /volume1 -type f -printf '%s\t%p\n' > /tmp/plain_index.tsv   # ⚠️ 千万别加 -xdev
   → 按 (basename, orig_len) 找**别的目录 / 快照 / 别人 home**里的明文原件
   → 按 basename 找**同名不同版本**（原件已被覆盖时的兜底）
   2026-11-01 实测：829514 个文件的索引里找到 23 个目标的明文副本（9 个能逐字节证实），
   另有 16 个目标能用「同名不同版本」顶替（`scripts/plain_index.py`）
④ 路线 B：明文提取（0x25/0x26）
   plain_extract.py → salvage_zip.py → pdf_rebuild.py → xlsx_from_members.py
   ⚠️ 0x25 的容器中央目录落在密文里，只能用密文原件抢救成员
⑤ 路线 D：通用雕刻（0x24 唯一出路，小时级）
   目标清单 = 还没有原件的密文的 (orig_len, ext, 路径)
   scripts/carve_gen.py（3 路）→ scripts/carve_claim.py
   详见 references/carve-generic.md
```

**几条实测结论，直接抄：**

- **`survey` 全是 `no_candidate` 不代表没救**，只说明旧 extent 已释放；
  路线 B/C/D 三条都还通着。
- **`@sharesnap` 快照很可能是"上一代目录结构"**（用户后来整理过），
  按路径对照不上是正常的，只有同名同大小的才算数。
- **home 里的 `Backup/`（PC 备份目录）往往是路线 C 的金矿**：
  2026-10-31 某用户这一轮 142 个原件**全部**来自 `Backup/<PC机器名>/…`。
- **密文的 mtime/ctime 不可信**：当前树里的密文 ctime 全是"当天"（整棵树被重新复制过）。
  判断加密时刻要靠 `gens`（Btrfs 代数）。

### 0.7 进度记录（每轮必做，拿到参数后的第一条命令）

**一次恢复动辄几小时、跨多个会话、夹着几个 GB 的后台任务。**
只把进度记在脑子里或对话里，换个会话就断了——可能把整盘重扫一遍，
也可能把已经删过的密文再删一次。

**所以：拿到用户给的信息后，第一条命令就是落一份 `PROGRESS.md`，之后每完成一个阶段就更新一次。**
（注意顺序：**先跟用户自我介绍并索取参数**——见「开工第一步」；
拿到参数了再落进度表、开工。）
用 `scripts/progress.py`（纯标准库，NAS 端 / 本地端都能跑）：

```bash
P="python3 scripts/progress.py"

# 开工（第一件事）
$P --dir /work init --target "某用户 home 的 624 个密文" \
      --nas "群晖/DSM 7.2.1/14.5TiB RAID1" --g 9324851 \
      --note "先走路线C，同步扫回收站" --next "读 footers 拿 orig_len"

# 每完成一个阶段就切一次
$P --dir /work stage --name "8 路线D 雕刻" --note "单路 nice 19"

# 拿到数字当场记（报告要用的那些）
$P --dir /work metric --name "已装回原件" --value 142
$P --dir /work log "已盘出 624 个密文，mode 分布 484/99/41"

# 换会话 / 接手时先读回来
$P --dir /work status

# 收尾结项
$P --dir /work close --result "救回 459/483，其余 24 个走路线C"
```

**记什么**：目标、环境、G 值、orig_len 长度表在哪、survey 各状态计数、
雕刻扫描进度、认领/装回/校验数字、密文还剩多少。
**不要**记能随时重算的东西（文件总数、目录大小）。

**两条纪律**：

1. `PROGRESS.md` 写在**工作目录**（最好在 NAS 之外），**不要提交到公开仓库**
   （已在 `.gitignore` 里）——它含目标路径、NAS 信息和真实数字。
2. 进度日志里 `log` 出来的**踩坑 / 异常**条目，就是第 14 步回写 skill 的现成素材。

完整规范见 `references/progress-log.md`。

### 1. 自检与可行性检查（几分钟，只读）

**任何设备都先跑 `RUN preflight <某个 .L0CK3D 文件>`。** 它会逐项检查：

- Python 版本、root 权限、是否 btrfs；
- 超级块（扇区大小、校验和算法）；
- dump-tree 工具与 chunk 映射；
- TREE_SEARCH 接口；
- 端到端读取比对（按 extent 映射读块设备，结果与直接读文件一致）；
- 与 `btrfs-map-logical` 的交叉验证；
- 校验和自检、NoCOW 标记。

每一项都会给出 OK、WARN 或 FAIL，失败时附带处理建议。**只要有 FAIL，就按 `references/compatibility.md` 的对应条目处理，处理好之前不要继续。** 那份文档还涵盖：群晖 DSM 6/7、OMV、Unraid 等其他 Btrfs 系统，**ext4 卷怎么走另一条路线**、ZFS 为什么不适用，没有 Python 3 时怎么办，以及拆盘到 Linux 电脑离线处理的通用方案。如果某台设备需要改脚本，改完后必须重新通过该文档最后一节列出的自检。

然后运行 `RUN env /volume1`，记录以下信息：

- 卷是不是 btrfs；块设备（群晖一般是 `/dev/mapper/cachedev_0`）；DATA 剖面（single 或 RAID1 类可以，RAID0/5/6/10 工具会拒绝）。
- **每个共享根目录是否 NoCOW**（`share_roots[].nocow`）。CoW 共享是主战场。
- **每个子卷的 `lastsnap`**。如果 NoCOW 共享的 lastsnap 大于 0，那么这个代数之前写入的文件仍可能恢复。这是 Btrfs 的规则：数据代数不大于 last_snapshot 的 extent，即使 NoCOW 也必须 CoW。
- 文件尾部的会话标记（marker）每个受害者都不同，工具按结构识别尾部，不依赖标记值。

### 2. 确定 G_ATTACK（区分"加密时新写"和"原有"的 extent）

`RUN gens /volume1/homes --sample 3000`，采样要覆盖**多个受影响的共享**，因为不同目录被加密的时间不同。

- 取 `pos0_gen_min`（加密时最早写入的代数）减去一点余量，作为 `--g`。
- 检查 `highest_gen_below_pos0_min`：它应当明显小于 G。第一个案例中，攻击期新写入的代数是 4,842,057–4,842,378，攻击前最近一次正常写入是 4,668,578，中间有一大段空档。如果两者紧挨着，就要人工核查：有的文件开头可能没被加密，或者攻击前不久有正常写入。
- **G 值必须按目录分别确定**：同一次勒索中，不同用户目录被加密的时间可能相差上百万个代数（实测三个目录的 `pos0_gen_min` 分别为 9,224,838 / 9,220,686 / 9,324,867）。用同一个 G 跑三个目录，会导致部分目录的 `no_candidate` 比例高达 100%。对每个要恢复的目录单独跑 `gens`，或至少分批跑。
- G 定错的后果：定得偏大，会把新写的密文 extent 当成"旧数据"读回；定得偏小，会把真正的旧数据当成新写入而丢掉。后面的边界自校验和"旧数据不等于密文"检查能发现这类错误。

### 3. 单文件原理验证（必须先做）

选一个**确知原件**的加密文件，比如从幸存 ZIP、手机或云盘里拿到的同一个文件：

1. 运行 `RUN plan <该文件> --g G`，确认未加密区段共用一个旧 extent，加密区段是新 extent；
2. 运行 `RUN extract <该文件> --g G` 导出它；
3. 本地比对 SHA-256，**完全一致才能继续**。

如果共享开了校验和，再跑 `RUN csum <该文件> --g G`，`bad` 必须为 0，`self_ok` 必须大于 0。

### 4. 全量普查（只读，输出 JSONL.gz）

`RUN survey /volume1/<共享> ... --g G > survey.jsonl.gz`，然后在本地运行 `python c3r_local.py report survey.jsonl.gz --depth 4`。

各状态的含义（详见 `references/principles.md`）：

| 状态 | 含义 | 处理 |
|---|---|---|
| `exact` | 每个被改写的字节都在仍被引用的旧 extent 里 | 直接导出，可用 csum 证实 |
| `needs_inference` | 部分原 extent 已完全被覆盖并释放，只能按相邻 extent 外推位置 | 导出 prev/next 两个候选，靠解码挑选，结果不保证 |
| `partial` | 部分字节无法找回 | 导出并标为部分恢复（缺失处填 0） |
| `inplace_lost` | NoCOW 且晚于快照，被原地覆盖 | 救不回 |
| `no_candidate` | 整文件加密（多为 1MiB 以下的小文件），旧 extent 已释放 | **改走路线 B**（见下）、路线 C 或路线 D |
| `boundary_mismatch` | 自校验失败 | 先查 G 和工具，不要导出 |
| `inline` / `compressed` | 内联小文件，或 Btrfs 透明压缩 | 本工具不处理，见 pitfalls |
| `no_rewrite_found` | 没找到新 extent（多为未知模式且原地覆盖），或文件并未被改写 | 单独人工看 |

要向用户说明规律：CoW 共享里，大于约 1.004MB 的照片和视频几乎都是 `exact`；1MiB 以下的小文件整个被加密，属于 `no_candidate`；数据库文件不论大小都被整个加密。

### 5. 路线 A：导出旧 extent

`RUN extract @LIST --g G` 的输出直接通过管道送给本地 `python c3r_local.py extract - 输出目录`，边传边解包，不落中间 tar 文件。

- 先导最重要的目录（照片、文档），按批次分目录。
- 写入前测一下目标盘的写速度。第一个案例里，一块近满的 SATA SSD 只有不到 1MB/s，换盘后达到 50–70MB/s。
- 导出和验证分开跑：上一批验证的同时导出下一批，验证用多进程。不要串行，否则 NAS 会长时间空等。
- tar 成员名就是 NAS 上的路径去掉 `.L0CK3D`。推测候选会在扩展名前加 `.__prev__`、`.__next__` 后缀，部分恢复的加 `_partial`。
- 推测类文件默认同时导出 `.__prev__` 和 `.__next__` 两份候选，体积接近翻倍。目标盘紧张时改用 `RUN extract @LIST --g G --variant prev` 只导一种；验证失败的文件再跑 `RUN patch @LIST --g G --variant next` 只补导推测段另一侧的数据，本地 `apply-patch` 后重测。流程与效果预期见第 10 节"省空间的候选流程"。

### 6. 路线 B：提取明文部分（`no_candidate` 的主救法）

**这是本 skill 相对原版最重要的补充。** 当 `survey` 显示大量 `no_candidate` 时，不是没救了——那些文件往往只是被整体重写，新 extent 里未加密的部分仍是明文。

**详细步骤见 `references/plain-extract.md`**，务必先读。要点：

- 加密模式在文件尾部 588 字节标记里（偏移 572 起）：`0x24` 整文件加密、`0x25` 分段加密（三等分、每段前 4%，明文占 88%）、`0x26` 前缀加密（只加密开头 1MiB）。已用备份原件逐块比对实证验证。
- 把密文区填 0、明文区填原字节，**保持原文件偏移**，这样 zip/pdf 的内部结构仍然自洽，可以继续抢救成员。
- 想知道某个 mode 的真实区间而标记里没写明时，用 `scripts/probe_modes.py` 反推（用 zip 中央目录、PDF `%%EOF`、JPEG `FFD9` 作结构探针）。
- 抢救出来的 xlsx 工作表 XML 往往包含完整业务数据（实测一个 2810 行、53390 单元格的工作表完整可读）。

### 6.5 容器型表格的修复（WPS OSheet 等）

`.osheet`（WPS OSheet）是国内企业常见格式，zipfile/openpyxl 都读不了，
"抢救出来的文件双击打不开""显示无效文件格式"多半就卡在这里。**详细步骤见 `references/osheet.md`**，务必先读。要点：

- **合并修法**：`修复件 = 密文的明文区间（逐字节原文） + 路线 A 候选的被加密区间（推测值）`。
  明文区因此是精确的 —— `scripts/osheet_fix.py` 直接实现。
- **再重建一次容器**：合并只保证内容对，长度字段仍可能错（实测头部 `schema` 字段长度被推成 2，
  正常是 3，整体错位一字节 → WPS 直接报"无效文件格式"）。
  用 `scripts/osheet_repair.py` 只重写 X/len 字段（其余字节逐字节保留），
  再用 `scripts/osheet_check.py` 严格复核。**修复器要先拿正常件往返验证（输出应逐字节相同）。**
  ⚠️ 旧的 `osheet_rebuild.py` 已知会多追加一段尾段、并把附件数据区吞进末条目，**不要直接拿它出交付件**。
- **容器打不开的四个坑**（2026-10-31 实测，7 个文件全中）：末尾多出 11 字节尾段、
  末条目 X 吞掉附件数据区、`schema` 长度被推成 2、条目链错位。
  另加两种：`id`/`ver` 值写反、文件里嵌了第二份条目链。详见 `references/osheet.md` 第 11 节。
- 容器结构：magic `78 00 00 00`，头部 TLV，条目链 `[u32 X][u8 tag][name\0][u32 len][数据]`
  （tag=0x05 是 zlib，tag=0x02 是原始数据），X = 到下一个条目的距离；尾部还有一段 `end` 标记。
  压缩数据的真实边界用 **zlib 自终止**确定，别信文件里的 len 字段。
- 单元格在分片 JSON 的 `cells[行][列]` 里；`text/index` 给出分片清单。
- **一个 `text/sh_N` 分片 = 一个工作表**（不是行分片）。所以"每个分片导一个 CSV"
  会把一个表格炸成十几个文件、工作表名字和顺序全丢 —— **那不是交付物**。
  **正式交付物是一个 xlsx**：用 `scripts/osheet_to_xlsx.py` 把整个容器还原成
  一个工作簿，每个工作表一个标签页（名字/顺序取自 `text/index`），
  字体/底色/边框/数字格式/对齐/合并单元格/行高列宽按容器里的 `text/style` 样式表还原，
  日期换真日期、公式保留并自动重算，表头加粗冻结 + 自动筛选。
  细节和坑见 `references/osheet.md` 第 9 节。
- **验证四关**：明文区逐字节一致 → 容器结构严格复核通过 → 分片全解 → 抽样有真业务数据。
  宽松解析器**不能**用来判断文件好坏（坏文件在宽松解析下照样"通过"）。
- **⚠️ "打不开"先分清是哪一类（2026-10-31 实战教训）**：
  - **网络类报错**（"无法执行此操作，可能是因为网络连接不稳定或系统正忙"、
    "网络路径找不到"）= WPS 根本没拿到文件内容，**不是格式错**。
    `.osheet` 要在**群晖上用 WPS 打开**（File Station 右键 → 用 WPS 打开）；
    在电脑上双击它，WPS 可能走云端转换，网络一抖就报这个。
    → 遇到这类报错，先在群晖上试，别急着改文件。
  - **格式类报错**（"无效文件格式"、"文件已损坏"）才是容器问题，
    按上面那四个坑查。
- **交付形态（用户确认的口径，2026-10-31）**：
  - `.osheet` 是**群晖上 WPS 用的格式**，`.xlsx` 是 **Excel/WPS 通用格式**
    （拷到电脑上双击就开）。两者是同一批数据的两份产物。
  - **表格类的正式交付物是"一个 xlsx"**（多工作表、多标签页）。
    如果某个 `.osheet` 的容器实在修不好、怎么试都打不开，
    **交 xlsx 就行，用户可以自己在群晖里把它手动转成在线表格，不影响使用**。
    不要为了一个打不开的 `.osheet` 死磕、也不要因此不敢交 xlsx。
  - `.osheet` 里的**附件（图片等）不在 xlsx 里**，用
    `scripts/osheet_extract_attach.py` 把它们抠成普通图片另存一个目录再删 `.osheet`，
    否则附件数据会随文件一起丢。
- **群晖上还要补 ACL**：root 写的文件没有 Synology ACL（`synoacltool -get` 报 "It's Linux mode"），
  admin 在 File Station 里读不到，用户会以为文件坏了。
  `synoacltool -copy <原始文件> <目标文件>`，且**必须放在 chmod 之后**（chmod 会把 ACL 抹掉）。
  两个细节：对自己新建的文件要**无条件 chown**（home 默认 ACL 会让"已有 ACL"的判断漏掉 chown）；
  有些 home 的默认 ACL **不带 administrators 条目**，admin 连读都读不到，
  要 `synoacltool -add <文件> "group:administrators:allow:rwxpdDaARWc--:----"`。

### 6.6 `.osheet` 的**字节级精确重建**（2026-11-03 新增，最省时的一招）

**当目标是 `.osheet` 且 `plan` 判 `no_candidate` 时，先试这条路**——不用雕刻、不用扫盘，
**分钟级**就能拿到与原件**逐字节相同**的容器。

**原理**：Synology Drive 把每个 WPS 文档存成独立 Git 仓库，`.git/objects` 里的 blob
（无扩展名）**没被勒索程序加密**，就是勒索前的明文。把这些 blob 按 WPS 的容器格式重新拼起来，
能拼出与原件**逐字节相同**的文件（2026-11-03 用回收站里的真实文件校准，SHA-256 完全相同）。

```bash
# ① 校准（必须先做）：重建结果要与一个**真实存在的** .osheet SHA-256 相同
python3 scripts/osheet_rebuild_from_drive.py --selftest <真实件> <office目录>

# ② 用勒索标记里的 orig_len 认领「到底是哪一版」
python3 scripts/osheet_rebuild_from_drive.py --survey <office目录> \
        --template <一个已知正常的 .osheet>

# ③ 重建（长度对不上 orig_len 就是重建错了，别往下走）
python3 scripts/osheet_rebuild_from_drive.py --repo <office目录> --ver <commit> \
        --template <模板> --out <输出.osheet> --expect-len 839115 \
        [--exclude text/attachment]
```

**关键细节**（写错过一遍，详见 `references/osheet-rebuild-exact.md`）：

- 压缩参数是 **zlib level 9**，Python 的 `zlib.compress(data, 9)` 与 WPS 输出**逐字节相同**；
- 每个压缩条目后面**还有一个 0x00 结束符**（要算进条目的 X 字段）；
- 头部 schema 后面是 **3 个** 0x00 填充，不是 1 个；
- `metatext` 条目后面**还跟一段未压缩副本**，且末尾**多一个** 0x00；
- Drive 仓库里的 `text/attachment` 条目**本地容器可能没有**，带上会多 1200 多字节 → `--exclude`；
- **`orig_len` 长度匹配前，先用同目录「密文 + 同名明文副本」验一下这个不变量**
  （2026-11-03 对照实验：另一个文件 `orig_len` 与明文副本**分毫不差**，所以 +7 才是真的内容差异）；
- 重建件的 `id`/`ver` 字段长度固定、**不影响总长度**，但影响是否字节级精确：
  内容来自哪个 commit 就配哪个 commit 的 ver。

**转 xlsx 时注意一个坑**：`openpyxl` 会把 `\n` 写成 CRLF，XML 解析器又把字面 CRLF 归一化成 LF，
源里**裸 `\r` 分隔**的格子会失真（2026-11-03 实测 80718 格里差 1 格）。
用 `scripts/osheet_fix_crlf.py` 只修真正失真的那几格，之后全量逐格校验应 0 不符。

### 7. 找其他副本（路线 C）

`no_candidate` 且路线 B 也拿不到内容时，按下面的顺序找：

1. **备份目录**：被勒索的用户往往自己做过备份。检查 `备份/`、`Backup/`、同步盘目录、NAS 快照、以及**备份 zip**——勒索程序改名前的快照 zip 里可能存着未加密的原件（用一个同名同大小的原件和密文逐字节比对即可确认）。
2. **同名文件换名**：很多目录被整体改名前，别的目录里还有同名的未加密文件。
3. **其它用户目录**：员工目录互有备份。
4. **手机 / 云盘 / 邮件 / 微信电脑端**：按路径、文件名、大小、月份生成清单帮用户找。
5. **应用级副本**：`@eaDir` 缩略图与转码视频可作低清保底。

### 8. 路线 D：雕刻已释放的旧 extent（最后手段）

A、B、C 都失败后再考虑：绕过文件系统，直接在块设备上按文件头尾特征扫描，
把还能认出来的文件切出来。它只能救**旧 extent 已释放、但物理块还没被复用**的那部分文件。

**详细步骤见 `references/carving.md`**，务必先读。要点：

- 群晖的 `/dev/mapper/cachedev_0` 上数据卷不在 0 偏移。先用 `scripts/carve_scan.py` 读分区表，并用 Btrfs 超块魔数**自验证**出数据卷的起点偏移（不靠猜）。
- DSM 上默认没有 foremost / PhotoRec：用 entware 装，或把设备流导出到本机再雕。
- DSM 的 `dd` 是 busybox，**不支持 `iflag=skip_bytes`**，只能按块取整；`carve_scan.py` 会打印现成命令。
- 只扫需要的文件类型。雕刻会狂读盘，**不要和导出同时跑**；输出目录必须在 NAS 之外。
- 切出来的文件没有路径。用 `python carve_match.py <雕刻输出目录> --enc <加密文件根目录>` 对应回原件：它在密文文件的**明文区**上逐字节比对，`confirmed` 是证实，`size_only`（整文件加密无法比对）只是弱候选，必须人工确认。
- **卷空闲空间 < 5% 时基本白干**——旧 extent 大概率已被复用。这时把精力放回路线 C。

#### 8.1 路线 D 的精确版：按容器强签名在数据区扫（2026-10-31 实测救回原件）

**当目标是被整文件加密（0x24）、`plan` 判 `no_candidate` 的小文件时，
不要在元数据区硬啃叶子块布局——直接拿文件容器自己的强签名去扫数据区。**

`.osheet`（现代版 WPS，`schema` 长度 = 3）的头部 39 字节完全固定，
其中 id 前 5 字节就是**作者 uid**，等于给每个用户一份专属签名，误报几乎为零：

```
78 00 00 00 | 12 "schema\0" 03 00 00 00 | 00 00 00 | 08 "enc\0" 00 | 02 "id\0" 23 00 00 00 | "<uid>_"
```

```bash
# 扫描（签名来源三选一：模板文件 / uid / 原始 hex）
python3 carve_osheet_sig.py /tmp/carve_out --uid 1042 1900000000000 2180000000000 > /tmp/carve_s1.log

# 批量认领（--len 取勒索标记里的 orig_len；日志一律用 --log 指定）
python3 carve_osheet_identify.py --len 48250 19559 \
        --label 客服上班表-最新 保税区退款订单 --log /tmp/carve_s*.log
```

多开几个进程分窗口并行（单流 225 MB/s → 6 路聚合 534 MB/s，2.63 TiB 约 4 小时）。

> ⚠️ **并发路数按盘的类型定，别照抄 6 路**（2026-10-31 实测）：
> RAID1 机械盘阵列上，**单路 258 MB/s、4 路聚合 906 MB/s、20 路反而掉到 341 MB/s**——
> 并发过高会磁头互踩。**用 2~4 路**，并给 NAS 日常访问留出带宽。
> DSM 无 `ionice`，只能 `nice -n 19`；IO 优先级靠限并发让出来。
> 另：`carve_worker.py` 的步进必须严格为正（`step = (want - OVERLAP) if want > OVERLAP else want`），
> 否则 chunk 末尾会陷入死循环、把 state 文件撑到几个 GB。详见 `references/pitfalls.md`。

**详细步骤、决策树、尾部格式、多历史版本比对方法、本轮走过的 6 条弯路（禁行清单）、
以及顺带确认的 Btrfs 事实，见 `references/carve-osheet.md`（务必先读）。**

#### 8.3 成批恢复几十个 `.osheet`（2026-10-31 晚定型）

单文件试水摸清容器格式后，**先盘点再批量**：全盘 8716 个密文里容器型文档只有 477 个
（`.osheet` 74 / `.xlsx` 306 / `.docx` 87），别被总数吓退。
用「雕刻索引认领」+「Drive 字节级重建」两条路**互为交叉验证**，
一次跑完 74 个 `.osheet` 救回 58 个（78%）。

**完整操作手册见 `references/batch-osheet-recovery.md`（务必先读）**，含：
长度反推公式、**长度匹配会撞车**的两种防线、`metatext` 长短两版、
交叉验证与密文明文区对证、Drive 同步覆盖的处置、Windows→NAS 传文件的坑。

#### 8.2 扫描一次，之后**按需恢复任意文件**（不用重新扫）

**这是雕刻路线最大的价值：扫一遍 = 建成一份"全盘容器位置索引"，之后想恢复哪个分分钟。**

两阶段是分开的：

| 阶段 | 干什么 | 成本 | 产出 |
|---|---|---|---|
| 扫描 | 全盘找 `.osheet` 强签名，把命中地址写进 `logs/w*.log` | **小时级**（全盘顺序读） | **日志 = 一份索引** |
| 认领 | 从日志取地址 → 映射物理地址 → 读块设备几百字节 → 按尾部标记定长度 → 严格解析 | **秒级**（随机读） | 那个 `.osheet` 文件 |

所以：**扫描跑完之后，日志长期有效**，以后指定任何目标都能直接认领，不用重扫。

```bash
# 一键按需恢复：原始长度直接从密文尾部 588 字节的 footer[580:588] 读，不用翻勒索信
python3 recover_one.py "/volume1/homes/xxx/某文件.osheet.L0CK3D" --xlsx
```

已实测：扫到 23.6% 时，直接从已有日志认领出了此前没打算恢复的
`2019年产品采购记录.osheet`（177020 字节，工作表「刘老板」「出纳」），**全程没重新扫盘**。

**三个必须知道的限制**：

1. **只覆盖扫描签名匹配的类型**。当前签名只认 `.osheet`（WPS 表格容器），
   docx/xlsx/pdf/zip 等其它类型**不在这次扫描范围内**，要另外用通用雕刻。
2. **有时效性**。旧 extent 可能被后来写入的数据覆盖——**扫完越早认领越安全**，
   拖很久再回头认，命中率会下降。
3. **未扫到的部分捞不到**。扫描没覆盖的区间，日志里就没有地址。

**所以最优策略是：把扫描跑完，拿到全量索引，然后随时按需恢复。**

#### 8.4 路线 D 的标准收尾流程（2026-11-01 定型，照抄）

扫描出候选之后，**别自己写认领/装回脚本**，用 `scripts/carve_install.py` 一条龙跑完：

```bash
# ① 认领（产出 <carve目录>/_认领结果.json，含每个物理副本的 start 偏移）
nice -n 19 python3 scripts/carve_claim.py <扫描日志目录> <targets.tsv> <carve目录>

# ② 建全盘明文索引（路线 C 的来源，⚠️ 千万不能加 -xdev）
find /volume1 -type f -printf '%s\t%p\n' > /tmp/plain_index.tsv

# ③ 出装回计划（路线C+D 合并择优）
python3 scripts/carve_install.py plan \
    --home /volume1/homes/<用户> --targets <targets.tsv> \
    --index /tmp/plain_index.tsv --claim <carve目录>/_认领结果.json \
    --out-plan /tmp/install_plan.tsv

# ④ 装回（只新增、不覆盖、不动密文）+ 属主/ACL + SHA 复核
#    ⚠️ install 收的是 **JSON** 计划文件（plan 步会同时写 xxx.tsv 和 xxx.tsv.json），
#    传成 TSV 会直接 JSONDecodeError 退出、装回静默不执行。
python3 scripts/carve_install.py install --plan /tmp/install_plan.tsv.json --log /tmp/install.log

# ⑤ 结构校验（"双击能不能打开"）
python3 scripts/validate_installed.py <pairs.tsv> <out.json>
#    更严的一档（查"打开是不是空白"、xlsx 逐个 XML 解析）
python3 scripts/deep_validate.py <pairs.tsv> <out.json>
```

> **装回后必须核对三件事**：① `install_*.log` 里 `^OK` 条数 = 预期条数；
> ② 深度校验里没有"装回件不存在"；③ 目标路径真的有文件。
> 后台脚本没有 `set -e` 时，装回那步失败会被后面的步骤掩盖（2026-11-01 踩过：图片装回第一次全空跑）。

> **⚠️ 0x26 文件别用路线 B 的"明文片段"当候选（2026-11-02 踩过）**：
> 片段在明文区与密文**逐字节一致** → 被判 `proven` → 排序排在所有雕刻件之前 →
> 循环遇到第一个 `proven` 就 break，**完整的雕刻原件根本没被考虑**；
> 而片段的文件头是 8 个 0（加密区被填 0），装回去**根本打不开**。
> **做法**：① `plan` 时把 `--index` 指向空文件（排除路线 C/B 副本），只用雕刻件；
> ② 装回前逐条筛 `严格校验通过`（含"修复后严格校验通过"），不合格的不装。
> 2026-11-02 实测：首轮计划 100 条里 42 条是片段，改完装回 92 个、深度校验 92/92、0 个片段。

> **⚠️ 大批量雕刻/计划一律放后台跑，并先看内存（2026-11-02 踩过）**：
> DSM 的 `/tmp` 是 **tmpfs（占内存）**，上一轮残留的中间产物能有十几 GB。
> `plan` 跑到一半被**内核 OOM killer 杀掉**时，**stdout 缓冲全丢**，
> 表现为"没输出、没报错、计划文件也没生成"——很容易误判成脚本没跑。
> 开工前：`df -h /tmp` + `free -m`；tmpfs 满了就清上一轮的中间产物；
> `plan`/`claim` 这种十几分钟的活儿用 `setsid nohup` 挂后台，单独打 `rc=$?`。

**这套流程里几个必须理解的点：**

1. **分组键是 (原始长度, 文件名)，不是长度。** 同名同长 = 同一份文档的副本；
   同长不同名 = 完全不同的文档，长度撞车时不要凭长度乱认。
2. **候选优先级**：能与密文**未加密区逐字节一致**（`proven`）的排第一，
   其余按结构质量排（zip 成员数 / PDF 页数与 xref 吻合度 / 图片像素数）。
3. **同一目标往往有多份物理副本**（2026-11-01 实测 240 份 / 63 个目标），
   要**逐份雕出来评质**，别只取第一份 —— 第一份可能是"碎片拼接"的坏副本。
4. **PDF 严格校验不过时用 `pdf_xref_repair.py` 就地修复**，
   不要用 `pdf_rebuild` 全量重建（重建会丢掉一半内容）。
5. **JPEG 允许 FFD9 之后有残留字节**，完整性检查别写 `endswith`。
6. **全盘明文索引是路线 C 的放大器**：同一个共享往往同时有「快照」「团队空间」
   「别人的 home」几份拷贝，只要有一份没被加密就是现成原件。
   2026-11-01 实测 829514 个文件的索引里，按 (basename, size) 找到 23 个目标有明文副本
   （9 个能逐字节证实），另有 16 个目标能用「同名不同版本」顶替。

### 8.5 ext4：没有 CoW 也能救（路线 E）

**卷是 ext4（QNAP 老卷、群晖老卷、手工装的 Linux）时，本 skill 的主线不适用**：
ext4 没有写时复制，勒索程序原地改写就把旧内容物理覆盖了 ——
这不是工具问题，是文件系统原理决定的。

但 ext4 有自己的一套路，完整路线见 **`references/ext4.md`**。速查：

| 顺序 | 做什么 | 命令 | 耗时 |
|---|---|---|---|
| 0 | **先看加密进程还在不在** | `ls -l /proc/*/exe \| grep deleted` | 秒级 |
| 1 | **立刻导出 jbd2 日志**（越早越灵） | `python3 scripts/ext4_probe.py --dev /dev/sda1 --dump-journal /tmp/jrn.bin` | 分钟级 |
| 2 | 路线 B：明文提取（0x25 约 88%、0x26 尾部全部） | `python3 scripts/plain_extract.py --stamp 恢复 /volume1/homes/xxx` | 分钟级 |
| 3 | 路线 C：找副本 | `python3 scripts/plain_index.py` + `verify_origins.py` | 分钟级 |
| 4 | **路线 E1：日志里找回旧内容** | `python3 scripts/jrn_match.py /tmp/jrn.bin --cipher-dir <密文目录> --out /tmp/jrn_out` | 分钟级 |
| 5 | 路线 E2：已删除 inode | `debugfs -R "dump <inode> /tmp/out" /dev/sda1` | 分钟级 |
| 6 | 路线 D：雕刻（**改用 `--range`**） | `carve_scan.py --fs ext4` → `carve_gen_hits.py --range START:END` | 小时级 |

**要点**：

- ext4 的元数据和数据混在同一分区，没有 Btrfs 的 DATA chunk 概念，
  所以扫描器要用 `--range START:END`（偏移相对 `--dev`），而不是自动找 chunk；
- `ext4_probe.py` / `jrn_match.py` 用的加密区间语义与 `plain_extract.py` **完全一致**
  （mode `0x24` / `0x25` / `0x26` 同一套定义）；
- **ext4 红线比 Btrfs 多两条**：**不要跑 `e2fsck`（不带 `-n` 的会清掉释放的块，
  把还没捞的旧数据彻底销毁）**、**不要用 `debugfs -w`**；
- 汇报口径：ext4 上切出的明文段是**逐字节精确**的；日志里拼回来的要标
  「候选 + 结构校验通过」，**不能和精确恢复混在一起说**。

### 9. 验证（缺一不可，分开登记）

1. **SHA**：解包时计算的 SHA 必须等于 NAS 端 manifest 里的 SHA，用来排除传输错误。
2. **校验和证实**：只适用于开启校验和的共享。运行 `RUN csum @LIST --g G`，逐个 4K 块比对 CRC32C，这是 exact 恢复最强的证据。NoCOW 共享没有校验和，只能依靠第 3、4 项。
3. **完整解码**：`python c3r_local.py validate 输出目录 --known 已知原件目录 --workers N`，图片用 Pillow/pillow-heif 完整解码，音视频用 ffmpeg 解码。
4. **已知原件对照**：拿手机、云盘、旧盘、幸存压缩包里的副本逐字节比对。
5. **明文部分的结构自证**（路线 B）：填充后的文件能否被 zipfile 解析、中央目录成员能否解压、PDF 能否打开、能否提取出文本。这一步能把"救出了东西"和"救出了垃圾"区分开。
6. **放回原目录前的最后一道闸**：用户要的是"双击能打开"，不是"目录里有个文件"。往原路径写之前必须过结构验证（zip 能 testzip、PDF 有 `%%EOF`、OSheet 容器能解析且分片全解、能抽出真业务数据），写完立刻回读校验。**只新增、不覆盖、不动 `.L0CK3D`。** 详见 `references/osheet.md` 第 3、4 节和 `scripts/restore_inplace.py`。

判读原则：

- exact 且校验和全部一致、但解码报错的文件，是**原文件本身**就有问题（老 DVDRip、录屏、iPhone HEVC 很常见），应算恢复成功。
- exact 且校验和一致、但和"已知原件"对不上时，**先怀疑本地副本**。第一个案例里就有一份本地副本坏了一个 4K 块。
- 推测类文件只有"解码通过"一种证据。如果两个候选都能解码，要标注出来，不能说成"证实"。
- 明文部分填充的文件**不是完整恢复**，必须单独登记，不能与 exact 混在一起汇报。

### 10. 难处理文件

- **大文件跨 extent**：一个 Btrfs extent 最大 128MiB。加密段一旦超过这个长度，或者原文件本来就碎片化，会有一整块原 extent 被完全覆盖并释放，只能外推它的位置。外推有时成功，有时那块已被别的数据重新占用。
  - **省空间的候选流程**：先用 `extract --variant prev` 只导出一种候选，用格式自带的校验（压缩包 CRC：`7z t`、`bz t`、`unrar t`；视频解码）筛出失败的文件；再对失败的文件跑 `patch --variant next`，只导出推测段另一侧的数据（通常只有几 MB），本地 `apply-patch` 后重测。如果没有变好，用 `revert-patch` 回退（原字节存在 `*.c3rbak` 里）。
  - **对效果要有预期**：第一个案例中，数据区几乎写满（99%）的卷上，88 个推测类压缩包只有 4 个完全通过 CRC，约一半只坏 1 个成员（推测段落在那个成员上）；对 18 个有另一侧候选的文件换成 next，**没有一个改善**。也就是说，被释放的原 extent 往往已被复用。卷空闲空间越大、事发后写入越少，推测成功率越高。
  - 只坏 1 个成员的压缩包，其余成员仍然完好，可以用解压工具"跳过错误继续解压"抢救出来。
- **视频缺 moov 或头尾**：中间 88% 以上通常都在，可以试 `untrunc`，用同一台设备、同样设置拍的完好视频作参照，重建索引。
- **Synology Photos 的 `@eaDir` 缩略图和转码视频**：原件救不回时，可以拿它们做低清保底。
- **小文件和数据库**：引导用户去找手机、云盘、PC 上的副本。可以按路径、文件名、大小、月份生成清单帮他们找。

### 11. 报告

按 `references/report-template.md` 输出，至少包括：

- 环境；G 值和取值依据；各共享的 CoW / NoCOW 状态和 lastsnap；
- 普查统计；导出、验证数字（精确并经校验和证实、仅 SHA、推测、部分明文、雕刻弱候选、失败，分开列）；
- 未恢复部分的去向建议；
- 产物路径；
- 保护提醒：密文继续保留；恢复结果至少再备份一份；重建 NAS 时所有共享开启校验和，并配置定时快照。

### 12. 交付前自检清单（最容易翻车的一步）

用户要的不是"目录里有个文件"，而是"**双击能打开**"。文件放进原目录之前，逐项过：

| # | 检查 | 工具 / 判据 | 踩过的坑 |
|---|---|---|---|
| 1 | 内容是不是原文 | 明文区与密文逐字节一致 | 只看文件名/大小 |
| 2 | 结构是不是自洽 | `osheet_check.py`（OSheet）、`pdf_validate.py`（PDF）、`zipfile.testzip()`（zip）、`Image.open().load()`（图片） | 用**宽松**解析器判"通过"——坏文件照样能读出条目 |
| 3 | 阅读器会不会拒 | PDF 要有 Catalog、xref 偏移要准、页面 `/Contents` 要在；OSheet 要头部/条目链/尾部全自洽 | 只查魔数和结尾标记 |
| 4 | 写回原位了吗 | 只新增、不覆盖、目标已存在就跳过 | 覆盖掉用户的文件 |
| 5 | 属主和 ACL 对吗 | `fix_nas_acl.py`：属主改成该用户，ACL 用同目录原始文件当模板 | root 建的文件 admin 在 File Station 里读不到；**已有 ACL 判断会漏 chown**；**有的 home 默认 ACL 没有 administrators 条目**，admin 连读都读不到（`synoacltool -add` 补） |
| 6 | 写完回读校验 | 重读算 SHA；OSheet 另用 `verify_xlsx.py` 抽样比对源容器每一格 | 相信"写成功"的返回值 |
| 7 | 目录干净吗 | 冗余中间产物删掉，唯一残留单独放一个名字说清楚的目录（如 `9_仅剩明文残片_打不开`）；上一轮的散装产物收进「_原样」留档目录，别留在顶层 | 一堆打不开的废品混在交付目录里 |
| 8 | 说明写了吗 | 每个目录一行说明：能开什么、不能开什么、为什么 | 用户以为是文件坏了 |
| 9 | **交付形态对不对** | 表格类必须交付**一个 xlsx**（多工作表、多标签页），不是"一个工作表一个 CSV"。`.osheet` 打不开就以 xlsx 为准（用户可自行在群晖转在线表格），但 `.osheet` 里的**附件要另外抠出来** | 用户原话："分了那么多文件出来，那才叫还原修复" |
| 10 | **数据量口径对不对** | 汇报"恢复了几格"要用**实际有值的格子数**，不是 `rowCount×colCount` 画布尺寸。`rowCount=100, colCount=30` 的表可能只有 4 行 40 格有值 | 把 3000 格画布说成"3000 格数据"，用户一看就发现对不上 |
| 11 | **校验是全量还是抽样** | 关键文件做**全量逐格比对**（`verify_osheet_xlsx.py` 抽样会漏：3000 格画布里 2960 格是空但带样式的格子，抽样 400 格只命中 2 格） | 只抽样就宣布"校验通过"，实际有值的格子根本没测到 |
| 12 | **工作表数量对吗** | 交付前统计每个 sheet 的**工作表数 + 非空格数**（openpyxl），和源容器 / 已知原件对比 | **重建件可能整张表地缺失**（实测丢过 4 张表、1.3 万格），而它"打开看起来完全正常" |

**给用户的话术**：先说清楚"哪些现在就能双击开、哪些要先下载到电脑用 WPS/Excel 开、
哪些是仅剩的残片"，再说"打不开不是文件坏，是格式/预览器不支持"。
`.osheet` 是群晖上 WPS 用的表格格式（在**群晖里**用 WPS 打开，在电脑上双击会走
云端转换，容易报"网络连接不稳定"），`.xlsx` 是 Excel/WPS 通用格式（拷到电脑上双击就开）；
群晖网页预览器不认识 `.osheet`，File Station 里双击预览不成功不代表文件有问题。
收尾时**每个文档只留一份恢复件、用原名**（同名多份会让用户点开错的那份）。

### 13. 收尾清理：把目录整理成"只留下用户要的文件"

恢复做完不等于结束。一个目录里往往同时躺着这些东西，用户看到的就是"一堆积乱七八糟的文件"：

```
原名.osheet.L0CK3D      密文（勒索产物）
原名.osheet             恢复件（WPS 打开）
原名.xlsx               恢复件（Excel 通用）
原名_Drive重建.osheet   中间产物（手工重建，WPS 可能打不开）
"原名 .osheet"          带空格 / 带 _1 后缀的重名副本（最容易点错的那份）
read-me3.txt            勒索信
```

**目标状态：每个文档一份 `.osheet` + 一份 `.xlsx`，其余清掉。**

用 `scripts/tidy_delivery.py`（**默认预览，必须显式 `--apply` 才真删**）：

```bash
# 1) 先预览，把清单给用户看
python3 tidy_delivery.py <目录> --dry --report /tmp/tidy.txt

# 2) 清理中间产物（保留密文）
python3 tidy_delivery.py <目录> --apply --backup-dir <NAS 外的备份目录>

# 3) 用户确认要连密文一起清（仅限"已成功恢复并验收通过"的那批）
python3 tidy_delivery.py <目录> --apply --drop-cipher --backup-dir <备份目录>
```

判定规则：

- 同一文档同一扩展名有多个 → **留 mtime 最新的那份**（精确原件是最后装上的，mtime 最新）。
- 文件名含 `_Drive重建` / `_已修复` / `_部分修复` / 空格 / `_1` 后缀 → 整组视为中间产物，删。
- **密文单独分组**，绝不能和同名恢复件混在一起判重（否则会把恢复件当成"重复"删掉，或反之）。
- `read-me3.txt` 勒索信**默认保留**（是事件凭证），要删得显式 `--drop-ransom-note`。
- 删任何东西之前先复制到 `--backup-dir`；群晖上删除默认进回收站，等于双保险。

**收尾自检**：

1. 目录里每个文档**只有一份** `.osheet` 和一份 `.xlsx`，文件名干净（无空格、无 `_1`）。
2. 交付件与交付前校验过的文件**SHA-256 一致**（整理过程最容易出错的就是"装错版本/装漏"）。
3. **只清了已恢复的那批**——其它目录里尚未恢复的 `.L0CK3D` 一个都没动。
4. NAS 之外**至少留一份备份**（本机 + 群晖回收站）。
5. 勒索信副本留在本机（`orig_len` 是雕刻认领的唯一长度依据，密文删了就只能靠它）。

**⚠️ 群晖回收站是 per-home 的**：`/volume1/homes/<用户>/#recycle/`，
**不是** `/volume1/#recycle/`。找回收站别找错地方。

**⚠️ 写清理脚本时别用 shell glob 删文件。** `"$DIR"/* .osheet` 里的 `*` 在引号外，
`for` 会把它当成**多个词**（第一个词展开成全部文件，后面是字面量 `.osheet`），
`rm -f "$f"` 就把**整个目录清空了**。**一律用 `find -maxdepth 1 -type f -name ... -exec rm {} \;`**。

## 14. 收尾回写 skill（**每轮必做，这是本 skill 的自我迭代机制**）

**恢复完一轮，不写回 skill = 这一轮的学费白交。** 下一轮换个会话、换个模型，
能继承的只有这个 skill 目录。所以每轮结束前，**必须**把新学到的东西落到文件里。

### 14.1 五处落点（按重要性）

| 落点 | 写什么 | 什么时候写 |
|---|---|---|
| `references/pitfalls.md` | **踩过的坑**：现象 / 原因 / 处理，一行一条 | 每次踩坑当场记，别攒到最后 |
| `references/batch-osheet-recovery.md`（及其它 reference） | **新打通的路线**、新的操作步骤、新的脚本用法 | 出现新方法时 |
| `SKILL.md` 的**工具表**和**执行顺序表** | 新脚本的用途、新的阶段顺序 | 加了新脚本时 |
| `references/case-*.md` | 本轮实战实录（数字、路径、结论） | 每轮结束 |
| `scripts/` | 本轮写的脚本**同步进 skill 目录** | 写完脚本立刻（否则下轮找不到） |

### 14.2 收尾自检（做完这几条才算这轮结束）

```
[ ] 新脚本已 cp 进 skill/scripts/（不是只留在工作目录）
[ ] 新脚本在 SKILL.md 工具表里有对应一行（用途 + 在哪运行）
[ ] 本轮踩的坑已在 references/pitfalls.md 里有条目
[ ] 本轮的新方法已在 references/*.md 里有可复制的命令
[ ] 实战案例已更新到 references/case-*.md（带真实数字）
[ ] 进度表已结项：progress.py --dir <工作目录> close --result "..."
[ ] 工作目录里的 NEXT-SESSION-PROMPT.md 已更新（下一轮的入口）
[ ] 报告已写（工作目录下的 RECOVERY-*.md），数字与实际装回的文件数一致
```

> **收尾时先 `progress.py close`，再回头把 `PROGRESS.md` 里 `log` 出来的
> 踩坑条目搬进 `references/pitfalls.md`**——那是这一轮最值钱的东西，
> 不用重新回忆，日志里已经写好了。

### 14.3 写回时的纪律

- **只写"实测过"的**：没验证过的推测不要写成结论，标注"待验证"。
- **带数字**：把"命中率从 0 到 7/16"和"效果很好"写成前者，前者下轮能直接用。
- **带可复制的命令**：路径、参数、顺序都写全，下一轮直接抄。
- **别覆盖上游**：同步上游更新时只 diff `c3r_btrfs.py` / `c3r_local.py` / `SKILL.md` / `pitfalls.md`
  四个文件，把上游新增片段**移植**进来，不要整file覆盖（会抹掉路线 B/D 和本地新增内容）。

## 给执行模型的提示

- **第一次跟用户说话，先自我介绍 + 索取 4 项参数**（SSH 地址/端口、账号密码、
  目标目录绝对路径、结果输出到哪），**不要一上来就开跑**。照「开工第一步」那节做。
- **主动讲清"不能解密"**。用户找过来时通常以为能"破解"，不提前说清楚，
  后面交付不完整会变成"你骗我"。
- **密码别让用户贴在对话里**；优先引导"你自己在终端跑，我给命令"，
  其次用 `NAS_PASS` 环境变量 + `SSH_ASKPASS`。
- 优先用本 skill 自带的脚本；需要改动时，保留只读特性和自校验，不要为了"省事"去掉 G 值检查或边界检查。
- NAS 上 Python 可能较旧（DSM 7 自带 3.8），不要引入第三方库。
- **开工第一件事是 `progress.py init`，不是先跑 preflight**（见 §0.7）。
  每完成一个阶段就 `stage` 一次，数字当场 `metric` 记下来，别攒到最后回忆。
  **换会话接手时第一件事是 `progress.py status`**，读完再动手。
- 长任务放到后台跑，并定期报告进度。估算时间时要考虑 NAS 机械盘的随机读，以及本地解码的 CPU 开销。
- 用户可能并不熟悉 Btrfs。解释时用"旧数据块还被文件的另一部分拽着，所以没被回收"这类说法，少用术语。
- 目标机是 Windows 时注意：PowerShell 管道会改写二进制数据；Windows 自带 ssh.exe 客户端可能卡死（见 `references/transport.md`），必要时改用反向推送。
- **收尾时务必执行第 14 步「收尾回写 skill」**。用户明确要求过："每次都要总结经验，优化技能，方便下次更好用。"
  本 skill 的价值就攒在这些文件里；只把报告写进工作目录、skill 原封不动，等于白干。
- **写回 skill 前先看 `PROGRESS.md` 的日志**——坑都在里面，不用重新回忆。

## 版本来源与维护

本项目是上游 [`crt106/c3rb3r-btrfs-recovery`](https://github.com/crt106/c3rb3r-btrfs-recovery)（MIT）的**扩展**。
上游版权声明保留在 `LICENSE`；同步上游时**移植片段，不要整文件覆盖**。

- **上游原样**：路线 A 的 `c3r_btrfs.py` / `c3r_local.py` / `mkjob.py`，以及 `compatibility.md`、`c3rb3r-format.md`、`report-template.md`。
- **本项目新增**：

| 方向 | 内容 |
|---|---|
| 路线 B（明文提取） | `plain_extract.py`、`salvage_zip.py`、`probe_modes.py`、`pdf_rebuild.py`、`pdf_validate.py`、`references/plain-extract.md` |
| Synology Drive 重建 | `gitls.py`、`gitgrep.py`、`rebuild_from_drive.py`、`office_index.py`、`office_report.py`、`references/synology-drive.md` |
| Drive 字节级精确重建 | `rebuild_exact.py`、`compare_drive.py`、`verify_vs_cipher.py`、`match_drive_all.py`、`export_map.py`、`plan_batch.py`、`rebuild_batch.py`、`final_pipeline2.py`、`references/synology-drive.md` 第 9 节 |
| OSheet 压缩形态重建 | `osheet_rebuild_from_drive.py`、`osheet_fix_crlf.py`、`drive_repo_probe.py`、`drive_grep_all.py`、`references/osheet-rebuild-exact.md` |
| 路线 D（雕刻） | `carve_scan.py`、`carve_match.py`、`carve_worker.py`、`carving.md` |
| 路线 D 精确版（`.osheet` 强签名） | `carve_osheet_sig.py`、`carve_osheet_identify.py`、`carve_osheet_near.py`、`carve-osheet.md` |
| 路线 D 通用版 | `carve_gen.py`、`carve_gen_hits.py`、`carve_claim.py`、`carve_install.py`、`references/carve-generic.md` |
| 雕刻索引反查 | `carve_id_dump.py`、`carve_probe.py`、`carve_len_dump.py`、`claim_by_len.py` |
| OLE2 解析与认领 | `ole2_lib.py`、`ole2_identify.py`、`ole2_install.py`（`ole2_size.py` 已标注为旧版，公式少算 512 字节） |
| OSheet 解析/修复/校验 | `osheet_parse.py`、`osheet_strict.py`、`osheet_fix.py`、`osheet_repair.py`、`osheet_check.py`、`osheet_compress.py`、`check_payload.py`、`references/osheet.md` |
| OSheet 交付 | `osheet_to_xlsx.py`、`verify_osheet_xlsx.py`、`osheet_extract_attach.py`、`references/osheet.md` 第 9、12 节 |
| 收尾清理 | `tidy_delivery.py`（单目录）、`cleanup_home.py`（递归整个 home） |
| 进度记录 | `progress.py`（`PROGRESS.md`：开工 / 切阶段 / 记数字 / 读回 / 结项）、`references/progress-log.md` |
| 原位放回 | `restore_inplace.py`、`fix_nas_acl.py` |
| **ext4 路线（v1.1.0 新增）** | `ext4_probe.py`（超块探测 + 已删 inode + **jbd2 日志导出**）、`jrn_match.py`（用明文区指纹**在日志里找回被覆盖的原始字节**）、`references/ext4.md` |
| 交付前闸门 | `validate_installed.py`、`deep_validate.py` |
| 其它 | `plain_index.py`、`read_footers.py`、`pdf_xref_repair.py`、`pdf_rebuild_plain.py`、`xlsx_from_members.py`、`drv_survey.py`、`drv_survey2.py`、`drv_grep.py`、`build_wps.py`、`scan.sh`、`status.sh`、`upload.sh`、`mkjob.py` |

### 配套技能

`performing-file-carving-with-foremost`、`recovering-deleted-files-with-photorec`
（安装到 `~/.agents/skills/`）。

### 实战案例（已脱敏）

- `references/case-20261031-osheet-batch.md` —— 成批恢复 74 个 `.osheet` 的实录：
  Drive 重建（**丢了 4 个工作表**）、雕刻捞回字节级精确原件、worker 步进死循环、
  扫描拖垮 NAS 的限并发方案；第二轮 Drive 重建升级为**字节级精确**（19/21 与原件 SHA 一致）、
  成批恢复 44 个、长度匹配撞车、Drive 同步覆盖、DSM 封禁 IP；第三轮按 `id` 反查
  把剩下 16 个里的 7 个变成精确原件（累计 65/74）。
- `references/case-20261031-user-home.md` —— 用户点名单个 home 目录的实录：
  624 个密文、`survey` 全 `no_candidate`、142 个原件来自 `Backup/`、
  7.9GB zip 里全是密文、`@sharesnap` 是上一代目录结构、密文 ctime 不可信、
  0x25 容器中央目录落在加密区、2.65TB 扫描约 2.2 小时；
  第二轮 159 个雕刻件 + 23 个明文副本装回（160/160 结构校验通过）、
  3 处同长度歧义逐个取证、**同一明文→密文不同**（每文件随机 nonce）、
  全盘明文索引挖出 23 个原件、17 个 PDF 就地修复零损失；
  第三轮扫描改单路、扫描器丢数据与覆盖两个 bug、**OLE2 改按正文认领救回 4 个 `.doc`**。
- `references/case-20261103-ext4-route.md` —— ext4 路线的设计与自检
  （⚠️ **没有真实 ext4 设备可跑**，逻辑只用合成样本验证）：
  为什么 ext4 没有写时复制、**jbd2 日志为什么留着旧内容**、用明文区当指纹的定位原理、
  28 项自检断言（含"拼出的候选件与原始文件逐字节相同"）、
  **顺手修掉的扫描器静默失败**（读失败被 `except Exception: pass` 吞掉 → "扫完了 0 命中"），
  以及**没验证的部分**（日志实际留存行为、跨事务映射、装回端到端）。
- `references/batch-osheet-recovery.md` —— 从"单个文件试水"到"成批交付"的操作手册：
  全盘密文盘点方法、雕刻索引批量认领、**Drive 仓库↔密文的长度反推公式与撞车防线**、
  `metatext` 长短两版、**两条路互为交叉验证**、密文明文区独立对证、四关交付自检。

> 案例中的**人名、公司名、共享名、NAS 地址、uid、子卷 ID 全部已替换为占位符**，
> 保留的是路线选择依据、数字和教训。

### 同步上游更新

拉 tarball（`codeload.github.com/crt106/c3rb3r-btrfs-recovery/tar.gz/refs/heads/main`），
只 diff `c3r_btrfs.py` / `c3r_local.py` / `SKILL.md` / `pitfalls.md` 四个文件，
把上游新增的片段**移植**进来，不要整文件覆盖（会抹掉路线 B/D 和本项目新增内容）。
