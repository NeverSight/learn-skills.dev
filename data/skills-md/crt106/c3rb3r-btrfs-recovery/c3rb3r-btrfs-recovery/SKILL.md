---
name: c3rb3r-btrfs-recovery
description: 恢复被 C3RB3R / Cerber 系勒索软件（文件后缀 .L0CK3D、勒索信 read-me3.txt）加密的群晖（Synology DSM）或其他 Btrfs NAS 上的数据，无需密钥：利用 Btrfs 写时复制留下的旧 extent 逐字节还原原文件，并用 Btrfs 校验和逐块证实。覆盖 CoW / NoCOW 判定、子卷快照代数（lastsnap）效应、extent 树精确重组、大文件跨 extent 推测、统计、导出、验证和报告。只要用户提到 NAS / 群晖 / 黑群晖 被勒索、.L0CK3D、read-me3.txt、C3RB3R、Btrfs 文件被加密想恢复、"没有备份没有快照怎么救"，即使没提 Btrfs 或 extent，也应使用本 skill。Use for ransomware recovery of .L0CK3D files on Synology/Btrfs volumes without the key.
---

# C3RB3R 勒索后的 Btrfs 无密钥恢复

## 这个 skill 解决什么

C3RB3R 用 ChaCha8 只加密每个文件的一部分：小文件整体加密，1–5MB 的文件只加密前 1MiB，更大的文件加密三段、共约 12%。加密后在文件末尾追加 588 字节，再改名为 `*.L0CK3D`。没有密钥就解不开，但**它是原地改写文件的**。只要满足下面任一条件，这次改写在 Btrfs 上就会写到新位置，原始明文留在旧 extent 里：

- 共享是 CoW（DSM 建共享时勾选了"数据校验和"）；
- 共享虽是 NoCOW，但数据写入早于该子卷**最后一次快照**（快照即使后来删掉了也算）。

旧 extent 只要还被文件中未加密的那部分引用，就不会被释放，原始字节也就一直在盘上。我们直接读块设备把它取回来，再拿 Btrfs 自己存的校验和逐块证实。

参考成果（第一个案例）：homes、photo 等 CoW 共享找回 35,445 个文件（229.9GB，经 SHA 核对与解码验证）；NoCOW 共享中 2024 年 6 月快照前写入的部分又找回约 1 万个可精确还原的文件。精确恢复的部分在开启校验和的共享上抽检约 20 万个 4K 块，全部与 Btrfs 校验和一致。

先读 `references/principles.md` 了解原理。遇到环境或设备问题查 `references/compatibility.md`，遇到结果异常查 `references/pitfalls.md`。

## 第 0 步：先判断还有没有"拿密钥"的窗口（只有几小时）

**加密进程可能还在跑。** 如果攻击就发生在几小时内，用 `ls -l /proc/*/exe 2>/dev/null | grep deleted`、`ps` 查有没有可疑进程，例如公开案例里的 `/usr/bin/libgld -n 308`。如果有，**先 `kill -STOP` 冻结它，不要 kill，也不要重启**，然后按公开救援项目从进程内存里取会话主密钥：

- https://github.com/soimy/c3rb3r-rescue
- https://github.com/Benjamin-zlt/c3rb3r-baremetal-rescue

这是唯一能把文件全部解开的路线，比本 skill 的收益大得多。

进程已经退出（重启过，或事发已十几小时）时，内存路线基本无望。第一个案例对 16.7GB RAM、zram、磁盘 swap 做了逐字节 AES 密钥扫描，又拿内存中 194 个 ChaCha 状态对 77.8 万个文件试解，结果都是 0。此时直接进入下面的 Btrfs 路线，不要在内存上反复投入。详见 `references/c3rb3r-format.md`。

## 安全红线（关系到恢复能否成功）

1. **不删除、不移动到别的卷、不覆盖任何 `.L0CK3D` 文件，不清空回收站。** 旧 extent 靠密文文件"拽着"才没被释放，删掉密文就等于销毁原件。
2. **不做 defrag、balance、`btrfs check --repair`、rescue，不运行来源不明的"解密器"。** defrag 会重写 extent。
3. 恢复期间尽量减少卷上的写入：暂停 NVR 录像、下载、Photos 索引、同步任务。NAS 重启或 DSM 升级本身不会破坏被引用的旧 extent，但会丢掉内存现场，并带来大量写入。等导出完成后再做。
4. 恢复结果写到 **NAS 以外**的盘，绝不回写原目录。
5. 所有 NAS 端操作只读。用本 skill 的 `scripts/c3r_btrfs.py`，它只做查询、读文件和读块设备，临时文件只放在 `/tmp`，用完删除。
6. 汇报要诚实："精确恢复 + 校验和证实"、"推测后解码通过"、"失败"必须分开写，候选不等于恢复成功。

## 工具

| 文件 | 在哪运行 | 作用 |
|---|---|---|
| `scripts/c3r_btrfs.py` | NAS（root，Python 3.6+ 标准库） | `preflight`（环境自检）、`env`、`gens`、`survey`、`extract`（可用 `--variant prev\|next\|both` 只导一种候选）、`patch`（只导出推测段另一侧候选的数据）、`csum`、`plan` |
| `scripts/mkjob.py` | 本地 | 把上面的脚本连同路径列表打包成一个 stdin 作业，避免命令行过长，也避免在数据卷上落文件 |
| `scripts/c3r_local.py` | 本地（Python 3.8+；可选 Pillow、pillow-heif、ffmpeg） | `extract`（解包 tar 流）、`validate`（SHA、解码、已知原件对照、挑选最佳候选）、`apply-patch` / `revert-patch`（打补丁换候选并可回退）、`report`（统计） |

运行方式和传输细节（Linux、macOS、Windows，sudo 密码，吞吐优化）见 `references/transport.md`。下文用 `RUN <参数>` 表示：

```
python mkjob.py [--list 列表.txt] -- <参数> | 加上 sudo 密码行 | ssh 用户@NAS "sudo -S -p '' sh -s" > 输出文件
```

## 工作流程

### 1. 自检与可行性检查（几分钟，只读）

**任何设备都先跑 `RUN preflight <某个 .L0CK3D 文件>`。** 它会逐项检查：

- Python 版本、root 权限、是否 btrfs；
- 超级块（扇区大小、校验和算法）；
- dump-tree 工具与 chunk 映射；
- TREE_SEARCH 接口；
- 端到端读取比对（按 extent 映射读块设备，结果与直接读文件一致）；
- 与 `btrfs-map-logical` 的交叉验证；
- 校验和自检、NoCOW 标记。

每一项都会给出 OK、WARN 或 FAIL，失败时附带处理建议。**只要有 FAIL，就按 `references/compatibility.md` 的对应条目处理，处理好之前不要继续。** 那份文档还涵盖：群晖 DSM 6/7、OMV、Unraid 等其他 Btrfs 系统，QNAP 与 ZFS 为什么不适用，没有 Python 3 时怎么办，以及拆盘到 Linux 电脑离线处理的通用方案。如果某台设备需要改脚本，改完后必须重新通过该文档最后一节列出的自检。

然后运行 `RUN env /volume1`，记录以下信息：

- 卷是不是 btrfs；块设备（群晖一般是 `/dev/mapper/cachedev_0`）；DATA 剖面（single 或 RAID1 类可以，RAID0/5/6/10 工具会拒绝）。
- **每个共享根目录是否 NoCOW**（`share_roots[].nocow`）。CoW 共享是主战场。
- **每个子卷的 `lastsnap`**。如果 NoCOW 共享的 lastsnap 大于 0，那么这个代数之前写入的文件仍可能恢复。这是 Btrfs 的规则：数据代数不大于 last_snapshot 的 extent，即使 NoCOW 也必须 CoW。
- 文件尾部的会话标记（marker）每个受害者都不同，工具按结构识别尾部，不依赖标记值。

### 2. 确定 G_ATTACK（区分"加密时新写"和"原有"的 extent）

`RUN gens /volume1/homes /volume1/photo --sample 3000`，采样要覆盖**多个受影响的共享**，因为不同目录被加密的时间不同。

- 取 `pos0_gen_min`（加密时最早写入的代数）减去一点余量，作为 `--g`。
- 检查 `highest_gen_below_pos0_min`：它应当明显小于 G。第一个案例中，攻击期新写入的代数是 4,842,057–4,842,378，攻击前最近一次正常写入是 4,668,578，中间有一大段空档。如果两者紧挨着，就要人工核查：有的文件开头可能没被加密，或者攻击前不久有正常写入。
- G 定错的后果：定得偏大，会把新写的密文 extent 当成"旧数据"读回；定得偏小，会把真正的旧数据当成新写入而丢掉。后面的边界自校验和"旧数据不等于密文"检查能发现这类错误。

### 3. 单文件原理验证（必须先做）

选一个**确知原件**的加密文件，比如从幸存 ZIP、手机或云盘里拿到的同一个文件：

1. 运行 `RUN plan <该文件> --g G`，确认未加密区段共用一个旧 extent，加密区段是新 extent；
2. `RUN extract <该文件> --g G` 导出它；
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
| `no_candidate` | 整文件加密（多为 1MiB 以下的小文件），旧 extent 已释放 | 救不回，去找其他副本 |
| `boundary_mismatch` | 自校验失败 | 先查 G 和工具，不要导出 |
| `inline` / `compressed` | 内联小文件，或 Btrfs 透明压缩 | 本工具不处理，见 pitfalls |
| `no_rewrite_found` | 没找到新 extent（多为未知模式且原地覆盖），或文件并未被改写 | 单独人工看 |

要向用户说明规律：CoW 共享里，大于约 1.004MB 的照片和视频几乎都是 `exact`；1MiB 以下的小文件整个被加密，属于 `no_candidate`；数据库文件不论大小都被整个加密。

### 5. 导出

`RUN extract @LIST --g G` 的输出直接通过管道送给本地 `python c3r_local.py extract - 输出目录`，边传边解包，不落中间 tar 文件。

- 先导最重要的目录（照片、文档），按批次分目录。
- 写入前测一下目标盘的写速度。第一个案例里，一块近满的 SATA SSD 只有不到 1MB/s，换盘后达到 50–70MB/s。
- 导出和验证分开跑：上一批验证的同时导出下一批，验证用多进程。不要串行，否则 NAS 会长时间空等。
- tar 成员名就是 NAS 上的路径去掉 `.L0CK3D`。推测候选会在扩展名前加 `.__prev__`、`.__next__` 后缀，部分恢复的加 `_partial`。

### 6. 验证（缺一不可，分开登记）

1. **SHA**：解包时计算的 SHA 必须等于 NAS 端 manifest 里的 SHA，用来排除传输错误。
2. **校验和证实**：只适用于开启校验和的共享。运行 `RUN csum @LIST --g G`，逐个 4K 块比对 CRC32C，这是 exact 恢复最强的证据。NoCOW 共享没有校验和，只能依靠第 3、4 项。
3. **完整解码**：`python c3r_local.py validate 输出目录 --known 已知原件目录 --workers N`，图片用 Pillow/pillow-heif 完整解码，音视频用 ffmpeg 解码。
4. **已知原件对照**：拿手机、云盘、旧盘、幸存压缩包里的副本逐字节比对。

判读原则：

- exact 且校验和全部一致、但解码报错的文件，是**原文件本身**就有问题（老 DVDRip、录屏、iPhone HEVC 很常见），应算恢复成功。
- exact 且校验和一致、但和"已知原件"对不上时，**先怀疑本地副本**。第一个案例里就有一份本地副本坏了一个 4K 块。
- 推测类文件只有"解码通过"一种证据。如果两个候选都能解码，要标注出来，不能说成"证实"。

### 7. 难处理文件

- **大文件跨 extent**：一个 Btrfs extent 最大 128MiB。加密段一旦超过这个长度，或者原文件本来就碎片化，会有一整块原 extent 被完全覆盖后释放，只能外推它的位置。外推有时成功，有时那块已被别的数据重新占用。
  - **省空间的候选流程**：先用 `extract --variant prev` 只导出一种候选，用格式自带的校验（压缩包 CRC：`7z t`、`bz t`、`unrar t`；视频解码）筛出失败的文件；再对失败的文件跑 `patch --variant next`，只导出推测段另一侧的数据（通常只有几 MB），本地 `apply-patch` 后重测。如果没有变好，用 `revert-patch` 回退（原字节存在 `*.c3rbak` 里）。
  - **对效果要有预期**：第一个案例中，数据区几乎写满（99%）的卷上，88 个推测类压缩包只有 4 个完全通过 CRC，约一半只坏 1 个成员（推测段落在那个成员上）；对 18 个有另一侧候选的文件换成 next，**没有一个改善**。也就是说，被释放的原 extent 往往已被复用。卷空闲空间越大、事发后写入越少，推测成功率越高。
  - 只坏 1 个成员的压缩包，其余成员仍然完好，可以用解压工具"跳过错误继续解压"抢救出来。
- **视频缺 moov 或头尾**：中间 88% 以上通常都在，可以试 `untrunc`，用同一台设备、同样设置拍的完好视频作参照，重建索引。
- **Synology Photos 的 `@eaDir` 缩略图和转码视频**：原件救不回时，可以拿它们做低清保底。
- **小文件和数据库**：引导用户去找手机、云盘、PC 上的副本。可以按路径、文件名、大小、月份生成清单帮他们找。

### 8. 报告

按 `references/report-template.md` 输出，至少包括：

- 环境；G 值和取值依据；各共享的 CoW / NoCOW 状态和 lastsnap；
- 普查统计；导出、验证数字（精确并经校验和证实、仅 SHA、推测、失败，分开列）；
- 未恢复部分的去向建议；
- 产物路径；
- 保护提醒：密文继续保留；恢复结果至少再备份一份；重建 NAS 时所有共享开启校验和，并配置定时快照。

## 给执行模型的提示

- 优先用本 skill 自带的脚本；需要改动时，保留只读特性和自校验，不要为了"省事"去掉 G 值检查或边界检查。
- NAS 上 Python 可能较旧（DSM 7 自带 3.8），不要引入第三方库。
- 长任务放到后台跑，并定期报告进度。估算时间时要考虑 NAS 机械盘的随机读，以及本地解码的 CPU 开销。
- 用户可能并不熟悉 Btrfs。解释时用"旧数据块还被文件的另一部分拽着，所以没被回收"这类说法，少用术语。
