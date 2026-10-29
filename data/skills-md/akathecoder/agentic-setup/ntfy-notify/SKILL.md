---
name: ntfy-notify
description: Publish a user update through ntfy when an ntfy notification is needed.
---

# Ntfy Notify

Publish a message to the user's ntfy topic with the ntfy CLI, falling back to curl
when the CLI is unavailable.

## Configure a topic

Take the topic from the current conversation when the user provides one. Otherwise,
read the repository-root `.ntfyconfig` file. It contains exactly one non-empty line:

```text
topic=agent-updates-random-suffix
```

The topic must match `[-_A-Za-z0-9]{1,64}`. If neither source provides a valid topic,
fail clearly and ask the user for one. Do not create a topic configuration unless the
user asks; ntfy creates a topic when it is first published to.

Use `NTFY_SERVER` from the shell environment as the server URL. If it is unset or
invalid, do not publish and ask the user to configure it; never fall back to a default
server URL. For access-token authentication, use `NTFY_ACCESS_TOKEN` from the shell
environment, falling back to `NTFY_TOKEN` for compatibility. Never put a token in
`.ntfyconfig`, source control, or a user-facing message. If the server requires
authentication and no token is available, report the publish failure and ask the user
to provide `NTFY_ACCESS_TOKEN` in the environment.

## Send a message

Set `title`, `message`, `priority`, and `tag` for the update. Write `message` as
Markdown so it can carry readable detail: use short headings, bullets, links, and
inline code where useful. ntfy accepts priorities `min`, `low`, `default`, `high`,
and `urgent`; its tags are comma-separated emoji shortcodes or labels.

When `ntfy` is on `PATH`, publish with the CLI. Pass the complete URL so that the
configured server is used rather than the CLI's local default host:

```sh
ntfy publish --markdown --title "$title" --priority "$priority" --tags "$tag" \
  "$server/$topic" "$message"
```

When an access token is available, add `--token "$access_token"` before the topic
URL. `access_token` is `NTFY_ACCESS_TOKEN` when set, otherwise `NTFY_TOKEN`.

When the CLI is unavailable, publish with curl:

```sh
curl --fail --silent --show-error \
  -H "Title: $title" \
  -H "Priority: $priority" \
  -H "Tags: $tag" \
  -H "Markdown: yes" \
  --data "$message" "$server/$topic"
```

When an access token is available, add this header to the curl request:

```sh
-H "Authorization: Bearer $access_token"
```

Quote every dynamic value. Do not print an expanded command that includes a token.
Treat a non-zero CLI exit code or curl failure as a failed notification and report the
actionable error without exposing secrets.

## Done when

- A valid topic came from the user or `.ntfyconfig`.
- A valid `NTFY_SERVER` was configured.
- The message was accepted by ntfy, or the user received the reason it could not be
  sent.
