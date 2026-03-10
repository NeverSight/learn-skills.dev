---
name: proactive-agent-skill
description: 让 AI Agent 从被动响应变为主动发现并汇报问题。提供心跳机制、异常检测、主动通知的标准化框架。
homepage: https://docs.openclaw.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🔔",
        "category": "productivity",
        "requires": { "bins": [] },
      },
  }
---

# Proactive Agent Skill - 主动性框架

让 AI Agent 从"等命令"变成"主动发现并汇报"。

---

## 核心理念

传统 Agent：被动执行，有问题才响应
Proactive Agent：主动检查，提前发现，立即汇报

---

## 三层主动性架构

### 层 1: 心跳机制（定时触发）

定义定期检查任务，确保 Agent 不会"睡死"。

**实现方式**：
```bash
# HEARTBEAT.md 定义心跳触发
Read HEARTBEAT.md if it exists (workspace context). Follow it strictly.

# 当心跳触发时，Agent 自动执行定义的任务
```

**心跳任务示例**：
```markdown
# HEARTBEAT.md

## 记忆维护（每 24 小时）
如果距离上次记忆维护超过 24 小时：
  node scripts/memory-maintenance-v2.js

## BotLearn 社区（每 4+ 小时）
如果距离上次检查超过 4 小时：
  检查社区动态
  对有价值的帖子点赞
  记录到 memory/YYYY-MM-DD.md

## 系统健康（每 8 小时）
检查磁盘空间、CPU 使用率、关键服务状态
```

**心跳状态追踪**：
```json
// memory/heartbeat-state.json
{
  "lastChecks": {
    "memoryMaintenance": 1741236131,
    "botlearn": 1741235460,
    "systemHealth": 1741230000
  },
  "lastHeartbeat": 1741236131
}
```

---

### 层 2: 异常检测（执行时监控）

在执行任务时，实时监控关键指标，判断是否异常。

**异常指标类型**：

| 类型 | 指标 | 阈值 | 示例 |
|------|------|------|------|
| 性能 | CPU 使用率 | > 90% | 进程卡住 5 分钟 |
| 性能 | 执行时间 | > 预期 10x | 5 秒任务跑了 50 秒 |
| 性能 | 文件大小 | > 1M 行 | MEMORY.md 100万+ 行 |
| 数据 | 增长趋势 | 指数级（O(n²)） | 关联数每次翻倍 |
| 数据 | 内存泄漏 | 持续增长 | RSS 每 10 分钟 +100MB |
| 业务 | 关键失败 | > 3 次 | Cron 任务连续失败 |
| 外部 | API 错误 | insufficient_quota | OpenAI 配额不足 |

**检测模式**：

```javascript
// 示例：执行时检测异常
function runWithMonitoring(task, thresholds) {
  const startTime = Date.now();
  const startMemory = process.memoryUsage().rss;

  const result = task();

  const duration = Date.now() - startTime;
  const memoryDelta = process.memoryUsage().rss - startMemory;

  // 检查异常
  const anomalies = [];

  if (duration > thresholds.maxDuration * 10) {
    anomalies.push({
      type: 'PERFORMANCE',
      metric: 'duration',
      actual: duration,
      threshold: thresholds.maxDuration * 10,
      severity: 'critical'
    });
  }

  if (memoryDelta > thresholds.maxMemoryDelta) {
    anomalies.push({
      type: 'MEMORY',
      metric: 'leak',
      actual: memoryDelta,
      threshold: thresholds.maxMemoryDelta,
      severity: 'warning'
    });
  }

  return { result, anomalies };
}
```

---

### 层 3: 主动汇报（立即通知）

发现异常后，立即通知用户，不等被问。

**汇报原则**：

| 原则 | 说明 |
|------|------|
| **立即性** | 发现即汇报，不等心跳周期 |
| **结构化** | 问题 + 证据 + 影响 + 建议 |
| **可操作** | 给用户明确的下一步 |
| **不过度** | 只汇报需要决策的问题 |

**汇报模板**：

```javascript
// 标准化异常汇报
function reportAnomaly(anomaly) {
  const report = {
    severity: anomaly.severity,
    title: anomaly.title,
    problem: anomaly.problem,
    evidence: anomaly.evidence,
    impact: anomaly.impact,
    recommendations: anomaly.recommendations
  };

  // 发送到用户主渠道
  message({
    action: 'send',
    channel: 'telegram', // 或其他主渠道
    to: USER_ID,
    message: formatReport(report)
  });

  // 记录到 memory/YYYY-MM-DD.md
  logToMemory(report);
}
```

**汇报格式示例**：

```
严重问题发现：

## 问题描述
MEMORY.md 过大（1,057,975 行），导致交叉引用分析无法完成

## 证据
- 记忆维护从 2026-03-01 开始运行
- 到 2026-03-06 仍在运行（5+ 天）
- 关联数增长：12k → 196k（指数级）

## 影响
- 心跳任务卡住，无法执行其他检查
- 内存占用持续增长

## 建议方案
1. 归档旧记忆（按时间分割）
2. 限制关联分析范围
3. 重构记忆维护脚本（增量更新）

等待你的决策。
```

---

## 实施步骤

### 步骤 1: 创建 HEARTBEAT.md

在 workspace 目录创建 HEARTBEAT.md，定义心跳任务：

```markdown
# HEARTBEAT.md

## 任务 1: 记忆维护（每 24 小时）
如果距离上次超过 24 小时：
  - 执行维护脚本
  - 检查执行结果
  - 记录到 memory/maintenance.log

## 任务 2: 系统健康（每 8 小时）
检查：
  - 磁盘空间
  - CPU 使用率
  - 关键服务状态

## 任务 3: 社区动态（每 4 小时）
  - 检查 BotLearn 社区
  - 点赞有价值的帖子
```

### 步骤 2: 创建 heartbeat-state.json

初始化状态追踪：

```json
{
  "lastChecks": {
    "task1": null,
    "task2": null,
    "task3": null
  },
  "lastHeartbeat": null
}
```

### 步骤 3: 在脚本中集成异常检测

```javascript
// 在心跳任务中添加监控
const result = runWithMonitoring(
  () => runMemoryMaintenance(),
  { maxDuration: 30000, maxMemoryDelta: 100 * 1024 * 1024 }
);

if (result.anomalies.length > 0) {
  reportAnomaly({
    title: '记忆维护异常',
    problem: '执行超时',
    evidence: result.anomalies,
    impact: '心跳任务卡住',
    recommendations: ['检查脚本逻辑', '调整阈值']
  });
}
```

### 步骤 4: 定义汇报渠道

在 MEMORY.md 或 TOOLS.md 中记录用户主渠道：

```markdown
## 重要渠道配置

### Telegram
- Bot 用户名: @your_bot
- 用户 ID: 123456789
- DM 策略: pairing（已授权）
```

### 步骤 5: 记录到日志

每次汇报都记录到 daily memory：

```markdown
# 2026-03-06

## 主动发现问题

**时间**: 09:11 AM
**类型**: PERFORMANCE
**严重程度**: critical
**问题**: MEMORY.md 过大
**行动**: 已汇报给用户，等待决策
```

---

## 检查清单

使用这个技能前，确保：

- [ ] HEARTBEAT.md 已创建，定义了心跳任务
- [ ] heartbeat-state.json 已初始化
- [ ] 心跳脚本中集成了异常检测
- [ ] 用户主渠道已在 MEMORY.md 中配置
- [ ] 汇报格式已定义（问题 + 证据 + 影响 + 建议）
- [ ] 日志记录机制已建立

---

## 常见异常类型

### 性能异常
- 任务执行时间 > 预期 10x
- CPU 使用率持续 > 90%
- 内存持续增长（泄漏）

### 数据异常
- 文件大小 > 阈值
- 增长趋势异常（指数级）
- 数据格式错误

### 外部依赖异常
- API 配额不足
- 网络超时
- 第三方服务不可用

### 业务异常
- 关键任务连续失败 > 3 次
- 关键数据丢失
- 用户反馈异常

---

## 最佳实践

### DO ✅

- **主动汇报**：发现问题立即通知，不要等
- **结构化信息**：问题、证据、影响、建议
- **可操作建议**：给用户明确的下一步
- **记录日志**：每次汇报都记录到 memory
- **适度频次**：不要过度汇报，只汇报重要问题

### DON'T ❌

- **沉默不报**：等待用户发现
- **模糊描述**："出了点问题"（没有证据）
- **过度报警**：每个小异常都汇报
- **无建议汇报**：只说问题，不给方案
- **忽视反馈**：用户说不需要的还要汇报

---

## 示例案例

### 案例 1: MEMORY.md 过大（本次）

**发现路径**：心跳 → 执行检测 → 主动汇报
**异常指标**：CPU 93.5%, 运行 5+ 天, 文件 100万+ 行
**汇报时机**：立即（不等心跳周期）
**结果**：用户决策重构脚本，问题已解决

### 案例 2: OpenAI API 配额不足

**发现路径**：用户发送语音 → 转录失败 → 主动告知
**异常指标**：insufficient_quota 错误
**汇报时机**：发现即汇报
**结果**：用户知道需要充值

### 案例 3: Cron 任务失败

**发现路径**：心跳检查 → 日志显示失败 5 次 → 主动汇报
**异常指标**：连续失败 5 次
**汇报时机**：发现即汇报
**结果**：用户及时修复，避免影响业务

---

## 扩展：从 Agent 到社区

### 1. 提交到 ClawHub

这个技能可以打包提交到 ClawHub，供其他 Agent 使用：

```bash
openclaw skill publish proactive-agent-skill
```

### 2. 创建模板

提供现成的 HEARTBEAT.md 模板：

```markdown
# HEARTBEAT.md

## 每日检查
- [ ] 任务 1
- [ ] 任务 2

## 每 4 小时检查
- [ ] 任务 3
```

### 3. 文档和教程

编写详细教程：
- 如何定义心跳任务
- 如何设置异常阈值
- 如何配置汇报渠道

### 4. 社区分享

在 BotLearn 社区分享经验：
- 写帖子介绍主动性框架
- 回答其他 Agent 的问题
- 分享实战案例

---

## 总结

主动性 = 心跳 + 检测 + 汇报

**三层架构**：
1. **心跳机制**：定期检查，确保 Agent 不"睡死"
2. **异常检测**：执行时监控，及时发现异常
3. **主动汇报**：发现即通知，不等用户问

**关键原则**：
- 立即性（发现问题即汇报）
- 结构化（问题 + 证据 + 影响 + 建议）
- 可操作（给用户明确下一步）
- 不过度（只汇报重要问题）

让每个 Agent 都从"工具"变成"伙伴"。
