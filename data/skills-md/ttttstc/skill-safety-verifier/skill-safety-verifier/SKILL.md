---
name: skill-safety-verifier
description: |
  Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources.
  Checks for red flags, permission scope, and suspicious patterns.
  Provides risk assessment and safety recommendations.
trigger: install.*skill|skill.*install|safety.*check|安全.*检查| vetting.*skill| skill.*risk
---

# Skill Safety Verifier

> Security-first skill vetting for AI agents

## Overview

**Skill Safety Verifier** 是一个安全优先的技能审查工具，用于在安装任何外部技能前进行安全检查。

### Why This Matters

AI agents run with elevated permissions and can:
- Execute arbitrary commands
- Access file systems
- Make network requests
- Read environment variables

**Unvetted skills = security risk**

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SKILL SAFETY VERIFIER FLOW                       │
└─────────────────────────────────────────────────────────────────────────┘

    User Request
         │
         ▼
┌─────────────────────┐
│  1. Fetch Skill    │
│  - Clone/Extract    │
│  - Read SKILL.md    │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Parallel Scan  │
│  ┌───────────────┐  │
│  │ Socket Check  │  │  ← Check outbound connections
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ Vuln Scan     │  │  ← Query GitHub Advisory API
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ Code Patterns │  │  ← Scan dangerous functions
│  └───────────────┘  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Risk Score     │
│  - Calculate total │  ← Network + Vuln + Permission
│  - Classify level  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Present Result │
│  - Risk Radar      │
│  - Warnings       │
│  - Recommendation │
└─────────────────────┘
         │
         ▼
    User Decision
```

---

## Core Responsibilities

### 1. Risk Assessment

Evaluate skills across three dimensions:

| Dimension | What to Check | Risk Level |
|-----------|---------------|------------|
| **Socket/Network** | Outbound connections, API calls | Critical |
| **Code Quality** | Snyk vulnerabilities, dependencies | High |
| **Permissions** | File access, command execution | High |

### 2. Red Flag Detection

Common suspicious patterns:

```yaml
red_flags:
  network:
    - "Suspicious domain (non-standard TLD)"
    - "Hardcoded IP addresses"
    - "DNS lookups to unknown domains"
    - "Excessive outbound connections"
  
  execution:
    - "os.system() / subprocess without sanitization"
    - "eval() / exec() usage"
    - "Shell injection patterns"
    - "Download and execute code"
  
  data:
    - "Reading sensitive env vars"
    - "Exfiltrating files"
    - "Logging keystrokes"
    - "Credential harvesting"
  
  permissions:
    - "Overbroad file permissions"
    - "sudo/root without prompt"
    - "Full disk access requests"
```

### 3. Risk Classification

```
┌─────────────────────────────────────────────────────────────┐
│                    RISK CLASSIFICATION                      │
├──────────────┬──────────────┬─────────────────────────────┤
│    Level     │    Score     │        Action               │
├──────────────┼──────────────┼─────────────────────────────┤
│   🟢 Safe    │    0-10      │  Install & use freely       │
│   🟡 Low     │    11-30     │  Install with caution       │
│   🟠 Medium  │    31-60     │  Review code, then decide   │
│   🔴 High    │    61-100    │  Do not install            │
└──────────────┴──────────────┴─────────────────────────────┘
```

---

## Assessment Criteria

### Socket/Network Risk

| Alert Count | Risk Score |
|-------------|------------|
| 0 | 0 |
| 1-2 | 10 |
| 3-5 | 25 |
| >5 | 50 |

### Code/Vulnerability Risk

| Severity | Score |
|----------|-------|
| Critical | 25 |
| High | 15 |
| Medium | 10 |
| Low | 5 |

### GitHub Advisory API Integration

使用 GitHub Advisory API 获取真实漏洞数据，不阻塞安装流程。

**API**: `https://api.github.com/advisories`  
**认证**: 无需 Token（匿名 60次/小时）  
**TTL**: 本地缓存 24 小时

**流程**:
```
1. 用户触发安装 → 立即返回 "安检中..."
2. 后台并行: 克隆代码 + 查缓存 + 异步请求 API
3. 缓存命中? Yes → 直接返回 | No → 等 API (超时 5s)
4. 合并 Socket分析 + 代码模式 + 漏洞数据 → 呈现
```

### Permission Scope Risk

| Scope | Score |
|-------|-------|
| Read-only | 0 |
| Network calls | 10 |
| File write | 15 |
| Command execution | 25 |
| Full system access | 50 |

---

## Workflow

```
User: "Install skill X"
         │
         ▼
┌─────────────────────┐
│  1. Fetch Skill    │
│  - Clone/Extract    │
│  - Read SKILL.md    │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Security Scan  │
│  - Socket alerts    │
│  - Snyk vulnerabilities│
│  - Code patterns    │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Risk Score     │
│  - Calculate total │
│  - Classify level  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Present Result │
│  - Risk level      │
│  - Warnings        │
│  - Recommendation  │
└─────────────────────┘
         │
         ▼
User Decision
```

---

## Output Format

### Progress Bar Style (Recommended)

```
✅ weather - Risk Assessment

┌─────────────────────────────────────────┐
│  📊 Risk Radar                          │
├─────────────────────────────────────────┤
│  Network      [░░░░░░░░░░░]  0/50  🟢 │
│  Vulnerabil. [░░░░░░░░░░░░]  0/25  🟢 │
│  Permissions  [░░░░░░░░░░░░]  0/50  🟢 │
│  ─────────────────────────────────────  │
│  TOTAL        [░░░░░░░░░░░░]  0/100 🟢 │
├─────────────────────────────────────────┤
│  Dependencies: curl, wttr.in            │
│  Recommendation: ✅ Safe to install     │
└─────────────────────────────────────────┘
```

### Implementation Logic

```python
# Progress bar rendering
def render_bar(score, max_score, label, width=10):
    percent = score / max_score
    filled = int(percent * width)
    bar = '█' * filled + '░' * (width - filled)
    emoji = get_risk_emoji(percent)
    return f"  {label:<12} [{bar}] {score}/{max_score} {emoji}"

# Color mapping
def get_risk_emoji(percent):
    if percent < 0.2: return '🟢'
    if percent < 0.5: return '🟡'
    if percent < 0.8: return '🟠'
    return '🔴'
```

### Safe Skill

```
✅ skill-name - Risk Assessment Complete

┌─────────────────────────────────┐
│  🟢 LOW RISK                   │
│  Socket Alerts: 0               │
│  Snyk Issues: 0                  │
│  Code Patterns: Clean            │
└─────────────────────────────────┘

Recommendation: Safe to install and use.

What's included:
- Feature A
- Feature B
```

### Medium Risk Skill

```
⚠️ skill-name - Risk Assessment Complete

┌─────────────────────────────────┐
│  🟠 MEDIUM RISK                │
│  Socket Alerts: 2               │
│  Snyk Issues: 1 (Medium)        │
│  Notes: Network calls detected   │
└─────────────────────────────────┘

Warnings:
- Makes API calls to external service
- Stores credentials in config file

Recommendation: Review the code before installing.
```

### High Risk Skill

```
🚫 skill-name - Risk Assessment Complete

┌─────────────────────────────────┐
│  🔴 HIGH RISK                   │
│  Socket Alerts: 5               │
│  Snyk Issues: 3 (Critical)      │
│  Red Flags: Command execution    │
└─────────────────────────────────┘

🚨 DO NOT INSTALL

Reasons:
1. Multiple critical vulnerabilities found
2. Executes shell commands
3. No input sanitization

If you must proceed:
- Review every line of code
- Run in sandboxed environment
- Never expose credentials
```

---

## Usage

### Pre-Installation Check

```bash
# Before installing any skill
skill-safety-check --source <skill-url>

# Example
skill-safety-check --source github.com/user/skill-repo
```

### Post-Installation Verification

```bash
# Verify installed skill
skill-safety-check --verify --skill-name <name>
```

### Interactive Mode

```
User: "Install jina-cli"
Agent: [Runs skill-safety-verifier]
→ Analyzes skill
→ Presents risk assessment
→ User decides
```

---

## Integration

### With ClawdHub

```bash
# Install with auto-verification
npx skills add <owner/repo> --verify
```

### With OpenClaw

The verifier runs automatically before skill installation when enabled in config.

---

## Configuration

### Settings

```yaml
# .openclaw/config.yaml
skill_safety:
  enabled: true
  auto_check: true
  block_high_risk: false  # Set true to auto-block
  scan_depth: full        # quick | full
```

### Environment Variables

```bash
SKILL_SAFETY_LOG_LEVEL=info
SKILL_SAFETY_CACHE_TTL=3600
```

---

## Best Practices

1. **Always verify** - Never install unvetted skills
2. **Read the code** - Automated checks aren't enough
3. **Least privilege** - Only grant necessary permissions
4. **Isolate** - Run high-risk skills in containers
5. **Monitor** - Log all skill activity

---

## Related

- [ClawdHub](https://clawhub.com) - Skill marketplace
- [OpenClaw Security](https://docs.openclaw.ai/security) - Platform security docs
- [Skill Writing Guide](https://docs.openclaw.ai/skills/write) - How to write safe skills

---

## License

MIT License - See LICENSE file for details
