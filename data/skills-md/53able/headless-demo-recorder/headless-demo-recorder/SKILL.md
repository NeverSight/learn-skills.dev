---
name: headless-demo-recorder
description: ブラウザや macOS アプリをヘッドレスで操作しながら録画し、ズーム・マーカー・字幕・ぼかしを付けた MP4/GIF のデモ動画を人手を介さずに作る。録画を開いたまま画面を観察して次の操作を1手ずつ決めることも、複数のエージェントがそれぞれの録画を同時に操作して1本に結合することも、録画済みの動画に後から編集を足すこともできる。Use when the user asks for a demo, walkthrough, or screen-recording video of a web page or a macOS app, wants agents to operate apps while being recorded, or wants zoom/captions/blur added to an existing screen recording. Don't use for live screen sharing, manual GUI video editing, physical mouse/drag input, or recording outside macOS.
---

# headless-demo-recorder

「Xのサインアップを20秒で見せるデモを作って」といった依頼を、人がエディタを触らずに MP4/GIF まで仕上げる。各コマンドは stdout に JSON を1つだけ出力する。

## 前提（Codex / Claude Code 共通）

- コマンドは `bun <skill-dir>/scripts/cli.ts <command>` で呼ぶ。`<skill-dir>` は、Claude Code / Codex がこのスキルを読み込むときに示す base directory（この SKILL.md があるディレクトリ）を指す。
- base directory が示されなければ、次の順に `scripts/cli.ts` があるディレクトリを `<skill-dir>` とする。プロジェクトへの導入（`npx skills add`）では `.claude/skills/headless-demo-recorder`、`.agents/skills/headless-demo-recorder`。ユーザー全体への導入（`npx skills add -g`）では `~/.claude/skills/headless-demo-recorder`、`~/.agents/skills/headless-demo-recorder`。
- どこにも無い、または `bun` が無い場合は止めて、利用者に導入を案内する（`npx skills add 53able/headless-demo-recorder -g -a claude-code -a codex`、bun は別途導入）。コマンドやフラグが `unknown command` になるなど、スキルが古いと思われる場合は `npx skills update headless-demo-recorder` を案内する。スキルの導入と更新は利用者が行う。
- シナリオと出力は、いま作業しているプロジェクトに置く（例: `scenarios/<name>.json`、`out/<name>.mp4`）。シナリオ内のパス（`output.path`、file ソースの `path`、composition の `scenarios[]`）は実行時のカレントディレクトリからの相対で解決される。録画には画面がそのまま入るので、出力先が `.gitignore` に入っていなければ利用者に伝える。
- 入力 JSON の形式は `<skill-dir>/scripts/types.ts`、例のシナリオは `<skill-dir>/assets/*.json` にある。`schema` を実行すると、型定義の全文、この文書のパス（`guide`）、依頼に応じて読む手順書のパス（`references`）、例のパス（`examples`）を1つの JSON で返す。返るパスは symlink を解決した実体のパスであり、`<skill-dir>` の表記と一致しないことがある。
- 同梱の example は、このスキルの開発リポジトリのルートを cwd にした雛形。導入先ではそのまま `check` / `run` せず、作業中のプロジェクトに写して書き換える（特に composition の `scenarios[]` のパスと、desktop の `target` の `name`。ボタン名などはアプリの表示言語で変わるので、下見で得た名前に置き換える）。
- `scripts/` の `*.test.ts` はスキルの開発用で、使うときは実行しない。導入先（`.agents/skills/` などドットで始まるディレクトリ）は、利用者のプロジェクトの `bun test` の探索対象に入らない。
- macOS の画面収録とアクセシビリティの権限は、エージェントを動かしているターミナルアプリに付与されている必要がある。付与は利用者が行う。
- Codex のサンドボックス（`workspace-write`）では、`check`・`plan`・`inspect`・`schema` 以外のコマンド（`doctor`、`render`、`run`、`capture`、`session`、下見の `agent-browser` / `agent-desktop`）を**最初から**サンドボックス外で実行する許可を求める。理由と、サンドボックス内で実行したときの症状は `references/codex-sandbox.md` にある。
- 録画中の進み具合（録画の開始、各手の番号・経過時間・字幕、失敗した手、停止）は stderr に出る。`session` では録画を持つプロセスのログ `<project-dir>/session/server.log` に出る。`fill` の入力値は出さない。
- `inspectSheet` は PNG 画像。画像を読めるツール（Claude Code の Read、Codex の view_image など）で開いて確認する。

## コマンドとリスク

| コマンド | リスク | 効果 |
|---|---|---|
| `doctor` | R0 | 読み取りのみ。ツール、バージョン、OS権限を確認する |
| `schema` | R0 | 入力 JSON の型定義、この文書、`references/` の手順書、例のシナリオの場所を返す |
| `check <scenario>` | R0 | シナリオを検証する。何も起動しない |
| `plan <project-dir> [--scenario s] [--edit e]` | R0 | `render` が書き込む編集領域を表示する |
| `inspect <project-dir> [--video f]` | R0 | アクションごとに1コマ並べたコンタクトシートを作る。`--video` を省くと元の録画（`capture.mp4`）を使い、字幕もマーカーも映らない |
| `render <project-dir> [--scenario s] [--edit e] [--out f]` | R1 | プロジェクトと出力ファイルを再生成する。`--edit` を渡すと `--scenario` の `edit` の代わりにそれを使う。既存の出力は `--force` がない限り上書きしない |
| `capture <scenario>` | R2 | アプリまたはページを起動・操作し、録画する |
| `run <scenario>` | R2 | check → capture → render → inspect を順に実行する |
| `session start <scenario> [--group g] [--idle-timeout 秒] [--allow-origin o] [--allow-app id]` | R2 | 録画を開始して開いたままにする（browser / desktop）。シナリオの `steps` があれば先に実行する |
| `session observe <project-dir> [--screenshot]` | R0 | 録画中の画面のアクセシビリティスナップショット（`act` で使える参照付き）を返す。`--screenshot` で PNG も保存する |
| `session act <project-dir> '<step JSON>'` | R2 | 1手だけ実行する。シナリオの手と同じ検証（不可逆な操作、`--allow-origin`）を通る |
| `session status <project-dir>` | R0 | 状態（`recording` / `stopping` / `stopped` / `failed`。録画プロセスが落ちていれば `recorder exited`）、経過時間、記録した操作数を返す |
| `session stop <project-dir>` | R1 | 録画を止め、通常のプロジェクト（`capture.mp4`、`events.json`）として保存する |

共通のフラグ: `--force`（既存の録画・出力を上書きする）、`--keep-work`（録画の中間ファイルを残す）、`--session-name <name>`（使う agent-browser のセッション名。composition では `<name>-<シナリオ名>`）。

## 作業ループ

0. **依頼の形を決め、該当する手順書を読む。** 該当しなければ読まずに1へ進む。
   - 手順を事前に決め切れない（画面を見て次の操作を決める、複数のエージェントで同時に録る）: `references/session.md`
   - 録画済みの動画に編集を足す（file ソース）: `references/file-source.md`
   - 2本の録画を1本に並べる・つなぐ（composition）: `references/composition.md`
1. `doctor` を実行する（Codex ではサンドボックス外で）。`ok:false` の項目があれば止めて、その `fix` を利用者に伝える。browser / desktop を録画する場合、権限が `granted` でなければ止めて、利用者に付与を依頼する。OS の設定やツールの導入を自分で行わない。file ソースだけを扱う場合、権限の項目は不要で、ツールの項目（ffmpeg、ffprobe、openscreen、openscreen CLI）が ok なら続けてよい。
2. **録画せずに下見する。** 先に、安定して指せる操作対象を見つける（file ソースでは不要）。
   - ブラウザ:
     1. `agent-browser --session explore open <url>` を実行し、続けて `agent-browser --session explore snapshot -i` を実行する。
     2. 対象は CSS・id・テキストのセレクタで指定する。`@eN` 参照は録画用のセッションに引き継がれず、`check` でも拒否される。
     3. 終わったら `agent-browser --session explore close` を実行する。
   - デスクトップ:
     1. 最初に一度だけ `agent-desktop skills get desktop` を実行する。
     2. `agent-desktop launch <App>` を実行し、続けて `agent-desktop snapshot --app <ローカライズ名> -i --compact` を実行する。ローカライズ名は `launch` の結果から取る（例: `Calculator` → `計算機`）。
     3. 対象は `find` のクエリで指定する（例: `{ "role": "button", "name": "7", "exact": true }`）。
3. `scenarios/<name>.json` を書く（形式は `scripts/types.ts` の `Scenario`。例は `assets/` のファイル）。字幕には「何をクリックしたか」ではなく「なぜそうするのか」を書く。秘密情報の入力欄には `"redact": true` を付ける。`check` が `ok:true` を返すまで直す。
4. `run scenarios/<name>.json` を実行する。
5. **`inspectSheet` を開いて目で確認する。** 書き出しに成功しても、動画の中身が正しいとは限らない。各コマについて、次の4点を確かめる。
   - 操作した要素が映っている。
   - 操作した要素にマーカーが重なっている。
   - 字幕が読める。
   - 個人情報が映っていない。
   - `inspect` の `timelineEdited` が `true` なら、書き出しにトリムか早送りがある。コマの時刻は、`render` が `render.json` に残した区間を通して書き出しの時刻に換算してある。`note` が「approximate」を含むときは、`render` をやり直してから `inspect` する。
6. 修正は再録画せずに行う。`events.json`（タイミング、字幕、座標）またはシナリオの `edit` を直し、`render <project-dir> --scenario <file> --force` で再生成してから、もう一度 `inspect` する。

## 操作の種類

`steps` と `session act` の手は同じ形式で、`scripts/types.ts` の `Step` に従う。

- `click` / `fill` / `select`（ドロップダウンやリストから `value` を選ぶ）は `target` を取る。
- `scroll`:
  - ブラウザではページ全体を `px` だけ動かす。`target` は付けない。
  - デスクトップでは `target` の要素を `max(1, round(px / 100))` 単位だけ動かす。`target` は必須で、`direction` は `up` / `down` / `left` / `right` を使う。
    - WebView のアプリ（Tauri / Pake / Electron など）では、`{ "role": "scrollarea" }` のような role だけのクエリが、ページ内の多数の要素に当たって失敗しやすい。`session observe` で得たスクロール領域の参照を使う。
    - WebKit のなめらかなスクロールは、操作の 350ms 後には終わっていないことがある。`inspectSheet` のスクロールのコマが途中の位置を映していても、録画の後半で行き着いているかを確かめる。
- `press`（キー）、`wait`（ミリ秒）、`mark`（字幕だけ）はどちらでも使える。`open`（URL を開く）はブラウザ専用。
- ドラッグ、ホバー、座標指定のクリックは扱わない。agent-desktop ではこれらが `--headed`（物理入力）を要するため。
- 1つの録画は1つのウィンドウ（desktop）または1つのページ（browser）だけを映す。複数のアプリを1本に入れるときは、アプリごとに録画して composition で並べる。
- browser で新しいタブを開く手（`target="_blank"` のリンクなど）は録画されない。そのような手は、開いたタブを閉じて録画中のタブに戻したうえで、`NEW_TAB` を含むエラーで失敗する。遷移先は `open` で同じタブに開く。
  - `--allow-origin` を指定していると、agent-browser 0.41.1 は新しいタブを開くクリックに応答を返さず、ページが `about:blank` になる（実測）。この状態からは戻せない。新しいタブを開くリンクは押さず、遷移先の URL を `open` で開く。セッションでこうなった場合は `session stop` して始め直す。

## マーカーとカーソル

- 既定では合成カーソルは描かない。操作した要素に約 1.2 秒、黄色のリングを動画へ焼き込む（`render` が `capture.marked.mp4` を作る）。動画ごとズームされるので、リングは要素に重なったまま動く。対象は `point` を持つ `click` / `type` で、`fill` は `type`、`select` は `click` として記録される。
- マーカーを付けないもの: `press` / `scroll` / `mark`、`redact: true` のイベント（クリックも入力も）、`point` の無いイベント、画面の 1/4 を超える面積の要素。
- step の `zoom: false` はマーカーを止めない。マーカーを止めるのは `edit.marker: false`。
- `edit.syntheticCursor: true` を明示したときだけ、従来どおり合成カーソルを描く。クリックの瞬間が実際の UI の反応と数百 ms ずれることがある。
- composition では、マーカーの有無は各録画の `{...scenario.edit, ...composition.edit}` で決まる。カーソルは `composition.edit.syntheticCursor` だけで決まる。

## 失敗時の対応: まず `retry` を読む

Codex で `doctor` の権限項目が `Operation not permitted`、または `render` が空のメッセージの `PROJECT_INVALID` になったら、まずサンドボックス内で実行していないかを疑う（`references/codex-sandbox.md`）。

`agent-desktop` が `PERM_DENIED Accessibility surface read failed for AXFrontmost` を返すのは、`doctor` の権限が `granted` でも起きる。アプリを絞らずに呼ぶと、無関係なアプリ1つの読み取り失敗で全体が失敗するため。下見で `agent-desktop` を直接呼ぶときは、`snapshot` / `find` / `list-windows` に必ず `--app <ローカライズ名>` を付ける。権限の付与を利用者に求めない。

- `safe`: 何も起きていない。そのまま再実行してよい。
- `after-fix`: `hint` が示す箇所を直してから再実行する。`render` 段階で失敗した場合は録画が残っているので、`artifacts.retryWith` のコマンドで書き出しだけをやり直せる。
- `no`: 実アプリまたはページでステップが途中まで実行されている（録画中の `TARGET_NOT_FOUND` など）。次の順で対応し、再試行を繰り返さない。
  1. アプリの状態を確認し、元に戻す。
  2. 失敗したステップの画面をもう一度下見する。
  3. ここまで済んでから `capture --force` を実行する。

## ガードレール

- `check` は、対象の名前が不可逆な操作に見えるステップを拒否する（delete、send、purchase、削除、送信など）。
  - 確認したうえで無害なステップ（計算機の「すべて消去」など）は、**そのステップに** `"allowDestructive": true` を付ける。
  - シナリオ全体に付ける `allowDestructive` は、実際にその操作を行うデモに限る。必ず利用者の承認を得てから使う。
  - 判定は単語リストによる推定にすぎない。`check` を通過しても、そのステップが安全だとは保証されない。
- agent-desktop はヘッドレスで動く。利用者が物理入力を許可しない限り、`--headed` を付けない。
- デスクトップ録画は実際のウィンドウを録る。上に重なった通知も映り込む。
- `openscreen` をサブコマンドなし、または `--version` 付きで実行しない。GUI が起動する。`doctor` は `openscreen help` を使う。
- `openscreen export --auto-zoom` は、ヘッドレス実行では効かない。ズームは操作ログから生成する。
- `session act` でも不可逆な操作の検証は変わらない。拒否された手は実行しない。`allowDestructive` を手に付けるのは、無害だと確かめた場合に限る。
  - 検証は語リストによる推定で、見るのは参照の名前（観察時点）か、セレクタ・クエリに書いた文字列だけ。観察のあとに画面が自分で書き換わった場合や、`select` で option の value 属性（表示名と異なる）を指定した場合は検出できない。
