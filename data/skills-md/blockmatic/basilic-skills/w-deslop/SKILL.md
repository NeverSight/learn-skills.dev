---
name: w-deslop
description: Remove AI-generated slop introduced on this branch relative to main.
disable-model-invocation: true
---

Diff this branch against main and remove comments, defensive noise, and `any` casts that do not match the surrounding file.

1. Diff against main for every file this branch changed, including existing files it modified, not only files it added.
2. Identify slop: extra comments a human would not add, abnormal try/catch on trusted paths, casts to `any`, style inconsistent with the file.
3. Remove it. Do not rewrite unrelated structure. Run the smallest existing check for the touched files.
4. Docs: `/w-docs` if behavior or commands changed.
