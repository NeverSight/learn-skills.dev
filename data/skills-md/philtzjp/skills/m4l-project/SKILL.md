---
name: m4l-project
description: Max for Liveデバイス、`.maxpat` / `.amxd`、Max JS、MIDI/Audio I/O、Presentation UI、Ableton User Libraryへのインストール、リリース梱包を追加・変更するときに参照する。細分化されたM4L知識を実務向けに統合し、生成元・生成物・検証・Freeze/Export上の注意を一つの判断軸にまとめる。
---

# M4L Project

このスキルは、Max for LiveデバイスをLLMが作るときに必要な実務ルールだけを残した統合スキルである。網羅的なリファレンスではなく、壊れやすい判断を避けるためのチェックリストとして使う。

## 基本方針

1. MUST: 生成スクリプトを正本として扱う。`.maxpat` / `.amxd` は生成物であり、直接編集した場合も必ず生成スクリプトへ反映する。
2. MUST: デバイスごとに `packages/<device>/` を作り、少なくとも `devices/`, `scripts/`, `assets/`, `releases/`, `DESIGN.md`, `VERSION`, `LICENSE` の責務を分ける。
3. MUST: UI寸法、色、余白、表示ロジック、MIDI仕様、同期仕様を変えたら `packages/<device>/DESIGN.md` に記録する。
4. SHOULD: Max patcher JSONは構造化データとして扱い、文字列置換で編集しない。
5. NEVER: `.amxd` を `.maxpat` のリネームで作らない。
6. NEVER: 生成物だけを直して、生成元と乖離させない。

## Max for Live生成

1. MUST: MIDI Effectは `midiin` / `notein` から入力し、`midiout` / `noteout` へ出力する。
2. MUST: Audio Effect / Instrument / MIDI Effect のデバイスタイプを決めてから、I/Oと `.amxd` typeを合わせる。
3. MUST: MIDI Effectの `.amxd` は FOURCC `mmmm` と `project.amxdtype = 1835887981` を持つ。
4. MUST: `.maxpat` は `openinpresentation: 1` を持つ。
5. MUST: visible UI object は `presentation: 1` と整数 `presentation_rect` を持つ。
6. MUST: 全visible UI objectは `x + w <= devicewidth` かつ `y + h <= 169` を満たす。
7. SHOULD: 画像、JS、外部依存を使う `.amxd` は単体ロードできるように依存ファイルを同梱する。

## UI / Presentation

1. MUST: Max for Liveデバイスの高さは `169px` 固定として設計する。
2. MUST: UIを変更したら、Presentation boundsを機械的に検査する。
3. MUST: 背景panelを使う場合は、操作UIを覆わない重なり順にする。
4. SHOULD: `live.*` UIはLiveテーマとの整合性を優先し、必要以上に色を上書きしない。
5. SHOULD: 固定サイズの入力欄、アイコン、キャンバス、ロゴは安定した `presentation_rect` を持たせ、値変更でレイアウトが動かないようにする。

## JS / MIDIロジック

1. MUST: 表示上のドット判定と発音判定は同じ関数、または同じデータから導出する。
2. MUST: Note OnとNote Offの対応を崩さない。
3. MUST: 入力MIDIを使う仕様では、入力が無いときに勝手にフォールバック音を鳴らさない。
4. MUST: Randomの対象は仕様で明示された値だけに限定する。
5. MUST: 「ヒットした瞬間だけ鳴る」仕様では、同じヒット範囲内にいる間に再発音しないエッジ判定を入れる。
6. SHOULD: Max JSの関数名はMaxメッセージ名との対応が分かるようにする。
7. SHOULD: JS `Task` は低優先度イベントであることを前提にし、Freeze/Exportで厳密なMIDIタイミングが必要な処理には慎重に使う。

## Transport / Freeze / Export

1. MUST: Live API (`live.object`, `live.observer`, `LiveAPI`) を発音クロックとして使わない。Live APIは低優先度・非同期で、Freeze/Export中のタイミング源として信頼しない。
2. SHOULD: Transport同期が必要な場合は、Maxのtransport/tempo-relative clockなど、Live transportに同期するMax側の仕組みを使う。
3. MUST: 重い処理でscheduler tickが飛んだとき、過去イベントを現在時刻にまとめて発音するcatch-up実装にしない。遅れた過去音は捨てるか、明示した別モードにする。
4. MUST: 同じtransport位置・同じdegree・同じtickが複数回来ても、同じイベントを再発音しない。
5. SHOULD: Freeze/Exportで問題が出る場合は、JS内の発音スケジューリングよりもMax標準オブジェクト (`makenote`, `pipe`, `flush`, `midiformat` など) へ逃がすことを検討する。

## AMXD / Packaging

1. MUST: `.amxd` のバイナリ容器を書き出す場合は、生成後に最低限、期待する `.maxpat` / JS / 画像名が含まれていることを検査する。
2. MUST: 依存ファイルの `dependency_cache` は配布環境で解決できるパスにする。ローカル絶対パスへ依存させない。
3. MUST: リリース成果物には `VERSION`, `LICENSE`, `.amxd`, `.maxpat`, JS、参照画像を含める。
4. SHOULD: Ableton User Libraryへインストールする場合、古い同名ファイルを削除してから新しい `.amxd` をコピーする。
5. MUST: ユーザーへ最終報告するとき、既存Liveインスタンスの挿し直しが必要なら明記する。

## 検証

1. MUST: JS変更後は `node --check <device>.js` を実行する。
2. SHOULD: Python生成スクリプト変更後は `python3 -m py_compile <script>.py` を実行する。
3. SHOULD: 生成後に `.maxpat` のPresentation boundsとpatchline endpointを検査する。
4. SHOULD: `.amxd` 生成後に、デバイスタイプ、同梱依存、主要JS文字列が入っていることを検査する。
5. SHOULD: Liveでの挙動確認が必要な場合は、Max Console / Open Max Windowのエラー有無を確認する。

## 削減した旧スキルの扱い

旧構成では、overview、maxpat format、amxd conversion、presentation layout、live api、javascript、gen、debugging、py2maxを別skillに分けていた。しかし実作業では、必要な判断が分断され、Live APIをクロックに使うなど局所知識に引っ張られるリスクがあった。

今後はこの統合スキルを入口にし、詳細な公式ドキュメントや既存実装は必要になった時点で個別に確認する。
