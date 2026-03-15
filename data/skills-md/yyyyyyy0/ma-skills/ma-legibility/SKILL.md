---
name: ma-legibility
description: >
  テキストの可読性、コントラスト、focus 不可視、placeholder-as-label、
  vague error、キーボード操作、スクリーンリーダー配慮を監査する。
  Use when ユーザーが「文字が読みにくい」「コントラストが低い」「フォーカスが見えない」
  「エラーメッセージが曖昧」「アクセシビリティを確認したい」「プレースホルダー頼みで分かりにくい」
  と言ったときに使うこと。作用対象や画面全体の情報順序だけの話には使わないこと。
license: MIT
metadata:
  author: yyyyyyy0
  version: 1.1.0
  tags:
    - accessibility
    - readability
    - typography
    - ma
---

`ma` のサブスキル。テキストとアクセシビリティを、理解の最後の砦として扱う。

## When to Use

- コントラスト不足があるとき
- フォーカスリングが見えないとき
- エラーメッセージが vague error になっているとき
- placeholder-as-label で文脈が消えるとき
- キーボード操作やスクリーンリーダー対応を点検したいとき

## Do Not Use

- 何を先に読ませるべきかの話だけをしたいとき。`ma-flow` を使う
- ボタンの作用対象だけを確認したいとき。`ma-mapping` を使う
- 不要要素の削減だけをしたいとき。`ma-reduction` を使う

## Core Principle

**テキストは情報の最も直接的な担い手だ。**
テキストが読みにくければ、情報は最後のステップで失敗する。
アクセシビリティのギャップは、そのまま通信の失敗である。

## What to Audit

### Visibility
- コントラスト比は十分か
- disabled / hover / error / focus でも読めるか
- 切り詰められたテキストに開示手段があるか

### Structure and wrapping
- 不自然な改行で意味単位を壊していないか
- 行長は適切か
- ラベルが誤読を生む位置で折り返されていないか

### Error and helper text
- vague error ではなく、問題と修正方法が伝わるか
- プレースホルダーがラベルの代わりになっていないか
- loading / empty / error 状態にテキストラベルがあるか

### Accessibility
- focus 不可視になっていないか
- キーボード順序は論理的か
- ラベルと入力は関連付いているか
- aria-describedby や alt text が必要箇所にあるか

## Process

1. すべての文字列を初見のつもりで読む
2. 文脈依存の文言に印を付ける
3. コントラスト不足と focus 不可視を確認する
4. エラー、空、ローディングの文言具体性を点検する
5. キーボードだけで操作して破綻点を探す

## Constraints

- 開示手段なしに切り詰めてはならない
- エラーメッセージは問題と修正方向を示さなければならない
- プレースホルダーはラベルの代用にしてはならない
- focus 指示なしに outline を消してはならない
- 状態を伝えるために色だけを使ってはならない

## Negative List

- **vague error**: 「エラーが発生しました」だけで止まる
- **placeholder-as-label**: 入力すると意味が消える
- **代替なしの outline: none**: キーボード利用者の位置感覚を失わせる
- **色だけの状態表示**: 形や文言がない
- **詰めすぎた本文字間**: 読みやすさより見た目を優先する

## Output Format

```
### ma-legibility findings

| Element | Issue | Severity | Action |
|---|---|---|---|
| [要素] | [どの原則に違反し、なぜか] | high / mid / low | fix / defer / accept |

Summary: [発見された問題のパターンについての1-2文]
```

問題が見つからない場合は `No violations found.` と明示する。

## Examples

**Positive example 1**

入力: 「低コントラストのフォームと、曖昧なエラーメッセージを見て」

期待: コントラスト、文言具体性、修正案を返す。

**Positive example 2**

入力: 「キーボード操作でこのUIが使えるか確認して」

期待: focus、tab 順、ラベル関連付けを中心に所見を返す。

**Negative example**

入力: 「この Save ボタンが何に効くか分からない」

対応: `ma-legibility` ではなく `ma-mapping` を使う。

哲学が審判。Negative List は判例集。
