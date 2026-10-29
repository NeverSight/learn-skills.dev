---
name: gplay-games
description: Play Games Services achievements and leaderboards with gplay `games` (draft config only; publishing to players is Console-only; not the in-game runtime SDK). Use when creating, editing, deleting or exporting a game's achievements or leaderboards.
---

# gplay games (Play Games Services configuration)

`gplay games` configures a game's Play Games Services **achievement** and
**leaderboard** configurations. Shared conventions are in `gplay-cli-usage`.
The whole namespace is `[experimental]`.

## Addressing: the numeric `--application-id`

Play Games resources are keyed by the numeric Play Games application ID, not
the package: `--application-id` on `list`/`create`, the resource id alone on
`view`/`set`/`remove`. The `.gplay/config.json` pin plays no part here.

```bash
gplay games achievements list --application-id 1234567890
gplay games leaderboards list --application-id 1234567890
```

## Writes land in the draft; publishing is Console-only

Every write edits the draft. There is no publish method: `create`/`set`
stage the change, then a human publishes it in the Play Console. Say so when
handing off.

## Achievements

```bash
gplay games achievements view <achievementId> --output json     # read one
gplay games achievements create --application-id 123 \
  --name "First Blood" --description "Win your first match" \
  --type STANDARD --initial-state REVEALED --point-value 10
```

Field flags, or `--file` for a full body: the round-trip of
`view --output json`, and the way to set several locales at once.

## Leaderboards

```bash
gplay games leaderboards view <leaderboardId> --output json     # read one
gplay games leaderboards create --application-id 123 \
  --name "High Scores" --score-order LARGER_IS_BETTER \
  --score-min 0 --score-max 1000000
gplay games leaderboards set <leaderboardId> --name "Top Scores"
```

## `set` replaces: fetch, edit, resend

`set <id>` is a full PUT replace: fetch, edit, resend with `--file`.
The field flags alone are fine for a one-field change.

```bash
gplay games achievements view <id> --output json > ach.json
# edit ach.json …
gplay games achievements set <id> --file ach.json
```

## Safety

`create`/`set` are routine draft writes (`--dry-run` previews the request
body). `remove` is irreversible and sits on the `--confirm` tier:

```bash
gplay games achievements remove <achievementId> --confirm
gplay games leaderboards remove <leaderboardId> --confirm
```
