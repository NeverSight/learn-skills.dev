---
name: ssot-refactor
description: Spec Loaderシステムが正しく使われているかをチェックし、未導入のファイルをリファクタリングする。実装でloadSpecを使っていないファイル、テストでtests/utils/loadSpecを使っていないファイルを検出し、spec loader経由に修正する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Spec Loader リファクタースキル

Spec Loaderシステムが実装やテストで正しく使われているかをチェックし、未導入のファイルをリファクタリングするスキルです。

## When to Use

- 「/ssot-refactor」と指示された時
- 「spec loaderが使われてるかチェックして」と言われた時
- 「specをロードしてないファイルを探して」と言われた時
- 新機能実装後のspec loader導入確認時
- リファクタリング対象の洗い出し時

## 実行フロー概要

```text
Phase 1: スキャン → prompts/01-scan.md
    ↓
Phase 2: 分析 → prompts/02-analyze.md
    ↓
Phase 3: リファクタ → prompts/03-refactor.md
    ↓
Phase 4: 検証 → prompts/04-verify.md
    ↓
完成
```

## 途中再開

「Phase 2から再開」のように指定可能。

---

## Phase 1: スキャン

**参照**: `prompts/01-scan.md`

1. 実装ファイルでspec loaderを使っていないファイルを検出
2. テストファイルでspec loaderを使っていないファイルを検出
3. 未導入ファイル一覧を作成
4. 次フェーズへ自動遷移

**検出対象**:

- `app/routes/` 配下で `loadSpec` をimportしていないファイル
- `app/components/` 配下で spec を使うべきなのに使っていないファイル
- `tests/` 配下で `tests/utils/loadSpec` を使っていないファイル

---

## Phase 2: 分析

**参照**: `prompts/02-analyze.md`

1. 各ファイルでどのspecを使うべきか特定
2. ハードコードされている値を洗い出し
3. リファクタリング対象を優先度付け
4. 次フェーズへ自動遷移

**分析観点**:

- どのサービス/セクションに属するか（blog/posts, account/authentication等）
- ハードコードされているリテラル値
- spec loaderで置き換え可能な箇所

**除外するハードコード**:

- `data-testid="..."` の文字列リテラル（`ui_selectors` 廃止済みのため対象外）
- `aria-labelledby="..."` / `id="..."` のアクセシビリティ属性値

---

## Phase 3: リファクタ

**参照**: `prompts/03-refactor.md`

1. spec loader の import を追加
2. ハードコード値をspec参照に置換
3. 型定義を追加（必要な場合）
4. 次フェーズへ自動遷移

---

## Phase 4: 検証

**参照**: `prompts/04-verify.md`

1. `npm run typecheck` 実行
2. `npm test` 実行
3. spec loader導入率の再計測
4. 完了報告

---

## チェックポイント

| # | 項目 | 確認内容 |
| :--- | :--- | :--- |
| 1 | 実装のspec loader | `app/routes/`で`loadSpec`を使っているか |
| 2 | テストのspec loader | `tests/`で`tests/utils/loadSpec`を使っているか |
| 3 | 正しいローダー | サーバー側とテスト側で適切なローダーを使い分けているか |
| 4 | 型定義 | spec用の型をimportしているか |
| 5 | ハードコード | リテラル値がspec参照に置き換えられているか |

---

## Spec Loader の使い分け

| 場所 | 使用するローダー | import文 |
|------|-----------------|----------|
| Route loader/action | `specLoader.server` | `import { loadSpec } from '~/spec-loader/specLoader.server'` |
| lib層 | `specLoader.server` | `import { loadSpec } from '~/spec-loader/specLoader.server'` |
| Vitest | `loadSpec.ts` | `import { loadSpec } from 'tests/utils/loadSpec'` |
| Playwright E2E | `loadSpec.ts` | `import { loadSpec } from 'tests/utils/loadSpec'` |

---

## Specファイルの対応表

| サービス | セクション | specファイル |
|---------|----------|-------------|
| blog | posts | `blog/posts-spec.yaml` |
| blog | post-detail | `blog/post-detail-spec.yaml` |
| blog | landing | `blog/landing-spec.yaml` |
| blog | common | `blog/common-spec.yaml` |
| account | authentication | `account/authentication-spec.yaml` |
| account | profile | `account/profile-spec.yaml` |
| account | subscription | `account/subscription-spec.yaml` |
| shared | project | `shared/project-spec.yaml` |
| shared | validation | `shared/validation-spec.yaml` |

---

## 成果物

| フェーズ | 成果物 |
| :--- | :--- |
| Phase 1 | spec loader未導入ファイル一覧 |
| Phase 2 | リファクタリング計画（優先度付き） |
| Phase 3 | 修正済みファイル |
| Phase 4 | 導入率レポート |

---

## 参照ドキュメント

| ファイル | 役割 |
| :--- | :--- |
| `prompts/*.md` | 各フェーズの金型 |
| `docs/adoption-patterns.md` | 導入パターン一覧と修正例 |
| `.claude/rules/ssot/spec-loader.md` | SsoTルール定義 |
| `app/spec-loader/specLoader.server.ts` | サーバー側ローダー実装 |
| `tests/utils/loadSpec.ts` | テスト側ローダー実装 |

---

## SSoT対象外（ハードコードが正しい値）

以下の値は **意図的にハードコード** されており、spec化してはならない。

| 値の種類 | 理由 |
|---------|------|
| `data-testid` 属性値 | `ui_selectors` は廃止済み。コンポーネント・テストに直接文字列で記述する |
| `aria-labelledby` / `id`（モーダル等） | アクセシビリティ用ハードコード識別子。spec管理不要 |

### `extractTestId` / `ui_selectors` の廃止について

- `app/lib/blog/common/extractTestId.ts` は**削除済み**（Phase 0 対応）
- 全 spec YAML から `ui_selectors:` セクションは**削除済み**
- `data-testid` 値は各 `.tsx` / `.test.tsx` / `.spec.ts` に直接ハードコード済み

**スキャン時にこれらをリファクタ対象と誤検出しないこと。**

---

## 注意事項

- **全フェーズを自動実行** - スキャン→分析→リファクタ→検証を一気通貫で処理
- **既存のロジックは維持** - spec loader導入のみ、機能変更はしない
- **複雑性が増す場合は相談** - コードが著しく複雑になる場合はオペレータに確認
- **`data-testid` はSSoT化しない** - ハードコードが正しい状態。誤って spec 化しないこと
