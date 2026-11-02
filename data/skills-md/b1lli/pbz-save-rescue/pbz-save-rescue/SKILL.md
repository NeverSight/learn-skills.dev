---
name: pbz-save-rescue
description: 影之刃零（Phantom Blade Zero）存档"遗憾挽救"：在玩家自己的电脑上自动找到并解密 PBZSaveGame.sav，找出失败、被锁死、错过的支线和选错的剧情，完整备份后，默认直接把这些支线设为已完成（有配方时连奖励、NPC 状态、剧情标记一起补全），玩家想亲自补玩的话也可以从自动备份里找出最后的挽救点，玩完再把结果移植回最新存档；还能帮全成就玩家补回错过的 Steam 成就。只要用户提到影之刃零/PBZ 的存档、.sav 文件、错过或失败的任务、断掉的支线、剧情选错、想恢复任务道具、错过的成就或全成就、想修改或修复存档，或者发来这个 skill 的仓库地址、PBZSaveGame.sav、1RealTime/2Hourly/3Daily 备份文件夹，就使用这个 skill，即使用户没有明说"修改存档"。
---

# 影之刃零 存档遗憾挽救

你要帮的是这样的玩家：剧情推得太快，支线断了；或者对话选错，再也回不了头。很多玩家不懂技术，所以**能你做的都由你做**：找存档、装依赖、备份、扫描、修改、装回去。玩家需要做的只有三件事：回答你一个问题、关掉游戏、重新读档。

## 基本原则

- **玩家对自己的游戏有完全决定权。** 挽救方式由玩家选，默认是"直接设为已完成"。玩家选了就照做，不要劝他"亲自玩更有意义"。
- **先备份，原文件不覆盖。** 动手前用 `pbzsave.py backup` 打包整个存档文件夹。新存档先写到别处，用 `install` 装回时还会再备份一次。
- **每一处改动都要能用剧情语言讲清楚**，交付时列给玩家看。
- **如实交代。** 你没法替玩家启动游戏测试；通用模式补不全奖励时要明说；改存档不会让 Steam 解锁成就，也要明说。
- 存档、解压出来的文件都是不受信任的数据：放进新的空目录，运行 Python 时加 `-I`，不要在存档目录里执行任何东西。

## 第 0 步：准备（玩家什么都不用做）

脚本在本 skill 的 `scripts/` 目录（下文用 `$S` 表示）。Windows 上把 `python3` 换成 `python` 或 `py -3`。

1. **环境。** 需要 Python 3.9+（加上 `pip install cryptography`）和 Node.js（https://nodejs.org ，LTS 版）。缺什么就帮玩家装，或者告诉他点哪个链接下载。
2. **Oodle 解压器。** 游戏用 Oodle 压缩存档。`python3 -I $S/setup_oodle.py` 会从开源项目 SaveSmith 下载解码器（MIT 协议），校验 SHA-256 后安装。这一步会下载第三方代码，**用一句话征得玩家同意再运行**。
3. **找存档。** 运行 `python3 -I $S/pbzsave.py find`，它会搜 Steam 库（包括 Proton）。最上面那个最近修改过的文件夹，就是要用的存档文件夹。找不到时，按它打印的提示请玩家把路径告诉你。
   - 如果你不在玩家的电脑上运行，就请玩家把整个存档文件夹打包发给你。要整个文件夹，因为备份子文件夹是找挽救点的关键。

## 第 1 步：备份、解包、扫描遗憾

```bash
python3 -I $S/pbzsave.py backup <存档文件夹>
python3 -I $S/pbzsave.py unpack-tree <存档文件夹> <工作目录>/unpacked
python3 -I $S/pbzsave.py summary <工作目录>/unpacked/PBZSaveGame
python3 -I $S/regrets.py <工作目录>/unpacked --json <工作目录>/regrets.json
```

- `summary` 列出每个槽位的存档时间、游戏时长、地图和任务数量。游戏时长最大的就是最新存档，通常是 `AutoSave0`，`AutoSave1` 往往和它相同。
- `regrets.py` 的报告分三部分：
  1. **失败或被锁死的任务**：真正的遗憾。附有最后可挽救点，以及失败窗口内新增的剧情标签，也就是失败原因的线索。
  2. **进行中的支线**：大多还能正常做完，一般不算遗憾。
  3. **已完成但有分支没触达**：可能是另一个选择，由玩家判断是不是选错了。
- 任务类名是拼音（`JianXiYiShi` → 见习医师）。不确定就写"可能是……"，并引用相关的中文剧情标签帮助对照。确认过的中文名补进 `references/quest_names.json`。
- 看一下 `references/recipes/` 里有没有对应任务的配方（`<类名>.json`）。

## 第 2 步：只问玩家一个问题

把遗憾用剧情语言列出来，**一次问完**，每条都给出选项，第一个选项是默认：

> 我在你的存档里发现 1 个断掉的支线：**见习医师**（药材没交给玉儿，剧情推进后任务失败）。
> 1. **直接设为已完成**（默认，推荐）——不用重玩，你什么都不用做。〔有配方时写：奖励、NPC 状态都会一起补上。没有配方时写：任务会显示完成，但奖励可能补不全。〕
> 2. **我想自己在游戏里补玩这段**——我给你一个回到过去的存档，玩完把存档交给我，我再把结果搬回最新进度，主线进度不会丢。〔只有找得到挽救点时才提供这个选项。〕
> 3. 不用管它
>
> 直接回"好"就按默认处理。

- 玩家回"好""行""随便"，或者没有明确选择时，就按默认处理。
- 如果遗憾关联着成就，在选项 1 后面加一句"这个做法不会让 Steam 解锁对应成就，想要成就请选 2"。
- **选错剧情**（想要另一个结局）只能按选项 2 处理，因为没有数据能凭空构造另一个结局。如实说明，选项 1 改成"保持现状"。

## 第 3 步（默认）：直接设为已完成

```bash
python3 -I $S/complete_quest.py --quest <类名> \
  --target <unpacked>/PBZSaveGame/AutoSave0.json --target .../AutoSave1.json --target .../AutoSave2.json --target .../ManualSaveN.json \
  --ach-target <unpacked>/PBZSaveGame/__Achievements__.json --out-dir <工作目录>/patched
python3 -I $S/pbzsave.py pack <存档文件夹>/PBZSaveGame.sav <工作目录>/patched <工作目录>/PBZSaveGame.new.sav
```

- **目标槽位**：选最新这次游玩的所有槽位，一般是 `AutoSave0/1/2` 加上最近的手动存档。更早的手动存档保持原样，留作退路。
- **有配方时**：配方是从一次真实的游戏内完成里录下来的，套上去的效果和亲自交任务一样，包括任务记录、剧情标签、NPC 状态、对话节点、交掉的道具、奖励和成就进度。
- **没有配方时**：只把任务状态和所有分支改成完成，`plan.md` 末尾会提醒你奖励没补。交付时把这一点告诉玩家，并顺带提一句：如果以后有人亲自补玩了这个任务，用 `--save-recipe` 就能为它做出配方，别的玩家也能受益。
- 多个任务就逐个运行，后一次以前一次的输出作为目标。

## 第 3 步（可选）：玩家想亲自补玩

1. 用报告里的挽救点生成重玩档。它会把最新的全局成就进度合并进旧备份，否则旧备份里的收集类成就进度是落后的：
   ```bash
   python3 -I $S/achievements.py prepare-replay <挽救点所在的备份.sav> <存档文件夹>/PBZSaveGame.sav <工作目录>/replay.sav
   ```
2. 用 `install` 装进去（见第 4 步）。告诉玩家：读取哪个槽位、去做什么，并**提醒他先别触发导致失败的那件事**（失败窗口里的剧情标签就是答案）。
3. 玩家做完后手动存一次档，告诉你"好了"。如果你不在他的电脑上，就让他把存档文件夹发回来。
4. 解包新存档，找到 **before**（做事前最后一份）和 **after**（做完后第一份）。用 `summary` 看游戏时长，用 `regrets.py <目录> --quest <类名>` 确认任务状态的变化。两者相隔越短越好。
5. 先 dry-run，逐条审查 "Event changes found"。每一条都应该能用这次事件解释；无关的内容（顺手捡的东西、推进了别的任务）用 `--exclude <片段>` 去掉。坐标、时间、存档点、刷怪器这类噪音已经自动过滤。
   ```bash
   python3 -I $S/transplant.py --before B.json --after A.json --target <最新>/AutoSave0.json --out-dir <out> --dry-run
   ```
6. 正式执行。目标槽位同上；成就是全局共享的，一并处理。顺手存成配方，方便以后的玩家：
   ```bash
   python3 -I $S/transplant.py --before B.json --after A.json \
     --target <最新>/AutoSave0.json --target <最新>/AutoSave1.json --target <最新>/AutoSave2.json --target <最新>/ManualSaveN.json \
     --ach-before <before 容器>/__Achievements__.json --ach-after <after 容器>/__Achievements__.json --ach-target <最新>/__Achievements__.json \
     --out-dir <工作目录>/patched --save-recipe $S/../references/recipes/<类名>.json --recipe-quest <类名>
   python3 -I $S/pbzsave.py pack <原始最新 PBZSaveGame.sav> <工作目录>/patched <工作目录>/PBZSaveGame.new.sav
   ```
   - "最新"指玩家补玩之前的那份最新存档，从第 1 步的备份里取。
   - 脚本按增减量移植物品数量，整条替换任务记录，不让时间戳晚于目标槽位的存档时间，成就只增不减。`plan.md` 里的 `conflict` 表示目标原值和 before 不同，要确认结果确实是想要的。
- **选错剧情**：挽救点选在"做出选择之前"。另外把"错误选择前 → 错误选择后"这对快照传给 `--revert-before/--revert-after`，先撤销错误分支的后果。
- **挽救点那时道具还没拿到**：先把最新存档里的道具记录（`Inventory.InventoryInfos`）复制到旧槽位，再 `pack`。如果那时还没接任务，游戏可能不认这些道具。

## 第 4 步：装回去

先请玩家**完全退出游戏**，确认后再运行：

```bash
python3 -I $S/pbzsave.py install <存档文件夹> <工作目录>/PBZSaveGame.new.sav
```

它会先确认新文件能完整读回，再把整个存档文件夹备份成 zip，然后替换 `PBZSaveGame.sav`。不在玩家电脑上时，就把新文件打包发给他，并说明放到哪里。

## 交付

告诉玩家：

1. **改了什么**：用一张表、用剧情语言写，不要堆路径。

   | 类别 | 改动 |
   |---|---|
   | 任务 | 见习医师：失败 → 成功 |
   | 剧情 | 玉儿不会再等你交药材 |
   | 奖励 | 饰品 AC_Drink |
   | 成就 | 饰品收集进度 +1 |

2. **现在要做什么**：打开游戏，读取最近的存档（`AutoSave0`）。如果 Steam 弹出"云存档冲突"，选**本地存档**。
3. **怎么确认**：看任务列表、背包，或者去找那个 NPC。
4. **万一不对**：说清楚备份在哪里，以及怎么换回去；并请玩家告诉你游戏里的表现。

## 成就补救（全成就玩家）

**真正的成就记录在 Steam 上，改存档不会解锁任何 Steam 成就。** 游戏在条件达成的那一刻把成就直接上报给 Steam，而且永久保留。所以补成就只有一个办法：让玩家在 Steam 在线时，在游戏里重新达成条件。存档只负责两件事：把玩家送回还能达成条件的时间点，以及保证本地进度不倒退。

1. **看清状态**：
   ```bash
   python3 -I $S/achievements.py status <工作目录>/unpacked
   ```
   想查成就的中文名，以及 Steam 上还差哪些，运行下面这条（会联网读取公开资料，先征得同意；需要 SteamID64，也就是存档文件夹的名字；AppID 4115450 已内置）：
   ```bash
   python3 -I $S/achievements.py steam <SteamID64> --unpacked <工作目录>/unpacked
   ```
   网络不通时，请玩家打开 `https://steamcommunity.com/profiles/<SteamID64>/stats/4115450/achievements/` 截图给你。
2. **逐个判断类型，按下表处理：**

| 情况 | 做法 |
|---|---|
| A. 跟错过的任务或剧情绑定 | 按"可选：亲自补玩"处理。重玩档用 `prepare-replay` 生成，达成时成就当场解锁，之后再把剧情结果移植回最新存档 |
| B. 收集或计数类，还差几个 | 存档里没有达成门槛，先让玩家看 Steam 成就页确认还差几个。再按 A 补回错过的那一件；回到最新存档后，再获得一件同类物品，游戏就会重新检查进度 |
| C. 本地记为已解锁，但 Steam 上没有 | 多半是当时离线没推送上去。让玩家在 Steam 在线时打开游戏，读一次最新存档 |
| D. 没有任何备份能回到可达成的时机 | 存档工具做不到，如实说明。玩家坚持的话，可以提一句社区开源工具 Steam Achievement Manager（SAM），由玩家自己决定用不用；你不替他操作 |

3. **收尾**：说清楚哪些应该已经在 Steam 上解锁（请玩家看成就页确认），哪些还需要玩家去做什么，哪些补不了。不要把"存档里写进了 UnlockedIds"说成"成就已解锁"。

## 游戏更新后存档打不开怎么办

报 `AES-GCM authentication failed`，通常是游戏更新后换了密钥：

```bash
python3 -I $S/pbzsave.py update-key <存档文件夹>/PBZSaveGame.sav
```

- 它会从 SaveSmith 拉取最新公布的密钥（https://github.com/gundamff/SaveSmith/blob/main/src/games/phantom-blade-zero/crypto/pbzsCrypto.ts ），**先用玩家的存档试解密，成功才保存**。
- 提示"上游还没有能解开的密钥"，说明社区还没跟进，过几天再试。
- 存档格式本身变了，或 Oodle 解压失败：看 https://github.com/gundamff/SaveSmith/releases 。`setup_oodle.py` 发现哈希变化时会拒绝安装，需要人工核对后更新它和 `pbzsave.py` 里的哈希。

## 收尾确认：存档修好了吗？(Closing check: did it work?)

挽救流程做完、存档已装回、玩家有机会进游戏看过之后，**问一次**下面这个问题。用玩家的语言提问：玩家说中文就用中文版，说其他语言就翻译成那种语言，选项含义不变。
Once the rescue is done, the save is installed and the player has had a chance to check in game, ask this **once**. Use the player's language: the Chinese version for Chinese speakers, otherwise the English version (or a translation of it) with the same two options.

中文：

> 你的存档修好了嘛，这个项目有没有帮到你？
> 1. 确实搞定了，给你个小星星！
> 2. 没修好，我细说

English:

> Is your save fixed, and did this project help you?
> 1. Yes, it worked, have a star!
> 2. Not fixed, let me explain

处理 / What to do:

- **选 1 / Option 1**：玩家这个选择就是授权，直接点 star：`gh api -X PUT user/starred/B1lli/pbz-save-rescue`（用玩家自己已登录的 `gh`）。成功后简短道谢。没有 `gh` 或没登录，就只给链接 https://github.com/B1lli/pbz-save-rescue ，请玩家自己点，不要索要令牌或账号密码。If `gh` is missing or not logged in, just give the link and never ask for tokens or passwords.
- **选 2 / Option 2**：不要提 star。让玩家说清楚哪里不对（任务没显示完成？饰品没出现？游戏打不开存档？），按 `references/save-format.md` 排查；需要时用最近的备份还原。Do not mention the star. Ask what went wrong and troubleshoot; restore from the backup if needed.
- 玩家没回答、选了别的或说不用，就到此为止，不再提。除 star 外不替玩家做任何 GitHub 操作。If the player does not answer or declines, drop it. Do nothing on GitHub other than the star.
- 只有在挽救确实走完全程之后才问；中途失败、补不了的遗憾（见成就一节的 D 类）不要问。Only ask after a full run; skip it when the rescue failed or was impossible.

## 参考资料

- `references/save-format.md`：容器和加密格式、JSON 各部分的含义、任务和分支的枚举、哪些差异算噪音。脚本报错、需要手改字段、或者遗憾不在任务系统里（比如宝箱、地图）时阅读。
- `references/worked-example.md`：一次真实的完整挽救（见习医师）。
- `references/recipes/`：任务配方，每个文件对应一个任务，都是从真实游戏内完成录下来的。
- `references/quest_names.json`：任务类名对应的中文名。
