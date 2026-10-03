---
name: react-query-key-jump
description: Jump to queryKey hook
argument-hint: "<queryKey>"
---

# React Query queryKey Jump

TanStack Query の **queryKey 先頭文字列**（例: `getDrawing`）から、**その key を定義している `useQuery` / `useInfiniteQuery` の `queryKey:` 行**へジャンプする。

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.

## 引数

`/react-query-key-jump <queryKey>`

- 例: `/react-query-key-jump getDrawing` → `src/apis/drawings/useDrawingQuery.ts:34`
- クォートは不要（`getDrawing` のみ渡す）

## 手順

1. **リポジトリ root に移動**し、検索スクリプトを実行:

```bash
bash ~/.agents/skills/react-query-key-jump/scripts/find-query-key.sh <queryKey>
```

（Claude Code: `~/.claude/skills/...`、Cursor: `~/.cursor/skills/...` または `.cursor/skills/...` に symlink される）

2. **カスタム API ディレクトリ**（デフォルト `src/apis` 以外）:

```bash
REACT_QUERY_APIS_DIR=src/api bash ~/.agents/skills/react-query-key-jump/scripts/find-query-key.sh <queryKey>
```

3. **出力の解釈**:
   - 1 行 = `path/to/useFooQuery.ts:34:    queryKey: [...]`（**定義元のみ**）
   - `not_found` … typo / 別名を疑い確認

4. **ジャンプの提示**（必ず両方）:
   - Cursor / IDE: `@src/apis/.../useFooQuery.ts:34`
   - コード引用: `Read` して ```startLine:endLine:path``` 形式

5. **複数ヒット** → 一覧を出し、どれが正か確認（通常 1 件）

## 検索対象の規約（多くの FE コードベース）

| 項目 | 内容 |
| ---- | ---- |
| key の位置 | `queryKey` 配列の **先頭** がエンドポイント名 |
| 定義の本体 | `src/apis/**/use*Query*.ts` / `use*InfiniteQuery*.ts`（要 `rg`） |
| 非定義の使用 | `invalidateQueries`, `setQueryData` 等は **ジャンプ先ではない** |

## フォールバック（スクリプト失敗時）

```bash
rg -n "queryKey:\s*\[\s*'<queryKey>'" src/apis --glob 'use*.ts'
rg -n "^\s*'<queryKey>',?\s*$" src/apis --glob 'use*.ts'
```

## やらないこと

- `invalidateQueries` / `useIsFetching` だけの行を定義元として提示しない
- hook 名（`useDrawingQuery`）で検索しない — その場合は `Glob` で hook ファイルを探す
