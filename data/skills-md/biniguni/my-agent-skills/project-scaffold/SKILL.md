---
name: project-scaffold
description: Automatically generates standard directory structures for different types of projects (data analysis, machine learning/deep learning, statistical modeling, and AI agents). Use this skill whenever a user wants to start a new project and needs to quickly create a standardized folder structure for their specific task. 
---

# Project Scaffold Generator

This skill provides a standardized way to generate directory structures for new projects, ensuring consistency across different types of workflows (e.g., Data Analysis, ML/DL, Statistical Modeling, and Agent development).

## When to use

Use this skill when a user asks to:
- "Create a new folder structure for data analysis"
- "Initialize an ML project"
- "Set up directories for an AI agent"
- "Make a skeleton for statistical modeling"

## Available Task Types

The scaffold generator supports the following task types:
- `data_analysis`: For EDA, data engineering, and general data analysis pipelines.
- `ml_dl`: For machine learning and deep learning research and experiments.
- `stat_modeling`: For statistical inference, A/B testing, and hypothesis testing.
- `agent`: For building AI agents and their tools/memory systems.

For the complete recommended file and folder layouts of each task type, load the corresponding reference document:
- [Data Analysis Structure](references/data_analysis_structure.md)
- [ML/DL Structure](references/ml_dl_structure.md)
- [Statistical Modeling Structure](references/stat_modeling_structure.md)
- [AI Agent Structure](references/agent_structure.md)

## How to use

Run the `scaffold.py` script to generate the necessary directories.

```bash
# General syntax
python scripts/scaffold.py <project_folder_name> --task <task_type>

# Example: Generating a data analysis structure in current directory
python scripts/scaffold.py my_data_project --task data_analysis

# Example: Generating an ML/DL structure in a specific path
python scripts/scaffold.py my_ml_project --task ml_dl --path ./my_projects_folder
```

> **Note:** The script will only create the fundamental empty directory structure and `.gitkeep` files. It will not auto-generate boilerplate code files (`main.py`, `train.py`, `.ipynb`, etc.), allowing the user to create files only when they actually need them. You can show them the recommended file structure from the reference files if requested.
