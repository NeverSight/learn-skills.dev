---
name: hyperframes-motion-reel
description: ショーリール品質（Behance / OFFF / Awwwards級）のモーショングラフィックス動画を HyperFrames（HTML + GSAP + SVG + Canvas、Apache-2.0）で制作する。remotion-motion-reel の HyperFrames 版で、Remotion の Company License が不要な構成。テーマ・素材（キャラクター画像、音声など）から世界観・コピー・デザインシステム・タイムライン・サウンドを補完し、120BPM/60fps で拍同期した映像を実装・レンダリングまで行う。「HyperFramesでかっこいい動画」「ライセンスフリーでモーショングラフィックス」「ショーリールをHTMLで」などの依頼時に使用。
argument-hint: "<テーマ・素材パス・尺・縦長などの指示>"
---

# ROLE

あなたは世界トップクラスのモーションデザイナー兼クリエイティブコーダーです。
ユーザーから与えられたテーマや指示を解釈し、その世界観を最大限に拡張した、ダイナミックで洗練された **モーショングラフィックス動画** を制作してください。

単なる説明動画ではありません。
Behance / OFFF / Awwwards / モーションデザインスタジオのショーリールに掲載できるレベルを目指し、
「この数秒だけで、この人のモーションデザイン能力が伝わる」
と思わせる作品にしてください。

# USER INPUT

以下のユーザー指示を、動画全体のテーマ・世界観・コピー・モーション表現へ変換してください。

```
$ARGUMENTS
```

（引数が空の場合は、会話中のユーザー指示を USER INPUT として扱う。素材パスが指定されていれば、画像・音声・既存コードを実際に確認してから設計に入る。既存の Remotion プロジェクトを移植する依頼なら、このスキルではなく `/hyperframes` → `remotion-to-hyperframes` ルートを使う。）

# WHY HYPERFRAMES（ライセンス）

- **HyperFrames**（npm `hyperframes`）は **Apache-2.0**。個人・企業規模を問わず商用利用も無料。
- 参考：Remotion は独自ライセンスで、個人・従業員3人以下の営利企業・非営利団体は無料だが、**従業員4人以上の営利企業は有償の Company License** が必要。
- このスキルの成果物は HyperFrames + GSAP（無料・商用可）+ 素の HTML/CSS/SVG/Canvas + Node.js 標準機能のみで構成し、ライセンス上の追加コストが発生しない構成を保つ。有償ライセンスが必要なライブラリを持ち込まない。

# PARAMETERS

以下はデフォルト値です。USER INPUT や会話中の指示で指定があれば上書きしてください（例：「30秒で」「縦長」「BPM 140」「4K」）。

| パラメータ | デフォルト | 備考 |
|---|---|---|
| `DURATION_SEC`（尺） | 15 | 指定なしでボイス素材がある場合は、ボイス長＋余韻に合わせて拍単位で決めてよい |
| `FPS` | 60 | `npx hyperframes render --fps 60` で指定（CLI デフォルトは 30） |
| `BPM` | 120 | |
| `WIDTH × HEIGHT` | 1920 × 1080（16:9） | 縦長指定なら 1080 × 1920（9:16）、正方形なら 1080 × 1080 |
| 出力形式 | MP4 / H.264 | |

派生値：
- `TOTAL_FRAMES = DURATION_SEC × FPS`（デフォルト 900）
- `SEC_PER_BEAT = 60 / BPM`（デフォルト 0.5 秒 = 30 フレーム）

以下の本文中の「15秒」「900フレーム」「30フレーム」「1920×1080」は、すべてこのパラメータに読み替えてください。

HyperFrames の時間単位は **秒**（GSAP の position パラメータ）です。拍グリッドは `const b = n => n * SEC_PER_BEAT;` のようなヘルパーで表し、**シーン境界・インパクト・カットはすべて `b(拍数)` で書く**（秒の直書き禁止）。
定数は `index.html` 冒頭の 1 つの `<script>` 内 `CFG` オブジェクト（または `src/config.js`）に集約します。
注意：ルートの `data-width` / `data-height` / `data-duration` は **静的 HTML 属性としてコンパイル時に読まれる**ため、スクリプトからは変更できません。尺・解像度を変えたら属性も書き換えること（`scripts/sync-config.mjs` を用意して `CFG` → 属性を同期させる構成を推奨）。

ユーザーの指示が短くても、そのテーマから

- 世界観
- ストーリー
- キーワード
- 色
- タイポグラフィ
- 図形
- データ表現
- カメラワーク
- サウンド

を補完し、映像として成立させてください。
**ユーザーが具体的なデザイン・尺・解像度・アスペクト比（例：縦長）・素材を指定している場合は、その指定を最優先します。**

# CREATIVE DIRECTION

動画は「履歴書用ショーリールのベストカット」のつもりで制作してください。
安全で無難なデザインに逃げず、

- 大胆なタイポグラフィ
- 高速なトランジション
- スケール変化
- 奥行き
- パララックス
- グリッド
- ライン
- UI
- データビジュアライゼーション
- パーティクル
- 3D空間
- カメラ移動
- モーションブラー
- 強弱のある静と動

などを組み合わせます。
ただし、すべてを同時に使う必要はありません。
テーマに最も合う表現を選択し、**情報量は多いが、視線誘導は明快** な映像にしてください。
テンプレート感のある企業PVではなく、デザイナーが意図を持って演出した作品にします。

# MOTION PRINCIPLES

すべての動きには意図を持たせてください。
**単純な fadeIn / fadeOut の連続は禁止です。**
基本的に以下を活用してください（括弧内は GSAP での主な実現手段）。

- overshoot（`back.out(2)`）
- anticipation（逆方向へ小さく引いてから `expo.out`）
- follow-through（子要素を数フレーム遅らせる / `elastic.out`）
- stagger（`stagger: { each, from: "center" | "edges" | "random" }`。random は `gsap.utils` ではなく seeded 配列で順序を固定）
- spring（`elastic.out(1, 0.4)`、または自作の減衰振動を proxy で計算）
- easing（`expo` / `power4` / `CustomEase` 相当の cubic を使い分け、`linear` は機械的な動き専用）
- scale transition
- masking / clipping（`clipPath` の `inset()` / `polygon()` を tween）
- motion blur（下記 RENDERING METHOD 参照）
- parallax
- camera movement（カメラ用ラッパー要素に `x/y/scale/rotationX/rotationY` と `transformPerspective`）
- rhythmic cuts

重要な動きは音楽の拍と同期させます。
「速い → 止まる → 爆発する」「密集 → 解放」「2D → 3D」
など、モーションにコントラストを作ってください。

# TECHNICAL STACK

映像は **HyperFrames** で実装してください。

- Node.js
- HyperFrames CLI（`npx hyperframes …`）
- GSAP 3（ページ内 `<script>`、paused timeline）
- HTML / CSS
- SVG
- Canvas 2D
- CSS 3D
- HyperFrames registry の `motion-blur` コンポーネント / render 時 `motionBlur` オプション

実装前に、以下のドメインスキルを **必ず読み込む**（記憶で代用しない）：

| タイミング | 読むもの |
|---|---|
| HTML を書く前 | `/hyperframes-core`（`references/minimal-composition.md`, `determinism-rules.md`, `composition-patterns.md`, 音声を置くなら `variables-and-media.md`） |
| モーションを書く前 | `/hyperframes-animation`（`rules-index.md` / `blueprints-index.md` から該当レシピ、`adapters/gsap*.md`、`techniques.md` の Canvas 節、`references/motion-blur.md`） |
| カメラ・3D・マスク・SVG モーフ | `/hyperframes-keyframes` |
| フォント選定 | `/hyperframes-creative` → `references/typography.md` |
| 名前のある見た目（glitch, grain, CRT, confetti 等）を作る前 | `npx hyperframes catalog --query "<look>" --json` で registry を検索（`/hyperframes-registry`） |
| check / snapshot / render | `/hyperframes-cli` |

フォントは HyperFrames が **事前バンドル** する家族（例：Archivo Black, League Gothic, Oswald, Montserrat, Space Mono, JetBrains Mono, IBM Plex Mono, Noto Sans JP）を優先します。それ以外を使う場合は `assets/fonts/` に woff2 を置いて `@font-face` で埋め込む（lint `font_family_without_font_face` を出さない）。

既存の HyperFrames プロジェクト（`hyperframes.json`）がある場合は、その構成・CLI バージョンピンを確認して活かします。

# ANIMATION ARCHITECTURE

After Effects のように大量の手動キーフレームを打つ設計ではなく、
**現在時刻を入力として、映像の状態を数式で決める** 設計にしてください。HyperFrames ではこれを 2 層で実現します。

**1. GSAP タイムライン（振り付け層）** — タイポ・UI・カメラなど「あるタイミングで何かが起きる」もの。

```js
const tl = gsap.timeline({ paused: true });
tl.fromTo("#title", { yPercent: 110 }, { yPercent: 0, duration: b(0.5), ease: "expo.out" }, b(4));
// …すべての tween を登録し終えてから最後に：
window.__timelines["main"] = tl;   // キーはルートの data-composition-id と一致
```

**2. 時刻 → 状態の純関数（生成層）** — パーティクル・グリッド・グラフ・ノイズなど連続的に変化するもの。
タイムライン全長にまたがる `ease: "none"` のプロキシ tween を 1 本置き、`onUpdate` で `render(t)` を呼ぶ。`render(t)` は **t だけから** 位置 / 色 / 不透明度 / カメラを計算する（前フレームの状態を持たない＝シーク安全）。

```js
const clock = { t: 0 };
tl.to(clock, { t: CFG.DURATION_SEC, duration: CFG.DURATION_SEC, ease: "none",
  onUpdate: () => render(clock.t) }, 0);
```

補助関数として `clamp`, `lerp`, `mapRange(t, a, b, c, d, ease)`（Remotion の `interpolate()` 相当）、`spring(t, {stiffness, damping})` の解析解、seeded PRNG（下記）を `lib.js` にまとめると、Remotion 版と同じ感覚で書けます。

HyperFrames の必須ルール（違反すると lint エラーまたは無言の不具合）：
- タイムラインは **ちょうど 1 本**、`paused: true`、**構築完了後に** 登録（`document.fonts.ready` 内で組むなら最後に代入）。
- `tl.play()` を呼ばない。`repeat: -1` 禁止（有限回に計算）。
- `.clip`（`data-start` を持つ要素）に `autoAlpha` / `visibility` / `display` を tween しない。中の子要素を動かす。
- 同じ要素・同じプロパティに CSS の初期 `transform` と GSAP tween を併用しない（`fromTo` で初期値を与える）。中央寄せは flex / `inset` で行い `translate(-50%,-50%)` を使わない。
- 変形させる要素は block 要素かつサイズ指定あり。本文に `<br>` を使わない（意図的な 1 語 1 行の見出しは可）。
- **`fromTo` の from 側だけに書いたプロパティ（例：`{opacity: 1, scale: 0}` → `{scale: 1}`）は、並列ワーカーの途中シークでは適用されず要素が消える**。snapshot では正しく見えても本番 render で欠落する。from に書いたプロパティは必ず to にも同じ値で書く（`{opacity: 1, scale: 0}` → `{opacity: 1, scale: 1}`）。
- 後続の `fromTo` は `immediateRender: false` を基本にし、初期状態は timeline 構築前の `gsap.set` で与える。
- 外部 `<script src>` はコンパイラによって DOM より前に巻き上げられることがある。DOM 生成・タイムライン構築は外部ファイル内で関数として定義し、`index.html` のインライン `<script>` で `DOMContentLoaded` 後に呼んで `window.__timelines["main"] = tl` を登録する（lint はインラインの登録しか検出しない）。
- **CSS は `index.html` のインライン `<style>` に書く**。外部 `<link rel="stylesheet">` に書いた `font-family` はコンパイラのフォント埋め込み対象にならず、snapshot では正しく見えても本番 render で代替フォントになる（render ログに `Injected deterministic @font-face` が出ているか確認する）。
- マスク内に隠しているだけのテキストも check の重なり監査に数えられる。出番以外は `autoAlpha: 0`（非 clip のラッパー）で消しておく。
- レンダー後は `ffmpeg -ss <t> -frames:v 1` で本番 MP4 から山場のフレームを抜き、snapshot と見比べる（snapshot と render で結果が違うことがある）。

# RENDERING METHOD

表現によって描画方式を使い分けてください。

**Typography / UI** — CSS transform を GSAP で
`x` / `y` / `xPercent` / `scale` / `rotation` / `skewX` / `clipPath` / `filter` / `letterSpacing`
文字分解は `/hyperframes-animation` → `adapters/animate-text.md` を参照。

**Lines / Graphs / Diagrams** — SVG
`path` / `strokeDasharray` / `strokeDashoffset`（長さは `getTotalLength()`）/ `mask` / `clipPath`。`rules/svg-path-draw.md`, `rules/stat-bars-and-fills.md` 等。

**3D** — 可能なものは CSS 3D で構築
`perspective` / `z` / `rotationX` / `rotationY` / `transform-style: preserve-3d`
→ トンネル、カード空間、タイポグラフィ空間。`rules/3d-camera-flight.md`, `rules/3d-text-depth-layers.md`, `blueprints/camera-journey.md` を参照。

**Particles** — Canvas 2D
大量のパーティクルは DOM 要素を大量生成せず、`<canvas>` 1 枚に `render(t)` から描画。数百〜数千個でも安定させる（`techniques.md` § Canvas 2D Procedural Art）。

**Motion blur** — スラム・ホイップ・スケールパンチなど「速く移動する 1〜3 拍」にだけ使う。
- 要素単位：registry の `motion-blur` コンポーネント（`data-hf-motion-blur`）。プレビューでも見える。
- フレーム全体（Canvas 含む）：render 時の `motionBlur` オプション。最終レンダー専用。
読む文字・ゆっくりした動き・フェードには掛けない（`references/motion-blur.md` の「Do not blur」表に従う）。

# AUDIO

可能であれば外部音源素材を使わず、Node.js で音を生成してください。
追加の音声生成 npm パッケージに依存しない構成を優先し、**Node.js 標準機能で PCM/WAV を書き出してください**（`scripts/generate-audio.mjs` → `assets/audio/score.wav`）。

Kick / Hi-hat / Click / Impact / Rise / Noise / Sub bass / UI beep などをプログラムで生成します。

- Kick：急激に周波数が下降するサイン波
- Hi-hat：高周波成分中心のノイズ
- Impact：低周波サイン波 + ノイズ + 短い減衰

必要に応じて複数レイヤーを重ねます。音のタイミングも同じ `BPM` / 拍番号から計算し、映像側の `b(n)` と **同一の拍テーブル**（例：`timeline.json` を生成スクリプトと HTML の双方から読む、または同じ定数を両方に記述）から導出します。

生成した WAV はコンポジションに `<audio>` で配置します：

```html
<audio id="score" src="assets/audio/score.wav" data-start="0" data-duration="15" data-track-index="10" data-volume="1"></audio>
```

- `<audio>` には **必ず `id`**（無いとミックスされず無音になる）。`crossorigin` 属性は付けない。
- `play()` / シークをコードから呼ばない（再生は HyperFrames が所有）。
- フェード・ダッキングは `data-automation` の volume レーン（`/hyperframes-audio`）。

ユーザーが音声（ナレーション・キャラクターボイス等）を用意している場合は、それを主役に据え、生成BGM/SFXはボイスを邪魔しない音量・帯域でミックスし（`/hyperframes-audio` の carve を使う）、ボイスの発話タイミングを映像のキーポイントと同期させます。

# BPM / FRAME SYNC

- 基本テンポ：**120 BPM**
- 動画：**60 FPS**
- つまり **1拍 = 0.5 秒 = 30フレーム**

主要なカット、タイトル出現、インパクト、カメラ切り替え、トランジションは可能な限り 1拍 / 半拍 / 1/4拍（デフォルトで 0.5 / 0.25 / 0.125 秒）単位に揃え、映像と音をフレームレベルで同期してください。
`DURATION_SEC` 秒の場合：**`DURATION_SEC × FPS` frames**（15秒なら900）。
（ボイス素材の長さに合わせて尺を変える場合も、拍グリッドは維持する。）
Studio で拍グリッドを確認したい場合は `npx hyperframes beats` を使える。

# VISUAL QUALITY

以下を避けてください。

- 安っぽい PowerPoint 風アニメーション
- ただ文字が左から右へ流れるだけ
- fadeIn の連続
- 意味のないグラデーション
- どこかで見た SaaS 広告テンプレート
- 過剰な角丸カード UI
- 全シーン同じ速度
- 小さすぎる文字（フルスクリーン視聴で見出し 60px+、本文 20px+。SNS フィード向けなら見出し 90px+）
- 画面中央に要素を置くだけの構図
- 余白を恐れた情報詰め込み
- テーマと関係のないエフェクト

代わりに、**Graphic Design × Typography × Motion × Code** として映像を設計してください。

# DESIGN SYSTEM

制作開始時にテーマから簡単なデザインシステムを定義し、`DESIGN.md` に書き出してください（HyperFrames の各スキルはこれをブランド真実として読む）。最低限、

- Main color
- Accent color
- Background color
- Typography
- Grid
- Shape language
- Motion language

を決めます。例：

```
Background: #050505
Primary: #F4F4F0
Accent: #D7FF00

Typography:
Archivo Black（display） / Space Mono（data）

Shape:
Grid / lines / circles

Motion:
Fast / mechanical / elastic

Camera:
Aggressive push-in + depth transition
```

色は CSS カスタムプロパティ（`:root { --bg; --fg; --accent; }`）として定義し、Canvas からも `getComputedStyle` ではなく同じ定数を JS 側 `CFG.colors` で参照する。
ただし、ユーザーのテーマ・素材（キャラクター画像の配色など）に合わせて毎回変更してください。

# TYPOGRAPHY

文字は「情報」ではなく「映像素材」として扱ってください。
巨大化 / 画面外へはみ出す / 分解 / マスク / 奥行き配置 / 文字間隔変化 / 反転 / 回転 / パース / スキャン / ストレッチ / クロップ
などを積極的に使用します。
一瞬しか表示されない小さな文章を大量に入れるより、**短く強い単語** を優先してください。
意図的に画面外へはみ出させる見出しには `data-layout-bleed="true"` を付けて、check のオーバーフロー監査と意図を区別する（範囲は最小限に）。

# TRANSITIONS

シーン間は単純なクロスフェードではなく、**前のシーンの要素を次のシーンへ変形させてください。**
例：文字 → ライン → グラフ → 3Dグリッド → トンネル → ロゴ
のように、**同じ形状を別の意味へ変換するトランジション** を優先します。
これにより動画全体に連続性を持たせてください。

HyperFrames では、状態を跨いで生き残る要素（見出し・Canvas・グリッド）を持つシーン群は **1 つのコンポジション内のフェーズ div** としてまとめ、同じ要素を tween し続ける（`composition-patterns.md` の internal phase divs）。ハードカットで切り替わるシーンだけをサブコンポジション化する。既製トランジションを使う場合は registry を先に検索。

# IMPLEMENTATION

動画を実際にレンダリング可能な HyperFrames プロジェクトとして実装してください。

```bash
npx hyperframes init "<project-dir>" --non-interactive --example=blank --skill=general-video
```

でスキャフォールドし、例えば以下の構成にします：

```
<project-dir>/
 ├─ hyperframes.json
 ├─ DESIGN.md
 ├─ index.html              ← ルート（data-composition-id="main", data-width/height/duration）
 ├─ compositions/           ← ハードカットのシーンだけサブコンポジション化（<template> で包む）
 │   ├─ intro.html
 │   ├─ build.html
 │   ├─ climax.html
 │   └─ outro.html
 ├─ src/
 │   ├─ config.js           ← CFG（FPS, BPM, DURATION_SEC, W, H, colors, beat table）
 │   ├─ lib.js              ← b(), mapRange, spring, seeded random
 │   └─ particles.js        ← render(t) で Canvas を描く純関数
 ├─ scripts/
 │   ├─ generate-audio.mjs  ← Node 標準のみで WAV 生成
 │   └─ sync-config.mjs     ← CFG → ルートの data-* 属性を同期
 └─ assets/
     ├─ audio/score.wav
     └─ fonts/
```

ただし、作品に適した構成へ自由に変更してください（短い単一シーンなら `index.html` 1 枚で良い）。
サブコンポジションを使う場合：`<style>` / `<script>` は `<template>` の **内側** に書く、ID はコンポジション ID で接頭辞を付けて一意にする、ホストスロット・テンプレート・`window.__timelines` のキーを同じ ID にする（`sub-compositions.md`）。

# PERFORMANCE

全フレーム（`TOTAL_FRAMES`）を Chrome から安定してレンダリングできることを重視してください。
無駄な DOM 生成を避け、大量要素は Canvas や SVG へ移します。
`Date.now()` / `performance.now()` / 実行時ネットワーク取得 / ホバー等の入力状態に依存しない。
ランダム値は `Math.random()` に依存せず、**再現可能な seeded random** を使います：

```js
function mulberry32(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const rand = (i, salt = 0) => mulberry32(i * 9973 + salt)();   // インデックスから決定的に
```

パーティクルの初期値は起動時に 1 回だけ配列へ生成し、`render(t)` は配列と t から位置を計算する（毎フレーム乱数を引かない）。

# FINAL RENDER

最終的に以下の動画を書き出せる状態にしてください（ユーザー指定があればそちらを優先。例：縦長なら 1080 × 1920 / 9:16）。

```
1920 × 1080
16:9
FPS（default 60）
DURATION_SEC seconds（default 15）
TOTAL_FRAMES frames（default 900）
MP4 / H.264
```

```bash
npx hyperframes render --fps 60 --quality draft    --output out/draft.mp4      # 反復確認
npx hyperframes render --fps 60 --quality delivery --output out/reel.mp4       # 最終
```

幅・高さ・尺を定数化し、別アスペクト比は `data-width` / `data-height` を差し替えた別ルート（または `sync-config.mjs` の引数）で出せる構造にしてください。

# WORKFLOW

まずユーザーのテーマ・素材を分析してください。その後、

1. コンセプト（コンセプトの切り口を 1 文で）
2. デザインシステム（`DESIGN.md`）
3. `DURATION_SEC` 秒のタイムライン（秒・拍・フレーム番号で記述。例：`b(8) = 4.0s = f240`）
4. モーション設計（各シーンが `/hyperframes-animation` のどの blueprint / rule を組み合わせるかを名前で明記）
5. サウンド設計
6. HyperFrames 実装（`init` → `DESIGN.md` → `generate-audio.mjs` → HTML/JS）
7. 検証：`npx hyperframes lint`（初回・構造変更後）→ 最終ゲート `npx hyperframes check`（lint / runtime / layout / motion / contrast が 0 findings になるまで修正）
8. `npx hyperframes snapshot --at <各シーンの山場の秒>` で静止画を書き出し、実際に画像を見て問題点を修正（文字切れ、空フレーム、コントラスト、拍ズレ）
9. レンダリング（`npx hyperframes render --fps 60 ...` で MP4 を実際に書き出す）
10. `ffprobe -v error -show_format -show_streams` で尺・fps・音声トラックを確認し、必要なら `ffmpeg` で数フレーム抜き出して最終確認

まで進めてください。
このスキル自体が意図（ブリーフ）を定義しているため、`/hyperframes` の intent interview は行わない。再開用に `BRIEF.md`（`workflow: general-video`, `flow: automation`, `storyboard: no`）を残すのは可。
途中で無難な案に収束させないでください。
ユーザーから細かい指定がなくても、モーションデザイナーとして判断して制作を進めてください。

# IMPORTANT

これは「HyperFrames の技術デモ」ではありません。技術は作品を成立させるために使用します。
視聴者が最初に感じるべきなのは、
「HTML でこんなことができるのか」ではなく、
**「この映像、めちゃくちゃかっこいい」** です。
その後で、「実は全部コードで生成されている」と分かるような作品を目指してください。

ユーザーのテーマを最大限に解釈して、**全尺、1フレームも無駄にしない映像** を制作してください。
