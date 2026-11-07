---
name: leaving-pr-comments
description: "Trigger only when the user or another skill explicitly invokes this skill."
---

# Leaving PR Comments

Run only when the user explicitly invokes `$leaving-pr-comments` (Codex) or
`/leaving-pr-comments` (Claude Code), or another skill explicitly instructs you to invoke
this skill.
Mentions, examples and matching tasks alone do not trigger this workflow.

Handle the requested PR communication from context to verified publication.
Work independently with a PR or thread and the requested message or findings;
no council, full-review or delivery run is required. An explicit request to post
or an invoking workflow that includes publication is authorization to post.
A request to draft, suggest or reword returns text only.

For a supplied-text rewrite, preserve the meaning and return the revised text
directly. No PR URL, remote lookup or identity discovery is required. Do not add
new factual claims or an attribution wrapper unless requested. Use the remaining
workflow when the task needs PR context, claim verification or publication.

## Prepare

Read the current head, relevant diff, existing comments and thread history.
Validate claims against current code and available evidence. For each actionable
finding explain the trigger, consequence and useful next step. Prefer one clear
issue per comment; omit speculative complaints, duplicates and already fixed
findings. Do not start a new full review or edit the implementation.

Use this prefix on its own line for agent-authored comments and replies:

```md
🤖 **<model> responding on behalf of <user>**

Actual comment starts here.
```

Use the model identity supplied by the host (or the host name if unavailable)
and the verified user name or authenticated GitHub login. Do not guess identity.
Exclude PR descriptions, commit messages and text the user requests verbatim.
Limit every comment or reply body to at most two sentences, excluding the
attribution prefix. Apply the same limit to drafts and supplied-text rewrites;
combine the trigger, consequence and next step within those two sentences.
Distinguish observations from judgment, and check the
complete text and attachments for private data and formatting.

## Publish and follow up

1. Recheck the current head and whether the message still applies. Post findings
   on valid diff lines, replies in their existing thread and general summaries as
   top-level comments. If an inline-only request cannot be anchored, report that
   limitation instead of silently changing the publication format.
2. Publish the authorized messages without another approval checkpoint. For
   review comments use COMMENT unless a formal review decision was explicitly
   requested. After a timeout or ambiguous response, inspect the remote state
   before retrying so the same message is not posted twice.
3. Verify the published body and returned URL. When thread resolution is within
   the request, verify the fix or explain withdrawal before resolving, and only
   after the reply succeeds. Resolve only threads owned by this review workflow
   unless managing other reviewers' threads was explicitly authorized. An
   outdated diff, “fixed” reply or green CI alone does not establish resolution.

Keep responses to the user to at most two sentences. Return posted URLs,
drafted text when requested, and any withheld message with
its reason. Do not merge, change PR status or monitor indefinitely unless that
additional work belongs to the caller's request.
