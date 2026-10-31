---
name: pr-recap
description: Write or refresh a visual recap of a GitHub pull request for its reviewers, posted as one PR comment between pstack-recap markers. The recap opens with two sentences on why the change exists and what it changes, then one hand-drawn sketch of the changed mechanism, attached as an image, then one line on what the PR does not prove. Risk, SHAs, reading order, and file areas sit in a collapsed block below. Use after you open a PR or push to one, or when asked to "recap this PR", "visual recap", "PR recap", "diagram this PR", or "summarize this PR for reviewers". Skip trivial PRs.
---

# PR recap

Write one recap of a pull request for the people who review it. A reviewer should understand from the first screen why the change exists, what it changes, and how. The recap points into the diff. It does not replace reading the diff.

Run this workflow locally. The recap is one PR comment: GitHub Markdown plus one PNG uploaded to the PR's own host. It needs `gh`, and for the sketch, Bun and the bundled sketch tool. It posts nothing to any other host.

## Decide whether the PR gets a recap

Skip the recap when the diff has no behavior that a reviewer must trace. Examples are a version pin and its hashes, a typo or wording fix, a formatting-only change, a lockfile-only change, and the revert of one commit. A version pin skips even across a major version, because a pin has no mechanism to sketch.

For a skipped PR, post nothing on GitHub. Put one line in your reply:

`Recap skipped for PR <n>: <what the diff is>, <why it needs no recap>.`

Otherwise, write the recap. Write it again after each push that changes the diff, once the new head is published and any gate run on it has reached its outcome.

## Gather the facts

1. Resolve `<host>/<owner>/<repo>` from origin's fetch URL. Pass `-R <host>/<owner>/<repo>` to every `gh pr` call. Pass `--hostname <host>` to every `gh api` call.
2. Read the PR record with `gh pr view <n> -R <host>/<owner>/<repo> --json number,title,body,baseRefName,baseRefOid,headRefOid,files,commits,reviews,comments,closingIssuesReferences`. Record `baseRefOid` and `headRefOid`. Every fact in the recap describes the diff between those two SHAs.
3. Read the whole diff with `gh pr diff <n> -R <host>/<owner>/<repo>`. Read the code around each hunk you will describe, its callers, and each linked issue. Make no claim about a file you did not read.
4. Read the posted reviews, the posted verdict comments, and the CI runs on the head. A verdict that is not posted on the PR is not evidence.
5. Build every claim from these records. Session memory can help you find a record. It cannot prove a claim.

## Find the story before you write

Answer three questions in your notes, each from a record:

- **Why.** What went wrong, or what was needed, before this PR? Name the concrete symptom a person saw, such as a lost route, a wrong verdict, or a merge with no watcher. "Improves X" is not a why.
- **What.** The one mechanism the PR changes. If it changes several, pick the one the why depends on.
- **How.** The move that fixes it, such as a reorder, a new role, a new check, or a rewired call.

Do not invent a rationale. State a reason only when the diff, the PR body, a linked issue, a commit message, or a posted review gives it. Write any other reason as `(a guess)`.

## Write the comment

Copy the template in [the block](references/block.md). The first screen has exactly three parts:

1. **The story.** At most two sentences and 60 words. The first says why, with the concrete symptom. The second says what changed and how, in the words a reviewer will find in the diff. No semicolons, no file lists, no counts that the sketch already shows.
2. **The sketch.** One image of the changed mechanism. See [the sketch](references/sketch.md).
3. **Not covered.** One line naming what the PR does not prove, such as an unmeasured runtime, an untested path, or a caveat from the posted verdict.

Everything else goes in one collapsed `<details>` block after them: the risk line, the SHAs, the reading order, the changed areas as a short list, and links to the proof. Do not use tables.

Never copy a secret, token, or credential-looking value from the diff. Write `<redacted>` in its place.

Use the **technical-writing** skill on the recap's sentences. Then use the **unslop** skill.

## Draw the sketch

Use one writable work folder outside the skill for `scene.json`, `sketch.png`, `story.txt`, and `recap.md`. Run the render, reader, and posting commands from that folder. Replace `<skill>` with the absolute path to this skill's directory.

Follow [the sketch](references/sketch.md). In short: pick one drawing from its catalog, write `scene.json` in the work folder, render it with `bun "<skill>/scripts/sketch/sketch.mjs" scene.json sketch.png`, fix every problem it reports, then look at the PNG yourself before you use it.

When your runtime has no Bun or only an older one, render through the `npx --allow-scripts=bun bun@1.4.0` route in [the sketch](references/sketch.md#setup). Skip the sketch when that route fails too, or when your runtime cannot show you an image. Post the story, the "Not covered" line, and the details block, and say in your reply that the sketch was skipped and why. Do not substitute a Mermaid diagram or a table.

## Check every claim before you post

1. List each factual sentence in the recap and each label in the sketch.
2. Check each one against a hunk of the diff or a SHA-pinned line. Mark it verified, corrected, unsupported, or unverifiable.
3. Fix each corrected claim. Delete each unsupported or unverifiable claim, or rewrite it as a guess. Re-render the sketch if a label changed.
4. Check each link. Pin source links to the recorded head SHA. Review and CI links must point at records on the PR, with CI runs on that head. Never include a bot review's URL anywhere in the comment, code spans included. A recap does not triage a review's findings, and watch-pr and merge-gate never count a recap as acknowledging one.
5. Read `headRefOid` again. If it moved, rebuild the recap from the new diff.

Keep the marks in your notes, not in the comment. Report the counts in your reply.

## Post or update the comment

Write the recap to `recap.md` in the same work folder, including when the sketch is skipped. With a sketch, the image line is `![<alt text>](./sketch.png)`. Run every command from that folder. `attachment.mjs` is `<skill>/scripts/attachment.mjs`. Run it with `bun` or `node`. Pass the PR's host as `--host`.

The comment records its sketch on the line after the start marker: `<!-- pstack-recap:sketch sha256=<sketch hash> url=<attachment URL> -->`. The next refresh reads it back and reuses the upload when the sketch is unchanged. The comment ID is not recorded, because a comment cannot hold its own ID. Find your recap comments by the start marker and author.

Without a sketch, do step 1, skip steps 2 and 3, and write `recap.md` over `current` with `gh api --hostname <host> -X PATCH "repos/<owner>/<repo>/issues/comments/<current>" -f body="$(cat recap.md)"`. When there is none, run `gh pr comment <n> -R <host>/<owner>/<repo> --body-file recap.md`. Take `<keep>` from the comment, then go to step 4.

1. List your recap comments, oldest first. The last one is `current`. Without one, go to step 3.

```sh
me=$(gh api --hostname <host> user --jq .login)
gh api --hostname <host> --paginate "repos/<owner>/<repo>/issues/<n>/comments" \
	--jq ".[] | select(.user.login == \"$me\" and (.body | startswith(\"<!-- pstack-recap:start -->\"))) | .id"
gh api --hostname <host> "repos/<owner>/<repo>/issues/comments/<current>" --jq .body > old.md
```

2. Reuse the upload. `reuse` prints the recorded URL only when `old.md` records the hash of this `sketch.png`. Then `stamp` puts that URL and a fresh record into the new body, and the API writes it over `current`. No attach runs.

```sh
url=$(bun "<skill>/scripts/attachment.mjs" reuse --host <host> sketch.png old.md) &&
bun "<skill>/scripts/attachment.mjs" stamp --host <host> sketch.png recap.md "$url" > body.md &&
gh api --hostname <host> -X PATCH "repos/<owner>/<repo>/issues/comments/<current>" -f body="$(cat body.md)"
```

Keep `<current>` as `<keep>` and go to step 4. When `reuse` exits 1, the sketch changed or the comment has no record, so upload.

3. Upload the sketch. Try the CLI once:

```sh
gh pr comment <n> -R <host>/<owner>/<repo> --body-file recap.md --attach sketch.png
```

It prints the new comment's URL. Its `#issuecomment-<id>` is `<keep>`. Read that comment's body into `new.md` with `gh api --hostname <host> "repos/<owner>/<repo>/issues/comments/<keep>" --jq .body > new.md`, run `stamp --host <host> sketch.png new.md > body.md`, and PATCH `<keep>` with `body.md`. Go to step 4.

When `gh` refuses the upload, or has no `--attach`, the CLI cannot upload to this host. Classify it once as a CLI limitation. GHES can reject the upload. It does not show that the repository disallows attachments. Do not retry the route.

- **The user authorized a manual upload.** Give the user the absolute path of `sketch.png`. Ask them to drag it into a comment box on the PR in the web UI, without submitting, and paste back the URL or the `![...](...)` or `<img>` markup that appears. Write the paste to `paste.txt` and run this block:

  ```sh
  url=$(bun "<skill>/scripts/attachment.mjs" url --host <host> paste.txt) &&
  bun "<skill>/scripts/attachment.mjs" stamp --host <host> sketch.png recap.md "$url" > body.md
  ```

  `url` accepts the markup forms and prints the bare URL, or exits 1 for any other host or path. The block's exit 1 can come from either command, so read the error. `no https://<host>/user-attachments/assets/<uuid> URL found` comes from `url` and means the paste is not an attachment on this host. Treat it as upload unavailable, do not guess the URL, and take the no-authorization path. `no <host> attachment image in the body; pass the attachment URL to replace ./sketch.png` or `the body must start with <!-- pstack-recap:start -->` comes from `stamp` and means `recap.md` has an authoring error. Fix `recap.md` and rerun the block. When the block exits 0, PATCH `current` with `body.md` (`<keep>` is `current`), or when there is none, POST it with `gh api --hostname <host> -X POST "repos/<owner>/<repo>/issues/<n>/comments" -f body="$(cat body.md)"` and take `<keep>` from the returned `id`.
- **No authorization.** Remove the image line from `recap.md`. Write that body over `current`, or post it when there is none, and take `<keep>`. Report `upload unavailable: <the gh error>`.

4. Delete every other recap of yours, so the PR keeps one.

```sh
me=$(gh api --hostname <host> user --jq .login)
gh api --hostname <host> --paginate "repos/<owner>/<repo>/issues/<n>/comments" \
	--jq ".[] | select(.user.login == \"$me\" and (.body | startswith(\"<!-- pstack-recap:start -->\")) and .id != <keep>) | .id" |
	while read -r id; do gh api --hostname <host> -X DELETE "repos/<owner>/<repo>/issues/comments/$id"; done
```

5. Check the saved comment, count your recaps, then check that the image renders. Report the upload, the saved comment, and the render as three separate outcomes.

```sh
me=$(gh api --hostname <host> user --jq .login)
gh api --hostname <host> --paginate "repos/<owner>/<repo>/issues/<n>/comments" \
	--jq ".[] | select(.user.login == \"$me\" and (.body | startswith(\"<!-- pstack-recap:start -->\"))) | .id" | grep -c .
gh api --hostname <host> "repos/<owner>/<repo>/issues/comments/<keep>" --jq .body > saved.md
bun "<skill>/scripts/attachment.mjs" check --host <host> --head <head SHA, 8 characters> saved.md
curl -s -o /dev/null -w '%{http_code} %{content_type}' -L -H "Authorization: Bearer $(gh auth token --hostname <host>)" "<url that check printed>"
```

`check` confirms the start marker, the end marker, the head SHA, and an image on this host in either form. When a record is present, it checks that the recorded URL is an image URL in the body. It does not require a record or verify its hash. Read its error to identify which check failed. The count must print `1`. Any other number means step 4 failed, so run it again. The fetch must print `200 image/png`. A 404 means the asset is unavailable to this request. When a reused URL fails the fetch, treat the record as dead and upload again from step 3. A signed-out fetch can fail on a working upload, so it proves nothing. Without a sketch, run `check` with `--no-image`, which checks the markers and the head SHA only, and skip the fetch.

The editor's `<img width=... alt=... src="...">` markup passes `url` and `check`. Author the recap with the Markdown image form and the alt text from [the block](references/block.md). `stamp` preserves the image form in the body it reads. Hosting the image in the repository or as a release asset is not part of this skill.

Post it as a PR comment, never in the PR body. In a repository gated by no-mistakes, the gate owns the PR body.

## Reply

- The comment URL and the head SHA that the recap describes, or the skip line.
- Which catalog drawing you used, or why you skipped the sketch.
- The claim check counts: verified, corrected, and deleted or rewritten as guesses.

[CREDITS.md](CREDITS.md) names the sources this skill adapts.
