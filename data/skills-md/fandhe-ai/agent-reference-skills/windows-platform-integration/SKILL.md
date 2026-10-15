---
name: windows-platform-integration
description: >
  Windows アプリ開発 (Windows App SDK / WinRT) の OS 統合 API リファレンス。
  DeviceInformation, DeviceWatcher, センサー (Accelerometer, Gyrometer, Compass,
  OrientationSensor, Pedometer, ActivitySensor), Bluetooth LE, USB, Serial, HID,
  Battery, HttpClient, StreamSocket, WebSocket, BackgroundDownloader/Uploader,
  NetworkInformation, PointerInput, KeyboardInput, FocusManager, DragAndDrop,
  IME/TextInput, Calendar, DateTimeFormatter, CurrencyFormatter, ResourceLoader
  (多言語化・地域化), PasswordVault, CryptographicBuffer, WindowsHello/Passkeys,
  WebAuthenticationBroker, Clipboard, DataTransferManager, Launcher, JumpList,
  TaskbarManager, SecondaryTile, StartupTask, ProtocolActivation。
user-invocable: false
---

# Windows Platform Integration リファレンス

Windows App SDK / WinRT が提供する OS 統合 API 群の公式ドキュメントを蒸留したリファレンス。
デバイス・センサー、ネットワーク通信、入力処理、地域化・多言語対応、セキュリティ・ID 管理、
シェル連携（クリップボード・共有・タスクバー・タイル等）を扱う。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-platform-integration/
  SKILL.md
  references/
    devices-sensors/
      README.md
      device-information.md
      device-watcher.md
      accelerometer.md
      gyrometer.md
      compass.md
      inclinometer.md
      light-sensor.md
      orientation-sensor.md
      simple-orientation-sensor.md
      pedometer.md
      proximity-sensor.md
      activity-sensor.md
      altimeter.md
      barometer.md
      bluetooth-le-device.md
      gatt-device-service.md
      bluetooth-le-advertisement-watcher.md
      bluetooth-rfcomm.md
      device-pairing.md
      gatt-server.md
      usb-device.md
      serial-device.md
      hid-device.md
      battery.md
      power-manager.md
      printing.md
      image-scanner.md
      point-of-service.md
      wifi-and-radios.md
      lamp-array.md
      device-capabilities-manifest.md
    networking/
      README.md
      http-client.md
      http-request-message.md
      http-response-message.md
      http-base-protocol-filter.md
      http-cookie-manager.md
      windows-vs-dotnet-http.md
      stream-socket.md
      stream-socket-listener.md
      datagram-socket.md
      message-web-socket.md
      stream-web-socket.md
      background-downloader.md
      background-uploader.md
      download-operation.md
      network-information.md
      connection-profile.md
      proximity.md
      dnssd.md
      syndication.md
      network-capabilities.md
      loopback-exemption.md
    input/
      README.md
      pointer-input.md
      keyboard-input.md
      keyboard-accelerators.md
      access-keys.md
      focus-manager.md
      xy-focus.md
      tab-navigation.md
      gesture-recognizer.md
      haptic-feedback.md
      input-activation-listener.md
      input-pointer-source.md
      input-keyboard-source.md
      input-pane.md
      pen-and-ink.md
      drag-and-drop.md
      text-input-ime.md
    globalization/
      README.md
      application-languages.md
      language.md
      calendar.md
      geographic-region.md
      clock-identifiers.md
      currency-identifiers.md
      decimal-formatter.md
      currency-formatter.md
      percent-formatter.md
      numeral-system.md
      date-time-formatter.md
      resource-loader-resw.md
      resource-qualifiers.md
      bidirectional-text.md
      package-manifest-languages.md
      multilingual-app-toolkit.md
    security-identity/
      README.md
      password-vault.md
      password-credential.md
      key-credential-manager.md
      key-credential.md
      user-consent-verifier.md
      user-consent-verification-result.md
      web-authentication-broker.md
      web-authentication-core-manager.md
      web-account-provider.md
      cryptographic-buffer.md
      hash-algorithm-provider.md
      symmetric-key-algorithm-provider.md
      asymmetric-key-algorithm-provider.md
      data-protection-provider.md
      certificate.md
      certificate-enrollment-manager.md
      smart-cards.md
      windows-hello-passkeys.md
      app-capabilities.md
      appcontainer.md
    windows-integration/
      README.md
      clipboard.md
      data-package.md
      data-package-view.md
      data-transfer-manager.md
      share-sheet-send.md
      share-sheet-receive.md
      share-sheet-contacts.md
      default-apps-platform.md
      protocol-file-association.md
      protocol-activation.md
      launcher.md
      cross-device-people-api.md
      cross-device-resume-overview.md
      connected-experiences-overview.md
      jump-list.md
      taskbar-manager.md
      pin-to-taskbar.md
      secondary-tile.md
      start-screen-manager.md
      startup-task.md
      app-diagnostic-info.md
      app-actions-search.md
      context-menu-extensions.md
      recall.md
      search-providers.md
      widget-providers.md
      feed-providers.md
      microsoft-copilot-key-provider.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| USB / Bluetooth LE / Serial / HID デバイスを列挙・接続したい | devices-sensors | [references/devices-sensors/README.md](references/devices-sensors/README.md) |
| Accelerometer / Gyrometer / Compass / OrientationSensor でセンサー値を取得したい | devices-sensors | [references/devices-sensors/README.md](references/devices-sensors/README.md) |
| Battery / PowerManager で電源状態を監視したい | devices-sensors | [references/devices-sensors/README.md](references/devices-sensors/README.md) |
| HttpClient / WebSocket で HTTP・双方向通信を実装したい | networking | [references/networking/README.md](references/networking/README.md) |
| StreamSocket / DatagramSocket で TCP/UDP 通信を実装したい | networking | [references/networking/README.md](references/networking/README.md) |
| BackgroundDownloader / BackgroundUploader でバックグラウンド転送を行いたい | networking | [references/networking/README.md](references/networking/README.md) |
| NetworkInformation / ConnectionProfile で接続状態を判定したい | networking | [references/networking/README.md](references/networking/README.md) |
| ポインター・キーボード入力をハンドリングしたい | input | [references/input/README.md](references/input/README.md) |
| FocusManager / XYFocus / タブナビゲーションでフォーカス制御したい | input | [references/input/README.md](references/input/README.md) |
| ペン入力・ドラッグアンドドロップ・IME 入力を扱いたい | input | [references/input/README.md](references/input/README.md) |
| 日付・通貨・数値を地域設定に合わせてフォーマットしたい | globalization | [references/globalization/README.md](references/globalization/README.md) |
| .resw リソースで多言語化・アプリの表示言語を切り替えたい | globalization | [references/globalization/README.md](references/globalization/README.md) |
| 右書き言語・双方向テキストに対応したい | globalization | [references/globalization/README.md](references/globalization/README.md) |
| PasswordVault / 資格情報を安全に保存したい | security-identity | [references/security-identity/README.md](references/security-identity/README.md) |
| Windows Hello / Passkeys / WebAuthenticationBroker で認証したい | security-identity | [references/security-identity/README.md](references/security-identity/README.md) |
| CryptographicBuffer / 証明書で暗号化・署名を行いたい | security-identity | [references/security-identity/README.md](references/security-identity/README.md) |
| クリップボード・共有 (DataTransferManager) を実装したい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |
| JumpList / TaskbarManager / SecondaryTile / スタート画面連携をしたい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |
| プロトコルアクティベーション・StartupTask で起動制御をしたい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |
| Share Sheet の送信・受信・連絡先候補への表示を実装したい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |
| Widgets Board のウィジェット・Dashboard フィードを提供したい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |
| Recall 連携・Windows Search 提供元・Copilot キー・taskbar ピン留めを実装したい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |
| Connected Experiences (People / Resume / Share) 全体像を把握したい | windows-integration | [references/windows-integration/README.md](references/windows-integration/README.md) |

このスキルは Windows App SDK / WinRT の OS 統合 API（デバイス・ネットワーク・入力・地域化・セキュリティ・シェル連携）のみを扱う。
コントロール・レイアウト・XAML UI は windows-winui-controls / windows-winui-ui / windows-design、グラフィックス・メディア描画は windows-graphics-media、パッケージング・配布は windows-packaging-publish が担当する。
