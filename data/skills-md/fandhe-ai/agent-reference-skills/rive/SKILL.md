---
name: rive
description: >
  Rive アニメーションランタイム (Web / React)。
  useRive, useRiveFile, useStateMachineInput, RiveComponent, State Machine,
  Data Binding, ViewModel / ViewModelInstance, Events, Layout / Fit / Alignment, .riv。
  @rive-app/canvas / webgl2 / react-canvas / react-webgl2、enableGPUCanvas、
  Semantics, Rive CLI。Scripting (Luau), Artboard, Property, Path / Paint / Renderer,
  WGSL Shaders, GPU pipeline, Node / Layout / Converter スクリプト。
user-invocable: false
---

対象バージョン: Rive docs ([rive.app/docs](https://rive.app/docs/llms.txt)、版数なし) を 2026-10-16 取得。参考版は `@rive-app/webgl2` 2.44.2 / `@rive-app/react-webgl2` 4.36.0。`stateMachine` パラメーターと非推奨化は Web v2.41.0、GPU Canvas (`enableGPUCanvas`) は v2.42.0、`useStateMachineInput` の非推奨化は React v4.33.0。

## ディレクトリ構成

```text
skills/rive/
  SKILL.md
  references/
    runtimes-web/
      README.md
      packages.md
      rive-constructor.md
      rive-methods.md
      layout.md
      state-machine-playback.md
      data-binding.md
      loading-assets.md
      fonts.md
      audio.md
      events.md
      rive-file.md
      preloading-wasm.md
      artboards.md
      caching-a-rive-file.md
      canvas-vs-webgl.md
      semantics.md
      gpu-canvas.md
      faq.md
      low-level-api-usage.md
      migration-guides.md
    runtimes-react/
      README.md
      overview.md
      use-rive.md
      use-state-machine-input.md
      layout.md
      data-binding.md
      artboards.md
      best-practices.md
      caching-a-rive-file.md
      migration-guides.md
      rendering-to-a-bitmap.md
      loading-assets.md
      fonts.md
      semantics.md
      gpu-canvas.md
      preloading-wasm.md
      playing-audio.md
    concepts/
      README.md
      state-machine.md
      states.md
      transitions.md
      layers.md
      inputs.md
      listeners.md
      data-binding.md
      data-binding-binding-data.md
      data-binding-controlling-data.md
      data-binding-lists.md
      data-binding-migration-guide.md
      data-binding-property-groups.md
      data-binding-property-types.md
      data-binding-stateful-components.md
      view-models.md
      instances.md
      properties.md
      converters.md
      enums.md
      events.md
      audio-events.md
      layout.md
      layout-animation.md
      layout-parameters.md
      layout-styles.md
      layout-tools.md
      n-slicing.md
      scrolling.md
      open-url-events.md
      component-sizing.md
      accessibility-semantics.md
      accessibility-focus.md
      accessibility-reduced-motion.md
    scripting-api-reference/
      README.md
      getting-started.md
      creating-scripts.md
      data-binding.md
      script-inputs.md
      pointer-events.md
      wgsl-shaders.md
      configuration.md
      debugging.md
      keyboard-shortcuts.md
      demos.md
      protocol-overview.md
      protocol-node-scripts.md
      protocol-layout-scripts.md
      protocol-converter-scripts.md
      protocol-listener-action-scripts.md
      protocol-path-effect-scripts.md
      protocol-transition-condition-scripts.md
      protocol-test-scripts.md
      protocol-util-scripts.md
      artboard-artboard.md
      artboard-animation.md
      artboard-view-model.md
      artboard-listener-context.md
      artboard-node-data.md
      artboard-text-input.md
      artboard-events.md
      data-value.md
      property.md
      color.md
      gradient.md
      paint.md
      path.md
      path-measure.md
      mat2d.md
      mat4.md
      vector.md
      renderer.md
      promise.md
      image.md
      font.md
      luau-types.md
      interface-context.md
      interface-node.md
      interface-layout.md
      interface-input.md
      interface-view-model.md
      interface-converter.md
      interface-path-effect.md
      interface-trigger.md
      interface-misc.md
      interface-decoded-image.md
      gpu-core.md
      gpu-buffers.md
      gpu-bindings.md
      gpu-textures.md
      gpu-pipeline-state.md
      unit-testing.md
      testing.md
      text.md
      mesh.md
      file-format.md
      artboard-drawable.md
  samples/
    README.md
    web-basic.md
    react-interactive.md
    state-machine-control.md
    web-data-binding.md
  scripts/
    README.md
    install.md
    cli.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの README.md を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
| --- | --- | --- |
| パッケージ選定（canvas / webgl2 / canvas-lite）を知りたい | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| Rive コンストラクタのオプションを調べたい | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| play / pause / stop など Rive インスタンスメソッドを使いたい | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| .riv ファイルを複数インスタンスで共有したい（RiveFile / caching） | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| フォント・音声アセットを動的に読み込みたい | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| WASM を自己ホストしてスタートアップを高速化したい | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| Artboard の切り替え・Low-level API・バージョン移行を調べたい | runtimes-web | [references/runtimes-web/README.md](references/runtimes-web/README.md) |
| React で useRive を使ってアニメーションを表示したい | runtimes-react | [references/runtimes-react/README.md](references/runtimes-react/README.md) |
| useStateMachineInput で State Machine 入力を操作したい | runtimes-react | [references/runtimes-react/README.md](references/runtimes-react/README.md) |
| React で Data Binding / ViewModel を使いたい | runtimes-react | [references/runtimes-react/README.md](references/runtimes-react/README.md) |
| React のパフォーマンス指針・ビットマップ描画・バージョン移行を知りたい | runtimes-react | [references/runtimes-react/README.md](references/runtimes-react/README.md) |
| State Machine の仕組み・状態・遷移を理解したい | concepts | [references/concepts/README.md](references/concepts/README.md) |
| Inputs / Listeners / Events / Audio Events の概念を把握したい | concepts | [references/concepts/README.md](references/concepts/README.md) |
| ViewModel / ViewModelInstance / Properties を理解したい | concepts | [references/concepts/README.md](references/concepts/README.md) |
| Converters / Enums / Data Binding（Lists / Property Groups / Stateful Components 含む）の概念を調べたい | concepts | [references/concepts/README.md](references/concepts/README.md) |
| Layout / Fit / Alignment・N-Slicing・Scrolling の概念を知りたい | concepts | [references/concepts/README.md](references/concepts/README.md) |
| Rive Scripting（Luau）で Node / Layout / Converter / Path Effect スクリプトを書き、Artboard / ViewModel / Property を操作したい | scripting-api-reference | [references/scripting-api-reference/README.md](references/scripting-api-reference/README.md) |
| Path / Paint / Renderer / Color / Gradient で描画処理を書きたい | scripting-api-reference | [references/scripting-api-reference/README.md](references/scripting-api-reference/README.md) |
| WGSL Shaders / GPU Buffers・Textures・Pipeline State を扱いたい | scripting-api-reference | [references/scripting-api-reference/README.md](references/scripting-api-reference/README.md) |
| アクセシビリティ・スクリーンリーダー対応（Semantics / Focus / Reduced Motion）を実装したい | runtimes-web / runtimes-react / concepts | [references/runtimes-web/README.md](references/runtimes-web/README.md) / [references/runtimes-react/README.md](references/runtimes-react/README.md) / [references/concepts/README.md](references/concepts/README.md) |
| GPU Canvas（3D / シェーダー、enableGPUCanvas）を有効化したい | runtimes-web / runtimes-react | [references/runtimes-web/README.md](references/runtimes-web/README.md) / [references/runtimes-react/README.md](references/runtimes-react/README.md) |
| Global View Model・Data Binding を Web / 概念面で調べたい | runtimes-web / concepts | [references/runtimes-web/README.md](references/runtimes-web/README.md) / [references/concepts/README.md](references/concepts/README.md) |
| React でフォント・アセット・WASM・音声を読み込みたい（useRiveFile 含む） | runtimes-react | [references/runtimes-react/README.md](references/runtimes-react/README.md) |
| Open URL Events・コンポーネントサイズ指定を知りたい | concepts | [references/concepts/README.md](references/concepts/README.md) |
| Scripting のテキストレイアウト・Mesh インスタンシング・ユニットテスト・独自ファイル形式を扱いたい | scripting-api-reference | [references/scripting-api-reference/README.md](references/scripting-api-reference/README.md) |
| 典型的な使い方を知りたい（Web Data Binding 含む） | samples | [samples/README.md](samples/README.md) |
| インストール・パッケージ追加・Rive CLI（create / preview / push / pull）を知りたい | scripts | [scripts/README.md](scripts/README.md) |
