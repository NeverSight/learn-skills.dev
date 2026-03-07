---
name: qiaomu-music-player-spotify
description: |
  Spotify 音乐播放控制 + 5947 风格数据库。搜索、播放、暂停、队列管理、场景音乐推荐、风格查询与探索。

  USE THIS SKILL when user mentions:
  - Playback: "播放音乐", "来首歌", "放点音乐", "播放", "想听XX", "来点XX音乐"
  - Controls: "暂停", "继续", "下一首", "上一首", "音量", "正在播放什么"
  - Genre lookup: /genre, "查询音乐风格", "推荐音乐类型", "XX风格有哪些子分类"
  - Scene/mood: "适合深夜的音乐", "有活力的", "空灵的", "推荐一些XX特点的音乐风格"
  - Suno integration: 用 Suno 生成音乐但未指定风格时
  - /spotify
triggers:
  - "播放音乐"
  - "来首歌"
  - "放点音乐"
  - "播放"
  - "想听"
  - "暂停"
  - "下一首"
  - "上一首"
  - "现在播放什么"
  - "音量"
  - "最近听了什么"
  - "查询音乐风格"
  - "推荐音乐类型"
  - "适合XX的音乐"
  - "/spotify"
  - "/genre"
---

# Qiaomu Music Player (Spotify)

统一的音乐播放 + 风格查询 Skill。通过自包含的 Python 脚本直接调用 Spotify Web API，集成 RateYourMusic 5947 个音乐风格数据库。

---

## Part 1: Spotify 播放器

### 脚本位置
`~/.claude/skills/qiaomu-music-player-spotify/spotify.py`

### 运行方式
```bash
~/.claude/skills/qiaomu-music-player-spotify/spotify.py <command> [args...]
```

### 命令列表

| 命令 | 参数 | 说明 |
|------|------|------|
| `search` | `<query> [type] [limit]` | 搜索 (type: track/artist/album/playlist，默认 track) |
| `play` | `<uri或track_id>` | 播放指定曲目/专辑/播放列表 |
| `pause` | | 暂停 |
| `resume` | | 继续播放 |
| `next` | | 下一首 |
| `prev` | | 上一首 |
| `queue` | `<uri或track_id>` | 加入队列 |
| `now` | | 当前播放信息 |
| `show-queue` | `[limit]` | 显示队列 |
| `volume` | `<0-100>` | 设置音量 |
| `devices` | | 列出可用设备 |
| `recent` | `[limit]` | 最近播放 |
| `playlists` | `[limit]` | 我的播放列表 |
| `batch-play` | `<id1> <id2> ...` | 批量播放（播第一首 + 其余加队列） |
| `shuffle` | `<on\|off>` | 随机播放 |
| `repeat` | `<track\|context\|off>` | 循环模式 |

### 配置
- **默认设备 ID**: `b21721f49276638d9fddb0946f9d5936fa7a91fb`（MacBook Pro）
- **Token 文件**: `~/.claude/skills/qiaomu-music-player-spotify/.spotify_tokens.json`（自动刷新）
- **OAuth 重新授权**: 运行 `auth_setup.py`
- 所有输出为 JSON 格式，方便 AI 解析
- 如果遇到 401 错误，脚本会自动尝试刷新 token 一次

---

## Part 2: 风格数据库（5947 个风格）

### 数据结构

`~/.claude/skills/qiaomu-music-player-spotify/references/` 目录下的分层数据：

```
references/
├── _index.json          # 49个主分类概览（必读，13KB）
├── _meta.json           # 元数据和使用说明
├── main/                # 49个文件，每个主分类的直接子分类
│   ├── ambient.json
│   ├── rock.json
│   └── ...
└── detailed/            # 578个文件，有孙分类的子分类详情
    ├── dark-ambient.json
    ├── shoegaze.json
    └── ...
```

**数据统计**：
- 总风格数：5947
- 主分类：49（Rock, Jazz, Ambient, Electronic 等）
- 子分类：737（level: sub）
- 孙分类及以下：5161（sub-2/sub-3/sub-4）

**每个风格的数据字段**：
```json
{
  "name": "Dark Ambient",
  "url": "https://rateyourmusic.com/genre/dark-ambient/",
  "description": "Emphasizes an ominous, gloomy, and dissonant atmosphere.",
  "level": "sub",
  "parent": "Ambient"
}
```

---

## Part 3: 播放决策流程（核心！必须严格遵循）

```
用户说"播放/想听 XX"
  │
  ├── 路径B（优先！）：XX 能匹配下方播放列表映射？（风格名/场景关键词）
  │   → 直接用缓存 ID：spotify.py play spotify:playlist:<id>（无需确认）
  │
  ├── 路径A：XX 是具体歌手/专辑/歌曲？（如"播放涅槃的专辑"、"听 Bohemian Rhapsody"）
  │   → spotify.py search "<query>" track 1 → 拿 ID → spotify.py play <id>
  │
  ├── 路径D：用户要求播放多首特定歌曲？（如"最好听的3首冲浪乐"、"来5首经典爵士"）
  │   → AI 选出 N 首代表作 → 并行 search 获取所有 ID
  │   → spotify.py batch-play <id1> <id2> <id3> ...
  │   → 列出完整播放清单给用户看
  │
  └── 路径C：XX 是模糊需求/场景描述？（如"雨天的歌"、"适合写代码"、"心情不好"）
      → 必须走【模糊需求完整流程】，见下方 3c
```

> **路径 D 触发词**："最经典的3首XX"、"来几首XX"、"推荐5首XX的歌直接放"、"XX 风格的代表作来几首"

### 3a. 标准播放流程（路径 A）

```bash
# 1. 搜索
spotify.py search "Bohemian Rhapsody" track 1
# → 拿到 ID

# 2. 播放
spotify.py play <track_id>

# 3. 验证（可选）
spotify.py now
```

### 3b. 批量播放流程（路径 D）

```bash
# 1. 搜索多首（可以并行多次调用 search）
spotify.py search "Miserlou Dick Dale" track 1
spotify.py search "Wipe Out Surfaris" track 1
spotify.py search "Pipeline Chantays" track 1

# 2. 一次性批量播放（播第一首 + 其余加队列）
spotify.py batch-play <id1> <id2> <id3>
```

### 3c. 模糊需求完整流程（路径 C，最重要！）

当用户描述的是**场景、心情、氛围**而非具体歌手/风格时，必须走此流程：

**Step 1: 风格库查询**
- 读取 `_index.json` 扫描49个主分类
- 根据关键词匹配，读取 2-3 个候选 `main/*.json` 获取子分类详情
- 从风格库中筛选出 3-5 个最匹配的风格

**Step 2: 结合 AI 推荐具体音乐**
- 基于匹配到的风格，结合自身音乐知识，为每个风格推荐 1 首具体的代表性歌曲/专辑
- 推荐格式必须包含：风格名 + 推荐理由 + 具体歌手/专辑/歌曲名

**Step 3: 呈现方案，等待用户确认**
- 展示 3-5 个选项，每个选项包含：风格 + 推荐曲目 + 一句话推荐理由
- **必须等用户选择后再播放，不要自作主张直接播！**

**Step 4: 用户确认后，搜索并播放**
- 用户选了序号/名字后 → `spotify.py search` → 拿 ID → `spotify.py play` 播放
- 播放后用 `spotify.py now` 确认播放信息

**示例对话**：
```
User: 适合雨天听的歌

AI: 🌧️ 根据风格库匹配，雨天推荐这几个方向：

1. 🎹 Bossa Nova — João Gilberto《Getz/Gilberto》
   慵懒的巴西爵士，雨天咖啡馆标配

2. 🌫️ Ambient Pop — Sigur Rós《( )》
   冰岛氛围，空灵织体像雨幕一样包裹你

3. 🎸 Contemporary Folk — Iron & Wine《Our Endless Numbered Days》
   原声吉他低语，安静雨夜的陪伴

4. 🎷 Cool Jazz — Chet Baker《Chet Baker Sings》
   内敛克制的小号，配雨声刚刚好

5. 🌑 Dark Jazz — Bohren & der Club of Gore《Sunset Mission》
   黑色电影质感，阴雨天的完美配乐

想听哪个？说序号就行。

User: 2

AI: [spotify.py search "Sigur Rós ( )" album 1 → spotify.py play <album_id>]
🌧️ 正在播放 Sigur Rós —《( )》
不喜欢说"换一个"，我从其他选项里挑。
```

**关键原则**：
- 模糊需求 → **必须先推荐、等确认、再播放**，三步缺一不可
- 每个推荐必须具体到**歌手 + 专辑/歌曲名**，不要只给风格名
- 推荐要结合风格库数据（确保风格准确）+ AI 音乐知识（推荐具体曲目）
- 用户说"换一个"时，从剩余选项中挑或推荐新的

---

## Part 4: 风格 → Spotify 播放列表映射

当用户说"想听 Jazz"等风格关键词时，直接用内置映射播放，无需搜索。

| 风格/场景 | Playlist ID | 播放列表名 |
|-----------|-------------|-----------|
| Jazz | `37i9dQZF1DXbITWG1ZJKYt` | Jazz Vibes |
| Lo-fi / 写代码 | `37i9dQZF1DWWQRwui0ExPn` | lofi beats |
| Ambient | `37i9dQZF1DX3Ogo9pFvBkY` | Ambient Relaxation |
| Classical | `37i9dQZF1DWWEJlAGA9gs0` | Classical Essentials |
| Electronic | `37i9dQZF1DX4dyzvuaRJ0n` | mint |
| Rock | `37i9dQZF1DXcF6B6QPhFDv` | Rock This |
| R&B | `37i9dQZF1DX4SBhb3fqCJd` | Are & Be |
| Hip Hop | `37i9dQZF1DX0XUsuxWHRQd` | RapCaviar |
| Pop | `37i9dQZF1DXcBWIGoYBM5M` | Today's Top Hits |
| Chill / 放松 | `37i9dQZF1DX4WYpdgoIcn6` | Chill Hits |
| Focus / 专注 | `37i9dQZF1DX8NTLI2TtZa6` | Deep Focus |
| Sleep / 睡眠 | `37i9dQZF1DWZd79rJ6a7lp` | Sleep |
| Workout / 运动 | `37i9dQZF1DX76Wlfdnj7AP` | Beast Mode |
| Indie | `37i9dQZF1DX2Nc3B70tvx0` | Indie Pop |
| Blues | `37i9dQZF1DXd9rSDyQguIk` | Blues Classics |
| Country | `37i9dQZF1DX1lVhptIYRda` | Hot Country |
| Latin | `37i9dQZF1DX10zKzsJ2jva` | Viva Latino |
| K-Pop | `37i9dQZF1DX9tPFwDMOaN1` | K-Pop ON! |
| Punk | `37i9dQZF1DX0KpeLYR2IHH` | Punk Essentials |
| Metal | `37i9dQZF1DWTcqUzwhNmKv` | Kickass Metal |
| Synthwave | `37i9dQZF1DX6GJXiuZRisr` | Synthwave from Space |
| Bossa Nova | `37i9dQZF1DX4AyFl3yqHeK` | Bossa Nova |
| Surf Rock | `37i9dQZF1DX5hR0J49CmXC` | Surf Rock Sunshine |
| Reggae | `37i9dQZF1DXbSbnqxMTGx9` | Reggae Classics |
| Soul | `37i9dQZF1DWULEW2JjEkIS` | Soul Classics |
| Funk | `37i9dQZF1DWWvhKV4FBciw` | Funk Outta Here |
| Disco | `37i9dQZF1DX1MUPbVKMBel` | Disco Forever |
| Grunge | `37i9dQZF1DX0FOF1IUWK1W` | Grunge Forever |
| Post-Rock | `37i9dQZF1DX9bubh97wEfA` | Post-Rock |
| Shoegaze | `37i9dQZF1DX6ujZpAN0v9r` | Shoegaze is Dead |

> **兜底**：如果播放列表 ID 失效，用 `spotify.py search "<genre>" playlist 1` 搜索替代。

---

## Part 5: 场景关键词映射表

当用户描述场景/氛围时，AI 应该自动映射到合适的搜索关键词：

| 用户描述 | 匹配关键词 | 推荐方向 | 搜索词 |
|---------|-----------|---------|--------|
| 深夜、放松、冥想 | ambient, atmospheric, calm, soothing | Ambient, Drone, Space Ambient | ambient relaxing |
| 有活力、激烈 | energetic, fast, aggressive, intense | Punk, Hardcore, Drum and Bass | energetic upbeat |
| 暗黑、压抑 | dark, gloomy, ominous, dissonant | Dark Ambient, Black Metal, Industrial | dark ambient |
| 空灵、梦幻 | ethereal, dreamy, atmospheric, reverb | Dream Pop, Shoegaze, Ambient Pop | dream pop ethereal |
| 电子、科技感 | electronic, synthetic, futuristic, digital | Techno, IDM, Ambient Techno | electronic techno |
| 复古、怀旧 | vintage, retro, nostalgic, classic | Synthwave, Vaporwave, Chillwave | synthwave retro |
| 实验、前卫 | experimental, avant-garde, unconventional | Noise, Free Jazz, Musique Concrete | experimental |
| 写代码、工作、专注 | focus, concentration, productivity | Lo-fi Hip Hop, Post-Rock, Downtempo | lofi hip hop focus |
| 开车、路上 | driving, road trip, upbeat | Indie Rock, Synthwave, AOR | driving music road trip |
| 运动、健身 | workout, gym, energetic | EDM, Drum and Bass, Trap | workout music |
| 古典、优雅 | classical, elegant, orchestral | Classical, Chamber Music, Baroque | classical music |
| 爵士、慵懒 | jazz, laid back, smooth | Jazz, Bossa Nova, Smooth Jazz | jazz smooth |
| 抽烟、放松 | trip-hop, chill, jazz lounge, atmospheric | Trip-Hop, Jazz Lounge, Atmospheric | trip-hop chill |
| 做饭、家务 | jazz cooking, bossa nova, feel good | Jazz, Bossa Nova, Feel Good Pop | jazz cooking bossa nova |
| 伤感、雨天 | melancholy, sad, rainy day | Melancholy Piano, Sad Indie | melancholy piano rainy day |
| 派对、嗨 | party, dance, festival | EDM, Hip Hop Party | party dance edm |

---

## Part 6: 风格查询功能

### 6a. 快速查询（精确匹配）

**用户说**："查一下 Shoegaze"

**执行流程**：
```
Step 1: 读取 _index.json，检查是否为主分类
Step 2: 如果不是，用 Grep 在 main/*.json 中搜索
Step 3: 找到后，显示风格信息 + 链接 + 子分类（如果有）
```

**示例输出**：
```
🎵 Shoegaze
📝 Characterized by ethereal vocals buried beneath walls of distorted guitars...
🔗 https://rateyourmusic.com/genre/shoegaze/
📂 属于：Alternative Rock > Noise Pop > Shoegaze

💡 Shoegaze 有 3 个子分类：
  - Blackgaze（融合黑金属元素）
  - Nu-Gaze（现代复兴）
  - Dream Pop（更柔和的变体）
```

### 6b. 智能推荐（语义匹配）

**用户说**："推荐一些适合深夜、有点空灵的风格"

**执行流程**：
```
Step 1: 读取 _index.json，扫描所有49个主分类的描述
Step 2: 用关键词匹配（参考 Part 5 关键词映射表）
Step 3: 找到候选主分类后，读取对应的 main/*.json
Step 4: 根据描述进一步筛选子分类
Step 5: 返回 Top 3-5 推荐，带简短说明
```

### 6c. 层级探索（树状浏览）

**用户说**："给我看看 Ambient 下面都有什么"

**执行流程**：
```
Step 1: 读取 main/ambient.json
Step 2: 列出所有直接子分类（level: sub）
Step 3: 如果用户进一步询问某个子分类，读取 detailed/{subgenre}.json
Step 4: 显示完整的层级树
```

---

## Part 7: 播放控制速查表

| 用户说 | 执行命令 |
|--------|---------|
| "暂停" / "停" | `spotify.py pause` |
| "继续" / "播放" | `spotify.py resume` |
| "下一首" / "切歌" | `spotify.py next` |
| "上一首" | `spotify.py prev` |
| "音量设为50" | `spotify.py volume 50` |
| "现在放的什么" | `spotify.py now` |
| "播放队列" / "接下来放什么" | `spotify.py show-queue` |
| "最近听了什么" | `spotify.py recent` |
| "加入队列" | `spotify.py queue <id>` |
| "随机播放" | `spotify.py shuffle on` |
| "单曲循环" | `spotify.py repeat track` |

---

## Part 8: 与 Suno 集成

当用户要用 Suno 生成音乐但没指定风格时，主动触发风格推荐：

**执行流程**：
```
Step 1: 询问用户想要什么氛围/场景（或直接推荐热门风格）
Step 2: 使用智能推荐功能，给出 3-5 个风格
Step 3: 用户选择后，将风格名称传递给 suno-music-creator
Step 4: Suno 生成时，在 tags 参数中包含风格名称
```

---

## 读取优化策略

**原则**：渐进式加载，最小化上下文消耗

1. **必读文件**：`_index.json`（13KB）- 每次风格查询都要读
2. **按需读取**：
   - 精确查询：只读 1 个 main/*.json 或 detailed/*.json
   - 智能推荐：读 _index.json + 最多 3 个候选 main/*.json
   - 层级探索：逐层展开，用户点击才读下一层
3. **上下文预算**：单次查询通常 < 30KB

---

## 错误处理

### 找不到风格时
```
❌ 没有找到 "Qiaomu Style" 这个风格。

💡 可能的原因：
- 风格名称拼写错误？
- RateYourMusic 数据库中没有此风格

🔍 你可以：
1. 描述一下这个风格的特点，我帮你找相似的
2. 直接访问 https://rateyourmusic.com/genres/ 浏览完整列表
```

### 播放列表 ID 失效时
```bash
# 用搜索替代缓存
spotify.py search "jazz" playlist 1
# → 拿到新的 playlist ID → spotify.py play spotify:playlist:<new_id>
```

---

## 最佳实践

### DO
- 总是先检查 Part 4 播放列表映射，命中直接播（最快）
- 风格查询时先读 `_index.json` 建立索引
- 根据用户需求渐进式加载风格数据
- 推荐时给出 3-5 个选项，不要太多
- 输出时包含 RateYourMusic 链接
- `batch-play` 是批量播放核心：播第一首 + 其余加队列

### DON'T
- 不要一次性读取所有 main/*.json 和 detailed/*.json
- 不要只返回风格名称列表（要有描述和推荐理由）
- 模糊需求时不要跳过推荐直接播放
- 不要假设用户知道专业术语

---

## 更新日志

### v3.0 (2026-03-04)
- **重大重构**：从 MCP 工具迁移到自包含 Python 脚本 (`spotify.py`)
- 合并 `music-genre-finder` 全部内容（5947 风格数据库、播放列表映射、决策流程）
- 不再依赖任何 MCP 工具，纯 Python + Spotify Web API
- OAuth 2.0 token 自动刷新，无需手动管理
- `batch-play` 命令一次性批量播放

### v2.1 (2026-03-04)
- 新增路径D：批量播放多首歌
- 强制 deviceId 规则
- 扩展播放列表映射至 30+ 风格

### v2.0 (2026-03-04)
- 播放后端从 spogo + AppleScript 迁移到 MCP Spotify 工具

### v1.0 (2026-01-31)
- 初始版本：5947 个音乐风格查询、推荐、探索

---

## 作者

Created by 乔帮主 with Claude Code
Genre data source: https://rateyourmusic.com/genres/
