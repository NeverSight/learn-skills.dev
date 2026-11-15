---
name: jellyfin
description: Jellyfin 媒体库命名与服务器维护工具。当用户需要按照 Jellyfin 命名规范重命名电影/剧集文件夹和文件（rename-folder）、处理多部电影共用一个目录的平铺目录批量重命名（rename-flat，如 TopNNN. 排序前缀的 IMDB Top250 合集）、获取或校验 IMDB ID（verify 批量校验文件名 imdbid 与 OMDb 反查是否匹配并检测孤儿 nfo/图片、lookup 即席查号/反查）、只替换文件名中的 imdbid 标签（retag）、跨目录查重并对比画质给出留删建议（dupes）、整组搬移电影及旁挂文件（move）、处理 BT/字幕组风格媒体文件名（含点分隔、中英混合、质量标记如 1080P.X264.AAC）、清理本地旧海报/nfo 让位在线刮削（de-localart）、调用 Jellyfin API 刷新媒体库/诊断海报不更新（server refresh/images）、纠正错误刮削重新识别（server identify）、或比对 Jellyfin 元数据与文件名找出错绑（server check）时使用。
---

# Jellyfin 媒体库重命名工具

## 配置

旧字段 `[jellyfin].omdb_api_key` 请迁移到 `[jellyfin.omdb].api_key`；旧字段会给出迁移提示。

在 `agent_config.toml` 中添加（完整示例见 `agent_config.example.toml`）：

```toml
# Jellyfin 服务器（server / de-localart --refresh 需要）
# api_key 在 Jellyfin 控制台 → 高级 → API 密钥 生成
[jellyfin]
base_url = "http://localhost:8096"
api_key = ""

# OMDb（rename-folder / rename-flat 查 IMDB ID 需要）
# 从 https://www.omdbapi.com/apikey.aspx 免费申请
[jellyfin.omdb]
base_url = "http://www.omdbapi.com"
api_key = ""
```

配置文件搜索顺序：当前目录 → skill 目录 → git 根目录 → `~/.agents/agent_config.toml`。

## 执行方式

```bash
# 变量定义（SKILL_DIR 为本 skill 的绝对路径）
SKILL_DIR="/path/to/skills/jellyfin"
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" <command> [options]
```

## 命令

### clean — 批量清理空格

遍历指定目录下的所有子文件夹，去掉文件夹名和文件名中的空格，图片重命名为 `{视频名}-poster{ext}`。

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" clean /path/to/media --dry-run
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" clean /path/to/media --yes
```

### rename-folder — 智能重命名（一部电影一个子文件夹）

解析 BT/字幕组风格的文件夹名，查询 OMDb API 获取 IMDB ID，按 Jellyfin 标准重命名。

**输出格式**：
- 电影文件夹：`Movie Name (year) [imdbid-ttXXXXXXXX]`
- 电影视频文件：`Movie Name (year) [imdbid-ttXXXXXXXX].mkv`
- 剧集文件夹：`Show Name (year) [imdbid-ttXXXXXXXX]`
- 剧集视频文件：`Show Name S01E01.mkv`
- 图片：首图 `Name (year) [imdbid-ttXXXXXXXX]-poster.jpg`，其余图片按 Jellyfin 约定移入 `extrafanart/fanart1.jpg`、`extrafanart/fanart2.jpg` …
- 字幕：文件名与某视频相同（或仅多出 `.chs` 等语言标签）的字幕会跟随该视频改名，便于 Jellyfin 挂载；无法匹配任何视频的字幕保留原名

```bash
# 单个文件夹（自动检测是电影还是剧集）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-folder "/path/to/Movie.Name.2020.1080P" --dry-run

# 批量处理整个目录（--exclude 跳过无需处理的子目录，可多次使用）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-folder /path/to/Movies/ --batch --exclude Film --exclude H --dry-run

# 手动指定标题（当自动解析不准时）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-folder "/path/to/folder" --title "The Matrix" --year 1999

# 手动指定 IMDB ID（当 API 返回候选列表时使用）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-folder "/path/to/folder" --imdb-id tt0133093 --yes

# 强制指定为剧集类型
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-folder "/path/to/folder" --type series
```

### rename-flat — 平铺目录智能重命名（多部电影共用一个目录）

适用于无电影子文件夹、所有文件平铺在一个目录的场景（如 IMDB Top250 合集，
文件名带 `TopNNN.` 排序前缀）。

**分组规则**：按文件名公共前缀分组（`Top001.肖申克的救赎.The.Shawshank...` 中的
`Top001.`），组内含视频的视为一部电影；无前缀的文件按 stem（去掉 `-poster` 等
图片后缀）分组，无视频的孤儿组（如无前缀字幕）尝试并入视频 stem 为其前缀的组。

**输出格式**（`--keep-prefix` 时保留前缀，排序不能丢）：

```
Top001.肖申克的救赎 The Shawshank Redemption (1994) [imdbid-tt0111161].mkv
```

标题/年份从**视频文件名**解析（逻辑与 rename-folder 一致）。组内其他文件跟随：
- 图片：保留现有 `-poster`/`-backdrop`/`-landscape`/`-logo` 后缀关键字只换 stem；无后缀的默认加 `-poster`
- `.nfo`：同名 stem + `.nfo`
- 字幕：stem 与视频相同（或仅多 `.chn` 等语言标签）的跟随改名；同前缀单视频组内不完全匹配的字幕也会跟随并保留语言标签

API 结果缓存在目录下的 `omdb_cache.json`，失败/中断重跑不重复请求；OMDb 间歇
返回垃圾数据时用 `--no-cache` 强制重查（结果会覆盖缓存）。

```bash
# 预览（务必先 --dry-run 看终审清单）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-flat /path/to/IMDBTop250 --keep-prefix --dry-run

# 对可疑匹配手动指定 IMDB ID 后重跑（已成功的命中缓存，不重复请求）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-flat /path/to/IMDBTop250 --keep-prefix \
  --imdb-id Top003=tt0071562 --imdb-id Top057=tt0050083 --yes

# 跳过某些组
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" rename-flat /path/to/dir --exclude Top099 --dry-run
```

**终审清单**：`--dry-run` 和执行结束后都会输出全部「prefix → 新名」清单，
对可疑标题（双年份、年份与原名不符超出 ±2、相似度低）用 ⚠ 单独标注，未匹配的用 ✗。

### verify — 批量校验文件名中的 IMDB ID

人工凭记忆指定的 IMDB ID 极易记错（实战中 4 个全错：tt0406662 实际是 The Coiner，
Se7en 记成 tt0113227 实际是 Die Grube）。verify 扫描目录下所有带
`[imdbid-ttXXX]` 的视频文件/子文件夹，逐个用 OMDb `i=` 反查，标题相似度低或
年份偏差 >2 的列入可疑清单。结果写入 `omdb_cache.json` 缓存，重跑零成本。
同时检测孤儿媒体文件：nfo/图片的 stem 匹配不到目录下任何视频的列为垃圾
（典型来源：错误绑定时期残留的旧 imdbid 文件），仅列出不动手。

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" verify /path/to/IMDBTop250
```

### retag — 只改文件名中的 imdbid 标签

`server check` / `verify` 发现错绑后，文件名里的 imdbid 往往也要改。retag 只替换
`[imdbid-ttXXX]` 标签，文件名其余部分原样保留（不像 rename-flat 会按 OMDb 官方
标题重建整个文件名）；带同一旧标签的旁挂文件（图片/nfo/字幕）一起改。新 id 会先
经 OMDb 反查验证，不符则拒绝（`--force-imdb` 强制）。

```bash
# 目录批量：可传多个映射
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" retag /path/to/IMDBTop250 tt0113227=tt0114369 tt0406662=tt0381061 --dry-run

# 单文件：旧 id 从文件名读取
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" retag "/path/Top245.七宗罪 Se7en (1995) [imdbid-tt0113227].mkv" tt0114369 --yes
```

另外，`rename-folder` / `rename-flat` 的 `--imdb-id` 现在都会先经 OMDb 反查验证：
相似度低时警告并要求确认；`--yes` 非交互模式下直接拒绝采用，确认无误后需加
`--force-imdb` 强制使用。

### lookup — 即席查询（给 --imdb-id 查号）

```bash
# 反查 IMDb ID 对应的标题/年份（验证手动 id 是否记对）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" lookup tt2059171

# TMDb ID 补全成 IMDb ID
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" lookup tmdbid:335462

# 标题搜索：英文走 OMDb，中文走 Jellyfin RemoteSearch（TMDb），候选带 imdbid/tmdbid
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" lookup 战狼
```

### dupes — 跨目录查重 + 画质对比

按 `[imdbid-]` 标签和规范化标题（中文数字/标点归一化）在多个目录间找重复电影。
`--probe` 时对每组重复做采样哈希（头中尾各 1MB，SMB 上秒级确认是否同一文件）
和 ffprobe 画质对比（分辨率/编码/码率/音轨），并给出「建议保留哪份」。

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" dupes /path/to/2020 /path/to/2023 --probe
```

### move — 整组搬移（视频 + 旁挂文件）

把指定电影的视频本体和同 stem 的旁挂文件（poster/backdrop/nfo/字幕）一起移动到
目标目录；名称按 stem 匹配，同名子文件夹整个移动。与 dupes 联动做隔离。

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" move /path/to/2023 /path/to/2099 "战狼.HD1280超清国语中英双字" 情仇 --dry-run
```

### server refresh — 触发媒体库全量刷新

对指定库（库名或路径）调用
`POST /Items/{id}/Refresh?Recursive=true&MetadataRefreshMode=FullRefresh&ImageRefreshMode=FullRefresh`，
`--replace-metadata` / `--replace-images` 分别透传 `ReplaceAllMetadata=true` /
`ReplaceAllImages=true`。

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server refresh 电影 --replace-images
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server refresh /volume1/media/movies --replace-metadata --replace-images
```

### server images — 诊断「海报为什么没更新」

列出某目录下所有电影的 ImageInfos（类型、尺寸、大小、来源路径）：

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server images /volume1/media/movies
```

### server identify — 纠正错误刮削（重新识别）

关键认知：Jellyfin 首次刮削后会把 ProviderIds 缓存在条目上，之后
ReplaceAllMetadata 刷新也只沿用旧 ID，**改文件名里的 imdbid 不会触发重新识别**。
唯一正确修法是「识别」流程：本命令调 `POST /Items/RemoteSearch/Movie`
（`SearchInfo.ProviderIds.Imdb` + 文件名解析出的 Name/Year 提示），取
ProviderIds.Imdb 与目标一致的首个结果，再 `POST /Items/RemoteSearch/Apply/{itemId}`
（不替换现有图片）。

Apply 前会自动把同名 `.nfo` 改名为 `.nfo.bak`：否则 Jellyfin 会把当前（可能是
错的）元数据写回 nfo，而本地 nfo 优先级最高，会把 Apply 的结果再压回去。

```bash
# 单文件：imdbid 从文件名读取，也可 --imdb-id 覆盖
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server identify "/path/Top245.七宗罪 Se7en (1995) [imdbid-tt0114369].mkv" --dry-run
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server identify "/path/file.mkv" --imdb-id tt0114369 --yes

# 目录批量：每个文件从自己的文件名读取 [imdbid-ttXXX]（目录模式不接受 --imdb-id）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server identify /path/to/IMDBTop250 --dry-run
```

注意 ItemId 时效：文件改名会让 Jellyfin 删除旧条目、新建条目，ItemId 随之变化。
本命令每次都实时按路径查询当前条目，不缓存 ItemId；文件刚改名后库中可能还没有
新条目，需先 `server refresh` 扫库。

### server check — 诊断对账（DB 元数据 vs 文件名）

批量比对目录下所有视频的文件名与 Jellyfin DB 元数据，输出分类清单：

- **✗ 需要 identify**：IMDB 错绑（文件 id ≠ DB ProviderIds.Imdb，如文件「七宗罪」
  DB 名「Die Grube」）、无法确认绑定时标题完全对不上、年份偏差 ≥2（如
  12 Angry Men 刮成 1997 电视电影版）——逐条给出修复命令
- **⚠ 年份口径差异**：产地年 vs 发行年（千与千寻 2001/2003），正常仅标注
- **ℹ 译名差异**：IMDB 一致但译名不同（无间行者/无间道风云），无需处理
- **? 未入库**：文件未扫描进库，提示先 `server refresh`

```bash
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" server check /path/to/IMDBTop250
```

### de-localart — 本地旧图/.nfo 让位在线刮削

Jellyfin 本地图片优先级高于在线刮削，旧海报会永久挡住在线海报（前端表现为
视频截图缩略图）。本命令把目录（含子目录）下匹配 `-(poster|backdrop|landscape|logo|fanart)`
的图片（含 `extrafanart/` 内的）和所有 `.nfo` 移动到 `<目录>_oldart_backup/`
（默认）或 `--delete` 直接删除。

```bash
# 预览 → 执行 → 执行并自动刷新库拉取在线图
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" de-localart /path/to/movies --dry-run
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" de-localart /path/to/movies --yes
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" de-localart /path/to/movies --yes --refresh
```

### audit — 系列库体检（只读）

对电影库做全面盘点：命名规范、文件名 imdbid 与反查/DB 三方对账、nfo 一致性、
入库状态（多 CD/套装/BDMV 感知）、孤儿旁挂、系列缺席与重复候选、无系列文件夹的套装。
输出分级清单（✗ 硬错误 / ⚠ 待人工 / ℹ 仅标注），`--json-output` 落盘完整数据。

```bash
# 全库体检：服务器电影库路径自动映射到 ROOT 下同名子目录；默认跳过 IMDBTop250
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" audit /path/to/movie --json-output /tmp/audit.json

# 指定系列目录名与反查缓存（缓存可增量重跑，不重复反查）
uv run --project "$SKILL_DIR/scripts" "$SKILL_DIR/scripts/jellyfin_tool.py" audit /path/to/movie \
  --series-dir 系列电影 --cache ~/.cache/jellyfin_audit.json
```

要点：
- 只读不改任何文件；反查走服务器 RemoteSearch（与 OMDb 配额无关）
- 元数据全量刷新（`server refresh --replace-metadata`）可能让残留 nfo 回压 DB——
  大刷新之后重跑 audit 可抓这类回归
- 跨语言（中文文件名 vs 英文反查名）无法字符串比对时标 ⚠ 人工核对；
  DB 刮削名与文件名相似度 ≥0.6 视为绑定正确

## 典型工作流

1. **先预览**：总是先用 `--dry-run` 查看解析结果和终审清单
2. **清理噪声文件夹名**：文件夹名若混入站点广告（如「xxx.电影港 地址发布页 www.dygang.me 收藏不迷路」），中文名会被整段带入新名称，先 `mv` 清理成干净的中文标题再 rename-folder
3. **处理候选列表**：若 API 返回多个候选，从列表选择正确的 IMDB ID 后用 `--imdb-id` 重试
4. **指定 IMDB ID 时同时给 --title/--year**：OMDb API 偶发超时，`--imdb-id` 查询失败时会回退到 `--title/--year`，同时提供可保证回退名称也正确
5. **批量处理**：使用 `--batch`（rename-folder）或 rename-flat 时，失败的条目会在末尾汇总，逐一用 `--imdb-id` 补处理；rename-flat 有 omdb_cache.json 缓存，重跑不重复请求
6. **确认执行**：预览无误后去掉 `--dry-run` 加 `--yes` 执行
7. **海报不更新**：先 `server images <路径>` 看 Jellyfin 实际用的是哪张图；若是本地旧图挡住了在线刮削，用 `de-localart` 移除后 `server refresh --replace-images`

## 教训（IMDBTop250 平铺目录实战）

- **本地图片/.nfo 会压制在线刮削海报**：Jellyfin 本地图片优先级高于在线刮削，
  旧海报会永久挡住在线海报（前端表现为视频截图缩略图）。要让在线海报生效，
  必须先用 `de-localart` 移除本地图，再刷新库。
- **OMDb 脏数据的识别特征**：同一 api_key 会间歇返回垃圾数据。可疑特征包括
  标题含 `(YYYY) (YYYY)` 双年份、含 `/`（会生成非法路径）、`Making of`、
  `Unmasked`、`Live on Stage` 类字样；这些年份容差 ±2 外的候选会被自动排除/降权，
  命中结果在终审清单中以 ⚠ 标注。文件名开头的续集序号（`2 The Godfather Part II`、
  `5- Star Wars V-`）和尾部剪辑版标记（DC/SP/EXT/UNRATED/ReCut/Redux）会在搜索前自动清洗；
  OMDb 年份常比文件名年份 +1（美国上映年 vs 产地年），±2 内视为正常。
- **平铺目录的分组规则**：`TopNNN.` 这类排序前缀是分组依据，重命名时务必加
  `--keep-prefix` 保留，否则合集顺序丢失；无前缀文件按 stem 分组，字幕等孤儿文件
  只有 stem 能匹配上视频时才会跟随改名。
- **影史名片直接手动 `--imdb-id` 最快**：Top250 这类名字的搜索结果候选多、
  重拍/同名干扰大，逐部调试搜索词不如查好 IMDB ID 一次性
  `--imdb-id TopNNN=ttXXXX` 传入，配合缓存重跑零成本。
- **手动 IMDB ID 必须验证（血的教训）**：人工凭记忆指定的 4 个 IMDB ID 全是错的
  （tt0406662 实际是 The Coiner；Se7en 记成 tt0113227 实际是 Die Grube，正确是
  tt0114369）。`--imdb-id` 现在一律先 OMDb 反查比对，批量存量用 `verify` 体检。
- **ProviderIds 缓存导致"永远刮不回来"**：Jellyfin 首次刮削后把 ProviderIds 缓存在
  条目上，ReplaceAllMetadata 刷新也只沿用旧 ID；改文件名里的 imdbid 不会触发重新
  识别。唯一修法是 `server identify`。
- **nfo 回压坑**：identify Apply 前必须移走同名 .nfo，否则 Jellyfin 把当前（可能是
  错的）元数据写回 nfo，本地 nfo 优先级最高，会把 Apply 结果再压回去（实战踩过：
  Apply 成功 → 几分钟后被旧 nfo 覆盖回脏数据）。`server identify` 已自动处理
  （改名为 .bak）。
- **ItemId 会失效**：文件改名触发 Jellyfin 删除旧条目、新建条目，ItemId 随之变化。
  所有按 ItemId 操作的流程（identify/refresh）必须在改名后重新按路径查询当前
  ItemId，不能复用改名前缓存的。
- **RemoteSearch 首结果可能不带 Imdb**：按 IMDB ID 搜索时，部分提供商（如 TMDb
  中文条目）返回的结果 ProviderIds 里没有 Imdb，盲目取第一个会绑错来源——
  `server identify` 会优先选 ProviderIds.Imdb 与目标一致的结果。
- **对账先看 IMDB 再看名字**：DB 名与文件名中文名对不上时，若两边 IMDB ID 一致，
  只是译名差异（无间行者/无间道风云），不是错绑；IMDB 不一致才是真正的错误绑定。

## 教训（2020/2023/2025/2026 批量重命名实战）

- **中文质量词会粘进中文标题**：BT 命名如「真实的谎言.BD中英双字1024高清」，CJK 提取后
  中文名变成「真实的谎言中英双字高清」，搜索必挂。工具内置中英双侧噪声剥离
  （CJK_NOISE/ENG_NOISE），包括国粤日三语、双字幕、精译版、（美）地区标记、复制（1) 等变体。
- **OMDb 会 401 熔断**：免费 key 每日 1000 次，大批量必然打爆。工具在 401/网络失败时
  自动熔断降级到 Jellyfin RemoteSearch（TMDb 支持中文），且熔断期的「未找到」不写缓存。
- **RemoteSearch 请求不要带年份**：服务端按年过滤太死，而文件名年份常是下载/封装年
  （「2013终极神差」实为 1997 的 The Postman）。年份只在本地评分做偏好。
- **TMDb 中文名 ≠ 常见中文名**：让子弹飞/十二猴子 vs 12只猴子、料理鼠王 vs 美食总动员、
  被解救的姜戈 vs 被解放的姜戈——比对要做中文数字转换（十二↔12）和标点规范化
  （本杰明·巴顿奇事）。相似度 ≥0.7 的异译名会采用但标 ⚠，更低的拒绝进人工清单。
- **目录名年份只是整理归类**，与电影发布年份无关，不要拿它过滤候选（用户明确纠正过）。
  同名不同年的歧义（飞行家 2004/2025、萤火虫之墓 1988/2008）只能靠人工或覆盖表定夺。
- **记忆里的 IMDB ID 极不可靠**：本次人工给的覆盖 id 经服务器反查校验，记错率超过 20%
  （tt0366540→tt0366548 快乐的大脚、tt0319062→tt0318462 摩托日记等）。任何手动 id
  都必须过 `--imdb-id` 的反查验证。
- **macOS/SMB 的 `._` AppleDouble 垃圾文件**会被当成独立电影组，浪费查询还制造重名冲突——
  分组时直接排除。
- **多 CD 资源**（cd1/cd2/disc1）自动堆叠为 `片名 (年) [imdbid-x] - cd1.mkv`，
  无碟片标记的 sample/花絮/不同版本一律跳过不碰，防止同名覆盖。
- **文件名自带的 `[tmdbid-…]`/`[imdbi-…]`（拼写变体）标签会直接复用**：tmdbid 经
  RemoteSearch 二段补全成 imdbid，不再浪费一次搜索。
- **dry-run 永远不交互**：覆盖 id 验证不通过时预览只标注不拦截，避免批处理卡死在提示符上。

## 教训（系列目录体检与修复实战 2026-09）

- **Refresh API 不入库新文件**：`server refresh`（POST /Items/{id}/Refresh）只刷新已入库条目；
  改名/移动后的新条目要等「扫描媒体库」任务——用 POST `/ScheduledTasks/Running/{taskId}` 触发
  （任务可能排队约 20 分钟才执行，轮询 DB 路径确认入库完成）
- **SMB 冒号映射 U+F022**：macOS 经 SMB 写入的文件名中 ASCII `:` 在 NAS 端存储为 U+F022，
  DB Path 与本地路径字符不同。所有按路径比对的操作（server check、identify 找条目、自制对账
  脚本）必须先把 U+F022 归一化为 `:`；`server identify` 对含英文冒号的文件名会"找不到条目"
- **手动合集（BoxSet）不自愈**：改名/删除后合集仍引用旧 ItemId——新条目用
  POST `/Collections/{id}/Items?Ids=` 补入、旧引用用 DELETE 移除；错绑年代的错误 ID 会把电影
  挂进别人的合集（如人鱼大海战挂进星球大战合集、纳尼亚1 挂进杀死比尔合集），修完 ID 后要清理合集
- **verify / server check / dupes 都只扫顶层**：系列文件夹（多部电影平铺一组）要逐目录调用；
  dupes 按规范化标题匹配，对 BT 噪声名无效——先重命名再查重
- **蓝光原盘套装是三层结构**（套装盒→电影目录→视频），浅层扫描看不见；一个目录装多部电影
  （如 AvP 与 AvP2 同目录）必须拆分成每部一个目录
- **TMDb 反查标题语言不定**（中英皆有可能）：中文文件名 vs 英文反查名无法字符串比对，降级为
  人工核对并用 DB 刮削名佐证；标题不符且 DB 同名 → "nfo/DB 一致地错绑"
- **纯数字子串误匹配**：标题比对剥离 CJK 后只剩数字会误判（'6' in 'big hero 6' 把电锯惊魂6
  判成超能陆战队）——剥离后长度 <3 的串不参与子串匹配
- **时长探针消歧**：无年份/未标号文件用 ffprobe 时长定身份（功夫熊猫 92min=第1部、勇敢者的
  游戏 104/101min=Jumanji/Zathura、超人 129min=2025 版）；但最终身份仍要 ID 反查验证——
  文件名标签不可信（分歧者1 被错标成分歧者2 的 ID，139min 正片长度才是真相）
- **元数据全量刷新**：ID 修对后 `server refresh <库> --replace-metadata --replace-images` 可统一
  更新名称/海报——"ProviderIds 沿用旧 ID"的特性在 ID 已正确时是优点
- **体检工作流模板**：审计（ID 反查 + DB 对账 + 时长消歧 + 孤儿检测）→ 批量重命名 → 逐对
  dupes --probe 定去留 → move 缺席项 → 扫描任务入库 → identify 错绑 → 孤儿清理 → 合集对账。
  审计驱动脚本样例（复用本工具函数、RemoteSearch 反查缓存、并发查号）见 motoko 仓库
  outputs/jellyfin_audit/audit.py

## 修复工具链总结

定期体检：`audit` 一条命令全库盘点（命名/绑定/入库/孤儿/缺席/无文件夹套装）。
上游防止制造问题：`--imdb-id` 反查验证 + `--force-imdb` 兜底；`verify` 批量体检存量
（含孤儿媒体文件检测）。
出问题后的修复链：`server check` 对账找错绑 → `retag` 修正文件名里的 imdbid（只换
标签不动其他）→ `server identify` 重新识别 → `server refresh` / `de-localart --refresh`
刷新拉图。

## 支持的文件格式

- 视频：`.mp4` `.mkv` `.avi` `.wmv` `.mov` `.ts` `.m2ts` `.flv` `.rmvb`
- 图片（poster/fanart）：`.jpg` `.jpeg` `.png` `.webp` `.gif` `.tbn`
- 字幕：`.srt` `.ass` `.ssa` `.sub` `.vtt`（能匹配到视频的跟随视频改名，其余保留原文件名）
