---
name: paint-mv-animate
description: >-
  Paints one chapter (src/ch/cNN_name.js) of a paint-mv music video in the PDoomVideo style: watercolour-and-ink frames
  drawn with p5.brush, the song's own characters (designed from its lyrics) acting on the beat, camera moves and
  motivated transitions, each frame a pure function of song time. The PDoomVideo ANIMATION_GUIDE as a skill, with the
  engine API reference, a guide to designing characters in the house style, a techniques catalogue and the nine original
  chapters as examples. Use when painting, fixing or polishing an MV chapter, shot or character, when briefed as a
  chapter subagent by paint-mv, or when editing src/ch/*.js or src/characters.js in a project made with paint-mv.
---

# 章节作画规范（paint-mv-animate）

项目把一首歌画成手绘水彩动画：p5.brush 在 headless Chrome 里离线逐帧绘制，所以质量优先于速度，但有预算。
镜头清单在项目的 `STORYBOARD.md`。**画风照原作，内容照歌词**：角色、场景、道具是这首歌的分镜从歌词里设计出来的；
画法、动作、镜头语言和下面的规则与原作一致。创作方向（源自原作）：**可爱、卡通、色彩欢快、动画活泼、每个镜头都有事发生，
大胆、有野心。**

开工前按顺序读：
1. 项目 `STORYBOARD.md`：开头的"歌曲信息"、角色表、你的章节表格，以及**前后相邻章节的"出"列**（Out，衔接要对上）。
2. 项目 `src/song.js`（BPM、首拍 `offset`、时长、`wipes`、`meter`）和 `src/lyrics.js`（每句歌词的起止时间）。
3. 项目 `src/characters.js`（本片主要角色）和 `src/sets.js`（共享场景/道具），并看角色模型表
   `node render.mjs --loop=cast --sheet=0,1,2,3,4,5 --cols=3 --out=out/check/cast.jpg`。
4. 本文件。需要具体签名时查 [api.md](api.md)；要新建客串角色时读 [characters.md](characters.md)；想找某种镜头/转场/表演的
   现成做法查 [techniques.md](techniques.md)，它会指到 `examples/` 里原作九个章节的具体函数（原作 P(doom) MV 的完整源码，
   画风与难度的标杆；它的角色和场景属于那首歌，学做法，不搬内容）。

## 章节文件怎么工作

每章一个文件 `src/ch/cNN_name.js`，包在 IIFE 里，私有 helper 随便起名不会冲突：

```js
// src/ch/c03_takeoff.js
(() => {
  const B = n => OFF + n * BEAT;                  // 第 n 拍的歌曲时间
  const gym = t => { ... };                       // 私有 helper
  function stable(t, lt, dur) { ... }             // 一个镜头
  function singularity(t, lt, dur) { ... }
  chapter('takeoff', 38.5, 59.0, [[38.5, stable], [41.5, singularity], ...]);
  CAST.sydney = (x, y, s, t, o = {}) => { ... };  // 只有终场要复用的客串角色才导出
})();
```

- `chapter(name, start, end, shots)` 注册章节。镜头函数以 `fn(t, lt, dur)` 调用（歌曲时间、镜头内时间、镜头长度），
  必须画出**整帧**（包括背景）。切镜发生在每个镜头的起始时间；第一个镜头的起始时间必须等于章节 `start`。
  最后一章的 `end` 写 `DUR + 1`，保证最后一帧也有章节覆盖。
- **帧是并行、乱序渲染的。**每个镜头必须是 `t` 的纯函数：不能有跨帧状态，不能用 `Math.random()`。
  稳定的逐物体随机用 `hash(i)`，手绘抖动用 `jit(a)`。`jit` 每秒重播种 12 次，线条会像手绘动画一样"沸腾"，这是想要的效果。
- **只改你自己的章节文件。**缺共享 helper 就在 IIFE 里私有实现一个。发现共享文件真有 bug，报告给总控，不要改。
  共享文件：`core.js`、`clawd.js`、`cast.js`、`props.js`、`timeline.js`、`lyrics.js`、`song.js`、`characters.js`、`sets.js`、
  `studio.html`、`render.mjs`。

## 画布与布局

- 1920×1080，y 向下，原点左上。没开相机时一切都在这个空间里画。
- **有歌词时，卡拉 OK 条盖住底部 y≈975–1070。**脸和关键动作放在 y≈960 以上。
- 每帧底下已经铺好纸纹，最上面会乘一层纸颗粒和暗角。
- 时间线自动叠加：卡拉 OK、`SONG.wipes` 处的笔刷擦除转场、`SONG.meter` 窗口里角落的小计量器
  （镜头里画了 `meterProp` 时自动隐藏）。

## 绘画 API（core.js）

`paint(pts, o)` 用点列 `[[x, y], ...]` 画一个形状：

| 选项 | 含义 |
|---|---|
| `wash, washOp` | 平涂色（0–255）。角色颜色和必须实在可读的东西用它。 |
| `fill, fillOp, bleed, tex, border` | 水彩填充，边缘洇开、有颜料肌理。背景、光晕、阴影、光斑用它。`bleed` ~.05–.3，`tex` ~.3–.9，`border` ~.2–.8。 |
| `hatch: { d, a, o, b, c, w }` | 排线（间距、角度、`{rand, gradient}`、笔刷如 `'charcoal'`/`'HB'`、颜色、粗细）。干笔肌理，少用。 |
| `ink, sw, br` | 描边颜色（默认墨色）、粗细（~.4–2）、笔刷（默认 `'ink'`，或 `'inkfine'`）。**`ink: null` 表示不描边。** |
| `curv` | 让轮廓平滑穿过各点（0–1），而不是直线段。 |

其他：
- **几何：**`rectPts(x, y, w, h, jitter)`、`ellPts(cx, cy, rx, ry, n, jitter, rot)`、`rrPts(x, y, w, h, r, jitter)`（圆角矩形）、
  `starPts(cx, cy, r, inner, n, rot)`、`heartPts(cx, cy, r)`。
- **线：**`inkLine(pts, sw, colour, brush = 'ink', curvature)`。笔刷：`'ink'`、`'inkfine'`、`'dry'`（毛糙），
  以及内置 `'2B'`、`'HB'`、`'charcoal'`、`'marker'`、`'spray'`、`'rotring'`、`'cpencil'`、`'pen'`。
- **变换：**p5 的 `push()/pop()/translate()/rotate()/scale()` 对所有笔刷调用都生效。
- **调色板 `PAL`：**`paper, ink, clay, clayDk, clayLt, night, indigo, rose, ochre, sap, teal, violet, cream, sky`。
  `mixCol(a, b, k)` 混合两个十六进制色。任何十六进制色都可以，但保持和谐（柔和、温暖、水彩感）。
  互补色直接混合（夜蓝渐变到晨桃）中途会发灰，中间加一个过渡色分两段混（夜蓝 → 紫玫瑰 → 晨桃）。
  不要纯黑纯白：用 `PAL.ink` / `PAL.night` 和 `PAL.cream`。
- **计时：**`bpOf(t)` 给出拍位置（BPM 见 `song.js`；拍长 `BEAT`，小节 4 拍）。另有：
  - `beatN(t)` 整数拍号；`pulse(t, k)` 每拍为 1 然后衰减，`pulse2` 八分音符版，用来做打点。
  - `seg(t, a, b)` 是 t 在 [a, b] 里的 0..1 进度；`kf(t, [[t0, v0], [t1, v1], ...], easeFn)` 关键帧插值，值可以是数组。
  - 缓动：`ease`（smoothstep）、`easeOut`、`easeIn`、`backOut`（过冲）、`elasticOut`。还有 `lerp`、`clamp`、`frac`、
    `wob(t, freq, phase)`、`hash(i)`、`TAU`。
- **相机：**`camBegin(cx, cy, zoom, rot)` 把世界点 (cx, cy) 放到屏幕中心；`camEnd()` 恢复。推、摇、俯仰、甩、拉远都用它。
  `shakeXY(t, amount)` 给出 [dx, dy] 震动，打点时加到 cx/cy 上。只能一层，务必配对 `camEnd()`。
- **字（Permanent Marker，带墨色投影）。**字会自动跟随当前相机，但**不跟随**你自己的 `push/translate`，所以字的坐标给世界坐标。
  - `letter(txt, x, y, size, colour, { pop, rot, alpha, ink:false, stroke, font, align, screen:true })`，`pop` 是 0..1 带过冲的出现进度。
  - `sfx(txt, x, y, size, colour, age, { life, rot })` 漫画拟声字：弹出、晃动、淡出。
  - 字在 `flushLetters()` 时合成进画面。它在镜头之后自动调用，所以之后画的东西（擦除转场）会盖住字。
    需要让后面的颜料盖住某个字时，镜头中途自己调用 `flushLetters()`。
- **全屏效果**（屏幕空间，在相机之外调用）：`flash(k, colour)` 全屏平涂强度 k；`iris(cx, cy, r, colour)` 圆外全涂；
  `irisShape(pts, colour)` 任意星形轮廓外全涂（嘴形揭幕、心形、钥匙孔）。

## 角色

本片的角色由分镜的角色表决定，是从歌词设计出来的：
- **主要角色**在 `src/characters.js`（共享，只读；缺表情、姿势或钩子就报告给总控）。先读它的头部注释，再看模型表。
- **客串**由首次登场的章节在自己的 IIFE 里实现，导出到 `CAST`（签名 `(x, y, s, t, o)`，要参加谢幕的支持 `o.bow` 0..1）；
  之后要用它的章节调用 `CAST.name` 并写一个简化的后备画法。按原作画风设计和实现角色的方法见 [characters.md](characters.md)。
- **群演**是主角的变体：换 `col`/`dk`/`lt`、戴帽子、缩小。

所有角色遵守同一套约定（原作 Clawd 和研究员的约定），所以下面这些工具对谁都通用：
- `name(x, y, u, o)`：(x, y) 是两脚之间的地面点；`u` 是尺寸单位（各角色身高几 u 写在它的头部注释里）。
- **姿态：**`dy`（单位 u，负为上）、`sq`（压扁；负为拉长）、`rot`、`flip`、`sx`/`sy`、`aL`/`aR`（手臂角：0 平伸，正为抬起，负为下垂）、
  `walk`（相位）、`noShadow`。
- **脸：**`eyes`：normal, look（+`lookX`/`lookY` −1..1）, happy, closed, wink, narrow, angry, scared, spark, heart, x, swirl, dot…
  （角色画不出的眼型会退回 normal）；`mouth`；`blush`；颜色 `col`/`dk`/`lt`。
- **钩子：**`draw(u, sw)` 在身体局部坐标画配饰；手臂末端的 `armL`/`armR(u, sw)`（研究员是 `handL`/`handR`）在手臂坐标系
  （+x 沿手臂向外）里被调用，用来拿道具。
- **表情符号：**`emote` + `emoteK` 在头边弹出反应符号：sweat, spark, heart, anger, music, swirl, zzz, !, ?, !?, !!。
- **情绪切换：**脸绝不硬切。用 `mood(t, [[t0, 'normal'], [t1, 'scared', 'sweat'], [t2, 'happy', 'heart']])`，
  返回 `{ eyes, squint, take, emote, emoteK }`，展开进角色就得到"闭眼-压扁-弹出"的切换。
- **跳舞：**`move(style, t, seed)` 返回与节拍同步的姿态偏移：bounce, hop, roof（举手）, sway, spin, wave, walk, run, idle, stomp,
  shimmy, mix。`dx` 以 u 为单位：`const m = move('bounce', t); hero(x + m.dx * u, y, u, { ...m, ...mood(t, keys) })`。
- **尺寸参考**（按身高约 8u 的角色）：小 u≈6–10，正常 u≈16–22，主角/特写 u≈30–60。副歌和舞蹈镜头里领舞的主角要大（约占画面高度 40%）。

**引擎自带的参考角色**：原作那首歌的演员，分镜用到时才出现；设计新角色时照它们的结构写。
- Clawd `clawd(x, y, u, o)`：方块身体 10u × 6u，连腿 8u 高；另有帽子 `hat`（party, hard, crown, halo, wizard, hood, top, fedora, band,
  sweatband, cat, masq, mask, bowtie）、便当盒嘴 `lid`、`noLegs`；`dancer(x, y, u, style, t, extra)` = `clawd` + `move`。
- 研究员 `researcher(x, y, s, o)`：白大褂、圆眼镜的小个子人类，约 13.2s 高；自己的眼型 dot, wide, star, swirl, closed, sad, x, heart, look，
  外加 `brows`、`hairUp`、`glassesTilt`、`sit`、`back`、`spin`；`mood()` 用在它身上要映射眼型名（techniques.md「表演」）。
- 完整选项见 [api.md](api.md)。

## 场景与道具

- 本片反复出现的场景和道具在 `src/sets.js`（共享，只读）；只在本章出现的场景画在本章里。
- 画在场景里的字（招牌、片名、墙上的字）写完 `letter()` 就调用 `flushLetters()`，否则字会浮在之后画的角色上面（c01 `curtainUp`）。
- 引擎自带原作的剧场道具（`props.js`），分镜用到时才用：`stageBack(t, o)` / `stageFront(t, o)`（舞台后景与木地板 / 两侧幕布与垂幔，
  `o.curtain` 合幕、`o.alarm` 警报色、`o.spots` 聚光灯）、`meterProp(x, y, s, pdoomAt(t), o)`（计量器，配合 `SONG.meter`）、
  `pumpProp` + `pumpH(t)`（下压落在每拍上的打气筒）、`sunburst`、`spotlight`。它们也是写新场景的范例：背景画得比画面大
  （相机移动和震动不露边）、后景在角色之前画、前景框在最后画。

## 风格规则

- **观感：**手绘水彩加墨线，像绘本。角色用平涂 `wash` 加墨线轮廓（sw 按大小约 0.8–1.6）。背景用柔和的水彩 `fill`，
  通常不描边或细描边。光晕和光线用低不透明度的 fill。肌理来自 fill 和偶尔的排线，而不是噪点。
- **颜色：**每章的调色在 STORYBOARD.md 里。欢快饱和但柔和。角色与背景的对比必须清楚。
- **运动：**一切都在动：相机漂移或推进，角色随拍弹跳（`pulse`、`move`），打点落在拍上。用压扁拉伸、预备动作和过冲
  （`backOut`、`elasticOut`）。镜头里的重要动作放在拍点上（拍点在 `OFF + n × BEAT`；章节里写 `const B = n => OFF + n * BEAT`）。
- **可读性：**每个镜头一个清晰的焦点动作，轮廓要大。镜头很短（1.4–4 s），笑点必须一眼看懂。
- **少字：**拟声字全片只有少数几个大的（FOOM、BOOM、CHOMP、SLAM…），偶尔一个短词或符号。不要标签、说明文字、
  重复歌词的牌子（卡拉 OK 已经有了）。
- **性能：**目标每帧 ≤ 2.5 s，绝不超过约 4 s。渲染日志会打印 ms/frame。开销来自 fill 形状和笔画的数量：几百个没问题，
  几千个不行。宁可更少、更大的形状。水彩 `fill` 的开销随顶点数增长，大形状用 `wash`，fill 保持低多边形。

## 检查你的作品

在项目根目录运行（渲染器用真 GPU；多个代理可以同时渲染）：

```bash
node render.mjs --sheet=38.6,39.3,40.1,40.9,41.6,42.3 --cols=3 --w=640 --out=out/check/c03_a.jpg
node render.mjs --stills=39.5,43.2 --out=out/check/c03_full
```

联系表（sheet）把几个时刻拼成一张图（并打印每帧 ms），用 Read 工具打开，仔细看。检查：
- 每个镜头的首帧、末帧和中间几帧；
- 连续时刻的运动是否读得通（例如打点前后每 0.1 s 一帧）；
- 进出本章的转场（与相邻章节的"出"和开场对上）；
- 没有重要内容落在卡拉 OK 带下面；
- 页面报错：渲染日志里的 `[page error]` 表示你的代码抛了异常（该帧会画坏）。

反复迭代，直到每个镜头都好看：有魅力、可读、有生气、造型一致。看着不对就改：比例、对比、杂乱、僵硬。

## 交付时汇报

完成后简短汇报：每个镜头一句话说明画了什么；检查过的联系表路径；最慢帧的 ms；导出的 `CAST` 角色及其签名；
与相邻章节的衔接状态（本章首帧/末帧是什么）；发现的共享文件问题（只报告，不修改）。
