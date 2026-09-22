---
name: github-agentic-workflows
description: Authors, reviews, installs, and debugs GitHub Agentic Workflows in repositories, including workflow markdown, frontmatter, gh aw compile and run flows, safe outputs, security guardrails, and operational patterns. Use when creating or maintaining GH-AW automation. Don't use for standard deterministic GitHub Actions YAML, generic CI pipelines, or non-GitHub automation systems.
license: MIT
metadata:
  author: webmaxru
  version: "1.1"
---

# GitHub Agentic Workflows

## Procedures

**Step 1: Identify the repository state**
1. Inspect the workspace for `.github/workflows/`, `.github/agents/`, existing `.lock.yml` files, and any `gh aw` usage.
2. Execute `node skills/github-agentic-workflows/scripts/find-gh-aw-targets.mjs .` when a Node runtime is available.
3. Run `gh aw version` before making compiler-sensitive decisions so the workflow authoring path matches the installed CLI behavior.
4. If the repository contains multiple candidate workflows, prefer the workflow the user named or the one closest to the active issue, pull request, or automation surface.
5. If the repository has no GH-AW setup and the task is to create or maintain agentic workflows, read `references/authoring.md` before editing.
6. If the task is limited to standard deterministic GitHub Actions YAML without agentic markdown workflows, stop and explain that this skill does not apply.

**Step 2: Choose the working mode**
1. Classify the task as one of: repository setup, new workflow authoring, workflow revision, workflow installation from another repository, security review, or failure debugging.
2. Read `references/examples.md` when the task needs a starting pattern for scheduled reports, issue or PR triage, orchestration, or agent handoff.
3. Read `references/security-and-operations.md` when the workflow needs safe outputs, network policy, authentication, lockdown, threat detection, or run observability.
4. Read `references/troubleshooting.md` when the workflow fails to compile, install, authenticate, execute safe outputs, or access tools.

**Step 3: Author or revise the workflow source**
1. Keep the workflow source of truth in `.github/workflows/<workflow-name>.md`.
2. Use `assets/workflow.template.md` as the base shape when creating a new workflow.
3. Choose the smallest viable trigger surface and repository role scope that satisfies the task.
4. Keep `permissions:` read-only unless the workflow truly needs broader GitHub Actions permissions outside the agentic section.
5. Prefer `safe-outputs:` for comments, issues, labels, PRs, agent assignment, and orchestration instead of granting direct write access to the agent.
6. In safe-output workflows, instruct the agent to call `noop` when no action is required.
7. Keep `tools:` and `toolsets:` minimal and specific to the task.
8. Default to `engine: copilot` unless the task explicitly requires another engine and the repository is already prepared for that engine's authentication model.
9. Configure `network:` with least privilege. Prefer ecosystem identifiers such as `node`, `python`, or `github` over individual registry domains when the compiler supports them.
10. If strict mode and the installed CLI reject custom domains that the workflow still needs, prefetch external sources in deterministic setup steps and pass local files into the agent instead of broadly relaxing the firewall.
11. Do not rely on `${{ steps.<id>.outputs.* }}` placeholders reaching the agent-visible markdown body in real runs. If prompt instructions depend on runtime values, write them into a deterministic local file during setup and tell the agent to read that file.
12. Use imported or reusable workflows only when the repository genuinely benefits from shared logic or orchestration.
13. For recurring work across a dynamic set of inputs, prefer a reusable GH-AW worker plus a deterministic YAML wrapper for discovery and matrix fan-out.
14. When a reusable GH-AW worker is called from a matrix, do not leave it on the default shared workflow-level concurrency group. Set an explicit concurrency group keyed by the matrix input or prompt identity so parallel legs are not cancelled by GitHub's one-running-one-pending concurrency behavior.
15. Recompile the workflow after frontmatter, imports, or other compile-time configuration changes.
16. If only the markdown body changed and the workflow is edited directly on GitHub.com, do not recompile solely for body text changes.
17. Treat `.github/aw/` as transient GH-AW runtime and compiler scratch space during local compile, validate, or trial flows unless the workflow intentionally uses checked-in files from that path.

**Step 4: Configure repository prerequisites and authentication**
1. Read `references/authoring.md` before first-time repository setup.
2. Run `gh aw init` when the repository is not configured for GH-AW authoring and the user wants persistent setup.
3. Configure engine secrets with `gh aw secrets bootstrap` or `gh aw secrets set`.
4. Use `COPILOT_GITHUB_TOKEN` for Copilot engine authentication.
5. For Copilot runs, use a fine-grained PAT in `COPILOT_GITHUB_TOKEN`; a general `gho_...` OAuth token may pass secret checks but still fail real Copilot execution.
6. When using `gh aw trial`, verify that the host repository also has the required engine secret. Secrets from the logical or source repository are not copied automatically into the temporary or reusable host repo.
7. Re-check `gh aw version` after extension upgrades or reinstall paths so the repository guidance and compiler behavior stay aligned.
8. If a deterministic wrapper calls a reusable worker, make the caller workflow permissions at least as broad as the nested worker's requested `actions`, `contents`, and `pull-requests` scopes or the run can fail before agent execution starts.
9. Use a GitHub App or custom GitHub token when the workflow needs cross-repository reads or writes, Projects access, remote GitHub tool mode, or advanced safe outputs.
10. If the repository is public and the workflow will inspect untrusted external content, preserve lockdown and approval controls unless the task is explicitly a low-risk public workflow.

**Step 5: Validate, compile, and execute**
1. Run `gh aw fix --write` when the workflow uses deprecated fields or the compiler points to codemod-able drift.
2. Run `gh aw validate --strict` before treating a workflow as ready.
3. When the CLI version changed or a workflow depends on newer frontmatter behavior, run `gh aw compile --verbose` so warnings and generated-version changes are visible.
4. Run `gh aw compile` after validation succeeds and commit both the `.md` source and the generated `.lock.yml` file.
5. Use `gh aw run <workflow> --dry-run` to validate remote dispatch behavior, especially when you suspect branch, trigger, or workflow-discovery problems.
6. Use `gh aw trial ./.github/workflows/<workflow>.md` when you need to execute a local workflow source before pushing it. The explicit `./` path matters; without it, the CLI may parse the argument as a repository spec instead of a local file.
7. Use `gh aw run <workflow>` for direct execution only after the workflow source or lockfile actually exists on the target branch.
8. Use `gh aw status`, `gh aw logs`, `gh aw audit`, and `gh aw health` to review state, failures, cost, tool usage, and success trends after changes.

**Step 6: Operate and improve professionally**
1. Review whether the workflow can be simplified, split into smaller workflows, or converted into shared components.
2. Prefer staged safe outputs for initial rollout of workflows that create issues, comments, or pull requests at scale.
3. For recurring maintenance, pin or review the installed `gh-aw` version deliberately and update workflows through `gh aw update` or `gh aw upgrade` instead of ad hoc copy-paste.
4. Keep workflow prompts specific, bounded, and auditable. Move broad strategy into reusable imports or agent files when multiple workflows need the same rules.

## Error Handling
* If `gh extension install github/gh-aw` fails, use the standalone installer path documented in `references/troubleshooting.md`.
* If compilation fails, fix frontmatter syntax, deprecated fields, imports, or permission mismatches before continuing.
* If compiler behavior does not match the docs you are reading, trust the installed `gh aw version` and validate against that version before rewriting the workflow shape.
* If `gh aw trial` rejects `.github/workflows/<name>.md` as an invalid repository spec, retry with an explicit local path such as `./.github/workflows/<name>.md`.
* If a reusable worker succeeds in isolation but the wrapper run fails at startup, inspect caller-workflow `permissions:` inheritance before changing the worker logic.
* If a matrix of reusable GH-AW workers cancels most legs immediately, inspect the called workflow's concurrency group first. A shared workflow-level group will cancel pending legs even when `cancel-in-progress` is `false`.
* If a trial run fails on the activation step with `Validate COPILOT_GITHUB_TOKEN secret`, inspect the host repository with `gh secret list -R <host-repo>`. The source repository's secrets are not inherited by the trial host.
* If `gh aw trial --force-delete-host-repo-before` fails, confirm you have admin rights on the host repository and that the current GitHub auth token includes `delete_repo` scope.
* If the workflow prompt still shows unresolved runtime placeholders during execution, move those values into a generated local context file and have the agent read that file explicitly.
* If local `gh aw compile`, `gh aw validate`, or `gh aw trial` commands create `.github/aw/` files such as `actions-lock.json` or logs, treat them as transient byproducts and remove them before commit unless the repository intentionally keeps them.
* If safe outputs do nothing, verify that staged mode is intentional and that the prompt explicitly instructs the agent to call `noop` when no write action is needed.
* If `gh aw mcp inspect` fails on a compiled scheduled workflow source with a fuzzy schedule parsing error, treat that as an inspection-path limitation first. Re-run `gh aw compile`, prefer installed-workflow or run-log based debugging, and do not assume the workflow itself is invalid if validation and compile already passed.
* If the compiler rejects engine fields or tool entries that look valid from older examples, trust the installed schema. In `gh aw v0.58.3`, `engine.max-turns` is not supported for Copilot, `bash` must be `true`, `false`, or an allowlist, and bare `edit:` / `web-fetch:` keys are accepted where boolean values are not.
* If URLs are sanitized as `(redacted)` or tools cannot reach required services, tighten and expand `network.allowed` deliberately rather than disabling the firewall.
* If Copilot inference fails with a configured token, verify that the PAT owner actually has Copilot license and inference access.
* If public-repository workflows miss external contributor content, confirm whether GitHub lockdown mode is blocking that content before changing workflow logic.