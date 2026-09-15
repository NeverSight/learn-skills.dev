---
name: telephone
description: Run the Telephone Website lesson. The user holds a paper worksheet written by someone else; interview them about it with the grilling skill, build the site described, and publish it to GitHub Pages. Use when the user types $telephone or says they are doing the telephone website lesson.
---

# The Telephone Website

The user is the **Receiver**. Another person, the **Author**, drew a website on a paper worksheet and handed it over. The Author is not available. The Receiver reads the paper and types answers. You build what the paper says and publish it. Drift between paper and site is expected: it is the lesson, so log it instead of hiding it.

Rules that hold for the whole session:

- Never tell the Receiver to go ask the Author.
- When the Receiver prefixes an answer with `guess:` it was not on the paper. Record it in `GUESSES.md`. If an answer looks invented and lacks the prefix, ask once: "Is that on the paper, or a guess?"
- Plain HTML and CSS, a little JavaScript only if the paper demands it. No frameworks, no build step, no packages.
- Do not add pages, features, or copy the paper did not ask for. Missing content is filled with short placeholder text that says what would go there.
- Do not stop for approval between phases except where a phase says so.

## Phase 0: Check the room

Run these and fix what fails before anything else:

```
gh auth status
git config --global user.name
ls ~/.agents/skills/grilling/SKILL.md
```

If `gh` is not signed in, tell the Receiver to re-run the setup wizard from https://ai.reidsurmeier.wtf/telephone/ and stop.

Ask for the site's name as written on the paper. Derive a folder and repo name from it: lowercase, hyphens, letters and digits only. Create the folder inside the current directory and `cd` into it. Everything below happens there.

## Phase 1: Grill

Read `~/.agents/skills/grilling/SKILL.md` and run that interview about the website on the paper. The Receiver answers from the paper. Open with this exact framing so the Receiver knows the rules:

> I will ask about the site in rounds. Answer from the paper. If the paper does not say, answer anyway and start with `guess:`.

The worksheet has these boxes, so the first round covers them: site name, who it is for, one-sentence pitch, three colors, font mood, list of pages, homepage wireframe, one inner page wireframe, one thing that must be on it, one thing that must never be on it. Later rounds settle what the wireframes do not: navigation, what each page contains, what the homepage says first, what "done" looks like on a phone.

Stop when the frontier is empty. Then write two files:

- `BRIEF.md`: every settled decision, one line each, grouped by page.
- `GUESSES.md`: every `guess:` answer, verbatim, with the question it answered.

Show both files to the Receiver and ask one question: "Anything on the paper I missed?" Fold the answer in.

## Phase 2: Build

Build the site from `BRIEF.md` only:

- `index.html` at the repo root, one HTML file per page listed in the brief, one `style.css`.
- Colors and font mood from the brief. If the paper gave colors by name, use the plain CSS color of that name.
- Layout follows the wireframes as drawn. If a wireframe is ambiguous, pick the simplest reading, note it in `GUESSES.md` under "Builder's guesses".
- Works at phone width. No horizontal scrolling.
- The "must never be on it" item is absent. Check it before moving on.

Open the result in the browser (`open index.html` on macOS, `Start-Process index.html` on Windows) and ask the Receiver to look. Fix what they say is wrong relative to the paper. Do not accept new ideas from the Receiver: those go in `GUESSES.md` as "Receiver's additions" and are built only if the Receiver insists.

## Phase 3: Publish

```
git init -b main
git add -A
git commit -m "Telephone website: <site name>"
gh repo create <repo-name> --public --source=. --push
gh api -X POST repos/<owner>/<repo-name>/pages -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"
```

`<owner>` is `gh api user --jq .login`. Then poll `gh api repos/<owner>/<repo-name>/pages --jq .html_url` and fetch that URL until it returns 200. The first build takes about a minute. Print the final URL on its own line.

## Phase 4: Hand back

Print, in this order: the live URL, the repo URL, the count of guesses, then the contents of `GUESSES.md`. Tell the Receiver to keep the paper and the URL together for the presentation. Stop.
