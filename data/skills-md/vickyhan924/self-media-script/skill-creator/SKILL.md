---
name: skill-creator
description: Skill 创建指南。当用户想要创建新 skill（或更新现有 skill）以扩展 Claude 的能力时使用，包括专业知识、工作流程或工具集成。
---

# Skill Creator（Skill 创建指南）

本 skill 提供创建有效 skill 的指导。

## 关于 Skills

Skills 是模块化、自包含的包，通过提供专业知识、工作流程和工具来扩展 Claude 的能力。可以将它们视为特定领域或任务的"入职指南"——它们将 Claude 从通用型 agent 转变为配备程序性知识的专业 agent。

### Skills 提供什么

1. **专业工作流程** - 特定领域的多步骤流程
2. **工具集成** - 与特定文件格式或 API 配合使用的指令
3. **领域专业知识** - 公司特定知识、架构、业务逻辑
4. **捆绑资源** - 用于复杂和重复任务的脚本、参考资料和资产

## 核心原则

### 简洁为王

上下文窗口是公共资源。Skills 与 Claude 需要的其他所有内容共享上下文窗口：系统提示、对话历史、其他 Skills 的元数据以及实际的用户请求。

**默认假设：Claude 已经非常聪明。** 只添加 Claude 尚不具备的上下文。对每条信息提出质疑："Claude 真的需要这个解释吗？"和"这段内容值得消耗这些 token 吗？"

优先使用简洁的示例而非冗长的解释。

### 设置适当的自由度

根据任务的脆弱性和可变性匹配具体程度：

**高自由度（文本指令）**：当多种方法都有效、决策取决于上下文或启发式方法指导时使用。

**中等自由度（伪代码或带参数的脚本）**：当存在首选模式、可接受一些变化或配置影响行为时使用。

**低自由度（特定脚本，少量参数）**：当操作脆弱且容易出错、一致性至关重要或必须遵循特定顺序时使用。

将 Claude 想象成在探索路径：有悬崖的窄桥需要特定护栏（低自由度），而开阔的田野允许多条路线（高自由度）。

### Skill 的结构

每个 skill 由必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name:（必需）
│   │   └── description:（必需）
│   └── Markdown 指令（必需）
└── 捆绑资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 按需加载到上下文的文档资料
    └── assets/           - 用于输出的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

每个 SKILL.md 包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。这是 Claude 用于确定何时使用 skill 的唯一字段，因此清晰全面地描述 skill 是什么以及何时使用非常重要。
- **Body**（Markdown）：使用 skill 的指令和指南。仅在 skill 触发后加载。

#### 捆绑资源（可选）

##### Scripts（`scripts/`）

用于需要确定性可靠性或重复编写的任务的可执行代码（Python/Bash 等）。

- **何时包含**：当相同代码被重复编写或需要确定性可靠性时
- **示例**：`scripts/rotate_pdf.py` 用于 PDF 旋转任务
- **优点**：节省 token，确定性，可在不加载到上下文的情况下执行
- **注意**：脚本可能仍需要 Claude 读取以进行修补或环境特定调整

##### References（`references/`）

按需加载到上下文中以指导 Claude 处理和思考的文档和参考资料。

- **何时包含**：Claude 工作时应参考的文档
- **示例**：`references/finance.md` 财务架构、`references/mnda.md` 公司 NDA 模板、`references/policies.md` 公司政策、`references/api_docs.md` API 规范
- **用例**：数据库架构、API 文档、领域知识、公司政策、详细工作流程指南
- **优点**：保持 SKILL.md 精简，仅在 Claude 确定需要时加载
- **最佳实践**：如果文件较大（>10k 字），在 SKILL.md 中包含 grep 搜索模式
- **避免重复**：信息应该只存在于 SKILL.md 或 references 文件中，不能两者都有。除非信息确实是 skill 的核心，否则优先使用 references 文件存储详细信息——这保持 SKILL.md 精简，同时使信息可被发现而不占用上下文窗口。仅在 SKILL.md 中保留基本的程序性指令和工作流程指导；将详细的参考资料、架构和示例移至 references 文件。

##### Assets（`assets/`）

不打算加载到上下文中，而是在 Claude 产出中使用的文件。

- **何时包含**：skill 需要在最终输出中使用的文件
- **示例**：`assets/logo.png` 品牌资产、`assets/slides.pptx` PowerPoint 模板、`assets/frontend-template/` HTML/React 样板、`assets/font.ttf` 字体
- **用例**：模板、图像、图标、样板代码、字体、被复制或修改的示例文档
- **优点**：将输出资源与文档分离，使 Claude 能够在不加载到上下文的情况下使用文件

#### Skill 中不应包含的内容

Skill 应只包含直接支持其功能的基本文件。不要创建额外的文档或辅助文件，包括：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等等

Skill 应只包含 AI agent 完成工作所需的信息。它不应包含关于创建过程的辅助上下文、设置和测试程序、面向用户的文档等。创建额外的文档文件只会增加混乱。

### 渐进式披露设计原则

Skills 使用三级加载系统来高效管理上下文：

1. **元数据（name + description）** - 始终在上下文中（约 100 字）
2. **SKILL.md body** - 当 skill 触发时（<5k 字）
3. **捆绑资源** - 根据 Claude 需要（无限制，因为脚本可以在不读入上下文窗口的情况下执行）

#### 渐进式披露模式

保持 SKILL.md body 精简且少于 500 行以最小化上下文膨胀。接近此限制时将内容拆分到单独的文件中。拆分内容到其他文件时，务必从 SKILL.md 引用它们并清楚描述何时读取，以确保 skill 的读者知道它们的存在及使用时机。

**关键原则：** 当 skill 支持多种变体、框架或选项时，仅在 SKILL.md 中保留核心工作流程和选择指导。将变体特定的详细信息（模式、示例、配置）移至单独的 reference 文件。

**模式 1：高级指南与 references**

```markdown
# PDF 处理

## 快速开始

使用 pdfplumber 提取文本：
[代码示例]

## 高级功能

- **表单填写**：参见 [FORMS.md](FORMS.md) 完整指南
- **API 参考**：参见 [REFERENCE.md](REFERENCE.md) 所有方法
- **示例**：参见 [EXAMPLES.md](EXAMPLES.md) 常见模式
```

Claude 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

**模式 2：按领域组织**

对于具有多个领域的 Skills，按领域组织内容以避免加载无关上下文：

```
bigquery-skill/
├── SKILL.md（概述和导航）
└── reference/
    ├── finance.md（收入、账单指标）
    ├── sales.md（商机、管道）
    ├── product.md（API 使用、功能）
    └── marketing.md（营销活动、归因）
```

当用户询问销售指标时，Claude 只读取 sales.md。

同样，对于支持多个框架或变体的 skills，按变体组织：

```
cloud-deploy/
├── SKILL.md（工作流程 + 提供商选择）
└── references/
    ├── aws.md（AWS 部署模式）
    ├── gcp.md（GCP 部署模式）
    └── azure.md（Azure 部署模式）
```

当用户选择 AWS 时，Claude 只读取 aws.md。

**模式 3：条件详情**

显示基本内容，链接到高级内容：

```markdown
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单编辑，直接修改 XML。

**跟踪变更**：参见 [REDLINING.md](REDLINING.md)
**OOXML 详情**：参见 [OOXML.md](OOXML.md)
```

Claude 仅在用户需要这些功能时读取 REDLINING.md 或 OOXML.md。

**重要指南：**

- **避免深层嵌套引用** - 保持 references 与 SKILL.md 仅一层深度。所有 reference 文件应直接从 SKILL.md 链接。
- **结构化较长的 reference 文件** - 对于超过 100 行的文件，在顶部包含目录，以便 Claude 预览时能看到完整范围。

## Skill 创建流程

Skill 创建包括以下步骤：

1. 通过具体示例理解 skill
2. 规划可复用的 skill 内容（scripts、references、assets）
3. 初始化 skill（运行 init_skill.py）
4. 编辑 skill（实现资源并编写 SKILL.md）
5. 打包 skill（运行 package_skill.py）
6. 基于实际使用进行迭代

按顺序执行这些步骤，仅在有明确理由不适用时才跳过。

### 步骤 1：通过具体示例理解 Skill

仅当 skill 的使用模式已经清楚理解时才跳过此步骤。即使在处理现有 skill 时，此步骤仍然有价值。

要创建有效的 skill，需清楚理解 skill 将如何使用的具体示例。这种理解可以来自直接的用户示例或通过用户反馈验证的生成示例。

例如，在构建 image-editor skill 时，相关问题包括：

- "image-editor skill 应该支持什么功能？编辑、旋转，还有其他吗？"
- "你能举一些这个 skill 如何使用的例子吗？"
- "我可以想象用户会问'从这张图片中去除红眼'或'旋转这张图片'这样的问题。还有其他你想象的使用方式吗？"
- "用户说什么应该触发这个 skill？"

为避免让用户感到不堪重负，不要在单条消息中问太多问题。从最重要的问题开始，根据需要跟进以提高效果。

当对 skill 应支持的功能有清晰认识时，结束此步骤。

### 步骤 2：规划可复用的 Skill 内容

要将具体示例转化为有效的 skill，通过以下方式分析每个示例：

1. 考虑如何从头执行该示例
2. 识别重复执行这些工作流程时哪些 scripts、references 和 assets 会有帮助

示例：构建处理"帮我旋转这个 PDF"等查询的 `pdf-editor` skill 时，分析显示：

1. 旋转 PDF 每次都需要重写相同的代码
2. 在 skill 中存储 `scripts/rotate_pdf.py` 脚本会很有帮助

示例：为"帮我建一个待办应用"或"帮我建一个跟踪步数的仪表板"等查询设计 `frontend-webapp-builder` skill 时，分析显示：

1. 编写前端 webapp 每次都需要相同的 HTML/React 样板
2. 在 skill 中存储包含样板 HTML/React 项目文件的 `assets/hello-world/` 模板会很有帮助

示例：构建处理"今天有多少用户登录？"等查询的 `big-query` skill 时，分析显示：

1. 查询 BigQuery 每次都需要重新发现表架构和关系
2. 在 skill 中存储记录表架构的 `references/schema.md` 文件会很有帮助

要确定 skill 的内容，分析每个具体示例以创建要包含的可复用资源列表：scripts、references 和 assets。

### 步骤 3：初始化 Skill

此时，是时候实际创建 skill 了。

仅当正在开发的 skill 已存在且需要迭代或打包时才跳过此步骤。在这种情况下，继续下一步。

从头创建新 skill 时，始终运行 `init_skill.py` 脚本。该脚本方便地生成一个新的模板 skill 目录，自动包含 skill 所需的一切，使 skill 创建过程更加高效和可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

该脚本：

- 在指定路径创建 skill 目录
- 生成带有正确 frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 SKILL.md 和示例文件。

### 步骤 4：编辑 Skill

编辑（新生成或现有的）skill 时，记住 skill 是为另一个 Claude 实例使用而创建的。包含对 Claude 有益且非显而易见的信息。考虑什么程序性知识、领域特定细节或可复用资产能帮助另一个 Claude 实例更有效地执行这些任务。

#### 学习经过验证的设计模式

根据 skill 的需求查阅这些有用的指南：

- **多步骤流程**：参见 references/workflows.md 了解顺序工作流和条件逻辑
- **特定输出格式或质量标准**：参见 references/output-patterns.md 了解模板和示例模式

这些文件包含有效 skill 设计的既定最佳实践。

#### 从可复用 Skill 内容开始

要开始实现，从上面识别的可复用资源开始：`scripts/`、`references/` 和 `assets/` 文件。注意此步骤可能需要用户输入。例如，实现 `brand-guidelines` skill 时，用户可能需要提供品牌资产或模板存储在 `assets/` 中，或文档存储在 `references/` 中。

添加的脚本必须通过实际运行来测试，以确保没有 bug 且输出符合预期。如果有许多类似的脚本，只需测试有代表性的样本以确保它们都能工作，同时平衡完成时间。

应删除 skill 不需要的任何示例文件和目录。初始化脚本在 `scripts/`、`references/` 和 `assets/` 中创建示例文件以演示结构，但大多数 skills 不需要所有这些。

#### 更新 SKILL.md

**编写指南：** 始终使用祈使句/不定式形式。

##### Frontmatter

编写包含 `name` 和 `description` 的 YAML frontmatter：

- `name`：skill 名称
- `description`：这是 skill 的主要触发机制，帮助 Claude 理解何时使用该 skill。
  - 包括 skill 做什么以及使用时的特定触发器/上下文。
  - 在此处包含所有"何时使用"信息 - 不要放在 body 中。Body 仅在触发后加载，因此 body 中的"何时使用此 Skill"部分对 Claude 没有帮助。
  - `docx` skill 的示例描述："全面的文档创建、编辑和分析，支持跟踪变更、注释、格式保留和文本提取。当 Claude 需要处理专业文档（.docx 文件）时使用，用于：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理跟踪变更，(4) 添加注释，或任何其他文档任务"

不要在 YAML frontmatter 中包含任何其他字段。

##### Body

编写使用 skill 及其捆绑资源的指令。

### 步骤 5：打包 Skill

开发完成后，必须将 skill 打包成可分发的 .skill 文件与用户共享。打包过程会自动先验证 skill 以确保满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

可选的输出目录指定：

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本将：

1. **验证** skill，自动检查：

   - YAML frontmatter 格式和必需字段
   - Skill 命名约定和目录结构
   - 描述的完整性和质量
   - 文件组织和资源引用

2. 如果验证通过则**打包** skill，创建一个以 skill 命名的 .skill 文件（例如 `my-skill.skill`），包含所有文件并保持适当的目录结构以供分发。.skill 文件是带有 .skill 扩展名的 zip 文件。

如果验证失败，脚本将报告错误并退出而不创建包。修复所有验证错误后再次运行打包命令。

### 步骤 6：迭代

测试 skill 后，用户可能会请求改进。这通常发生在使用 skill 后不久，此时对 skill 表现的上下文还很新鲜。

**迭代工作流程：**

1. 在实际任务中使用 skill
2. 注意困难或低效之处
3. 识别 SKILL.md 或捆绑资源应如何更新
4. 实施更改并再次测试
