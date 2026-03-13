---
name: skill-creator
description: 创建新 skills、改造已有 skills、并通过评测闭环持续优化。用户只要提到“做一个 skill”“改造 skill”“跑评测/benchmark”“验证 skill 效果”“优化 description 触发率”等场景，都应优先使用此技能。
---

# Skill Creator

用于“创建 -> 评测 -> 迭代 -> 优化触发”的完整工作流技能。

## 先对齐用户阶段

先判断用户当前在哪个阶段，再补齐下一步：

- 还在定义需求：先澄清目标、触发场景、输出标准
- 已有草稿：直接进入测试与迭代
- 已有多轮结果：重点做诊断与重构，而不是重写一遍

如果用户明确说“不需要完整评测流程”，可降级为轻量协作；否则默认走标准闭环。

## 与用户沟通风格

根据用户熟悉度调节术语密度：

- 可直接使用：`evaluation`、`benchmark`
- 对 `JSON`、`assertion` 等术语，若用户没有明显技术背景，先用一句话解释再使用

目标是“专业但不堆术语”。

---

## 一、创建 Skill

### 1) Capture Intent（先抽取上下文再提问）

若当前对话里已包含可复用流程，先从历史中提取：

- 用了哪些工具
- 步骤顺序是什么
- 用户纠正过哪些点
- 输入/输出格式长什么样

然后确认以下 4 点：

1. 这个 skill 要让 Claude 具体做成什么事？
2. 触发条件是什么（用户会怎么说）？
3. 预期输出格式是什么？
4. 是否需要测试用例？

默认建议：

- 可客观验证任务（文件转换、结构化提取、固定流程）建议有测试
- 主观创作任务（文风、设计偏好）可以先不做形式化断言

### 2) Interview & Research

主动补齐：

- 边界/异常情况
- 输入输出样例
- 依赖与运行环境
- 成功标准

测试提示词（eval prompts）在这一步完成前不要急着写。

### 3) 编写 SKILL.md

至少落实：

- `name`
- `description`（这是触发核心，必须写清“做什么 + 何时用”）
- 正文流程（必要步骤、工具用法、结果标准）

`description` 要稍偏“主动触发”，避免 under-trigger。

示例（表达方式）：

- 弱：`用于生成仪表盘`
- 强：`用于生成仪表盘。凡是用户提到 dashboard、指标可视化、看板、业务监控、数据展示，即便没说“仪表盘”，也应触发此技能。`

### 4) Skill 结构原则

```
skill-name/
├── SKILL.md (required)
└── optional resources
    ├── scripts/
    ├── references/
    └── assets/
```

渐进披露：

1. 元数据（name/description）总在上下文
2. `SKILL.md` 触发后加载（建议 <500 行，必要时可超）
3. `scripts/references/assets` 按需读取

设计要点：

- 若接近 500 行，把变体细节下沉到 `references/`
- `SKILL.md` 中要明确指向这些参考文件，告诉模型何时读
- 参考文件 >300 行建议提供目录

### 5) 安全与可预期

- 不得包含恶意代码、提权、未授权访问、数据外传流程
- Skill 的真实行为应与描述一致，不做“隐式意图”

### 6) 编写风格

- 以祈使句描述动作
- 少用机械化 `MUST`，多解释“为什么要这样做”
- 指令应可泛化，不要对少量样例过拟合

---

## 二、测试用例与评测闭环

写完草稿后，先准备 2-3 条真实用户风格测试提示词，并与用户确认。

把测试集存到 `evals/evals.json`（先写 prompts，断言可后补）：

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

完整 schema 见 `references/schemas.md`。

### 强制顺序：不要中途停

不要使用 `/skill-test` 或其他测试 skill；按下面连续完成。

工作目录规范：

- 在 skill 同级创建 `<skill-name>-workspace/`
- 迭代分目录：`iteration-1/`, `iteration-2/`
- 每条 eval 单独目录：`eval-0/`, `eval-1/`
- 仅在需要时创建目录，不要一次性全部建完

### Step 1：同一轮同时启动 with-skill 与 baseline

每个测试用例同轮启动两路：

- `with_skill`
- baseline

基线策略：

- 新建 skill：baseline = `without_skill`
- 改造现有 skill：baseline = 旧版本快照（`cp -r <skill-path> <workspace>/skill-snapshot/`）

每个 eval 写 `eval_metadata.json`（此时 assertions 可先空）：

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2：运行期间补断言

不要干等任务结束。并行完成：

- 草拟可客观验证的 assertions
- 向用户解释每条断言检验什么
- 更新 `eval_metadata.json` 与 `evals/evals.json`

主观任务不强行量化；以人工评审为主。

### Step 3：任务完成即记录时延/Token

子任务完成通知里会出现 `total_tokens` 与 `duration_ms`，这是唯一可靠来源。必须立即写入各运行目录 `timing.json`：

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Step 4：评分、聚合、分析、展示

1. **评分（grading）**  
逐 run 生成 `grading.json`。数组字段必须是 `text`、`passed`、`evidence`（viewer 依赖这些字段名）。

2. **聚合 benchmark**  
在 `skills/skill-creator/` 目录运行：

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

生成 `benchmark.json` 与 `benchmark.md`。

3. **分析（analyst pass）**  
结合 `agents/analyzer.md` 检查：

- 非区分性断言（各方案都通过）
- 高方差/可能 flaky 的评测
- 时延与 token 的权衡

4. **生成评审 viewer（必须）**  
使用官方脚本，不要自造 HTML：

```bash
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
VIEWER_PID=$!
```

如果是第 2 轮及以后，加 `--previous-workspace <workspace>/iteration-<N-1>`。

无图形/远程环境：使用 `--static <output_path>` 生成静态 HTML。用户点击提交后会下载 `feedback.json`，再拷回 workspace。

5. **通知用户评审入口**  
明确告诉用户：

- `Outputs` 看样例输出并填写反馈
- `Benchmark` 看量化对比

### Step 5：读取反馈并收尾

用户评审完成后读取 `feedback.json`，优先处理有明确投诉的用例；空反馈视为通过。

结束后关闭 viewer：

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## 三、迭代改进（核心）

改进时遵守 4 条：

1. **从反馈提炼可泛化规则**，不要只修当前样例
2. **保持 prompt 精简**，删掉“高成本低收益”指令
3. **解释为什么**，让模型理解意图而不是死记规则
4. **发现重复劳动就产品化**：多次重复写出的 helper 脚本应沉淀到 `scripts/`

迭代循环：

1. 修改 skill
2. 在 `iteration-(N+1)` 重新跑全部测试与 baseline
3. 用 `--previous-workspace` 再开 viewer
4. 用户评审
5. 再迭代

停止条件：

- 用户明确满意
- 反馈基本为空
- 连续迭代无显著增益

---

## 四、进阶：盲测对比（可选）

需要更严格比较两个版本时：

- 读 `agents/comparator.md`
- 让独立 agent 在不知来源前提下比较输出
- 再用 `agents/analyzer.md` 分析胜因

多数场景下，人审 + benchmark 已够用。

---

## 五、Description 触发优化

`SKILL.md` frontmatter 的 `description` 决定触发概率。建议在 skill 稳定后再做。

### Step 1：构造触发评测集

准备 20 条 query（建议 8-10 条应触发 + 8-10 条不应触发）：

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

质量标准：

- 贴近真实用户输入（路径、字段名、上下文、错别字/口语都可）
- 负例要“近邻混淆”，不是明显无关句子
- 多做边界样例，少做教科书样例

### Step 2：让用户审阅 query

用模板 `assets/eval_review.html`：

1. 读取模板
2. 替换占位符：
   - `__EVAL_DATA_PLACEHOLDER__`
   - `__SKILL_NAME_PLACEHOLDER__`
   - `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. 写到临时 HTML（如 `/tmp/eval_review_<skill>.html`）并打开
4. 用户导出 `eval_set.json`
5. 从 `~/Downloads` 读取最新导出文件

### Step 3：跑自动优化循环

后台执行：

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

要点：

- 训练/测试拆分：60%/40%
- 每条 query 跑 3 次统计触发率
- 结果用 test score 选 `best_description`，避免过拟合 train
- 描述优化脚本通过当前会话的 `claude -p` 执行，不需要单独配置 `ANTHROPIC_API_KEY`

执行期间需定期向用户同步迭代进度与得分变化。

### Step 4：应用结果

- 用 `best_description` 回写 SKILL.md
- 向用户展示 before/after 与评分变化

### 触发机制补充

技能只会在 Claude 认为“有必要调用 skill”时触发。简单一步请求即使语义匹配，也可能不触发。  
因此触发评测 query 要足够“复杂且值得调用 skill”。

---

## 六、打包交付（可选）

如环境支持，执行：

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

然后返回 `.skill` 产物路径给用户。

---

## 七、Claude.ai 适配

在 Claude.ai（无子任务并发）场景：

- 测试用例改为串行执行
- 可跳过 baseline 对照
- 无法开浏览器时，在对话里直接展示结果并收集反馈
- 定量 benchmark 可降级，优先做人审
- `run_loop.py/run_eval.py` 依赖 CLI 能力，受环境限制时可跳过
- 若目标是“更新已有 skill”而非新建：保持原 skill 名称不变；若安装路径只读，先复制到 `/tmp/<skill-name>/` 再编辑与打包

---

## 八、Cowork 适配

在 Cowork 场景：

- 可使用子任务并行（严重超时时可降级串行）
- 无显示环境时必须使用 `generate_review.py --static`
- 反馈文件通过下载获得后，放回 workspace 继续下一轮
- `run_loop.py` / `run_eval.py` 通常可用，建议放在技能收敛后执行
- 不要忘记：先生成 viewer 给人审，再做你自己的深入分析
- 如果是更新已有 skill，同样遵循 Claude.ai 章节中的“保留原名称 + 先复制到可写目录”规则

---

## 九、参考文件

`agents/`：

- `agents/grader.md`：断言评分规范
- `agents/comparator.md`：盲测比较流程
- `agents/analyzer.md`：benchmark 诊断方法

`references/`：

- `references/schemas.md`：`evals.json`、`grading.json`、`benchmark.json` 等结构定义

---

## 十、核心闭环（再强调）

- 明确 skill 目标
- 起草或修改 skill
- 运行测试（with-skill + baseline）
- 产出 benchmark + viewer，先让用户评审
- 依据反馈迭代
- 收敛后再做 description 优化与打包
