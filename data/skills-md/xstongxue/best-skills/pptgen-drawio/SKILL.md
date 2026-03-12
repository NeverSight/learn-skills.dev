---
name: pptgen-drawio
description: 根据论文或汇报内容生成多页 Draw.io 格式 PPT，支持论文答辩与通用汇报两种模式，自动导出为 .pptx。当用户提到论文答辩 PPT、答辩幻灯片、通用 PPT、汇报 PPT、根据模板生成 PPT、drawio2pptx 时使用。
---

# PPT 多页 Draw.io 生成（论文答辩 + 通用汇报）

本 skill 支持两种模式，**共用** `ppt_template/`、`scripts/`、`reference/` 目录，以及 **Step 0 自定义模板**、**Step 1 确定内容与风格**、**Step 3 & 4 输出与导出** 全流程。

---

## 模式识别

| 模式 | 使用时机 | 内容来源 | 默认页序 | 输出文件 |
|------|----------|----------|----------|----------|
| **论文答辩** | 学位论文答辩、开题、预答辩 | paper-write 结构化提取 | 封面→目录→背景→现状→方法→创新点→实验→结论→致谢→Q&A | `paper-defense.drawio` |
| **通用汇报** | 工作汇报、产品介绍、演讲 | 用户消息提取/生成 | 封面→目录→节标题→内容页→总结→致谢→Q&A | `general-presentation.drawio` |

---

## Step 0：用户自定义模板（可选，两种模式共用）

若用户提供了自己的 `.pptx` 模板文件：

1. **模板放置**：将 `.pptx` 放入 `ppt_template/` 目录
2. **运行样式提取**：在 skill 根目录下执行：
   ```
   python scripts/analyze_pptx.py ppt_template/xxx.pptx reference/style-custom.md
   ```
3. 读取 `reference/style-custom.md` 作为「自定义风格」继续

**目录约定**：`ppt_template/` 存放模板、`scripts/analyze_pptx.py` 样式提取、`reference/` 风格文件

---

## Step 1：确定内容与风格（两种模式共用）

### 1.1 确定内容

- **论文答辩**：若用户只有论文全文：先调用 paper-write 的「结构化信息提取」；若已提供结构化信息：从消息中提取【论文题目】【学科方向】【答辩时长】【论文结构/目录】【各章核心内容】【创新点/贡献】等，缺失则追问
- **通用汇报**：从用户消息中提取幻灯片大纲及内容，或根据核心需求扩展为完整结构

### 1.2 选择风格

两种模式均可选择以下风格之一，**读取对应 reference 文件**获取配色、字体、版式规则与 XML 样式片段：

| # | 风格 | 主色 | 强调色 | reference 文件 |
|---|------|------|--------|---------------|
| 1 | 经典学术 / 商务严谨 | `#1B2A4A` | `#C9A84C` | `reference/style1-classic-academic.md` |
| 2 | 现代极简 / 大字报感 | `#231F20` | `#F5C638` | `reference/style2-minimal-bigtype.md` |
| 3 | 暖色学术 / 亲和力 | `#2C5160` | `#B7472A` | `reference/style3-warm-academic.md` |
| 4 | 科技明快 / 现代前沿 | `#0170C1` | 同主色 | `reference/style4-tech-modern.md` |
| 5 | 自定义 | 从 style-custom.md 提取 | | `reference/style-custom.md` |

- **论文答辩**：用户未指定时默认风格 1
- **通用汇报**：用户选择或根据语境自动推荐

---

## Step 2：生成多页 Draw.io XML

**必须先读取所选风格的 reference 文件**，基于该风格生成 XML。

- 画布：16:9（pageWidth=1920，pageHeight=1080）
- 页序：按模式识别表中的默认页序
- 页数：10 分钟约 10–12 页，15 分钟约 14–18 页
  - 含节标题过渡页（每章独立一页引入）时，10 分钟约 11 页；无过渡页时约 9 页
  - 节标题过渡页风格：大号数字 + 章节名，可参考 style2 风格或 style4（无过渡页）

### ⚠️ 已知坑清单（生成前逐条过）

生成每一页 XML 前，必须按顺序检查以下所有坑，避免重复踩雷。

---

#### 坑 #1：必须使用 mxfile 多页格式

**drawio2pptx 只识别 `<mxfile>` 根节点 + 多个 `<diagram>` 子节点的格式**，每个 `<diagram>` 对应一张幻灯片。

**禁止**使用单一 `<mxGraphModel>` 根节点横向铺排多页（会被识别为 1 张幻灯片）。

**正确格式模板（必须严格遵守）：**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="page1_unique_id" name="封面">
    <mxGraphModel dx="1422" dy="762" grid="0" gridSize="10" guides="1"
                  tooltips="1" connect="0" arrows="0" fold="0" page="1"
                  pageScale="1" pageWidth="1920" pageHeight="1080" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 本页所有元素，x 坐标从 0 开始，不做跨页偏移 -->
      </root>
    </mxGraphModel>
  </diagram>
  <diagram id="page2_unique_id" name="目录">
    <!-- 同上结构，x/y 坐标同样从 0 开始 -->
  </diagram>
</mxfile>
```

---

#### 坑 #2：每页坐标从 0 开始，不得跨页偏移

- 每个 `<diagram>` 内部的所有 mxCell **x 坐标从 0 开始**，不得偏移（不能用 1960、3920 等跨页偏移）
- 每页独立坐标系，背景矩形 `x="0" y="0" width="1920" height="1080"`
- `<mxCell id="0"/>` 和 `<mxCell id="1" parent="0"/>` 必须出现在每页 root 内

---

#### 坑 #3：mxCell id 全局唯一

- 同一个文件内，**所有 diagram 的所有 mxCell id 必须全局唯一**
- 推荐命名规则：`p{页号}_{元素缩写}`，如 `p1_bg`、`p2_title`、`p3_box1`
- 绝对禁止不同页出现相同 id（会导致渲染错乱或解析失败）

---

#### 坑 #4：diagram id 唯一

- 每个 `<diagram>` 的 `id` 属性也必须唯一，推荐用 8 位随机字符串，如 `"aB3xKp7m"`

---

#### 坑 #5：文件必须一次性写入

- 同一个任务中如果多次调用 Write 写同一个文件名，后写的内容会覆盖前面的
- 必须**一次性写入完整内容**，不可分多次追加
- 若单次生成内容超长，**不可分割后合并**（XML 合并极易出错）；正确做法是减少每页装饰细节、合并相似页，确保能一次完整输出

---

#### 坑 #6：导出页数验证

- drawio2pptx 输出的 `(N slides)` 数字 **必须等于 diagram 数量**
- 若显示 `(1 slides)` 而预期多页，说明 XML 格式错误（触发了坑 #1），需检查是否用了单根 `mxGraphModel` 格式

---

#### 坑 #7：批量多风格时每种风格独立文件

- 每种风格写入**独立文件名**，如 `paper-defense-style1.drawio`、`paper-defense-style2.drawio`
- 每种风格**单独调用** drawio2pptx 导出
- 不要尝试把多种风格写入同一个 drawio 文件

---

#### 坑 #8：每页 mxCell 数量不得过少

- 每个 `<diagram>` 内容页（非封面/目录/节标题页）**必须包含 15 个以上 mxCell**（含背景、标题、正文、色块、装饰等）
- 节标题过渡页至少 8 个 cell；封面页至少 12 个 cell
- **绝对禁止出现只有 1~3 个 cell 的内容页**——这意味着内容未被正确写入该页，必须检查并补全

写入文件前可用以下脚本自验：
```python
import xml.etree.ElementTree as ET
root = ET.parse('paper-defense.drawio').getroot()
for d in root:
    cells = [c for c in d.find('mxGraphModel/root') if c.get('id') not in ('0','1')]
    print(d.get('name'), len(cells))
```

---

#### 坑 #9：浮层元素遮挡正文

**问题**：将带背景色的装饰元素（按钮/标签/图标）放在两列卡片之间的 x 坐标，y 区间与卡片文字重叠，导致遮挡正文。

**典型场景**：「研究问题」金色按钮 `x=760, width=400`，横跨左右两个宽 840 的卡片中间，遮挡右卡片内容。

**检查方式**：装饰元素的 `[x, x+width]` 区间若与相邻文字卡片 x 区间重叠，且 y 区间也重叠 → 必须修改。

**规则**：
- 装饰性标签/按钮只能放在卡片**内部**（内边距范围内）或卡片**正下方独立区域**
- 两列卡片之间的连接说明改用 `fillColor=none` 纯文字行，不加背景色
- z 层顺序（id 写入顺序）：背景色块 → 卡片底色 → 正文文字 → 最后写装饰，越重要越靠后

```xml
<!-- ❌ 错误：按钮悬浮两卡片中间，遮挡文字 -->
<mxCell id="badge" value="研究问题" style="...fillColor=#C9A84C;...">
  <mxGeometry x="760" y="320" width="400" height="60"/>
</mxCell>

<!-- ✅ 正确：移到卡片下方，改为无背景文字行 -->
<mxCell id="label" value="▼　核心研究问题" style="text;...fontColor=#C9A84C;fillColor=none;...">
  <mxGeometry x="660" y="618" width="600" height="44"/>
</mxCell>
```

---

#### 坑 #10：卡片高度不足，文字溢出底部

**问题**：卡片背景色块高度未考虑实际换行后的文字行数，正文溢出卡片底部被视觉截断。

**根本原因**：`whiteSpace=wrap` 让文字自动换行，但背景色块不会自动撑高，必须手动预算。

**高度计算公式**：
```
卡片总高度 = 上内边距(20) + 标题行高(字号×2) + 分隔线(6) + 正文行数×字号×1.6 + 下内边距(24)
```

**快速参考（正文字号 19~20pt）**：

| 正文行数 | 正文区最小高度 | 卡片建议总高度（含标题） |
|---------|------------|---------------------|
| 1 行 | 40px | 130px |
| 2 行 | 70px | 170px |
| 3 行 | 110px | 210px |
| 4 行 | 150px | 260px |
| 5 行 | 190px | 300px |

> **原则：宁可偏高留白，不可偏矮截文。**

**规则**：
1. 生成前估算正文字数 ÷ (卡片宽度 / 字号 × 0.55) ≈ 行数，代入公式
2. 文字容器底边（y + height）必须 ≤ 卡片底边（卡片 y + 卡片 height）− 20px
3. 多列并排卡片（2×2、1×N）统一使用相同高度，不参差

```xml
<!-- ❌ 错误：卡片高220，4行正文实际需要~230px，溢出 -->
<mxCell id="card_bg" style="...fillColor=#1B2A4A;">
  <mxGeometry x="80" y="190" width="840" height="220"/>
</mxCell>
<mxCell id="card_body" style="text;...fontSize=20;">
  <mxGeometry x="100" y="252" width="800" height="120"/>  <!-- 底边372，卡片底410，看似够但文字已换行超出 -->
</mxCell>

<!-- ✅ 正确：卡片高270，文字容器高180，底边432 < 卡片底460，余28px -->
<mxCell id="card_bg" style="...fillColor=#1B2A4A;">
  <mxGeometry x="80" y="190" width="840" height="270"/>
</mxCell>
<mxCell id="card_body" style="text;...fontSize=19;">
  <mxGeometry x="100" y="252" width="800" height="180"/>
</mxCell>
```

---

## Step 3 & 4：输出 Draw.io 并自动导出 PPT（两种模式共用）

### Step 3：输出 Draw.io 文件

将生成的 XML 写入工作区 `.drawio` 文件（论文答辩用 `paper-defense.drawio`，通用汇报用 `general-presentation.drawio`），并简述每页概要。

> 写入注意见坑 #5。

### Step 4：自动导出 PPT（必执行）

生成 `.drawio` 后，**必须**自动执行：

1. `pip install drawio2pptx -q`
2. 切换到 `.drawio` 文件所在目录（**必须先 cd/Set-Location，否则找不到文件**）：
   ```powershell
   Set-Location "d:\你的项目目录"
   drawio2pptx <文件名>.drawio <文件名>.pptx
   ```
3. 验证输出：`dir <文件名>.pptx`，确认文件存在且页数正确（输出中有 `Saved xxx.pptx (N slides)`）
4. 若失败，提示用户手动执行

> 页数验证见坑 #6。

### 其他注意事项

- XML 标签正确闭合，特殊字符转义（`&`→`&amp;`，`<`→`&lt;`）
- 每页布局：背景全画布矩形、标题区 44–56pt、正文 24–32pt、留白充足
- Windows 下不支持 `tail` 命令，Shell 输出截断请用 PowerShell 的 `Select-Object -Last N` 替代