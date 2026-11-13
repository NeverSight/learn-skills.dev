---
name: creating-hotglue-etl-scripts
description: Creates and tests Hotglue gluestick and pandas ETL transformation scripts. Use when scaffolding an ETL transformation or modifying a Hotglue pipeline's transformation logic.
---

# Creating Hotglue ETL Scripts

## Scaffold

```bash
cookiecutter https://github.com/hotgluexyz/etl-cookiecutter.git
cd <generated-project>
```

The template prompts for repo name, source/target systems, and input/output streams. It generates `etl.py`, `requirements.txt`, and lint/test tooling. Install requirements and follow the generated `AGENTS.md`. Keep sample data and credentials out of git.

## Run locally

Use a dedicated ETL venv (not tap/target venvs):

```bash
uv venv --python 3.10 --seed .venv
uv pip install --python .venv/bin/python -r requirements.txt
ROOT_DIR="$JOB_DIR" JOB_TYPE=read .venv/bin/python etl.py
```

Set `ROOT_DIR` to the job root and `JOB_TYPE` to the direction under test (`read` = connector → ETL → target; `write` = source → ETL → connector).

Pin runtime deps so pandas imports reliably in the ETL runtime, for example:

```text
gluestick
pandas<2.2
numpy<2
pyarrow<20
```

Use the Hotglue Docs MCP for gluestick APIs and transformation behavior.
