---
name: docs-react
description: |
  Look up CE.SDK React reference docs, guides, and configuration pages.

  Use when the user needs CE.SDK docs for React — configuration, UI customization,
  export options, feature guides, or getting-started instructions. Also triggered by "IMG.LY", "CreativeEditor",
  "CE.SDK", or "cesdk" when the user needs an existing React doc page.

  Not for writing code (use build) or concept explanations (use explain).

  <example>
  Context: User asks about React configuration
  user: "How do I configure the editor in React?"
  assistant: "I'll use /cesdk:docs-react to look up configuration options."
  </example>

  <example>
  Context: User needs React component setup
  user: "How do I embed CE.SDK in a React component?"
  assistant: "Let me use /cesdk:docs-react to find the relevant documentation."
  </example>
argument-hint: "[search-topic]"
---

## Documentation Index

<-- IMGLY-AGENTS-MD-START -->[CE.SDK React Docs Index]|root: .|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for any CE.SDK tasks. Consult the local docs directory before using pre-trained knowledge.|actions.md|animation:{create,edit.md,overview.md,types.md}|animation/create:{base.md,text.md}|api-reference:{overview.md}|automation:{auto-resize.md,batch-processing.md,data-merge.md,design-generation.md,overview.md}|browser-support.md|colors:{adjust.md,apply.md,basics.md,conversion.md,create-color-palette.md,for-print,for-screen,overview.md,replace.md}|colors/for-print:{cmyk.md,spot.md}|colors/for-screen:{p3.md,srgb.md}|compatibility.md|concepts:{architecture.md,assets.md,blocks.md,buffers.md,design-units.md,edit-modes.md,editing-workflow.md,events.md,headless-mode,pages.md,resources.md,scenes.md,templating.md,terminology.md,undo-and-history.md}|concepts/headless-mode:{browser.md}|configuration.md|conversion:{overview.md,to-base64.md,to-pdf.md,to-png.md}|create-audio:{audio}|create-audio/audio:{add-music.md,add-sound-effects.md,loop.md}|create-composition:{add-background.md,blend-modes.md,collage.md,group-and-ungroup.md,layer-management.md,layout.md,lock-design.md,multi-page.md,overview.md,programmatic.md}|create-templates:{add-dynamic-content,add-to-template-library.md,edit-or-remove.md,from-scratch.md,import,lock.md,overview.md}|create-templates/add-dynamic-content:{placeholders.md,set-editing-constraints.md,text-variables.md}|create-templates/import:{from-scene-file.md}|create-video:{audio,control.md,limitations.md,overview.md,timeline-editor.md,update-caption-presets.md}|create-video/audio:{adjust-speed.md,adjust-volume.md}|edit-image:{add-watermark.md,overview.md,remove-bg.md,replace-colors.md,transform,vectorize.md}|edit-image/transform:{crop.md,move.md,resize.md,rotate.md,scale.md}|edit-video:{add-captions.md,add-watermark.md,join-and-arrange.md,redaction.md,split.md,transform,trim.md}|edit-video/transform:{crop.md,flip.md,move.md,resize.md,rotate.md,scale.md}|engine-interface.md|export-save-publish:{create-thumbnail.md,export,for-printing.md,for-social-media.md,pre-export-validation.md,save.md,store-custom-metadata.md}|export-save-publish/export:{compress.md,overview.md,partial-export.md,size-limits.md,to-jpeg.md,to-mp4.md,to-pdf.md,to-png.md,to-raw-data.md,to-webp.md,with-color-mask.md}|file-format-support.md|fills:{color.md,image.md,overview.md,video.md}|filters-and-effects:{apply.md,blur.md,chroma-key-green-screen.md,create-custom-filters.md,create-custom-lut-filter.md,distortion.md,duotone.md,gradients.md,overview.md,support.md}|get-started:{clone-github-project.md,existing-project.md,mcp-server.md,new-project.md,new-project-without-ui.md,overview.md}|guides:{export-save-publish}|guides/export-save-publish:{export}|guides/export-save-publish/export:{audio.md}|import-media:{asset-library.md,asset-panel,capture-from-camera,concepts.md,content-json-schema.md,default-assets.md,edit-or-remove-assets.md,file-format-support.md,from-local-source,from-remote-source,overview.md,retrieve-mimetype.md,size-limits.md,source-sets.md}|import-media/asset-panel:{basics.md,customize.md,refresh-assets.md,thumbnails.md}|import-media/capture-from-camera:{record-video.md}|import-media/from-local-source:{user-upload.md}|import-media/from-remote-source:{asset-versioning.md,getty-images.md,imgly-premium-assets.md,pexels.md,remote-asset.md,soundstripe.md,third-party.md,unsplash.md,your-server.md}|insert-media:{audio.md,images.md,position-and-align.md,shapes-or-stickers.md,videos.md}|key-capabilities.md|key-concepts.md|licensing.md|llms-txt.md|open-the-editor:{blank-canvas.md,from-htmlcanvas.md,from-image.md,from-template.md,from-video.md,import-design,load-scene.md,overview.md,set-zoom-level.md,uri-resolver.md}|open-the-editor/import-design:{from-archive.md,from-indesign.md,from-photoshop.md}|outlines:{overview.md,shadows-and-glows.md,strokes.md}|overview.md|performance.md|plugins:{print-ready-pdf.md}|prebuilt-solutions:{3d-product-configurator.md,ai-editor.md,auto-resize.md,automated-video-generation.md,canva-clone.md,data-merge.md,design-editor.md,design-generation.md,mockup-editor.md,multi-image-generation.md,photo-editor.md,photobook-editor.md,postcard-editor.md,t-shirt-designer.md,video-editor.md}|rules:{asset-handling.md,common-pitfalls.md,content-fill-mode.md,enforce-brand-guidelines.md,lock-content.md,moderate-content.md,overview.md,silent-init-errors.md,strict-mode-double-mount.md,verify-properties-before-use.md}|security.md|serve-assets.md|settings.md|shapes.md|stickers.md|stickers-and-shapes:{combine.md,create-cutout.md,create-edit,insert-qr-code.md}|stickers-and-shapes/create-edit:{create-shapes.md,create-stickers.md,edit-shapes.md}|text:{add.md,adjust-spacing.md,auto-size.md,custom-fonts.md,edit.md,effects.md,emojis.md,language-support.md,overview.md,styling.md,text-designs.md}|to-v1-10.md|to-v1-13.md|to-v1-19.md|to-v1-32.md|upgrade.md|use-templates:{apply-template.md,generate.md,library.md,overview.md,programmatic.md,replace-content.md}|user-interface:{ai-integration,appearance,build-your-own-ui.md,customization,localization.md,overview.md,ui-extensions}|user-interface/ai-integration:{audio-generation.md,custom-provider.md,image-generation.md,integrate.md,proxy-server.md,text-generation.md,video-generation.md}|user-interface/appearance:{change-ui-font.md,custom-labels.md,icons.md,theming.md}|user-interface/customization:{canvas.md,canvas-menu.md,color-palette.md,crop-presets.md,disable-or-enable.md,dock.md,force-crop.md,inspector-bar.md,navigation-bar.md,page-format.md,panel.md,quick-start,reference}|user-interface/customization/quick-start:{add-action-buttons.md,add-dock-buttons.md,create-custom-components.md,reorder-components.md,show-hide-components.md}|user-interface/customization/reference:{component-order-api.md,component-reference.md}|user-interface/ui-extensions:{add-custom-feature.md,asset-library.md,create-custom-panel.md,customize-behaviour.md,notifications-and-dialogs.md,quick-actions.md,register-new-component.md}|what-is-cesdk.md|<-- IMGLY-AGENTS-MD-END -->

## API Index

<-- IMGLY-TYPES-MD-START -->
[CE.SDK Web API Index]|root: .

CreativeEngine:{asset,block,editor,event,scene,variable,reactor,version,addPlugin,unstable_setVideoExportInactivityTimeout,unstable_setExportInactivityTimeout,addPostUpdateCallback,addPreUpdateCallback,setWheelEventTarget,dispose},... (+5)
BlockAPI:{export,exportWithColorMask,exportVideo,exportAudio,loadFromString,loadFromArchiveURL,loadFromURL,saveToString,saveToArchive,create,createFill,getAudioTrackCountFromVideo,createAudioFromVideo,createAudiosFromVideo,getAudioInfoFromVideo},... (+347)
AssetAPI:{registerApplyMiddleware,registerApplyToBlockMiddleware,addSource,addLocalSource,addLocalAssetSourceFromJSONString,addLocalAssetSourceFromJSONURI,removeSource,findAllSources,findAssets,fetchAsset,getGroups,getSupportedMimeTypes,getCredits,name,url},... (+14)
SceneAPI:{loadFromString,loadFromURL,loadFromArchiveURL,saveToString,saveToArchive,create,createVideo,createFromImage,createFromVideo,get,applyTemplateFromString,applyTemplateFromURL,getMode,setMode,setDesignUnit},... (+22)
EditorAPI:{unlockWithLicense,startTracking,setTrackingMetadata,getTrackingMetadata,getActiveLicense,onStateChanged,setEditMode,getEditMode,unstable_isInteractionHappening,getCursorType,getCursorRotation,getTextCursorPositionInScreenSpaceX,getTextCursorPositionInScreenSpaceY,createHistory,destroyHistory},... (+74)
EventAPI:{subscribe}
VariableAPI:{findAll,setString,getString,remove}
Types:{AnimationType,AssetResult,BlendMode,Color,DesignBlockId,ExportOptions,PropertyType,Scope,TextCase,VideoExportOptions}
<-- IMGLY-TYPES-MD-END -->

# CE.SDK React Documentation

Look up documentation for IMG.LY CreativeEditor SDK (React).

**Query**: $ARGUMENTS

## How to Use

1. **Index lookup**: Match the query to a path in the Documentation Index above.
   The index uses compressed format: `dir:{file1.md,file2.md}` means files are at
   `dir/file1.md` and `dir/file2.md`.
   Resolve the path using Glob: `**/skills/docs-react/<path>.md`
   (e.g., for `text/add.md` → `**/skills/docs-react/text/add.md`)
2. **Search**: If no exact match exists, use Grep to search the documentation:
   `Grep pattern="<keyword>" path="**/skills/docs-react/" output_mode="content"`
   or search filenames: `Glob pattern="**/skills/docs-react/**/*<keyword>*.md"`
3. **Read and respond** with the relevant section and code examples
4. **Check rules** if the topic involves setup, initialization, or common
   operations: `**/skills/docs-react/rules/*.md`

## API Lookup

For TypeScript API queries (method signatures, types, parameters):

1. **Module lookup**: Match the query to a module in the API index above.
   Read the module file: `**/skills/docs-react/api/<ModuleName>.md`
   (e.g., for BlockAPI → `**/skills/docs-react/api/BlockAPI.md`)
2. **Method search**: If looking for a specific method, use Grep:
   `Grep pattern="<method>" path="**/skills/docs-react/api/" output_mode="content"`
3. **For common types**: Read `**/skills/docs-react/api/types.md`

**Tip**: Verify types against the TypeScript definitions — CE.SDK evolves rapidly and type shapes may differ from pre-trained knowledge.

## Quick Reference

| Topic | Path |
|-------|------|
| Getting started | `get-started/` |
| API methods | `engine-interface.md` |
| Configuration | `configuration.md`, `settings.md` |
| UI customization | `user-interface/customization/` |
| UI extensions | `user-interface/ui-extensions/` |
| Import media | `import-media/` |
| Export/save | `export-save-publish/` |
| Templates | `use-templates/`, `create-templates/` |
| Text operations | `text/` |
| Image editing | `edit-image/` |
| Video editing | `edit-video/`, `create-video/` |
| Fills & colors | `fills/`, `colors/` |
| Filters/effects | `filters-and-effects/` |
| Prebuilt solutions | `prebuilt-solutions/` |
| Known pitfalls | `rules/` |
| API modules | `api/BlockAPI.md`, `api/SceneAPI.md`, etc. |

## Additional Triggers

This skill also covers queries about CE.SDK block types, asset sources, and feature capabilities.
It handles API method lookups — BlockAPI, SceneAPI, EditorAPI, AssetAPI, method signatures,
return types, and "engine.block" style queries.

## Related Skills

- Use \`/cesdk:build\` when the user needs implementation help, not just docs
- Use \`/cesdk:explain\` for conceptual explanations beyond what docs cover
