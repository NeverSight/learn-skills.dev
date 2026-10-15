---
name: create-yss-app
description: 新建或初始化 YSS 微前端微应用工程首选入口，通过官方脚手架与 CLI 交互在线快速生成微前端工程骨架；create yss app scaffold micro-frontend project；当在线从零搭建微应用、新建 qiankun 子应用或运行脚手架创建项目时使用。已有项目开发迭代请转交 yss-frontend-dev，脱机离线创建请改用 yss-create-microapp。
---

# 新建 YSS 微前端微应用工程

本 Skill 是面向用户与 AI 智能体新建微应用工程的**首选顶层入口**，采用极薄封装理念，通过标准化参数推导与交互预检，最终调用官方 `@yss-ui/create` CLI（即 `npm create yss-app`）完成代码生成。

> [!NOTE]
> 在线网络环境下优先使用本 Skill。若处于完全离线环境或无法连通 npm，请切换至后备 Skill `../yss-create-microapp/SKILL.md`。

---

## 触发条件

- 用户要求在线创建、新建或生成 Vue3 + TypeScript + qiankun 微前端子应用工程。
- 用户要求使用 YSS 官方模板脚手架快速搭建新应用工程骨架。
- 用户输入关键词：创建微应用、新建微前端、搭建微前端子应用、create yss app、scaffold micro-frontend。

---

## 不适用场景

- **已有微应用内开发页面**：已有项目请转交 `../yss-frontend-dev/SKILL.md` 或 `../yss-ui-business-page-generation/SKILL.md`。
- **脱机离线或无 npm 网络环境**：无法连接公网 npm 时，转交 `../yss-create-microapp/SKILL.md` 使用内置离线脚本生成。
- **GitLab 建仓或服务器流水线部署**：本 Skill 仅负责本地工程生成，远程仓库与服务器发布请配合雨燕平台。

---

## 硬约束（禁止/必须）

1. **必须环境就绪核查**：Node.js 版本必须 $\ge 18.0.0$，推荐使用 `pnpm`。
2. **必须遵守最少提问原则**：
   - 必填项仅收集：应用英文名 `appName`（小写字母开头，短横线连接，如 `order-center`）与应用中文名 `appNameZh`（如 `订单中心`）。
   - 推导参数：激活路由 `activeRule` 默认推导单段小驼峰（`/orderCenter`）；端口 `port` 从 8081 起向上探测首个空闲端口；接口前缀 `apiBase` 默认为 `/api${activeRule}`；后端代理目标 `proxyTarget` 优先读取环境变量 `YSS_PROXY_TARGET`。更多参数规则详见 [params.md](./references/params.md)。
3. **必须强制执行 `--dry-run --json` 预检门禁**：
   - 在真实落盘生成前，**必须先执行 `--dry-run --json` 获取推导结果**，并将参数表格呈现在用户面前确认，未经用户确认禁止落盘写文件。
4. **禁止目录误覆盖**：检测到目标目录已存在时立即中止（退出码 3），禁止覆盖已有代码。
5. **禁止未经授权的高危操作**：没有用户明确许可，严禁私自执行 `pnpm install`、`pnpm dev`、`git init` 或远程推送。

---

## 标准代码骨架

### 1. 强制预检模式（Dry-run 预览确认）

```bash
npx -y @yss-ui/create "<appName>" \
  --name-zh "<appNameZh>" \
  --target-dir "<targetDir>" \
  --dry-run \
  --json
```

将返回的 JSON 渲染为预览确认表供用户确认：

| 配置项 | 推导值 | 来源/说明 |
|---|---|---|
| 应用英文名 | `order-center` | 命令行参数 |
| 应用中文名 | `订单中心` | 命令行参数 |
| 激活路由 (activeRule) | `/orderCenter` | 自动推导小驼峰 |
| 本地端口 (port) | `8081` | 自动探测首个空闲端口 |
| 目标落盘路径 | `/path/to/order-center` | 目录空闲无冲突 |

### 2. 真实生成落盘

用户确认无误后执行正式落盘命令：

```bash
npx -y @yss-ui/create "<appName>" \
  --name-zh "<appNameZh>" \
  --target-dir "<targetDir>" \
  --yes \
  --json
```

### 3. 项目配套资产初始化

在生成的新微应用工程根目录下同步最新官方 AI Skills（脚手架已集成）：

```bash
npx -y @yss-ui/skills-cli@latest sync
```

---

## 交付检查清单

- [ ] 应用英文名合法（小写字母开头、短横线分隔、不含非法字符）；
- [ ] 激活路由 `activeRule` 与基座对齐（以 `/` 开头单段路径，推荐小驼峰）；
- [ ] 本地开发端口已分配且无冲突；
- [ ] 必须经 `--dry-run --json` 预览确认表获用户同意后生成；
- [ ] 交付报告注明 qiankun 基座集成配置（`activeRule` 与 `entry`）以及独立运行说明。

---

## 失败兜底策略

1. **退出码快速排查**：
   - 退出码 `2`（参数非法）：核查英文名称与路由规范，修正参数后调用，禁止盲目重试；
   - 退出码 `3`（目标已存在）：禁止覆盖，提示用户更换目标目录名；
   - 退出码 `4`（端口冲突）：通过 `--port <port>` 手动传入指定空闲端口；
   - 退出码 `5`（网络/模板拉取失败）：检查网络或切换离线脚本。完整排障见 [troubleshooting.md](./references/troubleshooting.md)。
2. **完全离线 / 无 npm 降级通道**：
   若因内网隔离无法使用公网 CLI，立即提示切换使用内置离线脚本：
   ```bash
   node .agents/skills/yss-create-microapp/scripts/create.mjs \
     --name "<appName>" \
     --name-zh "<appNameZh>" \
     --target-dir "<targetDir>"
   ```
