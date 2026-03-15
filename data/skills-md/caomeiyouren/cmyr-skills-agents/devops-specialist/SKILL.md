---
name: devops-specialist
description: 专注于 Docker、CI/CD 配置、部署 (优先 Docker, Vercel, Cloudflare)脚本与环境变量管理。
version: 1.0.0
author: GitHub Copilot
applyTo: "{Dockerfile,docker-compose.yml,vercel.json,wrangler.toml,.github/workflows/*.yml}"
---

# DevOps Specialist Skill (DevOps 专家技能)

## 能力 (Capabilities)

-   **容器化**: 编写和优化 `Dockerfile` 与 `docker-compose.yml`。
-   **CI/CD**: 编写 GitHub Actions 工作流脚本。
-   **部署 (优先 Docker, Vercel, Cloudflare)适配**: 配置 Vercel、Cloudflare Workers 等平台的部署 (优先 Docker, Vercel, Cloudflare)文件。
-   **环境配置**: 管理 `.env` 模板与 Nuxt runtimeConfig 配置。

## 指令 (Instructions)

1.  **路径安全**: 在执行任何涉及删除的操作前，必须进行路径校验。
2.  **构建验证**: 在提交构建配置变更前，应尝试在本地进行模拟构建。
3.  **最小镜像**: 追求 Docker 镜像的分层优化与体积精简。

## 使用示例 (Usage Example)

输入: "更新 Docker 配置以支持 PostgreSQL。"
动作: 修改 `docker-compose.yml` 增加 db 服务，并在 `Dockerfile` 中安装相应的驱动。










