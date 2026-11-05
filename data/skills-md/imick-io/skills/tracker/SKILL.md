---
name: tracker
description: Build and open the issue tracker page, a snapshot of the repo's GitHub issues showing what you act on next, the epics' roadmap and each epic's board and blocking graph. Use when the user wants to see the tracker, what's waiting on them, or where the epics stand.
---

# Tracker

[build.mjs](./build.mjs) pulls every issue of the current repo with `gh` and writes `tracker/index.html`, one self-contained page with four tabs:

- **Action items**: everything waiting on a person (`ready-for-human`, `ready-for-review`, epics to brief, specs to approve, finished epics whose PR waits for a merge), with each issue's acceptance-criteria checklist and how many open issues it holds up, directly or down the chain.
- **Specs**: each spec, whether it's approved, and the decisions it lists.
- **Roadmap** (the page it opens on): the epics in dependency order with their status, progress and tickets, and a progress table. Done epics fold to one line. Arrows link an epic to the epics waiting on it: solid while it holds them back, dashed once done; hovering an epic shows only its links. An **Outside epics** card at the bottom of the first column lists the tickets in no epic (standalone bugs and changes from triage, each shipped as its own PR), with the backlog last; the Epic board has the same entry.

One colour key runs through the page, and red always means you. A ticket on your turn or for your review is solid red with a "You" tag. An epic is outlined in red when anything in it waits on you, and its status is red when the epic itself does (a brief, a spec to approve, a PR to merge). Green is an agent on it, blue the agents' queue, amber not triaged yet, grey waiting on something else, and faded done.
- **Epic board**: one epic's tickets by status, and a diagram of what blocks what.

It reads the conventions set up by `/setup-imick-skills` and used by `/scope-decomposer`, `/wayfinder` and `/triage`: the triage labels, `epic` and `spec` labels, one milestone per epic, and GitHub's native issue dependencies for blocking. GitHub only.

## Steps

1. **Install it in the repo** if `tracker/build.mjs` doesn't exist yet: copy [build.mjs](./build.mjs) to `tracker/build.mjs`, and add `tracker/index.html` and `tracker/.vercel` to `.gitignore`. The script lives in the repo so the agent loop and anyone without these skills can rebuild the page.
2. **Build and open**: `node tracker/build.mjs` from the repo root. It needs `gh` logged in with read access to the repo's issues. Use `--no-open` to only write the file.
3. Tell the user how many issues it read (the script prints it) and give the page's path.

The agent loop rebuilds the page before and after every pass when `tracker/build.mjs` exists, so a tab left open follows the loop after a reload.

When this skill's `build.mjs` is newer than the repo's copy, offer to copy it over.

## Hosting on Vercel

The page can also be served from Vercel, built from GitHub on every visit behind a password, so it's current even when the loop is off and nobody has to build it. Set it up when the user asks for a hosted tracker (or `/setup-imick-skills` chose **Vercel**):

1. **Copy** the [vercel/](./vercel/) folder's contents into `tracker/`: `api/index.mjs`, `vercel.json` and `.vercelignore`. The `.vercelignore` keeps the locally built `tracker/index.html` out of the upload: Vercel serves files before rewrites, so without it that snapshot would be public at `/`. The repo's root `.gitignore` doesn't apply, since the project's root is `tracker/`.
2. **Create the project** from `tracker/`: `vercel link --yes --project <repo>-tracker`. Confirm the Vercel scope (personal account or team) with the user first: it is the CLI's default otherwise.
3. **Set the repo**: `vercel env add TRACKER_REPO production` with `<owner>/<repo>`. A project connected to the Git repo gets it from Vercel's git variables instead.
4. **Secrets**: the user adds them themselves, never ask for or handle the values. Each `vercel env add <NAME> production` from `tracker/` prompts for one:
   - `GITHUB_TOKEN`: a fine-grained token for this repo with **Issues: read**, **Pull requests: read** and **Metadata: read**.
   - `TRACKER_USER` and `TRACKER_PASSWORD`: the basic-auth login for the page.
5. **Deploy**: `vercel deploy --prod` from `tracker/`, again after the secrets are added. Then check that `/` and `/index.html` answer **401** without the login, and the page loads with it.

The function sends no CDN cache headers, so every visit passes the password check; a warm instance reuses its last page for a minute, and `?refresh` rebuilds it. Without `TRACKER_USER` and `TRACKER_PASSWORD` it answers 401 to everyone. Code changes to the tracker reach Vercel with the next `vercel deploy --prod`; issue changes need none.
