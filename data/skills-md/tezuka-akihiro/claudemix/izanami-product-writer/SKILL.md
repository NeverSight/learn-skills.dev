---
name: izanami-product-writer
description: Izanamiプラットフォーム向けのプロダクト紹介記事を生成する。project-spec.yamlなどのSSoTから情報を収集し、5パート構成（概要・主要機能・料金プラン・始め方・FAQ）のテンプレートに基づいて記事を生成・統合する。Use when generating Izanami product introduction articles for ClaudeMix.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Izanamiプロダクト紹介記事生成スキル

ClaudeMixのSSoT（`*-spec.yaml`、機能仕様書）からプロダクト情報を収集し、Izanamiプラットフォーム向けのプロダクト紹介記事を半自動生成するスキルです。

## When to Use

- `/izanami-product-writer` と指示された時
- Izanamiにプロダクト紹介記事を投稿したい時
- プロダクト情報（機能・料金・始め方）を整理して公開ドキュメントにしたい時

## 実行フロー概要

```text
Phase 1: 情報収集 → prompts/01-collect.md
    ↓ SSoTファイルからプロダクト情報を収集・整理

Phase 2: パート別生成 → prompts/02-generate.md
    ↓ 5パート（概要・主要機能・料金・始め方・FAQ）を個別生成

Phase 3: マスター統合 → prompts/03-integrate.md
    ↓ 全パートを一つのファイルに統合して完成

完成: .claude/skills/izanami-product-writer/output/izanami-master.md
```

## 各フェーズの要約

### Phase 1: 情報収集

**参照**: `prompts/01-collect.md`

以下のSSoTファイルを読み込み、プロダクト情報を収集する：

| 収集情報 | 参照ファイル |
| :--- | :--- |
| プロダクト名・ターゲット・コンセプト | `app/specs/shared/project-spec.yaml` |
| 主要機能一覧 | `app/specs/shared/project-spec.yaml` → `services` |
| 料金プラン | `app/specs/account/subscription-spec.yaml` |
| 登録・認証フロー | `develop/account/authentication/func-spec.md` |
| サービスURL | `app/specs/shared/project-spec.yaml` → `references.app_url` |

### Phase 2: パート別生成

**参照**: `prompts/02-generate.md`

5パートをテンプレートに基づいて個別生成：

| パート | テンプレート | 出力先 |
| :--- | :--- | :--- |
| 概要 | `docs/templates.md` → gaiyou | `.claude/skills/izanami-product-writer/output/izanami-gaiyou.md` |
| 主要機能 | `docs/templates.md` → syuyoukinou | `.claude/skills/izanami-product-writer/output/izanami-syuyoukinou.md` |
| 料金プラン | `docs/templates.md` → price | `.claude/skills/izanami-product-writer/output/izanami-price.md` |
| 始め方 | `docs/templates.md` → hazimekata | `.claude/skills/izanami-product-writer/output/izanami-hazimekata.md` |
| よくある質問 | `docs/templates.md` → qa | `.claude/skills/izanami-product-writer/output/izanami-qa.md` |

### Phase 3: マスター統合

**参照**: `prompts/03-integrate.md`

5パートを統合して `.claude/skills/izanami-product-writer/output/izanami-master.md` を生成する。

## 成果物

| フェーズ | 成果物 |
| :--- | :--- |
| Phase 1 | 収集情報サマリー（コンソール出力） |
| Phase 2 | 各パートファイル（`.claude/skills/izanami-product-writer/output/izanami-*.md`） |
| Phase 3 | `.claude/skills/izanami-product-writer/output/izanami-master.md`（最終成果物） |

## 参照ドキュメント

| ファイル | 役割 |
| :--- | :--- |
| `prompts/01-collect.md` | Phase 1: SSoT情報収集の手順 |
| `prompts/02-generate.md` | Phase 2: パート別生成の手順 |
| `prompts/03-integrate.md` | Phase 3: マスター統合の手順 |
| `docs/templates.md` | 各パートのMarkdownテンプレート |

## 注意事項

- **SSoT原則**: プロダクト名・URL・料金などの値は必ずspecファイルから取得し、ハードコードしない
- **spec不在時の対応**: 参照ファイルが存在しない場合は `[情報なし - 手動入力が必要]` とプレースホルダーを記入する
- **出力先**: `.claude/skills/izanami-product-writer/output/` ディレクトリが存在しない場合は作成する
- **段階的生成**: 各フェーズを順序通りに完了させ、ユーザーに確認を求めながら進める
