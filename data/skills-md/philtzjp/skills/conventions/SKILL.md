---
name: conventions
description: git の commit-msg hook から呼ぶ、コミットメッセージの書式の検査器。規約の正本は philtzjp/.github の conventions.yml。hook が「書式の検査器がありません」と止めたとき、検査の結果に納得できないとき、hook を設定するときに使う。書式そのものの書き方は github スキルに従う。
---

# conventions

コミットメッセージを、Philtz の規約で検査する CLI です。各リポジトリの `.vite-hooks/commit-msg` が呼びます。

このスキルの中身は、philtzjp/organizer-bot の `packages/conventions` と、philtzjp/.github の `conventions.yml` から philtz-organizer-bot が写しています。ここを直接編集しないでください。次に写したときに上書きされます。

## 中身

- `cli.mjs`: 検査器。依存がなく、Node 22 以上だけで動く
- `conventions.yml`: 規約。作業中のリポジトリに `.github/conventions.yml` があれば、そちらを優先する

## hook から呼ぶ

```sh
#!/bin/sh
cli=.agents/skills/conventions/cli.mjs
if [ ! -f "$cli" ]; then
    echo "書式の検査器がありません。AGENTS.md の手順でスキルを入れてください"
    exit 1
fi
exec node "$cli" commit-msg "$1"
```

検査器がないときに黙って通すと、検査が効いているように見えて効いていない状態になります。止めて、スキルを入れる手順を出してください。

## 検査に落ちたとき

- 出たメッセージに従ってコミットメッセージを直す。書き方は github スキルに従う。
- `--no-verify` で hook を迂回しない。
- 規約がおかしいと思ったら、philtzjp/.github の `conventions.yml` を直す Issue を起票する。このスキルや hook に規則を書き足さない。
