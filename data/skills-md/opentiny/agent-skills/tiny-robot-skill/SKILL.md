---
name: tiny-robot-skill
description: TinyRobot component library **code generation** and **implementation guidance**. Use when analyzing, planning, or generating TinyRobot (AI chat UI) components. This skill provides API constraints, doc/example lookup flow, and code conventions.
license: MIT
metadata:
  author: opentiny
  version: '1.0.0'
---

# TinyRobot Component Library Assistant

This skill provides TinyRobot component library resources: component index, docs, and demo code, to help **generate compliant code quickly**.

## When to use

- Developing with TinyRobot component library (AI chat UI components)
- Configuring project theme and other setup
- Looking up component docs and demo code
- Writing code that follows TinyRobot best practices

## Directory structure

```
./themeConfig.ts - Sidebar/menu index from source (sharedSidebarItems = guide + components + tools)
./src/           - Markdown docs: components (src/components/), guide (src/guide/), tools (src/tools/), examples, migration
./demos/         - Demo source code per component (from source docs/demos)
./rules/         - Lookup and usage rules
```

## How to use

Follow the rule docs for the task:

| Rule document                                    | Use case                                                       |
| ------------------------------------------------- | -------------------------------------------------------------- |
| [project-setting](rules/project-setting.md)       | Install TinyRobot, import components, theme and project setup  |
| [component-use](rules/component-use.md)           | Find component docs and demo code                               |

## Constraints

- Follow project and component API docs strictly
- Do not guess TinyRobot usage from other libraries
- Look up in order: component name → API/docs → demo code
