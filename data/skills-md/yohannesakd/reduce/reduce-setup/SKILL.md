---
name: reduce-setup
description: "Configure the reduce skill: ask the user which models its subagents use in each harness, then write and validate ~/.config/reduce/config.json. Use to set up reduce on a new machine, change its models, or fix a configuration that reduce-step rejects."
---

# Reduce setup

Ask the user how the [reduce](../reduce/SKILL.md) skill picks its subagent models, and write `~/.config/reduce/config.json`.
The keys and their meanings are in [reduce's model table](../reduce/SKILL.md#models). Read that section first. Do not keep a second copy of it.
This skill changes only that file. It does not change the parent model, provider settings, or authentication.

Set `reduce_skill` to the `reduce` folder next to this skill's folder.
The driver owns the contract: `"$reduce_skill/scripts/reduce-step" config` validates a file and prints what each step uses.
For a question about the current configuration only, run that command, report its output, and stop.

## 1. Read the current state

1. Run `"$reduce_skill/scripts/reduce-step" config`. It prints the file path, `exists`, each step's class, and each harness's models.
   When it fails, keep its error message: the new file must fix that problem.
2. Find the current harness from your tools: `delegate_task` means `t3`, the Agent tool means `claude-code`, and `spawn_agent` means `codex`.
3. List the models that the current harness can start:
   - `t3`: call `orchestrator_capabilities`. Use its provider instance IDs and model IDs exactly.
   - `claude-code`: read the values of the Agent tool's `model` parameter.
   - `codex`: read the model choices of `spawn_agent`. When it shows no choices, offer only `null`.
4. Follow the current model-routing instructions when they exist. They can forbid models or providers.

You can validate models only for the current harness. For another harness, keep its current entries, or use model names that the user gives you. Report those as not validated.

## 2. Ask the user

Ask only what the user did not already say. Ask at most five questions in one message. Give your recommendation first in each question.
Use the question tool when it exists. Otherwise ask in one message, and wait for the answers.

1. Which harnesses to configure. Recommend the current harness. Keep the entries of the other harnesses unchanged.
2. For each harness that you configure, the model of each class: `cheap`, `standard`, and `powerful`.
   - Offer only the models from step 1.3, and `null` for the parent's own model.
   - Recommend the smallest capable model for `cheap`, a mid-size model for `standard`, and the strongest model for `powerful`.
   - A class can have a list of models. The subagents then use them in turn, and fall back to the next one when one cannot start. Offer a list for `cheap`, because a run has many check subagents.
3. The class of the `map`, `design`, and `checks` steps. Recommend the defaults: `standard`, `standard`, and `cheap`.
4. `map_subagents`. Recommend `feature`. Offer `one` to lower the cost of small targets.

When the current file is valid, show its values as the current choices. When the user accepts all of them, change nothing and report that.

## 3. Write and validate

1. Make the complete JSON object: the answers, plus every current key and harness entry that the user did not change.
   Write only the keys from reduce's model table. A T3 model is `{"provider": "<instance ID>", "model": "<model ID>"}`.
2. Write it to `~/.config/reduce/config.json.draft`. Create the folder when it does not exist.
3. Run `"$reduce_skill/scripts/reduce-step" config --file ~/.config/reduce/config.json.draft`.
   When it fails, correct the draft and validate again. Ask the user only when the correction changes one of their answers.
   When you stop without a valid draft, delete the draft and keep the current file.
4. Move the draft to `~/.config/reduce/config.json` with `mv`. Then run `"$reduce_skill/scripts/reduce-step" config` again.

## Report

- The file path, and the class and the models of each step from the last `config` output.
- The harnesses that you validated against a live model list, and the entries that you did not validate.
- A run that uses a model which cannot start falls back to the next model of the list, or to the parent's model. A run does not show this until a subagent starts.
