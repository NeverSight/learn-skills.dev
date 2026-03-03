---
name: developing-ansible
description: Guidelines for writing, reviewing, and refactoring Ansible playbooks, roles, and tasks. Delegates to reference documents by topic. Use when a user mentions writing a new playbook, creating or modifying a role, editing Ansible tasks, managing inventory or variables, or asks to review any Ansible code.
---

# developing-ansible skill

This skill covers any task involving **writing, reviewing, or refactoring** Ansible playbooks, roles, or tasks.

## Rule of Thumb

If the project already has existing examples, always follow them in terms of structure, naming, and style to maintain consistency.
If no relevant examples exist, apply the guidelines defined in this skill and its reference documents.

## Reference Documents

Determine which area of Ansible the request involves, then follow the matching reference document. A single request may involve multiple topics — follow all relevant documents.

| Reference Document                                       | Topic                                                                                 | Covers                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [common.md](common.md)                                   | Code style, file conventions, project layout, secrets                                 | Baseline requirements that apply to all Ansible files                        |
| [developing-playbooks.md](developing-playbooks.md)       | Playbook structure, plays, error handling                                             | Play definition, import vs include, idempotency                              |
| [developing-roles.md](developing-roles.md)               | Role directory layout, variables, handlers                                            | Role directory structure, variable placement, handler rules                  |
| [developing-tasks.md](developing-tasks.md)               | Task ordering, modules, iteration, idempotency                                        | Task key ordering, FQCN, module selection, loop                              |
| [handling-boolean-values.md](handling-boolean-values.md) | Boolean values: YAML booleans, `\| ansible.builtin.bool`, `is ansible.builtin.truthy` | The three bool mechanisms, when to use each, default value pitfalls          |
| [jinja2-templates.md](jinja2-templates.md)               | Jinja2 templates: macros, filters, defaults, whitespace                               | Macros, structured config generation, list/dict filters, undefined variables |
| [reference-code-blocks.md](reference-code-blocks.md)     | Reusable code patterns (block/rescue/always, etc.)                                    | Canonical patterns to compose from                                           |
