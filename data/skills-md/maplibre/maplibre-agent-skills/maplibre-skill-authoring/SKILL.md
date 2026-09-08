---
name: maplibre-skill-authoring
description: How to turn a working session into a MapLibre agent skill — you researched something MapLibre's docs did not cover, got it wrong before you got it right, shipped it, and the session is about to end. Covers what to capture while the context is still live, how to separate the durable claim from the project it came from, and where to hand it off. Use at the end of a MapLibre task that took real research, or when asked to capture one as a skill.
status: process
---

# Authoring a Skill From a Session

The most valuable input to [maplibre-agent-skills](https://github.com/maplibre/maplibre-agent-skills) is a session where an agent got a MapLibre answer wrong, went and found the right one, and shipped working code. That session holds something no later reconstruction can recover: **the wrong answer that came first.** It is the evidence that a skill is warranted at all, and it exists only until the context ends.

This skill is about that harvest. It does not restate how to contribute — [`AGENTS.md`](https://github.com/maplibre/maplibre-agent-skills/blob/main/AGENTS.md) has the agent-specific rules and [`CONTRIBUTING.md`](https://github.com/maplibre/maplibre-agent-skills/blob/main/CONTRIBUTING.md) has the lanes and the four-step order for writing a new skill. Read those for the handoff; read this before the session ends, because after that most of what follows is unrecoverable.

## When to Use This Skill

- A MapLibre task just took real research: docs, source, a CHANGELOG, an issue thread
- The first approach was wrong, or right for Mapbox GL JS and wrong for MapLibre
- A version boundary, gotcha, or failure mode turned up that the docs do not state plainly
- Someone asks to capture the session as a skill

## Capture first, decide later

Do this while the session is still open. Four things, in a scratch file:

1. **The wrong first answer, verbatim.** What you asserted, wrote, or would have written before you checked. This is the baseline hypothesis, and it is the only artifact here that cannot be reconstructed afterward — once the correct answer is in context, the model will not produce the wrong one again on request. A skill earns its place only where a model fails without it, so this is what makes the eval writable.
2. **The primary sources you actually opened.** URLs, not recollections: the style spec page, the GL JS docs page, the PR or issue, the CHANGELOG entry. A citation reconstructed later from memory is a guess wearing a link.
3. **The correct claim, in one or two sentences.** Written as a rule, not as a narrative of what you did.
4. **Versions and the minimal reproduction.** Which MapLibre version, which SDK (GL JS and Native diverge), and the smallest style or code that shows the behavior.

## Separate the claim from the project

Everything above is entangled with the codebase it came from. The test for each line: **would this be true in someone else's project?**

- Cut project names, file paths, internal architecture, and business logic. If a code sample only makes sense with your app around it, rewrite it against a bare map.
- Keep the version boundary. "Broken before X, works after" is judgment; "it works" is not.
- Keep the reason the wrong answer was plausible. That is what makes the skill catch the next agent, and it is usually a Mapbox GL JS habit or a stale training-data assumption.
- Nothing private ships. Anonymize the report; the failure travels, your employer's code does not.

## Size it before you write it

One session's failure buys **one test and one section** — usually an addition to a skill that already exists. Check [Available Skills](https://github.com/maplibre/maplibre-agent-skills#available-skills) and the [open issues](https://github.com/maplibre/maplibre-agent-skills/issues) before assuming you have a new one.

A new skill is warranted only when the claim has no home: not a subtopic of a shipped skill, and not one an existing skill should own. Prefer adding a section, then a pointer between skills, then a new skill last.

## Write the eval from the session, not from the draft

Turn the captured artifacts into an eval before writing content, and write it from what happened rather than from what you intend to say:

- The prompt is **the question the session actually started with**, stripped of the project.
- The rubric encodes **the correct claim** (artifact 3), phrased so it would grade a stranger's answer — not so it matches your draft's wording.
- The `icontains` tripwire is **the name the wrong answer invented** (artifact 1), asserted as `not-icontains`, plus the real name asserted as `icontains`. A session that hallucinated an API name hands you the sharpest tripwire you will ever write.

Mechanics, provider setup, and the baseline run are in [`evals/README.md`](https://github.com/maplibre/maplibre-agent-skills/blob/main/evals/README.md).

## Hand it off honestly

You are drafting a proposal, not a verified skill, and saying so is part of the handoff. State which claims you verified against a primary source and which you could not. If you cannot run the eval — no API keys, or you are working outside a clone of the repo — say that plainly rather than omitting it, and leave the pull request and its description to the human who will answer for them in review.

A failure report carrying artifacts 1, 2, and 4 is a complete contribution on its own. It is worth more than a draft skill with no evidence behind it.

## Do not

- **Don't paste the transcript.** A session is the source material, not the deliverable.
- **Don't cite a source you did not open.** Reconstructed references are the most common way a confidently wrong claim gets through review.
- **Don't report an eval result you did not run**, and don't invent the API keys to run one.
- **Don't promote a project quirk to a skill.** If the fix depended on your build setup, it is not MapLibre judgment.
- **Don't skip the baseline because the answer feels obviously missing.** The model may already get it right, and that finding is a result worth reporting, not a dead end.

## Related Skills

- [**maplibre-mapbox-migration**](../maplibre-mapbox-migration/SKILL.md) — the frequent source of a plausible wrong first answer, where a Mapbox GL JS habit carries over.

## References

- [AGENTS.md](https://github.com/maplibre/maplibre-agent-skills/blob/main/AGENTS.md) — orientation for agents in this repo; reporting a failure from outside it
- [CONTRIBUTING.md](https://github.com/maplibre/maplibre-agent-skills/blob/main/CONTRIBUTING.md) — the contribution lanes and what each one owes
- [evals/README.md](https://github.com/maplibre/maplibre-agent-skills/blob/main/evals/README.md) — prompts, rubrics, baseline checks, provider setup
- [Agent Skills specification](https://agentskills.io/specification) — the `SKILL.md` contract

---

**This skill is a snapshot.** Where a primary source contradicts it — the References above, MapLibre's current documentation, or what MapLibre does when you run it — that source wins. Follow it, then [report the disagreement](https://github.com/maplibre/maplibre-agent-skills/issues/new?template=ai-failure-report.md), citing the source and your MapLibre version: editing your installed copy helps no one else and is overwritten on the next update.
