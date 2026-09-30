---
name: update-codex-model-catalog
description: "更新 Codex 模型目录：当 Codex 以 API key 鉴权（自定义 model provider）时，从 provider 的 /models 接口拉取模型目录并同步到 model_catalog_json 指向的文件。当用户要更新 codex 模型目录、同步模型列表、服务端模型有增删、提到 model_catalog_json 时使用。OAuth（ChatGPT 登录）模式下 Codex 会自动拉取目录，不适用。"
metadata:
  requires:
    bins: ["jq", "curl"]
---

# 更新 Codex 模型目录

Codex 在 API 鉴权模式下不会自动刷新模型目录（`model_catalog_json` 指向的文件），服务端模型增删后需手动同步。流程：检查鉴权 → 检查配置 → 拉取并校验目录 → 备份替换 → 报告变化。**只有接口返回通过校验的完整目录才更新，其余情况一律报错终止、不做任何更改。**

开始前初始化（`model_catalog_json` 未配置时自动插入到 config.toml 第 1 行——TOML 顶层键必须位于第一个 `[table]` 之前，追加到文件末尾会落入 `[projects...]` 表中失效）：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
grep -q '^model_catalog_json' "$CODEX_HOME/config.toml" || {
  sed -i.bak '1i\
model_catalog_json = "~/.codex/codex-models.json"' "$CODEX_HOME/config.toml"
  rm -f "$CODEX_HOME/config.toml.bak"
}
CATALOG="$(grep '^model_catalog_json' "$CODEX_HOME/config.toml" | cut -d'"' -f2)"
CATALOG="${CATALOG/#\~/$HOME}"   # 配置值含字面 ~，shell 引号变量里不展开，必须替换
```

## 安全红线

- **绝不读取或打印 key 存放处的值**（cat、编辑器打开等任何方式；key 可能位于 `auth.json` 的 `OPENAI_API_KEY`，或 config.toml provider 块的 `experimental_bearer_token`）。鉴权判断对 auth.json 只用 `jq -r 'keys[]'` 看字段名；key 只允许出现在命令替换 `$(...)` 内直接传给 curl，不落盘、不回显。
- 改写目录文件前必须先做时间戳备份。
- 不修改 `config.toml` 的 `model` / `review_model`（用户的选择），只在报告中警告。

## 第 1 步：检查鉴权方式

解析活跃 provider 及其配置块（表头精确匹配，避免误取同前缀 provider 的块）：

```bash
PROVIDER=$(grep '^model_provider' "$CODEX_HOME/config.toml" | head -1 | sed 's/.*= *"\([^"]*\)".*/\1/')
PROVIDER="${PROVIDER:-openai}"
BLOCK=$(awk -v p="$PROVIDER" '
  { h = $0; gsub(/[ \t]+/, "", h) }
  h == "[model_providers." p "]" { inblk = 1; next }
  /^[ \t]*\[/ { inblk = 0 }
  inblk { sub(/^[ \t]+/, "", $0); print }' "$CODEX_HOME/config.toml")
```

按 Codex 自身的取 key 优先级判定来源：

- 块内含 `requires_openai_auth = true`，或 provider 为内置 `openai` 且块内无 `experimental_bearer_token` → `AUTH_SRC=json`，key 在 auth.json：

```bash
jq -r 'keys[]' "$CODEX_HOME/auth.json"
```

含 `OPENAI_API_KEY` → API 鉴权模式，继续。否则**结束**：`tokens` = OAuth（ChatGPT 登录），Codex 自动拉取目录无需手动更新；其他输出 = 无法识别，展示字段名说明无法判断；文件不存在 = 提示先 `codex login` 或配置 API key。
- 块内含 `experimental_bearer_token` → `AUTH_SRC=toml`，key 就在 config.toml 中，直接继续（**不查 auth.json**，避免拿到残留的旧 key）。
- 其余 → **结束**：该鉴权方式本 skill 不支持。

同时确认 `config.toml` 存在。

## 第 2 步：检查目录文件

`$CATALOG` 存在且为 `{models: [...]}` 结构（`jq -e '.models | type == "array"' "$CATALOG"`）→ 继续；否则**结束**，说明需先从备份恢复或从 OAuth 模式的 Codex 获取一份初始目录。

## 第 3 步：拉取并校验模型目录

```bash
BASE_URL=$(printf '%s\n' "$BLOCK" | grep '^base_url' | head -1 | cut -d'"' -f2)
```

`BASE_URL` 为空 → **报错终止**：API 鉴权模式下活跃 provider 必须配置 `base_url`，请检查 config.toml。

```bash
CV=$(codex --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'); CV="${CV:-0.147.0}"
curl -s -m 30 "${BASE_URL%/}/models?client_version=$CV" \
  -H "Authorization: Bearer $(
    [ "$AUTH_SRC" = toml ] \
      && printf '%s\n' "$BLOCK" | sed -n 's/^experimental_bearer_token *= *"\(.*\)" */\1/p' \
      || jq -r '.OPENAI_API_KEY' "$CODEX_HOME/auth.json"
  )" \
  > /tmp/codex_api_models.json
```

校验（不通过 → **报错终止，不做任何更改**；可能是网络错误、接口变更、网关异常或该接口不提供完整目录。可展示响应片段辅助排查，先确认不含敏感信息）：

```bash
jq -e '(.models | type == "array" and length > 0)
  and all(.models[]; (.slug | type == "string" and length > 0))
  and all(.models[]; ((.display_name // "") | type == "string" and length > 0))
  and all(.models[]; ((.context_window // 0) > 0))
  and ([.models[].slug] | length == (unique | length))
  and all(.models[]; . as $e
    | ($e | has("supported_reasoning_levels") | not)
      or (($e.supported_reasoning_levels | type == "array")
          and all($e.supported_reasoning_levels[]; (.effort | type == "string" and length > 0))
          and (($e.supported_reasoning_levels | length == 0)
               or (($e.default_reasoning_level // "") == "")
               or any($e.supported_reasoning_levels[]; .effort == $e.default_reasoning_level))))' /tmp/codex_api_models.json
```

校验内容：非空数组；每条目有非空 `slug`/`display_name`、`context_window` 为正数；slug 全局唯一；`supported_reasoning_levels` 存在时须为数组、每档有非空 `effort`、`default_reasoning_level` 落在档位内（字段缺失容忍，兼容非 reasoning 模型）。

## 第 4 步：备份并替换

**幂等**：内容一致则跳过备份与写入：

```bash
diff <(jq -S '.models |= sort_by(.slug)' /tmp/codex_api_models.json) <(jq -S . "$CATALOG") >/dev/null && echo "无变化"
```

输出「无变化」→ 直接进第 5 步。否则备份并替换：

```bash
cp "$CATALOG" "$CATALOG.bak-$(date +%Y%m%d-%H%M%S)"
jq -S '.models |= sort_by(.slug)' /tmp/codex_api_models.json > /tmp/catalog_new.json
jq -e '<第 3 步同一校验表达式>' /tmp/catalog_new.json && mv /tmp/catalog_new.json "$CATALOG"
```

- 落盘前复验（`jq -e`），失败则不落盘、报错终止
- `model` / `review_model` 引用的 slug 不在新目录中时，在报告中高亮警告"当前模型已下线，建议改用 <新目录中的模型>"，不要改用户的 config

## 第 5 步：报告

1. **新增 / 删除**：备份前后 slug 集合对比的差集
2. **变更**：slug 未变但条目内容有变化的模型，列出关键字段差异（context_window、default_reasoning_level 等）
3. 备份文件路径（供回滚：`cp <backup> $CATALOG`）
4. 提醒：正在运行的 Codex 会话需重启才会加载新目录
