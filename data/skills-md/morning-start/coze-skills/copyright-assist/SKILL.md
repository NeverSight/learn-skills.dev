---
name: copyright-assist
version: 1.0.0
description: 辅助软件著作权申请，包括设计说明书、用户说明书、操作手册撰写指导及源代码提取格式化；支持多版本申请、智能资源检查、自动打包符合官方要求的材料
dependency:
  python:
    - chardet>=5.0.0
    - PyYAML>=6.0
  system:
    - pip install PyYAML
---

# 软著申请辅助技能

## 任务目标
- 本技能用于：根据现有项目资源辅助完成软件著作权申请材料的准备
- 能力包含：
  - 源代码提取与格式化（符合软著要求的60页代码）
  - 设计说明书/用户说明书/操作手册撰写指导
  - 资源完整性检查与缺失提醒
  - 说明书模板填充与格式调整
- 触发条件：
  - 用户需要申请软件著作权
  - 用户已有项目代码、文档或部分材料
  - 用户需要指导如何准备软著申请材料

## 前置准备
- 依赖说明：
  - Python环境已包含所需标准库
  - 可选依赖：PyYAML（用于配置文件管理）
- 非标准文件/文件夹准备：无
- 配置文件：`config.yaml`（可选，用于自定义配置参数）

## 操作步骤

### 步骤1：资源收集与完整性检查

**交互式询问**：
请用户确认已提供或可提供以下资源：
- 项目源代码（路径：`./src/` 或其他代码目录）
- 项目文档（需求文档、设计文档、README等）
- 软件运行截图（建议至少10张，覆盖主要功能）
- 项目名称、版本号、开发工具、技术栈等基本信息

**资源完整性检查**：
调用 `scripts/check_resources.py` 检查资源完整性：
```bash
python /workspace/projects/copyright-assist/scripts/check_resources.py --code-dir ./src --doc-dir ./docs --screenshot-dir ./screenshots
```

**缺失资源提醒**：
根据检查结果，提醒用户收集缺失资源：
- 缺少截图：提醒用户需要准备系统运行截图（建议包含登录界面、主要功能模块、操作流程等）
- 缺少文档：提醒用户准备需求文档或设计文档
- 代码不完整：提醒用户确保包含主要业务逻辑代码

### 步骤2：选择说明书类型并准备

**说明书类型选择**：
请用户根据软著申请需求选择：
- 设计说明书（侧重软件设计思路、架构、技术实现）
- 用户说明书（侧重用户操作指南、功能介绍）
- 操作手册（侧重详细操作步骤、使用说明）

**说明书撰写指导**：
根据用户选择的类型，提供对应指导：

- **设计说明书**：参考 [references/design-manual-guide.md](references/design-manual-guide.md)
  - 核心章节：设计概要、系统架构、功能模块设计、数据结构设计、接口设计、算法设计
  - 重点：技术实现思路、架构图、流程图、设计亮点

- **用户说明书**：参考 [references/user-manual-guide.md](references/user-manual-guide.md)
  - 核心章节：软件简介、运行环境、安装指南、功能介绍、操作流程、常见问题
  - 重点：图文结合，截图清晰，操作步骤详细

- **操作手册**：参考 [references/operation-manual-guide.md](references/operation-manual-guide.md)
  - 核心章节：系统概述、环境配置、功能详解、操作指南、故障排除
  - 重点：详细的操作步骤，每个步骤配截图

### 步骤3：源代码提取与格式化

**调用代码提取脚本**：
```bash
python /workspace/projects/copyright-assist/scripts/extract_source_code.py --code-dir ./src --output ./formatted_code.txt
```

**脚本功能（严格符合国家版权局要求）**：
- 自动判断总行数，决定提取策略：
  - 代码总行数 < 3000行：全量提交所有代码
  - 代码总行数 ≥ 3000行：提取前30页+后30页
- 强制每页补足50行（含空行和注释）
- 自动用注释填充空白页
- 添加页码标记（如 `/* === 第1页 === */`）
- 保留代码结构和缩进
- 支持多版本申请：`--version 1.0.0` 参数

**代码格式要求**：参考 [references/source-code-format.md](references/source-code-format.md)

**配置文件**：可通过 `config.yaml` 自定义参数（如忽略目录、文件扩展名等）

### 步骤4：说明书内容生成

**根据选择的类型和已有资源，智能体将**：
- 分析项目代码和文档，提取关键信息
- 按照说明书结构，逐章节撰写内容
- 将用户提供的截图插入对应位置
- 调整语言表达，符合软著申请规范

**模板使用**：
- 设计说明书模板：[assets/templates/design-manual-template.md](assets/templates/design-manual-template.md)
- 用户说明书模板：[assets/templates/user-manual-template.md](assets/templates/user-manual-template.md)

### 步骤5：页数与格式检查

**页数检查**：
- 说明书：通常要求60页以上
- 源代码：根据代码总行数自动决定（全量或60页）
- 如页数不足，提醒用户补充内容或调整格式

**格式检查**：
- 截图是否清晰，是否有对应说明文字
- 代码是否格式规范，注释是否清晰
- 文档结构是否完整，章节是否连贯

**资源检查**：
运行详细的资源检查工具：
```bash
python /workspace/projects/copyright-assist/scripts/check_resources.py --code-dir ./src --doc-dir ./docs --screenshot-dir ./screenshots --output report.json
```
- 检查代码行数、文件数量
- 检查截图数量和分辨率
- 提供详细的问题分析和解决方案
- 生成JSON格式的检查报告

### 步骤6：自动打包提交材料

**调用打包脚本**：
```bash
python /workspace/projects/copyright-assist/scripts/package_submission.py \
  --software-name "用户管理系统" \
  --version 1.0.0 \
  --manual ./用户说明书.pdf \
  --code ./formatted_code.txt \
  --output ./output
```

**脚本功能**：
- 自动生成符合命名规范的ZIP包（如 `用户管理系统_1.0.0.zip`）
- 重命名文件为标准格式（`软件名称_版本号_说明书.pdf`）
- 生成资源清单文件
- 验证包结构完整性
- 检查文件大小和代码行数

**多版本支持**：
- 资源目录按版本组织（如 `screenshots/v1.0/`, `screenshots/v2.0/`）
- 每个版本独立打包
- 说明书模板包含版本字段

### 步骤7：输出与交付

**生成最终材料**：
- 源代码文件：`./formatted_code.txt`
- 说明书文件：`./<类型>_说明书.docx` 或 `.md`
- ZIP包：`./软件名称_版本号.zip`（包含说明书+代码+清单）
- 检查报告：`./report.json`（资源检查报告）

**交付确认**：
- 确认材料是否符合软著申请要求
- 提醒用户补充缺失内容（如需）
- 提供后续修改建议

## 资源索引

- 必要脚本：
  - [scripts/extract_source_code.py](scripts/extract_source_code.py)：源代码提取与格式化（符合国家版权局要求）
  - [scripts/check_resources.py](scripts/check_resources.py)：资源完整性检查（含详细日志和问题分析）
  - [scripts/package_submission.py](scripts/package_submission.py)：自动打包提交材料（生成ZIP包）
- 配置文件：
  - [config.yaml](config.yaml)：配置文件（支持自定义忽略目录、文件扩展名、阈值等）
- 领域参考：
  - [references/design-manual-guide.md](references/design-manual-guide.md)：设计说明书撰写指南
  - [references/user-manual-guide.md](references/user-manual-guide.md)：用户说明书撰写指南
  - [references/operation-manual-guide.md](references/operation-manual-guide.md)：操作手册撰写指南
  - [references/source-code-format.md](references/source-code-format.md)：源代码格式规范
- 输出资产：
  - [assets/templates/design-manual-template.md](assets/templates/design-manual-template.md)：设计说明书模板
  - [assets/templates/user-manual-template.md](assets/templates/user-manual-template.md)：用户说明书模板

## 注意事项

- 智能体负责内容创作、结构规划和交互指导，脚本负责技术性处理（代码提取、资源检查、打包）
- 说明书撰写时，充分利用智能体的内容生成能力，避免过度使用脚本
- 在整个过程中保持与用户的交互，及时提醒收集缺失资源
- 确保输出材料符合软著申请的规范要求
- 截图数量和质量对说明书页数影响较大，建议用户提前准备充足截图
- **合规性**：所有脚本严格按照国家版权局要求实现（代码行数、页数、格式）
- **配置化**：可通过 `config.yaml` 自定义配置参数，无需修改脚本代码
- **多版本**：支持同一软件多个版本（V1.0, V2.0）的独立申请和管理
- **日志系统**：所有脚本使用统一的日志系统，提供详细的错误信息和解决方案

## 使用示例

### 示例1：完整流程（设计说明书）

**用户需求**：
- 项目代码位于 `./myproject/src/`
- 已有部分设计文档 `./docs/design.md`
- 需要生成设计说明书

**执行流程**：
1. 检查资源完整性
2. 提取源代码（前30页+后30页）
3. 阅读设计文档，提取设计思路
4. 按照设计说明书结构生成内容
5. 生成 `./设计说明书.md`

### 示例2：补充资源（用户说明书）

**用户需求**：
- 已有代码和部分文档
- 缺少运行截图

**执行流程**：
1. 检查资源，发现缺少截图
2. 提醒用户准备系统运行截图（建议包含以下场景：登录界面、主要功能模块、数据录入、查询操作、报表导出等，每个场景至少2-3张截图）
3. 用户补充截图后，重新检查
4. 生成用户说明书

### 示例3：代码提取

**用户需求**：
- 只需要提取源代码

**执行流程**：
```bash
python /workspace/projects/copyright-assist/scripts/extract_source_code.py --code-dir ./myproject/src --output ./code.txt
```

生成 `./code.txt`，包含格式化的代码（根据总行数自动决定全量或60页）

### 示例4：多版本软著申请

**用户需求**：
- 同一软件需要申请V1.0和V2.0两个版本

**执行流程**：

**步骤1**：按版本组织资源目录
```
myproject/
├── src/                    # V1.0代码
├── src_v2/                 # V2.0代码
├── screenshots/
│   ├── v1.0/               # V1.0截图
│   └── v2.0/               # V2.0截图
└── docs/
    ├── v1.0/                # V1.0文档
    └── v2.0/                # V2.0文档
```

**步骤2**：提取V1.0代码
```bash
python /workspace/projects/copyright-assist/scripts/extract_source_code.py \
  --code-dir ./src --output ./code_v1.0.txt --version 1.0.0
```

**步骤3**：提取V2.0代码
```bash
python /workspace/projects/copyright-assist/scripts/extract_source_code.py \
  --code-dir ./src_v2 --output ./code_v2.0.txt --version 2.0.0
```

**步骤4**：生成V1.0说明书和V2.0说明书

**步骤5**：分别打包
```bash
# 打包V1.0
python /workspace/projects/copyright-assist/scripts/package_submission.py \
  --software-name "用户管理系统" --version 1.0.0 \
  --manual ./V1.0_说明书.pdf --code ./code_v1.0.txt \
  --output ./output

# 打包V2.0
python /workspace/projects/copyright-assist/scripts/package_submission.py \
  --software-name "用户管理系统" --version 2.0.0 \
  --manual ./V2.0_说明书.pdf --code ./code_v2.0.txt \
  --output ./output
```

生成 `./output/用户管理系统_1.0.0.zip` 和 `./output/用户管理系统_2.0.0.zip`

### 示例5：完整流程（含资源检查和打包）

**执行流程**：
```bash
# 1. 检查资源
python /workspace/projects/copyright-assist/scripts/check_resources.py \
  --code-dir ./src --doc-dir ./docs --screenshot-dir ./screenshots \
  --output report.json

# 2. 提取代码
python /workspace/projects/copyright-assist/scripts/extract_source_code.py \
  --code-dir ./src --output ./code.txt --version 1.0.0

# 3. 生成说明书（智能体完成）

# 4. 打包提交材料
python /workspace/projects/copyright-assist/scripts/package_submission.py \
  --software-name "用户管理系统" --version 1.0.0 \
  --manual ./用户说明书.pdf --code ./code.txt \
  --output ./output
```

生成 `./output/用户管理系统_1.0.0.zip`，可直接用于软著申请上传
