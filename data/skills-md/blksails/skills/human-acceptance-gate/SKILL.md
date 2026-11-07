---
name: human-acceptance-gate
description: Identify the current GitHub project and match changed files against a skill-owned JSON path registry, then enforce pre-commit human-acceptance report offers and commit or PR reminders. Use before an agent commits service changes that may require acceptance by a real person, or when maintaining cross-repository caller and implementer rules. Do not trigger from repository identity alone or for ordinary automated test authoring.
---

# Human Acceptance Gate

Maintain a traceable chain from the current Git project and its changed service code to a named acceptance procedure, a commit reminder, and PR evidence. The gate detects risk; it never pretends that a person ran the test.

## Non-negotiable behavior

- Identify the Git worktree and normalized GitHub source remote before matching rules. Never apply one repository's policy to another repository with a similar directory layout.
- Repository identity alone never triggers acceptance. Require both a registered GitHub source and a changed file matching that source's `files`, `directories`, or `globs`.
- Keep the cross-project inventory in [references/project-registry.json](references/project-registry.json), not in application repositories. Record each rule's caller, implementer, upstream, downstream, or data-contract role.
- Derive required flows from matched behavior paths, not from commit wording, repository name, or keyword frequency.
- Keep one stable ID per flow. Renaming display text must not silently invalidate existing commit trailers.
- Agents add the returned trailers and PR evidence reminders. Do not install hooks, CI, package scripts, or policy files into a project unless the user separately requests repository-level enforcement.
- Require environment, tester, time, and evidence for every affected flow. Never auto-check the PR box or invent those values.
- When an agent is about to run `git commit` and detection returns one or more required flows, stop before committing and ask the user whether to generate a test-request report. This question is mandatory even when the surrounding task already authorized committing, deploying, or creating a PR.
- A generated report is an application for a person to test, with status `待人类验收`; it is never proof that testing ran. If the user declines, proceed without a report and state that choice without weakening the acceptance gate.
- After generating a report, include a short, plain-language WeChat message in the user-facing handoff. It must contain actual test actions and expected results, not merely announce that a feature or report exists. It is a notification for the tester, not acceptance evidence.
- Distinguish automated checks from external completion. A passing unit test, HTTP acceptance, Toast, workflow ID, or local row does not prove a downstream platform terminal state.
- Ignore documentation, screenshots, and isolated unit-test edits unless they also change service behavior.
- Keep credentials, cookies, verification-file contents, real customer identity, and production payloads out of commit messages and PR evidence.
- If the real acceptance procedure changes, update its administrator article with `$feature-product-design`; do not duplicate a drifting checklist inside this skill.

Read [references/repository-contract.md](references/repository-contract.md) before changing the registry or evidence format.

## Assess a change

1. Run the global detector from any directory inside the worktree:

   ```bash
   node ~/.codex/skills/human-acceptance-gate/scripts/check-change.mjs --staged
   ```

   For a PR, use `--range <base>..<head>`. The detector normalizes SSH and HTTPS remotes, selects the project from the skill registry, and returns exact matched flows and roles.

2. If `registered` is false, report that the repository has no policy; do not infer one from its folder name.
3. If `registered` is true but `required` is empty, the repository is known but none of its specifically registered files changed, so this gate does not trigger.
4. If a service moves, update `references/project-registry.json` before relying on the result. Do not broaden a rule to the entire repository merely to make detection succeed.
5. Report the acceptance documents that must be executed. A non-trigger does not imply the change needs no other testing.

## Before an agent commits

1. Stage only the intended task files and run `check-change.mjs --staged`.
2. If no required flow is returned, continue the repository's normal commit workflow.
3. If one or more flows are returned, stop before `git commit` and ask exactly one concise blocking question in the user's language. In Chinese, use:

   > 检测到以下流程必须由人类验收：<流程列表>。是否生成“申请人工测试”报告？报告只会创建“待人类验收”的申请，不代表测试已经通过。

4. If the user agrees, generate the report with:

   ```bash
   node ~/.codex/skills/human-acceptance-gate/scripts/generate-test-request.mjs --staged
   ```

   Show the generated path, inspect it for secrets and accurate scope, stage it with the task, then continue the commit.

   Before writing the message, read the generated report and the affected flow's acceptance document when available. Extract two to four concrete checks that a tester can execute. Each numbered check must say both what to do and what should happen. Avoid vague phrases such as “请测试一下”, “重点检查相关功能”, or a release summary without test steps.

   In the same user-facing handoff, provide a copy-ready WeChat message of no more than eight short lines:

   ```text
   【申请人工测试】<流程名称>
   测试环境：<已知环境；未知时写“待确认”>
   请按下面步骤检查：
   1. <登录身份和具体操作>；预期：<页面、数据或外部结果>。
   2. <第二个具体操作>；预期：<对应结果>。
   3. <权限、失败或边界操作，如适用>；预期：<对应结果>。
   详细步骤：<验收文档或生成报告路径>
   完成后请回复“通过”；有问题请附截图和操作时间。
   ```

   Prefer user-visible verbs such as 登录、打开、修改、保存、查询、刷新 and 核对. Do not put file lists, commit trailers, credentials, customer data, or implementation jargon in this message. Do not describe testing as completed until a real tester supplies evidence.

5. If the user declines, do not generate a placeholder or silently mark acceptance complete. Add the detector's stable trailers to the commit message and carry the affected flows into the PR description.
6. Ask again only when the staged code set changes enough to trigger a different set of flows; do not repeatedly ask for the same staged set in one task.

## Commit and PR reminders

For a matched change, append the detector's idempotent trailer block to the commit message:

```text
Manual-Acceptance-Required: yes
Manual-Acceptance: <stable-id[, stable-id...]>
Manual-Acceptance-Docs: <global docs route[, global docs route...]>
```

In the PR description, add one unchecked acceptance item per unique flow with empty environment, tester, time, and evidence fields. Do not check it until a real person has completed the linked procedure.

## Add or change a mandatory flow

1. Define a stable flow ID, repository role, human label, acceptance document, and the narrowest behavior-bearing files or directories.
2. Add the GitHub source and rule to `references/project-registry.json`. Use exact `files` first, `directories` for cohesive modules, and `globs` only for controlled families such as timestamped migrations.
3. Never use `**` or a repository root as a positive match. A repository being registered is not itself a trigger.
4. Test at minimum one matching path, one unrelated source file in the same repository, and exclusions for docs, screenshots, and tests.
5. Create or update the protected acceptance document separately. For BlackSail, use `$feature-product-design` and the admin-only internal-testing section.

## Required validation

Validate the JSON registry, JavaScript helpers, representative matches, same-repository non-matches, and source isolation. Then run any project checks required by actual product-document changes.

```bash
node ~/.codex/skills/human-acceptance-gate/scripts/validate-registry.mjs
```

When product documentation changes, follow that repository's build and visual-inspection requirements. Report separately:

- gate mechanics verified;
- documentation rendered and access-controlled;
- real external manual acceptance still pending or completed, with actual evidence.
