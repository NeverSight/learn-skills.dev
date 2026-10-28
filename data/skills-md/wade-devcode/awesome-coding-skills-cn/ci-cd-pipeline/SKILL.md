---
name: ci-cd-pipeline
description: 配置 CI/CD 流水线时使用。快、稳、可重复、可回滚。
category: devops
tags: [ci,cd,流水线]
---

# CI/CD 流水线

## 何时用

- 新建或修改任何 CI/CD 配置文件（GitHub Actions、GitLab CI、Jenkinsfile 等）。
- 流水线频繁失败、构建结果不一致、部署不可回滚时。
- 接入新项目或新环境时设计部署策略。
- 发现流水线中存在硬编码密钥或依赖隐式环境时。

## 核心规则

### 1. 阶段清晰，前序失败即停

**规则：** 流水线按 `lint → test → build → deploy` 顺序分阶段，每个阶段只做一件事；前序阶段失败，后续阶段不执行。

**为什么：** AI 生成的 CI 配置最常见的问题是把 lint、测试、构建、部署全塞进一个 job，或者测试失败后继续往生产部署。曾见过真实事故：测试报告里明确有失败用例，因为 YAML 里 `continue-on-error: true` 被随手加上，部署仍然执行，问题代码上了生产。

**怎么做：**
```yaml
# GitHub Actions 示例
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    needs: lint        # ✅ 显式依赖，lint 失败即停
    runs-on: ubuntu-latest
    steps: [...]

  build:
    needs: test        # ✅ 测试通过才构建
    steps: [...]

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'   # ✅ 只部署 main 分支
    steps: [...]
```
- 不加 `continue-on-error: true`，除非确实需要收集所有失败报告再决策。

---

### 2. 构建可重复：锁版本 + 缓存 + 产物带标识

**规则：** 锁定所有工具和依赖的版本；缓存依赖目录加速重复构建；构建产物打上版本标识（commit SHA 或语义版本），使每次构建可追溯。

**为什么：** AI 配置 CI 时倾向于用 `npm install`（不加 `--frozen-lockfile`）、不固定 Action 版本（`uses: actions/checkout@main`）、不给镜像打 tag。结果：同一份代码在不同时间构建出不同产物，线上出问题却无法精确定位是哪个版本，依赖每次都重新下载让构建平均耗时从 30 秒变成 5 分钟。

**怎么做：**
```yaml
- uses: actions/setup-node@v4          # ✅ 固定 Action 版本
  with:
    node-version: '20'
    cache: 'npm'                        # ✅ 启用依赖缓存

- run: npm ci                           # ✅ 使用 lockfile，拒绝版本漂移

- name: Build & tag image
  run: |
    IMAGE_TAG="${{ github.sha }}"       # ✅ 用 commit SHA 作镜像标签
    docker build -t myapp:${IMAGE_TAG} .
    docker push myapp:${IMAGE_TAG}
```

---

### 3. 密钥走 secret store，最小权限

**规则：** 所有密钥、API token、部署凭据通过 CI 平台的 secret 机制注入，绝不硬编码进 YAML；为 CI 服务账号配置最小权限（只读仓库 + 只写目标服务），不用个人账号或 admin token。

**为什么：** AI 生成 CI 配置时极容易在 `env:` 块里直接写 `AWS_SECRET_KEY: "AKIA..."` 或在 `run:` 步骤里明文打印环境变量。这类配置一旦提交进公开仓库，密钥立刻面临泄露，且 git 历史删不干净。2023 年 GitHub 上每天有数千个 API key 因为这类配置被意外泄露。

**怎么做：**
```yaml
- name: Deploy
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}       # ✅ 引用 secret
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: aws s3 sync dist/ s3://my-bucket/
  # ❌ 不要 run: echo $AWS_SECRET_ACCESS_KEY（日志会打印出来）
```
- IAM role / OIDC 优于长期密钥；部署账号只有目标环境的写权限，无法操作其他环境。

---

### 4. 部署可回滚：灰度先行，失败自动退回

**规则：** 保留上一个成功版本的产物/镜像；生产部署先做金丝雀或蓝绿发布，确认健康检查通过再全量切流；部署失败时自动回滚到上一版本。

**为什么：** AI 生成的部署步骤通常是直接 `kubectl set image` 或 `scp` 覆盖，没有回滚机制，没有健康检查等待。一旦新版本有严重 bug，需要人工介入恢复，恢复期间服务持续不可用。曾有团队因为这一点，在凌晨生产故障时花了 40 分钟才恢复，原因仅仅是"不知道上一个镜像 tag 是什么"。

**怎么做：**
```yaml
- name: Rolling deploy with health check
  run: |
    kubectl set image deployment/myapp app=myapp:${{ github.sha }}
    kubectl rollout status deployment/myapp --timeout=5m   # ✅ 等待健康
  # 失败时自动触发回滚
- name: Rollback on failure
  if: failure()
  run: kubectl rollout undo deployment/myapp               # ✅ 失败即回滚
```
- 始终保留最近 3 个版本的镜像，不立即删除旧版本。

---

### 5. 流水线可本地复现，不依赖隐式环境

**规则：** 流水线所依赖的工具、环境变量、服务都通过配置显式声明；开发者能在本地用相同配置复现 CI 行为，不靠某台机器的特殊状态。

**为什么：** AI 生成的 CI 脚本常常隐式依赖 runner 上预装的工具（特定版本的 Python、某个全局 npm 包），在一台机器上通过，换一台或 runner 镜像升级后就失败。更严重的是这种失败只在 CI 上出现，本地无法复现，排查极耗时间。

**怎么做：**
- 用 `setup-node`、`setup-python` 等 Action 显式安装工具，不依赖 runner 预装。
- 本地测试用 `act`（GitHub Actions 本地运行器）或同款 Docker 镜像模拟 CI 环境。
- 把环境初始化步骤写成幂等脚本（`scripts/setup.sh`），既在 CI 用，也供开发者本地运行。
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'          # ✅ 显式声明，不依赖系统 Python
- run: pip install -r requirements.txt
```

---

## 正例 / 反例

### 反例：全在一个 job、硬编码密钥、无回滚

```yaml
# 反例
jobs:
  all-in-one:
    runs-on: ubuntu-latest
    steps:
      - run: npm install             # ❌ 不锁版本
      - run: npm test
        continue-on-error: true      # ❌ 测试失败也继续
      - run: npm run build
      - run: |                       # ❌ 密钥硬编码
          HEROKU_API_KEY=abc123 heroku deploy
```

### 正例：分阶段、密钥安全注入、带回滚

```yaml
# 正例
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci && npm run lint          # ✅ 锁版本，依赖缓存

  test:
    needs: lint                              # ✅ 阶段依赖
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci && npm test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}   # ✅ secret 注入
        run: heroku container:push web --app myapp
      - name: Rollback on failure
        if: failure()
        run: heroku rollback --app myapp                  # ✅ 失败回滚
```

---

## 自查清单

- [ ] 流水线有明确的阶段划分，前序失败不会触发后续阶段。
- [ ] 所有 Action 版本、工具版本、依赖版本均已固定，构建结果可重复。
- [ ] 构建产物带有版本标识（commit SHA 或语义版本标签）。
- [ ] 所有密钥通过 CI secret 机制注入，YAML 里没有任何明文凭据。
- [ ] 部署步骤有健康检查等待，失败时有自动回滚机制。
- [ ] 保留了上一个成功版本的产物，可随时手动触发回滚。
- [ ] 流水线所有依赖均显式声明，开发者能在本地用相同配置复现 CI 行为。
