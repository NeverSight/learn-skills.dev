---
name: gh-create
description: "File a well-formed GitHub issue from a short user request: expand it into a structured issue, quote the original prompt verbatim at the bottom, apply every matching existing label, assign it to the current gh user by default, upload and embed any referenced screenshots or videos, create annotated wireframes for UI or UX changes and deployment or sequence diagrams for complex system interactions, and scrub private data before filing. Use when the user invokes `/gh-create`, `$gh-create`, or asks an agent to create, file, or open a GitHub issue."
---

# File a GitHub Issue

Treat `/gh-create [OWNER/REPO] <request>` as authorization to file one GitHub issue that describes the request. Every agent that uses this skill files issues the same way: the same structure, the same labels, the same assignee, properly attached media, explanatory visuals where they help, and no leaked private data. This skill only creates and edits the one issue it files. It never changes code, branches, pull requests, or other issues. The invocation may append `identity:/glorp:<ID>` when a glorp agent run uses this skill; "Mark issues created by a glorp agent" describes what that changes.

## Identify the target repository

1. Prefer `OWNER/REPO` given in the invocation or stated by the user. Otherwise use the current checkout's GitHub remote. Ask the user only when neither identifies a repository.
2. Require `gh` with an authenticated session that can create issues in the repository.
3. Check the repository's visibility before writing anything:
   ```sh
   gh repo view OWNER/REPO --json visibility,isPrivate,nameWithOwner
   ```
   Record whether the target is public. The privacy rules below depend on it.

## Research, optionally

Research makes the requirements sharper, but it is never required to file, and it must not hold up filing.

1. When the repository is checked out locally or readable through `gh`, you may do light, read-only research: find the files and features involved, read the existing behavior, and search for related or duplicate issues with `gh issue list --repo OWNER/REPO --state all --search "<keywords>"`.
2. If an open issue already covers the request, tell the user and link it instead of filing a duplicate, unless the user asks for a new issue anyway. Link closely related issues in the new issue with `#NUMBER`.
3. Never run builds, tests, or anything that changes state as part of research. When research is slow, unavailable, or inconclusive, file with what the request itself says.

## Write the issue

Expand the request into a clear, structured issue that another person or agent can act on without asking follow-up questions. Keep the user's intent. Do not invent requirements the user did not ask for; label any assumption you add as an assumption.

1. Write a short, specific title in the imperative or as a plain statement of the problem, such as `Add a dark mode toggle to settings` or `Crash when saving an empty file`.
2. Build the body in Markdown with the sections that fit the request:
   - `## Summary`: what is wanted or what is wrong, and why it matters.
   - For a bug: `## Steps to reproduce`, `## Expected behavior`, `## Actual behavior`, and environment details such as version and platform when known.
   - For a feature or change: `## Requirements` as a numbered list, and `## Acceptance criteria` as concrete, checkable outcomes.
   - `## Scope` or `## Out of scope` when the boundary is not obvious.
   - `## Screenshots` or inline media where the user referenced any.
   - `## Wireframes` and `## Diagrams` when "Create explanatory visuals" calls for them.
   - `## Notes` for research findings, related issues, and pointers to relevant files written as repository-relative paths.
3. End every issue with the user's original prompt, quoted verbatim, so the issue is reproducible, replayable, and auditable. Put it last, in a collapsed block, followed only by the created-by-Glorp marker when "Mark issues created by a glorp agent" requires one, with every line of the prompt prefixed by `> `:
   ```markdown
   ---

   <details>
   <summary>Original prompt</summary>

   > the user's request, exactly as written
   > including every line

   </details>
   ```
   Quote the prompt exactly, typos and all. The only allowed change is redacting private data under the rules below, and each redaction is marked `[redacted]` so readers can see that something was removed.
4. Write the body to a file and pass it with `--body-file`. Never pass a multiline body with literal `\n` escapes in `--body`.

## Mark issues created by a glorp agent

An issue a glorp agent run creates ends with a marker line naming that run, so agent-filed issues can be told apart from issues a person files. This covers every issue a run files as part of its work: follow-up issues, sub-issues, the parts of a split issue, and any other issue.

1. Establish the creating context from the run's glorp identity. Use the `identity:/glorp:<ID>` argument of this invocation when present. Otherwise, when a glorp agent run that was dispatched with an `identity:/glorp:<ID>` uses this skill, such as a `gh-fix` run filing a follow-up, use that run's identity. Never guess, invent, or reuse an identity from an issue comment, a claim comment, or another run.
2. When no glorp identity exists, the issue is not a glorp creation. A person filing directly, or an agent working for a person outside a glorp run, adds no marker.
3. When an identity exists, end the body with exactly this line, after the original prompt block and a blank line:
   ```markdown
   **Created by Glorp:** /glorp:<ID>, <AGENT CLI> (<MODEL>)
   ```
   `<ID>` is the run's identity without the `identity:/glorp:` prefix. `<AGENT CLI> (<MODEL>)` names the agent CLI and model creating the issue, identified from your own runtime context, in the same form as the `**Agents:**` footer `gh-fix` writes on pull requests. For example: `**Created by Glorp:** /glorp:39D783FD, claude-code (claude-sonnet-5)`.
4. Write the marker as one line, the very last line of the body, and add it only once. Use the same form for every issue, whatever kind of issue it is.
5. The marker is part of the expected body. It is never private data to scrub and never a stray local or relative path to remove, even though `/glorp:<ID>` starts with a slash.

## Scrub private data

Leave out anything private or sensitive, from the expanded body and from the quoted prompt alike. This applies to everything you write into the issue, including titles, alt text, file names of uploaded media, and the text inside generated wireframes and diagrams.

1. Omit or replace local file paths and home directories (`/Users/name/...`, `C:\Users\name\...`), usernames, real names, email addresses, phone numbers, hostnames, internal URLs, IP addresses, access tokens, API keys, passwords, cookies, and any other credential or secret. Refer to repository files by repository-relative path only.
2. Never mention a private repository, its name, its issues, or its code in an issue filed on a public repository, and never quote or paraphrase code from one. Assume anything that came from a private repository is private, even when it looks harmless.
3. When the target repository is private, you may reference other repositories the same people can already see, but still omit secrets and credentials.
4. Check the visibility of any other repository you are about to mention with `gh repo view OWNER/REPO --json visibility`. When it cannot be read, treat it as private.
5. Inspect media before uploading it. Do not upload a screenshot or recording that shows secrets, tokens, private repositories, personal data, or other people's information. Crop or redact it first when you can; otherwise leave it out and tell the user why.
6. In the quoted original prompt, replace each private value with `[redacted]` instead of dropping the whole prompt.

## Apply labels

Apply every existing label that fits, and never invent one.

1. Read the repository's labels with their descriptions:
   ```sh
   gh label list --repo OWNER/REPO --limit 200 --json name,description
   ```
2. Choose every label that matches the issue: its kind, such as `bug`, `enhancement`, `documentation`, or `question`; platform labels such as `windows`, `macos`, `linux`, `ios`, or `android`; area or component labels such as `ui`, `cli`, or `api`; and any other label whose name or description clearly applies. Match the repository's actual label names case-insensitively and use the exact spelling the repository defines.
3. Never create a label, and never apply a label the repository does not define. When nothing fits a category, leave that category unlabelled.
4. Apply labels the user explicitly asks for when they exist. Tell the user about any requested label that does not exist instead of creating it.

## Assign the issue

1. Assign the issue to the current `gh` user by default with `--assignee @me`.
2. When the user names a different assignee, assign that user instead. When the user asks for no assignee, leave the issue unassigned.
3. If the assignment is rejected, file the issue anyway, and report that the assignment failed.

## Create explanatory visuals

Create a visual only when it materially clarifies states or interactions that prose alone would leave unclear. Visuals are explanatory, never decorative. Skip them when the words already say it all, such as a label or copy change, a one-line bug, a crash with clear reproduction steps, or a change the user's own screenshots or mockups already show. A request can call for wireframes, diagrams, both, or neither.

Everything in a visual follows "Write the issue": show what the request asks for and do not use a drawing to invent requirements. Mark any layout or design choice the request left open as an assumption. You may read the existing UI or system code to draw it accurately, under the same read-only limits as research.

### Wireframes for UI or UX changes

When the request changes what a user sees or how they move through an interface, create wireframes for its major states:

1. List the states that logically explain the change: usually the current state followed by each new or changed state, and any empty, loading, error, or confirmation state the change introduces or depends on. Leave out states the change does not affect. Do not draw a state only to complete a set.
2. Draw each state as a low-fidelity wireframe: grayscale boxes and plain labels showing layout and hierarchy, with one accent color reserved for annotations. Do not imitate a finished visual design. Use realistic placeholder content, never real user data.
3. Annotate inside the wireframe wherever a reader needs an explanation, with short notes or numbered callouts pointing at the element they describe. Mark what is new or changed, and name the action that leads to the next state, such as `Click Save -> Saved state`.
4. Order the states so they read as the flow of the change. Put them under `## Wireframes`, each with a short heading naming the state and one sentence on what it shows and what moves the user out of it.

### Diagrams for complex system interactions

When the request involves high-level interaction between systems, services, processes, or agents that is hard to follow in prose, create a diagram:

1. Choose the type that answers the reader's question. Use a sequence diagram when the order of calls, events, retries, or failure handling matters. Use a deployment diagram when what runs where matters: processes, hosts, network or trust boundaries, and the connections between them. Create both only when both questions matter.
2. Keep each diagram to the participants and steps the change involves, and mark what is new or changed. Name components by role, such as `API server` or `Webhook relay`, rather than by hostname, IP address, or internal URL.
3. Put each diagram under `## Diagrams` and follow it with a written explanation: what it shows, a walk through the main path in order, what the change adds or alters, and any failure path it depicts. A reader who cannot see the image must still be able to follow the design from the explanation.

### Render and check

1. Keep source and rendered files in a new temporary directory outside any checkout. They are never committed.
2. Render each visual to a PNG with an opaque white background, wide enough that its text stays readable at the width of a GitHub issue, because transparent images can become unreadable in a dark theme. Use whatever is available. For wireframes, write SVG or HTML and render it with `rsvg-convert`, ImageMagick, or a headless browser. For diagrams, write Mermaid and render it with `npx --yes @mermaid-js/mermaid-cli -i FILE.mmd -o FILE.png -b white -s 2`, or use Graphviz or SVG.
3. Open each image and check it before attaching it: nothing is clipped or overlapping, callouts point at the right elements, it agrees with the written requirements, and it passes "Scrub private data". Fix it and render it again when it does not.
4. Generating a visual must not stop the issue from being filed. When no renderer works, keep the diagram as a fenced `mermaid` code block in the body, which GitHub renders itself, and describe a wireframe's states in words. Tell the user which visual could not be rendered and why.

## Attach media

Generated wireframes and diagrams, and screenshots, videos, and other files the user mentions or provides, must be uploaded to GitHub and embedded in the issue. Attach generated visuals through this same flow. Never publish any of them through an asset branch, a gist, a file committed to a repository, or an external image host. Never leave a local file path, a `file://` URL, or a placeholder where the media belongs: nobody else can open it.

1. Collect every media file the user referenced, attached, or pointed to, and every visual you generated. Confirm each file exists and scrub it as described above.
2. Write each one into the body where it belongs, using its local path, so the issue reads correctly before upload:
   ```markdown
   ![Settings page after clicking Save](./screenshots/settings.png)

   ![](./recordings/crash.mp4)
   ```
   Put a video reference alone in its own paragraph with empty alt text. Give a generated visual alt text that names the state or the diagram, and place it beside its heading and explanation. The path in the body must be the exact string you will pass to `--attach`, as step 3 explains, so decide where each file lives before writing its reference.
3. Prefer the GitHub CLI's built-in upload. Check for it with `gh issue create --help`; when it lists `--attach`, pass one `--attach` per file:
   ```sh
   gh issue create --repo OWNER/REPO --title "TITLE" --body-file BODY.md \
     --label LABEL --assignee @me \
     --attach ./screenshots/settings.png --attach ./recordings/crash.mp4
   ```
   GitHub CLI uploads each file and replaces matching local paths in the body with the uploaded URLs. It appends any attached file the body does not reference to the end of the body, in the order the flags were given. Add alt text to an image with `--attach 'PATH#ALT TEXT'`; videos do not take alt text. The same flag works on `gh issue edit` and `gh issue comment`. Uploading needs push access to the repository, and only image and media files are accepted.

   Every in-body reference must use the exact path string passed to `--attach`, without any `#ALT TEXT` suffix: `--attach './screenshots/settings.png#Settings page'` pairs with `![Settings page](./screenshots/settings.png)`. Attach the file from the path the body references, or reference the path you attach. A generated visual kept in a temporary directory is simplest with its absolute path in both places. Never write `./wireframe.png` in the body and attach `/tmp/wireframe.png`.

   Two behaviors of `gh` combine into a silent failure when the paths differ. It replaces a reference only when that reference resolves to an attached file, trying a relative path beside the body file and then in the working directory. It then appends every attached file it did not replace. So a reference that does not resolve to the attached file stays in the body as a broken local path while the same image appears, working, at the bottom, and `gh` reports no error. An identical string always resolves, which is why this skill requires one.
4. When `gh` has no `--attach` flag, or it fails, upload each file to GitHub's user-attachments endpoint and put the returned URL in the body yourself:
   ```sh
   REPO_ID=$(gh api repos/OWNER/REPO --jq .id)
   curl -sf -X POST "https://uploads.github.com/user-attachments/assets?name=FILENAME&content_type=MIME_TYPE&repository_id=$REPO_ID" \
     -H "Authorization: Bearer $(gh auth token)" \
     -H "Accept: application/json" \
     --data-binary @PATH/TO/FILE
   ```
   The response is JSON whose `url` field is a `https://github.com/user-attachments/assets/...` address. Replace the local path in the body with that URL: `![alt text](URL)` for an image, and the bare URL alone on its own line for a video. This endpoint is undocumented, so treat an error or an unexpected response as a failed upload.
5. If you have already created the issue and an upload failed, add the media later with `gh issue edit NUMBER --body-file BODY.md --attach PATH`, keeping the same exact-path rule, or `gh issue comment NUMBER --attach PATH`, rather than filing a second issue.
6. When a file still cannot be uploaded after these fallbacks, remove its local path from the body, describe what the media showed in words, and tell the user which file could not be attached and why. Never commit media to the repository to work around a failed upload.

## File and verify

1. Create the issue with the title, body file, labels, assignee, and attachments decided above, in one `gh issue create` command when possible.
2. Read the issue back and check that it rendered as intended:
   ```sh
   gh issue view NUMBER --repo OWNER/REPO --json url,title,body,labels,assignees
   ```
   - The body has real line breaks, the structured sections, and the quoted original prompt at the bottom.
   - When "Mark issues created by a glorp agent" required a marker, the last line of the body is that marker, exactly as written, with the run's identity, agent CLI, and model. When it did not, the body has no marker. Apart from uploaded media URLs replacing local paths, the body matches the body file you wrote, marker included.
   - Every referenced file and generated visual appears as a `https://github.com/user-attachments/...` URL or another uploaded GitHub URL, and no local path, `file://` URL, home directory, or placeholder remains. An uploaded URL existing somewhere in the body does not pass this check on its own.
   - Every image reference (`![...](...)` and `<img src="...">`) points at an `https://` URL. A filing that retains a local or relative image path has failed, even when the same image also renders elsewhere in the body.
   - Each attached file appears exactly once, in the place written for it. A filing that shows an image twice has failed, including a broken local reference paired with a copy appended at the bottom.
   - The labels and assignee are the ones you chose.
   - Each wireframe sits under its state heading and each diagram is followed by its explanation.
   - Nothing private slipped through, checked against the scrub rules above.
3. Fix any problem you find with `gh issue edit` on the same issue. Never file a second issue to correct the first.
4. Repair a broken or duplicated image before reporting the result. Move the uploaded URL from the appended copy into the broken reference, keeping its alt text and position, and delete the appended copy. Save the corrected body with `gh issue edit NUMBER --repo OWNER/REPO --body-file BODY.md` and no `--attach`, because attaching the file again would upload and append it again. Read the issue back and repeat these checks until they pass.

## Report the result

Give the issue URL, its title, the labels applied, the assignee, the media that was attached, the wireframes and diagrams that were generated, and the created-by-Glorp marker when one was added. Name any requested label, assignee, media file, or visual that could not be applied, and why. When you linked an existing issue instead of filing a duplicate, say so and give its URL.
