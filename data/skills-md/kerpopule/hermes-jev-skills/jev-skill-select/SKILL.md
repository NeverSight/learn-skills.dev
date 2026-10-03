---
name: jev-skill-select
description: Use when unsure which of many installed skills applies to a request, if any, or when asked to make skill loading cheaper or more accurate. Jev ranks the whole catalog and may say no skill is needed.
version: 0.1.0
license: MIT
metadata:
  hermes:
    tags: [jev, typesafe, skills, routing]
---

# Skill selection with Jev

Two round trips, about 0.5 s on a warm connection (this was ~1.2 s before the connections were pooled — every call used to open a new TLS session). The first round trip ranks every skill against the turn: the catalog is cut into batches of 120 that are asked **side by side**, so a 377-skill catalog is four requests sent at once and a 960-skill one is eight, all landing in the time of the slowest. The second round trip is one request: it reads the top five properly, judges each on its own, and may reject them all. Wall clock and billed requests are not the same number, and it is the requests you pay for: reckon on `ceil(skills / 120) + 1` per turn that reaches Jev. A turn that nothing in the catalog comes close to ends after the first request. Small talk and ordinary turns come back with no skill. Reading the skill folders is extra: about 0.15 s for 460 skills.

**When the plugin also runs model routing, the two share one request.** Jev charges per *request*, not per question, so the plugin asks routing's three questions and this stage-1 question or questions in the same call (`jevkit/turn.py`), then hands the answers to each feature's own thresholds. Both halves are also pooled at the connection level (`client.py` keeps keep-alive sockets; a fresh TLS session per call cost ~275 ms of the ~520 ms a decision used to take). Measured against the live API on 2026-09-21/22 with a 379-skill catalog in this fleet: one question ~180-250 ms on a warm connection, and a full Hermes turn (routing + skill selection, merged, pooled) **1784 ms → 672 ms** — 3 requests down to 2. The decisions do not change — the same answers, the same floors — and eight live turns before shipping gave the same tier and the same skill on all eight. `/jev merge_requests off` puts them back in separate requests. A private profile, a turn that looks sensitive, or routing configured for features-only state never merges, so no text moves that was not moving before.

Acknowledgements never leave the machine. "ok", "thanks, that worked", "got it", "never mind", "yes go ahead", a bare "stop" and turns that are only punctuation or emoji are answered locally in 0 ms. That gate is deliberately narrow. A real question (except a pure `next?` continuation), an instruction however short ("do it", "stop it", "do all of them now"), a number, or a word the gate cannot read is sent to Jev, and that includes every request written in a non-Latin script. A wrong ask costs a fraction of a cent; a wrong skip makes the feature quietly do nothing.

The narrow local gate also recognises pure social openers (`how are you doing today`) and pure `next?` continuations; a real question or instruction (`all working?`, `next, fix the config`) still reaches Jev. Selector-only meta-skills such as `using-superpowers` are removed before ranking, including the merged routing/skill request, so they cannot crowd out a task procedure.

## On Hermes

`/jev skills on` makes the `hermes-jev` plugin do this once per fresh turn. When a skill clearly fits, a one-line suggestion is attached to the turn naming it; load it with `skill_view` unless it plainly does not apply. It asks Hermes which folders this session actually loads — the profile's skills folder and every `skills.external_dirs` folder — and it respects `skills.disabled`. Project-local skill folders are not read.

With `/jev routing on` as well, the stage-1 questions travel in routing's request instead of one of their own (see the cost note above), the two answers are read by the code that owns each decision, and the only extra thing in the log is a `merged` line. If that shared request fails, no skill is suggested and routing asks for itself on the next hook, which is the behaviour each feature already had on its own.

The suggestion is then checked against Hermes's own loader before it is made: a name that `skill_view` cannot open in this session is never offered, and the name offered is the one the loader answers to. So you will not be sent to a procedure you do not have — which matters on a profile whose catalog is smaller than the one Jev was ranking, and on a machine where a skill was never installed. Unverifiable means silent, because a suggestion is never worth a call that fails.

Two more rules keep suggestions worth reading:

- A skill the session has already loaded is not suggested again.
- A skill the agent keeps declining stops being offered on that profile. It is suppressed when it was loaded after fewer than 1 in 10 of its last 5 or more suggestions, within 14 days. It is still offered once every 6 hours, so a skill that became useful can come back.

The plugin records each suggestion when it makes it. The profile's `jev/skill-feedback.json` holds only skill names, times and whether the agent loaded the skill. Set `"skill_feedback": "off"` in `jev/state.json` to switch the second rule off.

Measured by replaying one real week (1,188 suggestions):

- **Before:** 403 were loaded within five minutes (34%).
- **With both rules:** 771 suggestions and 395 loads (51%).

That is 115 repeats and 294 declined offers removed, at the cost of 8 loads. A load within five minutes is correlation, not proof the suggestion caused it.

## Diagnosing fail-open

The local `skill` decision-log entry now includes a bounded `reason_code`: `no_skills`, `sensitive_turn`, `stage_one_incomplete`, a recognized transport/validation code such as `timeout` or `invalid_response`, or `other`. Success records use null. Arbitrary reason text, prompts and raw exception messages are not logged. Separate intentional privacy/catalog skips from service failures before changing budgets or thresholds. Older records without this field cannot establish the cause retrospectively; keep them in an unknown bucket rather than guessing. A fail-open remains silence, not a negative skill verdict.

## Asking directly (any agent)

```bash
jev pick-skill --turn "<the request>"            # searches Hermes, Claude Code, Codex and ./skills folders
jev pick-skill --turn "..." --root ~/my/skills   # or name the folders; repeat --root for each one
```

`--root` replaces the default folders, so name every folder you want searched. From Python, `skillpick.discover_roots(hermes_home)` returns the folders Hermes reads, shared ones included, ready to pass to `skillpick.discover()`.

## The reply

```json
{"status": "ok", "needs_skill": 0.78, "skills": [{"name": "xlsx", "path": ".../xlsx/SKILL.md", "match": 0.72}], "latency_ms": 1143}
```

`needs_skill` (0–1) and up to three `{name, path, match}`, best first. Load the first one whose `match` is 0.5 or more. An empty list means proceed without a skill; do not go hunting for one.

Three other shapes, all with an empty `skills` list:

| Reply | Meaning | What to do |
|---|---|---|
| `{"status": "ok", "needs_skill": 0.0, "skills": [], "latency_ms": 0, "skipped": "trivial"}` | Answered locally; Jev was not asked | Proceed without a skill |
| `{"status": "ok", "needs_skill": 0.0, "skills": [], "latency_ms": 663}` | Jev ranked the catalog and nothing came close, so there was no second request | Proceed without a skill |
| `{"status": "fail_open", "reason": "...", "skills": []}` | Jev was not asked or did not answer: outage, no skills found, or the turn looked like it held a secret | Proceed as if this skill did not exist. This is not a "no skill needed" verdict |

`skills_dropped` appears on any of them when the catalog is over the 960-skill cap. It is how many skills, the last ones found, were never ranked, so "no skill fits" does not cover them. Their names are logged once per process. Disable skills you do not use to get back under the cap.

## Notes

- It reads only each skill's `name` and `description` from its front matter, and only the first 200 characters of the description, so a skill with a vague or long-winded description will not be found. Fix the description, not the threshold.
- When two folders hold a skill of the same name, the first folder searched wins. On Hermes that is the profile's own folder.
- The turn is redacted before sending; a turn that looks like it holds a secret is not sent, and you get `fail_open` with an empty list.
- If any one batch fails, the whole pick fails open. A partial ranking would say "no skill" with confidence whenever the right skill sat in the batch that was lost.
- A suggestion is advice. If the loaded skill does not match the task once you read it, drop it and carry on.
