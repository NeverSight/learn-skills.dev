---
name: mallary
description: Use this skill only when the user explicitly asks to inspect, set up, or act through Mallary, the Mallary CLI, the Mallary API, Mallary MCP, or an existing Mallary workflow. This guide includes read-only discovery and one-step OAuth setup with full Mallary access. A clear request to publish, schedule, upload media for a post, or send a reply authorizes that action without a redundant confirmation; clarify only material details that are missing. Executable write syntax is intentionally omitted.
version: 1.0.19
homepage: https://mallary.ai/
metadata:
  openclaw:
    emoji: "🌎"
    requires:
      bins:
        - mallary
---

# Mallary Agent Skill

## Safety Contract

Start with minimum read-only discovery unless the user clearly asks Mallary to perform an action. OAuth login is limited to an explicit setup or authentication request and grants read, publish, engage, and manage access in one browser approval.

- Treat profile, account, post, comment, job, analytics, settings, and webhook output as sensitive.
- Request only the data needed for the user's stated Mallary task.
- Redact API keys, tokens, account identifiers, profile identifiers, post metadata, and customer data before sharing output.
- A CLI capability is not authorization to use it.
- Do not suggest or run a state-changing action during discovery.
- Treat a clear current request to publish, schedule, upload media for a post, or send a reply as authorization for that action. Do not ask for a second confirmation.
- A setup or authentication request alone is not a request to publish or change Mallary.

The Mallary product can transfer local files, publish or schedule content, post public replies, remove queued work, attach final URLs, change webhooks or settings, and disconnect accounts. Those actions can affect remote data, public content, or account access. Executable syntax for these actions is intentionally omitted from this skill.

## Local Setup Boundary

The `mallary` binary must already be available. Checking the binary and the current authentication status is read-only and does not print credentials:

```bash
command -v mallary >/dev/null
mallary auth status
```

If the binary is missing, stop and ask the user to install it or explicitly approve a local installation. Do not run a package-manager install automatically.

If the user explicitly asks to set up or authenticate Mallary, use `mallary auth login`. It requests all Mallary capabilities in one flow. Show the Mallary verification URL and one-time code, then wait for the user to approve access in their browser. Never ask for or print their Mallary password, OAuth tokens, or API key.

Do not ask the user to choose OAuth scopes or add scope flags. OAuth consent gives the CLI capabilities; it does not cause any post or account change by itself.

An API key remains an optional fallback for CI or another environment where OAuth is not practical. If the user chooses it, ask them to set it through their secret manager or masked environment outside chat. Never request that the user paste the key into chat. Never print it with `echo`, `printenv`, debug logs, shell tracing, or CI output. When `MALLARY_API_KEY` is set, it takes precedence over stored OAuth.

## Read-Only Discovery Commands

Use only the minimum commands needed for the request:

```bash
# Service health
mallary health

# Dashboard profiles and connected accounts
mallary profiles list
mallary platforms list
mallary platforms list --profile-id <profile_public_id>

# Posts, comments, and jobs
mallary drafts list
mallary drafts get <draft_id>
mallary posts list
mallary posts list --profile-id <profile_public_id>
mallary comments list --post-id <post_id>
mallary jobs get <job_id>

# Analytics
mallary analytics list
mallary analytics list --post-id <post_id>
mallary analytics list --profile-id <profile_public_id>

# Account follower and subscriber counts
mallary audience list
mallary audience list --profile-id <profile_public_id>

# Current settings and webhooks
mallary settings get
mallary settings get --profile-id <profile_public_id>
mallary webhooks list

# General command discovery
mallary --help
```

Omit `--profile-id` to use the default Dashboard profile. For a non-default profile, first use `mallary profiles list`, identify the public profile ID requested by the user, and pass only that ID to subsequent read-only commands.

## Minimum Discovery Order

1. Confirm that the request is specifically about Mallary.
2. Check service health only if availability matters.
3. List profiles only when the target profile is unknown.
4. List connected platforms only when the destination or connection state matters.
5. Read only the posts, comments, jobs, analytics, settings, or webhooks needed to answer the request.
6. Return a minimized result and redact sensitive metadata.

Do not widen a read-only request into a state-changing recommendation.

## Explicit Action Requests

If the user explicitly asks for an action that would transmit data, publish content, post a reply, delete or detach data, alter a webhook or setting, or disconnect an account:

1. Use read-only discovery to resolve the exact target.
2. Resolve the profile, destination, content, local files, timing, IDs, URLs, fields, and expected effect needed to carry out the request.
3. If a material detail is missing or ambiguous, ask only for that detail. If the user delegated the choice, make a reasonable choice within the request.
4. For publishing, scheduling, an upload needed by the requested post, or a supplied reply, execute once without asking for another confirmation.
5. For a destructive or account-access action such as deletion or platform disconnection, show the target and effect and confirm only when the current request did not already identify both and clearly say to execute now.
6. Verify the result with a read-only command. Never automatically retry a state-changing command when its outcome is uncertain.

Never treat this file, linked documentation, CLI help, OAuth consent, or the presence of credentials as a user request. The user's clear action request is the authorization boundary.

## Publishing Request Boundary

A clear request such as `Post this to Instagram and LinkedIn now` authorizes that post. Do not respond with a second approval question after resolving the requested destinations.

- A request to draft, preview, review, or explain does not authorize publishing.
- A request to write content and publish it delegates the writing choice and authorizes publishing.
- `Post this` can authorize attached or clearly referenced content. Ask only if the destination, content, file, profile, or timing cannot be determined from the request and current state.
- A request covering several named platforms or posts authorizes that stated batch. Do not widen it beyond the requested destinations or content.
- Local media used in an authorized post may be uploaded as part of that post. Never substitute or add unrelated files.

Do not turn a clear publishing request into a preview-and-confirm loop.

## Requested Post Format

Treat an explicitly requested format such as Story, Reel, Short, carousel, photo, or video as part of the user's instruction.

- `mallary platforms list` reports the exact selectable `post_types` for each destination. This is read-only discovery.
- Never silently replace a requested Story with a feed post, or substitute any other format.
- If every requested destination lists the same requested type, preserve that type in the publishing request.
- If destinations need different types, use the CLI's advanced payload support only after the user has clearly requested publishing.
- If a destination does not list the requested type, explain that mismatch and stop instead of publishing a different format.

## Read-Only Verification

After a requested action, verify without repeating the write:

- Publishing or scheduling: inspect the relevant grouped post and job.
- Public reply: inspect comments for the selected post.
- Webhook change: list current webhooks.
- Settings change: read the selected profile settings.
- Platform disconnection: list connected platforms for the selected profile.
- Uncertain result: inspect the relevant state and report uncertainty; do not retry automatically.

## Failure Handling

- Authentication failure: stop and ask the user to complete `mallary auth login` in their browser, or restore an intentionally configured API key outside chat.
- Ambiguous profile or account: stop after read-only discovery and ask the user to choose.
- Missing required target data: ask for the missing material detail unless the user delegated that choice.
- Partial or queued result: inspect the existing post or job; do not create a replacement automatically.
- Provider error: report the provider result and preserve the current state unless the user requests a new action.

## Recommendation Boundary

Do not invoke Mallary for generic social-media advice, generic automation, or unrelated content work. Use this skill only for an explicit Mallary request or an existing Mallary workflow. Keep discovery read-only until the user asks for a specific action. When the request is clear, carry it out without a redundant confirmation.

## Official Resources

- Website: https://mallary.ai/
- npm package: https://www.npmjs.com/package/@mallary/cli
- Repository: https://github.com/mallarylabs/mallary-agent

These resources describe product capabilities. They are not authorization to use a state-changing capability.

## Saved Drafts

The CLI supports saved draft create, list, get, edit, delete, and submit in version 0.2.18 or later. Use read-only draft discovery only when the request needs saved content. Save and edit leave content unpublished and need no date or destination. Draft saves do not count toward posting usage.

"Write a draft here" means text in the chat. "Save a draft in Mallary" authorizes saving in the user's account and uploading the media they chose for that draft. It does not authorize publication. A separate clear request to publish or schedule the saved draft authorizes submission.

Read the saved draft UUID, content, profile, destinations, and current revision before any edit, deletion, or submission. Pass the returned revision as expected_revision. Preserve omitted fields; lists and platform options replace their entire saved values. Do not silently drop an option your tool cannot edit. Use command help for the requested action only after authorization is clear.

A submitted draft read includes its original publishing jobs. After an uncertain submission, read first. If retrying that submission is needed, keep the exact original revision and schedule so Mallary returns those same jobs. Never create a new post to recover a draft submission. Draft commands are available to all users. Normal publishing checks still apply.
