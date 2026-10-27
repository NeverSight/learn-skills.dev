---
name: jev-setup
description: Use when Jev is not working yet, a Jev tool reports no_key or auth_failed, or the person asks to connect or fix Jev. Gets their TypeSafe or OpenRouter key into the secret store, unseen by you.
version: 0.2.0
license: MIT
metadata:
  hermes:
    tags: [jev, typesafe, setup, credentials]
---

# Connect Jev (the key never passes through you)

Jev is TypeSafe's decision model. It needs one API key. **You must never see, ask for, or handle that key.**

The key can come from any of four providers, and the same Jev answers either way:

- **TypeSafe** (`jev setup-key`, the default): a key from [console.typesafe.ai](https://console.typesafe.ai/settings/keys).
- **OpenRouter** (`jev setup-key --provider openrouter`): reaches Jev through OpenRouter's Decisions API. Worth offering when the person already has an OpenRouter key, because it is then one key instead of two and one bill instead of two.
- **Venice** (`jev setup-key --provider venice`): reaches the same Jev through Venice, which serves it as its own decision modality. Worth considering when the person already has a Venice key; check Venice's current pricing before relying on any cost claim.
- **OpenCode Zen** (`jev setup-key --provider zen`): reaches Jev through OpenCode Zen, whose free tier answers the same request with the same model id shape. Worth offering when the person has no TypeSafe key — TypeSafe is not accepting new signups — and wants to start without a bill.

`TYPESAFE_BASE_URL` is an explicit compatible-endpoint override for a local mock or HTTPS proxy (for example `http://127.0.0.1:8787`, or a gateway that mounts the API under a path such as `https://gw.example/jev`). It is not a built-in provider endpoint editor: the official URLs above stay fixed by default. The client never forwards a saved or supplied provider credential to an override endpoint — not the keychain entry, not the credentials file, and not `TYPESAFE_API_KEY` from the environment, because that variable is where most installs keep their real TypeSafe key. A gateway that requires a bearer gets `JEV_PROXY_API_KEY` instead: the operator sets it in the same environment as `TYPESAFE_BASE_URL`, for that gateway only, and it is sent to nothing else. The client permits plaintext only on numeric loopback and does not follow redirects. `jev doctor` names the override, says whether a bearer goes with it, and asks it: a gateway answering 401 shows up there as `auth_failed` instead of as silence. Do not send sensitive states to an untrusted proxy. Clear the variable to return to the official endpoint and normal key flow.

If more than one key exists, TypeSafe is used: an existing install never starts routing its decisions somewhere else because an OpenRouter or Zen key happened to be in the environment for a text model. To pick a different one on purpose, set `JEV_PROVIDER=openrouter` or `JEV_PROVIDER=zen` in the environment the commands run in; it is honoured only when that provider actually has a key here, and an unset or unknown value changes nothing. `jev doctor` reports which one is in use under `key.provider`.

## Image-preview qualification is not cloud opt-in

For an image-support review, use `scripts/live_images_check.py` only with authorized synthetic imagery and the existing private key flow. Do not enable `/jev vision_cloud shadow` merely because tests pass: it sends pictures to TypeSafe and needs separate permission for those images. Keep `vision_cloud` off during ordinary installation/readiness checks. A Box answer is an experimental localization result, not permission to execute coordinates. See `docs/images.md` for limits, sensitive-question skips and fail-open behavior.

For a bounded synthetic video-frame QA experiment, read `docs/video-qa-trial.md` in the source repo. `scripts/video_qa_trial.py` requires explicit synthetic-image upload consent and stays advisory; its known-answer pilot does not enable the fleet vision switch or authorize private footage. Preserve the fixed model/question/confidence identities and benchmark against local checks plus selective visual review, not an invented expensive-every-frame baseline.

For ordinary video QA, load `jev-video-qa` as the default workflow. Its general task-specific helper is separate from the opt-in fixed-heading pilot. It does not enable the general cloud-vision switch or authorize private images.

## Recorded score failures are not credential failures

If a paid batch received validated `client.ask` answers but offline `decide.rescore` failed on integer score-distribution keys, use the recorded-score regression and the patched rescorer before buying another answer. Keep validated replies and provider-reported usage before local scoring, distinguish POST attempts from scored rows, and carry all known charges or unknown reservations into any recovery cap. Never relax score validation or relabel `tuned_on` to hide model drift. The synthetic gate evidence in `evidence/gate-114-20261022/REPORT.md` documents the limited result, not permission to promote a policy or enable a mode.

## Rules

- The Hermes manifest intentionally does not require a single provider's environment variable. Provider/key resolution happens at runtime. An absent `TYPESAFE_API_KEY` does not mean an OpenRouter, Venice or Zen installation is broken. Use `jev doctor`'s provider/presence/reachability results, never secret-file inspection. With no key, decision calls keep their existing fail-open behavior; omission from the manifest is not a promise of keyless inference.

- Never ask the person to paste the key into the chat. If they paste one anyway, do not store it, do not repeat it, tell them that key should be replaced, and start the flow below.
- Never read the secret store, `.env` files or `~/.config/jev/credentials` to "check" the key. Use `jev doctor`, which reports only presence and length.
- Never put the key in a command line, a URL, a config file you write, or a log.

## Flow

1. Check the state: `jev doctor`. If `key.present` is true and `jev.reachable` is true, you are done.
2. Start the private key page:

   ```bash
   jev setup-key
   ```

   It opens a page in the browser on the computer you are running on and prints one JSON line on stderr with a `url`. The URL holds no secret.
3. Tell the person, in one sentence, to paste their TypeSafe key into the page that just opened. If `browser_opened` is false, or they are talking to you from another device (Telegram, phone), send them the `url` and tell them it only opens **on the computer the agent runs on**. If they have no key yet, they create one at https://console.typesafe.ai/settings/keys.
4. Wait for the command to finish. It prints `{"status": "stored", "verified": true, ...}` when the key was saved and the provider accepted it. `rejected` means the key was wrong: run it again. `timed_out` means nobody used the page within ten minutes.
5. Run `jev doctor` once more and report the result in a sentence.

## When there is no browser

Headless server over SSH: the person runs `jev setup-key --tty` **themselves** in their own terminal. It is a hidden prompt. Do not run it for them through a tool that captures the terminal.

Remote machine on a private network (Tailscale, VPN): `jev setup-key --host <private-ip> --no-open` and send them the link. That traffic is plain HTTP, so use it only on a network you trust end to end. Never bind a public address.

## Where the key goes

The OS secret store (macOS Keychain service `Hermes TypeSafe API`, or `secret-tool` on Linux), falling back to `~/.config/jev/credentials` (mode 0600). On a Hermes machine it is also written as `TYPESAFE_API_KEY` into `~/.hermes/.env` and every `profiles/*/.env`, because each Hermes lane reads its own file. Running gateways pick it up on their next restart; do not restart one without being asked.
