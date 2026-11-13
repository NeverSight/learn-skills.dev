---
name: apple-media
description: >
  AVFoundation / AVKit / PhotoKit リファレンス。
  AVPlayer, AVPlayerViewController, VideoPlayer, AVPlayerItem, AVMutableComposition,
  AVCaptureSession, AVCaptureDevice, AVCapturePhotoOutput,
  AVCaptureDeviceDirectionCoordinator, CameraCaptureAccessory (iPhone Duo),
  AVAudioEngine, AVAudioSession, AVAudioPlayer, AVSpeechSynthesizer,
  PHAsset, PHImageManager, PhotosPicker, PHPhotoLibrary。
user-invocable: false
---

## ディレクトリ構成

```text
skills/apple-media/
  SKILL.md
  references/
    avf-playback/
      README.md
      avplayer.md
      avqueueplayer.md
      avplayeritem.md
      avplayerlayer.md
      avplayerviewcontroller.md
      videoplayer.md
      avasset.md
      avurlasset.md
      avassettrack.md
      avplayeritemvideooutput.md
      avmutablecomposition.md
    avf-capture/
      README.md
      avcapturesession.md
      avcapturedevice.md
      avcapturedevice-discoverysession.md
      avcapturedeviceinput.md
      avcaptureoutput.md
      avcapturephotooutput.md
      avcapturephotosettings.md
      avcapturemoviefileoutput.md
      avcapturevideodataoutput.md
      avcapturevideopreviewlayer.md
      avcapturemetadataoutput.md
      avcapturedevicedirectioncoordinator.md
      camera-capture-accessory.md
    avf-audio/
      README.md
      avaudioplayer.md
      avaudiorecorder.md
      avaudioengine.md
      avaudiosession.md
      avaudioplayernode.md
      avaudiofile.md
      avaudiopcmbuffer.md
      avaudiomixernode.md
      avaudiouniteffect.md
      avspeechsynthesizer.md
      avspeechutterance.md
    photokit/
      README.md
      phphotolibrary.md
      phasset.md
      phassetcollection.md
      phfetchresult.md
      phfetchoptions.md
      phimagemanager.md
      phcachingimagemanager.md
      phassetchangerequest.md
      phphotolibrarychangeobserver.md
      phauthorizationstatus.md
      photospicker.md
      photospickeritem.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| 動画を再生したい（AVPlayer / VideoPlayer） | avf-playback | [references/avf-playback/README.md](references/avf-playback/README.md) |
| HLS / ストリーミング再生を実装したい | avf-playback | [references/avf-playback/README.md](references/avf-playback/README.md) |
| アセットのトラック・メタデータを取得したい | avf-playback | [references/avf-playback/README.md](references/avf-playback/README.md) |
| カスタム映像合成・コンポジションを作りたい | avf-playback | [references/avf-playback/README.md](references/avf-playback/README.md) |
| カメラで写真・動画を撮影したい | avf-capture | [references/avf-capture/README.md](references/avf-capture/README.md) |
| AVCaptureSession のセットアップをしたい | avf-capture | [references/avf-capture/README.md](references/avf-capture/README.md) |
| ライブプレビューを表示したい | avf-capture | [references/avf-capture/README.md](references/avf-capture/README.md) |
| QR コード・顔検出をリアルタイムで行いたい | avf-capture | [references/avf-capture/README.md](references/avf-capture/README.md) |
| iPhone Duo でカメラの向き（前面/背面）を追従してカメラを切り替えたい | avf-capture | [references/avf-capture/README.md](references/avf-capture/README.md) |
| iPhone Duo の外側ディスプレイに撮影用コンテンツ（台本など）を表示したい | avf-capture | [references/avf-capture/README.md](references/avf-capture/README.md) |
| 音声を再生・録音したい | avf-audio | [references/avf-audio/README.md](references/avf-audio/README.md) |
| AVAudioEngine でノードグラフを構築したい | avf-audio | [references/avf-audio/README.md](references/avf-audio/README.md) |
| AVAudioSession のカテゴリ・モードを設定したい | avf-audio | [references/avf-audio/README.md](references/avf-audio/README.md) |
| テキスト読み上げ（TTS）を実装したい | avf-audio | [references/avf-audio/README.md](references/avf-audio/README.md) |
| フォトライブラリへのアクセス許可を取得したい | photokit | [references/photokit/README.md](references/photokit/README.md) |
| PHAsset でアルバムや写真を取得・検索したい | photokit | [references/photokit/README.md](references/photokit/README.md) |
| PHImageManager でサムネイル・フル画像を取得したい | photokit | [references/photokit/README.md](references/photokit/README.md) |
| PhotosPicker（SwiftUI）を使いたい | photokit | [references/photokit/README.md](references/photokit/README.md) |
