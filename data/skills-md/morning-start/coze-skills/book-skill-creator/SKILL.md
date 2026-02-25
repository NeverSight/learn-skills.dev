---
name: book-skill-creator
version: 1.1.0
description: 技能工厂核心母技能，支持官方文档100%覆盖、网络搜索最佳实践、模板自动生成与知识沉淀，提供完整技能开发生态和高效工作流解决方案，有效提升开发效率并保证代码质量与可维护性，支持团队协作和持续集成，助力快速交付
---

# Book Skill Creator - 技能工厂

## 任务目标
- 本 Skill 用于：工厂化批量创建和管理技能包，提供从需求分析到自动化生成的完整流程
- 能力包含：
  - **官方文档100%覆盖**：深度解析官方文档，提取所有API、配置、示例
  - **网络搜索最佳实践**：搜索行业经验，提取优秀方案并总结为模板
  - **模板自动生成**：基于搜索结果自动生成可复用模板
  - **知识沉淀管理**：版本化模板库，支持检索和复用
  - **子技能自动化构建**：批量创建和依赖管理
  - **框架使用规范**：内置框架指南和最佳实践
- 触发条件：用户需要从官方文档生成技能、搜索行业最佳实践、批量创建技能包、管理和复用模板

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  pyyaml>=6.0
  networkx>=3.0
  beautifulsoup4>=4.12.0  # 文档解析可选
  semver>=3.0.0  # 模板版本管理
  ```

## 操作步骤

### 标准流程

#### 1. 官方文档100%覆盖解析（新增）

**适用场景**：用户提供官方文档，需要完整提取所有功能

**执行步骤**：
1. 文档格式检测
   - 自动检测文档格式（Markdown/HTML/OpenAPI）
   - 选择合适的解析器

2. 深度内容提取
   - 提取所有API端点（路径、方法、参数、响应）
   - 提取所有代码示例
   - 提取所有配置项
   - 提取章节结构

3. 自动生成技能
   - 生成完整的SKILL.md（包含所有API说明）
   - 生成API客户端脚本（支持所有端点）
   - 生成API参考文档
   - 生成代码示例文档

4. 质量验证
   - 验证覆盖率是否100%
   - 检查提取内容的完整性
   - 测试生成的脚本

**调用方式**：
```bash
python scripts/docs_parser.py \
  --docs-path /path/to/docs \
  --output /path/to/skill \
  --format auto  # 或 markdown/html/openapi
```

**输出报告**：
```
技能名称: MyAPI
API端点: 25个
代码示例: 12个
配置项: 8个
覆盖率: 100%
```

#### 2. 网络搜索与最佳实践提取（新增）

**适用场景**：需要查找行业最佳实践，生成可复用模板

**执行步骤**：
1. 多维度搜索
   - 搜索关键词："{技术} best practices"
   - 搜索关键词："{技术} production ready"
   - 搜索关键词："{技术} implementation patterns"

2. 结果过滤和评分
   - 按来源权威性过滤
   - 按代码质量评分
   - 按更新时间排序
   - 去除重复内容

3. 内容提取
   - 提取代码示例
   - 提取配置模板
   - 提取最佳实践建议
   - 提取常见问题解决方案

4. 模板生成
   - 基于提取内容生成标准化模板
   - 包含代码、配置、文档
   - 自动评分（完整性、实用性、可复用性）

**调用方式**：
```bash
python scripts/web_searcher.py \
  --tech FastAPI \
  --query "api client best practices" \
  --category api \
  --output ./assets/template-library
```

**输出结果**：
- 提取的方案列表
- 生成的模板文件
- 模板评分报告

#### 3. 模板管理与知识沉淀（新增）

**适用场景**：管理已生成的模板，支持版本控制和检索

**执行步骤**：
1. 模板添加
   - 手动添加模板
   - 从网络搜索器自动添加
   - 指定版本、标签、复杂度

2. 版本管理
   - 语义化版本号
   - 版本历史记录
   - 版本差异对比

3. 模板检索
   - 按技术筛选
   - 按分类筛选
   - 按评分筛选
   - 关键词搜索

4. 模板使用
   - 查看模板详情
   - 导出模板文件
   - 集成到项目

**调用方式**：
```bash
# 列出所有模板
python scripts/template_manager.py list --tech FastAPI --min-score 0.8

# 搜索模板
python scripts/template_manager.py search --query "api client"

# 获取模板详情
python scripts/template_manager.py get --id "FastAPI/api/api-client"

# 导出模板
python scripts/template_manager.py export \
  --id "FastAPI/api/api-client" \
  --output ./my-project
```

#### 4. 批量创建与自动化构建

**适用场景**：批量创建多个相关技能

**执行步骤**：
1. 编写配置文件
2. 调用批量创建脚本
3. 分析依赖关系
4. 按顺序构建

**调用方式**：
```bash
python scripts/batch_create.py \
  --config config.json \
  --output ./skills
```

#### 5. 质量验收与验证

**执行步骤**：
1. 验证技能结构
2. 分析依赖关系
3. 测试执行
4. 生成报告

### 可选分支

- **从官方文档生成技能**：使用 docs_parser.py 实现100%覆盖
- **搜索最佳实践**：使用 web_searcher.py 提取行业经验
- **管理模板库**：使用 template_manager.py 管理知识沉淀
- **批量创建技能**：使用 batch_create.py 批量生成
- **验证技能质量**：使用 skill_validator.py 验证规范

## 资源索引

### 必要脚本

#### 文档解析脚本（新增）
- [scripts/docs_parser.py](scripts/docs_parser.py)
  - 用途：官方文档深度解析，实现100%覆盖
  - 参数：--docs-path（文档路径）、--output（输出目录）、--format（格式）
  - 支持格式：Markdown、HTML、OpenAPI
  - 输出：完整技能包（SKILL.md、脚本、参考文档）
  - 详情见：[references/docs-parsing-guide.md](references/docs-parsing-guide.md)

#### 网络搜索脚本（新增）
- [scripts/web_searcher.py](scripts/web_searcher.py)
  - 用途：搜索行业最佳实践，提取优秀方案
  - 参数：--tech（技术名）、--query（查询）、--category（分类）、--output（输出目录）
  - 功能：多维度搜索、内容提取、模板生成、自动评分
  - 输出：模板文件和评分报告

#### 模板管理脚本（新增）
- [scripts/template_manager.py](scripts/template_manager.py)
  - 用途：模板版本管理、检索、导出
  - 操作：add、update、delete、list、search、get、export
  - 功能：版本控制、评分系统、分类索引
  - 详情见：[references/template-library.md](references/template-library.md)

#### 批量创建脚本
- [scripts/batch_create.py](scripts/batch_create.py)
  - 用途：批量创建技能包
  - 参数：--config（配置文件）、--output（输出目录）
  - 输入：JSON格式配置文件

#### 验证脚本
- [scripts/skill_validator.py](scripts/skill_validator.py)
  - 用途：验证技能是否符合规范
  - 参数：--skill-path（技能目录路径）
  - 输出：验证结果和问题列表

#### 依赖分析脚本
- [scripts/dependency_analyzer.py](scripts/dependency_analyzer.py)
  - 用途：分析技能间的依赖关系
  - 参数：--base-dir（基础目录）
  - 输出：依赖关系图和构建顺序

### 领域参考

#### 文档解析指南（新增）
- [references/docs-parsing-guide.md](references/docs-parsing-guide.md)
  - 何时读取：需要了解文档解析详细流程
  - 内容：支持的格式、解析能力、覆盖率保证、使用示例

#### 模板库索引（新增）
- [references/template-library.md](references/template-library.md)
  - 何时读取：需要了解模板管理和使用方法
  - 内容：模板分类、评分系统、管理命令、检索方法、最佳实践

#### 技能规范
- [references/skill-specs.md](references/skill-specs.md)
  - 何时读取：需要了解详细规范、配置文件格式
  - 内容：命名规范、目录结构、SKILL.md格式、验证规则

#### 框架指南
- [references/frameworks-guide.md](references/frameworks-guide.md)
  - 何时读取：选择技术框架、了解框架使用方法
  - 内容：常用框架分类、使用场景、配置方法、代码模式

#### 最佳实践
- [references/best-practices.md](references/best-practices.md)
  - 何时读取：查找最佳实践方案
  - 内容：方案分类库、问题场景、解决方案、代码示例

### 输出资产

#### 技能模板
- [assets/skill-templates/api-skill.md](assets/skill-templates/api-skill.md)
- [assets/skill-templates/data-process.md](assets/skill-templates/data-process.md)
- [assets/skill-templates/workflow.md](assets/skill-templates/workflow.md)

#### 代码脚手架
- [assets/code-scaffolds/python-script.py](assets/code-scaffolds/python-script.py)
- [assets/code-scaffolds/bash-script.sh](assets/code-scaffolds/bash-script.sh)

#### 模板库（新增）
- [assets/template-library/](assets/template-library/)
  - 按技术分类存储模板
  - 包含版本历史
  - 模板索引文件

## 注意事项

### 官方文档解析

#### 覆盖率保证
- **100%覆盖原则**：提取文档中所有API端点、代码示例、配置项
- **格式标准化**：统一API端点格式（如`GET /api/path`）
- **完整性验证**：检查解析报告，确保覆盖率100%
- **缺失处理**：手动补充解析器未提取的内容

#### 文档准备
- 确保文档格式正确
- API端点使用统一格式
- 代码块包含语言标识
- 配置项使用标准格式

### 网络搜索

#### 质量控制
- **来源权威性**：优先选择官方文档、知名技术博客
- **代码质量**：提取的代码应包含错误处理和注释
- **时效性**：优先选择近期更新的内容
- **去重处理**：避免重复的方案

#### 模板生成
- **标准化格式**：统一模板结构和命名
- **自动评分**：基于完整性、实用性、可复用性评分
- **版本管理**：使用语义化版本号
- **文档完善**：包含使用说明和示例

### 模板管理

#### 版本管理
- 使用语义化版本（Semantic Versioning）
- 记录版本变更日志
- 保持向后兼容
- 定期更新依赖

#### 质量维护
- 定期审查模板质量
- 收集用户反馈
- 优化评分算法
- 清理低质量模板

## 使用示例

### 示例1：从官方文档100%覆盖生成技能（新增）

**功能说明**：解析官方文档，提取所有内容生成完整技能

**执行方式**：脚本调用

**步骤**：
```bash
# 1. 解析Markdown文档
python scripts/docs_parser.py \
  --docs-path /path/to/fastapi-docs.md \
  --output ./skills/fastapi-complete

# 2. 查看解析报告
# 技能名称: FastAPI Documentation
# API端点: 25个
# 代码示例: 12个
# 配置项: 8个
# 覆盖率: 100%

# 3. 验证生成的技能
python scripts/skill_validator.py \
  --skill-path ./skills/fastapi-complete
```

### 示例2：搜索行业经验生成模板（新增）

**功能说明**：搜索FastAPI最佳实践，生成可复用模板

**执行方式**：脚本调用 + 智能体补充

**步骤**：
```bash
# 1. 搜索最佳实践
python scripts/web_searcher.py \
  --tech FastAPI \
  --query "api client best practices" \
  --category api \
  --output ./assets/template-library

# 2. 查看生成的模板
python scripts/template_manager.py list --tech FastAPI

# 3. 导出模板使用
python scripts/template_manager.py export \
  --id "FastAPI/api/api-client" \
  --output ./my-project
```

### 示例3：管理和检索模板库（新增）

**功能说明**：管理模板库，检索高质量模板

**执行方式**：脚本调用

**步骤**：
```bash
# 1. 列出所有FastAPI模板
python scripts/template_manager.py list --tech FastAPI

# 2. 筛选高质量模板
python scripts/template_manager.py list \
  --tech FastAPI \
  --min-score 0.8 \
  --complexity advanced

# 3. 搜索特定模板
python scripts/template_manager.py search --query "authentication"

# 4. 查看模板详情
python scripts/template_manager.py get --id "FastAPI/middleware/auth"
```

### 示例4：批量创建技能

**功能说明**：批量创建多个相关技能

**执行方式**：脚本调用

**步骤**：
```bash
# 1. 准备配置文件 config.json
{
  "skills": [
    {"name": "user-api", "type": "api", "description": "用户API"},
    {"name": "auth-service", "type": "workflow", "description": "认证服务"}
  ]
}

# 2. 批量创建
python scripts/batch_create.py \
  --config config.json \
  --output ./skills

# 3. 分析依赖关系
python scripts/dependency_analyzer.py \
  --base-dir ./skills
```

## 质量门槛与最佳实践

### 文档解析
- [ ] 覆盖率100%
- [ ] 所有API端点已提取
- [ ] 所有代码示例已提取
- [ ] 所有配置项已提取
- [ ] 生成的SKILL.md完整
- [ ] 客户端脚本可执行

### 网络搜索
- [ ] 来源权威可靠
- [ ] 代码质量高
- [ ] 模板格式标准
- [ ] 评分合理
- [ ] 文档完善

### 模板管理
- [ ] 版本号规范
- [ ] 分类清晰
- [ ] 评分准确
- [ ] 可检索性强
- [ ] 易于集成

## 框架使用规范速查

### Web框架
- **FastAPI**：高性能API，异步支持
- **Flask**：轻量级应用，灵活扩展
- **Django**：全栈应用，包含ORM

### 数据处理
- **Pandas**：数据分析
- **NumPy**：数值计算
- **PyTorch/TensorFlow**：深度学习

详细使用方法见 [references/frameworks-guide.md](references/frameworks-guide.md)

## 常见问题

### Q1: 如何确保官方文档100%覆盖？
**A**:
1. 使用 docs_parser.py 解析文档
2. 检查解析报告中的覆盖率
3. 验证生成的SKILL.md包含所有API
4. 手动补充解析器未提取的内容

### Q2: 网络搜索如何确保质量？
**A**:
1. 使用权威关键词（best practices, production ready）
2. 按来源权威性过滤
3. 自动评分系统评估
4. 手动审查和补充

### Q3: 模板如何保持最新？
**A**:
1. 定期使用 web_searcher.py 搜索新实践
2. 更新模板版本号
3. 收集用户反馈
4. 优化评分算法

### Q4: 如何提高复用率？
**A**:
1. 标准化模板格式
2. 提供完整文档
3. 包含使用示例
4. 支持灵活定制
