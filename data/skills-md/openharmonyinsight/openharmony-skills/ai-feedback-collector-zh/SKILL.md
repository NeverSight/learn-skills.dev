---
name: ai-feedback-collector-zh
description: 当用户想要反馈、收集、整理、归类或模板化 AI 工具使用过程中的问题时使用此 skill，适用于编码 Agent、聊天助手、办公助手、搜索、写作、数据分析、内部 AI 系统等任意场景。该 skill 会把自由描述转换为结构化反馈报告，并输出明确的问题分类、标签、严重程度、场景、影响和补充信息建议。
---

# AI 问题反馈收集器

使用此 skill 将用户对 AI 工具使用问题的自然语言描述，整理成结构化、客观、便于统计和分派的问题反馈记录。

此 skill 的目标是“收集与规范化”，不是直接排障。需要保留用户原意，避免过度推断，并让输出可以直接粘贴到 issue 系统、表格、群聊、飞书多维表格或内部反馈平台中。

## 工作流程

1. 判断用户是否在反馈 AI 工具或 AI 辅助工作流中的问题。
2. 提取可观察事实：工具、任务、场景、失败表现、影响、业务上下文、环境信息。
3. 判断可能的问题分类：模型能力、环境/工具链、业务描述清晰度、流程协作、用户技能/培训、数据/权限、安全/合规或未知。
4. 区分事实与推测。缺失或无法安全判断的字段使用 `unknown`，不要编造。
5. 按下方模板输出结构化反馈。
6. 需要标准标签时，参考 `references/label-taxonomy.md`。
7. 如果信息不足，把问题放到“建议补充信息”中，不要默认打断用户反复追问，除非用户明确希望进行访谈式收集。
8. 将输出的标题和markdown格式的内容存储在文件`scripts/issue_output.json`中，方便后续创建issue。
9. 根据当前操作系统环境，选择scripts下的脚本将反馈通过webhook发送到指定的issue系统或反馈平台。
   1. Windows环境：检查是否安装了Python，如果安装了Python，运行`python scripts/create_issue.py`；如果没有安装Python，提示用户需要安装Python环境以自动创建issue，或引导用户在浏览器中手动创建issue：打开浏览器访问`https://gitcode.com/openharmonyinsight/ai-dev-feedback/issues/create`，根据`scripts/issue_output.json`中的标题和内容手动填写并提交。
   2. Linux环境：运行`bash scripts/create_issue.sh`。

## 输出模板

```markdown
## AI 使用问题反馈

### 标题
<用一句话概括问题。>

### 问题摘要
<基于用户描述，客观总结发生了什么。>

### 原始描述
<保留用户原话。>

### 使用场景
- 工具：`<工具名称或 unknown>`
- 场景：`<scenario 标签>`
- 任务类型：`<task 标签>`
- 工作流阶段：`<workflow-stage 标签或 unknown>`
- 受影响角色：`<角色或 unknown>`

### 问题分类
- 主分类：`<category 标签>`
- 次分类：`<category 标签或 none>`
- 分类置信度：`<high|medium|low|unknown>`
- 判断依据：<基于用户描述给出简短证据>

### 标签
- `tool:<value>`
- `category:<value>`
- `scenario:<value>`
- `task:<value>`
- `issue:<value>`
- `capability:<value>`
- `severity:<value>`
- `frequency:<value>`

### 影响
<描述对效率、质量、信任、成本或安全的影响；不清楚则写 unknown。>

### 可能原因
<可选。只列出合理假设，并明确不确定性。>

### 改进方向
<说明这条反馈可以如何帮助改进 AI 辅助研发，例如模型行为、工具集成、环境配置、提示词/流程设计、业务需求表达或开发者赋能。>

### 建议补充信息
- <有助于分派或定位问题的具体信息。>
- <有助于复现或判断影响范围的具体信息。>

### 建议分派方向
<可选一个或多个：产品体验、模型能力、工具集成、环境配置、业务分析、提示词/流程设计、权限/数据访问、文档/培训、安全/合规、unknown。>
```

## 标签规则

使用简短、机器可读的标签。标签值优先使用英文 lowercase kebab-case，便于统计和跨语言汇总。

必填标签族：

- `tool`：涉及的 AI 产品或 Agent。
- `category`：用于统计和改进规划的根因问题分类。
- `scenario`：大的使用场景。
- `task`：用户想完成的任务类型。
- `issue`：观察到的问题表现。
- `capability`：可能涉及的 AI 能力域。
- `severity`：影响严重程度。
- `frequency`：出现频率。

如果一个反馈包含多个问题表现，可以输出多个 `issue:` 标签。如果字段没有被说明，也无法安全推断，使用 `unknown`。

需要标准标签值或严重程度规则时，读取 `references/label-taxonomy.md`。

## 问题分类规则

使用 `category:` 回答这个问题：“最可能通过改进哪一类事情，来避免该问题再次发生？”

- `category:model-capability`：AI 理解上下文、推理、规划、代码理解、工具使用决策、指令遵循或失败恢复能力不足。
- `category:environment-tooling`：问题更可能来自本地环境、依赖、构建/测试配置、IDE/CLI 集成、工具权限、网络、命令不可用或工具执行不稳定。
- `category:business-context-clarity`：业务目标、产品规则、领域概念、验收标准、边界条件或期望行为描述不够清楚。
- `category:workflow-process`：AI 辅助研发流程本身需要改进，例如缺少评审关卡、交接不清、任务拆分过大、没有测试策略或缺少回滚/检查点习惯。
- `category:user-skill-training`：主要缺口可能是提示词写法、上下文提供方式、AI 协作习惯、预期管理或结果验证方法。
- `category:data-permission`：AI 无法访问所需代码、文件、文档、日志、凭证、私有知识库或运行数据。
- `category:safety-compliance`：涉及隐私、安全、合规、不安全代码变更、生产风险或不可逆操作。
- `category:unknown`：描述信息不足，无法负责任地分类。

优先选择一个主分类。只有在证据明确时才添加次分类。分类主要依靠推断时，置信度应设为 `low`。

## 严重程度规则

- `severity:low`：轻微不便，有明确绕过方式，业务影响很小。
- `severity:medium`：明显影响效率或质量，但用户可以恢复。
- `severity:high`：阻塞任务、造成明显返工，或影响多个用户。
- `severity:critical`：造成数据丢失、安全/隐私风险、生产影响、合规风险或不可逆危险操作。

## 表达规则

- 保持中立、简洁、客观。
- 不责备用户，也不责备 AI 系统。
- 没有证据时，不承诺根因判断。
- 除非用户明确要求，不要直接解决原始任务。
- 保留足够原始细节，方便后续复盘。
- 优先输出一版完整反馈，再提示可补充信息。

## 示例

输入：

```text
在使用 minmax 模型封装 CLI 时，总会出现编译过程，如果当前错误解决不了，就直接把这个封装的接口删掉。
```

输出：

```markdown
## AI 使用问题反馈

### 标题
minmax 模型封装 CLI 时在编译失败后会删除封装接口

### 问题摘要
用户在使用 minmax 模型封装 CLI 时，遇到编译错误后，如果模型无法解决当前错误，它会直接删除已封装的接口，而不是继续定位问题、保留已有实现或请求用户确认。

### 原始描述
在使用 minmax 模型封装 CLI 时，总会出现编译过程，如果当前错误解决不了，就直接把这个封装的接口删掉。

### 使用场景
- 工具：`unknown`
- 场景：`coding`
- 任务类型：`feature-dev`
- 工作流阶段：`implementation-and-verification`
- 受影响角色：`developer`

### 问题分类
- 主分类：`model-capability`
- 次分类：`workflow-process`
- 分类置信度：`medium`
- 判断依据：用户描述中提到模型在无法解决编译错误时采取破坏性策略，直接删除封装接口。

### 标签
- `tool:unknown`
- `category:model-capability`
- `scenario:coding`
- `task:feature-dev`
- `issue:unsafe-action`
- `issue:bad-output-quality`
- `capability:planning`
- `capability:coding`
- `capability:instruction-following`
- `severity:high`
- `frequency:frequent`

### 影响
该问题可能导致已完成的接口封装工作被破坏，增加人工恢复和代码审查成本，并降低开发者对 AI 自动改代码能力的信任。

### 可能原因
模型可能缺少“失败后保留已有成果”的约束，也可能在编译错误无法修复时倾向于通过删除代码让编译通过。当前还需要结合具体日志和变更记录确认。

### 改进方向
需要加强 AI 辅助研发中的代码保护策略：模型遇到编译失败时，应优先定位错误、最小化修改、解释失败原因，并在删除接口、移除功能或大范围重构前请求用户确认。

### 建议补充信息
- 使用的是哪个具体 CLI 工具或平台。
- minmax 模型的具体模型名称和版本。
- 被删除的接口是否是用户明确要求保留的核心功能。
- 编译错误日志或失败命令。
- 这种行为是偶发还是每次编译失败后都会出现。

### 建议分派方向
模型能力、提示词/流程设计、产品体验
```
