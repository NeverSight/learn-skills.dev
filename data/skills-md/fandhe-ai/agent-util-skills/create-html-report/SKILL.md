---
name: create-html-report
description: >
  分析・比較・調査結果・進捗・計画を、意思決定しやすい自己完結 HTML レポートとして生成する。
  「HTML レポート作って」「レポートにまとめて」「比較を可視化」「グラフで見せて」「ガントチャート作って」
  「ダッシュボード風にまとめて」「見やすくまとめて」で使用。
  データと伝えたい関係に応じて KPI・表・bar・line・scatter・heatmap・waterfall・donut・radar・gantt
  から適切な表現を選び、アクセシブル・レスポンシブ・印刷対応の単一 HTML ファイルを生成する。
model: sonnet
user-invocable: true
argument-hint: "<レポートの目的・対象・データ/ファイル> [--interactive] [--output <path>]"
tools: [Bash, Read, Write]
---

# create-html-report

$ARGUMENTS をもとに、分析結果を「読むだけで要点が分かり、必要なら詳細まで確認できる」自己完結 HTML レポートへ変換する。

最終成果物は原則として単一 `.html` ファイルとする。

## 使い方

引数でレポート化したい内容（比較対象・データ・目的）を渡す。引数が曖昧な場合は Step 1 でユーザーに確認する。

- 出力先はユーザー指定がなければ `_/reports/<report-name>.html`
- `--interactive` 指定時、または静的表示では扱いにくい大量データの場合のみ inline JavaScript を許可する
- `--output <path>` で出力先を明示指定できる

## Core contract

必ず以下を満たす。

1. **Insight first** — グラフを作ること自体を目的にしない。最重要な結論・変化・リスク・意思決定材料を先に特定し、その理解を助ける可視化だけを使う。
2. **Do not invent data** — 不明な値・日付・割合・単位・ステータスを推測で補完しない。欠損は欠損として扱う。必要な仮定を置く場合はレポート内に明示する。
3. **Self-contained** — 外部 CDN・外部 font・外部 JavaScript library・外部 stylesheet・外部画像へ依存しない。CSS・SVG・必要な JavaScript は HTML 内に含める。データ出典への通常の `<a href="https://...">` は外部依存とみなさない。ページロード時に外部通信してはならない。
4. **Accessible by default** — 色だけに情報を依存させない。グラフの主要な内容は文章または表でも確認できるようにする。キーボード・screen reader・dark mode・拡大表示を考慮する。
5. **Progressive enhancement** — 主要な結論とデータは JavaScript なしでも読めるようにする。インタラクションは理解を補助する場合だけ追加する。
6. **Deterministic rendering** — SVG 座標計算・escaping・テーマ・基本コンポーネントは bundled renderer に任せる。Claude が毎回同じ SVG boilerplate を手作業で再実装しない。

## フロー

### Step 1: Context と入力データを把握する

会話・引数・指定ファイル・既存データから以下を特定する。

- レポートの目的、想定読者、意思決定したいこと
- 対象・期間、指標と単位、データソース
- 比較対象、スケジュール・依存関係、不確実性・欠損値

会話や既存データから十分推定できる場合は質問しない。情報不足でも有用な部分レポートを作れる場合は、勝手に値を補完せず「制約・不足情報」として明示して進める。正しいレポートを作れないほど目的・入力が曖昧な場合だけ最小限の確認を行う。

### Step 2: narrative を設計する

HTML を書く前に内部的に次を整理する。

- 最も重要な 1 メッセージ、3〜5 個の key findings
- 意思決定・推奨事項、findings を裏付けるデータ、詳細確認用の情報

情報階層は原則次の順序にする。

1. Title / scope
2. Executive summary
3. KPI / key findings
4. Decision / recommendation（該当する場合）
5. Main visual analysis
6. Schedule / risks / dependencies（該当する場合）
7. Detailed data
8. Methodology / assumptions
9. Sources / generated metadata

すべてを1画面のダッシュボードへ押し込まない。重要情報を上に置き、詳細は下へ続ける。

### Step 3: データの「関係」から chart type を選ぶ

renderer が対応する chart type は `bar` / `line` / `scatter` / `heatmap` / `waterfall` / `donut` / `radar` / `gantt` の8種のみ。chart type ありきで選ばず、伝えたい関係から選定する。

| 伝えたい関係 | chart type | 補足 |
|---|---|---|
| カテゴリ間の大きさ・順位比較 | `bar` | 横棒推奨、0起点の軸 |
| 時系列の傾向・推移 | `line` | 欠損は gap として表現、架空補完しない |
| 2変数の相関 | `scatter` | 相関の説明は annotation で補足 |
| 期間ごとの量・時間×カテゴリの分布 | `heatmap` | 連続値は知覚的に均一な配色を使う |
| 増減への寄与・累積変化 | `waterfall` | 開始値・終了値・差分を明示 |
| part-to-whole（構成比） | `donut` | 6分割以下、正確な値は表を併記 |
| 多変量プロフィール | `radar` | デフォルトにしない（下記参照） |
| タスクの期間・依存関係・milestone | `gantt` | 依存が密な場合は表を併記 |

上記に当てはまらない関係（分布・before/after・多系列比較等）は、対応 chart type への安易な代替を避け、data table での表現を優先する。無理に非対応の chart type を模して自作 SVG を追加しない。

Radar chart はデフォルトにしない。多軸プロフィールの「形」を俯瞰すること自体に価値があり、軸が少数で同一スケールへ正当に正規化できる場合だけ使用する。

#### Chart anti-patterns

原則として以下を避ける。

- 3D chart、gauge / speedometer、不要な gradient・過剰な shadow
- dual-axis chart、10系列以上を重ねた line chart、大量 slice の donut
- 装飾目的だけの chart、比較目的なのに baseline が不統一な chart
- 面積や色だけで厳密比較させる chart

### Step 4: gantt / schedule を使う場合

開始日・終了日・milestone・依存関係のある計画には `gantt` を優先する。gantt は次を満たす。

- 左側に task / workstream 名、横軸に実日付、week / month 等の適切な tick
- phase ごとの grouping、milestone は diamond 等 bar 以外の形で表示
- progress がある場合は planned bar 上へ progress を重ねる
- current date が期間内にある場合は today line を表示
- status は色だけでなく文字・pattern・symbol でも区別
- dependency arrow が密集する場合は無理に描画せず dependency table を併記
- mobile では潰さず `.chart-wrap` で横スクロール可能にする
- SVG と同じ task / start / end / status / progress を表でも確認可能にする

日付が不明な task に架空の日付を与えない。

### Step 5: report spec を作成する

HTML を直接組み立てる前に、renderer が扱える中間 report spec（JSON）を作る。仕様は [references/report-spec.md](references/report-spec.md) を参照する。

report spec には最低限以下を持たせる。

- metadata、title / subtitle、scope、executive summary、findings
- sections、chart definitions、tables、annotations、assumptions、sources

各 chart definition には最低限以下を含める。

- chart type（上記8種のいずれか）、semantic title、takeaway、units
- series、labels、raw numeric/date data、source、accessibility summary

計算済み SVG 座標を report spec に保存しない。座標計算は renderer の責務とする。project 内の成果物として残す必要がなければ一時ファイルとして扱う。

### Step 6: renderer で HTML を生成する

まず必須 CLI の `python3` の存在を確認する。

```bash
command -v python3 >/dev/null || echo "python3 が見つからない"
```

未導入の場合は処理を中止し、導入方法を案内する（macOS: `brew install python3`。その他の環境: 各環境の公式セットアップ手順または環境管理者に確認する。導入後に再実行。権限昇格を要するコマンドは案内しない）。

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/render_report.py" \
  --spec "<report-spec.json>" \
  --output "<output.html>"
```

ユーザー指定がなければ出力先は `_/reports/<descriptive-report-name>.html`。必要なら先に出力ディレクトリを作る。

renderer は Python 標準ライブラリのみで動作する設計とし、外部 package installation を前提にしない。詳細は [references/report-design.md](references/report-design.md) を参照する。

## HTML information design

### Page shell

必須: `<!doctype html>` / `<html lang="...">` / `<meta charset="utf-8">` / viewport meta / descriptive `<title>` / `<header>` / `<main>` / semantic `<section>` / `<footer>`。

長いレポートでは table of contents を追加する。`Skip to main content` link を設ける。desktop で sticky navigation を使う場合も main content の横幅を狭めすぎず、mobile では通常 flow に戻す。

### Visual hierarchy

- max content width を設定し1カラムを基本とする。KPI や小さな比較のみ responsive grid にする
- 長文の line length を制限し、section 間に十分な whitespace を取る
- chart とその説明を一つの visual unit として扱う
- KPI card だけを大量に並べない。KPI は「ユーザーが最初に知る価値が高い値」に限定する

### Chart unit

各 chart は原則 `figure > figcaption(chart title) > takeaway/explanation > SVG > annotation/source > exact-data table` の構造にする。

chart title は単なる名詞ではなく可能なら主要な傾向を伝える。悪い例: 「売上推移」。良い例: 「売上は4月以降3か月連続で増加」。

### Tables

`<caption>` / `<thead>` / `<tbody>` / `<th scope="col">` を使い、必要に応じて `<th scope="row">` を使う。数値は右寄せし単位と桁数を一貫させる。幅広 table は `.table-wrap { max-width: 100%; overflow-x: auto; }` で囲み、body 全体を横スクロールさせない。

## Data visualisation rules

chart-specific な詳細は [references/chart-selection.md](references/chart-selection.md) を参照する。共通ルール:

- 同じ series / entity はレポート全体で同じ visual identity を使い、色だけで区別しない
- 必要に応じて direct label・line style・marker・pattern を併用する
- annotation は短く対象の近くへ配置し、gridline は読取りに必要な分だけ使う
- axis・unit・period を曖昧にせず、chart の下に source / note を置く
- key finding は chart だけに閉じ込めず本文にも書く

### Axis integrity

`bar` の量を長さで表す軸は原則0から開始する。`line` / `scatter` は必要に応じて non-zero baseline を使用できるが、誤解を招かない scale とし切り取った範囲が重要なら明示する。

### Missing values

Missing data を 0 に変換しない。`line` では missing interval を gap として表現する。`N/A`・`unknown`・`not measured` が異なる意味なら区別する。

## SVG accessibility

Inline SVG を使う。意味のある chart は原則 `<svg role="img" aria-labelledby="chart-title-id chart-desc-id">` に `<title>` / `<desc>` を対応させる。SVG の情報が直前の文章と data table で完全に重複し screen reader の二重読上げが悪影響になる場合のみ `aria-hidden="true"` を選択してよい。どちらでも重要なデータを SVG だけに存在させない。

## Colour and contrast

CSS custom properties を design token として使う。最低限 `--bg` `--surface` `--fg` `--muted` `--border` `--grid` `--focus` `--series-1`〜 を `:root` に定義し `color-scheme: light dark` と `prefers-color-scheme` に対応する。

カテゴリカル系列には Okabe-Ito パレット（色覚多様性対応の事実上の標準）を使う。

```
#0072B2 #E69F00 #56B4E9 #009E73 #D55E00 #CC79A7 #F0E442 #000000
```

4系列以下は青(#0072B2)・オレンジ(#E69F00)・空色(#56B4E9)・朱(#D55E00)を優先する。カテゴリカルは6色以下に抑える。`heatmap` 等の連続値は Viridis / Cividis 系の知覚的に均一な配色を使う（グレースケール印刷でも判別可能）。

contrast の目標: 通常テキスト 4.5:1 以上、large text 3:1 以上、意味を持つ chart element / control は adjacent background と 3:1 以上。

red / green だけで positive / negative を表現しない。例: 「↑ +12.4% Increase」「↓ -8.1% Decrease」のように symbol / text も併用する。

## Responsive behaviour

- SVG は `viewBox` を持ち `.chart { width: 100%; height: auto; }` とする
- layout は Grid / Flexbox、font size には `clamp()` を利用してよい
- wide chart は `.chart-wrap` でラップし、small screen で意味が失われるほど chart を縮小しない
- mobile では decorative element を減らし、chart label が重なる場合は abbreviated label + table を使う

## Print / PDF-friendly CSS

必ず `@media print` を用意する。印刷時は light background・dark text とし、navigation / interactive controls を非表示にする。URL や chart がページ外へ切れないようにし、cards / figures / table rows の不自然な page break を `break-inside: avoid-page` 等で減らし、shadow・ink-heavy background を除去する。重要情報を閉じた disclosure 内だけに置かない。

## Interaction policy

標準モードでは JavaScript を必須にせず、まず native HTML / CSS（`<details><summary>`・anchor navigation・CSS sticky header）を使う。

`--interactive` が指定された場合、または静的表示では明らかに使いにくい大量データの場合だけ inline vanilla JavaScript を追加できる（table search / sort、series visibility、section collapse、theme override、gantt の detail toggle 等）。validator は renderer が注入する bundled JS との完全一致のみ許可するため、独自 script を HTML へ直接書かない（機能追加は renderer の `INTERACTIVE_JS` を拡張する）。

ただし以下を必ず守る。

- 最重要メッセージを見るために click を要求しない、hover-only tooltip を使わない
- keyboard で操作でき visible focus を消さない
- JavaScript 無効でも主要情報を読める、animation は原則不要

motion を追加する場合は `prefers-reduced-motion: reduce` で `animation-duration` / `transition-duration` 等を `0.01ms` に短縮する分岐を用意する。

## Security

詳細は [references/accessibility-security.md](references/accessibility-security.md) を参照する。

### Untrusted data

ユーザー入力・外部ファイル・Web 取得データを trusted markup として扱わない。HTML / SVG の text node と attribute に入る文字列は renderer の escaping function（Python では `html.escape(value, quote=True)` 相当）を必ず一元利用する。同じ escape 処理を JavaScript / CSS / URL context に流用しない。untrusted data を `<script>` / `<style>` / event handler attribute / raw URL / raw HTML へ直接埋め込まない。数値は parse 後に有限値であることを確認する。

### JavaScript

inline JavaScript を使う場合、external library・`eval`・`new Function`・untrusted string の `innerHTML` 代入・`onclick="..."` 等の inline handler を禁止する。DOM 挿入は `textContent` / `createElement` を優先し `addEventListener` を使う。`fetch` / `XMLHttpRequest` / `WebSocket` / `EventSource` / `sendBeacon` 等の network access を行わない。

### Links と external dependency

外部リンクを許可するのは原則 source / reference の `<a href>` のみで、URL scheme は `https:` に限定し `javascript:` URL を禁止する。新しい tab で開く場合は `rel="noopener noreferrer"` を付ける。

禁止: `<script src="https://...">`、external stylesheet / font、remote `<img>`、`<iframe src="https://...">`、`<object data="https://...">`、CSS `@import` / `url(https://...)`、remote SVG `<image>` / `<use>`、runtime network request。

## Sensitive data

token・credential・secret・個人情報・非公開内部情報を不用意にレポートへ埋め込まない。入力に secret が見つかった場合は `sk-abc...xyz` のように redaction する。公開可能性が不明な機密情報を含む場合、公開前提の出力先へ書き込まない。

## 検証

生成後、必ず validator を実行し、以下の5段階ゲートで完了を確認する（`.claude/rules/verification.md` 準拠）。

1. **特定**: `validate_report.py` の実行と exit code をもって完了とみなす
2. **実行**:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/validate_report.py" "<output.html>"
   ```
3. **読取**: 出力全体（PASS/FAIL・failure 一覧）と終了コードを確認する
4. **検証**: failure が0件であることを確認する。failure がある場合は HTML または report spec を修正し、再生成してから validator を再実行する
5. **宣言**: validator が pass した場合のみ完了を宣言する。「たぶん通る」等の推測で完了主張しない

validator は最低限以下を確認する。

- output file が存在し non-empty、doctype / html / head / body、charset / viewport / title
- duplicate IDs、SVG opening / closing consistency
- external resource dependency がない、network API を使っていない
- unsafe event handler / `javascript:` URL がない
- meaningful chart に accessible name / description がある
- data table に caption / headers がある、heading order に重大な問題がない
- horizontal body overflow を誘発する既知パターンがない、print CSS が存在する
- source hyperlink と external resource dependency を混同していない

可能なら browser でも目視確認する。browser tool がないことだけを理由に生成を失敗扱いにしない。

## 注意事項

- 対応 chart type は `bar` / `line` / `scatter` / `heatmap` / `waterfall` / `donut` / `radar` / `gantt` のみ。非対応の関係性は無理に代替せず data table を使う
- 外部 CDN・外部フォント・外部画像・外部 JS ライブラリは一切使用しない。ページロード時に外部通信してはならない
- validator が pass するまで完成扱いにしない
- レポートに機密情報を含める場合は、出力先が公開領域でないことを事前にユーザーへ確認する
- レポート化対象のデータに機密情報や信頼できない外部由来データが含まれ、埋め込み可否が不明な場合は生成を中止し、ユーザーに確認を求める
- 出力先ディレクトリ（`_/reports/` 等）が存在しない場合は `mkdir -p` で作成してから書き出す

## 最終報告

完了時は簡潔に以下を報告する。

- generated report の絶対 path
- validation result
- 主要なレポート内容を一文
- interactive mode を使った場合はその旨

例:

```text
HTML レポートを生成しました:
<absolute-path>

Validation: PASS
内容: 3案の性能・コスト・リスク比較と、実装スケジュールの gantt を含みます。
```

## 参照ファイル

必要な場合だけ読む。

- [references/chart-selection.md](references/chart-selection.md) — chart type ごとの選択条件・scale・annotation・gantt・heatmap・scatter 等の詳細
- [references/report-design.md](references/report-design.md) — page layout・design tokens・responsive・print・component implementation
- [references/report-spec.md](references/report-spec.md) — renderer に渡す JSON report spec の schema と examples
- [references/accessibility-security.md](references/accessibility-security.md) — WCAG-oriented checklist、SVG/table accessibility、escaping、safe JavaScript policy
- [samples/comparison.json](samples/comparison.json) — 比較レポートの report spec 例
- [samples/project-gantt.json](samples/project-gantt.json) — gantt / milestone / dependency を含む例
- [samples/time-series.json](samples/time-series.json) — 時系列・annotation の例

## sandbox 環境での実行

このスキルは sandbox 環境で実行できる。renderer（`scripts/render_report.py`）は純ローカルの Python 処理であり、ネットワーク越しの操作を行わない。既定の出力先 `_/reports/` はワークスペース内だが、`--output <path>` に絶対パスや `../` を含む相対パスを指定した場合はワークスペース外へも書き込み得る（ワークスペース内に限定する制約は設けていない）。そのため「ネットワーク不要かつワークスペース外への書き込み経路も無い」とは言い切れない。`--output` を省略するか、正規化後にワークスペース配下へ解決されるパスを指定する限り、実行結果はワークスペース内に収まる。
