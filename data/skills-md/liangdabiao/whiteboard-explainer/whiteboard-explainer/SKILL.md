---
name: whiteboard-explainer
description: 白板讲解动画 skill：把知识讲解/科普/推导内容变成「真手绘过程」视频——白板图上的图形被一笔笔描出来、文字逐笔写出、讲到哪画到哪（帧级音画对齐）。基于 whiteboard-animator 引擎（本地 CPU 渲染、零 API 成本、确定性可重渲）。当用户要做知识讲解视频、概念科普、数学/流程推导、数据图表讲解，或要求"手绘白板动画"、"讲解画面逐笔绘制"、"讲到哪画到哪"时使用。触发词：白板动画、白板讲解、手绘讲解、explainer、知识科普视频、讲到哪画到哪、逐笔绘制、whiteboard。
---

# Whiteboard Explainer（白板讲解动画）

把讲解稿变成白板手绘动画：每拍一张白板图，图形按笔画绘出、文字逐笔写出，**元素级精确对齐旁白（讲到哪画到哪）**。

**和另外两个手绘 skill 的区别**：`story-handdrawn-remotion` 是静帧擦除（假手绘）；`story-handdrawn-video` 是 Agnes 文生视频（真动但不可控）；本 skill 是**像素级笔画绘制**——帧帧确定、本地零成本、可秒级重渲，且支持"一图逐元素生长"的单画布模式（前两者做不到）。

**工具链**：whiteboard-animator 引擎（官方 PyPI 包 `==0.1.1`，首次 setup 自动安装，自带 CRAFT 文字检测模型约 83MB）+ Agnes Image 2.1（白板风生图，免费）+ PIL（确定性中文文字层）+ edge-tts（免费旁白）+ ffmpeg。

**安装（下载后只要 1 步）**：

| 平台 | 命令 |
|---|---|
| macOS / Linux / Git Bash | `bash scripts/setup.sh` |
| Windows PowerShell | `powershell -ExecutionPolicy Bypass -File scripts/setup.ps1` |

脚本会建 venv、装依赖（`whiteboard-animator==0.1.1` 引擎，约 83MB 的 CRAFT 模型随 pip 从 PyPI 下载，onnxruntime / edge-tts / Pillow / numpy 等传递依赖自动装上）、检查 ffmpeg 路径（缺失会报错并提示安装）。装完用 `source .venv/bin/activate`（或 `.venv\Scripts\Activate.ps1`），所有 `scripts/*.py` 都在 venv 里直接 `python scripts/xxx.py` 即可。

**质量原则（70% 即交付）**：单拍画面构图对、元素对就过，不逐拍修图。渲染是本地的、零成本，重渲比修图便宜——但也遵守"skip 已存在"纪律。

## 成片模式（两种）

| 模式 | 适用 | 做法 |
|---|---|---|
| **slide 序列**（默认） | 逐句讲解、步骤演示 | 一拍一图，每拍独立渲染后 concat |
| **单画布生长** | 数学推导、流程图、知识图谱 | 一张大图 + 多 region + 逐句 cue，画面持续累积 |

## 新一集工作流（7 步）

### 1. 写讲稿 + 拆 region（plan.build.json）

每拍 = 一张白板图 + 若干 region（一个 region = 图上一块绘制区域 + 一句 annotation）。**讲稿按 region 子句拆分，每个子句单独 TTS**——分片时长即精确 cue。

```json
{
  "idea": "解释日全食",
  "canvas": [1280, 720],
  "voice": "zh-CN-YunxiNeural",
  "gap": 0.35,
  "scenes": [
    {
      "id": "s01",
      "image": "boards/s01.png",
      "regions": [
        {"label": "title", "box": [10, 330, 125, 670], "annotation": "什么是日全食？"},
        {"label": "body", "box": [130, 80, 820, 720], "annotation": "当月亮恰好完全挡住太阳……"},
        {"label": "deco", "box": [790, 100, 1000, 900]}
      ]
    }
  ]
}
```

无 annotation 的 region = 纯图形（不说话），自动并入与其空间重叠最大的 cue 窗口一起画出；无任何重叠时并入最后一个窗口。

**box 写法**：`[ymin, xmin, ymax, xmax]`，归一化 0–1000（左上原点）。一个 region 也可以给 box 数组（多块同时画）。

### 2. 准备白板底图（三种来源）

| 来源 | 命令 | 说明 |
|---|---|---|
| **PIL 程序化绘制**（几何/图表首选） | 自写脚本，参考 `templates/chart-recipes/eclipse.py` | 几何精确、白底纯净、完全可控 |
| **Agnes 生图**（具象画面） | `python scripts/gen_board_images.py boards.json --out-dir boards` | 免费；prompt 铁律见下 |
| **用户已有图** | 直接放入 boards/ | Excalidraw 导出、教材图等 |

**文字铁律**：AI 只画无字插画（negative 排除 text/letters/Chinese characters）；所有中文/标签/公式用 `make_text_layer.py` 本机字体叠加：

```bash
python scripts/make_text_layer.py boards/s01.png --out boards/s01.png \
  --title "什么是日全食" --title-size 56 \
  --texts texts.json   # 多块文字用 JSON 文件
```

字体跨平台自动探测（Noto CJK / 苹方 / 微软雅黑 / simhei……）；`handwriting` preset 用 skill 自带毛笔字。

**底图硬规则（ink-on-white）**：
- 白底（近白像素引擎会 snap 成白）；灰度 <240 才算墨——浅黄/浅灰要够深（#FFF 系会消失）
- 长边 >1280 引擎自动缩小；项目级画布一次选定（横屏 1280×720 / 竖屏 720×1280）

### 3. 生成音轨 + 精确 cue

```bash
python scripts/build_narration.py plan.build.json
```

逐 region 子句 TTS → 分片 → 垫 gap（默认 0.35s）→ concat 成每拍音轨 → 用分片真实时长写出 `plan.json`（regions 带精确 start/end）。edge-tts 偶发 NoAudioReceived，脚本自带重试；**失败的 0 字节分片要删掉重跑**（`find audio/narration/parts -name "*.mp3" -size -2k -delete`）。

### 4. 渲染

```bash
python scripts/render_explainer.py plan.json --out out/<name>.mp4
# 常用：--only s03（单拍调试）  --force（忽略已存在重渲）  --quality high  --dry-run
```

每拍 mp4 输出到 `out/<name>_parts/`，最后 concat。**渲染速度 ≈ 视频时长**（8s 片段约 5-8s）。已存在的分拍自动 skip。

### 5. 验收

- `ffprobe` 成片 video/audio duration 一致
- 每拍抽 1-2 帧：`ffmpeg -i out/parts/s03.mp4 -vf "select=eq(n\,150)" -vframes 1 out/check.png`，确认 cue 对齐（该时刻只有已讲到的元素）
- Windows 下 ffmpeg/Read 图片一律用 `D:/...` 绝对路径（`/d/...` 会失败）

### 6.（可选）发布前自检

```bash
python scripts/self_test.py
```

跑三个最小测试：①CRAFT 中文识别 ②白板动画渲染 ③精确 cue 对齐。**任意一个失败就别发版本**。

## Region Plan 硬规则（踩坑总结，必读）

1. **box 紧贴实际内容，不要贪宽**。引擎按"组件 bbox 与 box 交叠 ≥60% 的 box 面积"判定归属；横贯全屏的宽 box 会让大组件被判成"跨多个窗口"（spanning）而归入最早的窗口，打乱绘制顺序。
2. **不同窗口的 box 不要罩住同一个组件**。尤其先画的窗口不要把 box 伸进后画元素的领地。
3. **图上物理相连的元素永远一起画**（连通域不可分割）。想让"本影/半影"分开讲，绘图时必须在它们之间留白缝（≥8px，锥尖附近要更宽——白缝三角形会收敛）。**文字标签必须放在纯白区域**，压在色块上的标签会和色块连成一体。
4. **AI 生图的大色块容易连成巨型连通域**——构图时让主要元素之间留白。
5. cue 窗口装不下绘制量时引擎报 `schedule exceeds cue window`，渲染脚本自动放宽 15%×N 重试，无需手动干预。

## 常见坑

- **edge-tts 0 字节分片**：NoAudioReceived 后 save 可能留 0 字节文件，重跑会被 skip。先 `find ... -size -2k -delete`。
- **Windows 路径**：所有 python 脚本内 subprocess 已带 `encoding="utf-8", errors="replace"`；ffmpeg 命令行用 `D:/` 路径不用 `/d/`。
- **进程替换不可用**：`--texts <(echo ...)` 在 Windows Python 下失败，用临时 JSON 文件。
- **concat 要求一致**：所有拍要么全有音轨要么全静音（脚本会强制校验）。
- **Agnes 画手/画笔的先验**：prompt 里出现 "whiteboard/marker" 容易画出手握马克笔的画面，negative 加 `no hands, no pens, no brushes, no people, no tools`。
- **managed python 的 venv 不带 pip**：先 `python -m ensurepip`。
- **AGNES_API_KEY 找不到**：把 `.env` 文件放到 `cwd`、`~/.env`、`~/.workbuddy/.env` 或环境变量任一处均会被读取；缺 key 时 `gen_board_images.py` 会硬报错（不会静默失败）。

## 依赖与凭证

| 依赖 | 类型 | 必须？ |
|---|---|---|
| `whiteboard-animator` | pip 包（PyPI，自带 83MB CRAFT 模型） | 必须，setup 自动 `pip install ==0.1.1` |
| `onnxruntime` / `numpy` / `Pillow` / `opencv` / `scipy` / `scikit-image` | pip 包（引擎传递依赖） | 必须，pip 自动装 |
| `edge-tts` | pip 包 | 必须（免费 TTS，无需账号） |
| `ffmpeg` / `ffprobe` | 系统二进制 | 必须，PATH 里要有 |
| `AGNES_API_KEY` | Agnes 生图 API key（可选） | 仅当 `gen_board_images.py` 需要生图时 |

无 `AGNES_API_KEY` 也能出片（PIL 自带的 `make_text_layer.py` + `templates/chart-recipes/*.py` 够画大部分图）；需要 AI 生图时才用它。

## 配套参考

- 完整流水线细节：`references/pipeline.md`
- region plan 写法与坐标纪律：`references/region-plan-guide.md`
- 程序化白板图示例（日全食全套）：`templates/chart-recipes/eclipse.py`
- region plan 示例：`templates/region-plan.example.json`
- 自检脚本：`scripts/self_test.py`
