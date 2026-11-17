---
name: run
description: Run a Shift against this repository via the Shift API
arguments: <sku>
---

# Shift Run

Run a Shift against this repository via the Shift API. The Shift code is: $ARGUMENTS

## Shift Codes

| Code | Shift |
|------|-------|
| `CI` | CI Generator |
| `TD` | Double Converter |
| `FL` | Fast Laravel |
| `HC` | HTML Converter |
| `10` | Laravel 10.x |
| `11` | Laravel 11.x |
| `12` | Laravel 12.x |
| `13` | Laravel 13.x |
| `50` | Laravel 5.0 |
| `51` | Laravel 5.1 |
| `52` | Laravel 5.2 |
| `53` | Laravel 5.3 |
| `54` | Laravel 5.4 |
| `55` | Laravel 5.5 |
| `56` | Laravel 5.6 |
| `57` | Laravel 5.7 |
| `58` | Laravel 5.8 |
| `60` | Laravel 6.x |
| `70` | Laravel 7.x |
| `80` | Laravel 8.x |
| `90` | Laravel 9.x |
| `CR` | Laravel Cloud Pre-Check |
| `LF` | Laravel Fixer |
| `LL` | Laravel Linter |
| `LP` | Laravel PreShift |
| `LS` | Laravel Slimmer |
| `L3` | Livewire 3.x |
| `L4` | Livewire 4.x |
| `LTL` | Lumen to Laravel |
| `MC` | MFC Converter |
| `MM` | MySQLi Shift |
| `NC` | Namespace Consolidator |
| `NM` | Namespace Models |
| `PP` | Pest Converter |
| `PU10` | PHPUnit 10 |
| `PU11` | PHPUnit 11 |
| `PU12` | PHPUnit 12 |
| `PU13` | PHPUnit 13 |
| `PU6` | PHPUnit 6 |
| `PU8` | PHPUnit 8 |
| `PU9` | PHPUnit 9 |
| `P4` | PSR-4 Shift |
| `T1` | Tailwind 1.x |
| `T2` | Tailwind 2.x |
| `T3` | Tailwind 3.x |
| ~~`T4`~~ | **Not a real Shift.** Tailwind 4.x has no Shift — laravelshift.com redirects to Tailwind's own upgrade tool. Never run this; point the user to https://tailwindcss.com/docs/upgrade-guide#using-the-upgrade-tool instead. |
| `TU` | Tailwind UI |
| `TG` | Tests Generator |
| `VC` | Vite Converter |

## Steps

1. If no Shift code was provided in `$ARGUMENTS`, ask the user which Shift they'd like to run. Show the code table above as a reference and suggest running `/shift:analyze` first if they're unsure which Shift applies to their project.

   If `$ARGUMENTS` is `T4` (or otherwise requests a "Tailwind 4" Shift), do not call the API. There is no Tailwind 4.x Shift — tell the user to use Tailwind's own upgrade tool instead: https://tailwindcss.com/docs/upgrade-guide#using-the-upgrade-tool

2. Check if `SHIFT_API_TOKEN` is set in the environment. If it's missing, let the user know they may generate an API token at: https://laravelshift.com/account/api-token, then ask them to provide it. Once provided, ask whether they'd like to save it to `~/.claude/settings.json` (recommended — available across all projects) or `.claude/settings.local.json` (this project only). Save it under the `env` key of whichever file they choose:
   ```json
   {
     "env": {
       "SHIFT_API_TOKEN": "their_token"
     }
   }
   ```
   If the target file already exists, merge the key into the existing `env` object rather than overwriting the file.

3. Determine the remote and current branch by running:
   ```bash
   git remote get-url origin
   git branch --show-current
   git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
   ```
   Parse the remote URL to extract `owner/repo` — handle both SSH (`git@github.com:owner/repo.git`) and HTTPS (`https://github.com/owner/repo.git`) formats. Strip any trailing `.git`. Also detect the git platform (GitHub or GitLab) from the remote URL hostname, and construct the HTTPS repo URL (e.g. `https://github.com/owner/repo`).

   The third command returns the remote default branch (e.g. `main` or `master`). If it produces no output, fall back to treating `main` and `master` as default branch names.

4. Check for uncommitted changes by running:
   ```bash
   git status --porcelain
   ```
   If there is any output, prompt the user:

   > You have uncommitted changes. Would you like to commit and push them before running Shift, or continue without doing so?

   If they want to commit, ask for a commit message, stage all changes (`git add -A`), commit, and push the current branch before proceeding.

5. If the current branch matches the default branch, warn the user and suggest they switch to a dedicated branch before running Shift — for example:

   > You're on the default branch (`{branch}`). It's recommended to run Shift against a separate branch (e.g. `laravel-upgrade`) so the changes can be reviewed and merged when done. Would you like to continue anyway, or switch to a new branch first?

   If they want to create and switch to a new branch, do so before proceeding. If they choose to continue on the default branch, note it and proceed.

6. Build the `scs` connection string in the format `github:owner/repo:branch`.

7. Run the Shift via the API, capturing both the HTTP status code and response body:
   ```bash
   curl -s -o /tmp/shift_response.json -w "%{http_code}" -X POST \
     -H 'Accept: application/json' \
     -d "api_token=$SHIFT_API_TOKEN" \
     -d "code=$ARGUMENTS" \
     -d "scs=github:owner/repo:branch" \
     https://laravelshift.com/api/run
   ```

8. Handle the response based on the HTTP status code:

   - **202** — Success. Parse the response body and extract `shift_number`. Display this message exactly:

     > Shift #{shift_number} has been queued. Most Shifts run within a few minutes. You may monitor its progress at: {pr_url}. Once the {pr_term} is open, you may use the `/shift:review {shift_number}` command to automate the review process.

     Where `{pr_url}` is the HTTPS URL to the repository's pull requests page (`{repo_url}/pulls` for GitHub, `{repo_url}/-/merge_requests` for GitLab) and `{pr_term}` is "pull request" for GitHub or "merge request" for GitLab.

   - **400** — Bad request. Parse the response body and display the `message` field directly to the user.

   - **401** — Invalid token. Tell the user their API token was rejected. Prompt them to re-enter it, then save the new value to `.claude/settings.local.json` under `env.SHIFT_API_TOKEN` (merging into any existing file). Retry the request once with the new token.

   - **402** — Payment required. Parse the response body and extract `shift_number` and `checkout_url`. Display this message exactly:

     > Shift #{shift_number} requires payment. You may complete checkout at: {checkout_url}. Once paid, your Shift will run. Then you may use the `/shift:review {shift_number}` command to automate the review process.

   - **403** — Not authorised to run this Shift. Tell the user their account does not have access to run this particular Shift (it may require a purchase or a different plan at laravelshift.com).

   - **Any other status** — Show the raw status code and response body and ask the user how they'd like to proceed.
