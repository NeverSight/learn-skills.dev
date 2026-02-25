---
name: create-anime-lifehack
description: |
  TikTok/Shorts向けアニメ風ライフハック動画を一括生成するスキル。
  トピック指定だけで、3D Pixar風の擬人化キャラクターが解説する4シーン縦型動画を自動生成する。
  キーワード: ライフハック動画, TikTok動画, ショート動画, anime lifehack, アニメ風動画, lifehack video
compatibility: Requires ffmpeg, ffprobe, Node.js
metadata:
  author: yokurin
  version: "1.0"
---

# Anime Lifehack Video Generator

トピック指定だけで、3D Pixar風キャラクターによるライフハック解説ショート動画を一貫生成する。

## Prerequisites

**スキル実行の最初に必ず以下をすべて確認すること。1つでも不足があれば対処方法を提示して中断する。**

### 1. FAL_KEY の確認

```bash
echo "${FAL_KEY:+OK}" || true
```

- `OK` と表示されればセット済み
- 空の場合、ユーザーに以下を案内して **中断** する:
  1. [fal.ai](https://fal.ai) でAPIキーを取得
  2. `export FAL_KEY="your-key-here"` をシェルで実行、または `~/.zshrc` / `~/.bashrc` に追記

### 2. ffmpeg / ffprobe の確認

```bash
which ffmpeg && ffmpeg -version | head -1
which ffprobe
```

未インストール時: `brew install ffmpeg`（macOS）/ `sudo apt install ffmpeg`（Linux）

### 3. npm 依存関係のインストール

```bash
cd ~/.claude/skills/create-anime-lifehack && npm install
```

## Workflow

### Step 1: トピック受取 → 4シーン台本作成

ユーザーからトピック（例:「玉ねぎを切っても泣かない方法」）を受け取り、4シーン台本を作成する。

| シーン | 役割 | 内容 |
|--------|------|------|
| 1 | フック | 大きなリアクションで視聴者の注意を引く |
| 2 | 共感・問題提起 | 「実は簡単な方法がある」と期待感を煽る |
| 3 | 解決策 | 具体的なライフハック手順を説明 |
| 4 | 結果 | ドヤ顔や喜びで成功をアピール |

### Step 2: 台本承認

台本をユーザーに提示して承認を得る。修正リクエストがあれば反映。

### Step 3: 4シーン画像生成

`fal-ai/nano-banana-pro` で4シーン並行生成する。プロンプトテンプレートは `references/REFERENCE.md` を参照。

```bash
npx tsx ~/.claude/skills/create-anime-lifehack/scripts/fal.ts image "プロンプト" \
  --model "fal-ai/nano-banana-pro" \
  --aspect-ratio "9:16" \
  --resolution "2K" \
  --output "./assets/{topic-slug}/scene{N}.png"
```

**4シーンすべて並行生成すること。** 生成後、ユーザーに4枚を提示して承認を得る（コスト防止）。

### Step 4: 4シーン動画生成

承認された画像を Kling v3 Pro で動画化する。`generate_audio: true` でネイティブ音声を生成。プロンプトテンプレートは `references/REFERENCE.md` を参照。

```bash
npx tsx ~/.claude/skills/create-anime-lifehack/scripts/fal.ts subscribe \
  "fal-ai/kling-video/v3/pro/image-to-video" \
  '{
    "prompt": "{motion_and_voice_prompt}",
    "image_url": "{scene_image_url}",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": true
  }' \
  --output "./assets/{topic-slug}/scene{N}.mp4" \
  --logs
```

**4シーンすべて並行生成すること。**

### Step 5: シーン結合

```bash
bash ~/.claude/skills/create-anime-lifehack/scripts/combine-scenes.sh \
  "./assets/{topic-slug}/scene1.mp4" \
  "./assets/{topic-slug}/scene2.mp4" \
  "./assets/{topic-slug}/scene3.mp4" \
  "./assets/{topic-slug}/scene4.mp4" \
  "./assets/{topic-slug}/final.mp4" \
  0.5
```

完成したら最終動画のパス・ファイルサイズ・再生時間をユーザーに報告する。

## Rules

- 画像は `nano-banana-pro` 単一モデル（比較不要、バッチ効率優先）
- 画像承認後に動画生成（コスト防止）
- 出力先: `./assets/{topic-slug}/`
- 動画は縦型 9:16（1080x1920）
- Kling v3 Pro の `generate_audio: true` でネイティブ音声生成（TTSは使わない）
- 環境変数 `FAL_KEY` が必要
