---
name: bazi-ziwei
description: 八字 + 紫微斗数 AI 排盘与综合分析。当用户提供生辰（阳历/农历日期、时辰、性别）询问八字、紫微、命理、命盘、流年大运相关问题时使用。基于 mingpan（Apache-2.0）+ iztro（MIT）两个独立开源排盘库 + enrichBazi 补全层精准排盘（杜绝 LLM 自行排盘出错），支持按需独立分析八字 / 独立分析紫微 / 两盘交叉印证。
---

# 八字 + 紫微斗数综合分析 Skill

## 何时触发

用户场景：
- 提供出生时间（"我是 2000-01-01 中午 12:00 男"）并希望分析
- 询问"帮我看八字 / 看紫微 / 算命 / 看命盘 / 看流年大运"
- 提供命盘文本（文墨天机、紫微斗数排盘软件导出格式）希望深度解读
- 询问特定大运/流年的吉凶

**不触发**：单纯的星座 / 塔罗 / 周公解梦 / 风水 / 姓名学。

## 必需输入

```
公历或农历日期 (YYYY-MM-DD)
出生时刻 (HH:MM, 24 小时制)
性别 (男/女)
```

若用户没给时辰，**必须主动询问**，不要默认子时。时辰对四柱日柱和紫微命宫影响极大。

> 不需要出生地。排盘直接使用钟表时间，不做真太阳时经度校正。

---

## 执行流程

### Step 0 — 决策门（开场必做，无例外） ⭐

**这一步不能跳，不能凭用户措辞自行判断意图后直接执行**。哪怕用户说的是"生成一个XXX男命的报告"、"给我看看XXX的命盘"这种听起来已经在指定具体产出物的话，也必须先问完下面的问题、等用户明确回复后，才能进入 Step 1。

> ❌ 错误示范：用户说"生成一个1990年男命"，Agent 直接默认走综合印证+海报模式并开始排盘。
> ✅ 正确做法：不管用户怎么问，先回问题1（要哪种分析），用户选了3再回问题2（要哪种呈现形态），拿到明确答复后再动手。

**问题 1：要看哪种命理？**
> "我可以做三种分析：
> 1. **八字独立分析**（事业 / 财运 / 婚恋 / 子女 / 六亲 / 健康，按八字格局推演 — 长文输出）
> 2. **紫微独立分析**（十二宫 + 大限 + 生年四化 + 流年 — 长文输出）
> 3. **八字 + 紫微综合印证**（两盘交叉对账 — 提供长文 / 可视化海报 / 两种都要）"

**如果用户选 3，再追问问题 2：呈现形态**
> "综合印证可以这样输出：
> A. **📜 长文深度版**（Markdown 散文，沉浸阅读）
> B. **🎴 结构化海报版**（单文件 HTML，可截图分享）
> C. **两种都要**"

**根据选择加载相应提示词和模板**：

| 用户选 | 加载提示词 | 模板 | 输出 |
|---|---|---|---|
| 1 | `prompts/bazi-prompt.md` | — | Markdown 对话回复 |
| 2 | `prompts/ziwei-prompt.md` | — | Markdown 对话回复 |
| 3 + A | `prompts/zonghe-yinzheng-prompt.md` | — | Markdown 对话回复 |
| 3 + B | `prompts/zonghe-poster.md` | `templates/report-zonghe-poster.html` | `<name>-zonghe.html` |
| 3 + C | 上述两份都跑 | 同上 | Markdown + HTML 两份 |

> **海报模板仅综合印证一种**。八字独立 / 紫微独立只有长文输出（用户深度阅读用）。这是经过设计的——海报是综合印证独占的杀手锏，承担社交分享 + 用户惊艳的角色。

---

### Step 1 — 排盘（算法层，产出 JSON）

**绝对不要让 AI 自己排八字或紫微**。必须调用算法层脚本：

```bash
cd calculator
npx tsx run-chart.ts --year=YYYY --month=MM --day=DD --hour=HH --minute=MM --gender=male > chart.json
```

**注意**：`run-chart.ts` 的 stdout 是纯 JSON，stderr 是 debug 信息。**重定向时只取 stdout**（`> chart.json`），不要 `2>&1`。

脚本输出 JSON：
- `bazi`：四柱 / 十神 / 星运 / 自坐 / 纳音 / 藏干 / 大运（含 startAge/endAge/startYear/endYear）
- `bazi.enrichment`：格局 / 旺衰 / 调候 / 五行旺相 / 五行统计 / 天干关系 / 地支关系 / 整柱判定
- `ziwei`：十二宫 / 生年四化 / 大限 / 阴阳 / 五行局 / 命主身主

> **关键约束**：纯 LLM 排盘会错排日柱 → 日主 → 格局 → 用神，全链失真。算法层不可绕过。

---

### Step 2 — 文本盘转换（算法层，产出可读文本）

LLM 读 JSON 不如读结构化文本。把 Step 1 的 JSON 转成文墨天机风格的树状文本：

```bash
npx tsx dump-text.ts --input=chart.json --output=chart.txt
```

文本盘包含：
- 紫微部分：基本信息 + 生年四化 + 十二宫（含主星 / 辅星 / 大限 / 流年）
- 八字部分：四柱（含藏干十神 / 星运 / 自坐 / 纳音）+ 大运 + 算法补层（格局 / 旺衰 / 调候 / 关系 / 整柱）

将 `chart.txt` 内容连同对应提示词一起送给 LLM 做分析。

---

### Step 3 — 分析（按 Step 0 用户选择执行对应分支）

#### Step 3 — 长文版（用户选 1 / 2 / 3+A / 3+C）
读取对应长文提示词（`bazi-prompt.md` / `ziwei-prompt.md` / `zonghe-yinzheng-prompt.md`），喂入 `chart.txt`，输出 Markdown 长文。

> 综合印证（3+A）的前置条件：先跑八字 + 紫微独立分析拿到中间报告，再喂给 `zonghe-yinzheng-prompt.md`。
> 如输出被截断，分段输出。

#### Step 3 — 海报版（仅用户选 3+B 或 3+C）
1. 读取 `prompts/zonghe-poster.md`，喂入 `chart.txt`
2. LLM **必须输出严格 JSON**（不是 Markdown）——提示词末尾会要求"直接以 `{` 开头"，照办即可
3. 把 LLM 输出的 JSON 保存为 `analysis.json`
4. 调用渲染脚本：
   ```bash
   cd calculator
   npx tsx render.ts \
     --chart=chart.json \
     --analysis=analysis.json \
     --template=../templates/report-zonghe-poster.html \
     --output=<user-name>-<date>.html \
     --currentYear=<YYYY>
   ```
5. 把生成的 HTML 文件路径告诉用户，让其用浏览器打开

> **重要**：海报版的视觉由 HTML 模板决定，**LLM 只产数据不产 HTML**。如果 LLM 输出含 markdown 包装（如 \`\`\`json … \`\`\`），渲染前需剥掉。

---

## 安装后行为（重要）

**装好 Skill 后不要主动跑任何验证 / 自检命令。** 不要试 Smoke Test、不要排示例盘、不要分析示例命主。装好就是装好，等用户来给生辰再开始工作。

> 自检命令由人工按需运行，不在 Agent 的职责范围内。Agent 主动跑会浪费 token + 触发上下文压缩。

依赖检查（仅在用户首次提供生辰、Agent 准备跑 run-chart.ts 报错时）：
```bash
cd <skill-root>/calculator
ls node_modules >/dev/null 2>&1 || npm install
```
也就是说，依赖问题**报错时再修**，不要装好就主动检查。

---

## 关键约束

1. **装好不自检**：见上节"安装后行为"。不要主动跑示例排盘 / 自检 / smoke test
2. **决策门必做，措辞不能当借口**：永远先问用户要哪种分析，哪怕用户说"生成一个/给我一份"这类听起来已经指定产出物的话，也不能跳过直接默认走海报模式。避免无意义的 token 消耗 + 输出截断
3. **排盘必须走算法层**：不要徒手算四柱、紫微宫位、大限。错一步全盘垮
4. **不引入命盘外变量**：风水、姓名、阳宅、紫白飞星不在本 Skill 范围
5. **冲突要说出来**：八字与紫微出现矛盾信号时按综合印证提示词的 4 条规则判定，不和稀泥
6. **置信度自评**：边界情况（旺衰临界、格局模糊、两盘对立）必须标"置信度：低"
7. **不替用户做决策**：投资、择偶、医疗、堕胎等决策类问题，给信号不给指令
8. **敏感问题拒答**：下蛊、断人财路、害人命运等违禁内容直接拒绝
9. **免责声明**：分析末尾必带"仅供文化研究与娱乐参考"

---

## 文件清单

```
├── SKILL.md                          ← 本文件
├── calculator/
│   ├── run-chart.ts                  ← 入口：生辰 → JSON（stdout 纯 JSON / stderr debug）
│   ├── dump-text.ts                  ← JSON → 文墨天机风文本
│   ├── render.ts                     ← 渲染脚本：chart.json + analysis.json + 模板 → HTML
│   ├── package.json                  ← 算法层依赖声明
│   ├── engine/                       ← 排盘引擎：对接 mingpan(八字,Apache-2.0) + iztro(紫微,MIT)
│   └── bazi-enrich/                  ← enrichBazi 补层（格局/旺衰/调候/关系/整柱）
├── prompts/
│   ├── bazi-prompt.md                ← 八字独立分析（长文）
│   ├── ziwei-prompt.md               ← 紫微独立分析（长文）
│   ├── zonghe-yinzheng-prompt.md     ← ⭐ 综合印证（长文）
│   └── zonghe-poster.md              ← ⭐ 综合印证（海报版 JSON 输出）
└── templates/
    ├── report-zonghe-poster.html     ← 综合印证海报模板（占位符）
    ├── UI-DESIGN.md                  ← 视觉设计文档
    └── OUTPUT-SCHEMA.md              ← 输出结构规范
```

**注**：HTML 渲染目前**仅支持综合印证模式**。如用户选了八字独立 / 紫微独立又问"能不能出 HTML 报告"，告知"目前 HTML 海报仅对综合印证开放，建议选综合印证（含八字+紫微）以拿到海报"。

---

## 工作示例

**用户**：我是 2000 年 1 月 1 日 12:00 出生的男生，帮我看下命盘。

**Skill 应该走**：
1. 信息确认（日期/时辰/性别 ✅）
2. **决策门**："想要八字分析 / 紫微分析 / 综合印证？"
3. 用户回 "八字"：
   - Step 1：跑 `run-chart.ts` 产出 `chart.json`
   - Step 2：跑 `dump-text.ts` 产出 `chart.txt`
   - Step 3a：加载 `prompts/bazi-prompt.md` + 喂入 `chart.txt` → 输出八字分析
4. 提醒"若要紫微 / 综合印证可随时追问"

---

## 失败模式与处理

| 现象 | 原因 | 处理 |
|---|---|---|
| 排盘脚本报错 | 日期超 1900-2100 / 时辰格式错 | 询问用户校正 |
| AI 想"凭记忆排盘" | 偷懒走捷径 | **拒绝**。算法层是不可绕过的硬约束 |
| 输出被截断 | 三段一锅出超 token 上限 | 回到决策门，拆分输出 |
| 算法层和用户其他软件结果不一致 | 命名流派差异（建禄格 vs 比肩格） | 按算法层 `notes` 解释，不偷换说法 |
| Windows + 中文路径 + PowerShell 编码错乱 | 平台特性 | 在 cmd / git bash / WSL 下运行，避免 PowerShell |

---

## 开源致谢

排盘算法层基于以下独立开源项目（均为真实、可验证的 LICENSE 文件，非徽章声明）：
- 八字排盘：[mingpan](https://github.com/ChesterRa/mingpan)（Apache-2.0）
- 紫微斗数排盘：[iztro](https://github.com/SylarLong/iztro)（MIT）

---

## 免责声明（每次输出末必带）
> 本分析基于传统八字与紫微斗数理论框架，仅供文化研究与娱乐参考，不构成医疗、投资、婚姻、法律等任何决策依据。命运由个人选择与客观环境共同塑造。
