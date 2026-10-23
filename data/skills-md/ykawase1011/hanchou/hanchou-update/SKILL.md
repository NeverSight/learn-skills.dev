---
name: hanchou-update
description: >-
  Check or explicitly update installed Hanchou skills while preserving install
  scope, agent targets and local modifications. Does not restart conversations,
  launch sokkin, or enable removed cron/dashboard features.
metadata:
  version: 2.0.0
---

# Update Hanchou

Inventory the actual installed Hanchou paths, selected source/version, local
changes and agent targets. Use the existing skill installer and its live help.
A check request is read-only; an explicit update permits the selected installed
subset to be updated. Do not update unrelated skills, Herdr or provider CLIs.
An installed orchestrator migrating to v2 also needs the new `hanchou-sokkin`
companion; include it in the same authorized scope and selected agent targets,
and report that addition. Updating an unrelated helper alone does not install
or activate the orchestrator.

Preserve local/global scope, pins and customized files; do not replace divergent
copies without resolving their edits. For the v2 migration, inventory old
`hanchou-cron`, `hanchou-kaizen` and `hanchou-publish-issues` copies. Remove only
verified obsolete Hanchou installs within the authorized scope, preserving
customizations and user `.hanchou` data. Old schedules/resources require their
own migration disposition; uninstalling a skill does not stop them.

Verify the installed files and executable modes of `launch-sokkin.sh` and
`measure-session.sh`. Distinguish
file installation from adoption by a running conversation. Use a fresh explicit
invocation to adopt v2; do not auto-close the current chat, rebind ownership or
start a successor. Report installed version/paths, local changes, obsolete copies
removed or retained and remaining manual adoption steps.
