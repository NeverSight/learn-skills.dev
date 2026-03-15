---
name: skills-vetter
description: |
  技能安全审核工具。验证 Claude Code skills 的安全性，检查恶意代码、敏感信息泄露、危险操作等。
  在安装或使用新技能前进行安全评估，生成安全报告。
trigger_words:
  - skills-vetter
  - vet skill
  - audit skill
  - check skill safety
  - skill security
  - verify skill
  - 安全审核
  - 技能安全
  - 检查技能
---

# Skills Vetter - 技能安全审核工具

## 概述

Skills Vetter 是一个安全审核工具，用于验证 Claude Code skills 的安全性。在安装或使用新技能前，自动检查以下安全风险：

| 检查类别 | 风险等级 | 检查内容 |
|----------|----------|----------|
| **恶意代码** | 🔴 严重 | 系统命令执行、文件删除、网络攻击 |
| **敏感信息** | 🔴 严重 | API Key、密码、Token 硬编码 |
| **危险操作** | 🟠 高危 | 无限制文件操作、Shell 执行 |
| **数据泄露** | 🟡 中危 | 外发数据、日志上传 |
| **资源滥用** | 🟡 中危 | 无限循环、内存泄漏、CPU 占用 |

## 使用方法

### 1. 审核单个技能

```bash
# 审核本地技能
skills-vetter check ~/.claude/skills/my-skill/

# 审核远程技能（GitHub）
skills-vetter check https://github.com/user/skill-repo
```

### 2. 批量审核

```bash
# 审核所有已安装技能
skills-vetter check-all

# 审核指定目录
skills-vetter check-dir ~/.claude/skills/
```

### 3. 生成报告

```bash
# 生成详细报告
skills-vetter report my-skill/ --output report.md

# JSON 格式输出
skills-vetter report my-skill/ --format json
```

## 安全检查项

### 🔴 严重风险（自动拒绝）

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 系统命令注入 | 未过滤的用户输入传入 shell | `exec(user_input)` |
| 文件系统破坏 | 删除系统文件、格式化操作 | `rm -rf /`, `format c:` |
| 网络攻击代码 | DDoS、端口扫描、漏洞利用 | socket flood, nmap |
| 凭证硬编码 | API Key、密码直接写在代码中 | `api_key = "sk-xxx"` |

### 🟠 高危风险（需要确认）

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 无限制文件读写 | 未验证路径的文件操作 | `open(user_path, 'w')` |
| Shell 命令执行 | 允许执行任意命令 | `subprocess.call(cmd)` |
| 外部网络请求 | 向未知服务器发送数据 | `requests.post(unknown_url)` |
| 环境变量读取 | 读取敏感环境变量 | `os.environ.get('AWS_SECRET')` |

### 🟡 中危风险（建议修改）

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 过度权限请求 | 请求不必要的权限 | 读取完整 home 目录 |
| 日志敏感数据 | 记录密码、Token 等 | `logger.info(password)` |
| 未加密存储 | 明文存储敏感信息 | 保存密码到文件 |
| 无超时限制 | 可能无限等待的操作 | `requests.get(url)` 无 timeout |

### 🟢 低危风险（仅供参考）

| 检查项 | 说明 | 示例 |
|--------|------|------|
| 缺少错误处理 | 可能导致信息泄露 | 裸 `except: pass` |
| 硬编码路径 | 可移植性问题 | `/Users/admin/...` |
| 版本依赖未声明 | 兼容性风险 | 未指定依赖版本 |

## 审核流程

```
1. 静态分析
   ├── 解析 SKILL.md 和脚本文件
   ├── 检查代码模式匹配
   └── 提取敏感信息

2. 行为分析
   ├── 识别文件操作
   ├── 识别网络请求
   └── 识别系统调用

3. 依赖分析
   ├── 检查第三方包安全性
   ├── 识别已知漏洞依赖
   └── 检查依赖来源

4. 生成报告
   ├── 风险等级汇总
   ├── 详细问题列表
   └── 修复建议
```

## 报告示例

```markdown
# Skills Security Report: my-skill

## Summary

| 风险等级 | 数量 |
|----------|------|
| 🔴 严重 | 0 |
| 🟠 高危 | 2 |
| 🟡 中危 | 3 |
| 🟢 低危 | 1 |

## Details

### 🟠 High Risk: Shell Command Execution
- **File**: scripts/run.py:42
- **Code**: `subprocess.call(user_input, shell=True)`
- **Fix**: 使用参数列表而非字符串，避免 shell=True

### 🟠 High Risk: Unrestricted File Write
- **File**: scripts/file_ops.py:15
- **Code**: `open(path, 'w')`
- **Fix**: 验证路径在允许的目录范围内

### 🟡 Medium Risk: No Timeout
- **File**: scripts/api.py:8
- **Code**: `requests.get(url)`
- **Fix**: 添加 timeout 参数

## Recommendation

⚠️ **不建议安装** - 存在 2 个高危风险需要修复
```

## 自动拒绝规则

以下情况将自动拒绝安装：

1. **检测到恶意代码** - 任何破坏性操作
2. **硬编码敏感凭证** - API Key、密码明文存储
3. **后门代码** - 隐藏的远程执行
4. **混淆代码** - 无法审计的加密代码
5. **已知的恶意来源** - 黑名单仓库

## 配置

在 `~/.claude/config.json` 中配置审核规则：

```json
{
  "skillsVetter": {
    "autoRejectLevel": "high",  // high, medium, low, none
    "strictMode": true,
    "whitelistedSources": [
      "github.com/official-plugins",
      "github.com/trusted-org"
    ],
    "blacklistedSources": [
      "github.com/malicious-user"
    ],
    "checkDependencies": true,
    "checkNetworkAccess": true
  }
}
```

## 与其他技能联动

- **skill-creator**: 创建技能后自动审核
- **skill-seekers**: 下载技能前先审核
- **automation-workflows**: 工作流执行前审核所有涉及的技能

## 注意事项

1. 审核仅做静态分析，无法保证 100% 安全
2. 高危技能需人工复核后才能使用
3. 建议在沙箱环境中测试新技能
4. 定期重新审核已安装的技能

## 命令速查

| 命令 | 说明 |
|------|------|
| `skills-vetter check <path>` | 审核单个技能 |
| `skills-vetter check-all` | 审核所有已安装技能 |
| `skills-vetter report <path>` | 生成详细报告 |
| `skills-vetter watch` | 监控技能目录变化 |
| `skills-vetter whitelist <source>` | 添加信任来源 |
| `skills-vetter blacklist <source>` | 添加黑名单来源 |