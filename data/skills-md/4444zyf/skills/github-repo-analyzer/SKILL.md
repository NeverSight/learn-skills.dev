---
name: github-repo-analyzer
description: |
  分析 GitHub 开源仓库的源代码，生成结构化的分析报告。
  支持生成项目架构概览、代码质量分析、核心模块说明等报告，
  并可选同步到 Notion。
---

# GitHub 仓库分析器

分析 GitHub 开源仓库，生成结构化的 Markdown 分析报告，支持同步到 Notion。

## 工作流程

### 第一步：获取仓库地址

按需询问用户提供 GitHub 仓库地址。格式示例：
- `https://github.com/user/repo`
- `github.com/user/repo`
- `user/repo`

### 第二步：Clone 仓库

1. 在现有目录下创建分析工作目录（使用时间戳命名，如 `analysis-20240314-123045`）
2. 在该目录下创建 `repo/` 子目录用于存放 clone 的代码
3. 执行 `git clone` 命令将仓库 clone 到 `repo/` 目录
4. 验证 clone 成功（检查目录非空）

### 第三步：获取分析要求

询问用户具体的分析要求，例如：
- "分析整体架构和模块关系"
- "检查代码质量和潜在问题"
- "生成 API 接口文档"
- "分析安全漏洞"
- "评估测试覆盖率"
- 或用户的自定义需求

### 第四步：分析仓库

根据用户要求，调用以下工具之一进行深度分析：
- 最优先：`Open Code` - 如果用户已配置
- 次优先：`Claude Code` - 如果用户已配置
- 最后：`Codex` - 如果用户已配置

分析策略：
1. 首先探索仓库结构（README、目录结构、主要配置文件）
2. 识别核心模块和入口文件
3. 针对用户要求，深度分析相关代码
4. 记录关键发现、模式、问题

### 第五步：生成分析报告

在工作目录（与 `repo/` 同级）创建以下 Markdown 文档：

```
analysis-20240314-123045/
├── repo/                    # clone 的仓库代码
├── reports/                 # 分析报告目录
│   ├── 01-主题1.md
│   ├── 02-主题2.md
│   ├── 03-主题3.md
│   └── 04-其他用户要求的主题.md
└── notion-sync.log         # Notion 同步日志（如果启用notion同步脚本）
```

#### 报告内容规范

**01-项目架构概览.md**
- 项目基本信息（名称、描述、技术栈）
- 目录结构说明
- 架构模式（MVC、微服务、分层架构等）
- 关键组件及其关系
- 依赖关系图（用文字描述）

**02-代码质量分析.md**
- 代码规范遵循情况
- 潜在 bug 或问题
- 复杂度分析
- 测试覆盖情况（如有）
- 改进建议

**03-核心模块说明.md**
- 主要模块/包的功能说明
- 关键类/函数的用途
- 数据流分析
- 重要算法或业务逻辑说明

### 第六步：Notion 同步（可选）

检查 `~/.config/notion/api_key` 是否存在：
- 如果存在，询问用户是否同步到 Notion
- 如果用户同意，将每个 Markdown 文档分块上传到 Notion
- 创建页面结构：父页面为仓库名称，子页面为各分析报告
- 记录同步日志到 `notion-sync.log`

Notion API 调用要点：
- 使用 Notion API v1
- 每个 Markdown 文件作为一个子页面
- 内容分块（每块不超过 2000 字符）
- 保持 Markdown 格式
- 在 Notion 中子页面如下：

```
仓库简介.md (名字依据仓库名和用户要求总结提炼)
├── 01-主题1.md
├── 02-主题2.md
├── 03-主题3.md
└── 04-其他用户要求的主题.md
```


### 第七步：清理（可选）

询问用户是否删除 clone 的仓库：
- 如果用户选择删除，删除 `repo/` 目录但保留 `reports/`
- 如果用户选择保留，告知完整路径

## 重要提示

1. **报告存放位置**：分析报告必须放在与 `repo/` 同级的 `reports/` 目录，不要放在仓库内部
2. **仓库路径**：始终使用 `/github-analysis/analysis-<timestamp>/` 结构
3. **错误处理**：
   - Clone 失败时（网络问题、仓库不存在、权限问题），提示用户并退出
   - 分析工具不可用时，询问用户是否采用当前会话的工具进行分析
   - Notion 同步失败时，记录错误但不中断流程
4. **大仓库处理**：如果仓库文件数超过 10000，提示用户分析可能需要较长时间
5. **敏感信息**：分析报告中如发现 API 密钥、密码等敏感信息，提醒用户注意

## 输出示例

分析完成后，向用户汇报：

```
✅ 仓库分析完成！

📁 分析报告位置：/github-analysis/analysis-20240314-123045/reports/

📄 生成文件：
   - 01-项目架构概览.md
   - 02-代码质量分析.md
   - 03-核心模块说明.md

📊 分析摘要：
   - 技术栈：Python/FastAPI + React
   - 代码文件：127 个
   - 主要问题：发现 3 处潜在问题，详见代码质量分析报告

🔄 Notion 同步：已同步到 https://notion.so/xxx（如适用）

❓ 是否删除 clone 的仓库？(y/n)
```

## 工具检查

在开始分析前，检查以下工具是否可用：

```bash
# 检查 git
command -v git &> /dev/null && echo "git: OK" || echo "git: MISSING"

# 检查 opencode
command -v opencode &> /dev/null && echo "opencode: OK" || echo "opencode: NOT FOUND"

# 检查 claude CLI
command -v claude &> /dev/null && echo "claude: OK" || echo "claude: NOT FOUND"

# 检查 codex
command -v codex &> /dev/null && echo "codex: OK" || echo "codex: NOT FOUND"

# 检查 Notion API 密钥
[ -f ~/.config/notion/api_key ] && echo "notion: CONFIGURED" || echo "notion: NOT CONFIGURED"
```
