---
name: ds-pr-comments
description: "Formats and posts GitHub comments written by an agent on the user's behalf, with clear attribution and no leaked secrets. Use whenever you post a PR comment, review reply or dismissal reason, or on /ds-pr-comments."
---

Make every agent-written comment easy to spot, short and safe to publish.

## Steps

1. Write the reply. Lead with the conclusion. Cite the code line, check, test or reproduction that supports it. Mark what you verified and what is your opinion.
2. Put this note at the top, with the reply below it:

   ```md
   > [!NOTE]
   > **<model> responding on behalf of <user>**

   Reply text starts here.
   ```

   Use the model name the harness reports. If it reports none, use the harness name. Use the user's name or GitHub login.
3. Scan the full comment, including quotes and attachments, for secrets, tokens, private paths and personal data. Remove them.
4. Preview the final Markdown. Confirm the note and the reply render as two separate blocks.
5. Post the comment.
6. Confirm GitHub returned the comment or review URL. Print it.
7. Resolve a review thread only after its reply posted.

## Stop when

- GitHub returned a URL for each comment you meant to post.
- A post fails twice. Report the error and do not resolve the thread.

## Rules

- Use the note on top-level comments, inline review comments, replies to bots and people, and dismissal reasons.
- Do not use it in PR descriptions, commit messages or text the user asked to post word for word.
- One attribution only. No signature, footer, heading or horizontal rule.
- No thanks, filler or status updates such as "still working on it".
- Never guess the model name.
