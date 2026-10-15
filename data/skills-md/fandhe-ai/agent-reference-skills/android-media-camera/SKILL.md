---
name: android-media-camera
description: >
  Android アプリ開発 (Kotlin) の Media3 / CameraX リファレンス。androidx.media3, androidx.camera。
  ExoPlayer, MediaSession, MediaSessionService, MediaLibraryService, DRM,
  Compose UI (PlayerSurface), ProcessCameraProvider, CameraSelector,
  ImageCapture, ImageAnalysis, VideoCapture, CameraInfo, CameraX Extensions,
  Camera2 Interop。
user-invocable: false
---

# Android メディア再生・カメラリファレンス

Android の Media3 (再生・セッション) と CameraX (撮影) の公式ドキュメントを蒸留したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-media-camera/
  SKILL.md
  references/
    media3-playback/
      README.md
      ad-insertion.md
      analytics.md
      audio-attributes.md
      cast-player.md
      compose-ui.md
      customization.md
      data-source-cache.md
      downloading-media.md
      drm.md
      exoplayer.md
      live-streaming.md
      media-item.md
      media-metadata.md
      media-source.md
      playback-exception.md
      playback-parameters.md
      player.md
      player-listener.md
      player-view.md
      preload-manager.md
      retrieving-metadata.md
      timeline-tracks.md
      track-selection.md
    media-session-editing/
      README.md
      command-button.md
      composition-player.md
      composition.md
      edited-media-item.md
      media-browser.md
      media-button-receiver.md
      media-controller.md
      media-library-service.md
      media-notification-provider.md
      media-session-callback.md
      media-session-service.md
      media-session.md
      muxer-customization.md
      session-commands.md
      session-token.md
      tone-mapping.md
      transformer.md
    media3-inspector/
      README.md
      frame-extractor.md
      media-extractor-compat.md
      metadata-retriever.md
    mediarouter/
      README.md
      media-router.md
      media-route-button.md
      media-route-provider.md
      media-route-selector.md
      remote-playback-client.md
    camerax-usecases/
      README.md
      camera-permissions.md
      camera-controller.md
      camera-effect.md
      camera-compose-viewfinder.md
      camera-selector.md
      image-analysis.md
      image-capture.md
      mlkit-analyzer.md
      orientation-rotation.md
      preview.md
      preview-view.md
      process-camera-provider.md
      recording.md
      transform-output.md
      use-case-group-viewport.md
      video-capture.md
      zero-shutter-lag.md
    camerax-config/
      README.md
      camera2-interop.md
      camera-control.md
      camera-filter.md
      camera-info.md
      camera-state.md
      camera-extensions.md
      camerax-config.md
      concurrent-camera.md
      dynamic-range.md
      exposure-state.md
      focus-metering-action.md
      resolution-selector.md
      zoom-state.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Player / ExoPlayer で音声・動画を再生したい | media3-playback | [references/media3-playback/README.md](references/media3-playback/README.md) |
| MediaItem / MediaSource / DataSource でメディアソースを構築したい | media3-playback | [references/media3-playback/README.md](references/media3-playback/README.md) |
| TrackSelector / Timeline / Tracks でトラック選択・再生リスト構造を扱いたい | media3-playback | [references/media3-playback/README.md](references/media3-playback/README.md) |
| PlayerView / Compose UI で再生画面を組み立てたい | media3-playback | [references/media3-playback/README.md](references/media3-playback/README.md) |
| DRM 保護コンテンツを再生したい | media3-playback | [references/media3-playback/README.md](references/media3-playback/README.md) |
| DownloadManager / DownloadService でオフライン再生用にメディアをダウンロードしたい | media3-playback | [references/media3-playback/README.md](references/media3-playback/README.md) |
| MediaSession / MediaSessionService でバックグラウンド再生・外部連携をしたい | media-session-editing | [references/media-session-editing/README.md](references/media-session-editing/README.md) |
| MediaController / MediaBrowser でセッションに接続・操作したい | media-session-editing | [references/media-session-editing/README.md](references/media-session-editing/README.md) |
| メディア通知 (MediaNotification.Provider) をカスタマイズしたい | media-session-editing | [references/media-session-editing/README.md](references/media-session-editing/README.md) |
| Transformer でメディアの編集・トランスコードをしたい | media-session-editing | [references/media-session-editing/README.md](references/media-session-editing/README.md) |
| 再生せずに MediaItem のメタデータ・解像度・コーデックを取得したい | media3-inspector | [references/media3-inspector/README.md](references/media3-inspector/README.md) |
| サムネイル・フレーム抽出や MediaExtractor 互換のデマルチプレクスをしたい | media3-inspector | [references/media3-inspector/README.md](references/media3-inspector/README.md) |
| 外部出力デバイス・出力先ルートの検出・選択をしたい | mediarouter | [references/mediarouter/README.md](references/mediarouter/README.md) |
| MediaRouteButton でルート選択 UI を表示したい | mediarouter | [references/mediarouter/README.md](references/mediarouter/README.md) |
| カスタム MediaRouteProvider の公開やリモート再生コマンド送信をしたい | mediarouter | [references/mediarouter/README.md](references/mediarouter/README.md) |
| ProcessCameraProvider / Preview / ImageCapture でカメラプレビュー・撮影を実装したい | camerax-usecases | [references/camerax-usecases/README.md](references/camerax-usecases/README.md) |
| ImageAnalysis / VideoCapture でフレーム解析・動画録画をしたい | camerax-usecases | [references/camerax-usecases/README.md](references/camerax-usecases/README.md) |
| CameraController で高レベル API を使いたい | camerax-usecases | [references/camerax-usecases/README.md](references/camerax-usecases/README.md) |
| CameraControl / CameraInfo でズーム・フォーカス・露出を制御したい | camerax-config | [references/camerax-config/README.md](references/camerax-config/README.md) |
| CameraX Extensions / Camera2 Interop / ConcurrentCamera を使いたい | camerax-config | [references/camerax-config/README.md](references/camerax-config/README.md) |

フォアグラウンドサービスの実装は `android-background-work`、通知の一般的な扱いは `android-platform-core`、撮影データの保存先（MediaStore/ストレージ）は `android-data` を参照。
