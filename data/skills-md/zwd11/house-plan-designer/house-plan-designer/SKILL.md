---
name: house-plan-designer
description: 把用户给的户型图（图片：房产平台 / 家装设计平台户型图、售楼处户型图、手绘带尺寸的平面图；CAD 图纸：设计院 / 装修公司导出的矢量 PDF、DXF、原始结构图、建筑平面图，黑底 CAD 截图）自动还原成可交互的装修设计器网页（单文件 HTML，2D 平面 + 3D 鸟瞰/漫游 + 家具布置 + 水电/吊顶/铺装/拆改图层 + 电路 / 水管 / 网线自动排布 + 报价 + PDF 施工图），初始户型就是这张图。触发词：户型图生成设计器、户型图转 3D、把户型图做成网页、CAD 图纸转设计器、DXF/PDF 户型图、原始结构图、户型还原、做一个装修设计网页、户型图 2D/3D 展示、电路布线图、水电管线排布、floor plan to 3D。
---

# 户型图 → 装修设计器网页

产出一个单文件 HTML，双击离线打开：界面和功能就是完整的“户型装修设计器”，只是示例户型换成了用户这张图。
模板 `assets/template.html` 由设计器项目打包而来（源码与本 skill 仓库：<https://github.com/ZWD11/house-plan-designer>），**不要改模板**。
你要做的只有一件事：写出准确的 **HouseSpec（户型描述 JSON）**，格式见 `reference/spec-format.md`（**动手前必读**）。

## 环境（首次）

- Python：`pip install numpy pillow opencv-python scipy pymupdf ezdxf pypdf`（scipy 给 rectify.py 拟合透视用）；Node：在 `scripts/` 下 `npm install`（只装 puppeteer-core）。
- Windows / macOS / Linux / 云端容器通用：浏览器由 `scripts/browser.mjs` 自动找（`CHROME_PATH` → 系统 Chrome / Edge / Chromium → Playwright 缓存），root / 容器自动 `--no-sandbox`；没有显卡时验收自动进慢速模式。细节、npm 源、无显卡怎么验收见 `reference/env-cloud.md`。

## 0. 开工前先问清（列成「待确认清单」，交付时再集中列一次）

1. **一比一还原**图上所有内容（家具、柜子、洁具、符号、电箱）再补没有的，还是只照图放主要家具、其余补最优搭配？默认一比一。
2. **公共区**（电梯厅、楼梯间、强弱电井、风井、管井）还原不还原？默认还原墙体和设备、不布家具。
3. 图上没标的参数：**层高、楼板厚、看不出窗台高的玻璃 / 窗**。问不到就按常规估，写 `heightFrom: "estimated"`、洞口 `unsure`，设计器「批注」页会提醒用户。
4. 两张图（原图 + 设计图）时：结构以哪张为准（默认墙按原图、家具按设计图，见 `route-dual.md`）。
5. 图上**不认识的符号**列出来问，不要静默跳过。

## 1. 选识别路线

| 输入 | 路线（读对应文件） |
|---|---|
| 户型图、截图、扫描件、只有位图的 PDF（`fitz` 200dpi 渲成 PNG） | `reference/route-image.md`：**先 rectify.py 按尺寸链拉正**（手机拍照 / 拍屏幕的透视、扫描歪斜、图本身比例不均都去掉），再 analyze.py 识别 |
| **黑底 CAD 截图**（模型空间截屏，彩色线） | `route-image.md`「黑底 CAD 截图」：cadshot.py 分色 + 自动找轴网定比例 → `analyze.py --wall-color cyan`；尺寸数字用 `dimocr.py` 读 |
| CAD 矢量 PDF（放大不糊，`get_drawings()` 几千个图元）、DXF | `reference/route-cad.md`：cadvec.py，尺寸按标注数字精确到 mm |
| cadvec 报“没认出墙厚” / 墙只认一半 / 数字炸成线条 / 一页一层的多页 PDF | `route-cad.md`「兜底」：cadpair.py（按线色线宽分层、平行线配墙、灰块认柱、多页共用原点） |
| 一页并排几层 / 描边墙在每个交接处断开（量房软件） | `reference/route-building.md`：cadsplit.py |
| 装修公司整套“家具布置图”DXF（几张图、块套块、乱码） | `reference/route-dxf-layout.md`：dxf_prepare + dxfinventory + dxfaudit |
| **原图 + 装修平面布置图两张图**（墙按原图、家具按设计图） | `reference/route-dual.md`：dimticks.py + align2.py 自动对位 |
| DWG | 让用户另存 DXF / 导出 SVG（最准），再走上面 CAD / 整栋楼路线 |

楼盘类型的补充：多层 / 复式 / 楼梯 → `route-building.md`；写字楼、培训、核心筒 → `route-office.md`；独栋别墅（车库、庭院、挑空、电梯）→ `route-villa.md`。
CAD 画法、**平面布置图图例**（三次实战读错的 30 个符号）、结构形式与承重判定 → `reference/cad-conventions.md`（**走 CAD 路线或图上有家具时必读**）。

## 2. 读图：先出「图上符号 → 建模」清单

逐块放大看全图（拿不准放大 4 倍），记下：总尺寸和**每一道**分段尺寸链、房间名、门（开向、门轴、门外是不是户内）、窗型、承重墙 / 柱 / 烟道 / 管井 / 立管 / 地漏、电箱表箱、空调位百叶、指北针、标注面积，以及每一件家具和设备符号。
把它整理成表（符号、位置、数量、对应 key / 做法），交付时附上（见 `reference/furnishing.md`）。图没有任何尺寸时问用户要一个已知尺寸，交付时说明比例是估的。

## 3. 写 HouseSpec

用 Python 生成脚本写（参考 `reference/example-gen*.py`），不要手写 JSON；识别脚本出的 `draft.json` / `building_draft.json` 读进来再补改，不要重写墙。
- 像素 → 毫米用 `axismap.Axis` 按标注定位，不要整体乘一个比例（`route-image.md`）。
- 尺寸链全部写进 spec 的 `dims` / `expectDims`，check 自动逐刻度对账（`workflow-check.md`）。
- 图上标了房间面积的，每个房间写 `area`（㎡），check 报「面积对不上」「房间合并」（`spec-format.md`「房间 rooms」）。
- 承重按结构形式判断，推断的写 `bearingFrom: "inferred"`；拿不准的写 `comments`（`spec-format.md`「批注与待确认」）。
- **生成脚本里注释一律独占一行，不用行尾注释**：用脚本替换代码时把注释插进行中间会吞掉后半行（实战里静默少过一面墙）。build.py 墙数比上次少会报 `[warn]`。

## 4. 生成并自查（循环直到 0 error 0 warn）

```bash
python scripts/build.py <工作目录>/spec.json -o <工作目录>/check.html
node scripts/check.mjs <工作目录>/check.html <工作目录>/check
```

逐项看 `report.json`（悬空墙端、被吞的墙、斜墙、丢掉的门窗、房间面积、`dimIssues` 尺寸链超差、`dimConflicts` 图纸自相矛盾、`issues`），一定要看 `overlay.png` / `plan2d.png` / `view3d.png`。细则见 `reference/workflow-check.md`。
**交付前固定跑五个对账**：墙体正向 `wallaudit.py`（玻璃 / 洞口 / 柱认错）、**墙体反向 `coverage.py`**（原图有、模型没有的漏墙，墙面偏位，一致度 ≥ 98%）、尺寸链 `dims`、**门开向 `doorcheck.py`**、家具 `furnoverlay.py` 叠图 + 设计器自查的摆放检查（窗帘活动区、推拉门轨道、高柜挡窗）。房间写上图上标的面积 `area`，自查逐间对账。用户说“整栋重新检查”时跑全套，不只修指出的那一处。
用户指出某处 3D 不对时先 `node scripts/closeup.mjs 设计器.html x y 方向 out.png` 拍近景再改。

## 5. 布置家具、家电和水电（默认要做）

原图画了的一比一还原（类型、位置、尺寸、朝向），同时门扇打得开、每扇门都有 ≥ 700 通道；没画的按房间功能补全套家具家电；`autoElec: true` 自动布水电点位和管线。
读图要点、家具库（含新增的立管 / 空调外机 / 百叶 / 表箱 / 斜角开放格 / 模块沙发 / 飘窗台 / 摆件 / U 形橱柜 `kit.d2` / 无门挂衣区 `hangOpen` / 双跑扇形楼梯 `stairDogleg`）、按现实装修的常理摆、水电规则 → `reference/furnishing.md`、`reference/mep-rules.md`。
吊顶：每个房间写 `ceil`（平顶 / 边吊 / 回字叠级 / 悬浮 / 铝扣板 / 木饰面，灯槽自动放灯带，窗帘盒、石膏线），局部吊顶造型用 `ceilZone*`；
灯带 / 磁吸轨道 / 线性灯写成带 `pts` 的 `elec`；中央空调、新风、庭院场地（草坪、碎石、水景、花境）等新家具 key 见 `reference/spec-format.md`。
非矩形的家具 / 柜子（斜墙夹角里斜切一端、梯形台面）写 `quad` 揉捏变形；图上画了筒灯阵列或用户给了灯距 / 离墙距离，房间写 `lighting`（见 `spec-format.md`）。
图上有、库里没有的异形造型：用 `free*` 自由模型拼，或交付时告诉用户在设计器的「造型」工作台里（草图 → 推拉 / 旋转 / 放样 / 布尔）做。
**`[error]` 和 `[warn]` 必须清零才能交付**（用户把“检查”页的橙色标记当错误）；确实改不掉的（原图就这么画）交付时逐条说明。

## 6. 交付

```bash
python scripts/build.py <工作目录>/spec.json -o <图片同目录>/<户型名>-装修设计器.html --zip
node scripts/qa.mjs <户型名>-装修设计器.html <工作目录>/qa --lite --quick      # 全功能验收；无显卡自动慢速模式
python scripts/qa_files.py <工作目录>/qa                                        # 导出的文件能不能打开（0 个文件 = 失败）
node scripts/elecaudit.mjs <户型名>-装修设计器.html                               # 水电逐房间审计：灯 / 开关 / 插座 / 关联 / 高度 / 门边位置，✗ 必须为 0
```

- qa 全部通过（⚠ 未验证的项人工看截图）才能交付，**一定人工过一遍 `qa/shots/`**。验收参数、判定规则、不要和渲染同时跑等见 `reference/delivery.md`。
- 交付给用户：HTML 路径 + zip（HTML、原图、生成脚本、spec、截图，用户问“怎么下载”就给它）、`plan2d.png` / `view3d.png`、**待确认清单**、五个对账结果（含 coverage 一致度）、「图上符号 → 建模」表、和原图可能不一致的地方、比例是否估算、承重判断依据；用法说明见 `delivery.md`。

## 识别回归基准

改了识别 / 对账脚本（analyze、rectify、wallfit、coverage、doorcheck）之后跑：
`python scripts/bench.py --root <放 *_design 案例的目录> --out <同目录>/_bench`——用验收过的户型当标准答案，量墙召回 / 准确 / 中线误差、一致度、门弧认出率，和上次比 ↑↓。变差的不要交。

## 更新模板

设计器项目改了功能后，在项目目录 `npm run skill:sync`（打包并复制到本 skill 的 `assets/template.html`，同时更新 `reference/catalog-sizes.json`）。
读取预设户型的代码在项目 `src/model/spec.ts`（`planFromSpec`、`window.__PRESET__`）和 `src/app.ts`（`initApp` / `samplePlan`）；自查规则在 `src/checks.ts`，自动水电在 `src/model/autoelec.ts`。
