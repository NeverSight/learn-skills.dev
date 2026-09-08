---
name: okf-bundle
description: "Maintain a directory of markdown docs as an Open Knowledge Format (OKF) bundle in any project: ensure each concept file has valid OKF frontmatter (required `type`, plus optional title/description/tags/timestamp), keep frontmatter the single source of truth, and regenerate the derived index.md (and an optional human-readable table) from it. Use when adding/editing concept docs (ADRs, knowledge bases, glossaries) or when a bundle's index looks stale. Project-specific drift detection stays in the project."
metadata:
  short-description: 任意プロジェクトの md 群を OKF バンドルとして保守（frontmatter=SSoT → index/表を生成・検証）。
---

# OKF Bundle Maintenance

Markdown ファイルのディレクトリを [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
バンドルとして保守する汎用スキル。**frontmatter を唯一の正準ソース (SSoT)** とし、
`index.md` や人間向けテーブルは frontmatter から生成する派生物として扱う。

プロジェクト非依存・stdlib only。`--bundle-root` で対象ディレクトリを受け取るので、
ADR・知識ベース・用語集など任意の OKF バンドルに使える。

## OKF の必須ルール (SPEC v0.1)

- frontmatter の必須キーは **`type` のみ**。`title` / `description` / `tags` / `timestamp` は任意。
- スカラー値メタデータ (status / timestamp 等) は **frontmatter に置く**。本文の散文に書かない。
- `index.md` / `log.md` は予約ファイル名。概念ドキュメントには使わない。`log.md` の日付は ISO 8601。
- `index.md` / 生成テーブルは**生成物**。手編集しない。

## スクリプト (scripts/)

すべて `python3` 単体 (依存なし) で動く。

| スクリプト | 役割 |
|---|---|
| `okf_validate.py --bundle-root DIR` | frontmatter 検証 (必須 `type` / ISO `timestamp` / `--require`・`--exclude`・`--skip-missing` 可) |
| `okf_index.py --bundle-root DIR --index` | OKF `index.md` (箇条書き) を生成 |
| `okf_index.py --bundle-root DIR --table --columns ... --link-column ...` | 列を frontmatter キーで指定する Markdown テーブルを生成 |

`okf_index.py` の `--check` は書き込まず「生成物が最新か」だけ検証する (drift 検出)。
`--table-output` 先に `<!-- OKF-TABLE:START -->` / `<!-- OKF-TABLE:END -->` マーカーがあれば、
その間だけ置換するのでテーブル前後の散文を保持できる。

`okf_validate.py --skip-missing` は frontmatter が無いファイルを違反にせず除外する
(段階的移行 / lazy migration 用)。frontmatter 未付与の既存ドキュメントを許容しつつ、
付与済みのものだけ `type` 必須 / ISO `timestamp` を強制したいバンドルで使う。
全件 frontmatter 必須のバンドル (例: ADR) には付けない。

## Workflow (Agent が判断で起動)

概念ドキュメントを追加・編集・改番したら:

1. **検証**: `python3 <skill>/scripts/okf_validate.py --bundle-root <DIR> [--exclude README.md]`
   — frontmatter 欠落や必須キー漏れを補う。
2. **再生成**: `python3 <skill>/scripts/okf_index.py --bundle-root <DIR> --index ...`
   (必要なら `--table ...` も) で派生ビューを更新する。
3. **コミット**: 生成物を含めてコミットする (docs chore は main 直 push 可なプロジェクトもある)。

CI 自走に頼らず Agent の判断で回す。許容するのは「実行漏れ (索引が一時的に古い)」だけで、
生成は決定論なので内容ドリフトは発生しない。**索引やテーブルを手で書き起こさない**
(書式ブレ・転記ミスの温床)。

## プロジェクト固有の責務 (スキル外)

「その概念を参照しているコードが概念より新しい」式の drift 検出 (REFERENCE-DRIFT) は
各プロジェクトの enactment surface に依存するため、本スキルには含めない。プロジェクト側の
専用ツール (例: ADR とソースの整合を見る drift チェッカー) が担う。

## 使用例

```bash
# ADR バンドル検証 (全件 frontmatter 必須)
python3 <skill-dir>/scripts/okf_validate.py --bundle-root docs/decisions --exclude README.md
# index.md + README テーブルを再生成
make adr-index   # 内部で okf_index.py を呼ぶ (Makefile target がある場合)

# 通常ドキュメント検証 (lazy migration: 未付与は skip、付与済みのみ検証)
python3 <skill-dir>/scripts/okf_validate.py --bundle-root docs --skip-missing
```
