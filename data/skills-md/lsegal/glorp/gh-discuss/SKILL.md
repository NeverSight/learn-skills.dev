---
name: gh-discuss
description: "Answer a numbered GitHub Discussion thread, read-only: read the thread and the repository to form an answer, then either post a single top-level reply or stop without commenting. Never executes code, never commits, never runs mutative git or gh commands, and never reads outside the repository. Use when the user invokes `/gh-discuss NUMBER`, `$gh-discuss NUMBER`, or asks to answer a GitHub Discussions thread."
---

# Answer a GitHub Discussion Thread

Treat `/gh-discuss NUMBER` as authorization to read a single top-level GitHub Discussion thread and, only if you can answer it accurately and positively, post one reply. This skill is strictly read-only against the repository and the wider system: it never writes code, never commits, never opens branches or pull requests, and never runs any command that mutates a repository, issue, discussion, label, or file. Its only permitted write is posting a reply comment on the discussion, and only when that reply is warranted.

## Validate the request

1. Require exactly one positive integer discussion number; accept an optional leading `#`.
2. Identify the GitHub repository from an explicit `Repository: OWNER/REPO` line in the invocation, or from the current checkout's GitHub remote.
3. Require `gh` with an authenticated session that can read the repository and read/write Discussions.
4. Fetch the discussion with its top-level body, author, category, and existing comments, for example:
   ```sh
   gh api graphql -f query='query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){discussion(number:$number){id title body author{login} answerChosenAt comments(first:100){totalCount nodes{id}}}}}' -F owner=OWNER -F name=NAME -F number=NUMBER
   ```
5. Stop without commenting, and without further action, if any of the following hold:
   - The discussion does not exist or cannot be read.
   - `comments.totalCount` is already greater than zero, or `answerChosenAt` is set. Another reply already exists or the thread is already answered; do not add a second one.
   - The discussion body is not an answerable question or request (for example, an announcement, poll, or open-ended chat with nothing to resolve).

## Read only the top-level thread

Only the discussion's own title and body are in scope for forming an answer. Do not fetch, read, or act on nested replies to other comments even if the query above happens to return them, and do not respond to sub-comments — only ever produce a single top-level reply to the discussion itself.

## Research the answer, read-only

1. Use only read operations to investigate: reading files in the current checkout of the repository (clone or fetch a fresh read-only copy if none exists locally; never modify it), `gh` read commands (`gh issue view`, `gh pr view`, `gh api` GET-style queries), and repository documentation.
2. Never execute application code, build scripts, tests, or any command whose purpose is to change state rather than to read it. Never run `git commit`, `git push`, `git branch`, package installs, or any other mutating command.
3. Never read outside the repository: do not fetch arbitrary external URLs, other repositories, or unrelated local files. If the discussion cannot be answered from the repository's own content and history, that is a reason to stop, not a reason to look elsewhere.
4. Form an answer only when the repository's content supports it with reasonable confidence. Do not speculate, and do not answer partially if the confident part does not resolve the asker's actual question.

## Reply or stop

1. If you cannot produce an answer that is both accurate and positively resolves the question, stop here and take no further action. Do not post a comment saying you don't know, and do not leave any other trace.
2. If you can, write a concise, accurate, on-topic reply grounded in what you read from the repository. Do not include large code dumps; reference file paths and summarize instead.
3. Post the reply as a single top-level comment on the discussion, not a reply to any existing comment:
   ```sh
   gh api graphql -f query='mutation($discussionId:ID!,$body:String!){addDiscussionComment(input:{discussionId:$discussionId,body:$body}){comment{id}}}' -F discussionId=DISCUSSION_ID -F body="..."
   ```
4. After posting, stop. Do not mark the discussion answered, change its category, or take any other action.

## Report the result

State plainly whether a reply was posted or the thread was left untouched, and why. If a reply was posted, include the discussion URL and a short summary of the answer.
