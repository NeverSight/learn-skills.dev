---
name: podcraft-episode-creation
description: Create and verify a Podcraft episode through the running service.
disable-model-invocation: true
---

# Podcraft episode creation

Produce one ready, playable, feed-visible episode through the Podcraft API. The
caller needs Python 3 and network access to the service. A Podcraft checkout is
not part of this workflow.

## 1. Connect

Set `SKILL_DIR` to this skill's absolute directory. The bundled client uses
`PODCRAFT_API_BASE_URL`, falling back to the current server's Tailscale DNS name.
Read [references/api.md](references/api.md), then run its readiness and series
commands.

Podcraft currently has no application-layer API authentication. Network policy
is its only access control. Use a Tailscale address and treat anyone who can
reach TCP port 5200 as having production access. If the caller cannot reach the
configured URL, report the failed check and stop.

**Complete when:** readiness passes and the requested series slug appears in the
API result.

## 2. Frame

Choose one content-authority branch:

- **Generated:** Podcraft researches and writes from a topic and supplied
  summary. Read [references/generated.md](references/generated.md).
- **BYOS:** the supplied script is authoritative; Podcraft renders and delivers
  it. Read [references/byos.md](references/byos.md).

Resolve every required input and use branch defaults for optional inputs the
user did not specify.

**Complete when:** one branch is selected and its create command has concrete
arguments.

## 3. Authorize

Run the branch command with `--dry-run`. This validates local limits, resolves
the series slug and voice, and prints content hashes without creating an
episode.

Episode creation is a production side effect. If the user's request has not
already authorized the exact plan, present its mode, series, title or topic,
source path and hash, voice, and optional overrides for confirmation.

**Complete when:** the dry run passes and the exact submission is authorized.

## 4. Create once

Run the authorized command once with `--dry-run` removed. Save its full stdout,
stderr, exit status, and returned episode ID. The API starts generation in the
background.

The client never retries creation. If the response is lost or the result is
ambiguous, preserve the evidence and reconcile against recent episodes before
considering another create request.

**Complete when:** one request returns an episode ID, or one failed attempt has
preserved evidence.

## 5. Wait and verify

When creation returns an ID, read
[references/verification.md](references/verification.md). Wait for a terminal
status, then apply every production and delivery gate. Keep listening quality
separate from mechanical delivery.

**Complete when:** every mechanical gate has explicit pass/fail evidence and
remaining human checks are named.

## Final report

Return mode, series, title or topic, episode ID, duration, URLs, gate results,
failure evidence, and human review still required.
