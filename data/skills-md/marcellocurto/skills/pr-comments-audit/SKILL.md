---
name: pr-comments-audit
description: Audit open pull-request comments, fix and push the justified ones, and reply to and resolve each thread.
---

# PR Comments Audit

Settle the open comments on a pull request. Run the whole workflow without asking for approval, unless the user asked to approve the audit first.

1. **Find the PR.** Use the PR from the conversation, otherwise the current branch's PR. Ask only if neither is clear. Fetch its comments with `python "<skill-path>/scripts/fetch_review_context.py" [--pr URL_OR_NUMBER]`.
2. **Audit each open comment.** Check the code to decide whether the comment is correct and whether its suggestion is the right fix. A reviewer's confidence or a ready-made patch is not evidence. If the concern is real but the suggestion is poor, fix it a better way.
3. **Fix.** Make the justified fixes, run the relevant checks, commit, and push to the PR branch. Reply in each thread with what changed and the commit, then resolve it.
4. **Explain.** For comments that need no fix, reply with the reason, then resolve the thread.
5. **Leave open** only comments that need a decision you cannot make, and say in the reply what is needed.

Finish with a short list of each comment and its outcome. Never force-push or merge.
