---
name: shipping-and-launch
description: 准备生产发布。用于准备部署到生产环境，或询问发布前需要准备什么时；用于需要发布前检查清单、设置监控、规划分阶段发布，或需要回滚策略时。
---

# 发布和上线

## 概览

带着信心发布。目标不只是部署，而是安全地部署：监控到位、回滚计划就绪，并且清楚知道成功是什么样子。每次上线都应该是可回滚、可观测、增量推进的。

## 何时使用

- 首次将功能部署到生产环境
- 向用户发布重大变更
- 迁移数据或基础设施
- 开放 beta 或 early access 项目
- 任何有风险的部署（也就是所有部署）

## 发布前检查清单

### 代码质量

- [ ] 所有测试通过（unit、integration、e2e）
- [ ] Build 成功且没有警告
- [ ] Lint 和类型检查通过
- [ ] 代码已 review 并获批准
- [ ] 没有应在上线前解决的 TODO 注释
- [ ] 生产代码中没有 `console.log` 调试语句
- [ ] 错误处理覆盖预期失败模式

### 安全

- [ ] 代码或版本控制中没有 secrets
- [ ] 生态的依赖审计（`npm audit`、`pip-audit`、`cargo audit` 等）没有 critical 或 high 漏洞
- [ ] 所有用户可访问 endpoint 都有输入校验
- [ ] 认证和授权检查已到位
- [ ] 安全 header 已配置（CSP、HSTS 等）
- [ ] 认证 endpoint 已设置 rate limiting
- [ ] CORS 配置为具体 origin（不是通配符）

### 性能

- [ ] Core Web Vitals 在 "Good" 阈值内
- [ ] 关键路径中没有 N+1 查询
- [ ] 图片已优化（压缩、响应式尺寸、lazy loading）
- [ ] Bundle size 在预算内
- [ ] 数据库查询有合适索引
- [ ] 静态资源和重复查询已配置缓存

### 可访问性

- [ ] 所有交互元素都支持键盘导航
- [ ] 屏幕阅读器可以传达页面内容和结构
- [ ] 颜色对比度满足 WCAG 2.1 AA（文本 4.5:1）
- [ ] 模态框和动态内容的焦点管理正确
- [ ] 错误消息具有描述性，并与表单字段关联
- [ ] axe-core 或 Lighthouse 中没有可访问性警告

### 基础设施

- [ ] 生产环境变量已设置
- [ ] 数据库 migration 已应用（或准备好应用）
- [ ] DNS 和 SSL 已配置
- [ ] 静态资源 CDN 已配置
- [ ] Logging 和 error reporting 已配置
- [ ] Health check endpoint 存在且有响应

### 文档

- [ ] README 已更新任何新的 setup 要求
- [ ] API 文档为最新
- [ ] 任何架构决策都有 ADR
- [ ] Changelog 已更新
- [ ] 面向用户的文档已更新（如适用）

## Feature Flag 策略

通过 feature flags 发布，将部署和发布解耦：

```typescript
// Feature flag check
const flags = await getFeatureFlags(userId);

if (flags.taskSharing) {
  // New feature: task sharing
  return <TaskSharingPanel task={task} />;
}

// Default: existing behavior
return null;
```

**Feature flag 生命周期：**

```
1. DEPLOY with flag OFF     → Code is in production but inactive
2. ENABLE for team/beta     → Internal testing in production environment
3. GRADUAL ROLLOUT          → 5% → 25% → 50% → 100% of users
4. MONITOR at each stage    → Watch error rates, performance, user feedback
5. CLEAN UP                 → Remove flag and dead code path after full rollout
```

**规则：**
- 每个 feature flag 都有 owner 和到期日期
- 全量发布后 2 周内清理 flags
- 不要嵌套 feature flags（会产生指数级组合）
- 在 CI 中测试 flag 的两种状态（on 和 off）

## 分阶段发布

### 发布序列

```
1. DEPLOY to staging
   └── Full test suite in staging environment
   └── Manual smoke test of critical flows

2. DEPLOY to production (feature flag OFF)
   └── Verify deployment succeeded (health check)
   └── Check error monitoring (no new errors)

3. ENABLE for team (flag ON for internal users)
   └── Team uses the feature in production
   └── 24-hour monitoring window

4. CANARY rollout (flag ON for 5% of users)
   └── Monitor error rates, latency, user behavior
   └── Compare metrics: canary vs. baseline
   └── 24-48 hour monitoring window
   └── Advance only if all thresholds pass (see table below)

5. GRADUAL increase (25% -> 50% -> 100%)
   └── Same monitoring at each step
   └── Ability to roll back to previous percentage at any point

6. FULL rollout (flag ON for all users)
   └── Monitor for 1 week
   └── Clean up feature flag
```

### 发布决策阈值

用这些阈值判断每个阶段应该继续推进、暂停调查，还是回滚：

| 指标 | 继续推进（green） | 暂停并调查（yellow） | 回滚（red） |
|--------|-----------------|-------------------------------|-----------------|
| Error rate | 基线 10% 以内 | 高于基线 10-100% | >2x baseline |
| P95 latency | 基线 20% 以内 | 高于基线 20-50% | >50% above baseline |
| Client JS errors | 没有新错误类型 | 新错误出现在 <0.1% 的 sessions 中 | 新错误出现在 >0.1% 的 sessions 中 |
| Business metrics | 中性或正向 | 下降 <5%（可能是噪声） | 下降 >5% |

### 何时回滚

如果出现以下情况，立即回滚：
- Error rate 增加到超过 2x baseline
- P95 latency 增加超过 50%
- 用户报告的问题激增
- 检测到数据完整性问题
- 发现安全漏洞

## 监控和可观测性

### 监控什么

```
Application metrics:
├── Error rate (total and by endpoint)
├── Response time (p50, p95, p99)
├── Request volume
├── Active users
└── Key business metrics (conversion, engagement)

Infrastructure metrics:
├── CPU and memory utilization
├── Database connection pool usage
├── Disk space
├── Network latency
└── Queue depth (if applicable)

Client metrics:
├── Core Web Vitals (LCP, INP, CLS)
├── JavaScript errors
├── API error rates from client perspective
└── Page load time
```

### Error Reporting（错误上报）

```typescript
// Set up error boundary with reporting
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Report to error tracking service
    reportError(error, {
      componentStack: info.componentStack,
      userId: getCurrentUser()?.id,
      page: window.location.pathname,
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}

// Server-side error reporting
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  reportError(err, {
    method: req.method,
    url: req.url,
    userId: req.user?.id,
  });

  // Don't expose internals to users
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' },
  });
});
```

### 上线后验证

上线后的第一个小时内：

```
1. Check health endpoint returns 200
2. Check error monitoring dashboard (no new error types)
3. Check latency dashboard (no regression)
4. Test the critical user flow manually
5. Verify logs are flowing and readable
6. Confirm rollback mechanism works (dry run if possible)
```

## Error Budget 发布门禁

服务的 error budget（SLO 允许失败的请求或时间占比）决定现在发布是否安全。把它当作客观门禁，而不是谈判筹码：

```
Budget remaining > 20%  →  Ship normally; monitor closely
Budget remaining 0–20%  →  Slow rollouts only; no high-risk changes
Budget exhausted        →  Freeze feature work; focus entirely on reliability
Budget resets           →  Resume normal pace; bake in the fix that recovered it
```

Canary 期间的高 burn rate（消耗预算的速度快于基线节奏）是上面发布决策阈值表中的**暂停**信号：按 error rate 升高同等处理。

## 回滚策略

每次部署发生之前都需要回滚计划：

```markdown
## Rollback Plan for [Feature/Release]

### Trigger Conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of [specific issue]

### Rollback Steps
1. Disable feature flag (if applicable)
   OR
1. Deploy previous version: `git revert <commit> && git push`
2. Verify rollback: health check, error monitoring
3. Communicate: notify team of rollback

### Database Considerations
- Migration [X] has a rollback: `npx prisma migrate rollback`
- Data inserted by new feature: [preserved / cleaned up]

### Time to Rollback
- Feature flag: < 1 minute
- Redeploy previous version: < 5 minutes
- Database rollback: < 15 minutes
```
## 另请参阅

- 关于每个变更在进入本清单前都要满足的项目级 Definition of Done，见 `../../references/definition-of-done.md`
- 关于发布前安全检查，见 `../../references/security-checklist.md`
- 关于发布前性能检查清单，见 `../../references/performance-checklist.md`
- 关于上线前可访问性验证，见 `../../references/accessibility-checklist.md`
- 关于告警规则和与 SLO 绑定的阈值，见 `observability-and-instrumentation`

## 常见合理化借口

| 合理化借口 | 现实 |
|---|---|
| “它在 staging 能用，production 也会能用” | Production 有不同的数据、流量模式和边界情况。部署后要监控。 |
| “这个不需要 feature flags” | 每个功能都受益于 kill switch。即使“简单”变更也可能破坏东西。 |
| “监控是额外负担” | 没有监控意味着你会从用户投诉而不是 dashboard 中发现问题。 |
| “以后再加监控” | 上线前就添加。看不见的东西无法调试。 |
| “回滚就是承认失败” | 回滚是负责任的工程实践。发布坏功能才是失败。 |
| “Error rate 看起来正常，继续发” | 要看 burn rate，不要只看当前 error rate。消耗预算快于基线就是暂停信号，即使各项单独阈值都是 green。 |

## 危险信号

- 没有回滚计划就部署
- 生产环境没有监控或 error reporting
- Big-bang releases（一次性全部发布，没有 staging）
- Feature flags 没有到期时间或 owner
- 部署后第一个小时无人监控
- 生产环境配置靠记忆完成，而不是靠代码
- “周五下午了，发吧”
- Error budget 已耗尽，但功能开发照常推进

## 验证

部署前：

- [ ] 发布前检查清单已完成（所有部分为 green）
- [ ] Feature flag 已配置（如适用）
- [ ] 回滚计划已记录
- [ ] Monitoring dashboards 已设置
- [ ] 团队已收到部署通知

部署后：

- [ ] Health check 返回 200
- [ ] Error rate 正常
- [ ] Latency 正常
- [ ] 关键用户流程可用
- [ ] Logs 正常流入
- [ ] 回滚已测试，或已验证可随时执行

对每个已发布的服务：

- [ ] Error budget 策略已就位：明确预算跌破 20% 以及耗尽时分别该采取什么行动
