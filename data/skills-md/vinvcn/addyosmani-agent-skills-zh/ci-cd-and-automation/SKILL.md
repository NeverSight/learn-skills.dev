---
name: ci-cd-and-automation
description: 自动化 CI/CD pipeline 设置。用于设置或修改构建和部署 pipeline 时；用于需要自动化质量门禁、在 CI 中配置 test runners，或建立部署策略时。
---

# CI/CD 和自动化

## 概览

自动化质量门禁，确保任何变更在进入生产环境前都通过测试、lint、类型检查和 build。CI/CD 是其他所有 skill 的执行机制，它能捕捉人类和 agents 漏掉的问题，并且对每一个变更都一致执行。

**Shift Left:** 尽可能早地在 pipeline 中捕捉问题。Linting 中发现的 bug 只花几分钟；同一个 bug 到生产环境才发现就要花几小时。把检查前移：static analysis 在 tests 之前，tests 在 staging 之前，staging 在 production 之前。

**Faster is Safer:** 更小批次、更频繁发布会降低风险，而不是增加风险。包含 3 个变更的部署比包含 30 个变更的部署更容易调试。频繁发布会建立对发布流程本身的信心。

## 何时使用

- 设置新项目的 CI pipeline
- 添加或修改自动化检查
- 配置部署 pipelines
- 当某个变更应触发自动化验证时
- 调试 CI failures

## 质量门禁 Pipeline

每个变更在合并前都经过这些门禁：

```
Pull Request Opened
    │
    ▼
┌─────────────────┐
│   LINT CHECK     │  eslint, prettier
│   ↓ pass         │
│   TYPE CHECK     │  tsc --noEmit
│   ↓ pass         │
│   UNIT TESTS     │  jest/vitest
│   ↓ pass         │
│   BUILD          │  npm run build
│   ↓ pass         │
│   INTEGRATION    │  API/DB tests
│   ↓ pass         │
│   E2E (optional) │  Playwright/Cypress
│   ↓ pass         │
│   SECURITY AUDIT │  npm audit
│   ↓ pass         │
│   BUNDLE SIZE    │  bundlesize check
└─────────────────┘
    │
    ▼
  Ready for review
```

**任何门禁都不能跳过。** 如果 lint 失败，就修 lint，不要禁用规则。如果测试失败，就修代码，不要跳过测试。

## GitHub Actions 配置

### 基础 CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Test
        run: npm test -- --coverage

      - name: Build
        run: npm run build

      - name: Security audit
        run: npm audit --audit-level=high
```

### 包含数据库集成测试

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Run migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - name: Integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

> **Note:** 即使是仅供 CI 使用的测试数据库，也要用 GitHub Secrets 存放凭据，而不是硬编码值。这能建立良好习惯，并防止测试凭据在其他上下文中被意外复用。

### E2E Tests（端到端测试）

```yaml
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps chromium
      - name: Build
        run: npm run build
      - name: Run E2E tests
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## 将 CI Failures 反馈给 Agents

CI 搭配 AI agents 的力量在于反馈闭环。当 CI 失败时：

```
CI fails
    │
    ▼
Copy the failure output
    │
    ▼
Feed it to the agent:
"The CI pipeline failed with this error:
[paste specific error]
Fix the issue and verify locally before pushing again."
    │
    ▼
Agent fixes → pushes → CI runs again
```

**关键模式：**

```
Lint failure → Agent runs `npm run lint --fix` and commits
Type error  → Agent reads the error location and fixes the type
Test failure → Agent follows debugging-and-error-recovery skill
Build error → Agent checks config and dependencies
```

## 部署策略

### Preview Deployments（预览部署）

每个 PR 都获得一个 preview deployment，用于手动测试：

```yaml
# Deploy preview on PR (Vercel/Netlify/etc.)
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - name: Deploy preview
      run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
```

### Feature Flags（功能开关）

Feature flags 将部署和发布解耦。把未完成或有风险的功能部署在 flags 后面，这样你可以：

- **发布代码但不启用。** 早合并到 main，准备好后再启用。
- **无需重新部署即可回滚。** 禁用 flag，而不是 revert 代码。
- **Canary 新功能。** 先对 1% 用户启用，再到 10%，再到 100%。
- **运行 A/B tests。** 比较有无该功能时的行为。

```typescript
// Simple feature flag pattern
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

**Flag 生命周期：** Create → Enable for testing → Canary → Full rollout → Remove the flag and dead code。永久存在的 flags 会变成技术债，因此创建时就设置 cleanup date。

### 分阶段发布

```
PR merged to main
    │
    ▼
  Staging deployment (auto)
    │ Manual verification
    ▼
  Production deployment (manual trigger or auto after staging)
    │
    ▼
  Monitor for errors (15-minute window)
    │
    ├── Errors detected → Rollback
    └── Clean → Done
```

### 回滚计划

每次部署都应该可回滚：

```yaml
# Manual rollback workflow
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          # Deploy the specified previous version
          npx vercel rollback ${{ inputs.version }}
```

## 环境管理

```
.env.example       → Committed (template for developers)
.env                → NOT committed (local development)
.env.test           → Committed (test environment, no real secrets)
CI secrets          → Stored in GitHub Secrets / vault
Production secrets  → Stored in deployment platform / vault
```

CI 永远不应拥有 production secrets。为 CI testing 使用单独的 secrets。

## CI 之外的自动化

### Dependabot / Renovate

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

### Build Cop 角色

指定某个人负责保持 CI green。当 build 失败时，Build Cop 的职责是修复或回滚，而不是由造成失败的人负责。这可以防止 broken builds 在“别人会修”的假设下累积。

### PR Checks（PR 检查）

- **Required reviews:** 合并前至少 1 个 approval
- **Required status checks:** 合并前 CI 必须通过
- **Branch protection:** 禁止 force-pushes 到 main
- **Auto-merge:** 如果所有检查通过且已批准，自动合并

## CI 优化

当 pipeline 超过 10 分钟时，按影响从大到小应用这些策略：

```
Slow CI pipeline?
├── Cache dependencies
│   └── Use actions/cache or setup-node cache option for node_modules
├── Run jobs in parallel
│   └── Split lint, typecheck, test, build into separate parallel jobs
├── Only run what changed
│   └── Use path filters to skip unrelated jobs (e.g., skip e2e for docs-only PRs)
├── Use matrix builds
│   └── Shard test suites across multiple runners
├── Optimize the test suite
│   └── Remove slow tests from the critical path, run them on a schedule instead
└── Use larger runners
    └── GitHub-hosted larger runners or self-hosted for CPU-heavy builds
```

**示例：缓存和并行**
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

## 常见合理化借口

| 合理化借口 | 现实 |
|---|---|
| “CI 太慢了” | 优化 pipeline（见下面的 CI Optimization），不要跳过它。5 分钟 pipeline 可以避免数小时调试。 |
| “这个变更很小，跳过 CI” | 小变更也会破坏 build。反正 CI 对小变更通常很快。 |
| “测试不稳定，重跑就行” | Flaky tests 会掩盖真实 bug 并浪费所有人的时间。修复 flakiness。 |
| “以后再加 CI” | 没有 CI 的项目会累积 broken states。第一天就设置。 |
| “手动测试就够了” | 手动测试无法扩展，也不可重复。能自动化的都自动化。 |

## 危险信号

- 项目中没有 CI pipeline
- CI failures 被忽略或静音
- 为了让 pipeline 通过，在 CI 中禁用测试
- 没有 staging verification 就部署 production
- 没有 rollback mechanism
- Secrets 存放在代码或 CI config files 中（而不是 secrets manager）
- CI 时间很长但没有优化投入

## 验证

设置或修改 CI 后：

- [ ] 所有质量门禁都存在（lint、types、tests、build、audit）
- [ ] Pipeline 在每个 PR 和 push to main 时运行
- [ ] Failures 会阻塞合并（已配置 branch protection）
- [ ] CI results 会反馈到开发循环
- [ ] Secrets 存放在 secrets manager 中，而不是代码中
- [ ] 部署有 rollback mechanism
- [ ] 测试套件的 pipeline 在 10 分钟内运行完成
