---
name: deploy-folder-to-modelscope
description: 当需要将项目特定目录部署到 ModelScope 仓库时，应使用此技能。
author: github/cafe3310
license: Apache-2.0
---

# 部署项目特定目录到 ModelScope (deploy-folder-to-modelscope)

## 描述

此技能旨在将当前项目中的指定目录部署到 ModelScope 仓库。

它通过以下方式简化部署流程：
-   管理本地 `.env` 文件中的 ModelScope 仓库 URL。
-   确保 `.env` 文件被 `.gitignore` 忽略。
-   自动化 Git 操作：克隆、清空（保留 .git）、复制、提交和推送。

## 使用方法

要使用此技能，只需说明您要将哪个目录部署到 ModelScope。例如：

"将 `gradio_app` 目录部署到 ModelScope。"

技能将引导您完成后续步骤。

**注意:** 此技能的入口脚本为 `scripts/run.py`。
