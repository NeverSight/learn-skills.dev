---
name: git-tag
description: 创建 Git 版本标签；用户要求打 tag、大小版本升级，或显式调用 /git-tag、$git-tag 时使用。通过 cyeam tag 执行，默认 minor，支持 major 和 --dry-run。仅编辑技能说明或讨论版本规则时不执行打标签。
---

# Git Tag

在用户指定的 Git 仓库中，通过 cyeam CLI 创建指向当前 HEAD 的本地版本标签。

## 调用

| 用户输入 | 执行命令 |
| --- | --- |
| `/git-tag` 或 `$git-tag` | `cyeam tag minor` |
| `/git-tag minor` | `cyeam tag minor` |
| `/git-tag major` | `cyeam tag major` |
| `/git-tag minor --dry-run` | `cyeam tag minor --dry-run` |
| `/git-tag major --dry-run` | `cyeam tag major --dry-run` |

`$git-tag` 支持同样的参数。只提供 `--dry-run` 时，模式仍为 `minor`。
小版本：`v1.2.3 → v1.3.0`；大版本：`v1.2.3 → v2.0.0`。

## 执行流程

1. 使用用户指定的仓库；没有指定则使用当前工作目录所属仓库。
2. 解析模式与 `--dry-run`。未指定模式时用 `minor`；不支持的参数应报错，不猜测映射或拼接到 shell 执行。
3. 显式调用或明确要求打 tag 已授权创建本地标签，直接执行对应的 `cyeam tag` 命令，无需再次确认，也无需先进行一次预览。
4. 读取 CLI 结果，报告旧版本、新标签及目标提交；预览时明确说明尚未创建标签。默认 JSON 信封的 `data` 包含 `previous`、`tag`、`commit`、`dry_run`。

## 版本和失败处理

- 版本计算交给 CLI：以本地最大稳定版本 `vMAJOR.MINOR.PATCH` 为基准，忽略其他格式和预发布标签；没有匹配标签时从 `v0.0.0` 开始。
- CLI 要求工作区干净，包括暂存和未跟踪文件。失败时展示原因并停止，不自动提交、stash、删除文件或覆盖标签。需要提交时按用户意图使用 [git-cmsg](../git-cmsg/SKILL.md)。
- 直接执行不代表 `git tag -f` 或强制推送；此入口不接受 `--force`。
- 默认只创建本地标签。仅在用户明确要求时拉取或推送；推送使用本次成功创建的确切标签，不能推送所有标签或强制覆盖远端。
- CLI 未安装或不支持 `tag` 时，说明需要安装或更新 cyeam；不要临时手算版本并退回到原生 `git tag`。若当前任务就是开发此 CLI，可从源码构建到临时目录，并在目标仓库运行该二进制。
