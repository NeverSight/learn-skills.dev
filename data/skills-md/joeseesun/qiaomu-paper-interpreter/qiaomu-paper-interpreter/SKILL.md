---
name: qiaomu-paper-interpreter
description: Transform academic papers into conversational Chinese articles in Qiaomu's style. Use when user provides arXiv URL/ID with keywords "解读论文", "论文解读", "理解paper", "读paper", or "乔木风格". Runs fully automatically.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, TodoWrite
---

# 乔木论文解读

## 概述

将学术论文自动转化为乔木风格的深度解读文章。**全自动执行**，无需用户中途确认。

**核心特点**：
- 对话式语言，像和朋友聊天
- 关键术语用引用块（>）解释，每出现新术语立刻加
- 生活化类比帮助理解，每个核心方法后必须紧跟一个类比
- 真实论文图表嵌入文章（从 LaTeX 源码精确提取）
- AI 生成纸雕水彩封面 + 《纽约客》风格配图（需配置图片生成服务）
- 写作风格规范已内嵌，无需外部依赖

---

## 配置（首次使用必读）

### 配置方式：.env 文件

在 skill 目录下创建 `.env` 文件（已加入 `.gitignore`，不会被发布）：

```bash
# ~/.claude/skills/qiaomu-paper-interpreter/.env

PAPER_OUTPUT_DIR=~/Papers/papers
PAPER_READING_DIR=~/Papers/reading
OBSIDIAN_VAULT=
IMAGE_PROVIDER=skip
IMAGE_GENERATOR_SCRIPT=
```

**参考模板**：skill 目录下的 `.env.example` 包含所有可用变量及说明。

**变量说明**：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PAPER_OUTPUT_DIR` | `~/Papers/papers` | 论文工作目录根路径 |
| `PAPER_READING_DIR` | `~/Papers/reading` | 最终文章存放目录 |
| `OBSIDIAN_VAULT` | 空 | Obsidian vault 名称，空则跳过自动打开 |
| `IMAGE_PROVIDER` | `skip` | `skip`（跳过配图）/ `jimeng` / `openai` |
| `IMAGE_GENERATOR_SCRIPT` | 空 | 图片生成脚本路径，空则用内置默认 |

系统环境变量优先级高于 `.env` 文件，适合 CI/CD 或多项目场景。

### 配置读取逻辑（每次执行时运行）

```python
import os
from pathlib import Path

SKILL_DIR = Path("~/.agents/skills/qiaomu-paper-interpreter").expanduser()

# 1. 读取 .env 文件（如果存在）
env_file = SKILL_DIR / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            # 系统环境变量优先，.env 不覆盖已设置的值
            os.environ.setdefault(k.strip(), v.strip())

# 2. 读取最终配置（含默认值兜底）
OUTPUT_DIR    = Path(os.environ.get("PAPER_OUTPUT_DIR",    "~/Papers/papers")).expanduser()
READING_DIR   = Path(os.environ.get("PAPER_READING_DIR",   "~/Papers/reading")).expanduser()
OBSIDIAN_VAULT = os.environ.get("OBSIDIAN_VAULT", "")
IMAGE_PROVIDER = os.environ.get("IMAGE_PROVIDER", "skip")   # skip | jimeng | openai
IMAGE_GENERATOR_SCRIPT = os.environ.get("IMAGE_GENERATOR_SCRIPT", "")

# 图片生成脚本默认路径
if not IMAGE_GENERATOR_SCRIPT and IMAGE_PROVIDER != "skip":
    IMAGE_GENERATOR_SCRIPT = str(
        Path("~/.agents/skills/qiaomu-image-generator/scripts/generate.py").expanduser()
    )
```

---

## 执行流程（4步）

**顺序**：步骤A → 步骤B → 步骤C → 步骤D

**执行原则**：全程自动，用 TodoWrite 显示进度，静默修复质量问题。

### 初始化 Todo

```python
TodoWrite([
    {"content": "A. 提取论文内容 + 并发转换图片", "status": "in_progress"},
    {"content": "B. 生成乔木风格解读文章", "status": "pending"},
    {"content": "C. 生成 AI 配图（封面 + 纽约客）", "status": "pending"},
    {"content": "D. 保存发布", "status": "pending"},
])
```

---

## 步骤A：提取论文内容 + 并发转换图片

**目标**：一次完成 LaTeX 提取、元数据解析、图片并发转换、图表清单生成。

### A1. 确定 arxiv_id

支持输入格式：

| 输入 | 处理方式 |
|------|---------|
| `https://arxiv.org/abs/2605.03269` | 直接提取 ID |
| `https://arxiv.org/pdf/2605.03269` | 直接提取 ID（和 abs 等价） |
| `https://arxiv.org/pdf/2605.03269v2` | 提取 ID，保留版本号 |
| `https://huggingface.co/papers/2605.03269` | 先 WebFetch 页面找 arXiv 链接，再提取 ID |
| `2605.03269` | 直接作为 ID 使用 |

**内部流程**：extract_tex.py 拿到 ID 后，从 `https://arxiv.org/e-print/{id}` 下载 LaTeX 源码 tar.gz，自动解压，找 main.tex，提取结构化内容和图片。

**如果论文没有 LaTeX 源码（PDF-only）**：
`e-print` 返回 PDF 而不是 tar.gz，extract_tex.py 会返回 `has_source: false`。此时自动切换到 markitdown fallback：
```bash
markitdown "https://arxiv.org/pdf/{arxiv_id}" -o "{paper_dir}/extracted_text.md"
```
fallback 情况下无法提取真实图表，figure_list.md 标注"LaTeX 源码不可用"，文章中用文字描述代替图片引用。

### A2. 并发启动：extract_tex.py + arXiv API（含断点续跑）

**断点续跑**：如果 `extract_result.json` 已存在且有效，直接跳过下载，从 A3 继续。适用于崩溃重试场景。

```python
import subprocess, threading, urllib.request, re, time, json
from pathlib import Path

# ── 断点续跑检测 ──
# 检查是否有已完成的 paper_id 目录（paper_id 此时尚未确定，用 arxiv_id 查找）
existing = list(OUTPUT_DIR.glob(f"*{arxiv_id.replace('.', '_')}*"))
_resume_dir = next((d for d in existing
                    if (d / "extract_result.json").exists()
                    and (d / "extract_result.json").stat().st_size > 100), None)

if _resume_dir:
    paper_dir = _resume_dir
    result_file = paper_dir / "extract_result.json"
    print(f"⚡ 断点续跑：跳过下载，使用 {paper_dir.name}")
    arxiv_meta = {}   # 仍需 API 获取日期，下面会并发请求
    _skip_extract = True
else:
    paper_dir = OUTPUT_DIR / f"tmp_{int(time.time())}"
    paper_dir.mkdir(parents=True, exist_ok=True)
    result_file = paper_dir / "extract_result.json"
    _skip_extract = False

# ── 线程1：并发请求 arXiv API（⚠️ 发布日期严禁猜测，只用此处返回值）──
arxiv_meta = {}
def fetch_arxiv_meta():
    try:
        xml = urllib.request.urlopen(
            f"http://export.arxiv.org/api/query?id_list={arxiv_id}", timeout=10
        ).read().decode()
        m = re.search(r'<published>(.*?)</published>', xml)
        arxiv_meta["published_date"] = m.group(1)[:10] if m else ""
        # ⚠️ 必须从 <entry> 内提取，xml 第一个 <title> 是 feed 标题，不是论文标题
        entries = re.findall(r'<entry>(.*?)</entry>', xml, re.DOTALL)
        entry = entries[0] if entries else ""
        t = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        arxiv_meta["title"] = t.group(1).strip().replace('\n', ' ') if t else ""
        arxiv_meta["authors"] = re.findall(r'<name>(.*?)</name>', entry)
    except Exception:
        arxiv_meta["published_date"] = ""

meta_thread = threading.Thread(target=fetch_arxiv_meta, daemon=True)
meta_thread.start()

# ── 线程2（主线程）：运行 extract_tex.py，120s 超时 ──
if not _skip_extract:
    try:
        proc = subprocess.run(
            ["python3",
             str(Path("~/.agents/skills/qiaomu-paper-interpreter/scripts/extract_tex.py").expanduser()),
             arxiv_url_or_id, "--json", "--output-dir", str(paper_dir / "latex_source")],
            capture_output=True, text=True, timeout=120
        )
        result_file.write_text(proc.stdout, encoding="utf-8")
    except subprocess.TimeoutExpired:
        print("⚠️ extract_tex.py 超时（>120s），切换 markitdown fallback")
        proc = None

meta_thread.join(timeout=5)
```

> `extract_tex.py` 已内置于本 skill 的 `scripts/` 目录，无需外部依赖。

### A3. 解析 JSON，失败检测 + 合并 arXiv 元数据

```python
import os

# ── 失败检测：空输出或无 JSON → 切 markitdown fallback ──
raw = result_file.read_text(encoding="utf-8") if result_file.exists() else ""
json_start = raw.find('{')

if json_start == -1 or len(raw.strip()) < 50:
    print("⚠️ extract_tex.py 输出无效，切换 markitdown fallback")
    import subprocess as _sp
    _sp.run(["markitdown", f"https://arxiv.org/pdf/{arxiv_id}",
             "-o", str(paper_dir / "extracted_text.md")], check=False)
    data = {}
    figures = []
else:
    try:
        data = json.loads(raw[json_start:])
    except json.JSONDecodeError:
        print("⚠️ JSON 解析失败，切换 markitdown fallback")
        import subprocess as _sp
        _sp.run(["markitdown", f"https://arxiv.org/pdf/{arxiv_id}",
                 "-o", str(paper_dir / "extracted_text.md")], check=False)
        data = {}
        figures = []

title    = data.get("title", "") or arxiv_meta.get("title", "")
authors  = data.get("authors", []) or arxiv_meta.get("authors", [])
arxiv_id = data.get("arxiv_id", arxiv_id)
markdown = data.get("markdown", "")
figures  = data.get("media", {}).get("figures", figures if 'figures' in dir() else [])
published_date = arxiv_meta.get("published_date", "")
```

# 生成 paper_id（代码化，避免每次结果不一致导致重名）
def make_paper_id(title: str, pub_date: str) -> str:
    year = pub_date[:4] if pub_date else "0000"
    # 提取全大写缩写词（长度 2-6），如 BERT、MACE、VL
    abbrevs = re.findall(r'\b[A-Z]{2,6}\b', title)
    if abbrevs:
        return f"{'_'.join(abbrevs[:2])}_{year}"
    # 否则取前 3 个英文关键词（跳过冠词介词）
    skip = {'a','an','the','of','for','on','in','to','and','or','with','via'}
    words = [w for w in re.findall(r'[a-zA-Z]+', title) if w.lower() not in skip]
    slug = "_".join(w.capitalize() for w in words[:3])
    return f"{slug}_{year}"

paper_id = make_paper_id(title, published_date)

# 重命名临时目录（如已存在则加后缀避免冲突）
new_dir = OUTPUT_DIR / paper_id
if new_dir.exists():
    new_dir = OUTPUT_DIR / f"{paper_id}_2"
os.rename(paper_dir, new_dir)
paper_dir = new_dir

# 保存文本和元数据
(paper_dir / "extracted_text.md").write_text(markdown, encoding="utf-8")
(paper_dir / "metadata.json").write_text(
    json.dumps({
        "paper_id": paper_id, "title": title, "authors": authors,
        "arxiv_id": arxiv_id,
        "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
        "published_date": published_date,
    }, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
```

### A4. 并发转换图片

**过滤规则**：跳过 >20MB 的图（多页定性对比图，不适合放博客）；其余全部转换。

```python
import concurrent.futures, subprocess, shutil

(paper_dir / "images").mkdir(exist_ok=True)

def convert_figure(fig):
    idx   = fig["index"]
    raw_src = fig["local_files"][0] if fig.get("local_files") else None
    if not raw_src:
        return None

    # local_files 可能是相对路径或绝对路径，逐级尝试
    latex_dir = paper_dir / "latex_source"
    candidates = [
        Path(raw_src),                              # 原始路径（绝对）
        latex_dir / raw_src,                        # 相对于 latex_source/
        latex_dir / Path(raw_src).name,             # 只取文件名，在 latex_source/ 下找
    ] + list(latex_dir.glob(f"**/{Path(raw_src).name}"))  # 递归搜索

    src = next((p for p in candidates if p.exists()), None)
    if not src:
        return None

    caption = fig.get("caption", "")
    words   = re.findall(r'[a-zA-Z]+', caption)[:3]
    slug    = "_".join(w.lower() for w in words) or "fig"
    dst     = paper_dir / "images" / f"figure{idx}_{slug}.png"

    ext = Path(src).suffix.lower()
    size_mb = Path(src).stat().st_size / 1024 / 1024

    if ext == ".pdf":
        if size_mb > 20:
            return {"index": idx, "skipped": True,
                    "reason": f"超大图({size_mb:.0f}MB)", "caption": caption}
        r = subprocess.run(
            ["pdftoppm", "-r", "150", "-png", "-singlefile", src, str(dst)[:-4]],
            capture_output=True
        )
        if r.returncode != 0 or not dst.exists():
            subprocess.run(["convert", "-density", "150", f"{src}[0]", str(dst)])
    elif ext in (".eps", ".ps"):
        subprocess.run(["convert", "-density", "150", src, str(dst)])
    elif ext in (".png", ".jpg", ".jpeg", ".gif"):
        shutil.copy2(src, dst)

    if not dst.exists():
        return {"index": idx, "skipped": True, "reason": "转换失败", "caption": caption}

    return {"index": idx, "file": str(dst),
            "filename": dst.name, "caption": caption,
            "size_kb": dst.stat().st_size // 1024}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(convert_figure, figures))

converted = [r for r in results if r and not r.get("skipped")]
skipped   = [r for r in results if r and r.get("skipped")]
```

### A4.5. TikZ 图补全（PDF 截图方案）

**背景**：arXiv 论文中有些图是用 LaTeX TikZ 代码直接绘制的，不是 `\includegraphics` 引用的文件。`extract_tex.py` 只提取 `\includegraphics` 图，TikZ 图不会出现在 `figures` 列表中，但它们往往是最重要的架构图和流程图。

**触发条件**：`extracted_text.md` 中出现 `**Figure N**:` 引用（说明正文里提到了这张图），但 `images/` 目录里没有对应文件。

**检测代码**：

```python
import re
from pathlib import Path

# 从 extracted_text.md 找所有 Figure 引用编号
mentioned_figs = set(re.findall(r'\*\*Figure (\d+)\*\*', paper_text))
# 已提取的图编号（来自 A4 converted 列表）
extracted_ids = set(str(r["index"]) for r in converted)
missing_ids = mentioned_figs - extracted_ids

if missing_ids:
    print(f"⚠️ 检测到 {len(missing_ids)} 张 TikZ 图（Figure {sorted(missing_ids)}），启动 PDF 截图补全")
```

**PDF 截图流程**：

```python
import subprocess
from pathlib import Path

if missing_ids:
    pdf_path = "/tmp/arxiv_paper.pdf"

    # 1. 下载 arXiv PDF
    subprocess.run(
        ["curl", "-sL", f"https://arxiv.org/pdf/{arxiv_id}", "-o", pdf_path],
        check=True
    )

    # 2. 渲染所有页面为 PNG（150 DPI）
    subprocess.run(
        ["pdftoppm", "-r", "150", "-png", pdf_path, "/tmp/arxiv_page"],
        check=True
    )
    page_files = sorted(Path("/tmp").glob("arxiv_page-*.png"))
    print(f"PDF 共 {len(page_files)} 页")

    # 3. 对每张缺失的图，找对应页面并裁剪
    from PIL import Image

    for fig_id in sorted(missing_ids, key=int):
        # 启发式：Figure N 通常在 PDF 第 N+1 到 N+3 页附近
        # 实际操作：先看 page N+1，不对再往后翻
        target_idx = min(int(fig_id), len(page_files) - 1)
        src_page = page_files[target_idx]

        img = Image.open(src_page)
        w, h = img.size

        # 截取上半页（图通常在页面上方，caption 在图下方）
        # crop 参数可能需要根据实际情况调整（0.4 ~ 0.55 之间）
        cropped = img.crop((0, 0, w, int(h * 0.5)))
        dst = paper_dir / "images" / f"fig{fig_id}_tikz.png"
        cropped.save(dst)

        # 提取该图的 caption（从 extracted_text.md 找）
        cap_match = re.search(
            rf'\*\*Figure {fig_id}\*\*[:\.]?\s*(.{{0,200}})',
            paper_text
        )
        caption = cap_match.group(1).strip() if cap_match else ""

        converted.append({
            "index": int(fig_id),
            "file": str(dst),
            "filename": dst.name,
            "caption": caption,
            "size_kb": dst.stat().st_size // 1024,
            "source": "pdf_screenshot"
        })
        print(f"✅ Figure {fig_id}: PDF 第 {target_idx+1} 页截图 → {dst.name}")

    # 清理临时文件
    for f in Path("/tmp").glob("arxiv_page-*.png"):
        f.unlink(missing_ok=True)
    Path(pdf_path).unlink(missing_ok=True)
```

**注意事项**：
- `pdftoppm` 来自 `poppler-utils`（macOS 用 `brew install poppler`）；不可用时用 `convert -density 150 paper.pdf[{page_idx}] output.png`（ImageMagick）
- `Pillow` 需已安装：`pip install pillow`
- 截图默认取上半页，论文图通常在页面上方；如果截出来有问题，调整 `0.5` 比例（例如改 `0.4` 或 `0.6`）
- TikZ 截图会包含 figure caption 文字，这是正常的，帮助读者理解图意
- **不要用 AI 生成图替代 TikZ 图**：架构图、流程图必须用论文原图，它们是作者精心设计的，随意替换会误导读者

### A5. 生成 figure_list.md

```markdown
# 论文图表清单

## 可用图表（建议全部引用）

| 编号 | 文件 | 大小 | Caption 摘要 | 建议章节 |
|------|------|------|-------------|---------|
| Figure 1 | figure1_teaser.png | 2.1MB | 整体效果展示 | 开头引入 |
| Figure 2 | figure2_overview.png | 746KB | 系统架构图 | 方法解读 |
| ...

## 跳过的图

| 编号 | 原因 | Caption 摘要 |
|------|------|-------------|
| Figure 3 | 超大图(84MB) | 定性对比图 |
```

**完成后**：更新 Todo A 为 completed，B 为 in_progress。

---

## 步骤B：生成乔木风格解读文章

### B0. 写作前准备（必须完整执行）

**第一步：读取完整论文内容 + 当前日期**

```python
import datetime

# 读取 A 步骤提取的完整正文（不能只靠记忆，必须重新读取）
paper_text = (paper_dir / "extracted_text.md").read_text(encoding="utf-8")
figure_list = (paper_dir / "figure_list.md").read_text(encoding="utf-8")
metadata = json.loads((paper_dir / "metadata.json").read_text(encoding="utf-8"))

# 读取当前日期，用于计算论文发布至今的时间跨度
today = datetime.date.today()   # e.g. 2026-05-12
pub_date = metadata.get("published_date", "")
years_since = (today.year - int(pub_date[:4])) if pub_date else 0
print(f"论文发布于 {pub_date}，距今 {years_since} 年（{today}）")
```

**当前日期的用途**：
- 在"写在后面"中具体说出"这篇论文发表于 X 年，距今 Y 年"，不用模糊说"几年前"
- 主动调用训练知识，找出这篇论文**发布后出现的重要后继工作**：哪些论文直接引用并发展了它的思路？哪些产品落地了它的方法？
- 如果论文发布时间超过 2 年，必须在"写在后面"或相关章节自然提到后续影响（不是列表，而是融入正文），例如"2 年后 Stable Diffusion 用的正是 CLIP 做图文对齐"这样的具体陈述
- 知识截止日期内未发生的事不要猜测，只写确实知道的

**第二步：自动判断是否为里程碑论文（决定字数下限）**

```python
LANDMARK_KEYWORDS = {
    # NLP / LLM
    "transformer", "attention is all you need",
    "bert", "gpt", "gpt-2", "gpt-3", "gpt-4",
    "rlhf", "reinforcement learning from human feedback",
    "instruct", "instructgpt",
    "chain-of-thought", "chain of thought",
    "in-context learning", "scaling laws",
    "codex", "alphacode", "word2vec", "seq2seq",
    # 多模态 / 生成
    "clip", "dall-e", "imagen", "stable diffusion",
    "diffusion", "ddpm", "gan", "generative adversarial",
    "vae", "variational autoencoder",
    # CV 骨干网络
    "resnet", "vit", "vision transformer",
    "alexnet", "vgg", "googlenet", "inception",
    "densenet", "efficientnet", "mobilenet",
    "batch normalization",
    # 视频理解
    "two-stream", "two stream", "i3d", "slowfast",
    "optical flow", "action recognition",
    # 检测 / 分割
    "faster rcnn", "yolo", "mask rcnn", "detr",
    "feature pyramid", "fpn",
    # 优化 / 训练技巧
    "lora", "dropout", "adam optimizer",
    "knowledge distillation",
    # 强化学习
    "dqn", "alphago", "ppo", "proximal policy",
}
title_lower = metadata.get("title", "").lower()
is_landmark = any(kw in title_lower for kw in LANDMARK_KEYWORDS)
min_words = 8000 if is_landmark else 5000
print(f"{'⭐ 里程碑论文' if is_landmark else '普通论文'}，字数下限：{min_words} 字")
```

**第三步：阅读写作规范**（见下方 B0 写作风格）

---

### B0. 乔木写作风格（内嵌，无需读取外部文件）

#### 语言特质
- 口语化、对话感强，像和读者面对面聊天
- 用"你"直接称呼读者
- **生活化类比触发规则**：每讲完一个核心方法/设计决策的技术解释后，**必须**紧跟一个类比段落。全文 ≥ 3 处，分散在不同章节。
  - **类比质量标准**：类比必须同时做到两点：① 用一个具体的日常场景（不是抽象描述），② 包含"如果不这样做会怎样"的反事实，让类比揭示的是这个设计决策的代价和收益，而不只是装饰性的比喻。
  - **禁止的类比**：太宽泛的比喻（"就像用地图导航"）、无法推出设计必要性的比喻、和技术原理对不上的类比，这些不算数，必须重写。
- 在专业性和可读性之间自然平衡

#### 表达习惯
- 短段落，多留白，视觉舒适
- 重要观点用 **加粗**，加粗句必须单独成段，不和其他句子同处一段
- 加粗句之前和之后都留空行
- **引用块触发规则**：每当文章中出现一个新的专有名词、技术术语、缩写时，**立刻**在其后加引用块解释，不要等写完再补。格式：`> **术语**：一句话解释`。全文累计 ≥ 10 处
- **引用块间距规则**：两个引用块之间必须至少隔一个正文段落。如果连续出现了多个新术语，把解释合并到同一个引用块里（用换行分隔），不要连续放多个独立引用块
- 冒号后接长内容，冒号后另起段落
- 三条以上并列经验，用列表

#### 内容层次
- 不满足于表面解释，延伸到更深的思考
- 善于在不同领域间建立联系（技术→生活→认知）
- 既讲"是什么"，也讲"为什么重要"
- 每段通过「增量信息测试」：这段提供了前面没有的新信息吗？

#### 风格调性
- 真诚、不装、承认自己的困惑
- 专业但不掉书袋，数据和案例支撑观点
- 批判性反思融入正文流，不辟独立章节

#### 让文章"生动有趣"的具体技法（每篇至少用 3 种）

1. **开头用悬念或反直觉事实**：不是"本文提出了X方法"，而是"2014 年，有一件让所有人困惑的事……"或"你可能不知道，深度学习曾经有整整两年打不过一个叫做'密集轨迹'的老方法"。
   - **使用前提**：这个"反直觉"必须是真的，读者读完之后会说"啊确实，我之前没想到"。如果你说的其实是领域常识，或者打了"反直觉"的标签但内容很平，给读者带来的是被欺骗感。**宁可不写反直觉，也不要凑一个假的**。
   - **判断方法**：写完这个反直觉事实后，问自己：一个对该领域有基本了解的读者，在读到这句话之前，他的默认预期是什么？如果这句话真的和他的预期相反，才算数。

2. **写研究者的困境和直觉**：不只说方法，要写"为什么他们会想到这个"。如果能推测研究者当时的思路（有据可查），大胆写出来

3. **反事实推理**：在讲完一个设计决策后，追问"如果不这样做会怎样"。例如"如果只用空间流，会发生什么？实验数据告诉我们：准确率从 88% 掉到 72.6%，整整少了 15 个点"

4. **具体化数字场景**：把抽象数字变成可感受的场景。"20 个百分点的差距，意味着什么？意味着每 5 个动作里，深度学习就要比手工方法多认错 1 个"

5. **图片叙事**：不只是插图，要描述图里能看到什么、这说明了什么。"看这张第一层卷积核的图，你会发现它们大多是方向性的滤波器……这不是巧合，这是网络自己学出来的，它发现光流场里最重要的信息就是方向"

6. **人物和机构背景**（仅限有公开信息的内容）：Simonyan 和 Zisserman 是同一个 VGG 组的，他们几个月后发表了 VGGNet——两篇论文是同期的工作。这个细节本身就是故事

7. **历史节点感**：点明这篇论文发表的时刻在历史上的意义。"这是深度学习在视频动作识别上第一次赢过手工特征——在 2014 年，这句话的分量不亚于 AlexNet 横空出世"

---

### B1. 硬性禁止清单（写完必须逐条自检）

| 禁止项 | 上限 | 替换方式 |
|--------|------|---------|
| 破折号（——） | **0 个** | 逗号、句号、冒号 |
| 总之 / 综上所述 / 综上 | **0 个** | 直接写结论 |
| 让我们 / 让我们来拆解 | **0 个** | 直接陈述 |
| 关键在于 / 关键来了 | **0 个** | 直接说关键点 |
| 想象一个世界 | **0 个** | — |
| 不是X而是Y | 最多 1 次 | — |
| 值得注意的是 / 重要的是 / 有趣的是 | **0 个** | 删掉，直接说 |
| delve / landscape / tapestry / robust / leverage | **0 个** | 用简单词 |
| 结尾写"总结" / 总结一下 | **0 个** | 画面或问题收尾 |
| 每个列表项都粗体开头 | **禁止** | 粗体只用于真正重点 |
| 连续的引用块（相邻无正文段落） | **禁止** | 合并到同一个引用块，或中间插入一句正文过渡 |
| 碎片式短句独立成段制造假强调 | **禁止** | 合并为一句 |
| 预告式渲染："最震撼的部分"/"一针见血" | **禁止** | 删掉，直接呈现内容 |
| "不只是X，更是Y" 排比式拔高 | **禁止** | 直接说那个"Y"是什么 |
| "不只是一个工程方案，更是一种思维方式" 类套话 | **禁止** | 没有信息量，删掉 |

### B2. 文章结构

文章由两部分组成：**正文**（主体解读）+ **写在后面**（意义总结）。

#### 正文结构

```
1. 开头场景引入（不直接说"这篇论文..."，用具体场景）
2. 核心问题（这件事难在哪？）
3. 方法解读（每个核心贡献一个 H2 节）
   - 是什么 → 为什么这么设计 → 生活化类比（必须有）
   - 新术语出现立刻加引用块
   - 插入对应论文原图
4. 数据表格（核心实验结果，加粗最佳值）
```

**字数要求**：
- 普通方法论论文：≥ 5000 汉字
- 里程碑论文：≥ 8000 汉字
- **由 B0 第二步的 `is_landmark` 自动判断**，覆盖关键词见上方列表
- **写完必须自检**：`grep -oP '[\x{4e00}-\x{9fff}]' article.md | wc -l`，低于 `min_words` 则继续扩充，不得以"文章完成"为由停笔

**每个 H2 节必须包含的四要素（缺一不可）**：
1. **技术解释**：这个设计是什么，为什么这样设计（不只是"是什么"）
2. **生活化类比**：用日常场景说明这个技术决策，每节 ≥ 1 个，全文 ≥ 3 个
3. **论文原图**：插入对应 figure，并用 1-2 句话解释图里能看到什么
4. **意义追问**：这个设计决策解决了什么根本矛盾？如果不这样做会怎样？

**历史现场要求**（论文发表 > 2 年时强制）**：
- 在"核心问题"节或第一个 H2 节中，必须描述该论文发表时领域的具体状态：当时最强的方法是什么、准确率是多少、为什么大家认为这是极限
- 用具体数字说话，不说"当时方法不好"，要说"当时最好的方法只有 X%，而手工特征达到 Y%，差了 Z 个百分点"
- 至少提及 1 个这篇论文发表前的代表性工作作为对照基准

**影响链要求**（写在后面）**：
- 必须追溯 ≥ 2 篇直接建立在本论文基础上的后续工作，用具体年份和改进点说明
- 格式参考："3 年后，X 团队的 Y 论文把这个思路扩展到……，准确率提升到……"
- 禁止只说"影响了后来的研究"，必须说出具体是哪篇论文、做了什么改变

#### 写在后面（必须包含，放文章末尾正文之前）

这一节的核心标准只有一个：**必须给读者带来正文里没有的新信息增量**，或者一个真实的感悟、启发、乐趣。不是正文的复述，不是宏观意义的拔高，不是鸡汤。

**可以写的内容**（选其中有货的，不必全写）：
- 读到这篇论文时，有什么具体的想法被触发了？（必须是具体的，不是"很有启发"）
- 这个方法打破了什么你原来以为是常识的东西？（如果有的话）
- 论文里有什么细节，值得单独拿出来说一说？（比如某个反直觉的实验结果）
- 这个思路让你联想到什么完全不同领域的东西？（只有联想是真实的才写）
- 这篇论文还没解决的问题是什么？值得追问吗？

**格式规范**：
- 用 `## 写在后面` 作为节标题
- 150-300 字，短而有料，不要为了凑字数而展开
- 不强制用"我"，但语气要是真实的，不是论文腔
- 结尾可以是一个开放性问题，但必须是你真正想问的，不是套话式的"未来值得期待"
- 禁止破折号、禁止"总之"、禁止"不只是X更是Y"这类排比

**禁止的写法举例**：
- "这篇论文不只是一个工程方案，更是一种思维方式" ← 套话，没有信息量
- "Lighthouse 的贡献对领域影响深远" ← 废话，读者已经知道了
- "未来的研究方向值得关注" ← 永远可以套用，等于没说
- 把正文已经说过的结论再说一遍 ← 没有新增量，直接删掉

#### 结尾升华（紧接"写在后面"之后）

用一个让读者脑子停不下来的画面、故事或问题作为最后一段，不归纳、不总结。

**完整顺序**：
```
论文信息引用块（开头）→ 正文主体 → ## 写在后面 → 结尾升华段落
```

#### 论文信息引用块（**仅开头放一次**，固定格式）

- **开头**：紧跟在 H1 标题之后，正文第一段之前。让读者一眼看到论文出处。
- **末尾不再重复**：结尾是画面或问题收尾，不加信息块。

所有字段均来自 `metadata.json`，**禁止凭记忆填写**。

⚠️ **换行规则**：每行之间必须加空的 `>` 行，否则 Markdown 渲染器会把所有行合并成一段：

```markdown
> **论文原文**：{完整英文标题}
>
> **arXiv**：https://arxiv.org/abs/{arxiv_id}
>
> **发布日期**：{published_date}
>
> **作者**：{前三位作者} et al.（{机构}）
```

注意：
- 不要在发布日期后加任何括号注释（如"来自 arXiv API，非推测"），直接写日期即可
- 如果 `published_date` 为空，写 `未能获取` 即可，不要猜测

### B3. 图片引用策略

**原则：所有已成功转换的图，都应在文章中找到对应位置引用。**

1. 读取 `figure_list.md`，了解所有可用图及其建议章节
2. 写每个章节时，主动匹配并插入对应图片
3. 不要集中堆放，每张图紧跟在最相关的段落之后

**引用格式（必须用标准 Markdown，禁止用 Obsidian wiki 格式）**：

```markdown
![图2：系统架构](images/figure2_overview.png)   ✅ 正确
```

```markdown
![[figure2_overview.png]]                        ❌ 禁止
```

> **为什么禁止 wiki 格式**：Obsidian 渲染 `![[xxx]]` 没问题，但发布到博客时这种格式既不会被图片上传逻辑识别，也无法被 markdown 渲染器解析，结果就是博客上一堆裂图。文章在 Obsidian 里也能正常显示标准 Markdown 格式（路径相对于文章所在目录），所以**永远用标准格式**。即便文章只准备本地阅读，也按标准格式写，避免日后想发布时再返工。

**图片-章节映射参考**：
- teaser / result 展示图 → 开头引入或结尾
- overview / architecture 图（含 TikZ 截图的 fig1_tikz.png 类型）→ 方法总览节，紧跟在介绍整体架构的段落之后
- 模块细节图（含 TikZ 截图的 fig2_tikz.png 类型）→ 对应具体方法节，讲到该模块时插入
- comparison / ablation 图 → 实验数据节
- user study / visualization → 数据分析节

**TikZ 截图图片的引用说明**：文章正文中正常引用，图名用图的实际内容命名而不是 `tikz`（例如 `![图1：Lighthouse Attention 架构图](images/fig1_tikz.png)`）。读者看到的是正常论文图，无需知道截图来源。

### B4. 写作后自检（必须执行，不合格必须修改后才能保存）

```python
import re

text = open(article_path, encoding="utf-8").read()
chinese_count = len(re.findall(r'[\u4e00-\u9fff]', text))

checks = [
    (len(re.findall(r'——', text)) == 0,         f"破折号: {len(re.findall(r'——', text))} 个（必须为0）"),
    (len(re.findall(r'总之|综上|让我们|关键在于|值得注意', text)) == 0,
                                                 "禁用词检查（必须为0）"),
    (len(re.findall(r'> \*\*', text)) >= 10,    f"术语引用块: {len(re.findall(r'> \*\*', text))} 个（≥10）"),
    (len(re.findall(r'!\[', text)) >= 3,        f"图片引用: {len(re.findall(r'!\[', text))} 张（≥3）"),
    ('## 写在后面' in text,                      "写在后面节（必须有）"),
    (text.count('> **论文原文**') >= 1,          "论文信息引用块（开头一次）"),
    (chinese_count >= min_words,                 f"汉字数: {chinese_count}（要求 ≥ {min_words}）"),
]

all_pass = True
for ok, msg in checks:
    status = "✅" if ok else "❌"
    print(f"{status} {msg}")
    if not ok:
        all_pass = False

if not all_pass:
    print("\n⚠️ 自检未通过，继续补充修改，不得保存！")
    # 字数不足时：继续写，展开已有章节，或新增"背景"/"技术细节"/"消融实验"节
else:
    print(f"\n✅ 自检通过，汉字数 {chinese_count}，保存文章")
```

**保存到** `{paper_dir}/{中文标题}_解读.md`

**完成后**：更新 Todo B 为 completed，C 为 in_progress。

---

## 步骤C：生成 AI 配图

**前提**：`IMAGE_PROVIDER != "skip"`，否则跳过本步骤，直接进入步骤D。

### C1. 封面图

提炼 1-3 个核心关键词（如 `MACE 音乐驱动舞蹈 级联专家`）：

```bash
mkdir -p "{paper_dir}/illustrations"

# 生成封面配置
cat > "{paper_dir}/illustrations/visual_config_cover.json" << EOF
{
  "task_id": "cover_{paper_id}",
  "cover": {
    "enabled": true,
    "filename": "cover.png",
    "style": "paper-watercolor-cover",
    "aspect_ratio": "16:9",
    "description": "{关键词1} {关键词2} {关键词3}"
  },
  "illustrations": [],
  "defaults": {
    "style": "paper-watercolor-cover",
    "provider": "{IMAGE_PROVIDER}",
    "retry_count": 2
  }
}
EOF

python "{IMAGE_GENERATOR_SCRIPT}" \
  "{paper_dir}/illustrations/visual_config_cover.json" --workers 1

# 插入文章开头
python3 -c "
content = open('{article_path}').read()
open('{article_path}', 'w').write('![封面](illustrations/cover.png)\n\n' + content)
"
```

### C2. 纽约客配图（3线程并发）

为每个主要 H2 节设计 visual_description（50-80字中文，具象场景隐喻抽象概念，不写风格指令）：

```json
{
  "task_id": "illustrations_{paper_id}",
  "cover": { "enabled": false },
  "illustrations": [
    {
      "id": "01",
      "h2_title": "对应H2标题",
      "visual_description": "50-80字具象场景描述",
      "filename": "01-slug.png"
    }
  ],
  "defaults": {
    "style": "newyorker",
    "provider": "{IMAGE_PROVIDER}",
    "retry_count": 2
  }
}
```

```bash
python "{IMAGE_GENERATOR_SCRIPT}" \
  "{paper_dir}/illustrations/visual_config.json" --workers 3
```

**完成后**：更新 Todo C 为 completed，D 为 in_progress。

---

## 步骤D：保存 + 打开

### D1. 复制到阅读目录

```python
import shutil
from pathlib import Path

article_path = paper_dir / f"{chinese_title}_解读.md"
images_dir   = paper_dir / "images"
dest_dir     = READING_DIR
dest_images  = dest_dir / f"{paper_id}_images"

dest_dir.mkdir(parents=True, exist_ok=True)
dest_images.mkdir(parents=True, exist_ok=True)

# 复制文章，更新图片路径为新的相对路径
content = article_path.read_text(encoding="utf-8")
content = content.replace("images/", f"{paper_id}_images/")
(dest_dir / article_path.name).write_text(content, encoding="utf-8")

# 复制图片
if images_dir.exists():
    for img in images_dir.glob("*.png"):
        shutil.copy2(img, dest_images / img.name)

print(f"已复制到: {dest_dir / article_path.name}")
```

### D2. 在 Obsidian 中打开（仅当 OBSIDIAN_VAULT 非空）

```python
import os, urllib.parse
from pathlib import Path

vault = os.environ.get("OBSIDIAN_VAULT", "")
if vault:
    reading_dir = Path(os.environ.get("PAPER_READING_DIR", "~/Papers/reading")).expanduser()
    dest_file = reading_dir / article_path.name
    # 计算相对于 vault 根目录的路径（Obsidian URI 需要 vault 内相对路径）
    vault_root = None
    for parent in dest_file.parents:
        if parent.name == vault:
            vault_root = parent
            break
    if vault_root:
        rel = dest_file.relative_to(vault_root)
        encoded = urllib.parse.quote(str(rel).replace(".md", ""), safe="/")
    else:
        # fallback: 只用文件名（去掉 .md）
        encoded = urllib.parse.quote(article_path.stem, safe="")
    uri = f"obsidian://open?vault={urllib.parse.quote(vault)}&file={encoded}"
    os.system(f'open "{uri}"')
```

### D3. 发布到博客

**触发条件**：用户输入包含"发布"/"博客"/"blog"/"post"时，本步骤必须自动执行，不询问用户。

上传本地图片并替换路径，然后发布（status 固定为 draft）：

> ⚠️ **API 调用统一走 curl（subprocess）**。博客 API 会用 User-Agent 拦截 Python 默认 `urllib`（返回 403 Forbidden），`requests` 库带的 UA 也不稳定。下面所有 HTTP 请求都用 `curl` 子进程，**不要换成 urllib/requests**。

```python
import json, re, subprocess
from pathlib import Path

TOKEN = open(Path("~/.claude/skills/qiaomu-blog-publish/config.json").expanduser()).read()
TOKEN = json.loads(TOKEN)["token"]

content = article_path.read_text(encoding="utf-8")
title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
title = title_match.group(1).strip()
body  = content[title_match.end():].lstrip('\n')

# 🔴 关键修复：Obsidian wiki 格式 (`![[xxx.png]]`) 必须先转成标准 Markdown，
# 否则下面的 `images/` 正则匹配不到 → 不会上传图片 → 发布出来全是裂图。
# 文章写作时本应用标准 Markdown，但若漏写则在此兜底。
def _wiki_to_md(m):
    name = m.group(1).strip()
    # 兼容 ![[folder/name.png]]，只取 basename
    base = Path(name).name
    if (article_path.parent / "images" / base).exists():
        return f"![{Path(base).stem}](images/{base})"
    return m.group(0)  # 找不到对应文件就保留原样，让人工 review

body = re.sub(
    r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp|svg))\]\]',
    _wiki_to_md, body, flags=re.IGNORECASE
)

# 上传单张图片，带 retry（最多 2 次）
def upload_image(abs_path):
    # timeout=60 防止大图超时（870KB 图曾在 30s 内超时）
    for _ in range(2):
        r = subprocess.run(["curl", "-s", "-X", "POST",
            "https://blog.qiaomu.ai/api/uploads",
            "-H", f"Authorization: Bearer {TOKEN}",
            "-F", f"file=@{abs_path}"], capture_output=True, text=True, timeout=60)
        try:
            resp = json.loads(r.stdout)
            if resp.get("success") and resp.get("url"):
                return resp["url"]
        except Exception:
            pass
    return None  # 两次都失败，保留原路径

# 并发上传所有图片（最多 5 线程）
import concurrent.futures
local_images = [
    (m[0], m[1], article_path.parent / m[1])
    for m in re.findall(r'!\[([^\]]*)\]\((images/[^)]+)\)', body)
]
local_images = [(alt, img_path, abs_path)
                for alt, img_path, abs_path in local_images if abs_path.exists()]

def upload_one(item):
    alt, img_path, abs_path = item
    url = upload_image(abs_path)
    return img_path, url

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for img_path, url in pool.map(upload_one, local_images):
        if url:
            body = body.replace(f"({img_path})", f"({url})")

# 生成 SEO slug：论文英文缩写/代号 + 1-2 个领域词，不含日期
# 规则：全小写、连字符分隔、≤50字符
# 例："two-stream-video-action-recognition", "bert-masked-language-model"
# 提取英文大写词（模型名/方法名）
_model_words = re.findall(r'\b([A-Z][A-Z0-9\-]{1,})\b', title)  # e.g. BERT, CLIP, GPT
_model_slug = "-".join(w.lower() for w in _model_words[:2]) if _model_words else ""
# 补充领域关键词（取自 paper_id 中的小写词，去掉年份和泛词）
_domain_words = [w for w in paper_id.lower().replace("_", "-").split("-")
                 if len(w) > 3 and w not in ("paper","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","2026")]
_domain_slug = "-".join(_domain_words[:3])
if _model_slug:
    seo_slug = f"{_model_slug}-{_domain_slug}"[:60]
else:
    seo_slug = _domain_slug[:60]
seo_slug = re.sub(r'-+', '-', seo_slug).strip('-')

# 去掉正文里的 H1 标题（博客已有单独标题字段，避免重复显示）
_lines = body.split('\n')
for _i, _line in enumerate(_lines):
    if _line.startswith('# '):
        del _lines[_i]
        while _i < len(_lines) and _lines[_i].strip() == '':
            del _lines[_i]
        break
body = '\n'.join(_lines)

payload = json.dumps({
    "title": title, "content": body,
    "slug": seo_slug,
    "category": "paper", "status": "draft"
}, ensure_ascii=False)
r = subprocess.run(["curl", "-s", "-X", "POST",
    "https://blog.qiaomu.ai/api/posts",
    "-H", f"Authorization: Bearer {TOKEN}",
    "-H", "Content-Type: application/json",
    "-d", payload], capture_output=True, text=True)
resp = json.loads(r.stdout)
slug = resp.get("slug", "")
if slug:
    print(f"✅ 博客草稿已创建")
    print(f"   Slug: {slug}")
    print(f"   编辑: https://blog.qiaomu.ai/editor?slug={slug}")
    print(f"   预览: https://blog.qiaomu.ai/posts/{slug}")
else:
    print(f"⚠️ 发布响应异常: {r.stdout[:200]}")
```

### D4. 完成报告

```
✅ 论文解读完成！

📄 标题：{h1_title}
📝 字数：约 X 字
🖼️ 原文图表：N 张引用 / M 张转换（K 张超大跳过）
🎨 封面：已生成 / 已跳过（IMAGE_PROVIDER=skip）
🎭 配图：N 张 / 已跳过

📁 {paper_dir}/
📖 已在 Obsidian 中打开 / Obsidian 未配置，请手动打开
🌐 博客草稿：https://blog.qiaomu.ai/editor?slug={slug}（如触发了发布）
```

---

## 常见问题处理

### arXiv 来源为 HuggingFace 链接

先 WebFetch 页面，找到 `arxiv.org` 链接，再传入 `extract_tex.py`。

### LaTeX 源码不可用（论文未上传 arXiv）

```bash
markitdown <pdf_url_or_path> -o {paper_dir}/extracted_text.md
```

此情况下无法提取真实图表，`figure_list.md` 标注"不可用"，文章中用文字描述代替图片引用。

### extract_tex.py 不存在

该脚本已内置于本 skill 的 `scripts/extract_tex.py`。如文件缺失，重新克隆本 skill 即可。

直接使用 markitdown fallback 亦可。

### 论文图是 TikZ 代码，extract_tex.py 没有提取到

这是正常现象。`extract_tex.py` 只提取 `\includegraphics` 引用的文件；TikZ 图是 LaTeX 代码绘制的矢量图，没有对应的图片文件。

检测方法：在 `extracted_text.md` 里搜索 `**Figure N**:`，如果某张图有文字描述但 `images/` 目录里没有文件，就是 TikZ 图。

解决方案：运行 A4.5 的 PDF 截图流程，或手动执行：

```bash
# 下载 PDF 并渲染指定页面（如第 3 页）
curl -sL "https://arxiv.org/pdf/{arxiv_id}" -o /tmp/paper.pdf
pdftoppm -r 150 -png -f 3 -l 3 /tmp/paper.pdf /tmp/paper_page
# 用 PIL 或 ImageMagick 裁剪图区域
python3 -c "
from PIL import Image
img = Image.open('/tmp/paper_page-03.png')
w, h = img.size
img.crop((0, 0, w, int(h*0.5))).save('{paper_dir}/images/fig1_architecture.png')
"
```

页面编号从 1 开始；Figure 1 通常在第 2-4 页，Figure 2 在第 3-5 页，具体看论文结构。

### 超大图（>20MB）需要强制转换

调低分辨率：
```bash
pdftoppm -r 72 -png -singlefile src.pdf dst
```

### 图片生成失败

如果 `IMAGE_PROVIDER` 配置了但生成失败，跳过配图步骤，保存纯文章版本，在报告中说明。

---

## 质量检查清单（保存前强制）

- [ ] `grep -c '——'` = 0
- [ ] `grep -c '总之\|综上\|让我们\|不只是.*更是'` = 0
- [ ] 术语引用块 ≥ 10 处
- [ ] 生活化类比 ≥ 3 处，每个类比含反事实（"如果不这样做..."）
- [ ] 数据表格 ≥ 1 个（加粗最佳值）
- [ ] 图片引用数 ≈ 已转换图总数（不漏图）
- [ ] 包含 `## 写在后面` 节（150-300字，有新信息增量，无套话）
- [ ] **开头**（H1 之后）有论文信息引用块（仅此一处，末尾不重复）
- [ ] 结尾以画面/问题收尾，无"总结"段落
- [ ] 逐段增量信息测试（每段提供新信息？）
- [ ] "写在后面"自检：是否包含正文里没有的新信息？删掉套话后还剩什么？

---

## 参考文档

- **LaTeX 提取**：`scripts/extract_tex.py`（已内置，自包含）
- **图片生成**：`~/.agents/skills/qiaomu-image-generator/scripts/generate.py`（可替换，需配置 `IMAGE_GENERATOR_SCRIPT`）
- **博客发布 token**：`~/.claude/skills/qiaomu-blog-publish/config.json`（`{"token":"qm_xxx"}`）
- **写作风格**：已内联到本 skill（步骤 B0），无需外部依赖
- **风格指南**：`references/style-guide.md`
- **使用示例**：`examples.md`
- **故障排查**：`TROUBLESHOOTING.md`
- **配图设计**：`visual_description_guide.md`
- **版本历史**：`CHANGELOG.md`
