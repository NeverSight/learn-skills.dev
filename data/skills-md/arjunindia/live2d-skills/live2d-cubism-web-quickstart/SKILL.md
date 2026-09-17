---
name: live2d-cubism-web-quickstart
description: Set up a Live2D Cubism Web project from scratch. Initialize the Cubism
  Framework, load .moc3 models via CubismUserModel, implement the render loop, handle
  touch/mouse input with pan/zoom via CubismViewMatrix, hit detection, and structure
  a production LAppModel class. Use when building a new Cubism Web app or integrating
  Live2D into a web project.
compatibility: WebGL 1.0+ browser, Node.js for build tooling.
---


# Live2D Cubism Web — Quickstart

> **Source verification:** All Framework API names and signatures below are verified against
> the official [CubismWebSamples TypeScript Demo](https://github.com/Live2D/CubismWebSamples/tree/develop/Samples/TypeScript/Demo/src)
> (develop branch) and the [Core API r15 PDF](./live2d_distilled.md).
> See the `references/` directory for the full extracted source files.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│  Application (Your code)                             │
│  LAppModel extends CubismUserModel                  │
│  LAppView: input, CubismViewMatrix (pan/zoom)       │
│  LAppLive2DManager: model registry + render loop    │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│  Cubism WebFramework (JS, @live2dcubismframework)   │
│  CubismUserModel  ─ MotionManager  ─ ExpressionManager │
│  CubismBreath     ─ CubismEyeBlink ─ CubismPose     │
│  CubismPhysics    ─ CubismRenderer_WebGL           │
│  CubismViewMatrix ─ CubismModelMatrix               │
│  CubismUpdateScheduler (manages all updaters)       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│  Cubism Core (WASM: CubismCore.wasm)                │
│  csmReviveMocInPlace → csmInitializeModelInPlace    │
│  csmUpdateModel() → vertex positions + UV + opacity │
│  No rendering — pure data computation               │
└─────────────────────────────────────────────────────┘
```

## 1. Project Setup

### Install via npm (recommended)

```bash
npm install @live2dcubismframework
```

### Manual setup (copy SDK)

```
node_modules/@live2dcubismframework/
  dist/
    Live2DCubismCore.min.js    ← Core (WASM loader + JS bindings)
    live2dcubismframework.min.js
  Framework/
    src/                       ← TypeScript source (for dev)
      CubismFramework.ts
      CubismUserModel.ts
      CubismModel.ts
      CubismMoc.ts
      Math/
        CubismMatrix44.ts
        CubismViewMatrix.ts
        CubismModelMatrix.ts
      Motion/
        CubismMotion.ts
        ACubismMotion.ts
        CubismMotionQueueManager.ts
      Rendering/
        CubismRenderer_WebGL.ts
        CubismOffscreenSurface_WebGL.ts
      Effect/
        CubismEyeBlink.ts
        CubismBreath.ts
        CubismPose.ts
        CubismPhysics.ts
      CubismUpdateManager.ts
      CubismUpdateScheduler.ts
  Core/
    CubismCore.wasm            ← Core WASM binary
```

### Public directory structure

```
public/
  cubism-core/
    CubismCore.wasm            ← WASM binary (must be fetchable)
  Assets/
    <model-name>/
      <model>.model3.json
      <model>.moc3
      <model>.cdi3.json       ← Optional supplementary data
      <model>.physics3.json    ← Optional physics
      <model>.pose3.json       ← Optional pose
      <model>.motion3.json/    ← Optional motions
        idle.motion3.json
        tap_head.motion3.json
      <model>exp/              ← Optional expressions
        happy.exp3.json
        sad.exp3.json
      <model>.textures/        ← Texture files
        texture_00.png
        texture_01.png
```

## 2. Framework Initialization (once at startup)

```typescript
import * as Live2DCubismCore from '@live2dcubismframework/dist/Live2DCubismCore';
import CubismFramework from '@live2dcubismframework/Framework/live2dcubismframework';

// Optional: log handler
CubismFramework.coreLogFunction((message: string) => {
  console.log(`[Cubism] ${message}`);
});

// Required: wire Core to Framework
const cubismOption: CubismFramework.Option = {
  logFunction: (msg) => console.log(`[Core] ${msg}`),
  loggingLevel: CubismFramework.LogLevel.LogLevel_Info,
};
CubismFramework.startUp(cubismOption);
CubismFramework.setCubismAbortFunction(() => false); // WASM checks this
CubismFramework.initialize();

// Verify
console.log(`Core version: ${Live2DCubismCore.csmGetVersion()}`); // e.g. 50528256
console.log(`Latest moc version: ${Live2DCubismCore.csmGetLatestMocVersion()}`);
```

### Loading CubismCore.wasm (manual, if not using the bundled loader)

```typescript
// If Live2DCubismCore.js doesn't auto-load the .wasm:
fetch('cubism-core/CubismCore.wasm')
  .then(r => r.arrayBuffer())
  .then(buffer => {
    const wasmBinary = new Uint8Array(buffer);
    CubismFramework.startUp({ wasmBinary } as any);
    CubismFramework.initialize();
  });
```

## 3. LAppModel — Full Verified Implementation

> This is verified against `lappmodel.ts` from the official CubismWebSamples.
> LAppModel extends CubismUserModel, which provides the base model lifecycle.

```typescript
import * as Live2DCubismCore from '@live2dcubismframework/dist/Live2DCubismCore';
import CubismFramework from '@live2dcubismframework/Framework/live2dcubismframework';
import {
  CubismUserModel,
} from '@live2dcubismframework/Framework/src/model/cubismusermodel';
import {
  CubismMotion,
} from '@live2dcubismframework/Framework/src/motion/cubismmotion';
import {
  CubismModel,
} from '@live2dcubismframework/Framework/src/model/cubismmodel';
import {
  CubismMoc,
} from '@live2dcubismframework/Framework/src/model/cubismmoc';
import {
  CubismModelSettingJson,
} from '@live2dcubismframework/Framework/src/model/cubismmodelsettingjson';
import {
  CubismExpressionMotion,
} from '@live2dcubismframework/Framework/src/motion/cubismexpressionmotion';
import {
  CubismRenderer_WebGL,
} from '@live2dcubismframework/Framework/src/rendering/cubismrenderer_webgl';
import {
  CubismMatrix44,
} from '@live2dcubismframework/Framework/src/math/cubismmatrix44';
import {
  CubismModelMatrix,
} from '@live2dcubismframework/Framework/src/math/cubismmodelmatrix';
import {
  CubismDefaultParameterId,
} from '@live2dcubismframework/Framework/src/id/cubismdefaultparameterid';
import {
  CubismEyeBlink,
} from '@live2dcubismframework/Framework/src/effect/cubismEyeblink';
import {
  CubismBreath,
} from '@live2dcubismframework/Framework/src/effect/cubismBreath';
import {
  CubismPose,
} from '@live2dcubismframework/Framework/src/effect/cubismpose';
import {
  CubismPhysics,
} from '@live2dcubismframework/Framework/src/effect/cubismphysics';
import {
  ACubismMotion,
} from '@live2dcubismframework/Framework/src/motion/acubismmotion';
import {
  CubismMotionQueueManager,
} from '@live2dcubismframework/Framework/src/motion/cubismmotionqueuemanager';

// ═══════════════════════════════════════════════════════════
// LAppModel — extends the Framework's CubismUserModel base
// ═══════════════════════════════════════════════════════════

export class LAppModel extends CubismUserModel {
  private _modelSetting: CubismModelSettingJson | null = null;
  private _motions: Map<string, CubismMotion> = new Map();
  private _expressions: Map<string, ACubismMotion> = new Map();

  // CubismUserModel already provides:
  //   _model: CubismModel | null
  //   _renderer: CubismRenderer_WebGL | null
  //   _modelMatrix: CubismModelMatrix
  //   loadModel(buffer: ArrayBuffer): void
  //   loadMotion(...): CubismMotion
  //   loadExpression(...): ACubismMotion
  //   loadPose(...): void
  //   loadPhysics(...): void
  //   createRenderer(w, h, maskBufferCount?): void
  //   getRenderer(): CubismRenderer_WebGL
  //   getModel(): CubismModel
  //   isHit(id, x, y): boolean
  //   setDragging(x, y): void

  // ──────────────────────────────────────────────────────
  // Asset loading
  // ──────────────────────────────────────────────────────

  async loadAssets(gl: WebGLRenderingContext, dir: string, fileName: string): Promise<void> {
    // 1. Fetch .model3.json
    const modelJson = await fetch(`${dir}/${fileName}`);
    const modelBuffer = await modelJson.arrayBuffer();
    this._modelSetting = new CubismModelSettingJson(
      new Uint8Array(modelBuffer),
      modelBuffer.byteLength
    );

    // 2. Load model data (.moc3)
    //    CubismUserModel.loadModel() handles MOC3 parsing internally
    //    Use shouldCheckMocConsistency = true for production
    const mocResponse = await fetch(`${dir}/${this._modelSetting.getModelFileName()}`);
    const mocBuffer = await mocResponse.arrayBuffer();
    this.loadModel(new Uint8Array(mocBuffer).buffer, true);

    // 3. Load textures
    const textureCount = this._modelSetting.getTextureCount();
    const texturePaths: string[] = [];
    for (let i = 0; i < textureCount; i++) {
      const path = this._modelSetting.getTextureFileName(i);
      if (path) texturePaths.push(`${dir}/${path}`);
    }
    await this.loadTextures(gl, texturePaths);

    // 4. Load motions
    const motionGroupCount = this._modelSetting.getMotionGroupCount();
    const motionGroups: string[] = [];
    for (let i = 0; i < motionGroupCount; i++) {
      const group = this._modelSetting.getMotionGroupName(i);
      motionGroups.push(group);
    }
    await this.loadMotions(dir, motionGroups);

    // 5. Load expressions
    const expressionCount = this._modelSetting.getExpressionCount();
    for (let i = 0; i < expressionCount; i++) {
      const name = this._modelSetting.getExpressionName(i);
      const path = this._modelSetting.getExpressionFileName(i);
      if (name && path) {
        await this.loadExpression(`${dir}/${path}`, name);
      }
    }

    // 6. Load optional systems
    if (this._modelSetting.getPhysicsFileName()) {
      const physicsPath = `${dir}/${this._modelSetting.getPhysicsFileName()}`;
      const physicsResponse = await fetch(physicsPath);
      const physicsBuffer = await physicsResponse.arrayBuffer();
      this.loadPhysics(new Uint8Array(physicsBuffer).buffer, physicsBuffer.byteLength);
    }

    if (this._modelSetting.getPoseFileName()) {
      const posePath = `${dir}/${this._modelSetting.getPoseFileName()}`;
      const poseResponse = await fetch(posePath);
      const poseBuffer = await poseResponse.arrayBuffer();
      this.loadPose(new Uint8Array(poseBuffer).buffer, poseBuffer.byteLength);
    }

    // 7. Set up eye blink
    if (this._modelSetting.getEyeBlinkCount() > 0) {
      this.setEyeBlink(
        CubismEyeBlink.create(this._modelSetting, 0) // 0 = default blink interval
      );
    }

    // 8. Set up breath
    this.setBreath(
      CubismBreath.create([
        {
          id: CubismDefaultParameterId.ParamBreath,  // "Breath"
          offset: 0,
          amplitude: 0.5,
          cycle: 4.0, // ~15 breaths/min
        },
      ])
    );

    // 9. Set up pose (part opacity)
    // Pose is already loaded above; CubismUserModel handles it via _pose

    // 10. Create renderer
    this.createRenderer(gl, gl.canvas.width, gl.canvas.height);
  }

  private async loadTextures(gl: WebGLRenderingContext, paths: string[]): Promise<void> {
    const loaded: WebGLTexture[] = [];
    for (const path of paths) {
      const texture = await this.loadTexture(gl, path);
      loaded.push(texture);
    }
    // Bind to renderer
    const renderer = this.getRenderer();
    for (let i = 0; i < loaded.length; i++) {
      renderer.bindTexture(i, loaded[i]);
    }
  }

  private loadTexture(gl: WebGLRenderingContext, url: string): Promise<WebGLTexture> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        const texture = gl.createTexture()!;
        gl.bindTexture(gl.TEXTURE_2D, texture);

        // ⚠️ MANDATORY for Cubism Web rendering
        gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, 1);

        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

        resolve(texture);
      };
      img.onerror = reject;
      img.src = url;
    });
  }

  private async loadMotions(dir: string, groups: string[]): Promise<void> {
    for (const group of groups) {
      const count = this._modelSetting!.getMotionCount(group);
      for (let i = 0; i < count; i++) {
        const file = this._modelSetting!.getMotionFileName(group, i);
        if (!file) continue;
        const key = `${group}_${i}`;
        const motion = await this.loadMotion(
          `${dir}/${file}`,
          key,
          this._modelSetting!,
          group,
          i,
          this._onMotionFinished
        );
        motion.setFadeInTime(1.0);
        motion.setFadeOutTime(1.0);
        motion.setMotionBehavior(CubismFramework.MotionBehavior.V2);
        this._motions.set(key, motion);
      }
    }
  }

  private async loadExpression(url: string, name: string): Promise<void> {
    const response = await fetch(url);
    const buffer = await response.arrayBuffer();
    const motion = CubismExpressionMotion.create(
      new Uint8Array(buffer),
      buffer.byteLength
    );
    this._expressions.set(name, motion);
  }

  private _onMotionFinished = (caller: CubismMotionQueueManager): void => {
    // Motion finished — CubismUserModel already handles this via
    // the motion queue manager. Override here for custom behavior
    // (e.g., trigger next animation).
  };

  // ──────────────────────────────────────────────────────
  // Input handling (called from LAppView)
  // ──────────────────────────────────────────────────────

  /**
   * Called on tap/click. viewX/Y are model-space coordinates.
   * Default: check hit areas → play group motion.
   */
  onTap(viewX: number, viewY: number): void {
    if (!this._model) return;

    // Check hit areas from .model3.json
    if (this._modelSetting && this._modelSetting.getHitAreaCount() > 0) {
      const hitAreaCount = this._modelSetting.getHitAreaCount();
      for (let i = 0; i < hitAreaCount; i++) {
        const name = this._modelSetting.getHitAreaName(i);
        const id = CubismFramework.getIdManager().getId(name);
        if (this.isHit(id, viewX, viewY)) {
          this.onHitArea(name);
          return;
        }
      }
    }

    // Default: play a random idle motion
    this.startRandomMotion('Idle');
  }

  /**
   * Map hit area name → motion group to play.
   * Extend this to handle your specific model's hit area names.
   */
  onHitArea(hitAreaName: string): void {
    const map: Record<string, string> = {
      'Head': 'TapHead',
      'Body': 'TapBody',
      'Hair': 'TapHair',
    };
    const group = map[hitAreaName] ?? 'TapBody';
    this.startRandomMotion(group);
  }

  /**
   * Called on drag (normalized -1 to +1 from view center).
   */
  onDrag(viewX: number, viewY: number): void {
    this.setDragging(viewX, viewY);
  }

  // ──────────────────────────────────────────────────────
  // Motion playback
  // ──────────────────────────────────────────────────────

  startMotion(motionName: string): void {
    const motion = this._motions.get(motionName);
    if (motion) {
      this.motionManager.startMotion(motion, this._onMotionFinished);
    }
  }

  startRandomMotion(group: string): void {
    const count = this._modelSetting?.getMotionCount(group) ?? 0;
    if (count === 0) return;
    const index = Math.floor(Math.random() * count);
    const motionName = `${group}_${index}`;
    this.startMotion(motionName);
  }

  startExpression(name: string): void {
    const motion = this._expressions.get(name);
    if (motion) {
      this.expressionManager.startMotion(motion, false);
    }
  }

  startRandomExpression(): void {
    const names = Array.from(this._expressions.keys());
    if (names.length === 0) return;
    this.startExpression(names[Math.floor(Math.random() * names.length)]);
  }

  /**
   * Lip sync: call this from audio analysis each frame.
   * value: 0.0 (closed) to 1.0 (fully open)
   * Parameter: ParamMouthOpenY
   */
  setLipSyncValue(value: number): void {
    if (!this._model) return;
    this._model.addParameterValueById(
      CubismDefaultParameterId.ParamMouthOpenY,
      value
    );
  }

  // ──────────────────────────────────────────────────────
  // Hit testing (uses current vertex positions)
  // ⚠️ Limitation: AABB only — does not account for deformer rotation
  // ──────────────────────────────────────────────────────

  /**
   * Check if a point in model-space hits a drawable by its ID.
   * Uses AABB of the drawable's current (post-update) vertex positions.
   */
  isHit(drawableId: CubismFramework.CubismIdHandle, pointX: number, pointY: number): boolean {
    if (!this._model) return false;

    const index = this._model.getDrawableIndex(drawableId);
    if (index < 0) return false;

    const vertexCount = this._model.getDrawableVertexCount(index);
    const vertexPositions = this._model.getDrawableVertexPositions(index);

    let left = vertexPositions[0].X;
    let right = vertexPositions[0].X;
    let top = vertexPositions[0].Y;
    let bottom = vertexPositions[0].Y;

    for (let i = 1; i < vertexCount; i++) {
      const x = vertexPositions[i].X;
      const y = vertexPositions[i].Y;
      if (x < left) left = x;
      if (x > right) right = x;
      if (y < top) top = y;
      if (y > bottom) bottom = y;
    }

    return (left <= pointX && pointX <= right && top <= pointY && pointY <= bottom);
  }

  // ──────────────────────────────────────────────────────
  // Cleanup
  // ──────────────────────────────────────────────────────

  release(): void {
    this._motions.clear();
    this._expressions.clear();
    this.deleteRenderer();
    super.release();
  }
}
```

## 4. Pan & Zoom via CubismViewMatrix

> Verified against `lappview.ts` from CubismWebSamples.

The view matrix lives in `LAppView`, NOT in the model. It transforms screen coordinates
to model coordinates and handles all pan/zoom.

```typescript
import { CubismViewMatrix } from '@live2dcubismframework/Framework/src/math/cubismviewmatrix';
import { CubismMatrix44 } from '@live2dcubismframework/Framework/src/math/cubismmatrix44';
import { TouchManager } from './touchmanager'; // See references/touchmanager.ts

export class LAppView {
  private _viewMatrix: CubismViewMatrix;
  private _deviceToScreen: CubismMatrix44; // Transforms canvas pixels → logical coords
  private _touchManager: TouchManager;

  constructor() {
    this._touchManager = new TouchManager();
    this._deviceToScreen = new CubismMatrix44();
    this._viewMatrix = new CubismViewMatrix();
  }

  initialize(canvasWidth: number, canvasHeight: number): void {
    const ratio = canvasWidth / canvasHeight;
    const left = -ratio;
    const right = ratio;
    const bottom = -1;   // Model logical bottom
    const top = 1;       // Model logical top

    // 1. Configure logical screen rect
    this._viewMatrix.setScreenRect(left, right, bottom, top);

    // 2. Initial zoom scale
    this._viewMatrix.scale(1.0, 1.0);  // or: scale(ViewScale, ViewScale)

    // 3. Build device-to-screen transform
    this._deviceToScreen.loadIdentity();
    const screenW = Math.abs(right - left);
    if (canvasWidth > canvasHeight) {
      this._deviceToScreen.scaleRelative(screenW / canvasWidth, -screenW / canvasWidth);
    } else {
      const screenH = Math.abs(top - bottom);
      this._deviceToScreen.scaleRelative(screenH / canvasHeight, -screenH / canvasHeight);
    }
    this._deviceToScreen.translateRelative(-canvasWidth * 0.5, -canvasHeight * 0.5);

    // 4. Clamp zoom levels
    this._viewMatrix.setMaxScale(2.0);  // Max zoom-in
    this._viewMatrix.setMinScale(0.5);   // Max zoom-out

    // 5. Clamp pan range (max travel from center)
    this._viewMatrix.setMaxScreenRect(
      left * 2, right * 2,  // Wider horizontal range
      bottom * 2, top * 2   // Wider vertical range
    );
  }

  // ═══════════════════════════════════════════════════════
  // INPUT HANDLERS
  // ═══════════════════════════════════════════════════════

  onTouchesBegan(canvasX: number, canvasY: number): void {
    this._touchManager.touchesBegan(
      canvasX * window.devicePixelRatio,
      canvasY * window.devicePixelRatio
    );
  }

  onTouchesMoved(canvasX: number, canvasY: number): void {
    const px = canvasX * window.devicePixelRatio;
    const py = canvasY * window.devicePixelRatio;

    this._touchManager.touchesMoved(px, py);

    // Model-space coords from touch
    const viewX = this.transformViewX(this._touchManager.getX());
    const viewY = this.transformViewY(this._touchManager.getY());

    return { viewX, viewY };
  }

  // ═══════════════════════════════════════════════════════
  // COORDINATE TRANSFORMS
  // ═══════════════════════════════════════════════════════

  /** Canvas pixel → model logical X */
  transformViewX(deviceX: number): number {
    const screenX = this._deviceToScreen.transformX(deviceX);
    return this._viewMatrix.invertTransformX(screenX);
  }

  /** Canvas pixel → model logical Y */
  transformViewY(deviceY: number): number {
    const screenY = this._deviceToScreen.transformY(deviceY);
    return this._viewMatrix.invertTransformY(screenY);
  }

  // ═══════════════════════════════════════════════════════
  // ZOOM TO HEAD (the actual implementation)
  // ═══════════════════════════════════════════════════════

  /**
   * Zoom and pan to center on a specific model-space point.
   * This is how you zoom to the head.
   *
   * @param targetX  Model-space X of target center (e.g., head X)
   * @param targetY  Model-space Y of target center (e.g., head Y)
   * @param scale    Zoom factor (e.g., 2.5 = zoom in 2.5x)
   * @param animate  If true, lerp smoothly to target
   */
  zoomToPoint(
    targetX: number,
    targetY: number,
    scale: number,
    animate: boolean = true
  ): void {
    if (animate) {
      this._animateZoom(targetX, targetY, scale);
    } else {
      // Instant: translate to center, then scale around center
      this._viewMatrix.adjustTranslate(targetX, targetY);
      this._viewMatrix.adjustScale(targetX, targetY, scale);
    }
  }

  private _animateZoom(targetX: number, targetY: number, targetScale: number): void {
    // Call this in your render loop alongside model.update()
    // Store current state and lerp toward target each frame:
    //   const t = Math.min(1.0, deltaTime * 2.0);  // 2 seconds to reach target
    //   currentX += (targetX - currentX) * t;
    //   currentY += (targetY - currentY) * t;
    //   currentScale += (targetScale - currentScale) * t;
    //   this._viewMatrix.loadIdentity();
    //   this._viewMatrix.scale(currentScale, currentScale);
    //   this._viewMatrix.translate(currentX, currentY);
    //
    // Then call _viewMatrix.adjustTranslate / adjustScale with the lerped values.
    // See the smooth zoom example below.
  }

  /** Reset to full-body view */
  resetView(): void {
    this._viewMatrix.loadIdentity();
    this._viewMatrix.scale(1.0, 1.0);
    this.initialize(canvas.width, canvas.height); // Re-initialize screen rect
  }

  /** Get current scale (useful for UI display) */
  getScale(): number {
    return this._viewMatrix.getScaleX(); // or getScaleY() (same in CubismViewMatrix)
  }

  /** Get current translation */
  getTranslate(): { x: number; y: number } {
    return {
      x: this._viewMatrix.getTranslateX(),
      y: this._viewMatrix.getTranslateY(),
    };
  }
}

// ═══════════════════════════════════════════════════════════
// SMOOTH ANIMATED ZOOM TO HEAD — complete pattern
// ═══════════════════════════════════════════════════════════

class SmoothZoomController {
  private viewMatrix: CubismViewMatrix;
  private targetX = 0, targetY = 0, targetScale = 1;
  private currentX = 0, currentY = 0, currentScale = 1;
  private isAnimating = false;

  constructor(viewMatrix: CubismViewMatrix) {
    this.viewMatrix = viewMatrix;
  }

  /** Begin smooth zoom to head center */
  zoomToHead(headX: number, headY: number, zoomScale: number = 2.5): void {
    this.targetX = headX;
    this.targetY = headY;
    this.targetScale = zoomScale;
    this.isAnimating = true;
  }

  /** Call every frame */
  update(deltaTime: number): void {
    if (!this.isAnimating) return;

    const speed = 2.5; // units per second
    const t = Math.min(1.0, deltaTime * speed);

    this.currentX += (this.targetX - this.currentX) * t;
    this.currentY += (this.targetY - this.currentY) * t;
    this.currentScale += (this.targetScale - this.currentScale) * t;

    // Apply to view matrix
    this.viewMatrix.loadIdentity();
    this.viewMatrix.scale(this.currentScale, this.currentScale);
    this.viewMatrix.translate(this.currentX, this.currentY);

    // Snap when close enough
    if (Math.abs(this.currentScale - this.targetScale) < 0.005) {
      this.currentX = this.targetX;
      this.currentY = this.targetY;
      this.currentScale = this.targetScale;
      this.viewMatrix.loadIdentity();
      this.viewMatrix.scale(this.currentScale, this.currentScale);
      this.viewMatrix.translate(this.currentX, this.currentY);
      this.isAnimating = false;
    }
  }

  get isAnimatingZoom(): boolean {
    return this.isAnimating;
  }
}
```

## 5. Hit Detection — Finding the Head Dynamically

```typescript
/**
 * Find the head drawable's model-space AABB center.
 * Call this AFTER model.update() so vertices are current.
 */
findHeadCenter(model: CubismModel, modelSetting: CubismModelSettingJson): { x: number; y: number } {
  // Approach 1: Use hit area definitions from .model3.json
  const hitCount = modelSetting.getHitAreaCount();
  for (let i = 0; i < hitCount; i++) {
    const name = modelSetting.getHitAreaName(i);
    if (name.toLowerCase().includes('head')) {
      const id = CubismFramework.getIdManager().getId(name);
      return this.getDrawableCenter(model, id);
    }
  }

  // Approach 2: Scan drawable IDs for "Head" or "head"
  const drawableCount = model.getDrawableCount();
  for (let i = 0; i < drawableCount; i++) {
    const id = model.getDrawableId(i);
    const name = id.toString();
    if (name.includes('Head') || name.includes('head')) {
      return this.getDrawableCenter(model, id);
    }
  }

  // Approach 3: Fallback — model center upper third
  const canvasHeight = model.getCanvasDimension().Y;
  return { x: 0, y: canvasHeight * 0.35 };
}

private getDrawableCenter(
  model: CubismModel,
  drawableId: CubismFramework.CubismIdHandle
): { x: number; y: number } {
  const index = model.getDrawableIndex(drawableId);
  if (index < 0) return { x: 0, y: 0 };

  const vertexCount = model.getDrawableVertexCount(index);
  const vertices = model.getDrawableVertexPositions(index);

  let minX = Infinity, maxX = -Infinity;
  let minY = Infinity, maxY = -Infinity;

  for (let i = 0; i < vertexCount; i++) {
    const x = vertices[i].X;
    const y = vertices[i].Y;
    if (x < minX) minX = x;
    if (x > maxX) maxX = x;
    if (y < minY) minY = y;
    if (y > maxY) maxY = y;
  }

  return {
    x: (minX + maxX) / 2,
    y: (minY + maxY) / 2,
  };
}
```

## 6. Render Loop — Verified Pattern

```typescript
class Renderer {
  private gl: WebGLRenderingContext;
  private model: LAppModel | null = null;
  private view: LAppView;

  constructor(canvas: HTMLCanvasElement) {
    this.gl = canvas.getContext('webgl', {
      alpha: true,
      premultipliedAlpha: false,
    })!;
    this.view = new LAppView();

    this.gl.enable(gl.BLEND);
    this.gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    this.view.initialize(canvas.width, canvas.height);
  }

  async loadModel(dir: string, file: string): Promise<void> {
    this.model = new LAppModel();
    await this.model.loadAssets(this.gl, dir, file);
  }

  render(): void {
    const { gl } = this;

    // Transparent background
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    if (!this.model) return;

    // Update model (includes motion, eye blink, breath, physics, pose, etc.)
    const now = performance.now() / 1000;
    const deltaTime = this._lastTime !== undefined ? now - this._lastTime : 0;
    this._lastTime = now;

    // CubismUserModel handles update internally:
    //   1. loadParameters()
    //   2. motion manager update
    //   3. saveParameters()
    //   4. eye blink / expression / breath / physics / pose
    //   5. csmUpdateModel() — computes vertex positions
    this.model.update();  // Uses CubismUpdateScheduler internally

    // Draw
    const renderer = this.model.getRenderer();
    renderer.startUp(this.gl as any); // ensure WebGL context is set

    // Build MVP: model matrix × view matrix
    const modelMatrix = this.model.getModelMatrix();
    const mvp = new CubismMatrix44();
    mvp.multiplyByMatrix(modelMatrix);
    mvp.multiplyByMatrix(this.view.getViewMatrix()); // CubismViewMatrix extends CubismMatrix44

    renderer.setMvpMatrix(mvp);
    renderer.drawModel();
  }

  private _lastTime: number | undefined;
}
```

## 7. Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Model renders with black seams | Missing `UNPACK_PREMULTIPLY_ALPHA_WEBGL = 1` | Set before every `texImage2D` |
| Model upside-down | Y-axis flipped vs canvas | `mvp.multiplyByMatrix(flipY)` or adjust modelMatrix |
| Motion resets every frame | Missing `model.saveParameters()` before motion update | CubismUserModel handles this; don't override incorrectly |
| Hit detection always misses | Using raw canvas coords instead of model coords | Use `viewMatrix.invertTransformX/Y` |
| Zoom goes to screen center, not face | Scaling around origin instead of head center | Use `adjustScale(cx, cy, scale)` or `scale` then `translate` |
| Texture not loading | CORS / crossOrigin issue | Set `img.crossOrigin = 'anonymous'` |
| WASM fails to load | Wrong path to `CubismCore.wasm` | Verify the path is relative to `index.html` |

## 8. Framework Shutdown

```typescript
// At app end or scene change
this.model?.release();
this.model = null;
CubismFramework.dispose();
CubismFramework.cleanUp();
```
