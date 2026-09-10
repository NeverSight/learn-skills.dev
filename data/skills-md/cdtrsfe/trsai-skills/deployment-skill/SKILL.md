---
name: deployment-skill
description: Use when the user asks to deploy, build, run a deployment pipeline, update or sync an image, deploy production, or add deployment configuration for projects using deploy.json with providers such as Apollo, Jenkins, or ArgoCD.
metadata:
  short-description: Route project deployments through provider-specific workflows
---

# Deployment Skill

Use this skill as the only deployment entrypoint for project-root `deploy.json` workflows. It separates user intent, shared deployment workflows, configuration shape, and provider-specific behavior.

When the user writes in Chinese, all user-facing progress updates, questions, and final reports must be in Chinese. Keep API paths, field names, image tags, branch names, commit hashes, and status constants such as `SUCCESS` in their original form.

## Routing

Read only `deploy.json` from the project root for deployment configuration. Do not infer deployment configuration from `package.json`.

When the user only says `部署`, `发布`, `build`, or another generic deployment request and `deploy.json` is missing or has no `provider`, ask which provider to use before asking provider-specific setup questions:

```text
当前项目还没有明确部署方式。

请确认这次走哪种部署：
1. Apollo 部署
2. Jenkins 部署

确认后我再按对应方式补齐配置并继续。
```

Do not ask for an Apollo pipeline name before the user has selected Apollo. Do not ask for Jenkins job/tag fields before the user has selected Jenkins.

Select the target environment before reading environment-specific configuration:

- `dev` means development / `开发环境`.
- `prod` means production / `生产环境`.
- If the user says `部署生产`, `生产部署`, `prod`, or otherwise clearly asks for production, use `prod`.
- In TRS projects, a bare `部署`, `发布`, `build`, or `运行流水线` means the development environment. Use `dev` even when `deploy.json.defaultTarget` is `prod` or only `environments.prod` exists.
- If the user names another environment, use that target key.
- Use `defaultTarget` only for non-TRS projects or when the user explicitly asks to use the configured default target.
- Do not create, discover, or require unrelated target configuration while handling the selected target.
- If the selected target is `dev` and `deploy.json` only contains `prod`, do not deploy or mutate `prod`. Treat `environments.dev` as missing and run `discover-config` for `dev` only.

Use `provider` to choose the provider reference:

- `apollo`: read [providers/apollo.md](providers/apollo.md).
- `jenkins`: read [providers/jenkins.md](providers/jenkins.md).
- `argocd`: read [providers/argocd.md](providers/argocd.md).
- Unknown provider: stop and say the configured provider is not supported yet.

If the user selects Apollo, continue with the Apollo provider rules in this skill. If the user selects Jenkins, treat TRS Jenkins deployments as `git-tag` deployments by default and collect the minimum missing information needed for the selected target. Do not try to rediscover whether Jenkins should be triggered by a Git tag or called directly on every deployment. Only use direct Jenkins triggering when `deploy.json` explicitly sets `trigger: "jenkins-build"` for the selected target or the user explicitly says to start Jenkins directly. For Jenkins `git-tag` projects, one exact Jenkins job URL is usually enough to start configuration when a Git remote already exists; tag naming rules live in the `git-tag-release` skill, not in `deploy.json`.

When asking for one missing Jenkins job URL, do not print a summary of inferred fields such as target, trigger, remote, tag prefix, version type, `editPkg`, or application name. Ask directly and keep example URLs clickable with Markdown links:

```text
请提供这个项目开发环境的 Jenkins Job 完整 URL，例如：[http://192.168.210.40:30080/job/cqwx-dual-grid-h5/](http://192.168.210.40:30080/job/cqwx-dual-grid-h5/)
```

When creating, updating, or validating `deploy.json`, read [config-schema.json](config-schema.json).

When executing a user action, read the selected workflow file and provider reference:

- `build-and-sync`: [workflows/build-and-sync.md](workflows/build-and-sync.md)
- `sync-image-only`: [workflows/sync-image-only.md](workflows/sync-image-only.md)
- `discover-config`: [workflows/discover-config.md](workflows/discover-config.md)

## Action Selection

- `部署`: use target `dev`, then run `build-and-sync`. If `environments.dev` is missing or incomplete, run `discover-config` for `dev` only.
- `部署生产`: use target `prod`, then run `build-and-sync`.
- `build`, `构建`, `运行流水线`: run the provider build flow; sync an image only when the selected target config enables it or the user asks for it.
- `更新镜像 <image>`, `变更镜像 <image>`, `sync image <image>`: run `sync-image-only` with the provided image.
- `更新镜像` with no image: run `sync-image-only` using the provider's latest successful image discovery.
- `添加环境`, `补配置`, missing or incomplete target config: run `discover-config` for only the selected target.

## Safety Boundaries

- Prefer API or CLI execution over UI clicking for deployment operations.
- Do not treat an existing production configuration as permission to deploy production. Production requires a current explicit production request.
- Do not deploy to production or mutate external deployment state when the required target configuration is missing or ambiguous.
- Do not ask for copied browser headers as the normal path. Prefer configured credentials, tokens, API sessions, or a documented provider authentication path.
- Redact raw build/deploy logs before showing them. At minimum mask authorization headers, cookies, tokens, passwords, and `docker login ... -p <value>`.
- When `deploy.json` is created or changed by this deployment workflow and the deployment or image update succeeds, automatically commit only the `deploy.json` change and push it to the current branch's remote. Do not include unrelated files in that commit.
- For Jenkins `git-tag` deployments, do not write tag naming rules such as tag prefix, version type, or rollover policy into `deploy.json`. Pass the selected target (`dev` or `prod`) to `git-tag-release` and let that skill discover existing tags, infer the prefix, and calculate the next tag.
- Before pushing a deployment tag, check whether the project already has runtime tag output capability, such as console output, a visible diagnostic area, or another project-local mechanism that exposes the built `package.json#tag`/build tag at runtime. If it is missing, explain that the final image will not be easy to verify, ask for confirmation, then add the smallest project-consistent tag output code, commit it, and push the branch before previewing or pushing the deployment tag.
- If `git-tag-release` creates a `package.json#tag` release commit during deployment, ensure the current branch commit is pushed to the remote before or along with the tag push. The deployment tag should point at a commit that can be found from the remote branch history whenever the branch can be pushed.
- If Git is unavailable, the project is not a Git repository, no upstream/remote can be determined, or the push fails, do not treat the deployment as failed. Report the deployment success and the Git follow-up problem separately.

## Reporting

Successful deployment reports should stay concise and user-facing:

For Apollo success reports, always include an access URL derived from the selected target and `environments.<target>.applicationName`: `dev` uses `https://ys.dev.trs/<applicationName>/`, and `prod` uses `https://ys.test.trs/<applicationName>/`.

```text
部署完成：<project> / <environment>

构建状态：SUCCESS
打镜像耗时：<duration>

Tag：
<tag>

Commit：
<commit>

镜像：
<full image>

Jenkins：
<build URL>

<环境名称>已同步：
<previous short image> 变更为 <new short image>
```

For image-only updates:

```text
更新完成：<project> / <environment>

镜像：
<full image>

<环境名称>已同步：
<previous short image> 变更为 <new short image>
```

If the provider cannot sync images and only builds, report the build result and produced image, then clearly say no image sync was configured.

If `deploy.json` was committed and pushed after success, include the commit hash and pushed branch in the report. If the Git follow-up was skipped or failed, include the reason.

On failure, report the failed phase, terminal state, the most relevant sanitized failure snippet, and a provider URL where the user can inspect or repair the failed build/deployment.
