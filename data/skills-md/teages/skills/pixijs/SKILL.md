---
name: pixijs
description: Use when asked about PixiJS, a popular 2D rendering library for the web. This skill provides information about PixiJS, its features, and how to use it effectively in web development projects.
license: MIT
meta:
  source: PixiJS Documentation https://pixijs.download/release/docs/index.html
---
# PixiJS Usage Guide for Copilot

When working with PixiJS tasks, follow these guidelines:

## How to Use This Skill

1. **Understand the task context** - Determine what type of PixiJS work is needed
2. **Locate relevant documentation** - Use the sections below to find appropriate references
3. **Apply the documentation** - Read the linked files for detailed information
4. **Implement solutions** - Use the patterns and examples from the documentation

## Common Task Scenarios

### Creating a PixiJS Application
- Start with: `app.md` for application setup
- Reference: `app.Application.html.md` for API details
- Plugins: `app-1.md` (Ticker), `app-2.md` (Resize), `app-3.md` (Culler)

### Working with Display Objects
- Sprites: `scene-3.md` and `scene.Sprite.html.md`
- Containers: `scene-1.md` and `scene.Container.html.md`
- Graphics: `scene-6.md` and `scene.Graphics.html.md`
- Text: `scene-9.md` through `scene-13.md`

### Handling User Input
- Event system: `events.md`
- Event types: `events.FederatedPointerEvent.html.md`, `events.FederatedMouseEvent.html.md`

### Loading Assets
- Asset management: `assets.md`
- Loading: `assets.Assets.html.md`
- Spritesheets: `assets.Spritesheet.html.md`

### Performance Optimization
- General tips: `core-concepts-7.md`
- Render groups: `core-concepts-3.md`
- Culling: `core-concepts-2.md`
- Cache as texture: `scene-2.md`

### Applying Filters
- Overview: `filters.md`
- Common filters: `filters.BlurFilter.html.md`, `filters.ColorMatrixFilter.html.md`

## Documentation Sections

The following sections are automatically generated from PixiJS documentation. Each link points to detailed information about specific topics.

# PixiJS

> PixiJS is the fastest, most lightweight 2D library available for the web, working across all devices and allowing you to create rich, interactive graphics and cross-platform applications using WebGL, WebGPU, and Canvas as a fallback.

## core-concepts

- [Architecture](./core-concepts.md): A comprehensive guide to the architecture of PixiJS, including its major components and extension system.
- [Scene Graph](./core-concepts-1.md): Understanding the PixiJS scene graph, its structure, and how to manage parent-child relationships, render order, and culling for optimal performance.
- [Render Loop](./core-concepts-2.md): Understanding the PixiJS render loop, including how it updates the scene graph and renders frames efficiently.
- [Render Groups](./core-concepts-3.md): Learn how to use Render Groups in PixiJS to optimize rendering performance by grouping scene elements for efficient GPU processing.
- [Render Layers](./core-concepts-4.md): Understanding PixiJS Render Layers for controlling rendering order independently of logical hierarchy.
- [Environments](./core-concepts-5.md): Learn how PixiJS adapts to different environments like browsers, Web Workers, and custom execution contexts, and how to configure it for your needs.
- [Garbage Collection](./core-concepts-6.md): Managing GPU resources and garbage collection in PixiJS for optimal performance.
- [Performance Tips](./core-concepts-7.md): Performance tips for optimizing PixiJS applications, covering general practices and specific techniques for maximizing rendering efficiency.

## accessibility

- [Overview](./accessibility.md): Use PixiJS's built-in accessibility features to make your applications inclusive for users with disabilities.
- [AccessibilitySystem](./accessibility.AccessibilitySystem.md): The Accessibility system provides screen reader and keyboard navigation support for PixiJS content.

## app

- [Overview](./app.md): Create and configure a PixiJS Application with WebGL, WebGPU, or Canvas rendering, built-in plugins, and custom application plugins.
- [Ticker Plugin](./app-1.md): Use the TickerPlugin in PixiJS for rendering and frame updates.
- [Resize Plugin](./app-2.md): Use the ResizePlugin in PixiJS to make your application responsive to window or element size changes.
- [Culler Plugin](./app-3.md): Use the CullerPlugin in PixiJS to skip rendering for offscreen objects.
- [Application](./app.Application.md): Convenience class to create a new PixiJS application.
- [CullerPlugin](./app.CullerPlugin.md): An {@link Application} plugin that automatically culls (hides) display objects that are outside the visible screen area.
- [ResizePlugin](./app.ResizePlugin.md): Middleware for Application's resize functionality.
- [TickerPlugin](./app.TickerPlugin.md): Middleware for Application's {@link Ticker} functionality.

## assets

- [Overview](./assets.md): Learn how to load, cache, and manage assets in PixiJS using the Assets API, including textures, fonts, spritesheets, and bundles with format detection and background loading.
- [Resolver](./assets-1.md): Learn how to use PixiJS's asset resolver for dynamic, multi-format asset loading with platform-aware optimizations.
- [Manifests and Bundles](./assets-2.md): Learn how to manage assets in PixiJS using manifests and bundles, and how to automate this with AssetPack.
- [Background Loader](./assets-3.md): Learn how to use the PixiJS background loader to load assets in the background, improving application responsiveness and reducing load times.
- [Compressed Textures](./assets-4.md): Learn how to use compressed textures in PixiJS for lower memory usage and faster GPU uploads.
- [SVGs](./assets-5.md): Learn how to render SVGs in PixiJS, including using them as textures or graphics, and understand their advantages and limitations.
- [Assets](./assets.Assets.md): The global Assets class is a singleton that manages loading, caching, and unloading of all resources in your PixiJS application.
- [Spritesheet](./assets.Spritesheet.md): Utility class for maintaining reference to a collection of Textures on a single Spritesheet.

## color

- [Overview](./color.md): Learn how to use the Color class in PixiJS for creating, converting, and manipulating colors across multiple formats including hex, RGB, HSL, and CSS color names.
- [Color](./color.Color.md): Color utility class for managing colors in various formats.

## environment

- [Overview](./environment.md): Learn how to configure PixiJS for different environments including browsers, Web Workers, and custom platforms using the DOMAdapter system.

## events

- [Overview](./events.md): Learn how to handle mouse, touch, and pointer input in PixiJS using the federated event system with bubbling, capturing, and delegation.
- [EventSystem](./events.EventSystem.md): The system for handling UI events in PixiJS applications.
- [FederatedEvent](./events.FederatedEvent.md): A DOM-compatible synthetic event implementation for PixiJS's event system.
- [FederatedMouseEvent](./events.FederatedMouseEvent.md): A specialized event class for mouse interactions in PixiJS applications.
- [FederatedPointerEvent](./events.FederatedPointerEvent.md): A specialized event class for pointer interactions in PixiJS applications.
- [FederatedWheelEvent](./events.FederatedWheelEvent.md): A specialized event class for wheel/scroll interactions in PixiJS applications.

## extensions

- [Overview](./extensions.md): Learn how to use the PixiJS extension system to register, remove, and create modular plugins for rendering, asset loading, and more.
- [extensions](./extensions.extensions.md): Global registration system for all PixiJS extensions.

## filters

- [Overview](./filters.md): Learn how to apply post-processing effects like blur, color adjustments, noise, displacement, and custom shaders to display objects in PixiJS.
- [AlphaFilter](./filters.AlphaFilter.md): Simplest filter - applies alpha.
- [BlurFilter](./filters.BlurFilter.md): The BlurFilter applies a Gaussian blur to an object.
- [ColorBlend](./filters.ColorBlend.md): The final color has the hue and saturation of the top color, while using the luminosity of the bottom color.
- [ColorBurnBlend](./filters.ColorBurnBlend.md): The final color is the result of inverting the bottom color, dividing the value by the top color, and inverting that value.
- [ColorDodgeBlend](./filters.ColorDodgeBlend.md): The final color is the result of dividing the bottom color by the inverse of the top color.
- [ColorMatrixFilter](./filters.ColorMatrixFilter.md): The ColorMatrixFilter class lets you apply color transformations to display objects using a 5x4 matrix.
- [DarkenBlend](./filters.DarkenBlend.md): The final color is composed of the darkest values of each color channel.
- [DifferenceBlend](./filters.DifferenceBlend.md): The final color is the result of subtracting the darker of the two colors from the lighter one.
- [DisplacementFilter](./filters.DisplacementFilter.md): A filter that applies a displacement map effect using a sprite's texture.
- [DivideBlend](./filters.DivideBlend.md): The Divide blend mode divides the RGB channel values of the bottom layer by those of the top layer.
- [ExclusionBlend](./filters.ExclusionBlend.md): The final color is similar to difference, but with less contrast.
- [HardLightBlend](./filters.HardLightBlend.md): The final color is the result of multiply if the top color is darker, or screen if the top color is lighter.
- [HardMixBlend](./filters.HardMixBlend.md): Hard defines each of the color channel values of the blend color to the RGB values of the base color.
- [LightenBlend](./filters.LightenBlend.md): The final color is composed of the lightest values of each color channel.
- [LinearBurnBlend](./filters.LinearBurnBlend.md): Looks at the color information in each channel and darkens the base color to reflect the blend color by increasing the contrast between the two.
- [LinearDodgeBlend](./filters.LinearDodgeBlend.md): Looks at the color information in each channel and brightens the base color to reflect the blend color by decreasing contrast between the two.
- [LinearLightBlend](./filters.LinearLightBlend.md): Increase or decrease brightness by burning or dodging color values, based on the blend color Available as `container.blendMode = 'linear-light'` after importing `pixi.js/advanced-blend-modes`.
- [LuminosityBlend](./filters.LuminosityBlend.md): The final color has the luminosity of the top color, while using the hue and saturation of the bottom color.
- [NegationBlend](./filters.NegationBlend.md): Implements the Negation blend mode which creates an inverted effect based on the brightness values.
- [NoiseFilter](./filters.NoiseFilter.md): A filter that adds configurable random noise to rendered content.
- [OverlayBlend](./filters.OverlayBlend.md): The final color is the result of multiply if the bottom color is darker, or screen if the bottom color is lighter.
- [PinLightBlend](./filters.PinLightBlend.md): Replaces colors based on the blend color.
- [SaturationBlend](./filters.SaturationBlend.md): The final color has the saturation of the top color, while using the hue and luminosity of the bottom color.
- [SoftLightBlend](./filters.SoftLightBlend.md): The final color is similar to hard-light, but softer.
- [SubtractBlend](./filters.SubtractBlend.md): Subtracts the blend from the base color using each color channel Available as `container.blendMode = 'subtract'` after importing `pixi.js/advanced-blend-modes`.
- [VividLightBlend](./filters.VividLightBlend.md): Darkens values darker than 50% gray and lightens those brighter than 50% gray, creating a dramatic effect.

## maths

- [Overview](./maths.md): Learn how to use PixiJS math utilities for 2D transformations, geometry, shapes, and hit testing.
- [Circle](./maths.Circle.md): The Circle object represents a circle shape in a two-dimensional coordinate system.
- [Ellipse](./maths.Ellipse.md): The Ellipse object is used to help draw graphics and can also be used to specify a hit area for containers.
- [Matrix](./maths.Matrix.md): A fast matrix for 2D transformations.
- [ObservablePoint](./maths.ObservablePoint.md): The ObservablePoint object represents a location in a two-dimensional coordinate system.
- [Point](./maths.Point.md): The Point object represents a location in a two-dimensional coordinate system, where `x` represents the position on the horizontal axis and `y` represents the position on the vertical axis.
- [Polygon](./maths.Polygon.md): A class to define a shape via user defined coordinates.
- [Rectangle](./maths.Rectangle.md): The `Rectangle` object represents a rectangular area defined by its position and dimensions.
- [RoundedRectangle](./maths.RoundedRectangle.md): The `RoundedRectangle` object represents a rectangle with rounded corners.
- [Triangle](./maths.Triangle.md): A class to define a shape of a triangle via user defined coordinates.
- [DEG_TO_RAD](./maths.DEG_TO_RAD.md): Conversion factor for converting degrees to radians.
- [PI_2](./maths.PI_2.md): Two Pi.
- [RAD_TO_DEG](./maths.RAD_TO_DEG.md): Conversion factor for converting radians to degrees.

## rendering

- [Overview](./rendering.md): Learn how PixiJS renderers draw scenes using WebGL, WebGPU, and Canvas 2D, including renderer selection, systems, and render targets.
- [Textures](./rendering-1.md): Learn how PixiJS handles textures, their lifecycle, creation, and types, and how to manage GPU resources.
- [Bounds](./rendering.Bounds.md): A representation of an axis-aligned bounding box (AABB) used for efficient collision detection and culling.
- [CanvasRenderer](./rendering.CanvasRenderer.md): The Canvas PixiJS Renderer.
- [ExtractSystem](./rendering.ExtractSystem.md): System for exporting content from a renderer.
- [GenerateTextureSystem](./rendering.GenerateTextureSystem.md): System that manages the generation of textures from display objects in the renderer.
- [Texture](./rendering.Texture.md): A texture stores the information that represents an image or part of an image.
- [WebGLRenderer](./rendering.WebGLRenderer.md): The WebGL PixiJS Renderer.
- [WebGPURenderer](./rendering.WebGPURenderer.md): The WebGPU PixiJS Renderer.
- [autoDetectRenderer](./rendering.autoDetectRenderer.md): Automatically determines the most appropriate renderer for the current environment.

## scene

- [Overview](./scene.md): Learn how to use scene objects in PixiJS, including containers, sprites, transforms, and more. This guide covers the basics of building your scene graph.
- [Container](./scene-1.md): Learn how to create and manage Containers in PixiJS, including adding/removing children, sorting, and caching as textures.
- [Cache as Texture](./scene-2.md): Learn how to use cacheAsTexture in PixiJS to optimize rendering performance by caching containers as textures. Understand its benefits, usage, and guidelines.
- [Sprite](./scene-3.md): Learn how to create and manipulate Sprites in PixiJS, including texture updates, scaling, and transformations.
- [NineSlice Sprite](./scene-4.md): Learn how to use the NineSliceSprite class in PixiJS for creating scalable UI elements with preserved corners and edges.
- [Tiling Sprite](./scene-5.md): Learn how to use the TilingSprite class in PixiJS for rendering repeating textures efficiently across a defined area.
- [Graphics](./scene-6.md): Learn how to use PixiJS Graphics to create shapes, manage graphics contexts, and optimize performance in your projects.
- [Graphics Fill](./scene-7.md): Learn how to use the fill method in PixiJS to fill shapes with colors, textures, and gradients, enhancing your graphics and text rendering.
- [Graphics Pixel Line](./scene-8.md): Learn how to use the pixelLine property in PixiJS Graphics API to create crisp, pixel-perfect lines that remain consistent under scaling and transformations.
- [Text](./scene-9.md): Learn how to use PixiJS's text rendering classes Text, BitmapText, and HTMLText.
- [Text (Canvas)](./scene-10.md): Learn how to use the Text class in PixiJS to render styled text as display objects, including dynamic updates and font loading.
- [Bitmap Text](./scene-11.md): Learn how to use BitmapText in PixiJS for high-performance text rendering with pre-generated texture atlases.
- [HTML Text](./scene-12.md): Learn how to use HTMLText in PixiJS to render styled HTML strings within your WebGL canvas, enabling complex typography and inline formatting.
- [Text Style](./scene-13.md): Learn how to use the TextStyle class in PixiJS to style text objects, including fills, strokes, shadows, and more.
- [SplitText & SplitBitmapText](./scene-14.md)
- [Mesh](./scene-15.md): Learn how to create and manipulate meshes in PixiJS v8, including custom geometry, shaders, and built-in mesh types like MeshSimple, MeshRope, and PerspectiveMesh.
- [Particle Container](./scene-16.md): Learn how to use the ParticleContainer and Particle classes in PixiJS for high-performance particle systems.
- [AnimatedSprite](./scene.AnimatedSprite.md): An AnimatedSprite is a simple way to display an animation depicted by a list of textures.
- [Container](./scene.Container.md): Container is a general-purpose display object that holds children.
- [Culler](./scene.Culler.md): The Culler class is responsible for managing and culling containers.
- [DOMContainer](./scene.DOMContainer.md): The DOMContainer object is used to render DOM elements within the PixiJS scene graph.
- [FillGradient](./scene.FillGradient.md): Class representing a gradient fill that can be used to fill shapes and text.
- [FillPattern](./scene.FillPattern.md): A class that represents a fill pattern for use in Text and Graphics fills.
- [Graphics](./scene.Graphics.md): The Graphics class is primarily used to render primitive shapes such as lines, circles and rectangles to the display, and to color and fill them.
- [GraphicsContext](./scene.GraphicsContext.md): The GraphicsContext class allows for the creation of lightweight objects that contain instructions for drawing shapes and paths.
- [MeshPlane](./scene.MeshPlane.md): A mesh that renders a texture mapped to a plane with configurable vertex density.
- [MeshRope](./scene.MeshRope.md): A specialized mesh that renders a texture along a path defined by points.
- [NineSlicePlane](./scene.NineSlicePlane.md): Please use the {@link NineSliceSprite} class instead.
- [NineSliceSprite](./scene.NineSliceSprite.md): The NineSliceSprite allows you to stretch a texture using 9-slice scaling.
- [Particle](./scene.Particle.md): Represents a single particle within a particle container.
- [ParticleContainer](./scene.ParticleContainer.md): The ParticleContainer class is a highly optimized container that can render 1000s or particles at great speed.
- [PerspectiveMesh](./scene.PerspectiveMesh.md): A perspective mesh that allows you to draw a 2d plane with perspective.
- [RenderLayer](./scene.RenderLayer.md): The RenderLayer API provides a way to control the rendering order of objects independently of their logical parent-child relationships in the scene graph.
- [Sprite](./scene.Sprite.md): The Sprite object is one of the most important objects in PixiJS.
- [TilingSprite](./scene.TilingSprite.md): A TilingSprite is a fast and efficient way to render a repeating texture across a given area.

## text

- [AbstractSplitText](./text.AbstractSplitText.md): A container that splits text into individually manipulatable segments (lines, words, and characters) for advanced text effects and animations.
- [BitmapFont](./text.BitmapFont.md): A BitmapFont object represents a particular font face, size, and style.
- [BitmapText](./scene.BitmapText.md): A BitmapText object creates text using pre-rendered bitmap fonts.
- [HTMLText](./scene.HTMLText.md): A HTMLText object creates text using HTML/CSS rendering with SVG foreignObject.
- [HTMLTextStyle](./text.HTMLTextStyle.md): A TextStyle object rendered by the HTMLTextSystem.
- [SplitBitmapText](./text.SplitBitmapText.md): A container that splits text into individually manipulatable segments (lines, words, and characters) for advanced text effects and animations.
- [SplitText](./text.SplitText.md): A container that splits text into individually manipulatable segments (lines, words, and characters) for advanced text effects and animations.
- [Text](./scene.Text.md): A powerful text rendering class that creates one or multiple lines of text using the Canvas API.
- [TextStyle](./text.TextStyle.md): A TextStyle Object contains information to decorate Text objects.

## gif

- [Overview](./gif.md): Learn how to load, display, and control animated GIFs in PixiJS using GifSource and GifSprite.
- [GifSprite](./gif.GifSprite.md): Runtime object for playing animated GIFs with advanced playback control.

## ticker

- [Overview](./ticker.md): Use the Ticker class in PixiJS to run game loops, animations, and time-based updates with priority control and FPS limiting.
- [Ticker](./ticker.Ticker.md): A Ticker class that runs an update loop that other objects listen to.

## utils

- [Overview](./utils.md): Learn about PixiJS utility functions for browser detection, device capabilities, data manipulation, and canvas operations.
- [Transform](./utils.Transform.md): The Transform class facilitates the manipulation of a 2D transformation matrix through user-friendly properties: position, scale, rotation, skew, and pivot.
- [isMobile](./utils.isMobile.md): Detects whether the device is mobile and what type of mobile device it is.
- [path](./utils.path.md): Path utilities for working with URLs and file paths in a cross-platform way.
- [isWebGLSupported](./utils.isWebGLSupported.md): Helper for checking for WebGL support in the current environment.
- [isWebGPUSupported](./utils.isWebGPUSupported.md): Helper for checking for WebGPU support in the current environment.

## migrations

- [v8 Migration Guide](./migrations.md): PixiJS v8 Migration Guide - Transitioning from PixiJS v7 to v8
- [v7 Migration Guide](./migrations-1.md): PixiJS v7 Migration Guide - Transitioning from v6 to v7
- [v6 Migration Guide](./migrations-2.md): PixiJS v6 Migration Guide - Transitioning from PixiJS v5 to v6
- [v5 Migration Guide](./migrations-3.md): PixiJS v5 Migration Guide - Transitioning from PixiJS v4 to v5

## Optional

- [BackgroundLoader](./assets.BackgroundLoader.md): The BackgroundLoader handles loading assets passively in the background to prepare them for future use.
- [Cache](./assets.Cache.md): A global cache for all assets in your PixiJS application.
- [Loader](./assets.Loader.md): The Loader is responsible for loading all assets, such as images, spritesheets, audio files, etc.
- [Resolver](./assets.Resolver.md): A class that is responsible for resolving mapping asset URLs to keys.
- [basisTranscoderUrls](./assets.basisTranscoderUrls.md): The urls for the Basis transcoder files.
- [ktxTranscoderUrls](./assets.ktxTranscoderUrls.md): The urls for the KTX transcoder library.
- [loadBasis](./assets.loadBasis.md): Loads Basis textures using a web worker.
- [loadBitmapFont](./assets.loadBitmapFont.md): Loader plugin for loading bitmap fonts.
- [loadDDS](./assets.loadDDS.md): Loads DDS textures.
- [loadJson](./assets.loadJson.md): A simple loader plugin for loading json data
- [loadKTX](./assets.loadKTX.md): Loads KTX textures.
- [loadKTX2](./assets.loadKTX2.md): Loader parser for KTX2 textures.
- [loadSvg](./assets.loadSvg.md): A loader plugin for loading SVG data as textures or graphics contexts.
- [loadTextures](./assets.loadTextures.md): A simple plugin to load our textures! This makes use of imageBitmaps where available.
- [loadTxt](./assets.loadTxt.md): A simple loader plugin for loading text data
- [loadVideoTextures](./assets.loadVideoTextures.md): A simple plugin to load video textures.
- [loadWebFont](./assets.loadWebFont.md): A loader plugin for handling web fonts
- [spritesheetAsset](./assets.spritesheetAsset.md): Asset extension for loading spritesheets
- [WorkerManager](./assets.WorkerManager.md): Manages a pool of web workers for loading ImageBitmap objects asynchronously.
- [crossOrigin](./assets.crossOrigin.md): Set cross origin based detecting the url and the crossorigin
- [setBasisTranscoderPath](./assets.setBasisTranscoderPath.md): Sets the Basis transcoder paths.
- [setKTXTranscoderPath](./assets.setKTXTranscoderPath.md): Sets the paths for the KTX transcoder library.
- [BrowserAdapter](./environment.BrowserAdapter.md): This is an implementation of the {@link Adapter} interface.
- [DOMAdapter](./environment.DOMAdapter.md): The DOMAdapter is a singleton that allows PixiJS to perform DOM operations, such as creating a canvas.
- [WebWorkerAdapter](./environment.WebWorkerAdapter.md): This is an implementation of the {@link Adapter} interface.
- [autoDetectEnvironment](./environment.autoDetectEnvironment.md)
- [loadEnvironmentExtensions](./environment.loadEnvironmentExtensions.md): Automatically detects the environment and loads the appropriate extensions.
- [EventBoundary](./events.EventBoundary.md): Event boundaries are "barriers" where events coming from an upstream scene are modified before downstream propagation.
- [EventsTicker](./events.EventsTicker.md): This class handles automatic firing of PointerEvents in the case where the pointer is stationary for too long.
- [BlurFilterPass](./filters.BlurFilterPass.md): The BlurFilterPass applies a horizontal or vertical Gaussian blur to an object.
- [Filter](./filters.Filter.md): The Filter class is the base for all filter effects used in Pixi.js As it extends a shader, it requires that a glProgram is parsed in to work with WebGL and a gpuProgram for WebGPU.
- [groupD8](./maths.groupD8.md): Implements the dihedral group D8, which is similar to [group D4]{@link http://mathworld.wolfram.com/DihedralGroupD4.html}; D8 is the same but with diagonals, and it is used for texture rotations.
- [floatEqual](./maths.floatEqual.md): The idea of a relative epsilon comparison is to find the difference between the two numbers, and see if it is less than a given epsilon.
- [isPow2](./maths.isPow2.md): Checks if a number is a power of two.
- [lineIntersection](./maths.lineIntersection.md): Computes the point where non-coincident and non-parallel Lines intersect.
- [log2](./maths.log2.md): Computes ceil of log base 2 log2
- [nextPow2](./maths.nextPow2.md): Rounds to next power of two.
- [segmentIntersection](./maths.segmentIntersection.md): Computes the point where non-coincident and non-parallel segments intersect.
- [AbstractRenderer](./rendering.AbstractRenderer.md): The base class for a PixiJS Renderer.
- [AbstractTextSystem](./rendering.AbstractTextSystem.md): Base system plugin to the renderer to manage canvas text.
- [AlphaMask](./rendering.AlphaMask.md): AlphaMask is an effect that applies a mask to a container using the alpha channel of a sprite.
- [BackgroundSystem](./rendering.BackgroundSystem.md): The background system manages the background color and alpha of the main view.
- [Batch](./rendering.Batch.md): A batch pool is used to store batches when they are not currently in use.
- [Batcher](./rendering.Batcher.md): A batcher is used to batch together objects with the same texture.
- [BatcherPipe](./rendering.BatcherPipe.md): A pipe that batches elements into batches and sends them to the renderer.
- [BatchGeometry](./rendering.BatchGeometry.md): This class represents a geometry used for batching in the rendering system.
- [BatchTextureArray](./rendering.BatchTextureArray.md): Used by the batcher to build texture batches.
- [BindGroup](./rendering.BindGroup.md): A bind group is a collection of resources that are bound together for use by a shader.
- [BindGroupSystem](./rendering.BindGroupSystem.md): This manages the WebGPU bind groups.
- [Buffer](./rendering.Buffer.md): A wrapper for a WebGPU/WebGL Buffer.
- [BufferImageSource](./rendering.BufferImageSource.md): A texture source that uses a TypedArray or ArrayBuffer as its resource.
- [BufferResource](./rendering.BufferResource.md): A resource that can be bound to a bind group and used in a shader.
- [CanvasContextSystem](./rendering.CanvasContextSystem.md): Canvas 2D context system for the CanvasRenderer.
- [CanvasFilterSystem](./rendering.CanvasFilterSystem.md): Canvas2D filter system that applies compatible filters using CSS filter strings.
- [CanvasGraphicsContextSystem](./rendering.CanvasGraphicsContextSystem.md): A system that manages the rendering of GraphicsContexts for Canvas2D.
- [CanvasLimitsSystem](./rendering.CanvasLimitsSystem.md): Basic limits for CanvasRenderer.
- [CanvasRendererTextSystem](./rendering.CanvasRendererTextSystem.md): System plugin to the renderer to manage canvas text for Canvas2D.
- [CanvasRenderTargetAdaptor](./rendering.CanvasRenderTargetAdaptor.md): Canvas adaptor for render targets.
- [CanvasRenderTargetSystem](./rendering.CanvasRenderTargetSystem.md): The Canvas adaptor for the render target system.
- [CanvasSource](./rendering.CanvasSource.md): A texture source that uses a canvas as its resource.
- [CanvasTextSystem](./rendering.CanvasTextSystem.md): System plugin to the renderer to manage canvas text for GPU renderers.
- [CanvasTextureSystem](./rendering.CanvasTextureSystem.md): Texture helper system for CanvasRenderer.
- [ColorMask](./rendering.ColorMask.md): The ColorMask effect allows you to apply a color mask to the rendering process.
- [CompressedSource](./rendering.CompressedSource.md): A texture source that uses a compressed resource, such as an array of Uint8Arrays.
- [CubeTexture](./rendering.CubeTexture.md): A cube texture that can be bound to shaders (samplerCube / texture_cube).
- [CubeTextureSource](./rendering.CubeTextureSource.md): A {@link TextureSource} that represents a cube texture (6 faces).
- [DefaultBatcher](./rendering.DefaultBatcher.md): The default batcher is used to batch quads and meshes.
- [DefaultShader](./rendering.DefaultShader.md): DefaultShader is a specialized shader class designed for batch rendering.
- [ExternalSource](./rendering.ExternalSource.md): A texture source that uses a GPU texture from an external library (e.g., Three.js).
- [FilterSystem](./rendering.FilterSystem.md): System that manages the filter pipeline
- [GCSystem](./rendering.GCSystem.md): A unified garbage collection system for managing GPU resources.
- [Geometry](./rendering.Geometry.md): A Geometry is a low-level object that represents the structure of 2D shapes in terms of vertices and attributes.
- [GlBackBufferSystem](./rendering.GlBackBufferSystem.md): For blend modes you need to know what pixels you are actually drawing to.
- [GlBufferSystem](./rendering.GlBufferSystem.md): System plugin to the renderer to manage buffers.
- [GlColorMaskSystem](./rendering.GlColorMaskSystem.md): The system that handles color masking for the WebGL.
- [GlContextSystem](./rendering.GlContextSystem.md): System plugin to the renderer to manage the context
- [GlEncoderSystem](./rendering.GlEncoderSystem.md): The system that handles encoding commands for the WebGL.
- [GlGeometrySystem](./rendering.GlGeometrySystem.md): System plugin to the renderer to manage geometry.
- [GlLimitsSystem](./rendering.GlLimitsSystem.md): The GpuLimitsSystem provides information about the capabilities and limitations of the underlying GPU.
- [GlobalUniformSystem](./rendering.GlobalUniformSystem.md): System plugin to the renderer to manage global uniforms for the renderer.
- [GlProgram](./rendering.GlProgram.md): A wrapper for a WebGL Program.
- [GlRenderTargetSystem](./rendering.GlRenderTargetSystem.md): The WebGL adaptor for the render target system.
- [GlShaderSystem](./rendering.GlShaderSystem.md): System plugin to the renderer to manage the shaders for WebGL.
- [GlStateSystem](./rendering.GlStateSystem.md): System plugin to the renderer to manage WebGL state machines
- [GlStencilSystem](./rendering.GlStencilSystem.md): This manages the stencil buffer.
- [GlTextureSystem](./rendering.GlTextureSystem.md): The system for managing textures in WebGL.
- [GlUboSystem](./rendering.GlUboSystem.md): System plugin to the renderer to manage uniform buffers.
- [GlUniformGroupSystem](./rendering.GlUniformGroupSystem.md): System plugin to the renderer to manage shaders.
- [GpuBufferSystem](./rendering.GpuBufferSystem.md): System plugin to the renderer to manage buffers.
- [GpuColorMaskSystem](./rendering.GpuColorMaskSystem.md): The system that handles color masking for the GPU.
- [GpuDeviceSystem](./rendering.GpuDeviceSystem.md): System plugin to the renderer to manage the context.
- [GpuEncoderSystem](./rendering.GpuEncoderSystem.md): The system that handles encoding commands for the GPU.
- [GpuLimitsSystem](./rendering.GpuLimitsSystem.md): The GpuLimitsSystem provides information about the capabilities and limitations of the underlying GPU.
- [GpuProgram](./rendering.GpuProgram.md): A wrapper for a WebGPU Program, specifically designed for the WebGPU renderer.
- [GpuRenderTargetSystem](./rendering.GpuRenderTargetSystem.md): The WebGL adaptor for the render target system.
- [GpuShaderSystem](./rendering.GpuShaderSystem.md): A system that manages the rendering of GpuPrograms.
- [GpuStateSystem](./rendering.GpuStateSystem.md): System plugin to the renderer to manage WebGL state machines.
- [GpuStencilSystem](./rendering.GpuStencilSystem.md): This manages the stencil buffer.
- [GpuTextureSystem](./rendering.GpuTextureSystem.md): The system that handles textures for the GPU.
- [GpuUboSystem](./rendering.GpuUboSystem.md): System plugin to the renderer to manage uniform buffers.
- [GraphicsContextSystem](./rendering.GraphicsContextSystem.md): A system that manages the rendering of GraphicsContexts.
- [HelloSystem](./rendering.HelloSystem.md): A simple system responsible for initiating the renderer.
- [HTMLTextSystem](./rendering.HTMLTextSystem.md): System plugin to the renderer to manage HTMLText
- [ImageSource](./rendering.ImageSource.md): A texture source that uses an image-like resource as its resource.
- [InstructionSet](./rendering.InstructionSet.md): A set of instructions that can be executed by the renderer.
- [MaskEffectManager](./rendering.MaskEffectManager.md): A class that manages the conversion of masks to mask effects.
- [PipelineSystem](./rendering.PipelineSystem.md): A system that creates and manages the GPU pipelines.
- [PrepareBase](./rendering.PrepareBase.md): Part of the prepare system.
- [PrepareQueue](./rendering.PrepareQueue.md): Part of the prepare system.
- [PrepareSystem](./rendering.PrepareSystem.md): The prepare system provides renderer-specific plugins for pre-rendering DisplayObjects.
- [PrepareUpload](./rendering.PrepareUpload.md): Part of the prepare system.
- [RenderableGCSystem](./rendering.RenderableGCSystem.md): The RenderableGCSystem is responsible for cleaning up GPU resources that are no longer being used.
- [RenderGroup](./rendering.RenderGroup.md): A RenderGroup is a class that is responsible for I generating a set of instructions that are used to render the root container and its children.
- [RenderTarget](./rendering.RenderTarget.md): A class that describes what the renderers are rendering to.
- [RenderTargetSystem](./rendering.RenderTargetSystem.md): A system that manages render targets.
- [RenderTexture](./rendering.RenderTexture.md): A render texture, extends `Texture`.
- [SchedulerSystem](./rendering.SchedulerSystem.md): The SchedulerSystem manages scheduled tasks with specific intervals.
- [ScissorMask](./rendering.ScissorMask.md): ScissorMask is an effect that applies a scissor mask to a container.
- [Shader](./rendering.Shader.md): The Shader class is an integral part of the PixiJS graphics pipeline.
- [State](./rendering.State.md): This is a WebGL state, and is is passed to {@link GlStateSystem}.
- [StencilMask](./rendering.StencilMask.md): A mask that uses the stencil buffer to clip the rendering of a container.
- [TextureGCSystem](./rendering.TextureGCSystem.md): System plugin to the renderer to manage texture garbage collection on the GPU, ensuring that it does not get clogged up with textures that are no longer being used.
- [TextureMatrix](./rendering.TextureMatrix.md): Class controls uv mapping from Texture normal space to BaseTexture normal space.
- [TexturePoolClass](./rendering.TexturePoolClass.md): Texture pool, used by FilterSystem and plugins.
- [TextureSource](./rendering.TextureSource.md): A TextureSource stores the information that represents an image.
- [TextureStyle](./rendering.TextureStyle.md): A texture style describes how a texture should be sampled by a shader.
- [UboSystem](./rendering.UboSystem.md): System plugin to the renderer to manage uniform buffers.
- [UniformGroup](./rendering.UniformGroup.md): Uniform group holds uniform map and some ID's for work `UniformGroup` has two modes: 1: Normal mode Normal mode will upload the uniforms with individual function calls as required.
- [VideoSource](./rendering.VideoSource.md): A texture source that uses a video as its resource.
- [ViewSystem](./rendering.ViewSystem.md): The view system manages the main canvas that is attached to the DOM.
- [BLEND_TO_NPM](./rendering.BLEND_TO_NPM.md): The map of blend modes supported by Pixi
- [DRAW_MODES](./rendering.DRAW_MODES.md)
- [SCALE_MODES](./rendering.SCALE_MODES.md): The scale modes that are supported by pixi.
- [TexturePool](./rendering.TexturePool.md): The default texture pool instance.
- [WRAP_MODES](./rendering.WRAP_MODES.md): The wrap modes that are supported by pixi.
- [fastCopy](./rendering.fastCopy.md): Copies from one ArrayBuffer to another.
- [GraphicsPath](./scene.GraphicsPath.md): The `GraphicsPath` class is designed to represent a graphical path consisting of multiple drawing instructions.
- [Mesh](./scene.Mesh.md): Base mesh class.
- [MeshGeometry](./scene.MeshGeometry.md): A geometry used to batch multiple meshes with the same texture.
- [MeshSimple](./scene.MeshSimple.md): A simplified mesh class that provides an easy way to create and manipulate textured meshes with direct vertex control.
- [NineSliceGeometry](./scene.NineSliceGeometry.md): The NineSliceGeometry class allows you to create a NineSlicePlane object.
- [PerspectivePlaneGeometry](./scene.PerspectivePlaneGeometry.md): A PerspectivePlaneGeometry allows you to draw a 2d plane with perspective.
- [PlaneGeometry](./scene.PlaneGeometry.md): The PlaneGeometry allows you to draw a 2d plane
- [RenderContainer](./scene.RenderContainer.md): A container that allows for custom rendering logic.
- [RopeGeometry](./scene.RopeGeometry.md): RopeGeometry allows you to draw a geometry across several points and then manipulate these points.
- [ShapePath](./scene.ShapePath.md): The `ShapePath` class acts as a bridge between high-level drawing commands and the lower-level `GraphicsContext` rendering engine.
- [ViewContainer](./scene.ViewContainer.md): A ViewContainer is a type of container that represents a view.
- [shapeBuilders](./scene.shapeBuilders.md): A record of shape builders, keyed by shape type.
- [styleAttributes](./scene.styleAttributes.md): A map of SVG style attributes and their default values.
- [buildGeometryFromPath](./scene.buildGeometryFromPath.md): When building a mesh, it helps to leverage the simple API we have in `GraphicsPath` as it can often be easier to define the geometry in a more human-readable way.
- [AbstractBitmapFont](./text.AbstractBitmapFont.md): An abstract representation of a bitmap font.
- [AbstractText](./scene.AbstractText.md): An abstract Text class, used by all text type in Pixi.
- [BitmapFontManager](./text.BitmapFontManager.md): The BitmapFontManager is a helper that exists to install and uninstall fonts into the cache for BitmapText objects.
- [CanvasTextMetrics](./text.CanvasTextMetrics.md): The TextMetrics object represents the measurement of a block of text with a specified style.
- [GifSource](./gif.GifSource.md): Resource provided to GifSprite instances.
- [GifAsset](./gif.GifAsset.md): Handle the loading of GIF images.
- [Pool](./utils.Pool.md): A generic class for managing a pool of items.
- [PoolGroupClass](./utils.PoolGroupClass.md): A group of pools that can be used to store objects of different types.
- [ViewableBuffer](./utils.ViewableBuffer.md): Flexible wrapper around `ArrayBuffer` that also provides typed array views on demand.
- [DATA_URI](./utils.DATA_URI.md): Regexp for data URI.
- [earcut](./utils.earcut.md): A polygon triangulation library
- [formatShader](./utils.formatShader.md): formats a shader so its more pleasant to read
- [sayHello](./utils.sayHello.md): Prints out the version and renderer information for this running instance of PixiJS.

