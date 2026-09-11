---
name: shunk031-manage-public-private-skills
description: Route and carry out work on coding-agent skills. Use when an edit to a skill under ~/.agents/skills or ~/.claude/skills vanished, reverted, or did not take effect; when asked to add, edit, rename, split, or remove a skill; when deciding whether a skill belongs in shunk031/skills or shunk031/skills-private; when writing eval or trigger cases; or when a request names a skill while you are in a dotfiles repository, because skill content no longer lives there.
---

> [!NOTE]
> After reading this `SKILL.md`, say: `🧰 I read shunk031-manage-public-private-skills.`

# Manage Public and Private Skills

Skill content lives in two dedicated repositories. Neither dotfiles repository holds it any more, so a request to change a skill is a request to change one of these, not the checkout you are probably standing in.

## Where a skill lives

| Repository                  | Holds                                                                                                    |
| --------------------------- | -------------------------------------------------------------------------------------------------------- |
| `shunk031/skills`           | Every publishable skill                                                                                  |
| `shunk031/skills-private`   | Skills whose body names an internal host, a credential, an internal endpoint, or an org-internal process |
| `shunk031/dotfiles`         | The reconcile script and the public subscriptions. No skill content                                      |
| `shunk031/dotfiles-private` | The private subscriptions. No skill content                                                              |

The deciding test is that single question about the skill body. Being written for work does not make a skill private; naming an internal system does. When a skill is close to the line, prefer private and say why.

## Routing a request

1. Identify the skill by name. `~/.agents/skills/<name>` is the installed copy; it tells you the skill exists, not where its source is.
2. Decide the owning repository with the test above, or by checking which repository already contains it.
3. Work in a task worktree of that repository. Never edit the installed copy.
4. If the change spans both skill repositories, keep the worktrees, commits, and pull requests separate and state the ordering between them.

## Never edit the installed copy

`~/.agents/skills/<name>` is a real directory that the `skills` CLI writes. It is a copy, not a link to any source, so edits there are silently discarded by the next `skills update`.

This differs from the old arrangement, where the pool entry was a symlink into the chezmoi source tree and editing the live skill did edit the source.

## The loop from edit to running skill

```
edit in the skill repository worktree
  → gates pass locally
  → pull request
  → merge
  → chezmoi apply on the machine, which runs skills add/update
```

`chezmoi apply` throttles `skills update` to once a day so that a file-watch loop does not fetch on every save. Right after merging, force it:

```bash
DOTFILES_SKILLS_FORCE_UPDATE=1 chezmoi apply    # or: make skills-update
```

| Skill source              | Subscription handling                                                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `shunk031/skills`         | The repository-wide subscription discovers additions; removals and renames add the old name to `SKILLS_RETIRED_NAMES` in `shunk031/dotfiles` |
| `shunk031/skills-private` | Add or remove its entry in `home/dot_config/agents/skills-private.allowlist` in `shunk031/dotfiles-private`                                  |
| Third-party repository    | Add or remove its selected entry in `install/common/skills.sh` in `shunk031/dotfiles`                                                        |

After merging a public skill change, use `DOTFILES_SKILLS_FORCE_UPDATE=1 chezmoi apply` or `make skills-update` to bypass the daily discovery throttle. Ordinary reconciliation discovers additions within one day. The pinned `skills` CLI does not remove upstream deletions in non-interactive mode, so keep the retired-name cleanup until the CLI gains that behavior.

**Never write a private skill's name into `shunk031/dotfiles`.** It is a public repository, and the name alone discloses the internal host, service, or process that putting the skill in the private repository was meant to hide. The reconcile script is public and stays public; only the list of private names moves.

The reconciler reads the applied private file at reconcile time and appends its entries to its own public list, so both sets install through one pass. A machine that has only the public source has no such file, which is normal rather than an error.

In that file only a leading `#` starts a comment, because an entry may carry a `#<ref>` suffix pinning a branch or tag.

## Layout rules that are easy to get wrong

- One directory per skill at `skills/<name>/`, holding `SKILL.md`. Frontmatter `name` must equal the directory name.
- Never put a `SKILL.md` at a repository root. The `skills` CLI stops discovery there and returns only that skill, hiding every other one from installers.
- Never nest a skill deeper than `skills/<name>/`.
- `evals/` is reserved: shuhari looks for `evals/evals.json` and `evals/triggers.json` at fixed paths.
- Never commit `skills/<name>-workspace/`. Those are shuhari run artifacts holding verbatim agent transcripts.
- Scripts a skill needs at runtime go inside the skill directory. The CLI copies the whole skill directory into the pool, so anything outside it will not be there when the skill runs.

## Writing evals

Behavior cases go in `evals/evals.json`, each with `id`, `prompt`, and `expected_output`; `assertions` and `files` are optional. Trigger cases go in `evals/triggers.json` and need at least one positive and one near-miss negative control.

Write `expected_output` as one to three sentences describing the behaviour that should result, not the wording of a good reply, and **do not restate the assertions**. Shuhari runs a blind A/B comparator between the with-skill and without-skill outputs alongside assertion grading, so `expected_output` that echoes assertion text biases that comparison.

Make negative controls near misses. A control that shares the skill's vocabulary while genuinely not calling for it measures the boundary; an unrelated prompt measures nothing.

**An assertion may only test what its own prompt asks for.** To measure something else, write another case whose prompt asks for it. An assertion that demands a warning the prompt never invited, or an outcome the prompt forbade, fails a correct answer: the model answered the question it was given. Such a case reads as a weak skill while it is really a mis-scoped test, and the usual reaction — making the prompt harder or the assertion looser — moves the number without measuring anything.

Assertions multiply, so an unreliable one is worse than it looks. A trial passes only when every assertion in it passes, and the case needs a majority of trials. Three assertions that each hold every time are fine. Three that each hold two times in three leave the case failing about a third of the time purely on which trial each miss lands in, and the verdict then flips between runs with nothing changed — which reads as a flaky skill and is really one case asking several things at once.

Three trials decide a gate, not a question. An assertion scoring worse with the skill than without is a reason to re-measure at five, not a finding: three such assertions once read as the skill hurting, and at five trials two were flat and the third had reversed into the skill's largest single gain. Do not act on a sign you have seen once.

When that happens, split the _case_, not the assertion. Splitting one assertion into two tells you which claim failed but leaves the conjunction intact; separate cases are each judged on their own claim. Prefer a case that asks one thing from the start.

Also watch for an assertion that judges execution in a case whose prompt says not to execute. It is unpassable: judge the decision the response states instead.

Judge substance, not wording. An assertion that lists three nouns fails a response covering two of them, and one that demands a particular word fails a response giving the same reason in different words. Both look like a weak skill and are a brittle test.

A case where both arms pass every trial is a finished measurement, not a broken one: it says the model already does this without the skill. Delete the case and keep the rule in `SKILL.md`. Do not sharpen the case until a difference appears — that manufactures the result.

Runs are offline by default. A skill whose subject is the live network cannot be graded offline: it correctly refuses to proceed and loses to a baseline that guesses. Declare the exception with an `evals/network-required` marker, which makes the gate skip those cases and say why.

It skips rather than enabling egress because the pinned models cannot use the web-search tool at all — they answer `403 Forbidden: Selected provider is forbidden` and fall back to memory or a direct API call, often without saying so. Leave such cases in `evals.json` rather than deleting them: they are correct, and a deleted case leaves the restore condition in prose with nothing to notice when it is met. Removing the marker is both how you put them back and how you test whether the constraint has lifted.

Order of work is `--validate-only`, then `shuhari check trigger`, then `shuhari eval skill`. The first is instant and offline; the last runs both arms plus a grader and a comparator.

## Authoring and reviewing a skill

Write one `SKILL.md`. Do not create per-agent variants: a global install keeps a single canonical copy at `~/.agents/skills/<name>` and points each agent at it.

In shared skill prose, eval prompts, and cross-agent guidance, refer to another skill as `<skill-name> skill`. Do not use Codex's `$skill-name` or Claude Code's `/skill-name` invocation syntax as a general reference. Use those forms only when documenting invocation syntax for that specific agent.

Review the draft with both agents' skill-creation skills, because they disagree usefully:

- Claude Code: `/skill-creator`
- Codex: `$skill-creator` (its built-in, at `~/.codex/skills/.system/skill-creator`)

## Before finishing

Run the owning repository's gates and report which repository owns each change. Keep credential values out of command output, quoted diffs, and summaries — this matters in the private repository, where eval prompts are committed in plaintext and must use placeholders.

Creating or updating a pull request is part of ordinary work. Merging, running `chezmoi apply`, and changing runtime state are not: ask first.
