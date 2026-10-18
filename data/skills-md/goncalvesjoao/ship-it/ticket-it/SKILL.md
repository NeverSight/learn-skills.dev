---
name: ticket-it
description: "Turn a spec into GitHub tickets using Matt Pocock's to-tickets skill, attaching every ticket as a native sub-issue, adding ticket, and defaulting to status/todo when no status/ label exists."
disable-model-invocation: true
metadata:
  dependency: "to-tickets"
  credits-author: Matt Pocock
  credits-url: https://github.com/mattpocock/skills
---

# Ticket it

## Repository identity

Before GitHub access, Git writes/network operations, delegation, or scheduling, read and follow [the shared identity instructions](references/github-identity.md). Apply them to invoked upstream skills and every worker.

## User questions

Before asking or relaying any user question, read and follow [the user question rules](references/user-questions.md).

Requires Matt Pocock's `to-tickets` skill, its prerequisites, and authenticated `gh`.

## Prepare and draft

1. Locate and read the installed `to-tickets` skill. Use the Skill tool when available; otherwise read its `SKILL.md`. If it or a required capability is missing, report the prerequisite and leave the work incomplete.
2. Read the spec and repository instructions. Resolve the GitHub repository and the existing parent issue associated with the spec from the user's reference, spec metadata, or tracker configuration. When the spec is itself a GitHub issue, use that issue as the parent. Fetch the parent's full body and comments and verify that it is an issue, not a pull request. If the association is missing or ambiguous, ask for the parent issue before publishing. Do not guess or create a replacement parent.
3. Follow `to-tickets`, replacing only its publishing step with the procedure below. Include the resolved parent URL in the proposed breakdown. Every ticket must be a direct sub-issue of that parent, including tickets blocked by other tickets.

## Publish to GitHub

Use explicit repository arguments and safely quoted values. Check `gh auth status` before any writes. Follow the upstream breakdown approval step unless the user has already approved that breakdown.

1. List the parent's existing sub-issues with pagination and inspect any matching tickets, including closed ones, before creating new issues. Reuse tickets for the same approved slice; ask if a match is ambiguous. On resumed runs, also inspect recorded issue URLs and issues referencing the parent, since a previous creation may have succeeded before attachment failed.
2. Ensure `ticket` and the configured triage labels exist in each child repository, preserving existing label settings. Create a missing `ticket` label with `gh label create ticket --repo <owner/repo> --description "Implementation ticket" --color 1D76DB`.
3. Process one approved slice at a time, blockers first. For an unmatched slice, save its body to a temporary Markdown file and create it with:

   ```sh
   gh issue create --repo <owner/repo> --title <title> --body-file <body-file> --label ticket
   ```

   Add the configured triage labels as additional `--label` arguments. Include the parent URL in the upstream template's Parent section. Record the returned URL immediately. Reused tickets skip creation and continue below.
4. For a reused ticket, check its current parent first. Keep a correct attachment; report a different parent as a conflict rather than reparenting. For an unattached child, fetch its numeric REST issue ID and attach it using GitHub's [sub-issues API](https://docs.github.com/en/rest/issues/sub-issues):

   ```sh
   gh api repos/<child-owner>/<child-repo>/issues/<child-number> --jq .id
   gh api --method POST repos/<parent-owner>/<parent-repo>/issues/<parent-number>/sub_issues -F sub_issue_id=<child-id>
   ```

   `sub_issue_id` is the database `id`, not the issue number or GraphQL `node_id`. A parent link in the body does not establish this relationship.
5. Complete labels and native blocking relationships, then verify each child before processing the next slice. Read its labels and parent:

   ```sh
   gh issue view <child-number> --repo <child-owner/child-repo> --json url,labels
   gh api repos/<child-owner>/<child-repo>/issues/<child-number>/parent
   ```

   For new and reused tickets, add `ticket` if missing. Add `status/todo` only when no current label starts with `status/`; if absent from the repository, create it with `gh label create 'status/todo' --repo <child-owner/child-repo>`, preserving existing settings. Use `gh issue edit --add-label` and preserve all existing issue labels. Establish the approved native blocking edges. Fetch the labels again and verify `ticket`, at least one `status/` label, the resolved parent's repository and number, and all approved blocking edges.

If creation, labeling, attachment, or verification fails, stop publishing further tickets. Report the issue URLs already created, the incomplete operation, and the remaining slices. After an uncertain API result, inspect GitHub state before retrying; repair the existing child rather than creating a duplicate. Leave the parent's title, body, labels, and state unchanged and keep created children available for recovery.

## Finish

Claim completion only when every approved slice has a ticket verified in step 5. Return the parent and child URLs with their blockers. Remove temporary body files after success; preserve bodies needed for a retry.
