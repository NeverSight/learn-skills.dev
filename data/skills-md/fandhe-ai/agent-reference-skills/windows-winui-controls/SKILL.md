---
name: windows-winui-controls
description: >
  Windows アプリ開発 (WinUI 3 / Windows App SDK) のコントロール API リファレンス。
  Microsoft.UI.Xaml.Controls。Button, CheckBox, RadioButtons, ToggleSwitch, Slider,
  TextBox, RichEditBox, AutoSuggestBox, NumberBox, ListView, GridView, ItemsView,
  ItemsRepeater, TreeView, ComboBox, NavigationView, TabView, Frame, SplitView,
  BreadcrumbBar, ContentDialog, Flyout, CommandBar, TeachingTip, InfoBar,
  MediaPlayerElement, WebView2, CalendarView, DatePicker, ColorPicker, TitleBar。
user-invocable: false
---

# Windows WinUI Controls リファレンス

WinUI 3 (Microsoft.UI.Xaml.Controls) が提供するコントロール群の公式ドキュメントを蒸留したリファレンス。
Windows App SDK ベースのデスクトップアプリで使う入力・表示・ナビゲーション・ダイアログ・メディア系コントロールの API を網羅する。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-winui-controls/
  SKILL.md
  references/
    basic-controls/
      README.md
      button.md
      hyperlinkbutton.md
      repeatbutton.md
      togglebutton.md
      dropdownbutton.md
      splitbutton.md
      togglesplitbutton.md
      checkbox.md
      radiobutton.md
      radiobuttons.md
      toggleswitch.md
      slider.md
      progressbar.md
      progressring.md
      ratingcontrol.md
    text-controls/
      README.md
      text-block.md
      rich-text-block.md
      text-box.md
      rich-edit-box.md
      password-box.md
      auto-suggest-box.md
      number-box.md
      run.md
      span.md
      bold.md
      italic.md
      hyperlink.md
    collections/
      README.md
      annotated-scroll-bar.md
      list-view.md
      grid-view.md
      items-view.md
      items-repeater.md
      items-control.md
      tree-view.md
      flip-view.md
      list-box.md
      combo-box.md
      selector-bar.md
      semantic-zoom.md
      item-container.md
      scroll-view.md
    navigation-controls/
      README.md
      navigationview.md
      navigationviewitem.md
      tabview.md
      tabviewitem.md
      pivot.md
      breadcrumbbar.md
      frame.md
      splitview.md
      menubar.md
      menubaritem.md
      pipspager.md
      twopaneview.md
    dialogs-flyouts-commands/
      README.md
      content-dialog.md
      message-dialog.md
      flyout.md
      menu-flyout-item.md
      command-bar.md
      command-bar-flyout.md
      app-bar-button.md
      app-bar-toggle-button.md
      app-bar-separator.md
      teaching-tip.md
      info-bar.md
      info-badge.md
      tool-tip.md
      popup.md
    media-misc-controls/
      README.md
      image.md
      icon-elements.md
      media-player-element.md
      webview2.md
      inkcanvas-inktoolbar.md
      calendar-view.md
      calendar-date-picker.md
      date-picker.md
      time-picker.md
      color-picker.md
      person-picture.md
      expander.md
      animated-icon.md
      animated-visual-player.md
      swipe-control.md
      refresh-container.md
      parallax-view.md
      shapes.md
      title-bar.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Button / CheckBox / RadioButtons / ToggleSwitch / Slider で基本的な操作 UI を実装したい | basic-controls | [references/basic-controls/README.md](references/basic-controls/README.md) |
| ProgressBar / ProgressRing / RatingControl で進捗・評価を表示したい | basic-controls | [references/basic-controls/README.md](references/basic-controls/README.md) |
| SplitButton / DropDownButton でフライアウト付きボタンを実装したい | basic-controls | [references/basic-controls/README.md](references/basic-controls/README.md) |
| ToggleSplitButton で on/off 状態を持つフライアウト付きボタンを実装したい | basic-controls | [references/basic-controls/README.md](references/basic-controls/README.md) |
| TextBox / RichEditBox / PasswordBox / NumberBox でテキスト・数値入力を実装したい | text-controls | [references/text-controls/README.md](references/text-controls/README.md) |
| AutoSuggestBox でサジェスト付き検索入力を実装したい | text-controls | [references/text-controls/README.md](references/text-controls/README.md) |
| TextBlock / RichTextBlock / Run / Span / Bold / Hyperlink でリッチテキスト表示を組み立てたい | text-controls | [references/text-controls/README.md](references/text-controls/README.md) |
| ListView / GridView / ComboBox / ListBox で選択可能な一覧を実装したい | collections | [references/collections/README.md](references/collections/README.md) |
| ItemsView / ItemsRepeater でカスタムレイアウトの仮想化コレクションを構築したい | collections | [references/collections/README.md](references/collections/README.md) |
| TreeView / FlipView / SelectorBar / ScrollView で階層表示・スワイプ・スクロールを実装したい | collections | [references/collections/README.md](references/collections/README.md) |
| NavigationView / TabView / Pivot でアプリのトップレベルナビゲーションを実装したい | navigation-controls | [references/navigation-controls/README.md](references/navigation-controls/README.md) |
| Frame / SplitView / BreadcrumbBar でページ遷移・パンくず・折りたたみペインを実装したい | navigation-controls | [references/navigation-controls/README.md](references/navigation-controls/README.md) |
| MenuBar / PipsPager でメニューバー・ページネーションを実装したい | navigation-controls | [references/navigation-controls/README.md](references/navigation-controls/README.md) |
| ContentDialog / Flyout / Popup でモーダル・ライトディスミスな UI を表示したい | dialogs-flyouts-commands | [references/dialogs-flyouts-commands/README.md](references/dialogs-flyouts-commands/README.md) |
| CommandBar / CommandBarFlyout / AppBarButton でコマンドツールバーを実装したい | dialogs-flyouts-commands | [references/dialogs-flyouts-commands/README.md](references/dialogs-flyouts-commands/README.md) |
| TeachingTip / InfoBar / InfoBadge / ToolTip で通知・ヒントを表示したい | dialogs-flyouts-commands | [references/dialogs-flyouts-commands/README.md](references/dialogs-flyouts-commands/README.md) |
| Image / MediaPlayerElement / WebView2 でメディア・Web コンテンツを表示したい | media-misc-controls | [references/media-misc-controls/README.md](references/media-misc-controls/README.md) |
| CalendarView / DatePicker / TimePicker / ColorPicker で日付・時刻・色を選択したい | media-misc-controls | [references/media-misc-controls/README.md](references/media-misc-controls/README.md) |
| FontIcon / SymbolIcon / PathIcon / BitmapIcon / ImageIcon でコントロールにアイコンを割り当てたい | media-misc-controls | [references/media-misc-controls/README.md](references/media-misc-controls/README.md) |
| Expander / AnimatedIcon / SwipeControl / RefreshContainer / TitleBar でその他の UI 挙動を実装したい | media-misc-controls | [references/media-misc-controls/README.md](references/media-misc-controls/README.md) |

このスキルは WinUI 3 / Windows App SDK 固有のコントロール API のみを扱う。同名の Button / TextBox / NavigationView 等は apple-swiftui, ark-ui, chakra-ui, fandhe-frontend, android-compose-components とは無関係の別 API であり、Windows レイアウト・ウィンドウ管理・データバインディングなど他の windows-* スキルが存在する場合はそちらが担当する。
