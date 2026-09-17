---
name: sdlc-intent
description: Digests and health-checks product requirement documents (PRD). Stage 1 produces a structured digest (roles, concepts, feature map, flow diagrams, state machines) to build shared understanding; stage 2 audits the requirement against a six-layer defect taxonomy and produces a graded issue report plus a PM clarification checklist. Use when the user shares a requirement/PRD document (Feishu/wiki link or local file) and wants to understand it, prepare for design, or find problems before development. 触发词：需求文档、需求梳理、需求体检、需求评审、产品需求、帮我理解这个需求、sdlc-intake、PRD digest、requirement audit.
---

# 需求接收助手（sdlc-intent）

两段式：**第一段梳理**建立对需求的共识理解，**第二段体检**尽早暴露需求缺陷。梳理是体检的前提——先与用户对齐理解，再找问题。

## 选择工作流

按用户意图选择分支：

- 用户说「梳理 / digest / 理解需求」，或**首次**给出需求文档 → 只跑【第一段：需求梳理】，跑完暂停
- 用户说「体检 / 评审 / 找问题 / review」→ 跑【第二段：需求体检】；若已存在梳理文档（`sdlc/*/intake/digest-*.md`）优先复用，不存在则提示先梳理
- **复用梳理文档前强制版本校验**：体检本身要重新读取原文，读取后将本次原文的版本/修订时间与梳理文档头「版本」字段比对——一致 → 直接复用；不一致 → 告知用户「原文已从 vX 更新至 vY，梳理文档基于旧版」，建议重梳理（用户明确说沿用才沿用）；原文无版本信息时，向用户展示梳理文档的梳理日期，请其确认原文是否有更新
- 用户只给文档未指明 → 两段连跑：梳理完成后**暂停**，向用户展示摘要并提示「请确认或补充业务理解，完成后说“继续体检”」，得到确认再跑体检

## 输入读取

- 飞书链接（feishu.cn / doubao.com 的 /docx/、/wiki/）：`lark-cli docs +fetch --doc "<URL>" --doc-format markdown`（权限不足时向用户说明，不要反复重试）
- 飞书链接在读取正文后**必须**同步读取评论区：`lark-cli drive +list-comments --url "<URL>" --solved-status all --comment-scope all --need-relation --format json`（权限不足时同样只向用户说明一次、不重试，正文流程照常继续）
- 评论区是正文的补充信息源，正文外的关键决策/变更说明/答疑常在评论区；评论结论与正文不一致时以最新评论为准。本地文件输入或评论数为 0 时记「无评论」，权限不足记「未读取（原因）」，均如实写入梳理文档头「评论区」字段
- 本地 markdown/text 文件：直接 Read
- 文档内嵌表格已随正文返回；若正文出现 `<sheet>`/`<bitable>` 引用且与核心流程相关，用 lark-sheets/lark-base 下钻读取（有权限时）
- 原文内容（正文 + 评论区）在后续体检阶段还要反复引用，梳理时先在本地留存原始内容（如 `/tmp/` 下临时文件；评论 JSON 与正文 markdown 分开存放）

## 第一段：需求梳理

复制此 checklist 跟踪进度：

```
梳理进度：
- [ ] Step 1: 通读原文，提取角色与术语
- [ ] Step 2: 按 references/digest-template.md 生成 8 区块梳理文档
- [ ] Step 3: 落盘 sdlc/<需求名>/intake/digest-<YYYYMMDD>.md
- [ ] Step 4: 终端展示摘要 + 暂停等待用户确认
```

**Step 2** 是核心：读取 [references/digest-template.md](references/digest-template.md)，严格按模板 8 区块产出，功能地图、流程图、状态机、规则表必须图表化（markdown 表格 + mermaid）。

**梳理纪律**（违反即返工）：
- 忠实转述原文，**不评价、不脑补、不优化**——评价是体检阶段的事
- 原文缺失的流转/触发/字段，用 ❓ 标注，**禁止自行补全**
- 对模糊内容的个人理解，逐条记入「假设清单」区块（编号 + 原文位置 + 按 X 理解），并标注类型（推断 = 有原文推导链 / 假设 = 无依据拍板）
- §7 关键规则逐条编 FR 号、状态机图每条流转须有原文出处——编号与出处纪律详见 digest-template 标注约定（FR 编号稳定性、ID 命名空间、评论区判定口径均以模板为权威）

**Step 3** 落盘路径：当前项目 `sdlc/<需求名>/intake/` 目录（不存在则创建），文件名 `digest-<YYYYMMDD>.md`。

**Step 4** 暂停：展示各区块摘要（尤其 ❓ 集中处和假设清单），明确说「请确认或补充业务理解，完成后说“继续体检”」，然后**停止等待**。

## 第二段：需求体检

复制此 checklist 跟踪进度：

```
体检进度：
- [ ] Step 1: 准备输入（原文 + 梳理文档，含用户补充）
- [ ] Step 2: 按 references/dimensions.md 六层维度逐层检查
- [ ] Step 3: 按 references/report-template.md 产出体检报告 + PM 确认清单
- [ ] Step 4: 终端摘要（各级问题数 + 阻断项列表）
- [ ] Step 5: 交互收尾（用户逐条回应后回写梳理文档）
```

**Step 2** 读取 [references/dimensions.md](references/dimensions.md)，按层序检查：概念层最先（术语表是后续所有检查的基准），文档质量层最后。该文件定义了每个检查项的命中标准与严重度。

**体检纪律**：
- 每条命中必须附**原文定位**（章节名 + 关键引文片段），禁止脱离原文泛泛而谈
- 六层维度是启发式锚点而非封闭清单：发现维度外的问题也应记录，标注维度为「补充」
- 严重度从严不从宽：拿不准阻断还是严重时，标高一级并在描述中说明

**Step 3** 读取 [references/report-template.md](references/report-template.md)，产出两个文件到 `sdlc/<需求名>/intake/`：
- `audit-<YYYYMMDD>.md`（五章结构：执行摘要/阻断速览/分层明细/主题关联/状态汇总——唯一的成段文字在执行摘要，其余表格化）
- `pm-checklist-<YYYYMMDD>.md`（可直接整篇复制发给产品经理的确认清单）

两个文件产出后，**必须**按 report-template.md 的「终检」清单核对（统计表重数 / 跨文件计数一致 / 主题组关联核对），通过后才进入 Step 4。

**Step 5** 交互收尾：引导用户对每条问题回应「问 PM」/「按假设 X 处理」/「忽略」；有结论后将其回写至梳理文档的假设清单，形成共识版。用户不想逐条过时直接结束，不强制。

## 边界

- 本 skill 只处理需求文档本身，不读代码库、不做技术设计（设计属后续任务）
- 体检只审需求本身的质量，**不评估技术方案的合理性**（方案合理性属后续技术设计评审范围）
- 一次处理一份需求文档；多份文档时请用户明确主文档
- 产出语言跟随需求文档语言（中文文档产出中文）
