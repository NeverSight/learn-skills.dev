---
name: agent-figure-gallery
description: Query visual scientific figure references, show candidates for human preference selection, export selected reference bundles, and guide plotting agents from human-selected visual examples to code action.
---

# Agent Figure Gallery

## Core Rule

Treat this skill as a lightweight controller. Do not load the full visual corpus into the skill. Use `AGENT_FIGURE_GALLERY_ROOT` or `DRAWING_KB_ROOT` to point at the external AgentFigureGallery knowledge base.

## Key Files

- KB root: `AGENT_FIGURE_GALLERY_ROOT=/path/to/AgentFigureGallery`
- CLI: `agentfiguregallery` or `python -m agentfiguregallery.cli`
- Gallery server: backend command that serves the reference gallery on localhost
- Candidate index: `data/reference_candidate_index.json`
- Global preferences: `data/reference_global_preferences.json`
- Reference sessions: `outputs/reference_sessions/`

## Minimal Workflow

1. Resolve the KB root:
   ```bash
   export AGENT_FIGURE_GALLERY_ROOT=/path/to/AgentFigureGallery
   ```
2. Query before reading individual references:
   ```bash
   agentfiguregallery query --task "<user task>"
   ```
3. Generate visible candidates:
   ```bash
   agentfiguregallery gallery --plot-type <plot_type> --task "<user task>" --limit 50 --serve
   ```
4. Record human preferences:
   ```bash
   agentfiguregallery prefer --session outputs/reference_sessions/<session_id> --like <ID> --reject <ID> --select <ID>
   ```
5. Export a selected bundle:
   ```bash
   agentfiguregallery bundle --session outputs/reference_sessions/<session_id> --copy-scripts
   ```
6. Use the bundle before writing or revising plotting code.

## Preference Semantics

- `like`: useful for this task or plot type.
- `reject`: not useful for this task or plot type.
- `select`: use this candidate for the current agent action.
- `global_like`: generally useful across tasks.
- `global_reject`: hide from future sessions.

Local preferences must preserve `plot_type`. Global preferences are cross-task.

## Validation

After changing the CLI, gallery, preference logic, or bundle export:

```bash
agentfiguregallery gallery --plot-type embedding_plot --limit 20 --serve
agentfiguregallery prefer --session outputs/reference_sessions/<session_id> --like E01 --select E02
agentfiguregallery bundle --session outputs/reference_sessions/<session_id>
```

Success means visible candidates render, stable IDs are shown, preferences persist, global rejects are hidden from later generated sessions, and the bundle contains selected references plus source code paths.
