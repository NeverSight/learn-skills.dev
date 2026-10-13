---
name: apple-graphics
description: >
  Apple グラフィックスフレームワークリファレンス。
  Metal, Core Animation, Core Graphics, Core Image, SpriteKit, SceneKit。
  MTLDevice, MTKView, MTLBuffer, MTLTexture,
  Metal 4 (MTL4CommandQueue, MTL4CommandBuffer, MTL4ArgumentTable),
  CALayer, CABasicAnimation, CADisplayLink, CAMetalDisplayLink, CAMetalDrawable,
  CGContext, CGPath, CGImage,
  CIFilter, CIContext, CIImage, CIRAWFilter, CIWarpKernel, CIBlendKernel,
  SKScene, SKSpriteNode, SKAction,
  SCNNode, SCNGeometry, SCNMaterial。
user-invocable: false
---

## ディレクトリ構成

```text
skills/apple-graphics/
  SKILL.md
  references/
    metal/
      README.md
      mtldevice.md
      mtlcommandqueue.md
      mtlcommandbuffer.md
      mtlrendercommandencoder.md
      mtlcomputecommandencoder.md
      mtlrenderpipelinestate.md
      mtlrenderpipelinedescriptor.md
      mtlcomputepipelinestate.md
      mtlbuffer.md
      mtltexture.md
      mtltexturedescriptor.md
      mtllibrary.md
      mtlfunction.md
      mtlrenderpassdescriptor.md
      mtkview.md
      mtktextureloader.md
      mtl4commandqueue.md
      mtl4commandbuffer.md
      mtl4compilerdescriptor.md
      mtl4argumenttable.md
      mtl4renderpipelinedescriptor.md
    core-animation/
      README.md
      calayer.md
      cashapelayer.md
      cagradientlayer.md
      catextlayer.md
      caemitterlayer.md
      careplicatorlayer.md
      caanimation.md
      cabasicanimation.md
      cakeyframeanimation.md
      caspringanimation.md
      caanimationgroup.md
      catransition.md
      catransaction.md
      camediatimingfunction.md
      cadisplaylink.md
      cametaldisplaylink.md
      cametaldrawable.md
      cascrolllayer.md
      catiledlayer.md
      catransformlayer.md
      caconstraint.md
      capropertyanimation.md
      cavaluefunction.md
    core-graphics/
      README.md
      cgcontext.md
      cgpath.md
      cgmutablepath.md
      cgrect.md
      cgsize.md
      cgpoint.md
      cgaffinetransform.md
      cgcolor.md
      cgcolorspace.md
      cgimage.md
      cggradient.md
      cglayer.md
      cgfont.md
      cgdataprovider.md
      cgbitmapinfo.md
      cgblendmode.md
    core-image/
      README.md
      ciimage.md
      cifilter.md
      cicontext.md
      cicolor.md
      civector.md
      cikernel.md
      cicolorkernel.md
      cifilterbuiltins.md
      cidetector.md
      cisampler.md
      ciimageprocessorkernel.md
      ciwarpkernel.md
      cirawfilter.md
      ciblendkernel.md
      cifiltershape.md
      cirenderdestination.md
    spritekit/
      README.md
      skscene.md
      skview.md
      sknode.md
      skspritenode.md
      sklabelnode.md
      skshapenode.md
      skaction.md
      skphysicsbody.md
      skphysicsworld.md
      skemitternode.md
      sktexture.md
      sktextureatlas.md
      skconstraint.md
      skcameranode.md
      skfieldnode.md
    scenekit/
      README.md
      scnscene.md
      scnview.md
      scnnode.md
      scngeometry.md
      scnmaterial.md
      scncamera.md
      scnlight.md
      scnaction.md
      scnphysicsbody.md
      scnphysicsworld.md
      scnanimation.md
      scnscenesource.md
      scngeometrysource.md
      scnbox.md
      scnsphere.md
      scncylinder.md
      scnplane.md
      scncone.md
      scntorus.md
      scncapsule.md
      scnpyramid.md
      scntube.md
      scnvector3.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| GPU デバイス・コマンドキューを初期化したい | metal | [references/metal/README.md](references/metal/README.md) |
| レンダーパイプライン・シェーダーを設定したい | metal | [references/metal/README.md](references/metal/README.md) |
| バッファ・テクスチャを作成・管理したい | metal | [references/metal/README.md](references/metal/README.md) |
| MTKView でメタルレンダリングループを構築したい | metal | [references/metal/README.md](references/metal/README.md) |
| Metal 4 API (MTL4CommandQueue / MTL4ArgumentTable) でコマンドを記録したい | metal | [references/metal/README.md](references/metal/README.md) |
| レイヤーにアニメーションを追加したい | core-animation | [references/core-animation/README.md](references/core-animation/README.md) |
| グラデーション・パーティクル・テキストをレイヤーで描きたい | core-animation | [references/core-animation/README.md](references/core-animation/README.md) |
| スプリングアニメーション・キーフレームアニメーションを使いたい | core-animation | [references/core-animation/README.md](references/core-animation/README.md) |
| 表示同期コールバック (CADisplayLink / CAMetalDisplayLink) を設定したい | core-animation | [references/core-animation/README.md](references/core-animation/README.md) |
| スクロールレイヤー・タイル表示・3D レイヤー階層を扱いたい | core-animation | [references/core-animation/README.md](references/core-animation/README.md) |
| Quartz 2D でパスを描画・塗りつぶしたい | core-graphics | [references/core-graphics/README.md](references/core-graphics/README.md) |
| アフィン変換・クリッピングを適用したい | core-graphics | [references/core-graphics/README.md](references/core-graphics/README.md) |
| ビットマップコンテキストを作成したい | core-graphics | [references/core-graphics/README.md](references/core-graphics/README.md) |
| カラースペース・グラデーション・ブレンドモードを指定したい | core-graphics | [references/core-graphics/README.md](references/core-graphics/README.md) |
| 組み込みフィルターで画像を加工したい | core-image | [references/core-image/README.md](references/core-image/README.md) |
| カスタムカーネル (GPU) を書きたい | core-image | [references/core-image/README.md](references/core-image/README.md) |
| 顔・QR コードを検出したい | core-image | [references/core-image/README.md](references/core-image/README.md) |
| Metal バックエンドで CIImage を高速レンダリングしたい | core-image | [references/core-image/README.md](references/core-image/README.md) |
| RAW 画像・ジオメトリワープ・ブレンドカーネルを処理したい | core-image | [references/core-image/README.md](references/core-image/README.md) |
| 2D ゲームシーンを構築したい | spritekit | [references/spritekit/README.md](references/spritekit/README.md) |
| スプライト・テキスト・シェイプを配置したい | spritekit | [references/spritekit/README.md](references/spritekit/README.md) |
| 物理シミュレーション・衝突判定を設定したい | spritekit | [references/spritekit/README.md](references/spritekit/README.md) |
| パーティクルエフェクト・フィールドノードを使いたい | spritekit | [references/spritekit/README.md](references/spritekit/README.md) |
| 3D シーン・ノード階層を構築したい | scenekit | [references/scenekit/README.md](references/scenekit/README.md) |
| マテリアル・ライト・カメラを設定したい | scenekit | [references/scenekit/README.md](references/scenekit/README.md) |
| プリミティブジオメトリ (Box / Sphere 等) を使いたい | scenekit | [references/scenekit/README.md](references/scenekit/README.md) |
| 3D 物理シミュレーション・アニメーションを追加したい | scenekit | [references/scenekit/README.md](references/scenekit/README.md) |
