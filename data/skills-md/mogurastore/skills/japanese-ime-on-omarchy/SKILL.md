---
name: japanese-ime-on-omarchy
description: Omarchy で fcitx5 + Mozc 日本語入力を構築する。
disable-model-invocation: true
---

# Omarchy 日本語入力セットアップ

Omarchy（Arch Linux + Hyprland + Wayland、fcitx5 + Mozc）の fcitx5 フルセットアップ.

## 1. パッケージ

導入済みか調査し、未導入があればユーザーに実行を促す（スキル側では実行しない）。

調査コマンド:

```bash
omarchy pkg present fcitx5 fcitx5-gtk fcitx5-qt fcitx5-mozc
```

提示コマンド:

```bash
omarchy pkg add fcitx5 fcitx5-gtk fcitx5-qt fcitx5-mozc
```

## 2. profile

バックアップ → `~/.config/fcitx5/profile` 編集 → サービス再起動。
`~/.config/fcitx5/profile` に `keyboard-jp` + `mozc` を登録する。

```ini
[Groups/0]
Name=Default
Default Layout=jp
DefaultIM=keyboard-jp

[Groups/0/Items/0]
Name=keyboard-jp

[Groups/0/Items/1]
Name=mozc

[GroupOrder]
0=Default
```

```bash
# 必ず停止してからprofileに書き込む。
systemctl --user stop omarchy-fcitx5.service
cp ~/.config/fcitx5/profile ~/.config/fcitx5/profile.bak.$(date +%s)
# 編集
systemctl --user start omarchy-fcitx5.service
```

## 3. ホットキー

バックアップ → `~/.config/fcitx5/config` 編集。

```ini
[Hotkey/TriggerKeys]
0=Zenkaku_Hankaku

[Hotkey/ActivateKeys]
0=Henkan

[Hotkey/DeactivateKeys]
0=Muhenkan

[Behavior]
ShareInputState=No
```

```bash
cp ~/.config/fcitx5/config ~/.config/fcitx5/config.bak.$(date +%s)
# 編集
```

結果: 変換 → mozc（ひらがな）、無変換 → keyboard-jp（英語入力）、半角/全角 → トグル、`Ctrl+Space` は無効、IME 状態は各アプリで独立。

- 設定完了後はユーザーに動作確認を依頼する
