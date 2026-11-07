---
name: shell-scripting-safe
description: 写 shell/bash 脚本时使用。防止静默失败与误删。
category: devops
tags: [shell,bash,脚本]
---

# Shell 脚本安全

## 何时用

- 新写或修改任何 `.sh` / bash 脚本。
- 脚本涉及文件删除、目录覆盖、远程操作等危险步骤时。
- 发现脚本某步骤出错后默默继续、没有任何输出时。
- 把手动运维步骤固化成自动化脚本前做方案设计。

## 核心规则

### 1. 头部加 `set -euo pipefail`，让错误立即暴露

**规则：** 每个脚本第一行（shebang 之后）加 `set -euo pipefail`，确保命令非零退出立即终止脚本（`-e`），引用未定义变量报错（`-u`），管道中间命令失败也能被捕获（`-o pipefail`）。

**为什么：** AI 生成的 bash 脚本默认不加这三个选项，导致静默失败危害极大。曾见真实事故：`TARGET_DIR=""` 变量赋值失败（来自上一条命令出错），下一步 `rm -rf "$TARGET_DIR/"` 展开为 `rm -rf "/"` 并成功执行——因为没有 `-u`，空变量不报错；因为没有 `-e`，上一步出错没停下来。加上这三行，相同场景会在变量赋值处立即报错退出。

**怎么做：**
```bash
#!/usr/bin/env bash
set -euo pipefail

# 之后的所有命令：任何一步失败即停止，未定义变量即报错
```
- 若某条命令允许失败，用 `command || true` 或 `command || echo "可选步骤失败，继续"` 显式豁免，不要关掉全局 `-e`。
- 子 shell 调用的脚本同样需要各自设置，不继承父脚本的 `set` 选项。

---

### 2. 变量永远加双引号

**规则：** 引用任何变量时都用双引号：`"$var"`、`"$@"`、`"${array[@]}"`；只在明确需要分词或通配符展开时才省略引号。

**为什么：** AI 写 bash 时很少给变量加引号，遇到含空格或通配符的路径时立刻出事。典型案例：`cp $SRC $DST` 在 `SRC="/home/user/my files/data.txt"` 时被 shell 解析为 `cp /home/user/my files/data.txt $DST`，变成三个参数，`cp` 报错或拷错文件。更危险的是 `rm -rf $DIR/*`，若 `DIR` 是 `/tmp/app `（带尾随空格），展开结果不可预料。

**怎么做：**
```bash
# 反例
cp $SRC $DST
rm -rf $DIR/*

# 正例
cp "$SRC" "$DST"
rm -rf "${DIR:?}/"*      # :? 额外保证变量非空，空则报错退出
```
- 数组展开用 `"${arr[@]}"` 而非 `${arr[*]}`，保留每个元素的边界。
- 命令替换也加引号：`output="$(some_command)"`。

---

### 3. 危险操作前校验变量非空与路径合法，提供 dry-run

**规则：** 执行 `rm -rf`、`dd`、`mkfs`、大范围覆盖等不可逆操作前，必须：① 用 `${VAR:?错误信息}` 或显式 `if [ -z "$VAR" ]` 校验关键变量非空，② 检查路径符合预期（不是根目录、不是系统目录），③ 支持 `DRY_RUN=1` 模式只打印不执行。

**为什么：** AI 生成的清理脚本几乎从不做这类防御，使用者一旦环境变量配置错误，`rm -rf "$DEPLOY_DIR/"` 就会变成 `rm -rf "/"` 或 `rm -rf "/var/"` 并实际执行。这类事故在运维历史上反复出现，恢复成本极高。

**怎么做：**
```bash
#!/usr/bin/env bash
set -euo pipefail

DEPLOY_DIR="${DEPLOY_DIR:?必须设置 DEPLOY_DIR 环境变量}"
DRY_RUN="${DRY_RUN:-0}"

# 路径安全检查
if [[ "$DEPLOY_DIR" == "/" || "$DEPLOY_DIR" == "/usr" || "$DEPLOY_DIR" == "/etc" ]]; then
  echo "❌ DEPLOY_DIR 疑似系统目录，拒绝执行" >&2
  exit 1
fi

do_rm() {
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[DRY_RUN] rm -rf $1"
  else
    rm -rf "$1"
  fi
}

do_rm "${DEPLOY_DIR}/old_release"
```

---

### 4. 检查命令存在与退出码，不假设环境

**规则：** 依赖外部命令前检查其是否存在（`command -v`）；关键步骤打印清晰日志；捕获并展示有意义的错误信息，不让失败静默消失。

**为什么：** AI 生成的脚本常假设 `jq`、`aws`、`kubectl` 等工具已安装，在开发机上跑通了，在干净的 CI 容器或另一台服务器上立刻失败，且因为没有检查，报错信息是"command not found"而非"请先安装 jq"。加上静默管道失败（无 `pipefail`），真正的出错行往往被淹没。

**怎么做：**
```bash
#!/usr/bin/env bash
set -euo pipefail

# 前置依赖检查
for cmd in jq aws curl; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "❌ 缺少依赖：$cmd，请先安装" >&2
    exit 1
  fi
done

# 关键步骤带日志
echo "🔄 开始上传到 S3..."
aws s3 sync ./dist "s3://${BUCKET_NAME}/" \
  || { echo "❌ S3 上传失败，退出码：$?" >&2; exit 1; }
echo "✅ 上传完成"
```
- 脚本末尾用 `trap 'echo "脚本在第 $LINENO 行意外退出"' ERR` 输出出错行号，方便定位。

---

### 5. 用函数拆分逻辑，参数做校验；复杂场景换更安全的语言

**规则：** 超过 50 行的脚本用函数组织，每个函数只做一件事；脚本入口校验参数数量和格式；业务逻辑复杂（JSON 处理、并发、错误恢复）时考虑改用 Python/Go，不要用 bash 硬扛。

**为什么：** AI 生成的长 bash 脚本常常是一整个线性流，几百行没有任何函数，全局变量满天飞，出错后根本无从定位。更隐蔽的问题：bash 的字符串处理、算术、数组在边界情况下行为出人意料，AI 很少把这些坑写进脚本注释，维护者往往在生产事故后才发现。

**怎么做：**
```bash
#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "用法: $0 <环境> <版本>" >&2
  echo "  环境: staging | production" >&2
  exit 1
}

# 参数校验
[[ $# -eq 2 ]] || usage
ENV="$1"
VERSION="$2"
[[ "$ENV" =~ ^(staging|production)$ ]] || { echo "❌ 无效环境: $ENV" >&2; usage; }

deploy() {
  local env="$1" version="$2"
  echo "部署 $version 到 $env..."
  # ... 具体逻辑
}

deploy "$ENV" "$VERSION"
```
- 需要解析 JSON 就用 `jq`，不用 `grep`/`sed` 手撕；更复杂的改用 Python。

---

## 正例 / 反例

### 反例：无保护、无引号、静默失败

```bash
#!/bin/bash
# 反例：没有 set -euo pipefail

TARGET=$1                         # ❌ 无引号，无参数校验
BACKUP_DIR=/tmp/backup

mkdir $BACKUP_DIR
cp -r $TARGET $BACKUP_DIR         # ❌ 路径含空格时出错
rm -rf $TARGET                    # ❌ TARGET 为空则 rm -rf ""（行为未定义）

echo "done"                       # 即使前面出错也会打印
```

### 正例：有保护、安全引号、干跑模式

```bash
#!/usr/bin/env bash
set -euo pipefail
trap 'echo "脚本在第 $LINENO 行意外退出" >&2' ERR

usage() { echo "用法: $0 <目标目录>" >&2; exit 1; }
[[ $# -eq 1 ]] || usage

TARGET="${1:?目标目录不能为空}"    # ✅ 非空校验
DRY_RUN="${DRY_RUN:-0}"
BACKUP_DIR="/tmp/backup_$(date +%Y%m%d%H%M%S)"

# 路径合法性检查
[[ -d "$TARGET" ]] || { echo "❌ 目标目录不存在: $TARGET" >&2; exit 1; }

echo "备份目录: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"                          # ✅ 变量加引号
cp -r "$TARGET" "$BACKUP_DIR/"                 # ✅

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[DRY_RUN] 不执行 rm，目标: $TARGET"    # ✅ dry-run 保护
else
  rm -rf "$TARGET"
fi

echo "完成"
```

---

## 自查清单

- [ ] 脚本头部有 `set -euo pipefail`（shebang 紧接其后）。
- [ ] 所有变量引用都加了双引号（`"$var"`），数组用 `"${arr[@]}"`。
- [ ] 危险操作（rm/覆盖）之前有变量非空校验（`${VAR:?}`）和路径合法性检查。
- [ ] 脚本支持 `DRY_RUN` 模式，或在危险步骤前有显式确认提示。
- [ ] 依赖的外部命令通过 `command -v` 提前检查，缺失时给出明确提示。
- [ ] 关键步骤有日志输出，失败时有可读的错误信息，不静默继续。
- [ ] 超过 50 行的脚本用函数拆分；复杂业务逻辑（JSON、并发）已考虑换更安全的语言。
