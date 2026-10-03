---
name: model-datasets
description: 模型与数据集的统一下载、落盘与加载约定：平台（HF / ModelScope）只是下载手段，本地一律 /data/models/<org>__<name>、/data/datasets/<org>__<name>，只用绝对路径喂给 transformers / datasets。含新机器的 /data 磁盘准备规则（无 /data 时初始化或软链）。Use when downloading or organizing models/datasets, deciding where to store them, using hf / modelscope CLI, or loading with from_pretrained / load_dataset. 触发词：模型放哪、数据集放哪、下载模型、from_pretrained 路径、/data、hf、modelscope、大文件放哪。
---

# 模型 / 数据集统一存放与加载约定

## 一句话

下载平台是手段，文件本身才是本质。所有模型和数据集，无论来自 HF 还是 ModelScope，都落成同一个形状：

```
/data/models/<org>__<name>/      模型实体
/data/datasets/<org>__<name>/    数据集实体
```

目录里直接是文件本体（`config.json`、`*.safetensors`、tokenizer… 或数据集数据文件），**没有** `snapshots/`、commit-hash 这类中间层。加载**只用绝对路径**，不搞 id 索引、不区分平台。

## 命名规则

目录名 = `repo_id` 里的 `/` 换成 `__`：

| repo_id | 目录 |
|---|---|
| `meta-llama/Llama-3.1-8B-Instruct` | `/data/models/meta-llama__Llama-3.1-8B-Instruct` |
| `ZhipuAI/GLM-4.7-Flash` | `/data/models/ZhipuAI__GLM-4.7-Flash` |
| `HuggingFaceH4/ultrachat_200k` | `/data/datasets/HuggingFaceH4__ultrachat_200k` |

org 名在两个平台偶尔有细微差别（如 `ZhipuAI` vs `zai-org`）无所谓，只要看名字能认出是谁家的哪个模型即可。id 名字不重要，**能用绝对路径加载才是目的**。

## 安装工具（uv）

用 `uv` 装这两个 CLI（隔离环境，可执行文件 shim 到 `~/.local/bin`，确保它在 PATH 里）。

```sh
# 1) uv 本身（没有才装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 国内加速：给 uv 配清华 PyPI 源
mkdir -p ~/.config/uv
printf 'index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"\n' > ~/.config/uv/uv.toml

# 2) HF CLI（提供 hf 命令）
uv tool install huggingface_hub        # 老版本写 huggingface_hub[cli]

# 3) ModelScope CLI —— 包名是 modelscope-hub，不是 modelscope！
uv tool install modelscope-hub
# 注意：uv tool install modelscope 会报 "No executables are provided"，
#       因为新版把 CLI 拆到了 modelscope-hub 这个包，装它的同时会带上 modelscope 库。
```

装完验证：`hf --version`、`modelscope --help`。可用命令：`hf`、`modelscope`、`ms`。
升级：`uv tool upgrade --all`。

## 下载

统一用 `dl` 工具（源码见文末，放到 `~/.local/bin/dl` 且 `chmod +x`）：

```sh
dl <hf|ms> <repo_id> [--type model|dataset] [--name NAME]

dl hf meta-llama/Llama-3.1-8B-Instruct
dl ms ZhipuAI/GLM-4.7-Flash
dl hf HuggingFaceH4/ultrachat_200k --type dataset
```

等价原始命令（`dl` 只是拼好路径 + 强制 `--local-dir`）：

```sh
hf download <repo_id> --repo-type model|dataset --local-dir /data/models/<org>__<name>
modelscope download --repo-type model|dataset <repo_id> --local-dir /data/models/<org>__<name>
```

平台选择只看哪个平台有这个仓：国产模型先在 ModelScope 试，没有的走 `hf`（国内配镜像）。落盘结果完全一样。

## 加载

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
AutoModelForCausalLM.from_pretrained("/data/models/ZhipuAI__GLM-4.7-Flash")
AutoTokenizer.from_pretrained("/data/models/ZhipuAI__GLM-4.7-Flash")

from datasets import load_dataset
load_dataset("/data/datasets/<org>__<name>")
```

ModelScope 下下来的是标准 HF 格式（config.json + safetensors + tokenizer），所以两种来源的绝对路径写法通用。

## 环境变量

```sh
export HF_ENDPOINT=https://hf-mirror.com   # HF 走镜像（国内）
export HF_HOME=/data/hub/hf                # HF 工具缓存
export MODELSCOPE_CACHE=/data/hub/ms       # ModelScope 缓存/中转
export HF_HUB_DISABLE_XET=1                # 必须：HF 2.0 的 Xet 协议经镜像会 401，禁用走普通 HTTP
```

写进 `~/.bashrc` / `~/.zshrc`。`/data/hub` 只是工具缓存，可随时清；`/data/models`、`/data/datasets` 是实体，别乱删。

## 新机器上准备 /data（按现状决策）

原则：**模型/数据集是共享的不可变文件，必须放在大盘上**，不要放根盘、`~`、`~/.cache`。用户习惯统一用 `/data`。

| 现状 | 做法 |
|---|---|
| `/data` 已存在且就是大盘 | 直接用 |
| 没有 `/data`，但已有挂载好的大盘目录（如 `/datahdd`、`/datanfs`） | `ln -s /datahdd /data`（`/data` 不存在时才能建软链；若 `/data` 已是个空目录，先 `rmdir` 再链） |
| 没有 `/data`，但有未初始化磁盘 | 初始化并挂载为 `/data`：分区/格式化（有 LVM 优先 LVM，便于以后扩容）→ 写入 `/etc/fstab`（用 UUID + `nofail`）→ `mount -a` |
| 有多个盘可用 | 可组 LVM 卷合成一个大 `/data`；模型数据集共享不可变，合并成一个卷最省心 |
| 不确定 | 先 `lsblk -f`、`df -h` 看清有没有大盘、挂在哪儿，再决定；具体情况具体分析 |

初始化磁盘会让原有数据丢失，动手前先确认盘是空的。初始化完记得建 `/data/models`、`/data/datasets`、`/data/hub`。

## 验证清单

```sh
ls /data/models /data/datasets         # 目录在
df -h /data                            # 指向大盘，且不是根盘
dl hf hf-internal-testing/tiny-random-gpt2   # 下个小模型试通
python -c "import json;print(json.load(open('/data/models/hf-internal-testing__tiny-random-gpt2/config.json'))['model_type'])"
rm -rf /data/models/hf-internal-testing__tiny-random-gpt2   # 清掉测试
```

## 附录：`dl` 脚本（自包含，直接复制）

```bash
#!/usr/bin/env bash
# dl - 统一的模型/数据集下载（HF / ModelScope 只是下载手段，落盘组织完全一致）
#   dl <hf|ms> <repo_id> [--type model|dataset] [--name NAME]
# 目录：/data/models/<org>__<name>  或  /data/datasets/<org>__<name>
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
ROOT=/data
export HF_HOME="${HF_HOME:-$ROOT/hub/hf}"
export MODELSCOPE_CACHE="${MODELSCOPE_CACHE:-$ROOT/hub/ms}"
export HF_HUB_DISABLE_XET=1   # HF 2.0 的 Xet 经 hf-mirror 会 401，禁用改走普通 HTTP

usage() {
  cat >&2 <<'EOF'
用法:
  dl <hf|ms> <repo_id> [--type model|dataset] [--name NAME]
说明:
  --type   默认 model；dataset 落到 /data/datasets/<org>__<name>
  --name   自定义目录名，默认 repo_id 的 "/" 换成 "__"
示例:
  dl hf meta-llama/Llama-3.1-8B-Instruct
  dl ms ZhipuAI/GLM-4.7-Flash
  dl hf HuggingFaceH4/ultrachat_200k --type dataset
EOF
  exit 1
}
die() { echo "错误: $*" >&2; exit 1; }

[ $# -ge 2 ] || usage
src="$1"; repo="$2"; shift 2
[ "$src" = hf ] || [ "$src" = ms ] || die "平台只能是 hf 或 ms"
type=model; name=""
while [ $# -gt 0 ]; do
  case "$1" in
    --type) type="$2"; shift 2;;
    --name) name="$2"; shift 2;;
    *) die "未知参数: $1";;
  esac
done
[ "$type" = model ] || [ "$type" = dataset ] || die "--type 只能是 model 或 dataset"
[ -n "$name" ] || name="${repo//\//__}"
if [ "$type" = dataset ]; then dest="$ROOT/datasets/$name"; else dest="$ROOT/models/$name"; fi
mkdir -p "$dest"

if [ "$src" = hf ]; then
  echo ">> hf  $repo -> $dest"
  hf download "$repo" --repo-type "$type" --local-dir "$dest"
else
  echo ">> ms  $repo -> $dest"
  modelscope download --repo-type "$type" "$repo" --local-dir "$dest"
fi

echo "完成: $dest"
echo "加载: from_pretrained(\"$dest\")"
```

依赖两个 CLI：`hf`、`modelscope`（安装见上文「安装工具（uv）」），都在 `~/.local/bin`。
