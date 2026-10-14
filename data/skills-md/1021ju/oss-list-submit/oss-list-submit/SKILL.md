---
name: oss-list-submit
description: Use when someone wants to promote a company open-source GitHub project by getting it into awesome-xxx lists, MCP/agent registries, developer directories or free backlink sites; or asks "提交 awesome 列表"、"开源项目推广"、"上列表"、"外链目录"、"submit to awesome list"、"list my repo"、"get more stars".
---

# 开源项目上列表 / 外链提交

把一个开源项目提交到对口的 awesome 列表、registry 和目录站，并记录每一条的真实状态。**agent 负责找渠道、筛选、写草稿和核验；PR 和表单由项目作者本人的账号提交。**

## 工具对照（Claude Code / Codex / Cursor 同一份 skill）

| 需要 | Claude Code | Codex | Cursor |
|---|---|---|---|
| GitHub 查询、开 PR、定时监听 | `gh` CLI | `gh` CLI | `gh` CLI |
| 打开目录站、填表、核验 `href` | Claude in Chrome 扩展 | [Tabgent](https://github.com/FibonaAI/tabgent)（Codex 的 Chrome 侧栏） | Cursor 自带的浏览器工具（如果开启了） |

读公开页、查 `href` 也可以直接用 `curl`。

这个 skill 不依赖任何付费 SEO 工具或 API key，装上就能用。没有浏览器工具时，只出草稿，由人去填表。

## 三条硬规则

1. **不批量代提。** 不用公司 bot 或共享账号在短时间内向多个列表开 PR。维护者会把这当 spam 关掉甚至 block，之后整个组织都受牵连。很多列表明文拒收自动/AI 生成的 PR。每个列表只开一个 PR，由作者本人的 `gh` 登录态提交，或把草稿交给作者手动开。用户要求“直接批量提”也一样：说明原因，给出逐个提交的草稿。
2. **先定链接指向哪里。** 指向 `github.com/...` 的链接给 GitHub 涨权重，对公司域名的 SEO 没用。awesome 列表按惯例链 repo，照办。目录站、registry 允许填 website 的，优先填公司域名上的项目页（如 `<公司域名>/oss/<slug>`）；没有项目页就填 repo，并在报告里注明“这条外链不给公司域名”。
3. **已提交 ≠ 已上线。** PR 已开、表单已交只记为“已提交”。PR 合并且列表里能看到条目、目录页公开可访问且 `href` 指向正确，才记为“已上线”。

## 流程

### 1. 项目底稿（先读已有信息，缺的再问）

repo URL、一句话定位（≤ 15 词英文）、类别（MCP server / agent / CLI / 库 + 语言）、star 数、首次提交日期、license、公司域名上有没有项目页、提交人的 GitHub 账号。

仓龄、star 数和 license 是很多列表的准入门槛。用 `gh api repos/<o>/<r>` 查 star 数和 license，首次提交日期要翻 commits 的最后一页（`gh api` 默认只拿到最近一页）。

### 2. 找 awesome 列表并检查活跃度

用 `gh search repos "awesome <类别关键词>" --sort stars` 加上 `references/channels.md` 里的种子列表。每个候选列表都要查以下几项，任何一项不过就跳过，并记下原因：

```bash
L=<owner/list>; R=<我们的repo名>
gh repo view $L --json isArchived,pushedAt                                     # 是否归档
gh api "repos/$L/commits?per_page=1" --jq '.[0].commit.committer.date'         # 默认分支最后一次提交（列表仓库基本等于最后一次合并）
gh pr list -R $L --state merged --search "sort:updated-desc" -L 20 --json mergedAt --jq 'map(.mergedAt)|max'  # 最近一次合并 PR
gh api "search/issues?q=repo:$L+is:pr+is:open&per_page=1" --jq .total_count      # open PR 的真实数量（gh pr list -L 会截断）
gh pr list -R $L --state open --search "sort:created-asc" -L 1 --json createdAt --jq '.[0].createdAt'  # 最老的 open PR
gh api "repos/$L/contents/.github/workflows" --jq '.[].name'                      # 然后逐个读 YAML 和它引用的脚本/配置；404 = 没配 CI
gh api repos/$L/contents/README.md -H "Accept: application/vnd.github.raw" | grep -i $R  # README 查重（超过 1MB 时必须加 raw 头）
gh search prs --repo $L $R --json number,state,author; gh search issues --repo $L $R --json number,state  # 已开的 PR/issue 查重
```

| 检查项 | 不过的情况 |
|---|---|
| 归档 | `isArchived: true` → 跳过 |
| 维护 | 最后一次提交和最近一次合并都在 90 天以前 → 跳过。如果没有任何合并记录（可能是维护者直接 push），以默认分支最后一次提交为准，并在记录里注明 |
| 提交入口 | 先确认这个列表收不收外部 PR：读 CONTRIBUTING 和 issue 模板，有些列表只收 issue（外部开 PR 会被拦）。按它的实际入口出草稿 |
| 积压 | 不作为跳过理由，但要把数量和最老日期如实告诉作者，不要折算成“要等几天”。只收 issue 的列表，看的是 issue 队列 |
| 准入门槛 | CONTRIBUTING、PR/issue 模板、CI 引用的脚本和配置（不能只看文件名）。star、仓龄、license、徽章、manifest 等要求不满足就跳过，并写明“补齐什么之后可以提” |
| 对口 | 同类项目放在哪个分类，我们就放哪个；找不到合适的分类就跳过，不要硬塞 |
| 重复 | README 已收录，或者已经有 open 的 PR/issue（不管是谁开的）→ 跳过，不要重复提 |

这一步只做检查和报告。修改我们自己的 repo（补 topics、改 README、加徽章等）属于另外的动作，要先问作者。

### 3. 写 awesome 条目草稿

严格照抄该列表现有条目的格式：链接写法、描述长度、句尾标点、emoji 和徽章。语言、部署方式这类图标按 repo 的实际情况选，不知道就查，不要猜。

- **分类**：同类项目分散在几个分类时，选和我们功能最接近的那一个，草稿里写明理由，让作者确认。
- **插入位置**：分类本身按字母序排，就按字母序插；分类本身没排序，就加在末尾。
- **PR 模板**：标题和正文按模板填，要勾选的项逐项确认，不能直接全勾。
- **自动化通道**：列表如果给 bot/agent 设了专用通道（比如标题加特定标记），不要用。这个 PR 是作者本人提交的。

每个列表单独出一份草稿。只收 issue 的列表就按它的 issue 模板写，模板里需要提交人本人确认的项留空，不要替他勾：

```
列表: <owner/repo>  分类: <section>  插入位置: <在哪两条之间>
条目: - [name](url) - Description.
PR 标题: ...
PR 正文: ...
```

### 4. 外链 / 目录站：先过筛选关

**先看 `references/directories.md`**：这是已经核实过、分好层的清单。按项目类型选层：所有项目都提第 1 层；AI/agent、MCP、skill 类项目再加对应的层；中文渠道看团队需不需要；发布日渠道按需。清单里标“未核实”的行，提交时顺便补全；超过 3 个月没核实的行，先确认提交页还在。

清单之外新发现的站，不看 DR（站点权重分），只过下面五项。查不到的项标“未查”，不能当作通过。通过的站补进 `directories.md`：

| 检查项 | 怎么查 | 判据 |
|---|---|---|
| 价格 | 打开提交页 | 免费入口包含哪些内容；加急、置顶、付费收录单独列出。零元任务不升级成付费 |
| 领域 | 看站内同类条目 | 有开发者、AI 或开源工具类目，而且我们的项目放进去不突兀 |
| 有没有人专门搜这个站 | `curl -s "https://suggestqueries.google.com/complete/search?client=firefox&q=<站名>"`（Google 搜索联想，不需要 key） | 联想词里出现“站名 + reviews / login / alternative / submit”这类品牌搜索，说明是真站；只联想出站名本身或无关词，就要警惕是农场站 |
| 近 7 天新页面有没有收录 | `site:<domain>` 配合 Google 的“过去一周”筛选，或抽一条最近收录的条目页去搜 | 新页面一周内能被收录，我们的条目才有机会被看到 |
| 同行有没有用 | 在目录站里搜 1–2 个同类优秀开源项目的名字；或者看同行 README 里的 “Featured on” 徽章 | 同行在这里有条目，说明渠道可信 |

另外，上线后要记录链接的 `rel`。`nofollow` 不代表失败，只是如实记下来；`noopener noreferrer` 不等于 `nofollow`。

### 5. 提交（永远用提交人自己的 GitHub 账号）

先运行 `gh auth status` 看当前环境，再选一种方式：

**A. 本机 `gh` 已登录提交人自己的账号（Claude Code / Codex / Cursor 的常见情况）**

把草稿逐条给用户看，用户明确说“提交”之后，agent 代为执行：
- 收 PR 的列表：`gh repo fork <list> --clone=false`，在 fork 里建分支，改那一行，然后 `gh pr create -R <list>`。
- 只收 issue 的列表：`gh issue create -R <list>`；如果用的是 issue 表单，就按表单字段拼好正文。

每确认一条才提交一条，不能一次确认就批量提交，每天不超过 3–5 个。提交后把链接写进第 6 步的记录。

**B. 没有 `gh`，或者登录的不是提交人本人（比如 Fleet 等云端 agent 用的是 agent 自己的账号）**

不要用 agent 的账号提交，改为给提交人发链接：
- **只收 issue 的列表**：发一个已经预填好内容的 issue 链接。提交人点开，检查一遍，勾选模板里的确认项，点 Create 就提交了。这个 issue 属于点开链接的人自己的账号。生成方法：
  ```bash
  python3 <本 skill 目录>/scripts/issue_link.py <owner/list> fields.json
  ```
  `fields.json` 的字段名取自列表 `.github/ISSUE_TEMPLATE/*.yml` 里每一项的 `id`，再加上 `template` 和 `title`。勾选框故意不预填，必须由提交人自己勾。
- **收 PR 的列表**：GitHub 不支持通过链接预填文件改动，只能发 `https://github.com/<list>/edit/<默认分支>/README.md` 这个网页编辑链接，同时告诉对方“在第几行、哪两条之间粘贴这一行”，并附上 PR 标题和正文。点开后 GitHub 会自动 fork，粘贴后点 Propose changes，再点 Create pull request，大约一分钟。
- 提交人把提交后的链接发回来，agent 再写进记录。

**目录站：agent 用浏览器工具自己提交，人只负责登录。**

- 开始前把通过第 4 步筛选的站点列给用户，用户批准这一批后，agent 逐个打开提交页，自己填表、上传 Logo 或截图、提交。批准过的站点不用每个再问一遍，超出这批的、要付费的，要另外问。
- 遇到注册、登录、邮箱验证、验证码，停下来请用户在浏览器里完成，完成后 agent 接着往下做。等用户的时候先去做下一个站，不要卡住。agent 不替人注册账号，也不输入密码。
- 网址字段优先填公司官网上的项目页，没有就填 repo。描述要按每个站的受众改写，不要全部用同一段。
- 提交后打开公开页或后台，核对产品名、描述、网址字段实际的 `href`。审核中的标记为“已提交”，公开页能看到且链接正确的才算“已上线”。
- 没有浏览器工具的环境（比如纯 CLI），就把站点和要填的内容列给用户，让用户自己去填。
- 密码、token、验证码一律不写进表格或日志。

### 6. 记录

每一个提交动作记一行，写进 `~/.oss-list-submit/submissions.csv`（表头见 `references/tracker-template.csv`，文件不存在就先拷一份）。第 7 步的监听脚本读的就是这个文件，所以“PR或表单回执链接”一栏要填完整的 PR/issue 链接。团队另有共享表的话，两边都记。

用了方式 B（发链接）的，提交人自己点完后不用回来贴链接，运行下面两条就能找到：

```bash
gh search prs "<owner>/<repo>" --json url,author,state ; gh search issues "<owner>/<repo>" --json url,author,state
gh search prs "<repo名> in:title" --json url,author,state      # 有些 PR 正文里的链接没被索引，标题再搜一遍；结果要人工确认是不是我们的项目
```

状态只用这几种：`草稿` / `已提交` / `已上线` / `被拒（原因）` / `跳过（原因）`。汇报时把各状态分开计数。**不要把已提交的数量说成新增外链数。**

### 7. 装定时监听（提交完 PR/issue 后）

先问用户要不要装（它会在本机常驻一个定时任务）。同意后运行：

```bash
bash <本 skill 目录>/scripts/install_watch.sh        # 默认每 6 小时检查一次；--uninstall 卸载
```

- macOS 用 launchd，Linux 用 crontab，只依赖 `python3` 和已登录的 `gh`，Claude Code、Codex、Cursor 都能用。
- 检测到这些变化时，会弹系统通知：PR 合并、issue 被处理、PR/issue 被关闭、维护者有新回复或 review。合并之后它会去读列表的 README，确认条目真的出现了，再把状态改成“已上线”。
- 想同时推到飞书或 Slack 群：在 `~/.oss-list-submit/config` 里写一行 `NOTIFY_WEBHOOK=<webhook 地址>`。团队共用一个群机器人的话，地址找管理这个机器人的人要。**webhook 地址谁拿到都能往群里发消息，不能写进 repo、skill 或提交记录。** 每条消息都以 `[oss-list-submit]` 开头，可以在机器人的安全设置里把它设成关键词。
- 想马上查一次：`python3 <本 skill 目录>/scripts/watch_submissions.py`，加 `--dry-run` 就只看不写。
- 收到“维护者回复了”要尽快回。维护者提了修改意见没人理，PR 通常会被直接关掉。

目录站的表单没有 PR 可以监听，一周后手动复查一次：页面有没有上线，`href` 和 `rel` 是什么。

## 文案规则（条目描述、PR / issue 正文）

维护者每天收到大量 AI 生成的 PR，一看到营销腔就会直接关掉。

- **条目描述**：一句话说清它做什么，长度和句式照抄相邻条目。写具体功能（“reads the current page, fills forms”），不写形容词。
- **禁用词**：revolutionary、seamless、powerful、cutting-edge、game-changing、next-gen、ultimate、effortless、supercharge、unlock、leverage、robust、best-in-class。
- **只写能核实的事实**：star 数要带日期；没有的用户数、下载量不要写。还在早期就写 early preview。
- **PR / issue 正文写 3–5 句**：加了什么、放在哪个分类以及理由、提交人和项目的关系（比如“I'm on the team behind X”）。不写 “I'm excited to share”，不加 emoji（列表要求的除外）。
- 写长文（比如发布帖）时，如果装了 anti-ai-slop-writing 之类的写作 skill，可以配合使用。本 skill 不依赖它。

## 常见错误

| 错误 | 正确做法 |
|---|---|
| 用 bot 账号一次给 20 个列表开 PR | 用提交人自己的账号，每条单独确认，分几天进行；云端 agent 只发预填链接 |
| 按 DR 从高到低挑外链站 | 只过第 4 步的五项筛选，DR 高不等于对口，也不等于有人看 |
| 目录站填的是 GitHub repo | 有公司项目页就填项目页 |
| 条目格式自己发挥 | 照抄相邻条目，按字母序插入 |
| 所有列表用同一句描述 | 按每个列表的风格和长度改写 |
| PR 开了就算完成 | 装第 7 步的监听；合并且 README 里能看到条目才算上线 |
| 往不对口的分类硬塞 | 跳过，并写下原因 |
