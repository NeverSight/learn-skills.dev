---
name: coze-skill-creator
version: 1.0.0
description: 从配置或需求描述创建完整技能，支持工具配置、工作流编排和代码生成
dependency:
  python:
    - jsonschema>=4.0.0
---

# Coze Skill Creator

## 任务目标
- 本 Skill 用于:从配置文件或需求描述创建完整的 Skill，包括工具配置、工作流编排和代码生成
- 能力包含:配置验证、文件生成、模板渲染、技能打包
- 触发条件:用户描述技能需求、提供技能配置 JSON、设计工作流结构

## 前置准备
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  jsonschema>=4.0.0
  ```
- 非标准文件/文件夹准备:无

## 操作步骤
- 标准流程:
  1. **需求分析**
     - 智能体根据用户描述，理解技能的核心能力、触发场景和工具需求
     - 参考 [references/config-reference.md](references/config-reference.md) 确定配置结构
  2. **配置生成**
     - 根据分析结果，生成技能配置 JSON 文件
     - 配置包含:元数据、工具列表、工作流节点、脚本定义
  3. **Schema 验证**
     - 调用 `scripts/validate_schema.py --config <config_path>` 验证配置格式
     - 若验证失败，根据错误信息修正配置
  4. **文件生成**
     - 调用 `scripts/generate_skill.py --config <config_path> --output <output_dir>` 生成技能文件
     - 脚本自动创建 SKILL.md、scripts/、references/、assets/ 结构
  5. **打包测试**
     - 使用 `package_skill(skill_dir_name=<skill_name>)` 工具打包技能
     - 验证 .skill 文件生成成功且内容完整

- 可选分支:
  - 当 **用户提供配置 JSON**:直接跳到步骤 3 进行验证
  - 当 **仅需生成工作流设计**:参考 [references/workflow-guide.md](references/workflow-guide.md)，智能体生成工作流图和节点定义
  - 当 **仅需配置工具集成**:参考 [references/tool-reference.md](references/tool-reference.md)，智能体生成工具配置

## 资源索引
- 必要脚本:
  - [scripts/validate_schema.py](scripts/validate_schema.py) (用途与参数:验证技能配置 JSON 是否符合 Schema，参数:--config)
  - [scripts/generate_skill.py](scripts/generate_skill.py) (用途与参数:根据配置生成完整技能文件，参数:--config, --output)
- 领域参考:
  - [references/config-reference.md](references/config-reference.md) (何时读取:生成或验证配置时)
  - [references/workflow-guide.md](references/workflow-guide.md) (何时读取:设计工作流时)
  - [references/tool-reference.md](references/tool-reference.md) (何时读取:配置工具时)
- 输出资产:
  - [assets/templates/skill-template.md](assets/templates/skill-template.md) (直接用于生成 SKILL.md)
  - [assets/templates/python-script.py](assets/templates/python-script.py) (直接用于生成 Python 脚本)
  - [assets/templates/schema.json](assets/templates/schema.json) (用于验证配置格式)

## 注意事项
- 配置 JSON 必须符合 [assets/templates/schema.json](assets/templates/schema.json) 定义的 Schema
- 生成的技能命名必须使用小写字母和连字符，禁止使用 -skill 后缀
- 工作流节点的连接关系必须保持有向无环图结构
- 充分利用智能体的自然语言理解能力，仅在需要结构化输出时调用脚本

## 使用示例

### 示例 1:从需求描述创建技能
- **功能说明**:用户描述"需要一个处理图片压缩的技能"
- **执行方式**:智能体分析需求→生成配置→脚本验证→生成文件→打包
- **关键参数**:技能名称 image-compressor、描述、工具列表
- **配置示例**:
  ```json
  {
    "name": "image-compressor",
    "description": "压缩图片文件大小",
    "tools": [
      {
        "name": "compress",
        "type": "python",
        "parameters": [{"name": "quality", "type": "integer"}]
      }
    ]
  }
  ```

### 示例 2:从配置文件生成技能
- **功能说明**:用户已提供 skill-config.json 配置文件
- **执行方式**:脚本验证→脚本生成→打包
- **关键参数**:--config skill-config.json, --output ./my-skill
- **命令**:`python scripts/generate_skill.py --config skill-config.json --output ./my-skill`

### 示例 3:设计工作流
- **功能说明**:用户需要创建包含分支逻辑的技能工作流
- **执行方式**:智能体读取工作流指南→设计节点→生成配置→生成技能
- **关键参数**:节点类型、连接关系、条件表达式
- **工作流示例**:
  ```
  [开始] → [条件判断] → [分支A: API调用] → [结束]
                    ↘ [分支B: 本地处理] → [结束]
  ```
