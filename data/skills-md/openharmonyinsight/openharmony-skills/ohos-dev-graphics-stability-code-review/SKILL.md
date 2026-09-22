---
name: ohos-dev-graphics-stability-code-review
description: >
  C/C++ 稳定性代码审查框架，覆盖 5 个稳定性分类（异常处理、并发稳定性、资源管理、边界条件、图形稳定性）共 34 条规则。
  触发场景：稳定性专项全仓扫描、代码上库前本地检视、稳定性审计、故障预防检视、代码审查、OpenHarmony 稳定性扫描、
  以及用户要求检查 C/C++ 代码稳定性风险时均应使用此技能。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: graphics
  capability: stability-code-review
  version: 0.2.1
  status: trial
  tags:
    - cpp
    - stability
    - review
---

# OpenHarmony Stability Code Review

可扩展的稳定性规则检视框架，对 C/C++ 代码库执行稳定性风险检视并生成结构化报告。规则以 Markdown 文档存放在 `references/` 目录，AI 模型直接读取规则文档进行检视，输出中文检视报告到 `./report/` 目录。详细工作流、核心概念和操作细节请参考 [references/WORKFLOW_GUIDE.md](references/WORKFLOW_GUIDE.md)。

## 触发场景

- **稳定性专项全仓扫描**：对 C/C++ 代码库执行稳定性审计或风险检视
- **指定规则扫描**：用户明确指定规则 ID、级别或分类进行针对性检视
- **代码上库前本地检视**：在代码提交前进行稳定性检视
- 检测稳定性风险（异常处理不当、并发死锁、性能退化、资源泄漏等）
- 审查生命周期管理（对象生命周期、异步任务管理）
- 用户明确要求检查代码稳定性时

**触发示例**：

```
# 全量扫描
稳定性全量扫描 ./rosen/
代码稳定性检视 ./src/

# 指定规则扫描
用 ExceptionHandling_001 规则检视 ./src/
用 ExceptionHandling_001,ExceptionHandling_002,BoundaryCondition_001 规则检视 ./rosen/

# 按级别过滤扫描
对 ./rosen/ 做稳定性扫描，只检视 HIGH 级别的规则

# 指定分类扫描
对 ./src/ 做稳定性扫描，只检视异常处理分类的规则
用BoundaryCondition和GraphicsStability分类的规则检视 ./rosen/
```

## NEVER

1. **永远不要修改被扫描的源代码** — 你的工作只是检视代码，识别稳定性风险，禁止对源代码文件进行任何修改操作
2. **不要输出非必要的过程中间件** — 除了目标输出的中文检视报告之外，不要输出其它非必要的过程中间文件或临时文件
3. **永远不要报告没有可复现 RiskFlow 和 ImpactAnalysis 的检出** — 缺少风险流和影响分析的检出是无效的，必须说明来源、传播和后果
4. **永远不要在应用白名单之前标记 test、mock、generated、build 或 protobuf 文件** — 必须先执行白名单过滤再进行规则检视
5. **永远不要将崩溃、内存损坏、资源耗尽或 GPU 资源泄漏降级为风格问题** — 严重程度由后果决定，不由代码外观决定
6. **永远不要静默跳过用户请求的规则 ID** — 无效或不存在的规则必须在开始检视前报告给用户
7. **永远不要合并底层风险路径或规则 ID 不同的检出** — 同位置但不同规则或不同风险传播路径的问题应分别保留

## 渐进式加载触发器

根据扫描场景精确控制加载内容，避免过度加载或不足加载：

### 全量扫描

**必须加载**：`config/rules.yaml`、`config/whitelist.yaml`、`references/RULE_INDEX.md`、所有启用的规则文档、`references/PROBLEM_TEMPLATE.md`、`references/REPORT_TEMPLATE.md`、`references/REPORT_TEMPLATE.csv`

**不要加载**：`references/RULE_DEVELOPMENT_GUIDE.md`、`references/RULE_TEMPLATE.md`、`references/WORKFLOW_GUIDE.md`（除非你对流程有疑问）

### 指定规则扫描

**必须加载**：`config/rules.yaml`、`config/whitelist.yaml`、用户指定的规则文档、`references/PROBLEM_TEMPLATE.md`、`references/REPORT_TEMPLATE.md`、`references/REPORT_TEMPLATE.csv`

**不要加载**：未指定的规则文档、`references/RULE_DEVELOPMENT_GUIDE.md`、`references/RULE_TEMPLATE.md`

### 分类扫描

**必须加载**：`references/RULE_INDEX.md`、`config/whitelist.yaml`、该分类下的规则文档、`references/PROBLEM_TEMPLATE.md`、`references/REPORT_TEMPLATE.md`、`references/REPORT_TEMPLATE.csv`

**不要加载**：其他分类的规则文档、`references/RULE_DEVELOPMENT_GUIDE.md`、`references/RULE_TEMPLATE.md`

### 新增/修改规则

**必须加载**：`references/RULE_DEVELOPMENT_GUIDE.md`、`references/RULE_TEMPLATE.md`、`config/rules.yaml`

**不要加载**：规则检视文档和报告模板（除非同时进行检视）

## 工作流决策树

```
用户输入
  │
  ├─ 指定规则 ID？ ──→ 解析 ID 列表，验证有效性 → 加载对应规则文档
  ├─ 指定级别？ ──→ 从 rules.yaml 筛选匹配级别 → 加载对应规则文档
  ├─ 指定分类？ ──→ 从 RULE_INDEX.md 筛选匹配分类 → 加载对应规则文档
  └─ 未指定？ ──→ 加载 rules.yaml 所有启用规则 → 加载全部规则文档
  │
  ▼
加载 config/whitelist.yaml，初始化白名单过滤
  │
  ▼
按稳定性分类启动 5 个 Subagent 并行检视
每个 Subagent：白名单过滤 → 遍历规则 → RISK_PATTERN → CONTEXT → IMPACT → 安全写法排除 → 按 PROBLEM_TEMPLATE.md 格式输出
  │
  ▼
主 Agent 汇总：收集 → 格式验证 → 去重合并 → 按严重程度分组排序（CRITICAL→HIGH→MEDIUM→LOW）
  │
  ▼
输出报告到 ./report/ 目录
  ├── report_{target}_{timestamp}.md  （按 REPORT_TEMPLATE.md）
  └── report_{target}_{timestamp}.csv （按 REPORT_TEMPLATE.csv）
```

详细工作流图示、核心概念定义和操作细节请参考 [references/WORKFLOW_GUIDE.md](references/WORKFLOW_GUIDE.md)。

## 输出合约

| 项目 | 要求 |
|------|------|
| 问题格式 | 严格遵循 `references/PROBLEM_TEMPLATE.md`，必须包含：标题、分类、规则、位置、函数、严重程度、关键源码、问题描述、RiskFlow、ImpactAnalysis、修复建议 |
| 报告格式 | Markdown 报告遵循 `references/REPORT_TEMPLATE.md`，CSV 报告遵循 `references/REPORT_TEMPLATE.csv` |
| 输出路径 | 默认 `./report/`，用户可指定其他路径；若目录不存在则先创建 |
| 去重规则 | 同位置同规则问题合并；不同规则或不同风险路径的问题保留 |
| 规则覆盖 | 必须遍历所有指定或启用的规则，不得遗漏；无效规则 ID 必须在检视前报告 |

## 项目结构

```
├── SKILL.md                       # 技能说明（本文件，紧凑路由）
├── README.md                      # 项目说明
├── config/
│   ├── rules.yaml                 # 规则配置
│   └── whitelist.yaml             # 白名单配置
├── references/
│   ├── RULE_INDEX.md              # 规则总索引
│   ├── WORKFLOW_GUIDE.md          # 工作流详细指南
│   ├── RULE_DEVELOPMENT_GUIDE.md  # 规则开发指南（仅规则开发时加载）
│   ├── RULE_TEMPLATE.md           # 规则文档模板（仅规则开发时加载）
│   ├── PROBLEM_TEMPLATE.md        # 检出问题格式模板
│   ├── REPORT_TEMPLATE.md         # 报告格式模板（Markdown）
│   ├── REPORT_TEMPLATE.csv        # 报告格式模板（CSV）
│   ├── ExceptionHandling/         # 异常处理（2条）
│   ├── ConcurrencyStability/      # 并发稳定性（1条）
│   ├── ResourceManagement/        # 资源管理（5条）
│   ├── BoundaryCondition/         # 边界条件（14条）
│   └── GraphicsStability/         # 图形稳定性（12条）
└── scripts/
    └── add-rule.py                # 规则脚手架工具
```
