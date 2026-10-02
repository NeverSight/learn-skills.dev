---
name: svg-figure
description: Explicit-only skill. 文書に載せる説明図を figures/<name>.svg に手座標の SVG で描き、必要なら PNG も書き出す。md・html・docx のどこからでも同じ図を参照できる、形式に依存しない部品として扱う。ユーザーが「/svg-figure」「svg-figure を使って」のように明示的に指定した時のみ使用する。「図にして」「図解して」と言われただけでは自動起動しない。画面ワイヤ・数値のグラフには使わない。
---

# svg-figure

説明図を `figures/<name>.svg` に **座標で直接** 書く。1 図 1 ファイル。文書の形式（md / html / docx）とは独立した部品として扱う。

mermaid / D2 を使わない理由: レイアウトがレンダラ任せだと、箱の中に 2 行入れる・特定の箱だけ色を変える・数値を赤で強調する、といった「言いたいことを図に埋め込む」操作ができない。レーン図や比較図を D2 で描こうとすると、透明な中継点や手指定の幅・高さで位置を作ることになり、実質手座標になる。最初から座標を持つ方が短い。

**例外**: 箱が 15 個を超える図や、ノード間を総当たりで繋ぐ図は座標計算が割に合わない。その時だけ D2 などのレンダラで下書きし、出力された SVG を下の規約に合わせて手で整える。

## 手順

### 1. 何を主張する図かを先に書く

座標を置く前に `aria-label` を書く。**これが規約の要**で、図で何を言うのかを先に言語化させ、飾りの図を防ぐ。読み上げ対応も兼ねる。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 {高さ}" width="920" height="{高さ}"
     style="font-family:Roboto,'Noto Sans JP',sans-serif"
     role="img" aria-label="{この図が主張していることを 100〜200 字の日本語で。最後は「〜という図」}">
```

- 幅は 920 固定。高さだけ内容に合わせる（200〜470 程度）
- ファイル名は英語 kebab-case（`login-flow.svg`）。何の図かが分かる名前にする

### 2. 描く（縛り）

- 使う要素は **`rect` / `text` / `line` / `path` / `defs>marker` だけ**。`g` と `transform` は使わない（座標は全部絶対値にして、後から数値だけ直せるようにする）
- 箱は `rect` + 別の `text`。`text` は `text-anchor="middle"` で箱の中央に置く。2 行目は `y` を +16〜18
- 強調は `font-weight="700"` のみ。中間の太さは使わない
- 文字サイズは `10.5 / 11 / 11.5 / 12 / 12.5` から選ぶ（図中の見出しだけ 12.5 太字）
- 角丸は `rx="8"`（小さい箱 6、外側の括り枠 12）
- 線は `stroke-width="1.4"`〜`1.6`、強調は `2`。**分岐は 1 本の `path` に `M`/`L` を並べて書く**。結果を示す要素（確定の箱・承認の矢印）は `2` に上げる
  例: `<path d="M154 164 L154 180 M104 180 L214 180 M104 180 L104 196" fill="none" stroke="#0d74ce" stroke-width="1.4"/>`
- 矢印は `defs > marker` を定義して `marker-end` で使う。**id はその図固有のプレフィックスにする**（1 つの文書に複数の図が並ぶため）。色違いは `-r` / `-g` のようにサフィックスで分ける
  ```svg
  <marker id="{図の略号}-a" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12"
          refX="10.5" refY="6" orient="auto"><path d="M0 0L11 6L0 12z" fill="#113264"/></marker>
  ```
- 線種は次の 3 つを使い分ける

  | 線種 | 書き方 | 使いどころ |
  |---|---|---|
  | 実線 | `stroke-dasharray` なし | 通常の流れ、箱の枠 |
  | 点線 | `stroke-dasharray="6 4"` | 範囲の括り、現状 / 将来の区別、差し戻し |
  | 細かい点線 | `stroke-dasharray="2 3"` | 確認待ち |

- **重ね順は描いた順。枠をまたぐ線は最後に書く**（先に書くと後から置いた枠に隠れる）
- 色は CSS 変数を使わず、**次の値だけを 16 進で直書き**する

  | 用途 | 値 |
  |---|---|
  | 文字 / 補助文字 | `#1c2024` / `#60646c` |
  | 主線 / 強調枠 | `#0d74ce` / `#113264` |
  | 淡い塗り / 面 / 白 | `#e6f4fe` / `#f9f9fb` / `#fff` |
  | 成功・確定 | `#218358`（塗り `#f4fbf6`） |
  | 注意 | `#ab6400`（塗り `#fefbe9`） |
  | 問題・危険 | `#ce2c31`（塗り `#fff7f7`） |
  | 弱い枠 / 中間の枠 | `#d9d9e0` / `#8b8d98` |

  プロジェクトの CLAUDE.md / AGENTS.md が色表のファイルを指定していれば、構造の 4 スロット（主線・強調枠・淡い塗り・面）はそちらの値を使う。状態色（成功・注意・危険）と文字色は、意味を保つためこの表のまま使う。
- **色だけで意味を伝えない。** 状態（確定・確認待ち・差し戻し など）は箱や矢印に必ず文言を併記し、線種（上の表）と太さでも区別する

型（迷ったらこの 3 つ）:

- **比較**: 点線で括った塊を 2 つ横に並べ、間に矢印 1 本（現状 → 提案 / Before → After）
- **階層**: 縦に積んで `path` で分岐
- **フロー**: 横に並べて矢印でつなぐ。レーン（登場人物ごとの帯）は点線の `rect` で括る

### 3. 文書から参照する

**図の直前に、その図が言いたいことを述べる本文を置く。** キャプションは付けない（`aria-label` と本文が説明を兼ねる）。

| 文書 | 書き方 |
|---|---|
| md | `![{aria-label と同じ文}](../figures/<name>.svg)` |
| html | `<img src="../figures/<name>.svg" alt="{aria-label と同じ文}">` |

`alt` に `aria-label` と同じ文を書くのは、pandoc が docx の代替テキストに移すため。**md を原本にする文書も、html を原本にする文書も、同じ SVG ファイルを見る。** 図のために原本の形式を変えない。

### 4. PNG が要るとき

Google Docs・Keynote・PowerPoint は SVG を扱えない（Notion は SVG 可）。docx へ落とす場合も PNG が要る。

Chrome の headless で 2 倍に描画する。`--window-size` には `viewBox` の幅・高さをそのまま入れる。

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --hide-scrollbars --disable-gpu \
  --force-device-scale-factor=2 --default-background-color=FFFFFFFF \
  --window-size=920,{高さ} \
  --screenshot="$PWD/figures/<name>.png" "file://$PWD/figures/<name>.svg"
```

Chrome のパスは macOS の既定。Linux では `google-chrome` / `chromium`、Windows では `chrome.exe` のパスなど、環境に合わせて読み替える。

### 5. 確認

- ブラウザか VS Code のプレビューで開き、①矢印が繋がっているか ②枠に隠れた線が無いか ③`aria-label` の説明と図が一致しているか
- 文書に載せたら、印刷（PDF）で**紙幅からはみ出していないか**を見る

## やらないこと

- 画面ワイヤフレーム、数値のグラフ
- 図の中に結論を書かない。結論は本文に書き、図は構造を示す
