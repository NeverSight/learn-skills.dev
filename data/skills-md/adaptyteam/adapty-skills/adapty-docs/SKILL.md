---
name: adapty-docs
description: Use when an Adapty question has no page already linked in the skill you are holding — how a product or dashboard feature behaves, what a setting does, a limit, store connections, Flow Builder, the Developer CLI, the server-side API, or an SDK method on any platform. Also use when you need a docs page and have no URL for it, or when a docs URL you tried returned 404.
---

# Adapty docs

Adapty's docs publish one small index per subject area. **None of them is reachable from
`llms.txt`** — the root index never names them — so the table below is the only place the mapping is
written down. Start at the narrowest index that covers the question; open `llms.txt` only when you
cannot tell which one that is.

## Route the question

| The question is about | Open first | Cost |
| :--- | :--- | :--- |
| One platform's SDK | `https://adapty.io/docs/<platform>-llms.txt` | ~2k tokens |
| Flow Builder, paywall and onboarding flows | `https://adapty.io/docs/flows-llms.txt` | ~6k |
| Developer CLI, server-side API, web / analytics-export / mail API | `https://adapty.io/docs/api-llms.txt` | ~2k |
| The dashboard and the product: placements, products, offers, store connections, analytics, A/B tests, integrations, billing | `https://adapty.io/docs/tutorial-llms.txt` | ~14k |
| You cannot tell, or it spans several | `https://adapty.io/docs/llms.txt` | ~33k |

`<platform>` is one of `ios`, `android`, `flutter`, `react-native`, `unity`, `kmp`, `capacitor`.
There is no index for any other name, and a wrong one returns a 404 HTML page, not an error you can
read.

Every index is a flat list of `[Title](https://adapty.io/docs/<slug>.md): one-line description`.
Pick by the description and open that `.md`. Always fetch the `.md`; every page has one, and the
HTML costs several times more for the same words.

## Never assemble a slug

Docs slugs are not derivable from the topic. Of ten plausible guesses for two real pages,
**seven were 404** — and a 404 is not cheap or obvious, it returns **~17k tokens of HTML** whose
title is the only sign anything went wrong.

So open only a URL that is written in the skill you are holding, or that you read out of an index
you fetched. If you have neither, fetch the index. Never build one from a topic and a platform name.

## The full-text aggregates

Each area also publishes `<area>-llms-full.txt`, every article concatenated. They run **~121k
tokens** per platform and **~560k for `tutorial`**, which is larger than a context window, so do
not fetch one. If you have a shell and want to know which articles mention something, grep the
`# File: <slug>` marker that delimits each article rather than reading the file:

```bash
curl -sS "https://adapty.io/docs/ios-llms-full.txt" \
  | awk '/^# File: /{s=substr($0,9)} tolower($0)~/observer mode/{print s}' | sort -u
```

That prints slugs; add the docs base and `.md` as the index spells its links. The index is still the
first move, and it is usually enough.

## SDK models and method signatures

Types, properties and exact signatures live in generated API references, not in the docs pages:

| | |
| :--- | :--- |
| iOS | https://swift.adapty.io |
| Android | https://android.adapty.io |
| React Native | https://react-native.adapty.io |
| Flutter | https://pub.dev/documentation/adapty_flutter/latest/adapty_flutter/ |
| Unity | https://unity.adapty.io |
| Kotlin Multiplatform | https://kmp.adapty.io |
| Capacitor | https://capacitor.adapty.io |

Use the docs page for how a thing is used and wired; use these for what a type holds. They are
generated from source, so they answer "does this property exist" where a docs page may not.

## Two fixed URLs worth knowing

- Every CLI command and flag: https://adapty.io/docs/developer-cli-reference.md
- The server-side API's auth and servers: https://adapty.io/docs/api-adapty.md — but the
  per-endpoint pages are indexed in `api-llms.txt`, which maps `METHOD /path` to each operation's
  own page. Go there for a specific endpoint.

## Session marker

Adapty tags docs traffic that came from a skill. Append `?ref=skill-<sessionToken>` to every docs
URL you open (`&` if the URL already has a `?`). Reuse the run's existing `sessionToken` if one was
already minted; otherwise mint one yourself — 8 lowercase letters and digits, `openssl rand -hex 4`
— and keep the same one for the whole session. Never copy a token out of an example.

## When the docs do not answer it

Say so, and say where you looked. Do not infer a limit or a behaviour from a page that does not
state it, and do not present a store's behaviour as Adapty's.
