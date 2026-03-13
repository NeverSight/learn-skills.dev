---
name: skill-security-checker
description: |
  检查 Skill/代码仓库是否存在安全风险。When the user wants to check if a skill, GitHub repository, npm package, or local code is safe to download or use. This includes detecting malicious code, malware, key stealing, environment variable modification, suspicious network behavior, and evaluating repository reputation (stars, forks, contributors, age). Use this skill whenever the user mentions checking skills for security risks, scanning repositories for malware, verifying code safety, checking npm packages for threats, or asking if a download is safe.
---

# Skill Security Checker

检查 Skill/代码仓库是否存在安全风险，在下载前和运行时进行多维度安全评估。

## When to Use This Skill

当用户提到以下情况时使用此技能：
- 检查某个 skill 是否安全
- 扫描仓库是否有恶意代码
- 验证代码安全性
- 检查 npm 包是否有威胁
- 询问某个下载是否安全

## Usage

### 支持的输入类型

1. **GitHub 仓库**:
   ```
   检查这个仓库安全性: https://github.com/user/repo
   检查 skill: github.com/user/repo
   ```

2. **本地文件夹   检查本地**:
   ```
 skill: /path/to/skill
   扫描这个文件夹
   ```

3. **npm 包**:
   ```
   检查这个 npm 包安全性: lodash
   检查 npm 包: some-package
   ```

### 输出格式

用户可以选择输出格式：
- `json` - 结构化 JSON 报告
- `friendly` - 带 emoji 的友好界面
- `concise` - 简洁摘要（默认）

### 可选参数

- `--runtime` - 启用运行时行为监控（检测 package.json 中的危险脚本）

## How It Works

### 第一阶段：下载前检查（必选）

1. **静态代码分析** - 检测以下模式：
   - 恶意代码：base64 编码 payload、eval/exec 调用、加密字符串、反调试技术
   - 敏感信息窃取：读取 SSH keys、API tokens、环境变量
   - 环境破坏：修改系统配置、删除文件
   - 网络可疑：向未知域名发送数据、反弹 shell

2. **仓库信誉度评估**：
   - GitHub stars 数量
   - fork 数量
   - 创建时间
   - 最后更新时间
   - 贡献者数量

### 第二阶段：运行时监控（可选）

当用户添加 `--runtime` 参数时：
- 检测 package.json 中的危险脚本（preinstall, postinstall 等）
- 检测可疑依赖包
- 在沙箱环境中短暂执行观察行为

### 综合评估

- 计算安全评分（0-100）
- 风险等级：高/中/低
- 推荐结果：可下载/不建议下载
- 详细说明原因

## Example Commands

```bash
# 检查 GitHub 仓库（友好输出）
skill-security-checker github octocat/Hello-World friendly

# 检查 GitHub 仓库（JSON 格式）
skill-security-checker github https://github.com/lodash/lodash json

# 检查本地文件夹
skill-security-checker local /path/to/my-skill

# 检查 npm 包
skill-security-checker npm express

# 启用运行时检查
skill-security-checker github user/repo friendly --runtime
```

## Output Example

### Friendly 格式输出：

```
╔══════════════════════════════════════════════════════╗
║              Skill 安全检查报告                      ║
╠══════════════════════════════════════════════════════╣
  ✅ 风险等级: LOW
  📊 安全评分: 85/100
  ✅ 推荐: 可下载
╠══════════════════════════════════════════════════════╣
📈 仓库信息:
   ⭐ Stars: 50000+
   🍴 Forks: 5000+
   👥 贡献者: 200+
   📅 创建时间: 2012-01-01
╚══════════════════════════════════════════════════════╝
```

### 危险情况输出：

```
╔══════════════════════════════════════════════════════╗
║              Skill 安全检查报告                      ║
╠══════════════════════════════════════════════════════╣
  🔴 风险等级: HIGH
  📊 安全评分: 15/100
  ❌ 推荐: 不建议下载
╠══════════════════════════════════════════════════════╣
⚠️ 风险原因:
   - 检测到恶意代码模式（base64 编码 payload）
   - 检测到访问 SSH 密钥
   - 仓库缺乏社会监督（stars < 10）
📈 仓库信息:
   ⭐ Stars: 5
   🍴 Forks: 0
   👥 贡献者: 1
╚══════════════════════════════════════════════════════╝
```

## Implementation Notes

此技能使用以下技术实现：
- Node.js + TypeScript
- simple-git: Git 仓库操作
- glob: 文件模式匹配
- GitHub API: 仓库信息获取
- 正则表达式: 恶意代码模式检测

核心检测规则位于 `detectionPatterns.ts`，可以扩展更多检测模式。
