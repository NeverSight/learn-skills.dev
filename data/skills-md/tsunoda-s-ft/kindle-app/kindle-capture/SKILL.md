---
name: kindle-capture
description: Kindle Web Reader/Kindle macOSアプリからスクリーンショットをキャプチャしてPDF生成。書籍名やASIN指定でKindle本を自動PDF化。Kindleライブラリ検索、Playwrightでページ自動取得、PNG画像からPDF変換、レイアウト設定（single/double）、範囲指定、品質調整、リサイズに対応。タイトル取得に失敗した場合は表紙キャプチャをAIで視認して命名する。
---

# Kindle Capture Skill

Kindle Web Readerから書籍のスクリーンショットを自動取得し、PDFを生成します。

## 概要

このSkillは、Amazon Kindle Web Reader（read.amazon.co.jp）とKindle macOSアプリの両方に対応します。WebはPlaywrightとKindleRenderer APIで自動キャプチャし、アプリはスクリーンショットで取得します。タイトル取得に失敗した場合は、表紙を1枚キャプチャしてAIが視認し、適切な書籍名で命名します。

## エージェント運用ルール（必読）

- ユーザーから指示がない限り、**すべてデフォルト設定で実行**する。不要な確認はしない。
- ローカルmacOSアプリで取得する場合、ユーザーが書籍タイトルを指定しなくても**AIが自動取得**する。
  - `capture_cover.py --json` → `view_image`で表紙タイトル確認 → 取得タイトルを `--book` に使用
- 取得に失敗・判別不能な場合のみ、最小限の確認を行う。
- **PDF生成前に、`src/dedupe_tail.py` で巻末末尾の重複ページを必ず検出・削除する**（末尾の連続ページで同一画像が続く場合は重複として除去する）。
- **PDF生成後は、親フォルダを日本語の書籍タイトル名にし、その直下にPDFと画像フォルダを配置してGoogle Driveへ必ず移動する**（`/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle`）。

## タイムアウトの目安

- 300ページ超の書籍は、一般的に約20分かかります。短いタイムアウト設定は避けてください。
- **エージェントはコマンド実行のタイムアウトを設定しない**（ツール側のtimeoutも指定しない）。完走まで待機する。
- 例外的に上限が必要な場合は、**ユーザー合意の上で**十分長い値（目安30分以上）を設定する。

## 前提条件

- **Google Chrome**: インストール済みで、Kindle Web Reader（https://read.amazon.co.jp）にログイン済みであること
- **ブラウザ自動化拡張機能**（オプション）: 書籍名での自動検索を行う場合に必要
  - 拡張機能未接続の場合は、ASINを手動で指定する必要があります
- **Python**: 3.10以降
- **依存パッケージ**: requirements.txtに記載のライブラリ
- **Kindle macOSアプリ（ローカル時）**: 書籍を開いた状態で前面にする
- **画面収録/アクセシビリティ許可（ローカル時）**: ターミナル（または実行元）に許可が必要

## セットアップ

```bash
cd /Users/tsunoda/Development/kindle-app

# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt

# 注意: このツールはシステムのGoogle Chromeを使用します
# Playwrightのブラウザインストールは不要です
```

## 基本的な使い方

**重要**: トリミングは必須ステップです。UIが映り込んでいても無視し、本体ページの四隅（紙面の外枠）に合わせてトリミングします。

### ステップ1: スクリーンショット取得

```bash
source venv/bin/activate
python src/capture.py --asin <ASIN> --layout double
```

書籍のASINコードを指定して、全ページのスクリーンショットを取得します。
デフォルトはログイン済みの既存プロファイルを使用します。Chrome起動中でプロファイルロックが発生した場合は、自動的に `~/Library/Application Support/Google/Chrome-Kindle` にフォールバックします（初回ログインが必要）。

### ステップ2: トリミング（必須）

```bash
# AIがサンプル画像（page_0001.png等）を確認してcrop_box値を決定
# UIは無視し、本体ページの外枠（四隅）を基準に計測する
# ここに数値の例は書かない（画像ごとに必ず計測する）
python src/trim.py --input ./kindle-captures/<ASIN>/ --crop "<left,top,right,bottom>"
```

キャプチャ画像のうち、本体ページの外枠（紙面）に合わせてトリミングします。AIは複数ページを確認して最適なcrop_box値を決定します。
詳細は「AIアシストトリミング ワークフロー」セクションを参照。

### ステップ3: 巻末末尾の重複削除（必須 / スクリプト使用）

PDF生成前に `src/dedupe_tail.py` を実行して末尾重複を削除します。

### ステップ4: PDF生成

```bash
source venv/bin/activate
python src/dedupe_tail.py --input ./kindle-captures/<ASIN>/trimmed/
python src/create_pdf.py --input ./kindle-captures/<ASIN>/trimmed/
```

### ステップ5: Google Driveへ移動（必須 / 親フォルダ=書籍タイトル）

```bash
mkdir -p "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>"
mv "<PDF_PATH>" "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>/<BOOK_TITLE>.pdf"
mv "./kindle-captures/<CAPTURE_DIR>/" "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>/画像_<RUN_ID>"
```

トリミング後の画像からPDFを生成します。**必ず `/trimmed/` ディレクトリを指定してください。**

## ローカル（Kindle macOSアプリ）

### 表紙1枚で命名（AI視認の標準フロー）

```bash
source venv/bin/activate
python src/capture_cover.py --json
```

1. `kindle-captures/<ASIN>/cover.png` を `view_image` で確認
2. 表紙のタイトルを読み取り、適切な書籍名で命名する
3. 必要なら出力ディレクトリ名と `metadata.json` の `book` を更新

**注意**: 表紙が表示されている状態で実行すること（現在表示中のページを撮影）。

### 全ページキャプチャ

```bash
source venv/bin/activate
python src/capture_app.py --book "<BOOK_TITLE>"
# 末尾の重複ページを削除してからPDF生成（スクリプト使用）
python src/dedupe_tail.py --input ./kindle-captures/<BOOK_TITLE>/
python src/create_pdf.py --input ./kindle-captures/<BOOK_TITLE>/
# PDF生成後にGoogle Driveへ移動（PDF+画像フォルダ）
mv "./<BOOK_TITLE>.pdf" "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>/<BOOK_TITLE>.pdf"
mv "./kindle-captures/<BOOK_TITLE>/" "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>/画像_<RUN_ID>"
```

## コマンドオプション

### capture.py - スクリーンショット取得

**必須オプション**:
- `--asin <ASIN>`: 書籍のASINコード（Amazon商品識別子）

**主要オプション**:
- `--chrome-profile <パス>`: Chromeプロファイルパス（デフォルト: `~/Library/Application Support/Google/Chrome`）
  - Chrome起動中でプロファイルロックが発生した場合は `~/Library/Application Support/Google/Chrome-Kindle` に自動フォールバック
- `--layout <single|double>`: レイアウトモード（デフォルト: double）
  - `single`: シングルページ表示
  - `double`: 見開き（ダブルページ）表示
- `--start <位置>`: キャプチャ開始位置（Kindleの位置番号）
- `--end <位置>`: キャプチャ終了位置（Kindleの位置番号）
- `--output <ディレクトリ>`: 出力先ディレクトリ（デフォルト: ./kindle-captures/{ASIN}/）
- `--headless`: ヘッドレスモードで実行（デフォルト: false）
- `--max-pages <数値>`: 取得ページ数の上限（デフォルト: 無制限）
- `--viewport-width <数値>`: ブラウザのviewport幅（デフォルト: 3840）
- `--viewport-height <数値>`: ブラウザのviewport高さ（デフォルト: 2160）

### create_pdf.py - PDF生成

**必須オプション**:
- `--input <ディレクトリ>`: スクリーンショットが保存されているディレクトリ

**主要オプション**:
- `--output <ファイル名>`: 出力PDFファイル名（デフォルト: {ASIN}.pdf）
- `--quality <1-100>`: JPEG品質（デフォルト: 85）
- `--resize <0.1-1.0>`: リサイズ比率（デフォルト: 1.0 = リサイズなし）

### capture_app.py - Kindle macOSアプリのスクリーンショット取得

**必須オプション**:
- `--book <タイトル>`: 書籍名/識別子

**主要オプション**:
- `--output <ディレクトリ>`: 出力先（デフォルト: `./kindle-captures/{book}`）
- `--max-pages <数値>`: 取得ページ上限
- `--region <x,y,w,h>`: キャプチャ領域指定
- `--scale <倍率>`: 座標スケール（Retinaなら2.0）
- `--wait <秒>`: ページ送り後の待機
- `--next-key <right|left|space|pagedown>`: ページ送りキー

### capture_cover.py - 表紙1枚キャプチャ

**主要オプション**:
- `--book <タイトル>`: 書籍名を直接指定（命名用）
- `--asin <ASIN>`: ASIN指定（タイトル取得の補助）
- `--online`: ローカルでタイトルが取れない場合にAmazonから補完
- `--json`: スクリプト連携向けJSON出力

## よくある使用パターン

### パターン1: 完全キャプチャ＆PDF生成（標準ワークフロー）

書籍全体をキャプチャしてPDF化する基本的なワークフローです。**トリミングは必須です。**

```bash
source venv/bin/activate

# 1. スクリーンショット取得
python src/capture.py --asin B0DSKPTJM5 --layout double

# 2. AIがサンプル画像を確認してcrop_box値を決定
# （AIエージェントがpage_0001.png等を読み、本体ページの外枠に合わせて判断）

# 3. トリミング実行（画像から測定した値を使用）
python src/trim.py --input ./kindle-captures/B0DSKPTJM5/ --crop "<left,top,right,bottom>"

# 4. AIがトリミング結果を複数ページで確認
# （本体外枠のバランス、コンテンツ切れがないか確認）

# 5. 巻末末尾の重複削除（トリミング後の画像で末尾重複を除去 / スクリプト使用）
python src/dedupe_tail.py --input ./kindle-captures/B0DSKPTJM5/trimmed/

# 6. PDF生成（トリミング後の画像から）
python src/create_pdf.py --input ./kindle-captures/B0DSKPTJM5/trimmed/

# 7. Google Driveへ移動（日本語ディレクトリ名・ファイル名）
mkdir -p "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>"
mv "./<BOOK_TITLE>.pdf" "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>/<BOOK_TITLE>.pdf"
mv "./kindle-captures/<BOOK_TITLE>/" "/Users/tsunoda/Library/CloudStorage/GoogleDrive-tsunoda799@gmail.com/マイドライブ/Kindle/<BOOK_TITLE>/画像_<RUN_ID>"
```

### パターン2: 部分キャプチャ（範囲指定）

特定の範囲のみをキャプチャする場合に使用します。**トリミングは必須です。**

```bash
source venv/bin/activate

# 1. 位置1000から5000までをキャプチャ
python src/capture.py --asin B0DSKPTJM5 --start 1000 --end 5000 --layout double

# 2. トリミング（画像から測定した値を使用）
python src/trim.py --input ./kindle-captures/B0DSKPTJM5/ --crop "<left,top,right,bottom>"

# 3. PDF生成
python src/create_pdf.py --input ./kindle-captures/B0DSKPTJM5/trimmed/
```

### パターン3: ページ数指定キャプチャ

指定したページ数だけキャプチャする場合に使用します。**トリミングは必須です。**

```bash
source venv/bin/activate

# 1. 最初の15ページをキャプチャ
python src/capture.py --asin B0DSKPTJM5 --max-pages 15 --layout double

# 2. トリミング（画像から測定した値を使用）
python src/trim.py --input ./kindle-captures/B0DSKPTJM5/ --crop "<left,top,right,bottom>"

# 3. PDF生成
python src/create_pdf.py --input ./kindle-captures/B0DSKPTJM5/trimmed/
```

### パターン4: モバイル最適化PDF

モバイルデバイス用にファイルサイズを最適化する場合に使用します。**トリミングは必須です。**

```bash
source venv/bin/activate

# 1. キャプチャ
python src/capture.py --asin B0DSKPTJM5 --layout double

# 2. トリミング（画像から測定した値を使用）
python src/trim.py --input ./kindle-captures/B0DSKPTJM5/ --crop "<left,top,right,bottom>"

# 3. リサイズ＆圧縮してPDF生成
python src/create_pdf.py --input ./kindle-captures/B0DSKPTJM5/trimmed/ --resize 0.7 --quality 80
```

## AIアシストトリミング ワークフロー

AIエージェントが視覚的にキャプチャ画像を確認し、最適なトリミング範囲を決定するワークフローです。

### ワークフロー概要

```
capture.py
    ↓
[AI: 中程から3-5ページ選択（例: 5,8,10,12）]
    ↓
mark.py --pages "5,8,10,12" --crop "..." (元画像にマーカー描画)
    ↓
[AI: マーカー付き画像を確認] → 位置調整が必要？ → crop値調整して mark.py 再実行
    ↓ 位置OK                          ↑ (2-3回繰り返し)
trim.py --crop "..." (全ページトリミング)
    ↓
create_pdf.py
```

**⚠️ 重要: マーカーで視覚的に位置を確認してからトリミングを実行します。**

- **mark.py で元画像にマーカーを描画**して位置を視覚的に確認
- マーカーが本体ページの四隅に合っているか確認
- 位置が決まったら trim.py で一発でトリミング実行

### サンプルページ選択ガイドライン

**原則**:
- 1-3ページ目は表紙・扉なので**避ける**（レイアウトが本文と異なる）
- 中程から3-5ページをサンプリング
- ページ総数の20%、50%、80%付近を目安に選ぶ

**例**:
- 15ページの場合: `--pages "5,8,10,12"`
- 50ページの場合: `--pages "10,20,30,40"`
- 100ページの場合: `--pages "20,40,60,80"`

### AIによるcrop_box決定ガイドライン

AIは以下の要素を確認してトリミング範囲を決定します：

1. **上部境界**: 本体ページ（紙面）の上端
2. **下部境界**: 本体ページ（紙面）の下端
3. **左右境界**: 本体ページ（紙面）の左右端
   - 見開きページの場合、左ページ外枠の左端と右ページ外枠の右端を揃える
   - 左右のバランスを確認（右側だけ外枠が削られやすい）
4. **UIは無視**: ヘッダー/Location/ナビ矢印などは判断材料にしない

**コマンド例（テンプレート）**:
```bash
python src/trim.py --input ./kindle-captures/<ASIN>/ --crop "<left,top,right,bottom>"
```

**注意**: 数値の例は記載しません。必ず対象画像を見て測定し、他書籍や過去の値を流用しないこと。

**判断手順**:
1. **複数ページを確認**（表紙、目次、本文2-3ページ）
2. 本体ページの外枠（紙面）を確認して上下面を決定
3. 見開きの場合、左右の外枠を揃えて決定
4. 本体外枠が切れていないかを確認
5. crop_box値を `"left,top,right,bottom"` 形式で決定（数値は画像から測定）

### トリミング結果の確認（最重要ステップ）

**⚠️ このステップが最も重要です。一発でOKになることは稀なので、厳しい目でチェックしてください。**

トリミング後、AIは**サンプルページ**を確認します（1ページだけで判断しない）：

**確認すべきページ（中程から3-5ページ）**:
- **本文ページ（中程）** - page_0005以降から3-5ページ
- 表紙や扉（page_0001-0003）はレイアウトが異なるため参考にしない
- 見開きページの余白バランスを重視

**確認チェックリスト**:
- [ ] **右側の余白**: 本体ページの右端に不要な余白が残っていないか **←最も見落としやすい**
- [ ] **下側の余白**: 本体ページの下端に不要な余白が残っていないか **←最も見落としやすい**
- [ ] **左側の余白**: 本体ページの左端に不要な余白が残っていないか
- [ ] **上側の余白**: 本体ページの上端に不要な余白が残っていないか
- [ ] **コンテンツ切れ**: 本文やイラストが切れていないか
- [ ] **左右バランス**: 見開きの左右ページの余白が均等か

**🔴 余白が少しでも残っている場合は、即座に再トリミングを実行してください。**

基準: 本体ページ（紙面）の端がトリミング後の画像の端にほぼ一致していること。グレーや白の余白が目立つ場合はNGです。

**⚠️ 重要な注意事項**:
- 1ページだけ確認して「OK」と判断しないこと
- 必ず複数ページを並列で読み取り、余白のバランスを確認する
- **ユーザーに「これでOKですか？」と聞く前に、自分で余白を厳しくチェックする**
- **2〜3回のトリミング反復を標準として想定する**
- 「まあこれくらいなら」と妥協しない

**再トリミングの手順**:
元画像は保持されているため、新しいcrop_box値で`trim.py`を再実行するだけでOKです。
```bash
# 例: 右側と下側の余白を詰める場合
# right値を小さく、bottom値を小さくして再実行
python src/trim.py --input ./kindle-captures/<ASIN>/ --crop "<left,top,新しいright,新しいbottom>"
```

### mark.py - トリミング位置プレビュー（マーカー描画）

元画像にトリミング位置を示すマーカー（赤い枠線とL字コーナー）を描画します。
**各ページにつき5つの画像を生成**：全体画像 + 4辺の拡大画像で、位置を精密に確認できます。

**生成される画像**:
- `{page}_marked.png`: 全体画像（マーカー付き）
- `{page}_top.png`: 上辺の拡大画像
- `{page}_bottom.png`: 下辺の拡大画像
- `{page}_left.png`: 左辺の拡大画像
- `{page}_right.png`: 右辺の拡大画像

**必須オプション**:
- `--input <ディレクトリ>`: 元画像ディレクトリ
- `--crop "left,top,right,bottom"`: マーカー位置（絶対座標）

**オプション**:
- `--pages "5,8,10,12"`: 指定ページのみマーカー描画
- `--output <ディレクトリ>`: 出力先（デフォルト: `{input}/marked/`）
- `--color <色>`: マーカーの色（デフォルト: red）
- `--width <数値>`: 線の太さ（デフォルト: 4）
- `--margin <数値>`: 拡大画像のマージン（デフォルト: 150px）

**マーカー→確認→トリミングの手順**:
```bash
# 1. サンプルページにマーカーを描画（5画像×ページ数 生成）
python src/mark.py --input ./kindle-captures/<ASIN>/ --crop "305,115,3280,1955" --pages "5,8,10,12"

# 2. 各辺の拡大画像と全体像を確認（5画像）
# - page_0005_top.png: 上辺のマーカー位置を確認
# - page_0005_bottom.png: 下辺のマーカー位置を確認
# - page_0005_left.png: 左辺のマーカー位置を確認
# - page_0005_right.png: 右辺のマーカー位置を確認
# - page_0005_marked.png: 全体画像で四隅のバランスを確認

# 3. 位置調整が必要なら crop値を変更して再実行
python src/mark.py --input ./kindle-captures/<ASIN>/ --crop "310,120,3270,1950" --pages "5,8,10,12"

# 4. 位置がOKなら全ページをトリミング
python src/trim.py --input ./kindle-captures/<ASIN>/ --crop "310,120,3270,1950"
```

### trim.py - 画像トリミング

**必須オプション**:
- `--input <ディレクトリ>`: 元画像ディレクトリ
- `--crop "left,top,right,bottom"`: トリミング範囲（絶対座標）

**オプション**:
- `--pages "5,8,10,12"`: 指定ページのみトリミング（省略時は全ページ）
- `--output <ディレクトリ>`: 出力先（デフォルト: `{input}/trimmed/`）
- `--note <テキスト>`: メタデータに記録するメモ

## ブラウザ自動化によるASIN検索

このスキルはブラウザ自動化ツールを使用してKindleライブラリから書籍を検索できます。使用するエージェントに応じて適切なツールを使用してください。

### 抽象的なフロー（全エージェント共通）

1. Kindleライブラリ（https://read.amazon.co.jp/kindle-library）にアクセス
2. ログイン状態を確認（未ログインならユーザーに依頼）
3. 検索バーにキーワードを入力
4. 検索結果から書籍を選択
5. URLからASINを抽出（例: `https://read.amazon.co.jp/?asin=B0DSKPTJM5`）
6. `source venv/bin/activate && python src/capture.py --asin <ASIN> --layout double` を実行
7. **【必須】マーカーでトリミング位置を決定**:
   - 中程から3-5ページ選択（例: 5,8,10,12）
   - `python src/mark.py --input ./kindle-captures/<ASIN>/ --crop "<値>" --pages "5,8,10,12"` でマーカー描画
   - マーカー付き画像（marked/ディレクトリ）を確認 → 位置調整が必要なら再実行（2-3回繰り返し）
8. **全ページトリミング**: 位置が決まったら `python src/trim.py --input ./kindle-captures/<ASIN>/ --crop "<値>"` で全ページトリミング
9. `source venv/bin/activate && python src/create_pdf.py --input ./kindle-captures/<ASIN>/trimmed/` を実行
10. 完了報告

### Claude Code

ブラウザ自動化ツール: `mcp__claude-in-chrome__*`

| 操作 | ツール |
|------|--------|
| タブ確認/作成 | `tabs_context_mcp`, `tabs_create_mcp` |
| ナビゲート | `navigate` |
| 要素検索 | `find` |
| フォーム入力 | `form_input` |
| クリック/操作 | `computer` |
| ページ読み取り | `read_page` |

**前提条件**: Claude in Chrome エクステンション（https://claude.ai/chrome）

**実装例**:
1. `mcp__claude-in-chrome__tabs_context_mcp` でブラウザ接続を確認
2. `mcp__claude-in-chrome__navigate` でKindleライブラリにアクセス
3. `mcp__claude-in-chrome__find` で検索バーを特定
4. `mcp__claude-in-chrome__form_input` でキーワードを入力
5. `mcp__claude-in-chrome__computer` で検索を実行
6. `mcp__claude-in-chrome__read_page` で検索結果を取得

### Codex CLI

ブラウザ自動化ツール: `mcp__chrome-devtools__*`

| 操作 | ツール |
|------|--------|
| 新規ページ | `new_page` |
| ナビゲート | `navigate_page` |
| スナップショット | `take_snapshot` |
| フォーム入力 | `fill` |
| キー入力 | `press_key` |
| クリック | `click` |
| スクリプト実行 | `evaluate_script` |

**実装例**:
1. `mcp__chrome-devtools__new_page` でKindleライブラリにアクセス
2. ログイン画面が表示されていれば、ユーザーにログインを依頼
3. `mcp__chrome-devtools__take_snapshot` で検索バーを特定
4. `mcp__chrome-devtools__fill` でキーワードを入力
5. `mcp__chrome-devtools__press_key`（Enter）で検索実行
6. `mcp__chrome-devtools__take_snapshot` で検索結果を取得

### 他のエージェント

上記に該当しないエージェントを使用している場合：

1. エージェントのブラウザ自動化ツールを確認
2. 「抽象的なフロー」に従って同等の操作を実行
3. ブラウザ自動化が利用できない場合は、ユーザーに手動でASINを確認してもらう

**手動確認の案内**:
1. ユーザーにKindleライブラリ（https://read.amazon.co.jp/kindle-library）へのアクセスを依頼
2. 検索バーでキーワード検索を実行してもらう
3. 該当書籍のURLまたはASINを教えてもらう
4. 提供されたASINでキャプチャを実行

### ASINの確認方法

- **Kindle Web Reader URL**: `https://read.amazon.co.jp/?asin=B0DSKPTJM5` → ASIN: `B0DSKPTJM5`
- **Amazon商品URL**: `https://www.amazon.co.jp/dp/B0DSKPTJM5/` → ASIN: `B0DSKPTJM5`（`/dp/`の後の英数字）

## ユーザーリクエストの解釈と対応

**「githubの本をPDF化して」（書籍名が曖昧な場合）**:
1. ブラウザ自動化ツールでKindleライブラリを検索
2. 複数の候補がある場合はリスト表示してユーザーに確認
3. 選択された書籍のASINでキャプチャを実行

**「アプリで（ローカルで）PDF化して」**:
1. Kindleアプリで対象書籍を前面表示
2. 書籍名が不明なら `python src/capture_cover.py --json` で表紙を取得
3. `view_image` で表紙を読み取り、適切な書籍名で命名
4. `python src/capture_app.py --book "<BOOK_TITLE>"` を実行
5. `python src/create_pdf.py --input ./kindle-captures/<BOOK_TITLE>/` を実行

**「この本の100ページ目から200ページ目までPDF化」**:
1. ページ番号とKindleの位置番号の違いを説明（必要に応じて）
2. `--start` と `--end` オプションで範囲指定

**「見開きでキャプチャして」**:
1. `--layout double` オプションを使用

**「モバイル用に軽量化してPDF化」**:
1. `--resize 0.7 --quality 80` オプションを使用

## トラブルシューティング

### ブラウザ自動化が利用できない

**症状**: ブラウザ自動化ツールが接続されていない

**対処法**:
1. 手動でKindleライブラリから書籍のASINを確認
2. `source venv/bin/activate && python src/capture.py --asin <ASIN>` で直接実行

### タイトルが取得できない（ローカル）

**対処法**:
1. `python src/capture_cover.py --json` を実行
2. `view_image` で `cover.png` を確認して書籍名を決める
3. `--book` にその書籍名を使って再実行

### セッション切れエラー

**症状**: `Session invalid. Please log in to Kindle in Chrome and retry.`

**原因**: Kindle Web Readerのログインセッションが切れている

**対処法**:
1. Google Chromeを開く
2. https://read.amazon.co.jp にアクセス
3. Amazonアカウントでログイン
4. スクリプトを再実行

### Chromeプロファイルがロックされているエラー

**症状**: `Failed to launch browser` または `Chrome profile is locked`

**原因**: 既にChromeが起動中で、デフォルトのプロファイルが使用されている

**対処法**（推奨）:
一時的なプロファイルを使用してプロファイル競合を回避します。この方法を使えば、通常のChromeを起動したままでもキャプチャできます。
```bash
source venv/bin/activate
python src/capture.py --asin <ASIN> --chrome-profile /tmp/kindle-test-profile
```

**補足**: 自動フォールバック後は初回ログインが必要です。

**代替対処法**:
1. 起動中のGoogle Chromeをすべて終了
2. スクリプトを再実行

### ページ読み込みタイムアウト

**症状**: キャプチャが途中で進まなくなる、または遅い

**原因**: ネットワーク速度が遅い、またはページ読み込み検知のタイムアウトが短すぎる

**対処法**:
1. ネットワーク接続を確認
2. `config.yaml` の `wait_timeout` を増やす（例: `3.0` → `5.0`）
3. スクリプトを再実行

```yaml
# config.yaml
capture:
  wait_timeout: 5.0  # 3.0から5.0に変更
```

### スクリーンショットが見つからないエラー

**症状**: `No screenshots found in {directory}`

**原因**: capture.pyを実行せずにcreate_pdf.pyを実行した、またはディレクトリパスが間違っている

**対処法**:
1. 先に `source venv/bin/activate && python src/capture.py --asin <ASIN>` を実行（フォールバック時は初回ログイン）
2. 正しい入力ディレクトリパスを指定（`--input ./kindle-captures/<ASIN>/`）

## 出力ファイル

### ディレクトリ構造

```
kindle-captures/
└── {ASIN}/
    ├── page_0001.png          # 元画像
    ├── page_0002.png
    ├── page_0003.png
    ├── ...
    ├── metadata.json          # キャプチャメタデータ
    ├── marked/                # マーカー付き画像（mark.py実行時）
    │   ├── page_0005_marked.png  # 全体画像
    │   ├── page_0005_top.png     # 上辺拡大
    │   ├── page_0005_bottom.png  # 下辺拡大
    │   ├── page_0005_left.png    # 左辺拡大
    │   ├── page_0005_right.png   # 右辺拡大
    │   └── ...
    └── trimmed/               # トリミング後（trim.py実行時）
        ├── page_0001.png
        ├── page_0002.png
        ├── ...
        └── trim_metadata.json # トリミング設定・履歴
```

### metadata.json

各キャプチャセッションの詳細情報を記録します：
- ASIN
- レイアウト設定（single/double）
- キャプチャページ数
- 位置範囲（最小・最大）
- 各ページの位置情報とタイムスタンプ

### 生成されるPDF

- **デフォルト**: カレントディレクトリに `{ASIN}.pdf`
- **カスタム**: `--output` オプションで指定したファイル名

## 注意事項

このツールは**私的利用のみ**を目的としています。以下の点を遵守してください：

- 日本の著作権法を遵守してください
- Amazon Kindleの利用規約に従ってください
- 商業利用や第三者への再配布は禁止されています
- 生成したPDFは個人的な利用のみに使用してください
- ページ数が多い書籍（300ページ超）はキャプチャ完了まで20〜30分かかることがあります。**外部タイムアウトは設定しない**（必要ならユーザー合意の上で長めに設定）。

## 技術情報

### 使用ライブラリ

- **Playwright**: ブラウザ自動化（Chrome制御）
- **img2pdf**: PNG→PDF変換（ロスレス圧縮）
- **Pillow**: 画像処理（リサイズ、JPEG変換）
- **PyYAML**: 設定ファイル管理
- **tqdm**: 進捗表示

### KindleRenderer API

Kindle Web ReaderのJavaScript APIを利用：
- `getMinimumPosition()` / `getMaximumPosition()`: 書籍の位置範囲取得
- `gotoPosition(position)`: 指定位置へ移動
- `hasNextScreen()`: 次ページの有無確認
- `nextScreen()`: 次ページへ移動

## 詳細情報

- **詳細なオプション説明**: [REFERENCE.md](REFERENCE.md) を参照
- **より多くの使用例**: [EXAMPLES.md](EXAMPLES.md) を参照
