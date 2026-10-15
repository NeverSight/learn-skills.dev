---
name: android-compose-components
description: >
  Android Jetpack Compose (Kotlin) の androidx Material3 コンポーネントリファレンス。
  Button, IconButton, FloatingActionButton, Checkbox, Switch, Slider, TextField,
  SearchBar, DropdownMenu, Chip, DatePicker, TimePicker, Card, Scaffold, Dialog,
  BottomSheet, TopAppBar, NavigationBar, NavigationRail, Tab, Snackbar,
  ProgressIndicator, Badge, Icon, MaterialTheme, ColorScheme, Typography, Shapes。
user-invocable: false
---

# Jetpack Compose Material3 コンポーネントリファレンス

Jetpack Compose Material3 (`androidx.compose.material3`) コンポーネント API を網羅したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-compose-components/
  SKILL.md
  references/
    buttons/
      README.md
      button.md
      filledtonalbutton.md
      elevatedbutton.md
      outlinedbutton.md
      textbutton.md
      iconbutton.md
      icontogglebutton.md
      floatingactionbutton.md
      extendedfloatingactionbutton.md
      segmentedbutton.md
      splitbutton.md
      buttongroup.md
      floatingactionbuttonmenu.md
      togglebutton.md
    inputs/
      README.md
      checkbox.md
      tristatecheckbox.md
      radiobutton.md
      switch.md
      slider.md
      rangeslider.md
      textfield.md
      outlinedtextfield.md
      securetextfield.md
      scrollfield.md
      rememberscrollfieldstate.md
      searchbar.md
      dockedsearchbar.md
      expandedfullscreensearchbar.md
      expandeddockedsearchbar.md
      dropdownmenu.md
      dropdownmenuitem.md
      exposeddropdownmenubox.md
      exposeddropdownmenu.md
      assistchip.md
      filterchip.md
      inputchip.md
      suggestionchip.md
    pickers/
      README.md
      datepicker.md
      rememberdatepickerstate.md
      datepickerdialog.md
      daterangepicker.md
      rememberdaterangepickerstate.md
      timepicker.md
      timeinput.md
      remembertimepickerstate.md
      timepickerdialog.md
    containers/
      README.md
      card.md
      scaffold.md
      surface.md
      listitem.md
      segmentedlistitem.md
      divider.md
      modalbottomsheet.md
      bottomsheetscaffold.md
      navigationdrawer.md
      alertdialog.md
      dialog.md
      carousel.md
      swipetodismissbox.md
      pulltorefreshbox.md
      tooltipbox.md
      verticaldraghandle.md
      noninteractivescrollbar.md
    navigation-components/
      README.md
      topappbar.md
      topappbarscrollbehavior.md
      bottomappbar.md
      horizontalfloatingtoolbar.md
      verticalfloatingtoolbar.md
      appbarrow.md
      navigationbar.md
      navigationbaritem.md
      shortnavigationbar.md
      shortnavigationbaritem.md
      navigationrail.md
      navigationrailitem.md
      widenavigationrail.md
      widenavigationrailitem.md
      navigationdraweritem.md
      primarytabrow.md
      tab.md
      leadingicontab.md
      appbarcolumn.md
    feedback/
      README.md
      snackbar.md
      snackbarhost.md
      snackbarhoststate.md
      snackbardata.md
      linearprogressindicator.md
      linearwavyprogressindicator.md
      circularprogressindicator.md
      circularwavyprogressindicator.md
      loadingindicator.md
      badge.md
      badgedbox.md
      icon.md
      text.md
    theming/
      README.md
      material-theme.md
      material-expressive-theme.md
      color-scheme.md
      dynamic-color-scheme.md
      typography.md
      shapes.md
      content-color.md
      motion-scheme.md
      surface-tonal-elevation.md
      theme-anatomy.md
      custom-design-system.md
      material2-material3-migration.md
      material-shapes.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Button / IconButton / FloatingActionButton などの操作ボタンを実装したい | buttons | [references/buttons/README.md](references/buttons/README.md) |
| SegmentedButton / SplitButton / ButtonGroup でボタン群を作りたい | buttons | [references/buttons/README.md](references/buttons/README.md) |
| Checkbox / RadioButton / Switch / Slider で選択・切り替え UI を作りたい | inputs | [references/inputs/README.md](references/inputs/README.md) |
| TextField / OutlinedTextField / SecureTextField でテキスト入力を実装したい | inputs | [references/inputs/README.md](references/inputs/README.md) |
| SearchBar / DropdownMenu / Chip 系コンポーネントを使いたい | inputs | [references/inputs/README.md](references/inputs/README.md) |
| DatePicker / DateRangePicker で日付選択 UI を実装したい | pickers | [references/pickers/README.md](references/pickers/README.md) |
| TimePicker / TimeInput で時刻選択 UI を実装したい | pickers | [references/pickers/README.md](references/pickers/README.md) |
| rememberDatePickerState 等の State や DatePickerDialog / TimePickerDialog でダイアログ表示したい | pickers | [references/pickers/README.md](references/pickers/README.md) |
| Card / Surface / Scaffold / ListItem でコンテンツを表示したい | containers | [references/containers/README.md](references/containers/README.md) |
| Dialog / AlertDialog / ModalBottomSheet / BottomSheetScaffold / NavigationDrawer でモーダル・シートを表示したい | containers | [references/containers/README.md](references/containers/README.md) |
| Carousel / TooltipBox / SwipeToDismissBox / PullToRefreshBox でジェスチャ付きコンテナを使いたい | containers | [references/containers/README.md](references/containers/README.md) |
| TopAppBar / BottomAppBar / FloatingToolbar で画面上下のバーを実装したい | navigation-components | [references/navigation-components/README.md](references/navigation-components/README.md) |
| NavigationBar / NavigationRail / ShortNavigationBar で主要ナビゲーションを実装したい | navigation-components | [references/navigation-components/README.md](references/navigation-components/README.md) |
| PrimaryTabRow / Tab / LeadingIconTab / AppBarRow / AppBarColumn でタブ・アクション行を実装したい | navigation-components | [references/navigation-components/README.md](references/navigation-components/README.md) |
| Snackbar / SnackbarHost / SnackbarHostState でメッセージ通知を実装したい | feedback | [references/feedback/README.md](references/feedback/README.md) |
| LinearProgressIndicator / CircularProgressIndicator / LoadingIndicator で進捗を表示したい | feedback | [references/feedback/README.md](references/feedback/README.md) |
| Badge / BadgedBox / Icon / Text で表示要素を組み立てたい | feedback | [references/feedback/README.md](references/feedback/README.md) |
| MaterialTheme / ColorScheme / Typography / Shapes / MaterialShapes / Dynamic color でテーマをカスタマイズしたい | theming | [references/theming/README.md](references/theming/README.md) |
| Material2 から Material3 へ移行したい | theming | [references/theming/README.md](references/theming/README.md) |
| レイアウト・状態管理・ジェスチャを扱いたい | — | 別スキル `android-compose-ui` の担当 |
| アニメーション・描画を扱いたい | — | 別スキル `android-compose-graphics-animation` の担当 |
