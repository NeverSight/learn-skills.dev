---
name: dreamina-cli
description: Use when an agent needs to install, update, authenticate, troubleshoot, or operate Dreamina（即梦） CLI across account, session, image, video, task-query, and download workflows.
license: Complete terms in LICENSE.txt
---

# Dreamina CLI

Use this skill when you need Dreamina（即梦） image or video generation, login, session management, or task history work through `dreamina`.

即梦 is the Chinese product name of Dreamina. If the user says 即梦, treat it as Dreamina and use this skill.

This skill is intentionally short. Detailed flags and supported values belong to the CLI itself, so always treat `dreamina -h` and `dreamina <subcommand> -h` as the primary reference.

Read references progressively:

- For installation, authentication, account checks, every public command family,
  Session CRUD, update, and log troubleshooting, read
  [references/official-cli-install-to-use.md](references/official-cli-install-to-use.md).
- For v1.4.18 model, resolution, duration, and ratio constraints, read
  [references/dreamina-cli-v1.4.18-contract.md](references/dreamina-cli-v1.4.18-contract.md).

## When to use and boundary

Use this umbrella skill from first-time installation through troubleshooting, or
when login, sessions, task history, async follow-up, or command routing spans
multiple modalities. Do not use it as a replacement for the four execution
skills' mode-specific workflow or for prompt-only authoring.

## What this tool is for

`dreamina` is the local CLI entrypoint for all currently exposed Dreamina（即梦） image and video generation workflows, plus the account/session operations around them.

Use it for:

- checking or reusing an existing Dreamina login session
- checking account credit
- managing sessions with `dreamina session`
- clearing the local OAuth login state with `dreamina logout`
- submitting image generation tasks
- submitting video generation tasks
- querying async task results and downloading result media
- reviewing saved task history

## Default workflow

When using this CLI as an agent:

### Step 1：验证环境

If `dreamina` is missing, read the install-to-use reference and obtain explicit
authorization before installing or updating software. Otherwise start with
`dreamina version` and `dreamina -h`, then run `dreamina <subcommand> -h` before
real use.

### Step 2：完成认证与路由

Reuse login unless the user requests a login-state change. Use `user_credit` as
the post-login readiness check. Route generation to the matching execution
skill.

### Step 3：提交与终态闭环

Warn about credit consumption, distinguish help inspection from real submit, and follow every accepted task until `success` or `fail`.

## Validation

- Validate the installed CLI help against the reviewed contract before changing model or resolution assumptions.
- Discover video ratio support at runtime with `dreamina <subcommand> --help`: four video commands expose `--ratio`, while `multiframe2video` infers it from the first image.
- Validate local files before upload and preserve every returned `submit_id`.
- Validate terminal status from `query_result`, not shell exit code alone.

## Gotchas

1. **Help drift**: release notes are not a substitute for current subcommand help.
2. **Double fact source**: keep parameter matrices in the v1.4.18 contract reference.
3. **Accepted versus successful**: `querying` is not terminal success.
4. **Paid action**: warn before any real generation submit.
5. **OAuth pause**: always report whether login succeeded, was reused, or failed.
6. **Troubleshooting order**: capture the exact command, error, `dreamina version`,
   and relevant `~/.dreamina_cli/logs/` excerpt; redact secrets, update the CLI
   with authorization, then retry the same command once.

## Login completion: mandatory user-visible confirmation

`dreamina login` / `dreamina relogin` prints OAuth Device Flow instructions and then waits for authorization. When the command finishes successfully, tell the user explicitly that login succeeded or the local OAuth state was reused.

- **Do not** wait for the user to ask “登录好了吗”.
- **Do not** stop after only sending the device code: keep the login command running, read stdout to the end, then confirm success/reuse/failure.
- **Failure** must still be reported with the concrete error and the next step.

## Choosing the right command

At a high level:

- Use `user_credit` to check budget.
- Use `session` to create, list, search, rename, or delete sessions; all generator commands accept `--session=<id>` and `0` is the default session.
- Use `query_result` when you already have a `submit_id`; add `--download_dir` when you want the generated media saved locally.
- Use `list_task` to review recent saved tasks, especially when you want to filter by status or task type.
- Use `text2image` for prompt-only image generation, `image2image` for image-guided editing, and `image_upscale` for upscaling.
- Use `text2video` for prompt-only video generation.
- Use `image2video` when one main image is enough; if the user has multiple images for a coherent story, prefer `multiframe2video`.
- Use `frames2video` for first-and-last-frame driven video generation.
- Use `multiframe2video` for Dreamina's intelligent multi-frame flow: multiple images in, one coherent story video out.
- Use `multimodal2video` for Dreamina's flagship video mode when the task needs all-around references across images, video, and audio; it supports the `seedance2.0` family. If the legacy name `ref2video` appears, trust `dreamina -h` for the current command surface.

For the exact flags and supported combinations, rely on each subcommand's `-h`.

## Model selection rule

Do not hardcode model support from this skill.

If the user specifies a model, always check the relevant subcommand help before running it:

```bash
dreamina <subcommand> -h
```

Use the subcommand help to confirm:

- whether that command exposes model selection
- whether the requested model is supported on that command
- what other constraints apply to that model, such as duration, ratio, resolution, or whether the command supports `model_version` at all

Additional guidance:

- some commands do not expose model selection at all
- some models, especially the `seedance2.0` family, can be capacity-constrained
- if the user cares more about speed than maximum quality, do not default to `seedance2.0` unless they explicitly ask for it

## How to judge submit acceptance and terminal success

Do not rely on shell exit code alone.

For async generation commands, `submit_id` plus `gen_status=querying` means only that the
submission was accepted. Treat the generation as terminally successful only when
`gen_status=success`. If `gen_status=fail`, inspect `fail_reason` and reply proactively.

## Follow-up pattern for async tasks

After a submit returns `querying`:

1. Save the `submit_id`.
2. Use `query_result --submit_id=<id>` for follow-up.
3. Use `list_task` when you want to review saved tasks in bulk.
4. Continue until the task reaches `success` or `fail`.

If you are running a test sweep, keep results in a machine-readable format so you can query the returned `submit_id` values later.

## Important user-facing rules

- Some generation commands are asynchronous; submit and query are separate steps.
- Some models may require a one-time authorization on Dreamina Web.
  If the CLI returns `AigcComplianceConfirmationRequired`, reply proactively: ask them to complete that web-side confirmation first, then retry.
- Do not assume that different commands support the same models, ratios, durations, or resolutions.
  Check each subcommand's `-h` before use.
- In v1.4.18, `text2video` and `multimodal2video` accept explicit `--ratio`; `image2video`
  and `frames2video` expose the flag but reject it with `seedance2.5`; `multiframe2video`
  has no ratio flag. Re-discover these rules at runtime instead of generalizing across commands.

## Good agent behavior

- Relay OAuth Device Flow instructions exactly enough for the user to complete login.
- Always close the loop when the login command finishes with a user-visible confirmation.
- Prefer small, reviewable batches when running real generation tasks.
- Keep a record of the command, arguments, `submit_id`, and final status for every paid test you run.
- When the user cares about generation speed, do not default to the `seedance2.0` family unless they explicitly ask for it or clearly prioritize output quality.
- If you are preparing a report, separate:
  - help-only inspection
  - submit-stage validation
  - later async result follow-up
