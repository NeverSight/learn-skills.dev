---
name: geo-sleuth
description: 照片拍摄地点定位（看图找地点 / 网络迷踪 / 图寻 / 推拍摄时间）。给一张或几张照片，先一条命令做完元数据、OCR、以图搜图（intake.py），把线索和候选记到候选盘（board.py）上由脚本排名、给下一步；查表线索用 clues.py；卫星图和街景都是"机器先排序、人只看前几名"（sat_scan.py、match.py）；每个结论都用真实数据核对，输出坐标 + 误差半径、证据图和分档置信度。Geolocate or chronolocate a photo with tool-verified reasoning — EXIF, OCR, reverse image search (Baidu/Yandex), lookup tables (plates, area codes, calling codes, driving side, territories), candidate board with likelihood ranking, sun and shadow math, OSM Overpass, CLIP-ranked satellite scan, DINOv2+SIFT-ranked street view matching, DEM skyline rendering. Use when the user shares a photo and asks 这是哪 / 在哪拍的 / 帮我定位这张照片 / 网络迷踪 / 几点拍的 / where was this taken / geolocate this.
---

# 迷踪 · geo-sleuth（v2）

目标：找到一个**经得起核对**的地点，每个结论都能指出用了哪条线索、跑了哪个命令、产出了哪个文件。

> 命令里的 `${CLAUDE_SKILL_DIR}` 指本 SKILL.md 所在目录（references 里的命令也一样）。Claude Code 会自动替换；其他 agent 先 `export CLAUDE_SKILL_DIR=<本目录的绝对路径>` 再跑（shell 不跨命令保留变量时，每条命令前都带上这句），或者直接把它换成这个路径。

工作方式分三层，先记住这个，再看流程：

| 层 | 谁做 | 工具 |
|---|---|---|
| 决策：候选有哪些、证据怎么算分、能不能排除、下一步扫哪 | **脚本**（候选盘） | `board.py` |
| 感知：读字、查表、卫星图上找目标、街景比对 | **脚本先算先排，人只看前几名** | `intake.py` `ocr.py` `clues.py` `sat_scan.py` `match.py` `geo.py bearings` |
| 判断：从画面里提线索、查表没有时提假设、在机器排好的前几名里裁定 | **你** | — |

方法来自 14 个网络迷踪博主视频、22 道题的拆解和多轮盲测对照；拆解笔记不随仓库发布。v1 的教训：规则写成散文不会被执行，同一版 skill 两次跑结果差很大；所以 v2 把能写成代码的规则都放进了 `board.py`。

## 硬规则（全程有效；标 ★ 的由 board.py 强制，你照做就行）

0. 用户说照片不是自己拍的，或画面里是私人住处、未成年人，先问一句用途再继续；提示里已写明来源或用途（评测题、出题人提示、用户明说是自己拍的）时不问，照常做到最细一级。
1. **不编核验**。"在地图上量过""街景对上了""±10 m"必须对应本次会话里实际跑过的命令和产出的文件。没跑过就写"未核实"。
2. **精度要有出处**：误差半径 ≤100 m，必须有两条独立约束的交会，或实景比对 ≥3 项不变特征。报机位前先跑一次自检：`pose.py project --horizon <海天线行号>` 会算出 pitch 该是多少、各地物按当前机位"应落在第几行"，和照片对账（目标的俯角 ≠ 相机的俯仰角；机位高程用 `terrain.py elev` 查，高差和画面俯角对不上就是机位错了）。
3. **找到唯一锚点就闭环**：后面的搜索和几何都从锚点出发，不再回到"湖水蓝绿""热带公园"这类泛化特征挑同类里最有名的地方。
4. **先算方位，再认构件**：照片里的塔、烟囱对应卫星图上哪个方块本身是解读。先用 `sun.py compass` 或已确认地标算出它在画面里的真实方位，再用 `geo.py bearings` 看候选机位周围哪个轮廓落在那个方位上；对不上时先做"原图/镜像""日出/日落"双模板，没核实就只降档不排除。
5. ★ **类别推断先列全**：从"山城""热带""IP 直辖市"推地区时，`board.py children` 把全部下级行政区加进候选，再用证据排。不默认主城，不按人口挑。
6. **元数据和提示都是假设**：EXIF、IP 属地、定位标签、出题人的话和画面冲突时以画面为准，不编故事去圆。IP 是 A 国、提示或制式指向另一大洲：`clues.py lookup territories <A国> --continent <洲>` 求交集。
7. **自洽性**：关键判断换一个裁剪或一组关键词重做一次，两次结果差几十公里以上就降档。
8. ★ **定不到点就给区间 + 缺什么信息**；候选是离散的几个时不取中点：`board.py report` 的主答案永远是第一名，其余进备选并写区分检验。
9. ★ **排除和确认用同一个标准**：`board.py exclude` 只接受 read/computed 级线索 + 算过的文件（`geo.py frame`、`terrain.py` 等的产出）；观察和推测只能 `evidence --against` 降权，似然比被夹在 1/3–3（推测）或 1/5–5（观察）。用"附近有 X"生成候选也是过滤，X 必须是画面里确认过的东西。校园、小区、街段这类细层候选同样要进盘：一批的用 `board.py add --from <poi.py --out / osm.py geom 的输出> --level area/road` 一次全进，不手挑；放弃一个就写 `evidence --against` 附比对图，`check` 会列出一条证据都没有的（等于没看过）；第三方数据的标签（市政清单的树种、校名精确匹配）只能降权，不能当排除理由（两例都是真值被这样手动跳过）。**排除范围必须 ≤ 证据范围**：区县/片区/路这类有延展的候选，`exclude` 要用 `--covers lat,lon[:lat,lon]` 写明证据覆盖到哪一段，覆盖不足一半会被脚本拒（在一条路的一个点上看过就整条排除，两例都栽过）。
10. ★ **人口、名气不是证据**；扫描顺序按"份额 ÷ 页数"（`board.py next`）：小城区先扫完，大城区放最后并设页数上限。

## 流程

不必走满：第 1 步识图直接命中时，跳到第 6、7 步确认。每一步的产出都要进候选盘。

### 第 1 步：一条命令做完第 0–3 步

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/intake.py photo.jpg --out-dir intake/ [--box x0,y0,x1,y1 ...] [--proxy socks5://127.0.0.1:10808]
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py init --photo photo.jpg
```

`intake.py` 一般 1–2 分钟，第一次运行要装依赖会更久：命令超时给够（10 分钟以上）或放后台跑。被命令超时打断时，识图子进程可能还在往 `rev/` 里写文件，但不会生成 `intake.md`，别当成已经跑完。

`intake.md` 里有：元数据、OCR 文字（放大/切块读出的标 pass=up/tile，是假设）、百度相似图片（来源站点计数 + 编号拼图）、识图标签分级计票、疑似小区/楼盘名、边缘图清单、失败项。然后你做四件事：

- **看图**：`edges/` 四边四角逐张看；`references/observe.md` 的清单过一遍；每条线索 `board.py clue "<文本>" --kind <类> --status observed|read|inferred|computed --file <放大图>`。状态要诚实：读出来的字是 read，"楼大概 8 层""路在上坡"是 inferred。
- **查表**：车牌、区号、电话国家码、行驶方向、海外领地 → `clues.py lookup <kind> <value>`；能落到行政区的直接 `board.py apply --kind plate --value 渝G --file <放大图>`（自动加候选和证据，同级其余候选只降权不排除）。
- **识图结果**：先打开 `rev/<名>_baidu_similar.jpg`（左上角是查询图），找同一个物体或同一处场景的近重复照片，有就按编号去 JSON 的 `similar[i].from` 看来源页；标签里的小区名、楼盘名、酒店名 → `poi.py "<名>" --city <城市> --out pois.json` 落坐标，同名的（几个校区、几家分店）`board.py add --from pois.json --level area` 全部进盘再核；截图务必打开看，命中帖子后把同组照片也看一遍。检索处按物体类型选（`references/search.md`）。
- **提示与元数据**：逐条登记为 inferred 线索，写明可信度；IP 属地只说明发帖时人在哪，发帖时间不是拍摄时间。

### 第 2 步：候选列全、证据打分、看下一步

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py children <上级行政区名>          # 直辖市 → 全部区县；国家 → 一级行政区（gazetteer.py 查 OSM，带 bbox）
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py evidence --clue K1 --for <候选A>:5 --for <候选B>:2 --against <候选C>:0.3 --why "…" --file <比对图>
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py rank
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py next
```

`next` 只会说两种话：
- **分不开**：按便宜到贵做区分检验，每项对全部候选一起做——查表 → 地形（平原 vs 山城，`tiles.py fetch --zoom 13` 或 `terrain.py`）→ 车辆涂装（`revimg.py --query "<城市> <颜色> 公交"`，从结果图读线路牌，按区县比车尾腰线）→ 市政设施（`baidu_pano.py sample --bbox <建成区> --n 24`）→ 水系/路网模板。都做过仍分不开：不要停，按它给的"份额 ÷ 页数"顺序扫。
- **可以缩圈**：先 `board.py urban <候选>` 把范围缩到建成区（或 `scan-bbox` 手动给），再 `board.py falsify <候选> --text "…"` 写证伪条件，然后进第 3 步。

环境粗定位的规则仍在：地形先于河宽和建筑色；物候必须配月份；罕见设施组合取交集；认得出的物种只当排除工具；只有地类时先用土地覆盖图缩到那类地块（`references/clues/`）。

### 第 3 步：选分支缩圈

| 手里有什么 | 做法 | 读 |
|---|---|---|
| 唯一锚点（楼、雕像、塔、景区建筑） | 锚点几何：视线交会、对齐线、切线、按拍摄高度筛楼 | `geometry.md` |
| 远山、天际线 | `terrain.py view` 渲染候选机位比对，只定一条视线，再找第二条约束 | `geometry.md` |
| 清晰影子、受光面、太阳在画面里 | `sun.py locate / when / facing / compass`：地带、时刻、朝向、画面里物体的真实方位 | `sky.md` |
| 线路号、铁路或输电线规格、大河 | 线状走廊 + 线变点：`osm.py route / crossings / along` | `corridors.md` |
| 两三种基础设施同框 | `osm.py near --report`、两类线交叉 `osm.py intersect`（折角只标注不删） | `corridors.md` |
| 线状设施 + 认不出的山，没有文字 | 设施沿线接高程算地平线，整个大区过滤 → 天际线 + 设施距离数值打分 → 前 3–5 名叠图 → 等间距构件定机位：`terrain.py scan --lines … --out hits.json --clusters-out clusters.json` → `terrain.py ridge photo.jpg --x0 … --x1 … --out ridge.json` → `terrain.py fit --hits hits.json --ridge ridge.json [--line … --line-dist …] --sheet top.jpg --photo photo.jpg`（精搜换 `--at lat,lon --radius 800 --grid 100 --zoom 13`）→ `imgprep.py piers photo.jpg --rows … --out cols.json --sheet piers.jpg` → `geo.py spacing --cols … --line … --span … --center lat,lon --ridge ridge.json` | `corridors.md` 4.3、`geometry.md` 7.4 / 7.7 |
| 街道格局清楚、没有锚点 | `osm.py street-scan` 筛路口 → `tiles.py sheet` → 街景 | `corridors.md` |
| 识图无近重复、没有文字，只有一组场景要素（路的规格 + 相邻地物 + 地貌） | **别先手挑点位**：把场景写成一句英文 query，`sat_scan.py grid --bbox <海岸带/走廊> --zoom 17 --cell 360 --query … --neg …` 让 CLIP 排序，人只看前 20–30 名缩略图；`grid` 优于 `points`，因为 OSM 的 `amenity=parking` 一类要素未必收全 | `search.md` |
| 画面里 ≥4 个已知位置的点（窗景、俯拍；平视拍远处塔桥码头也行，fix 掉 height） | `pose.py solve` 反解机位、朝向、高度；几处候选都说得通时 `pose.py check --cands` 逐个打分，稳健Δchi2 > 9 的才能 `board.py exclude --computed` | `geometry.md` 第 10 节 |
| 想用"画面里没有 X"排除 | `geo.py frame` 先算 X 该不该在框里、够不够大、会不会被挡；能排除的才 `board.py exclude --computed` | `geometry.md` 第 11 节 |
| 认得出设施类型（烘干塔、饲料厂、糖厂、水泥站） | 查产业分布 → `osm.py buildings` 枚举大建筑 → `sat_scan.py points` 排序 | `search.md` |
| 连锁品牌子品牌门店 | 先搜开业新闻稿拿地址，定位器只当候选池 → `osm.py along` + 街景抽样 | `search.md` |
| 机窗、无人机俯拍 | 航拍分支 | `aerial.md` |

### 第 4 步：卫星图找点——机器先排序

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/sat_scan.py grid --bbox <scan_bbox> --zoom 17 --preset track --multi-scale --top 30 --out sat.json --sheet sat_top.jpg --heat heat.jpg
uv run ${CLAUDE_SKILL_DIR}/scripts/poi.py "<区县> 学校" --city <地级市> --out schools.json      # 种子：--seeds schools.json 给附近格子加分
uv run ${CLAUDE_SKILL_DIR}/scripts/sat_scan.py points --points big.json --preset factory --out r.json --sheet r.jpg   # osm.py buildings / poi.py 的候选点排序
```

- 预设：track（操场跑道）、stadium、factory、silo、dam、bridge、quarry、solar、greenhouse、port；自定义 `--query`。实测：城区 300 多格里，OSM 标注的跑道一半以上进前 30 名；国内 OSM 空白的老城，学校操场也能排第一。**它是排序不是判定**：看前 20–30 格的缩略图，再按照片里的方位、形状核。
- 把画面描述翻译成俯视特征后再看：圆弧楼、八角亭屋顶、球场、车位和铁路垂直；高楼看楼底；影像有年代。
- 候选多时列候选表：一行一个点，一列一条照片里直接看得到的标准。
- 前 30 名都没对上：先回头看 `board.py check` 列的"被推测降权的候选"和证伪条件，再换预设或 z18，最后才扩大范围。

### 第 5 步：确认——街景也先排序

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/baidu_pano.py scan <lat,lon> --radius 300 --out panos.json                     # 国内；国外 gsv.py
uv run ${CLAUDE_SKILL_DIR}/scripts/match.py rank --query photo.jpg --panos panos.json --toward <地标lat,lon> --spread 15 --refine sift --top 10 --out m.json --sheet m.jpg
uv run ${CLAUDE_SKILL_DIR}/scripts/match.py rank --query photo.jpg --items around.index.json --render gsv --spread-headings -30,0,30 --out m.json --sheet m.jpg
```

- `match.py` 用 DINOv2 全局相似度粗排、SIFT 内点精排；实测同一地点不同年份的街景真值都进前 4。只打开前 10 名，比**不变特征**（楼的轮廓、窗位、阳台、电杆位置、路缘、山脊），不比车辆、招牌、树叶。到路 ≥2 项、到楼 ≥3 项。内点 ≥15 的一张都没有**不代表不对**：换季、老批次、照片在人行道而街景在路中间时，真值实测只有 5 个、0–8 个内点（两例），先打开前 10 张比不变特征，都不对再换 `--spread-headings` 或扩大 `--within`。全局分会被季节主导（花期批次不论在哪都排前面），和照片同季节的历史批次（`gsv.py sheet --date`）最好比。
- 全景点多时按日期和道路分组，`sheet --road <路名> --spread 60` 只看一条路；老批次视野更开阔。
- 没有街景不等于不能确认：`terrain.py view --photo` 比山脊；给候选设施找名字（OSM 名字、附近地名 + 当地语言的设施类型词），搜新闻、百科、官网配图比立面细节。
- 街景比照片早很多年时，以老建筑和永久结构为准。

### 第 6 步：定机位与输出

- 回头看：在对上的街景点转 180°，看拍摄者那一侧是什么。
- 机位要两条独立约束（`geo.py intersect` 视线交会、`geo.py line` 对齐线、`pose.py` 多点反解、拍摄高度、反向街景）；只有一条时，楼级置信度最高"中"。
- 朝向没有可量的影子时用受光面：`sun.py facing --lit left --shaded camera`。车里、船上、火车上拍的写出行进方向。

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py check                      # 出结论前：排除有文件吗、主答案有核实证据吗、哪些线索没用上
uv run ${CLAUDE_SKILL_DIR}/scripts/board.py report --merge result.json # 主答案=第一名；备选、排除、未用线索自动写进 result.json
uv run ${CLAUDE_SKILL_DIR}/scripts/evidence.py spec.json --out evidence.jpg
```

输出：
1. 一句话结论：地点 + 机位 + 朝向（+ 行进方向、拍摄时间，如适用）
2. 坐标：WGS84 和 GCJ-02（`geo.py convert`），**带误差半径**
3. 证据图（卫星图标机位和朝向扇形 + 比对图）
4. 推理链：线索 → 推断 → **实际跑过的命令和产出文件** → 范围
5. 分档置信度（下表）。**每一级分开评，自报档位取"中"及以上的最细一级**：楼级低不拖累片区级高
6. 排除过的候选和理由、备选和区分检验、没用上或没解开的线索（`board.py report` 生成）
7. 定不到点时：已确定到哪一级 + 还需要什么信息

| 级别 | 高 | 中 | 低 |
|---|---|---|---|
| 城市 | 文字、车牌、区号或确认过的锚点 | 多条独立弱线索一致 | 单条弱线索或只靠提示 |
| 片区 | 唯一的设施或地标在卫星图上对上 ≥3 项俯视特征（全候选区看完、没有第二处） | 候选区里最像的一处，还有没看完的候选 | 推测 |
| 路 | 实景对上 ≥2 项独有特征 | 格局一致，独有特征 1 项；**没有任何地面照片时**：片区级为高 + 方位自检通过 | 只有卫星图格局 |
| 楼 | 两条独立约束 + 实景 ≥3 项 | 两者之一 | 推测 |
| 楼层 | 两种参照交叉 | 单一参照 | 不给 |

## 预算与停止条件

- `intake.py` 算一次调用；识图换 3 组关键词无果就停，回清单找别的线索。
- **候选还分不开时不做任何逐个扫点**（`board.py next` 说"分不开"就先做区分检验）；便宜检验做完仍分不开，按它给的顺序扫，每个候选先扫建成区前 3 页。
- 扫描和确认一律先排序：`sat_scan.py` 看前 30 格，`match.py` 看前 10 张；前几名全不对再扩大，不是逐页翻。
- 用 OSM 枚举候选前先 `osm.py coverage`：偏少的区县会被静默排除，改用 `sat_scan.py grid`，并在结论里写明。
- 单个片区全景点 ≤500 个；3 个片区都没对上就停，`board.py report` 报告已确定到哪一级。
- 停之前 `board.py check`：被推测降权但没排除的候选按排序先回头看前 20 个。

## 运行环境

- Python 3.10+；一律 `uv run ${CLAUDE_SKILL_DIR}/scripts/xxx.py`（脚本头写了依赖；`match.py`、`sat_scan.py` 第一次会装 torch 并下载模型，走代理）。references 里的 `scripts/` 都相对于本 skill 目录。`revimg.py`/`intake.py` 需要本机 Chrome；`ocr.py` 在 macOS 用 Apple Vision。
- 代理地址以 `GEO_PROXY` 环境变量为准（`export GEO_PROXY=socks5h://...`），文中和脚本帮助里的 `127.0.0.1:10808` 是示例端口，换成你自己的。走代理：Google 卫星图、Google 街景、Overpass、Yandex、HuggingFace。直连：百度全景、百度识图、必应国内版、高程切片。`intake.py --proxy` 写 `socks5://`（Chrome 的写法）。
- 缓存写当前目录 `.geo-cache/`；候选盘是当前目录 `board.json`。脚本清单和数据源见 `references/data-sources.md`。
- macOS 没有 `timeout` 命令；zsh 里 `$var` 不分词，循环用 `bash -c` 或 `${=var}`。整省 Overpass 查询可能要几分钟，放后台跑。
